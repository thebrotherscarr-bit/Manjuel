"""Parity: measure the local chain against a reference answer.

The question this exists to answer is whether the machinery is worth its cost.
By default the reference runs the SAME MODEL the seats run, as a single bare
call -- so the comparison is the whole chain (Steward, Router, tools, rack,
drift, closing Steward) against just asking the model. Several calls versus
one. If the chain does not change the answer, it is not earning what it costs.

Point `**Model:**` at a larger local model instead and the question changes to
"where does the small model fall short", which is the one worth asking once
the machinery has proved itself.

Method: run each case through the local chain, run the same case through `ant`
against a large model, embed both with the embedder already on this machine,
and take the cosine. Same operation the drift check already performs -- no new
dependency, no new concept, and the embedder is free.

WHAT THE SCORE IS, AND IS NOT

A cosine between two answers measures whether they are ABOUT THE SAME THING.
It is not a correctness score and must never be read as one. Two answers can
agree closely and both be wrong. A low score is a flag to go and READ the
pair, never a verdict on either. An embedding cannot know a fact.

AND THE DIRECTION OF THE READING DEPENDS ON THE REFERENCE:

  Same model as the seats (the default). HIGH means the chain produced roughly
  what a bare call produced -- the machinery changed nothing, and on that case
  it is overhead. LOW means the chain diverged: go and read whether it diverged
  into something better or something worse.

  Larger model. HIGH means the small seats kept up. LOW means they fell short.

The same number means opposite things in those two cases, so a run that mixes
reference models cannot be averaged into one verdict. The report groups them.

Cases live in `parity.md`, because the ground is markdown.

A SECOND SET, ON A HOSTED ROUTE (2026-10-02, the operator: "set up a second set for parity, why not?
I'm not scared of it"). A case may carry `- **Set:** hosted` and a `**Model:**` of the form
`route://model`. The default run is the cases with NO set, and none of those leaves the machine; a
set runs only when it is NAMED (`/parity hosted`), `preamble` says first exactly what will leave, and
the report says afterwards what did. This module opens no connection and imports nothing that could:
a hosted reference goes through routes.py alone, which is off until its key is in `.env`.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from pathlib import Path

from . import mathkit
from . import routes
from .registry import Agent

# Below this, the two answers are not really discussing the same thing and the
# pair is worth reading. Deliberately lower than the drift floor: two models
# answering freely differ more than one model paraphrasing a source.
CLOSE = 0.75
FAR = 0.55

# The reference a case gets when it names none. NOT a statement about what
# the seats run -- it was used as one until sitting 81 and printed the
# reading backwards for two years' worth of rack changes. render() reads the
# live seat map instead. The comment here used to say "a model clearly above
# the local seats", which contradicted this module's own docstring four
# lines from the top; the docstring is right and this is the default, no
# more than that.
DEFAULT_REFERENCE_MODEL = "llama3.2:latest"
MIN_SCORABLE_CHARS = 40
_GROUND = Path(__file__).resolve().parent.parent

_CASE_RE = re.compile(
    r"^##[ \t]+Case:[ \t]*(?P<name>.+?)[ \t]*$(?P<body>.*?)(?=^##[ \t]+Case:|\Z)",
    re.MULTILINE | re.DOTALL)
_FIELD_RE = re.compile(r"^-[ \t]+\*\*(?P<key>[^*]+?):?\*\*:?[ \t]*(?P<val>.*)$",
                       re.MULTILINE)


class ParityError(Exception):
    pass


@dataclass(frozen=True)
class Case:
    name: str
    objective: str
    feed: str = ""
    model: str = DEFAULT_REFERENCE_MODEL
    expect: str = ""       # "refusal" -> the chain SHOULD refuse this one
    set_name: str = ""     # "" = the default set, which never leaves the machine; "hosted" = a named set


@dataclass
class Outcome:
    case: str
    model: str = ""
    refused_as_designed: bool = False
    score: float | None = None
    local: str = ""
    reference: str = ""
    seconds: float = 0.0
    tokens: int = 0
    error: str = ""
    route: str = ""                  # the route this reference was asked of; "" = the rack's
    remote: bool = False             # True when that call LEFT THE MACHINE (read off the address)
    sent_chars: int = 0              # what was sent, in characters
    billed_in: int | None = None     # tokens as the provider counted them
    billed_out: int | None = None

    @property
    def verdict(self) -> str:
        if self.refused_as_designed:
            return "refused ✓"
        if self.error:
            return "ERROR"
        if self.score is None:
            return "unscored"
        if self.score >= CLOSE:
            return "close"
        return "far" if self.score < FAR else "loose"

    def line(self) -> str:
        if self.refused_as_designed:
            return (f"  {self.case:28}   n/a  refused ✓ {self.seconds:5.1f}s  "
                    f"(the gate held, as designed)")
        if self.error:
            return f"  {self.case:28} ERROR  {self.seconds:5.1f}s  {self.error[:60]}"
        score = "  n/a" if self.score is None else f"{self.score:5.2f}"
        return (f"  {self.case:28} {score}  {self.verdict:8} "
                f"{self.seconds:5.1f}s  {self.tokens} words"
                + (f"  via {self.route}" + ("" if self.remote else " (this machine)")
                   if self.route else ""))


@dataclass
class Report:
    outcomes: list[Outcome] = field(default_factory=list)

    @property
    def scored(self) -> list[Outcome]:
        return [o for o in self.outcomes if o.score is not None]

    @property
    def mean(self) -> float | None:
        s = self.scored
        return sum(o.score for o in s) / len(s) if s else None

    @property
    def tokens(self) -> int:
        return sum(o.tokens for o in self.outcomes)

    @property
    def by_reference(self) -> dict:
        groups: dict[str, list] = {}
        for o in self.scored:
            groups.setdefault(o.model, []).append(o)
        return groups

    def stamp(self, ground, seats: dict | None = None) -> bool:
        """Append this run to sessions/parity_history.jsonl.

        Parity has always MEASURED and never REMEMBERED, so nobody could
        see whether quality moved when the seats did -- and the seats have
        moved a great deal (llama3.2 to phi4-mini across eleven of them,
        the Router to a thinking model, the embedder to v2-moe). A mean
        without a history is a number; a mean beside the seats that
        produced it, over time, is evidence.

        Append-only, one line per run (LAW 1: fold, never delete). Never
        raises: a measurement must not fail the thing it measures.
        """
        import json
        import time
        from pathlib import Path as _P
        try:
            row = {
                "at": time.time(),
                "mean": round(self.mean, 4) if self.mean is not None else None,
                "cases": len(self.outcomes),
                "scored": len(self.scored),
                "tokens": self.tokens,
                "by_reference": {m: round(sum(o.score for o in g) / len(g), 4)
                                 for m, g in self.by_reference.items()},
                "verdicts": {v: sum(1 for o in self.outcomes if o.verdict == v)
                             for v in {o.verdict for o in self.outcomes}},
                "seats": dict(seats or {}),
            }
            left = [o for o in self.outcomes if o.route and o.remote]
            if left:
                # WHAT LEFT THE MACHINE is part of the history, so a later reader can see which
                # runs asked a hosted route and how much they sent (2026-10-02).
                row["left_the_machine"] = {"calls": len(left),
                                           "routes": sorted({o.route for o in left}),
                                           "sent_chars": sum(o.sent_chars for o in left)}
            p = _P(ground) / "sessions" / "parity_history.jsonl"
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open("a", encoding="utf-8", newline="\r\n") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            return True
        except Exception:
            return False

    def where(self) -> str:
        """Where the references were produced, said plainly. All on the rack is the old sentence. A call to
        another machine is named as having LEFT THE MACHINE, with what was sent and what the provider
        counted; a call to a route on THIS machine is named as that, and nothing is said to have left."""
        called = [o for o in self.outcomes if o.route]
        if not called:
            return f"  reference produced {self.tokens} words, all of it on this machine"
        left = [o for o in called if o.remote]
        here = [o for o in called if not o.remote]
        said = f"  reference produced {self.tokens} words"
        if left:
            tin = sum(o.billed_in or 0 for o in left)
            tout = sum(o.billed_out or 0 for o in left)
            names = ", ".join(sorted({o.route for o in left}))
            said += (f"; {len(left)} of {len(self.outcomes)} reference call(s) LEFT THIS MACHINE (via {names}): "
                     f"{sum(o.sent_chars for o in left)} characters sent, {tin} tokens in and {tout} out as "
                     f"the provider counted them. The provider bills the operator for them")
        if here:
            names = ", ".join(sorted({o.route for o in here}))
            said += f"; {len(here)} went through a route on this machine (via {names}), and nothing left"
        return said + "."

    def render(self, seats: dict | None = None) -> str:
        """The report. `seats` is what the seats ACTUALLY run, this run.

        SITTING 81, and it inverted the answer to the question the operator
        had just asked. The reading of a score depends entirely on whether
        the reference IS the seats' model (HIGH = the chain changed nothing)
        or a different one (LOW = the seats fell short) -- this module's own
        docstring says so. The test for which was `model ==
        DEFAULT_REFERENCE_MODEL`, a CONSTANT that still said llama3.2 from
        when llama3.2 was the spine. The seats run phi4-mini now, so:

            llama3.2  0.82  labelled "same model as the seats"
                            -- it is named by nothing on the rack
            phi4-mini 0.53  labelled "the seats fell short"
                            -- it IS the seats' model, so LOW means the
                               chain DIVERGED from a bare call

        Both backwards, on the two models that mattered. stamp() already
        receives the real seat map; render() did not, and inferred instead
        of reading. It reads now, and says plainly when it was given
        nothing to read rather than guessing from a constant.
        """
        out = ["", "  case                         score  verdict    time  words", ""]
        out += [o.line() for o in self.outcomes]
        out.append("")
        if not self.scored:
            out.append("  nothing scored.")
        for model, group in sorted(self.by_reference.items()):
            mean = sum(o.score for o in group) / len(group)
            low = min(group, key=lambda o: o.score)
            out.append(f"  vs {model}: mean {mean:.2f} over {len(group)}; "
                       f"furthest is {low.case} at {low.score:.2f}")
            running = set((seats or {}).values())
            if not running:
                out.append("    (no seat map given, so which reading applies "
                           "is UNKNOWN -- see the module docstring)")
            elif model in running:
                n = sum(1 for m in (seats or {}).values() if m == model)
                out.append(f"    (this IS the seats' own model, on {n} of "
                           f"{len(seats)} seats: HIGH means the chain changed "
                           f"nothing and is overhead on that case; LOW means "
                           f"it diverged -- go read the pair)")
            else:
                out.append("    (a DIFFERENT model from the seats: HIGH means "
                           "the seats kept up with it, LOW means they fell "
                           "short of it. It is not evidence about the chain.)")
        out.append(self.where())
        out.append("")
        out.append("  A score is topical agreement, NOT correctness. Read the")
        out.append("  low pairs before concluding anything about either answer.")
        out.append("")
        return "\n".join(out)


def load_cases(path: Path) -> list[Case]:
    """Parse `parity.md`. Same markdown-is-the-source rule as everything else."""
    text = Path(path).read_text(encoding="utf-8") if Path(path).exists() else ""
    if not text.strip():
        raise ParityError(f"{path} has no cases in it")

    cases: list[Case] = []
    for m in _CASE_RE.finditer(text):
        fields = {k.strip().lower(): v.strip()
                  for k, v in _FIELD_RE.findall(m.group("body"))}
        objective = fields.get("objective", "").strip()
        if not objective:
            raise ParityError(f"case '{m.group('name')}' has no **Objective:**")
        cases.append(Case(name=m.group("name").strip(),
                          objective=objective,
                          feed=fields.get("feed", ""),
                          model=fields.get("model") or DEFAULT_REFERENCE_MODEL,
                          expect=fields.get("expect", "").strip().lower(),
                          set_name=fields.get("set", "").strip().lower()))
    if not cases:
        raise ParityError(f"{path} declares no `## Case:` blocks")
    return cases


def compare(local: str, reference: str, embed) -> float | None:
    """Cosine between two answers, or None when either is too thin to mean it."""
    a, b = (local or "").strip(), (reference or "").strip()
    if len(a) < MIN_SCORABLE_CHARS or len(b) < MIN_SCORABLE_CHARS:
        return None
    try:
        return mathkit.cosine(embed(a), embed(b))
    except Exception:
        return None


def reference_seat(model: str) -> Agent:
    """A throwaway seat for the reference model.

    Deliberately given NO persona: the reference must answer the question, not
    perform a role. Anything else measures the prompt, not the model.
    """
    return Agent(name="Reference", model=model,
                 system_prompt="Answer the question directly and completely.",
                 stage="transform", context=8192, max_tokens=1024)


def run(cases: list[Case], answer_locally, embed, runtime, report=print, ground=None) -> Report:
    """Score each case. `answer_locally(case) -> str` runs the local chain. A case whose model is
    `route://model` is answered by that route (routes.chat, the only way anything leaves) and its
    outcome says so; every other reference is the rack's, as always. `ground` is where the routes'
    records are read from."""
    ground = Path(ground) if ground is not None else _GROUND
    rep = Report()
    for i, case in enumerate(cases, 1):
        report(f"  [{i}/{len(cases)}] {case.name}")
        started = time.time()
        out = Outcome(case=case.name, model=case.model)

        def keep(o=out, t0=started):
            # EVERY OUTCOME'S TIME IS MEASURED (2026-09-29). Only a scored case
            # set it; a refusal and a failure kept the dataclass's 0.0, which
            # is a number nobody measured.
            o.seconds = time.time() - t0
            rep.outcomes.append(o)

        try:
            out.local = answer_locally(case)
        except Exception as exc:
            if case.expect == "refusal":
                # The refusal IS the correct answer; the guard did its job.
                out.local = f"(refused: {exc})"
                out.refused_as_designed = True
                keep()
                continue
            out.error = f"local chain failed: {exc}"
            keep()
            continue
        if case.expect == "refusal":
            # It was supposed to refuse and answered instead. THAT is the
            # failure -- an unsafe feed sailed through the gate.
            out.error = "expected a refusal; the chain answered instead"
            keep()
            continue
        try:
            if routes.is_routed(case.model):
                seat = reference_seat(case.model)
                reply = routes.chat(case.model, seat.system_prompt, _prompt(case), ground=ground,
                                    max_tokens=seat.max_tokens or 1024)
                out.reference, out.route, out.remote = reply.text, reply.route, reply.remote
                out.sent_chars = reply.sent_chars
                out.billed_in, out.billed_out = reply.tokens_in, reply.tokens_out
            else:
                out.reference = runtime.chat(reference_seat(case.model), _prompt(case))
            out.tokens = len(out.reference.split())
        except Exception as exc:
            if isinstance(exc, routes.RouteFailed):
                out.route = routes.split(case.model)[0]     # the call was made: say where it went
                out.remote = exc.remote
            out.error = f"reference model failed: {exc}"
            keep()
            continue
        out.score = compare(out.local, out.reference, embed)
        keep()
    return rep


def _prompt(case: Case) -> str:
    if case.feed.strip():
        return f"{case.objective}\n\n---\n{case.feed}"
    return case.objective


def models_needed(cases: list[Case]) -> set[str]:
    """Reference tags these cases will pull onto the rack. A routed model is not the rack's and is
    never asked of it: `routes_needed` names those."""
    return {c.model for c in cases if not routes.is_routed(c.model)}


def routes_needed(cases: list[Case]) -> set[str]:
    """The hosted routes these cases will reach, by name."""
    return {routes.split(c.model)[0] for c in cases if routes.is_routed(c.model)}


def routes_off(cases: list[Case], ground=None) -> list[str]:
    """Why a run cannot start, said once per route: a route with no record, or one with no key. Empty
    when every route the cases name is declared and on. The key's NAME is said; no value is ever read
    into a message."""
    table = routes.load(ground if ground is not None else _GROUND)
    out: list[str] = []
    for name in sorted(routes_needed(cases)):
        route = table.get(name)
        if route is None:
            out.append(f"route {name!r} has no record: there is no us/route_{name}.us")
        elif not routes.enabled(route):
            out.append(f"route {name!r} is OFF: {route.key_env} is not set. Put it in .env yourself "
                       f"-- it is never printed and never typed here -- and restart.")
    return out


def sets(cases: list[Case]) -> list[str]:
    """The named sets, in the order they first appear. The default set has no name."""
    seen: list[str] = []
    for c in cases:
        if c.set_name and c.set_name not in seen:
            seen.append(c.set_name)
    return seen


def select(cases: list[Case], arg: str = "") -> tuple[list[Case], str]:
    """(the cases to run, a reason there are none). `arg` is what followed `/parity`.

    NO ARGUMENT: the default set only, the cases that never leave the machine. A FIRST WORD THAT NAMES
    A SET: that set, narrowed by the rest as a part of a case name. ANYTHING ELSE: a part of a case
    name, searched in the DEFAULT set only. A word that happens to match a hosted case's name must
    never send a case off the machine, so a set is reached by its own name or not at all."""
    words = (arg or "").strip()
    first, _, rest = words.partition(" ")
    if first.lower() in sets(cases):
        pool = [c for c in cases if c.set_name == first.lower()]
        want = rest.strip().lower()
        label = f" in the {first.lower()} set"
    else:
        pool = [c for c in cases if not c.set_name]
        want = words.lower()
        label = ""
    chosen = [c for c in pool if want in c.name.lower()] if want else pool
    if not chosen:
        return [], f"no case matching '{want or words}'{label}"
    return chosen, ""


def preamble(cases: list[Case], ground=None) -> list[str]:
    """What the operator reads BEFORE he says yes. A run with a case on another machine says what will
    leave this machine, to whom, and that the provider bills it; a run with none says nothing leaves
    (a route on this machine is named as one, and nothing is said to leave by it). The REPL prints
    exactly this, so the sentence and the behaviour cannot part."""
    ground = Path(ground) if ground is not None else _GROUND
    routed = [c for c in cases if routes.is_routed(c.model)]
    table = routes.load(ground) if routed else {}

    def leaves(case: Case) -> bool:
        route = table.get(routes.split(case.model)[0])
        return True if route is None else routes.leaves(route)     # an undeclared route is assumed to leave

    out = ["", f"  {len(cases)} case(s), each answered twice: once by the seats on THIS machine, "
               f"once by the reference it names.", ""]
    for c in cases:
        mark = ""
        if routes.is_routed(c.model):
            name = routes.split(c.model)[0]
            mark = (f"   << LEAVES THIS MACHINE via {name}" if leaves(c)
                    else f"   << a route on this machine ({name}): nothing leaves")
        out.append(f"    · {c.name:30} -> {c.model}{mark}")
    local = models_needed(cases)
    if local:
        out += ["", f"  local reference models: {', '.join(sorted(local))}"]
    leaving = [c for c in routed if leaves(c)]
    if not leaving:
        out += ["  Nothing leaves the box and nothing is billed. Costs time and VRAM —",
                "  a big reference will spill to CPU on a 16GB card and run slowly."]
        return out
    hosts = sorted({routes.host(table[r]) for r in routes_needed(leaving) if r in table}
                   or routes_needed(leaving))
    chars = sum(len(c.objective) + len(c.feed) for c in leaving)
    out += ["",
            f"  WHAT LEAVES THIS MACHINE: the objective and feed of {len(leaving)} case(s), {chars} "
            f"characters in all, sent to {', '.join(hosts)}.",
            "  Nothing else goes: not the seats' answers, not a file, not the record. The answer",
            "  comes back and is scored here.",
            "  WHAT IT COSTS: the provider bills the operator for those calls, at its own prices. The",
            "  token counts it reports are printed with the result; no price is, because a price table",
            "  is a second thing to keep true.",
            "  The route is on only because its key is in .env. Nothing prints it."]
    return out
