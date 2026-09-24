"""The capability manifest, parsed and reconciled against the code.

    python -m manjuel.us

`us/*.us` declares what a thing MAY REACH -- `wall`, `writes`, `remote`,
`lands`, `can_approve` -- rather than what it does. That is the estate's
security claim in one readable place, and until 2026-09-03 NOTHING CHECKED
IT. The manifest was indexed and retrievable, so a seat could quote it; no
code compared it to the implementation, and it had drifted badly: twenty of
thirty-five skills carried no record at all, ten of eleven seat records
named a model the seat had not run in weeks, and the two seats that
actually touch the disk both UNDERSTATED their reach.

A declaration nobody checks is a promise. LAW 5 applies to the manifest
exactly as it applies to a seat: a claim is not a fact until the record
proves it. This module is that proof.

IT REPORTS AND NEVER GATES, for audit_record.py's reason and not a weaker
one: a manifest describes a ground that the operator edits by hand, so an
assertion over it would go red because he added a skill rather than because
something broke. The STROKES gate; this informs. What it must never do is
be silently green -- a reconciler that finds nothing because it looked at
nothing is worse than no reconciler, which is why every finding names the
field, the record and the disk fact that disagree.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

US_DIR = "us"

# A record is a fenced json block. The prose around it is for people; the
# block is the declaration. Both are kept in one file on purpose -- a
# machine-readable field with no argument beside it is how a manifest
# becomes a checkbox nobody reads.
_BLOCK_RE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)

# What a git skill needs before it may leave the machine, and the three
# skills that CAN. Kept here beside the check rather than imported, because
# skills.py has no opinion about `remote` -- the gate lives in the handlers.
REMOTE_SKILLS = {"git_pull", "git_push", "rack_pull"}

# THE FIELDS THIS MODULE ACTUALLY READS off a `.us` record (2026-09-24).
#
# A manifest field nobody reconciles is a LOOSE wire in the reconciler
# ITSELF -- the declaration this module exists to check, unchecked. `lands`
# is the standing example: BUILDPATH's Layer 8 says reconcile asserts
# "`lands` is false everywhere except the operator's path", and it never
# has. Nothing said so, because nothing compared the fields declared with
# the fields read.
#
# ADDING A CHECK MEANS ADDING ITS FIELD HERE. Forget, and section 7 reports
# the field as LOOSE on the next run -- loud, and one line to fix. That is
# the deal: this set is hand-kept, and getting it wrong FAILS LOUD rather
# than quietly widening what goes unchecked.
CHECKED_FIELDS = {
    "wall", "writes", "remote", "model", "source", "can_approve",
    "may_call", "permission",
}

# Read by `load` and the finding lines rather than by a check, and carried
# deliberately: `id`/`kind` key every record, `us` is the format version,
# `_file` is this module's own. Named so they are not mistaken for unread.
BOOKKEEPING_FIELDS = {"id", "kind", "us", "_file"}


@dataclass(frozen=True)
class Finding:
    """One disagreement between a declaration and the disk.

    `where` is the file a reader should open. `field` is the thing that
    lied. Both are required: a finding that says only "router is wrong"
    sends someone hunting, and hunting is where a fix becomes a guess.
    """
    # GAP   -- on the disk and undeclared, or declared and absent
    # DRIFT -- declared, and the disk says otherwise
    # LOOSE -- declared, correct, and NOTHING READS IT (2026-09-24, his word)
    #
    # The third one is the one that stays invisible. A GAP and a DRIFT both
    # have two sides that disagree, so either side can raise them. A LOOSE
    # agrees with everything: the vocabulary is right, the spelling is right,
    # the file exists -- and the wire is dead. `agents/proofreader.md` waited
    # on `prose` from the day it was written and no check, stroke or reader
    # said so, because nothing was WRONG.
    level: str
    where: str
    field: str
    said: str
    disk: str

    def line(self) -> str:
        return (f"  {self.level:5} {self.where:28} {self.field:14} "
                f"declared {self.said!r} / disk {self.disk!r}")


def load(ground) -> tuple[list[dict], list[Finding]]:
    """Every record in us/, and every block that would not parse.

    A malformed block is NAMED, never swallowed. The whole point of this
    module is that a claim gets checked; a parser that quietly drops the
    one record it could not read would defeat it in the least visible way
    available.
    """
    root = Path(ground) / US_DIR
    records: list[dict] = []
    broken: list[Finding] = []
    if not root.is_dir():
        return records, [Finding("GAP", US_DIR, "directory", "declared", "missing")]
    for path in sorted(root.glob("*.us")):
        text = path.read_text(encoding="utf-8", errors="replace")
        blocks = _BLOCK_RE.findall(text)
        if not blocks:
            broken.append(Finding("GAP", path.name, "record", "a .us file",
                                  "no json block in it"))
            continue
        for i, raw in enumerate(blocks):
            try:
                rec = json.loads(raw)
            except ValueError as exc:
                broken.append(Finding("GAP", path.name, f"block {i + 1}",
                                      "valid json", f"{type(exc).__name__}: {exc}"))
                continue
            rec["_file"] = path.name
            records.append(rec)
    return records, broken


def reconcile(ground, registry, library, installed: set | None = None
              ) -> list[Finding]:
    """Compare every record to the thing it names. Report; change nothing.

    `installed` is the rack's model tags. It is OPTIONAL and its absence is
    REPORTED rather than passed over -- a check that silently skips is the
    failure this module exists to prevent, one level up.

    But "absent" must not be reported as "unreachable". Those are different
    facts and the module said the wrong one on the operator's own machine
    with Ollama running, because main() never asked. `rack_tags()` asks,
    and names the error when the answer is no.
    """
    from .skills import WRITING_SKILLS

    records, findings = load(ground)
    by_id = {r["id"]: r for r in records}

    skills_on_disk = set(library.keywords())
    seats_on_disk = {a.name.lower().replace(" ", "_") for a in registry.all()}

    skill_recs = {r["id"] for r in records if r.get("kind") == "skill"}
    seat_recs = {r["id"][len("seat_"):] for r in records
                 if r.get("kind") == "agent" and r["id"].startswith("seat_")}

    # --- 1. everything on disk is declared, and nothing declared is absent
    for k in sorted(skills_on_disk - skill_recs):
        findings.append(Finding("GAP", f"skills/{k}", "record", "nothing",
                                "a skill with no declared wall"))
    for k in sorted(skill_recs - skills_on_disk):
        findings.append(Finding("DRIFT", f"us/{k}", "record", "a skill",
                                "no such skill on disk"))
    for a in sorted(seats_on_disk - seat_recs):
        findings.append(Finding("GAP", f"agents/{a}", "record", "nothing",
                                "a seat with no declared permission"))
    for a in sorted(seat_recs - seats_on_disk):
        findings.append(Finding("DRIFT", f"us/seat_{a}", "record", "a seat",
                                "no such seat on disk"))

    # --- 2. the fields a machine can check ------------------------------
    for k in sorted(skills_on_disk & skill_recs):
        rec = by_id[k]
        spec = library.spec(k)

        if not str(rec.get("wall", "")).strip():
            findings.append(Finding("GAP", f"us/{k}", "wall", "", "no wall declared"))

        writes = bool(rec.get("writes"))
        if writes != (k in WRITING_SKILLS):
            findings.append(Finding("DRIFT", f"us/{k}", "writes", str(writes),
                                    str(k in WRITING_SKILLS)))

        if "remote" in rec and bool(rec["remote"]) != (k in REMOTE_SKILLS):
            findings.append(Finding("DRIFT", f"us/{k}", "remote",
                                    str(bool(rec["remote"])),
                                    str(k in REMOTE_SKILLS)))

        declared_model = rec.get("model")
        real_model = getattr(spec, "model", "") or ""
        if declared_model and declared_model != real_model:
            findings.append(Finding("DRIFT", f"us/{k}", "model",
                                    declared_model, real_model or "(none)"))

        if rec.get("source") and not (Path(ground) / rec["source"]).exists():
            findings.append(Finding("DRIFT", f"us/{k}", "source",
                                    rec["source"], "no such file"))

    # --- 3. the seats: the model, and the reach it actually holds -------
    for name in sorted(seats_on_disk & seat_recs):
        rec = by_id[f"seat_{name}"]
        seat = next(a for a in registry.all()
                    if a.name.lower().replace(" ", "_") == name)
        if rec.get("model") != seat.model:
            findings.append(Finding("DRIFT", f"us/seat_{name}", "model",
                                    str(rec.get("model")), seat.model))
        may = sorted(seat.callable_set(skills_on_disk))
        if sorted(rec.get("may_call") or []) != may:
            findings.append(Finding("DRIFT", f"us/seat_{name}", "may_call",
                                    str(len(rec.get("may_call") or [])),
                                    f"{len(may)} from May Call"))
        # A seat cleared for a WRITING skill and declaring edit: deny is the
        # exact shape that made this module necessary -- the Router said it
        # read only the workspace while holding every ground reader.
        # A PERMISSION MAY BE A MAP OR A BARE WORD. Older records wrote
        # `"edit": "deny"`; the reconciled ones write a map of path to
        # verdict. The first draft of this assumed the map and CRASHED on
        # the old manifest -- which is the one shape it most needed to
        # survive, because reporting on a stale manifest is the entire job.
        # A reconciler that dies on the input it was written to judge has
        # judged nothing.
        perm = rec.get("permission") or {}
        edits = perm.get("edit")
        if isinstance(edits, str):
            allows_edit = edits.startswith("allow")
        elif isinstance(edits, dict):
            allows_edit = any(isinstance(v, str) and v.startswith("allow")
                              for k2, v in edits.items() if k2 != "*")
        else:
            allows_edit = False
        if set(may) & WRITING_SKILLS and not allows_edit:
            findings.append(Finding("DRIFT", f"us/seat_{name}", "permission.edit",
                                    "deny", "cleared for a writing skill"))

    # --- 4. THE INVARIANT. No record, ever, may approve anything --------
    for r in records:
        if r.get("can_approve"):
            findings.append(Finding("DRIFT", f"us/{r['id']}", "can_approve",
                                    "true", "RULE 6: no agent approves"))

    # --- 6. THE FLAGS: a channel nobody feeds is a promise, not a wire ---
    #
    # The flags are a closed set (pipeline.FLAGS) for the reason HOOK_POINTS is
    # one: a seat that declares a summons the engine never raises LOOKS
    # installed and never runs, and nothing in the record distinguishes it from
    # a seat that simply was not needed today. `agents/proofreader.md` waited on
    # `prose` -- a flag nothing sets and no prompt names -- from the day it was
    # written until this check was added.
    #
    # BOTH DIRECTIONS, because they fail differently. A flag that is not in the
    # set at all is a typo or an invention. A flag that IS in the set but that
    # nothing can raise is the harder one: the vocabulary agrees and the wire is
    # still dead.
    from .pipeline import FLAGS, FLAGS_ENGINE
    from .seating import wake_flags

    known = set(FLAGS)
    # What can actually put a flag on a run: the engine's own, plus every flag
    # a seat's prompt tells a model to raise. Read off the prompts rather than
    # trusted from a list, so a seat that stops naming one is visible here.
    raisable = set(FLAGS_ENGINE)
    for a in registry.all():
        raisable |= {m.lower() for m in
                     re.findall(r"<flags>([a-z_]+)</flags>", a.system_prompt or "",
                                re.IGNORECASE)}

    for a in registry.all():
        where = f"agents/{a.name.lower().replace(' ', '_')}"
        for f in wake_flags(a):
            if f not in known:
                findings.append(Finding("DRIFT", where, "wakes on", f,
                                        "no such flag -- " + ", ".join(sorted(known))))
            elif f not in raisable:
                # LOOSE, not DRIFT (2026-09-24). Nothing here disagrees with
                # anything: the flag is in the closed set, spelled right, and
                # the seat is declared correctly. It simply never wakes. That
                # is the whole reason the third kind exists.
                findings.append(Finding("LOOSE", where, "wakes on", f,
                                        "nothing raises it: this seat never wakes"))
        # A seat's PROMPT naming a flag the engine does not know is the same
        # fault read from the other end -- it teaches a model a word that moves
        # nothing, and a raised flag that wakes nobody is noise in the record.
        for f in {m.lower() for m in
                  re.findall(r"<flags>([a-z_]+)</flags>", a.system_prompt or "",
                             re.IGNORECASE)}:
            if f not in known:
                findings.append(Finding("DRIFT", where, "prompt flag", f,
                                        "no such flag -- the seat teaches a "
                                        "word that moves nothing"))

    # --- 7. LOOSE: declared, correct, and read by nothing ----------------
    #
    # His ruling, 2026-09-24, after a review found four seams built in one
    # week -- each piece correct, proved by reversal, documented, and wired to
    # nothing. RULE 10 is why they stay invisible: the wire is never the piece
    # that was named, so it is never the piece that gets built. This is the
    # place that notices anyway.
    #
    # Two arms here; the third is the `wakes on` line in section 6 above,
    # which is the archetype and was already being found under the wrong name.
    #
    # WHAT THIS IS NOT: general dead-code detection. A name in `manjuel/` that
    # nothing references is a different question, wants an exception list for
    # entry points and dynamic access, and that list would be a convention
    # doing a type's job -- the exact fault this check is for. The three known
    # cases (`can_call`, `registry.override`, `history_block`'s limit) are on
    # his TASKS list already and close by hand. What recurs here is a
    # DECLARATION nobody wired, because "add a markdown file" is how this
    # ground grows.

    # A word in the closed set that neither end uses: nothing raises it and no
    # seat waits on it. Not a typo -- vocabulary carried for a wire that was
    # never run, or that was removed and left its word behind.
    waited_on: set[str] = set()
    for a in registry.all():
        waited_on |= set(wake_flags(a))
    for f in sorted(known - (raisable | waited_on)):
        findings.append(Finding("LOOSE", "pipeline.FLAGS", "flag", f,
                                "nothing raises it and no seat waits on it"))

    # A manifest field this module never reads. The reconciler, reconciled
    # against itself: `lands` has been declared and unchecked since the
    # manifest was written, and BUILDPATH says otherwise in as many words.
    for field in sorted({k for r in records for k in r}
                        - CHECKED_FIELDS - BOOKKEEPING_FIELDS):
        carried = sorted({r["id"] for r in records if field in r})
        findings.append(Finding("LOOSE", f"{US_DIR}/*.us", field,
                                f"{len(carried)} record(s)",
                                "no check in us.reconcile reads it"))

    # --- 5. the rack, when there is one to ask --------------------------
    #
    # THE UNASKED QUESTION IS NOT AN UNREACHABLE RACK. This finding used to
    # read "not checked - no rack was reachable" whenever `installed` was
    # None -- and main() never passed it, so on the operator's own machine,
    # with Ollama running, the reconciler ASSERTED A FACT IT HAD NOT
    # CHECKED. That is precisely the class of lie this module exists to
    # catch, committed by the module itself.
    #
    # Two different states, said differently, and neither pretends to be
    # the other: nothing asked, or the rack was asked and did not answer
    # (with the error named).
    declared = {r["model"] for r in records if r.get("model")}
    if installed is None:
        findings.append(Finding("GAP", "the rack", "model tags",
                                f"{len(declared)} declared",
                                "NOT ASKED - no rack was offered to this "
                                "check; that is not the same as unreachable"))
    else:
        for tag in sorted(declared - set(installed)):
            findings.append(Finding("DRIFT", "the rack", "model", tag,
                                    "not installed"))
    return findings


def report(ground, registry, library, installed=None) -> str:
    findings = reconcile(ground, registry, library, installed)
    records, _ = load(ground)
    head = (f"the manifest: {len(records)} records in {US_DIR}/, "
            f"{len(findings)} finding(s)")
    if not findings:
        return head + "\n  the manifest agrees with the disk."
    # THREE KINDS SINCE 2026-09-24, and the tally counts all three. It read
    # "N undeclared, the rest drifted" -- so a LOOSE finding would have been
    # reported as a DRIFT in the one line most readers stop at, which is the
    # fault this check was built to name, committed by the line describing it.
    gaps = sum(1 for f in findings if f.level == "GAP")
    loose = sum(1 for f in findings if f.level == "LOOSE")
    return "\n".join([head,
                      f"  {gaps} undeclared, {len(findings) - gaps - loose} drifted, "
                      f"{loose} loose", ""]
                     + [f.line() for f in findings])


def rack_tags() -> tuple[set | None, str]:
    """What is installed on the rack, or None and the reason why not.

    ASK, DO NOT ASSUME. The reconciler's rack finding used to say "no rack
    was reachable" whenever nobody handed it a list -- and nobody ever did,
    so it said that on a machine where Ollama was running fine. A module
    that checks other people's claims does not get to make an unchecked one.
    """
    try:
        from .runtime import OllamaRuntime
        return OllamaRuntime().installed_models(), ""
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def main() -> int:
    from .registry import AgentRegistry
    from .skills import SkillLibrary
    ground = Path(__file__).resolve().parent.parent
    installed, why = rack_tags()
    out = report(ground, AgentRegistry.load(ground / "agents"),
                 SkillLibrary.load(ground / "skills"), installed)
    if installed is None:
        # Say WHICH failure, with the error, rather than leaving the
        # reconciler's generic "not asked" to stand for a real refusal.
        out += (f"\n\n  the rack could not be asked: {why}\n"
                f"  (every other check above ran; only the model tags are "
                f"unverified.)")
    print(out)
    return 0          # REPORTS, NEVER GATES.


if __name__ == "__main__":
    raise SystemExit(main())
