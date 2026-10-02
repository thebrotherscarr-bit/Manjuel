"""Sessions and the toll.

A SITTING is one REPL launch. Sittings are numbered monotonically and recorded
in `sessions/sessions.jsonl` (append-only, one line each), so a session id is
not just a timestamp but a version with an ordinal, a git stamp, and the runs
it produced.

Every sitting pays its toll: an entry in `SEAT_LOG.md` saying WHAT PROVED,
WHAT IS THIN, and WHAT IS OWED (LAW 10). The log is append-only -- entries are
added below, never rewritten above.

What the toll states as fact is only what was observed: runs, stages, models,
timings, git state. "Thin" and "owed" are judgment, so they come from the
operator, and an unattended close says so rather than inventing them.
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

from . import gitstate

SEAT_LOG = "SEAT_LOG.md"
SESSIONS = Path("sessions") / "sessions.jsonl"

HEADER = (
    "# SEAT_LOG — manjuel\n\n"
    "### The toll of every sitting. Append below; never rewrite above.\n"
    "### The full record of a sitting is its transcripts in `logs/`;\n"
    "### this is the spine, not the body.\n\n"
    "---\n"
)


@dataclass
class RunNote:
    objective: str
    pipeline: str
    stages: int
    failed: int
    elapsed: float
    transcript: str
    # THE STORY'S FIELDS (0.1.6, 2026-09-08). The ledger line is the WAL
    # -- the operator: "the WAL, and the on-turn indexing ... is just
    # building out empirical context for the agent to run on." A run's
    # tools, the guards that fired, the seats that failed or ran out of
    # time, and the first line of what was delivered are written as the
    # run ends, so the sitting story (story_block) is READ off the ledger
    # and never remembered by a seat. Older lines lack them; they read
    # as empty.
    tools: list = field(default_factory=list)
    guards: list = field(default_factory=list)
    seats_failed: list = field(default_factory=list)
    out_of_time: list = field(default_factory=list)
    delivery: str = ""


# Notes that mean a guard fired. Kept as substrings of the notes as the
# pipeline writes them (tests/standup.py keeps the same list for the same
# reason: a renamed note shows up as a miss, not as silence).
GUARD_MARKS = (
    "carried to the Router", "discarded", "recited the conversation scaffold",
    "replied with control markup", "REFUSED", "claimed the contents",
    "said it wrote", "cited", "already ran this turn", "LAW 8 gate refused",
    "recompose:", "hard gate:", "gate:", "technical flag set aside",
    "judged the work unfinished", "empty reply", "not seated", "decided by arithmetic",
    "CUT by the rack",
)


def note_for(ctx, pipeline: str, transcript: str) -> RunNote:
    """The ledger line for one run, read off its RunContext as it ends."""
    steps = list(getattr(ctx, "steps", []) or [])
    notes = list(getattr(ctx, "notes", []) or [])
    delivery = ""
    try:
        delivery = " ".join((ctx.last_output() or "").split())[:200]
    except Exception:
        pass
    return RunNote(
        objective=str(getattr(ctx, "objective", "")),
        pipeline=pipeline,
        stages=len(steps),
        failed=sum(1 for s in steps if getattr(s, "error", None)),
        elapsed=float(getattr(ctx, "elapsed", 0.0) or 0.0),
        transcript=transcript,
        tools=sorted({k for s in steps for k in (getattr(s, "tool_calls", None) or ())}),
        guards=[n[:120] for n in notes if any(m in n for m in GUARD_MARKS)][:8],
        seats_failed=[s.agent for s in steps if getattr(s, "error", None)],
        out_of_time=list(getattr(ctx, "out_of_time", []) or []),
        delivery=delivery,
    )


@dataclass
class Sitting:
    n: int
    id: str
    started: str
    ground: str = ""
    git_start: dict = field(default_factory=dict)
    runs: list = field(default_factory=list)
    ended: str = ""
    git_end: dict = field(default_factory=dict)
    toll_paid: bool = False
    # WHO IS HOLDING IT OPEN (2026-09-17). A sitting's own process can close
    # it on EOF, on Ctrl-C and on an unhandled exception -- every one of those
    # is caught. What it cannot do is close it after being KILLED, and a
    # sitting left open by a dead process is RULE 9's lock held by nothing:
    # the ground refuses edits for a hand that is not there. The pid makes the
    # question answerable by the next sitting. Optional and defaulted, so the
    # 526 lines written before this parse exactly as they did.
    pid: int = 0
    # How it closed, when it was not closed at its own prompt: "reaped" by
    # the next sitting, or the headless door's own reason -- "idle: no command
    # in 30 minutes", "closed by the client", "the client hung up" (serve.Door.
    # _close, 2026-09-29). Until then an idle close and a Dashboard Close
    # wrote the same line and the same toll, and nothing said which it was.
    closed_by: str = ""

    @property
    def label(self) -> str:
        return f"sitting {self.n} · {self.id}"


def _sessions_path(ground: Path) -> Path:
    return Path(ground) / SESSIONS


def all_sittings(ground: Path) -> list[dict]:
    p = _sessions_path(ground)
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def next_number(ground: Path) -> int:
    prior = all_sittings(ground)
    return (max((s.get("n", 0) for s in prior), default=0)) + 1


def open_sitting(ground: Path, session_id: str) -> Sitting:
    ground = Path(ground)
    st = Sitting(
        n=next_number(ground),
        id=session_id,
        started=datetime.now().isoformat(timespec="seconds"),
        ground=str(ground),
        git_start=gitstate.read(ground).as_dict(),
        pid=os.getpid(),
    )
    return st


def _alive(pid: int) -> bool:
    """Is that process still running? Every doubt answers YES.

    FAIL CLOSED, and which way that points matters. Believing a live sitting
    dead would close somebody's open sitting under them -- the worst thing in
    this file. Believing a dead one live only leaves an orphan for a hand to
    close, which is where the estate already was. So an error, a permission
    refusal, a pid we cannot ask about: all alive.

    NEVER `os.kill(pid, 0)` ON WINDOWS. CPython's os.kill there does not send
    a signal -- for anything but CTRL_C_EVENT/CTRL_BREAK_EVENT it calls
    TerminateProcess, so the portable-looking liveness probe would KILL the
    process it was asking about. ctypes asks the kernel instead.
    """
    if not pid or pid <= 0:
        return True                      # nothing to judge: leave it alone
    if os.name == "nt":
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            k = ctypes.windll.kernel32
            h = k.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
            if not h:
                return False             # no such process
            code = ctypes.c_ulong()
            ok = k.GetExitCodeProcess(h, ctypes.byref(code))
            k.CloseHandle(h)
            return (not ok) or code.value == STILL_ACTIVE
        except Exception:
            return True
    try:
        os.kill(int(pid), 0)
        return True
    except ProcessLookupError:
        return False
    except Exception:
        return True


def reap_orphans(ground: Path, report=lambda s: None) -> list[int]:
    """Close sittings whose process is gone. Returns the numbers closed.

    EARNED 2026-09-17, on the operator's ground and by this hand: a REPL run
    with its output piped into `Select-Object -First 45` was killed the moment
    the pipe closed, mid-print. Sitting 226 stood open in the ledger with no
    process behind it -- and an open line is what RULE 9 reads as "hands off,
    someone is sitting", what `tests/release.py` refuses a tag over, and what
    the door refuses a world for. A lock held by nobody.

    THE THREE WAYS A SITTING ENDS ITSELF ARE ALREADY CAUGHT: EOF and Ctrl-C at
    the prompt, and any unhandled exception (`main`'s own handler). This is the
    fourth, which cannot be caught from inside: the kill. So it is answered at
    the next open instead, which is the only moment another process is
    certainly looking.

    IT CLOSES ONLY WHAT IT CAN PROVE IS DEAD. A line with no pid -- every line
    written before today -- is never touched: this cannot tell an old orphan
    from an old close, and guessing would rewrite history it cannot read.
    A live pid is left alone, so a second REPL on the same ground never closes
    the first one's sitting.

    A REAPED SITTING THAT RAN SOMETHING STILL PAYS (LAW 10). The same two calls
    `cli._close` makes for an unattended close, so the toll cannot be skipped
    by the process dying.
    """
    ground = Path(ground)
    rows = all_sittings(ground)
    if not rows:
        return []
    latest: dict[int, dict] = {}
    for row in rows:
        n = row.get("n")
        if isinstance(n, int):
            latest[n] = row            # a closing line supersedes its opening
    closed: list[int] = []
    for n in sorted(latest):
        row = latest[n]
        if row.get("ended"):
            continue
        pid = row.get("pid") or 0
        if not pid or _alive(pid):
            continue
        st = Sitting(
            n=n, id=row.get("id", ""), started=row.get("started", ""),
            ground=row.get("ground", "") or str(ground),
            git_start=row.get("git_start") or {},
            runs=row.get("runs") or [],
            toll_paid=bool(row.get("toll_paid")),
            pid=int(pid), closed_by="reaped",
        )
        close_sitting(ground, st)
        if st.runs and not st.toll_paid:
            try:
                pay(ground, render_toll(st, attended=False))
                st.toll_paid = True
            except Exception as exc:
                report(f"  (sitting {n}'s toll was not written: {exc})")
        record(ground, st)
        closed.append(n)
        report(f"  sitting {n} was left open by a process that is gone "
               f"(pid {pid}); closed{' and tolled' if st.runs else ''}.")
    return closed


def record(ground: Path, sitting: Sitting) -> None:
    """Append/refresh the sitting's line. The ledger is append-only, so a
    closing line supersedes an opening one rather than editing it."""
    p = _sessions_path(ground)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\r\n") as f:
        f.write(json.dumps(asdict(sitting), ensure_ascii=False) + "\n")


def close_sitting(ground: Path, sitting: Sitting) -> Sitting:
    sitting.ended = datetime.now().isoformat(timespec="seconds")
    sitting.git_end = gitstate.read(ground).as_dict()
    return sitting


# ---------------------------------------------------------------------
# the standing
# ---------------------------------------------------------------------

DAYBOOK = "DAYBOOK.md"
STANDING_CHARS = 1800
_SESSION_HEAD = "\n## Session "
# The fields of a DAYBOOK entry that say what the sitting is FOR. The
# rest of an entry is what happened, and the transcripts hold that.
_STANDING_FIELDS = ("**Standing**", "**The plan**", "**Next session**")


def standing_block(ground: Path, chars: int = STANDING_CHARS) -> str:
    """What this sitting is for, from the LAST entry of DAYBOOK.md.

    CLAUDE.md READ FIRST, for the seats (the operator, 2026-09-07): the
    hand begins every turn with total amnesia and DAYBOOK's last entry is
    "the only file that carries intent". The seats begin every run the same
    way, and sitting 87's toll named the cost: "needs more context and
    reasoning intent." This is that entry's Standing, plan and next-session
    lines, bounded, labelled as RECORD -- built once at sitting open by the
    CLI and handed to the door and the court (pipeline.carried_blocks).

    Read, never generated: no model touches it, and a DAYBOOK with no
    entry yields "" and no block. Bounded on purpose -- an entry can run to
    pages, and this rides on prompts whose windows are 8192."""
    path = Path(ground) / DAYBOOK
    if not path.is_file():
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    at = text.rfind(_SESSION_HEAD)
    if at == -1:
        return ""
    entry = text[at + 1:]
    head, _, body = entry.partition("\n")
    keep: list[str] = []
    take = False
    for line in body.splitlines():
        line = line.rstrip()
        if line.startswith("**"):
            take = line.startswith(_STANDING_FIELDS)
        if take and line.strip():
            keep.append(line)
    if not keep:
        return ""
    picked = "\n".join(keep)
    if len(picked) > chars:
        picked = picked[:chars].rsplit(" ", 1)[0] + " ..."
    return ("## Standing -- what this sitting is for, from DAYBOOK.md "
            "(the record, not a model's words)\n"
            f"{head.strip()}\n{picked}")


# ---------------------------------------------------------------------
# the story
# ---------------------------------------------------------------------

STORY_CHARS = 1800


def story_block(sitting: Sitting, chars: int = STORY_CHARS) -> str:
    """What THIS sitting has done so far, read off its ledger runs.

    THE SITTING STORY (0.1.6; the operator, 2026-09-07 and 2026-09-08).
    Sitting 93: "What happened? Why did you suck so bad?" went to a
    semantic search over the whole record and came back "the operator
    doesn't have access to see previous outputs in this session." No
    seat was handed what this sitting had done -- the standing carries
    the SESSION's intent, the dialogue carries the words, and the runs
    between them were nowhere. This block is those runs: objective,
    seconds, tools, the guards that fired, seats that failed or ran out
    of time, and the first line delivered -- the WAL, bounded like a
    window. Newest last. When the runs outgrow the budget the OLDEST are
    folded into one counted line and the seat is told where the rest
    is: the transcripts in logs/, reachable by semantic_search. Read,
    never generated; a sitting with no runs yields "" and no block.

    Handed to the door and the court beside the law and the standing
    (pipeline.carried_blocks). Not the Router: it routes; it does not
    narrate the day."""
    runs = list(getattr(sitting, "runs", []) or [])
    if not runs:
        return ""
    lines: list[str] = []
    for i, r in enumerate(runs, 1):
        bits = [f"{float(r.get('elapsed') or 0):.0f}s"]
        if r.get("tools"):
            bits.append("tools: " + ", ".join(r["tools"]))
        if r.get("seats_failed"):
            bits.append("FAILED: " + ", ".join(r["seats_failed"]))
        elif r.get("failed"):
            bits.append(f"{r['failed']} stage(s) FAILED")
        if r.get("out_of_time"):
            bits.append("OUT OF TIME: " + ", ".join(r["out_of_time"]))
        line = f"{i}. {str(r.get('objective', ''))[:80]}  ({'; '.join(bits)})"
        guards = [g for g in (r.get("guards") or [])
                  if not g.startswith("law: chain whole")]
        if guards:
            line += "\n   guards: " + " | ".join(g[:80] for g in guards[:3])
        if r.get("delivery"):
            line += f"\n   -> {r['delivery'][:140]}"
        lines.append(line)
    # Fold the oldest until the newest fit the window.
    folded = 0
    while lines and sum(len(l) + 1 for l in lines) > chars and len(lines) > 1:
        lines.pop(0)
        folded += 1
    head = ("## The sitting so far -- what THIS sitting has done, from the "
            "ledger (the record, not a model's words)\n"
            f"sitting {sitting.n}, {len(runs)} run{'' if len(runs) == 1 else 's'} "
            f"since it opened at {sitting.started[11:16] if len(sitting.started) > 15 else sitting.started}. "
            "When asked what happened, answer from this and name the run.")
    if folded:
        head += (f"\n({folded} earlier run{'' if folded == 1 else 's'} folded; "
                 f"their transcripts are in logs/ and reachable by semantic_search)")
    return head + "\n" + "\n".join(lines)


# ---------------------------------------------------------------------
# the toll
# ---------------------------------------------------------------------


def summarize(sitting: Sitting) -> str:
    """The observed facts of the sitting. No judgment in here."""
    if not sitting.runs:
        return "  no runs."
    lines = []
    for i, r in enumerate(sitting.runs, 1):
        flag = f"  {r['failed']} stage(s) FAILED" if r.get("failed") else ""
        lines.append(
            f"  {i}. {r['objective'][:64]}\n"
            f"     {r['pipeline']} · {r['stages']} stages · "
            f"{r['elapsed']:.1f}s · {r['transcript']}{flag}"
        )
    return "\n".join(lines)


def render_toll(
    sitting: Sitting,
    proved: str = "",
    thin: str = "",
    owed: str = "",
    attended: bool = True,
) -> str:
    g0 = gitstate.GitState(**sitting.git_start) if sitting.git_start else gitstate.GitState()
    g1 = gitstate.GitState(**sitting.git_end) if sitting.git_end else g0

    day = (sitting.ended or sitting.started)[:10]
    title = proved.strip().splitlines()[0][:70] if proved.strip() else "a sitting"

    # A sitting may be tolled more than once: pay, run one more thing, pay
    # again (`_cmd_toll` offers it). Sitting 57 did exactly that and the two
    # entries came out byte-identical in the head, so a reader could not tell
    # a deliberate re-toll from a double write. Say which it is. The earlier
    # entry stands -- LAW 1, nothing above is rewritten.
    retoll = sitting.toll_paid

    out = [
        f"\n## {day} — sitting {sitting.n}{' (re-tolled)' if retoll else ''} — {title}",
        "",
        f"**The seat:** manjuel REPL, session `{sitting.id}`, "
        f"{sitting.started[11:16]}–{(sitting.ended or sitting.started)[11:16]}. "
        + ("Operator present." if attended else
           f"Closed unattended ({sitting.closed_by})." if sitting.closed_by else
           "Closed unattended."),
        "",
    ]
    if retoll:
        out += [
            "**A toll for this sitting already stands above.** This one is later "
            "and supersedes it; the earlier entry is kept, not corrected.",
            "",
        ]
    out += [
        f"**Version:** {g0.stamp()}",
    ]
    # WHENEVER THE STAMP MOVED (2026-09-29). This was written only when the
    # head changed or the ground went from clean to dirty or back -- so a
    # sitting that opened on 3 changed files and closed on 30, or moved to
    # another line of work at the same commit, was tolled as though nothing
    # had moved. The stamp is what a reader compares; compare the stamp.
    if g1.stamp() != g0.stamp():
        out.append(f"**At close:** {g1.stamp()}")

    out += ["", "**WHAT RAN** (observed)", "", summarize(sitting), ""]

    if proved.strip():
        out += ["**WHAT PROVED**", "", proved.strip(), ""]
    if thin.strip():
        out += ["**WHAT IS THIN**", "", thin.strip(), ""]
    if owed.strip():
        out += ["**WHAT IS OWED**", "", owed.strip(), ""]

    if not attended and not (thin.strip() or owed.strip()):
        out += [
            "**WHAT IS THIN / OWED**", "",
            "Not stated — the sitting closed without the operator paying the "
            "toll by hand. What ran above is observed; nothing here is a "
            "judgment about it.", "",
        ]
    return "\n".join(out)


def pay(ground: Path, text: str) -> Path:
    """Append the toll. Never rewrites what stands above it. Then refresh the index beside it (THE
    TOLL INDEX, below): a toll that is paid is never why the index is stale, and an index that
    cannot be written is never why a toll is not paid."""
    p = Path(ground) / SEAT_LOG
    if not p.exists():
        p.write_text(HEADER, encoding="utf-8", newline="\r\n")
    with p.open("a", encoding="utf-8", newline="\r\n") as f:
        f.write(text)
    try:
        write_index(ground)
    except Exception as exc:                     # the toll stands; say what did not follow it
        print(f"  (the toll is paid; {SEAT_LOG_INDEX} was not refreshed: {exc})", file=sys.stderr)
    return p


# THE TOLL INDEX -----------------------------------------------------------------------------------
#
# SEAT_LOG_INDEX.md, beside the log: every toll in the order it was paid, with the numbering's gaps
# and duplicates counted. Built 2026-10-01 (his ruling of 2026-09-30, WHAT'S LEFT B13). The log is
# append-only (ESTATE LAW 8) and written by more than one hand, so its sitting numbers carry gaps and
# duplicates and its order is the order of writing, and he asked for it "sorted and numbered". The log
# cannot be sorted without rewriting it, which the law forbids; this is the same tolls sorted by each
# sitting's own session timestamp, regenerated from the log so it cannot drift. The log is never
# touched.
#
# THE WIRE (2026-10-02). It began as a generator beside the suites with a stroke holding the copy
# current, and that stroke went red after EVERY sitting that paid a toll, until a hand ran the
# generator: the staleness was made at `pay` and caught at the suites, a day later (twice on the
# morning of 2026-10-02). So the wire is where the staleness is made. `pay`, the one writer of a toll,
# refreshes the index after the append: a toll that is paid is never why the index is stale, and an
# index that cannot be written is never why a toll is not paid. The stroke stays, as the reconciler
# for a log written any other way (the builder's entries are appended by hand), and
# `python tests/seatindex.py` is still the hand's way to run it. SEAT_LOG.md is untracked (his ruling
# 2026-09-08) and so is this index.

SEAT_LOG_INDEX = "SEAT_LOG_INDEX.md"

_HEAD = re.compile(r"^## (?P<title>.+)$")
_SITTING = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2}) — sitting (?P<n>\d+) — (?P<what>.*)$")
_SESSION = re.compile(r"session `S(?P<ymd>\d{8})-(?P<hms>\d{6})`")
_CLOCK = re.compile(r"(\d{2}:\d{2})[–-](\d{2}:\d{2})")


def toll_rows(text: str) -> list[dict]:
    """One row per `## ` heading in the log, in the order written."""
    rows: list[dict] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        m = _HEAD.match(line)
        if not m:
            continue
        title = m.group("title").strip()
        s = _SITTING.match(title)
        # an unnumbered toll (the builder's, an outside hand's) carries its date in the heading
        in_title = re.search(r"\d{4}-\d{2}-\d{2}", title)
        row = {"line": i, "title": title, "date": s.group("date") if s else (in_title.group(0) if in_title else ""),
               "n": int(s.group("n")) if s else None, "what": s.group("what").strip() if s else title,
               "session": "", "clock": ""}
        # the seat line follows within a few lines: the session id and the clock
        for look in lines[i:i + 6]:
            ms = _SESSION.search(look)
            if ms:
                row["session"] = f"{ms.group('ymd')[:4]}-{ms.group('ymd')[4:6]}-{ms.group('ymd')[6:]}T{ms.group('hms')[:2]}:{ms.group('hms')[2:4]}:{ms.group('hms')[4:]}"
            mc = _CLOCK.search(look)
            if mc:
                row["clock"] = f"{mc.group(1)}–{mc.group(2)}"
            if ms or mc:
                break
        rows.append(row)
    return rows


def ordered_tolls(rows: list[dict]) -> list[dict]:
    """By the session's own timestamp, then the heading's date, then the line."""
    return sorted(rows, key=lambda r: (r["session"] or r["date"] or "0000", r["date"], r["line"]))


def numbering(rows: list[dict]) -> tuple[list[int], dict[int, list[str]]]:
    """(the sitting numbers never tolled between the first and the last,
    {number: [dates]} for every number tolled more than once)."""
    seen: dict[int, list[str]] = {}
    for r in rows:
        if r["n"] is not None:
            seen.setdefault(r["n"], []).append(r["date"])
    if not seen:
        return [], {}
    lo, hi = min(seen), max(seen)
    gaps = [n for n in range(lo, hi + 1) if n not in seen]
    dups = {n: d for n, d in seen.items() if len(d) > 1}
    return gaps, dups


def index_text(text: str) -> str:
    rows = toll_rows(text)
    order = ordered_tolls(rows)
    gaps, dups = numbering(rows)
    numbered = [r for r in rows if r["n"] is not None]
    out = ["# SEAT_LOG_INDEX — every toll, in the order it was paid",
           "",
           "GENERATED from SEAT_LOG.md at every toll (manjuel/seatlog.py, `pay`) and by",
           "`python tests/seatindex.py`; never hand-edited, never a substitute for the log. The log is",
           "append-only and in the order of writing; this is the same tolls sorted by each sitting's",
           "own session timestamp, with the numbering's gaps and duplicates counted as arithmetic",
           "over the headings. `--check` refuses a stale copy.",
           "",
           f"{len(rows)} tolls ({len(numbered)} numbered sittings, {len(rows) - len(numbered)} unnumbered); "
           f"numbers {min(r['n'] for r in numbered) if numbered else '-'} to "
           f"{max(r['n'] for r in numbered) if numbered else '-'}; "
           f"{len(gaps)} number{'s' if len(gaps) != 1 else ''} never tolled; "
           f"{len(dups)} number{'s' if len(dups) != 1 else ''} tolled more than once.",
           "",
           "## In order",
           "",
           "| # | paid | sitting | what | log line |",
           "|---|---|---|---|---|"]
    for k, r in enumerate(order, 1):
        paid = (r["session"] or r["date"] or "?") + (f" ({r['clock']})" if r["clock"] else "")
        n = str(r["n"]) if r["n"] is not None else "—"
        what = r["what"].replace("|", "\\|")
        out.append(f"| {k} | {paid} | {n} | {what} | {r['line']} |")
    out += ["", "## The numbering, as arithmetic", ""]
    out.append("Never tolled: " + (", ".join(str(g) for g in gaps) if gaps else "none") + ".")
    out.append("")
    if dups:
        out.append("Tolled more than once:")
        out.append("")
        for n in sorted(dups):
            out.append(f"- {n}: " + ", ".join(dups[n]))
    else:
        out.append("Tolled more than once: none.")
    return "\n".join(out) + "\n"


def write_index(ground: Path) -> Path | None:
    """Rewrite SEAT_LOG_INDEX.md from SEAT_LOG.md, in the log's own line endings. None where there is
    no log (a fresh checkout: the record is untracked, so there is nothing to index)."""
    log = Path(ground) / SEAT_LOG
    if not log.exists():
        return None
    raw = log.read_bytes()
    new = index_text(raw.decode("utf-8", errors="replace").replace("\r\n", "\n"))
    out = Path(ground) / SEAT_LOG_INDEX
    out.write_bytes((new.replace("\n", "\r\n") if b"\r\n" in raw else new).encode("utf-8"))
    return out


def index_is_current(ground: Path) -> bool:
    """True when SEAT_LOG_INDEX.md is exactly what a regeneration would write (and where there is no
    log, there is nothing to be stale)."""
    log = Path(ground) / SEAT_LOG
    if not log.exists():
        return True
    out = Path(ground) / SEAT_LOG_INDEX
    want = index_text(log.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n"))
    have = out.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n") if out.exists() else ""
    return have == want
