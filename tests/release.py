"""THE RELEASE GATE -- may this ground be tagged? Reads; never writes.

    python tests/release.py --check          exit 0 = the tag may be cut
    python tests/release.py --check v0.1.5   name the version being cut

The operator's ask, 2026-09-08 ("the documentation within the estate gets
reviewed, updated, and logged, at all times"), and the shape from TASKS
"THE PATH TO 0.1.8": one command, run before every tag, that REFUSES BY
NAME unless every check below holds. Until today these were seven scripts
and two habits; a habit is a rule that has not failed yet.

WHAT IT READS (nothing it decides is generated -- LAW 1 for the hands):

    strokes    tests/last_run.json  -- green, finished, and stamped AFTER the
               newest edit under manjuel/ agents/ skills/ tests/ (a green
               older than the code is not a green; boot.suite_tally's rule)
    smoke      the same file, the same rule
    buildmap   tests/buildmap.py --check, run here
    standup    tests/run_history.jsonl's newest "standup" line -- LIVE (dry
               runs never write it), green, and after the newest edit
    law        law/law.py --prove, run here, exit 0
    manifest   manjuel.us.report(): 0 undeclared, 0 drifted (the rack is
               asked; if it cannot be, that one line is reported, not failed)
    spec       every SPEC.md section-4 line whose MET/OPEN/RULED OUT status
               differs from the last tag's copy has a CHANGELOG entry under
               "Unreleased" naming its section (4.x); no tagged copy = first
               tag with a SPEC, counted and passed
    daybook    DAYBOOK.md's last entry carries **At close**
    handoff    HANDOFF.md has a block for THE MARK'S OWN DAY (its
               `creatordate`), falling back to today when no mark is named --
               "the mark is a true record of time", his ruling 2026-09-24
    mark       the named mark points at a real commit AND that commit is
               carried by the main line; not asked when no mark is named
    tasks      every TASKS box ticked since the last mark carries a date on
               or after that mark -- a tick with nothing written down is
               the one shape the record cannot later explain
    pins       pyproject.toml and manjuel/__init__.py agree, and equal the
               mark's number at the mark's commit when one is named
    marks      every mark git holds has a CHANGELOG heading (gated); where
               each heading says its mark sits, against where it does, is
               REPORTED -- the sha is written in the commit after the cut,
               and older headings are history (LAW 1)
    remotes    core and atlas each level with origin/main as last fetched
    flows      every spec in flows/ the door would list parses and passes
               the flow law (gated; the door's flow_list names one it cannot
               read too, since 2026-09-25); folded versions that would fail
               today's law, flows
               never fired, and flows never COMPLETE are REPORTED. The
               terminal's: flows/ is runtime state and in no checkout
    workflows  every .github/workflows/*.yml is tracked (an untracked one is
               one CI never sees), and every python command in it names a
               script in the tree and flags that script knows

THE OPERATOR'S TERMINAL IS THE PROOF. A hand runs this on a mirror as its
own check (CLAUDE.md's rule); last_run.json there is the mirror's stamp,
not his. The tag is cut only where this passes on the real ground.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# EVERY CHILD HERE CLOSES STDIN, AND IT IS LOAD-BEARING (2026-09-10).
#
# `subprocess.run()` with no `stdin` hands the child the PARENT's stdin. From a
# shell that is a console and harmless. Inside the engine under `manjuel.py
# --headless` it is the pipe `serve.Inbox` has a thread permanently blocked
# reading -- two readers on one pipe, and git never returns. Worse than a slow
# call: `run(timeout=N)` raises TimeoutExpired, then kills the child and calls
# communicate() AGAIN with no timeout, which blocks for the life of the process.
#
# boot.py's `_gate()` loads this module and calls `spec(ROOT, None)` at EVERY
# boot, and spec() with no tag calls last_tag() -> `git tag`. So this omission
# froze the engine during boot: nine sittings on 2026-09-10 opened, hung, and
# were closed by THE LINE's timeout with nothing run. gitstate.py was given
# this same fix on 2026-09-09 and calls it load-bearing; this file was not.
#
# No command here ever reads stdin, so closing it costs nothing.
DEVNULL = subprocess.DEVNULL

# THE THREE CHECKS THAT ARE TRUE OF A GROUND AND NOT OF A CHECKOUT
# (2026-09-24, his word: "integrate that missing CI gate for releases and tag
# cutting").
#
# `strokes`, `smoke` and `standup` all ask the same question: is the stamp
# NEWER than the newest edit? `newest_edit` reads filesystem mtimes, and **git
# does not carry mtimes** -- a fresh checkout stamps every file with the
# checkout time, which is newer than any committed stamp. So on a runner those
# three read STALE by construction, every time, whatever the truth is.
#
# That is not a defect to work around; it is this file's own docstring already:
# THE OPERATOR'S TERMINAL IS THE PROOF. The six below are facts about the
# RECORD and are true of any checkout of it; these three are facts about the
# machine the suites actually ran on.
#
# ONE LIST, READ BY BOTH DOORS. `--record-only` skips exactly these, and the
# workflow names none of its own -- so CI and his terminal can never come to
# mean two different things, which is what a second definition would be.
#
# `flows` IS THE FOURTH, FOR A DIFFERENT REASON (his ruling, 2026-09-25). Not
# mtimes: flows/ is the workflow engine's own store and is gitignored as
# per-ground runtime state, so no checkout has that folder at all. His
# terminal does, and at cut time that is where "would the door list every one
# of these, and has the flow that cuts marks ever been fired" gets its answer.
TERMINAL_ONLY = ("strokes", "smoke", "standup", "flows")
FLOWS_WHY = ("flows/ is per-ground runtime state (.gitignore) and is in no "
             "checkout; the operator's terminal reads it at cut time")

CODE_DIRS = ("manjuel", "agents", "skills", "tests")
# What the suites write into tests/ as they run. Counting these as edits
# made the strokes STALE the moment smoke finished after them.
STAMPS = {"last_run.md", "last_run.json", "run_history.jsonl", "last_audit.md"}
SPEC_LINE = re.compile(r"^- \*{0,2}(MET|OPEN|RULED OUT)\b", re.M)
SPEC_HEAD = re.compile(r"^### (4\.\d+)\b", re.M)


class Check:
    # `ran` is a THIRD STATE and not a green (2026-09-24). A check that was not
    # run is not a check that passed, and recording it as one is exactly the
    # lie this gate exists to refuse. It prints as `not here`, it is counted
    # apart, and `render` says how many were left to his terminal.
    def __init__(self, name: str, ok: bool, why: str = "", ran: bool = True):
        self.name, self.ok, self.why = name, bool(ok), why
        self.ran = bool(ran)

    def line(self) -> str:
        mark = "ok " if self.ok else "REFUSED"
        if not self.ran:
            mark = "not here"
        return f"  {mark:8} {self.name:10} {self.why}"


# ---- what the ground says --------------------------------------------

def newest_edit(root: Path = ROOT) -> float:
    """The newest mtime under the code dirs -- boot.suite_tally's rule."""
    touched = 0.0
    for d in CODE_DIRS:
        for f in (root / d).rglob("*"):
            if f.name in STAMPS:
                continue          # the suites' own writes are not edits
            if f.suffix in (".py", ".md") and "__pycache__" not in f.parts:
                try:
                    touched = max(touched, f.stat().st_mtime)
                except OSError:
                    pass
    return touched


def suites(root: Path = ROOT, edited: float | None = None) -> list[Check]:
    edited = newest_edit(root) if edited is None else edited
    out: list[Check] = []
    stamp = root / "tests" / "last_run.json"
    try:
        book = json.loads(stamp.read_text(encoding="utf-8"))
    except Exception as exc:
        return [Check("strokes", False, f"tests/last_run.json unreadable ({exc})"),
                Check("smoke", False, "the same stamp")]
    for suite in ("strokes", "smoke"):
        r = book.get(suite) or {}
        if not r:
            out.append(Check(suite, False, "never stamped"))
            continue
        if r.get("state") == "running":
            out.append(Check(suite, False, "DID NOT FINISH (state: running)"))
            continue
        tally = f"{r.get('passed')}/{r.get('total')}"
        if not r.get("green"):
            out.append(Check(suite, False, f"{tally} RED"))
        elif (r.get("at") or 0) < edited:
            out.append(Check(suite, False, f"{tally} green but STALE: the ground "
                                            f"changed since; re-run"))
        else:
            out.append(Check(suite, True, f"{tally} green, after the newest edit"))
    return out


def standup(root: Path = ROOT, edited: float | None = None) -> Check:
    edited = newest_edit(root) if edited is None else edited
    hist = root / "tests" / "run_history.jsonl"
    last = None
    if not hist.exists():
        return Check("standup", False, "never run LIVE (a --dry run does not count)")
    try:
        for line in hist.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("suite") == "standup":
                last = rec
    except Exception as exc:
        return Check("standup", False, f"run_history.jsonl unreadable ({exc})")
    if last is None:
        return Check("standup", False, "never run LIVE (a --dry run does not count)")
    tally = f"{last.get('passed')}/{last.get('total')}"
    if not last.get("green"):
        return Check("standup", False, f"{tally} -- failed: {', '.join(last.get('failed') or [])}")
    if (last.get("at") or 0) < edited:
        return Check("standup", False, f"{tally} green but before the newest edit; run it live again")
    return Check("standup", True, f"{tally} live, {last.get('report', '')}")


def buildmap(root: Path = ROOT) -> Check:
    r = subprocess.run([sys.executable, str(root / "tests" / "buildmap.py"), "--check"],
                       capture_output=True, text=True, cwd=str(root), timeout=120,
                       stdin=DEVNULL)      # see DEVNULL, above -- load-bearing
    tail = (r.stdout or r.stderr).strip().splitlines()[-1:] or [""]
    return Check("buildmap", r.returncode == 0, tail[0])


def law(root: Path = ROOT) -> Check:
    r = subprocess.run([sys.executable, str(root / "law" / "law.py"), "--prove"],
                       capture_output=True, text=True, cwd=str(root), timeout=120,
                       stdin=DEVNULL)      # see DEVNULL, above -- load-bearing
    tail = (r.stdout or r.stderr).strip().splitlines()[-1:] or [""]
    return Check("law", r.returncode == 0, tail[0][:100])


def manifest(root: Path = ROOT) -> Check:
    try:
        from manjuel import us
        from manjuel.registry import AgentRegistry
        from manjuel.skills import SkillLibrary
        installed, why = us.rack_tags()
        text = us.report(root, AgentRegistry.load(root / "agents"),
                         SkillLibrary.load(root / "skills"), installed)
    except Exception as exc:
        return Check("manifest", False, f"could not reconcile ({exc})")
    # ALL THREE KINDS GATE (LOOSE added 2026-09-24, his word: "loose gates the
    # tag"). This list was the wire the LOOSE check needed and did not have:
    # `us.report` would have printed a LOOSE line, this filter would not have
    # collected it, and the gate would have passed a manifest carrying a
    # declaration nothing reads -- a check built to find unwired things,
    # unwired. Spelled with the trailing space each line actually carries
    # (`Finding.line` pads the level to five), so a fourth kind added without
    # a thought here fails to gate LOUDLY rather than silently.
    findings = [l for l in text.splitlines()
                if l.startswith(("  GAP ", "  DRIFT ", "  LOOSE "))]
    if installed is None:
        # The rack could not be asked. That is a fact about this machine
        # (a mirror, a box without Ollama), not a drift in the manifest;
        # the line is reported and the other findings still gate.
        findings = [l for l in findings if "the rack" not in l]
    if findings:
        return Check("manifest", False, f"{len(findings)} finding(s): "
                     + "; ".join(l.split()[1] for l in findings))
    return Check("manifest", True, "agrees with the disk"
                 + ("" if installed is not None else f" (rack not asked: {why[:60]})"))


def spec_statuses(text: str) -> dict[str, list[str]]:
    """{'4.1': ['MET', 'MET', 'OPEN'], ...} in order of appearance."""
    out: dict[str, list[str]] = {}
    section = ""
    for line in text.splitlines():
        h = SPEC_HEAD.match(line)
        if h:
            section = h.group(1)
            out.setdefault(section, [])
            continue
        if not section:
            continue
        m = SPEC_LINE.match(line)
        if m:
            out[section].append(m.group(1))
    return out


def last_tag(root: Path = ROOT, cutting: str = "") -> str:
    """The newest mark, EXCLUDING the one being cut.

    On his terminal the gate runs BEFORE the mark exists, so the newest tag is
    the previous one and `cutting` changes nothing. In CI on a tag push the
    mark already exists -- so without this, `spec` would fetch SPEC.md at the
    tag being cut, compare it with itself, find nothing changed, and PASS.
    A gate that passes because it compared a thing to itself is worse than no
    gate; it is a green nobody earned.
    """
    try:
        r = subprocess.run(["git", "tag", "--sort=-v:refname"], capture_output=True,
                           text=True, cwd=str(root), timeout=30,
                           stdin=DEVNULL)  # see DEVNULL, above -- load-bearing
        tags = [t for t in r.stdout.split() if t.startswith("v") and t != cutting]
        return tags[0] if tags else ""
    except Exception:
        return ""


def tagged_file(root: Path, tag: str, rel: str) -> str | None:
    """A file as it was at `tag`, or None if the tag did not hold it.
    `git show` reads objects and never touches the index (CLAUDE.md)."""
    if not tag:
        return None
    # DECODED AS UTF-8, NOT AS THE CONSOLE'S LOCALE (2026-09-24). `text=True`
    # alone decodes with the locale, which on this Windows ground is cp1252,
    # so every em-dash in a tagged file came back as three wrong characters.
    # `spec` never noticed -- its regexes are ASCII -- and `tasks` found it on
    # its first run: 28 titles that "flipped" only because the copy from the
    # mark no longer spelled them the way the working tree does.
    try:
        r = subprocess.run(["git", "show", f"{tag}:{rel}"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           cwd=str(root), timeout=30,
                           stdin=DEVNULL)  # see DEVNULL, above -- load-bearing
    except Exception:
        return None
    return r.stdout if r.returncode == 0 else None


def unreleased(changelog: str) -> str:
    """The text under '## Unreleased' up to the next '## '."""
    m = re.search(r"^## Unreleased[^\n]*\n(.*?)(?=^## |\Z)", changelog, re.M | re.S)
    return m.group(1) if m else ""


def spec(root: Path = ROOT, tag: str | None = None, cutting: str = "") -> Check:
    tag = last_tag(root, cutting) if tag is None else tag
    try:
        now = (root / "SPEC.md").read_text(encoding="utf-8")
        log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    except Exception as exc:
        return Check("spec", False, f"SPEC/CHANGELOG unreadable ({exc})")
    cur = spec_statuses(now)
    n_lines = sum(len(v) for v in cur.values())
    before_text = tagged_file(root, tag, "SPEC.md")
    if before_text is None:
        return Check("spec", True, f"{n_lines} section-4 lines; no SPEC at {tag or 'any tag'} "
                                   f"to compare -- first tag with one")
    before = spec_statuses(before_text)
    changed = [s for s in sorted(set(cur) | set(before)) if cur.get(s) != before.get(s)]
    if not changed:
        return Check("spec", True, f"{n_lines} section-4 lines, none changed since {tag}")
    unlogged = [s for s in changed if s not in unreleased(log)]
    if unlogged:
        return Check("spec", False, f"changed since {tag} with no Unreleased CHANGELOG line "
                                    f"naming them: {', '.join(unlogged)}")
    return Check("spec", True, f"changed since {tag}: {', '.join(changed)} -- each in CHANGELOG")


def daybook(root: Path = ROOT) -> Check:
    try:
        text = (root / "DAYBOOK.md").read_text(encoding="utf-8")
    except Exception as exc:
        return Check("daybook", False, f"unreadable ({exc})")
    entries = re.split(r"^## Session ", text, flags=re.M)
    if len(entries) < 2:
        return Check("daybook", False, "no session entry")
    last = entries[-1]
    head = last.splitlines()[0].strip()
    ok = "**At close**" in last
    return Check("daybook", ok, f"Session {head[:50]}" + ("" if ok else " -- no **At close** line"))


def mark_date(root: Path = ROOT, tag: str = "") -> str:
    """The day the MARK says it was made, or "" if there is no such mark.

    `creatordate` is the tagger's own time on an annotated mark and falls back
    to the commit's on a lightweight one, so both kinds answer. Read-only, and
    `for-each-ref` never touches the index (CLAUDE.md).
    """
    if not tag:
        return ""
    try:
        r = subprocess.run(["git", "for-each-ref", "--format=%(creatordate:short)",
                            f"refs/tags/{tag}"], capture_output=True, text=True,
                           cwd=str(root), timeout=30, stdin=DEVNULL)
    except Exception:
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def mark(root: Path = ROOT, tag: str = "") -> Check:
    """Does the mark point at a real commit, and is that commit on the line?

    His ruling, 2026-09-24: the gate "verifies the tag points at a real commit
    on the main line". A mark on a commit the main line does not carry can
    publish a history that line has not -- which is CLAUDE.md RULE 1's whole
    argument, and the reason the door refuses to SEND such a mark.

    WITH NO MARK NAMED there is nothing to ask and the check says so rather
    than passing quietly: that is the ordinary case on his terminal, where the
    gate runs BEFORE the mark is cut.

    THE WORKING TREE IS NOT ASKED HERE, deliberately. The door already refuses
    to cut over a dirty tree at HEAD (BUILDPATH, "The marks, and how one is
    cut", step 5), and `git status` from a sandbox is the one command
    CLAUDE.md forbids outright -- a second copy of that refusal here would buy
    nothing and could leave a lock in his ground.
    """
    if not tag:
        return Check("mark", True, "no mark named -- nothing to point at yet", ran=False)
    try:
        sha = subprocess.run(["git", "rev-parse", "--verify", f"{tag}^{{commit}}"],
                             capture_output=True, text=True, cwd=str(root),
                             timeout=30, stdin=DEVNULL)
    except Exception as exc:
        return Check("mark", False, f"git could not be asked ({exc})")
    if sha.returncode != 0:
        return Check("mark", False, f"{tag} names no commit in this ground")
    commit = sha.stdout.strip()[:9]
    # THE LINE, by either name: a checkout in CI is detached at the mark and
    # carries `origin/main`; his ground carries `main`. Asked in that order,
    # and an answer from either is the same fact.
    for line in ("main", "origin/main"):
        try:
            r = subprocess.run(["git", "merge-base", "--is-ancestor", commit, line],
                               capture_output=True, text=True, cwd=str(root),
                               timeout=30, stdin=DEVNULL)
        except Exception:
            continue
        if r.returncode == 0:
            return Check("mark", True, f"{tag} -> {commit}, carried by {line}")
    return Check("mark", False, f"{tag} -> {commit}, which the main line does NOT "
                                f"carry -- sending it would publish a history "
                                f"that line has not (RULE 1)")


def handoff(root: Path = ROOT, today: str | None = None, tag: str = "") -> Check:
    """HANDOFF carries a block for the day the work was marked.

    THE MARK IS A TRUE RECORD OF TIME (his ruling, 2026-09-24). This asked the
    RUNNER's clock, which is his terminal's on his terminal and UTC in CI --
    so a mark cut in his evening became tomorrow on the runner and the gate
    refused a record that was whole. A mark carries its own date; the gate
    reads that, and falls back to today only when there is no mark to ask.
    """
    named = mark_date(root, tag)
    today = today or named or time.strftime("%Y-%m-%d")
    try:
        text = (root / "HANDOFF.md").read_text(encoding="utf-8")
    except Exception as exc:
        return Check("handoff", False, f"unreadable ({exc})")
    ok = f"## HANDOFF FOR {today}" in text
    whose = f" (the mark's own day)" if named and today == named else ""
    return Check("handoff", ok, f"HANDOFF FOR {today}{whose}"
                 + ("" if ok else " -- missing"))



# ---- version control against the record (2026-09-24, his word) ----------
#
# "The CI gate needs to make sure the version control is actually matching
# the spec and vision and tasks." Four comparisons, each arithmetic, each
# reading git only through the verbs the allowlist in test_manjuel permits.

TASK_LINE = re.compile(r"^(\s+)\[([ x-])\]\s+(.*)$")
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
HEADING_RE = re.compile(r"^## (v?\d+\.\d+\.\d+)\b[^\n]*", re.M)
TAG_ON_RE = re.compile(r"\(tag on ([0-9a-f]{7,})\)")


def task_blocks(text: str) -> dict[str, tuple[str, str]]:
    """{title: (state, whole block)} for every checkbox line in TASKS.md.

    A block is the `[ ]` line and the more-indented lines under it. The title
    is the first line's text, which is how a task keeps its identity across
    the annotations that grow beneath it as it closes.
    """
    out: dict[str, tuple[str, str]] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = TASK_LINE.match(lines[i])
        if not m:
            i += 1
            continue
        indent, state, title = m.groups()
        block = [lines[i]]
        i += 1
        while i < len(lines) and lines[i].strip() and (
                len(lines[i]) - len(lines[i].lstrip()) > len(indent)):
            block.append(lines[i])
            i += 1
        out[title.strip()] = (state, "\n".join(block))
    return out


def tasks(root: Path = ROOT, tag: str | None = None, cutting: str = "") -> Check:
    """A box ticked since the last mark carries a date since that mark.

    TASKS is his (CLAUDE.md RULE 10), so nothing here judges WHAT was ticked.
    What it asks is narrower and arithmetic: every tick in that file carries
    a dated account of when it closed and on whose word, and a tick with no
    date is a box closed with nothing written down -- the one shape the
    record cannot later explain.
    """
    tag = last_tag(root, cutting) if tag is None else tag
    try:
        now = task_blocks((root / "TASKS.md").read_text(encoding="utf-8"))
    except Exception as exc:
        return Check("tasks", False, f"TASKS.md unreadable ({exc})")
    before_text = tagged_file(root, tag, "TASKS.md")
    if before_text is None:
        return Check("tasks", True, f"{sum(1 for s_, _ in now.values() if s_ != ' ')} "
                                    f"ticked; no TASKS at {tag or 'any mark'} to compare")
    before = task_blocks(before_text)
    since = mark_date(root, tag)
    flipped = [t for t, (st, _) in now.items()
               if st != " " and before.get(t, (" ", ""))[0] == " "]
    undated = []
    for t in flipped:
        dates = DATE_RE.findall(now[t][1])
        if not dates or (since and max(dates) < since):
            undated.append(t)
    if undated:
        shown = "; ".join(u[:48] for u in undated[:3])
        more = f" (+{len(undated) - 3} more)" if len(undated) > 3 else ""
        return Check("tasks", False, f"{len(undated)} of {len(flipped)} ticked since {tag} "
                                     f"with no date since {since or 'the mark'}: "
                                     f"{shown}{more}")
    return Check("tasks", True, f"{len(flipped)} ticked since {tag}, each dated")


def pins(root: Path = ROOT, cutting: str = "") -> Check:
    """pyproject.toml and manjuel/__init__.py say one version -- and, when a
    mark is named, the version at THAT COMMIT is the mark's number.

    BUILDPATH's first step in cutting a mark is "bump the pins and SAVE them",
    and the door refuses a number the version file does not agree with at the
    commit. This is the same question asked BEFORE the button, on his terminal,
    where a disagreement costs a line rather than a refused mark.
    """
    def read(rel: str) -> str:
        text = tagged_file(root, cutting, rel) if cutting else None
        if text is None:
            try:
                text = (root / rel).read_text(encoding="utf-8")
            except Exception:
                return ""
        m = re.search(r'(?m)^(?:version|__version__)\s*=\s*"([^"]+)"', text)
        return m.group(1) if m else ""

    a, b = read("pyproject.toml"), read("manjuel/__init__.py")
    where = f"at {cutting}" if cutting else "in the working tree"
    if not a or not b:
        return Check("pins", False, f"a pin is unreadable {where}: "
                                    f"pyproject={a or '?'} __init__={b or '?'}")
    if a != b:
        return Check("pins", False, f"the pins disagree {where}: pyproject {a}, __init__ {b}")
    if cutting and cutting.lstrip("v") != a:
        return Check("pins", False, f"the pins say {a} {where}, but the mark is {cutting}")
    return Check("pins", True, f"both {a} {where}" + (f" == {cutting}" if cutting else ""))


def marks(root: Path = ROOT, cutting: str = "") -> Check:
    """Every mark git holds has a CHANGELOG heading, and the newest one's
    heading names the commit the mark actually sits on.

    EXISTENCE GATES; THE SHA IS REPORTED. Two facts decided that, both read
    off the record. First, the heading's sha is written in the commit AFTER
    the mark (v0.1.14 sits on de2420e; e88039b, the next commit, is the one
    that wrote "tag on de2420e" into the heading) -- so at the moment a mark
    is cut, its own heading cannot yet name it, and gating there would refuse
    every honest cut. Second, four older headings name commits as they stood
    before the history was rewritten on his word (2026-09-21), and LAW 1
    forbids rewriting the headings to agree. What this GATES is that every
    mark has a heading at all; what it REPORTS is where each heading says the
    mark sits against where it does -- the check BUILDPATH's "THE MARKS AS GIT
    HOLDS THEM" pass did by hand once, made automatic.
    """
    try:
        log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        r = subprocess.run(["git", "tag", "--sort=-v:refname"], capture_output=True,
                           text=True, cwd=str(root), timeout=30, stdin=DEVNULL)
    except Exception as exc:
        return Check("marks", False, f"could not read the marks ({exc})")
    held = [t for t in r.stdout.split() if t and t != cutting]
    if not held:
        return Check("marks", True, "no marks in this ground yet")
    headed = {m.group(1): m.group(0) for m in HEADING_RE.finditer(log)}
    missing = [t for t in held if t not in headed and t.lstrip("v") not in headed]
    if missing:
        return Check("marks", False, f"{len(missing)} mark(s) with no CHANGELOG heading: "
                                     + ", ".join(missing))

    def sits_on(t: str) -> str:
        try:
            q = subprocess.run(["git", "rev-parse", "--short=7", f"{t}^{{commit}}"],
                               capture_output=True, text=True, cwd=str(root),
                               timeout=30, stdin=DEVNULL)
            return q.stdout.strip() if q.returncode == 0 else ""
        except Exception:
            return ""

    agree, disagree, unsaid = [], [], []
    for t in held:
        head = headed.get(t) or headed.get(t.lstrip("v"), "")
        m = TAG_ON_RE.search(head)
        real = sits_on(t)
        if not m:
            unsaid.append(t)
        elif real and real.startswith(m.group(1)[:7]):
            agree.append(t)
        else:
            disagree.append(f"{t} (says {m.group(1)[:7]}, sits on {real or '?'})")
    parts = [f"{len(held)} marks, each with a heading"]
    if agree:
        parts.append(f"{len(agree)} sit where they say")
    if disagree:
        parts.append(f"{len(disagree)} name a commit as it stood before the rewrite of "
                     f"2026-09-21: " + ", ".join(disagree))
    if unsaid:
        parts.append(f"{len(unsaid)} name no commit: " + ", ".join(unsaid))
    return Check("marks", True, "; ".join(parts))


def remotes(root: Path = ROOT) -> Check:
    """core and atlas each level with the remote as last fetched.

    "The two repos are in step" (his ruling). Read-only: `rev-parse` against
    the tracking ref, which is the remote AS LAST KNOWN -- the gate fetches
    nothing, so this says "level with what this machine last heard", and says
    so. Unsaved work is the DOOR's refusal at cut time, and `git status` is
    not run from here (CLAUDE.md).
    """
    def head_and_remote(d: Path) -> tuple[str, str]:
        out = []
        for ref in ("HEAD", "origin/main"):
            try:
                q = subprocess.run(["git", "rev-parse", "--short", ref], capture_output=True,
                                   text=True, cwd=str(d), timeout=30, stdin=DEVNULL)
                out.append(q.stdout.strip() if q.returncode == 0 else "")
            except Exception:
                out.append("")
        return out[0], out[1]

    lines, bad = [], []
    for name, d in (("core", root), ("atlas", root / "atlas")):
        if not (d / ".git").exists():
            lines.append(f"{name}: no repository")
            continue
        h, rmt = head_and_remote(d)
        if not h or not rmt:
            bad.append(f"{name}: {'no HEAD' if not h else 'no origin/main known'}")
        elif h != rmt:
            bad.append(f"{name}: HEAD {h}, origin/main {rmt}")
        else:
            lines.append(f"{name} level at {h}")
    if bad:
        return Check("remotes", False, "; ".join(bad + lines))
    return Check("remotes", True, "; ".join(lines) + " (as last fetched)")


# ---- the gate ----------------------------------------------------------

# ---- the flows the door would list, and the workflows CI would run --------
#
# THE FLOW LAW, STATED TWICE ON PURPOSE AND RECONCILED. flow.Validate
# (atlas/line/internal/flow/flow.go) is the law; it runs when a flow is SAVED
# or FIRED and nowhere else. flow.List read each spec back and, if it would
# not parse, skipped it without a word (`if err != nil { continue }`), so a
# corrupt flow was invisible until somebody fired it -- found here on
# 2026-09-25 and taught to the engine the same day on his word (flow.Unread;
# flow_list prints UNREADABLE). A spec that parses but breaks the law is
# listed and refused only when fired. The gate runs
# where the door is not, so the law is restated here, and a stroke in
# tests/test_manjuel.py holds these constants to flow.go's and play.go's own
# text on every run of the suite on his ground. Two copies and a promise
# would be a convention; the stroke is the wire.
FLOW_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")               # flow.go NameRe
FLOW_HISTORY = re.compile(r"^([a-z0-9][a-z0-9_-]{0,63})\.v(\d+)$")   # <name>.v<k>.json
FLOW_KINDS = {"ask", "prompt", "seat", "memory", "eval", "gate", "run"}  # flow.go Kinds
FLOW_MATCHES = {"equals", "contains"}                                  # flow.go Matches
FLOW_MAX_RETRIES = 5                                                   # flow.go MaxRetries
FLOW_VAR = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")                # play.Render's slot


def flow_faults(spec) -> list[str]:
    """Every fault flow.Validate would name in this spec, in its words -- and
    the one it does not ask: that every `{{out_x}}` names a node. play.Render
    refuses a missing var by name, but at RUN time, on the node that reads it,
    after every node before it has already spent its budget; asking here costs
    nothing and fires nothing. A bare `{{input}}` is the run's to supply and is
    not a fault. Where Validate stops at the first fault, this names them all.
    """
    if not isinstance(spec, dict):
        return ["the spec is not an object"]
    faults: list[str] = []
    name = spec.get("name")
    if not isinstance(name, str) or not FLOW_NAME.match(name):
        faults.append(f"flow name {name!r} breaks the name law")
    nodes = spec.get("nodes") or []
    if not nodes:
        faults.append("carries no nodes")
    by_name: dict[str, dict] = {}
    for n in nodes:
        n = n if isinstance(n, dict) else {}
        nn, kind = str(n.get("name", "")), str(n.get("kind", ""))
        if not FLOW_NAME.match(nn):
            faults.append(f"node name {nn!r} breaks the name law")
        if nn in by_name:
            faults.append(f"duplicate node name {nn!r}")
        if kind not in FLOW_KINDS:
            faults.append(f"node {nn!r} carries unknown kind {kind!r}")
        if kind == "run" and not str(n.get("question") or "").strip():
            faults.append(f"run node {nn!r} has no objective")
        if kind == "eval" and not str(n.get("node") or "").strip():
            faults.append(f"eval node {nn!r} names no node to check")
        match = str(n.get("match") or "").strip().lower()
        if kind == "eval" and match and match not in FLOW_MATCHES:
            faults.append(f"eval node {nn!r} carries unknown match {match!r}; "
                          f"the set is equals, contains")
        if kind != "eval" and match:
            faults.append(f"node {nn!r} is a {kind} and has no answer to test, "
                          f"so `match` means nothing on it")
        retries = n.get("retries") or 0
        if not isinstance(retries, int) or retries < 0 or retries > FLOW_MAX_RETRIES:
            faults.append(f"node {nn!r} asks for {retries!r} retries; the range is "
                          f"0 to {FLOW_MAX_RETRIES}")
        elif retries > 0 and kind in ("eval", "gate"):
            faults.append(f"node {nn!r} is a {kind}, and a {kind} is not retried -- "
                          f"retry answers an ERROR, never a verdict")
        by_name[nn] = n
    for nn, n in by_name.items():
        ref = str(n.get("node") or "")
        if n.get("kind") == "eval" and ref and ref not in by_name:
            faults.append(f"eval node {nn!r} checks unknown node {ref!r}")
        texts = [str(n.get(k) or "") for k in ("question", "title", "expected")]
        if isinstance(n.get("vars"), dict):
            texts += [str(v) for v in n["vars"].values()]
        for var in sorted({v for t in texts for v in FLOW_VAR.findall(t)}):
            if var.startswith("out_") and var[4:] not in by_name:
                faults.append(f"node {nn!r} reads {{{{{var}}}}} and no node is named {var[4:]!r}")
    incoming = {k: 0 for k in by_name}
    adj: dict[str, list[str]] = {}
    for e in spec.get("edges") or []:
        e = e if isinstance(e, dict) else {}
        frm, to = str(e.get("from", "")), str(e.get("to", ""))
        when = str(e.get("when") or "always")
        if frm not in by_name:
            faults.append(f"edge from unknown node {frm!r}")
            continue
        if to not in by_name:
            faults.append(f"edge to unknown node {to!r}")
            continue
        if when not in ("always", "pass", "fail"):
            faults.append(f"edge {frm}->{to} carries bad when {when!r}")
        if when == "fail" and by_name[frm].get("kind") not in ("eval", "gate"):
            faults.append(f"fail-edges leave eval/gate nodes only "
                          f"({frm} is {by_name[frm].get('kind')})")
        incoming[to] += 1
        adj.setdefault(frm, []).append(to)
    if by_name:
        starts = sorted(k for k, v in incoming.items() if v == 0)
        if len(starts) != 1:
            faults.append(f"want exactly one start, got {len(starts)}")
        ready, order, indeg = list(starts), [], dict(incoming)
        while ready:                      # Kahn, name-sorted, as Validate walks it
            cur = ready.pop(0)
            order.append(cur)
            for to in sorted(adj.get(cur, [])):
                indeg[to] -= 1
                if indeg[to] == 0:
                    ready.append(to)
            ready.sort()
        if len(order) != len(by_name):
            faults.append(f"cycle or unreachable node in flow {name!r}")
    return faults


def flows(root: Path = ROOT) -> Check:
    """Every flow the door would list is one it could fire, and the ones
    nobody has fired are named. Reads <root>/flows, the research tenant's store.

    THIS IS THE TERMINAL'S (TERMINAL_ONLY). flows/ is gitignored as runtime
    state, so a checkout has none and `--record-only` says `not here`. On his
    ground at cut time it asks four things. GATED: does every spec parse
    (flow.List skipped one that did not, silently, until 2026-09-25 -- now
    the door names it too), and does the latest version
    of each pass the flow law -- a corrupt or unlawful flow is refused by file
    name. REPORTED: which folded versions would fail today's law (history is
    not rewritten, and a law that tightened since a fold is exactly what a
    folded copy will fail); which flows have never been fired, and which have
    never finished COMPLETE. A flow declared and fired by nothing is the LOOSE
    shape -- and on 2026-09-25 `version-tag`, the flow that cuts marks, had
    never once been fired.
    """
    d = root / "flows"
    if not d.is_dir():
        return Check("flows", True, "no flows/ on this ground -- nothing saved, nothing to judge")
    latest: dict[str, list[str]] = {}
    history: list[str] = []
    corrupt: list[str] = []
    broken: list[str] = []
    stale: list[str] = []
    for f in sorted(d.glob("*.json")):
        base = f.name[:-5]
        folded = FLOW_HISTORY.match(base)
        if not folded and not FLOW_NAME.match(base):
            continue                  # neither listed nor fetchable by the door
        try:
            spec = json.loads(f.read_text(encoding="utf-8"))
        except Exception as exc:
            corrupt.append(f"{f.name} ({type(exc).__name__}) -- corrupt; the door's "
                           f"flow_list names it UNREADABLE too")
            continue
        faults = flow_faults(spec)
        if folded:
            history.append(f.name)
            if faults:
                stale.append(f"{f.name} ({faults[0]})")
        else:
            latest[base] = faults
            if faults:
                broken.append(f"{f.name}: " + "; ".join(faults[:2]))
    starts: dict[str, int] = {}
    complete: dict[str, int] = {}
    run_flow: dict[str, str] = {}
    runs = d / "runs.jsonl"
    if runs.is_file():
        for line in runs.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("kind") == "start":
                fl = str(r.get("flow", "?"))
                starts[fl] = starts.get(fl, 0) + 1
                run_flow[str(r.get("run", ""))] = fl
            elif r.get("kind") == "stopped" and r.get("verdict") == "COMPLETE":
                fl = run_flow.get(str(r.get("run", "")), "?")
                complete[fl] = complete.get(fl, 0) + 1
    if corrupt or broken:
        return Check("flows", False, "; ".join(corrupt + broken))
    parts = [f"{len(latest)} flow{'s' if len(latest) != 1 else ''} the door would list, each valid"]
    if history:
        parts.append(f"{len(history)} folded version{'s' if len(history) != 1 else ''}"
                     + (f", {len(stale)} would not pass today's law: " + ", ".join(stale)
                        if stale else ""))
    never = sorted(n for n in latest if not starts.get(n))
    if never:
        parts.append("NEVER FIRED: " + ", ".join(never))
    unfinished = sorted(n for n in latest if starts.get(n) and not complete.get(n))
    if unfinished:
        parts.append("fired, never COMPLETE: " + ", ".join(unfinished))
    gone = sorted(n for n in starts if n not in latest)
    if gone:
        parts.append("runs of flows no longer on disk: " + ", ".join(gone))
    return Check("flows", True, "; ".join(parts))


RUN_KEY = re.compile(r"^(\s*)(?:-\s+)?run:\s*(.*)$")
PY_CMD = re.compile(r"(?<![\w./-])python3?\s+(\S+\.py)((?:[ \t]+[^\s|&;]+)*)")


def run_commands(text: str) -> list[tuple[str, str]]:
    """Every `python <script>.py [args]` a workflow's run: steps would execute,
    as (script, args). Both forms are read -- `run: cmd` and `run: |` with an
    indented block -- by indentation, the way the runner reads them. No YAML
    library: the record's workflows are plain, and the gate installs nothing
    (prove.yml's own rule).
    """
    out: list[tuple[str, str]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = RUN_KEY.match(lines[i])
        i += 1
        if not m:
            continue
        indent, rest = len(m.group(1)), m.group(2).strip()
        if rest.startswith(("|", ">")):
            body = []
            while i < len(lines) and (not lines[i].strip()
                                      or len(lines[i]) - len(lines[i].lstrip()) > indent):
                body.append(lines[i])
                i += 1
            rest = "\n".join(body)
        for cmd in PY_CMD.finditer(rest):
            out.append((cmd.group(1), cmd.group(2).strip()))
    return out


def workflows(root: Path = ROOT) -> Check:
    """Every CI workflow in the record is one CI will run as written: tracked
    (an untracked workflow is one CI never sees -- release-gate.yml sat on disk
    untracked the day this was built), every python command naming a script
    that is in the tree, every flag one that script's source knows.

    RECORD, NOT RUN. Whether a workflow last went green is GitHub's to say and
    is not asked here (RULE 4: the gate reaches no server). What is asked is
    the part that goes red silently: a renamed script or flag fails the step
    on the runner, after the mark is cut, where nobody is reading.
    """
    d = root / ".github" / "workflows"
    files = (sorted(d.glob("*.yml")) + sorted(d.glob("*.yaml"))) if d.is_dir() else []
    if not files:
        return Check("workflows", True, "no .github/workflows here")
    tracked: set[str] | None = None
    try:
        r = subprocess.run(["git", "ls-files", "--", ".github/workflows"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", cwd=str(root),
                           timeout=30, stdin=DEVNULL)
        if r.returncode == 0:
            tracked = {Path(p.strip()).name for p in r.stdout.splitlines() if p.strip()}
    except Exception:
        tracked = None
    bad: list[str] = []
    if tracked is not None:
        bad += [f"{f.name} is untracked -- CI never sees it" for f in files if f.name not in tracked]
    n_cmd = 0
    for f in files:
        for script, args in run_commands(f.read_text(encoding="utf-8", errors="replace")):
            n_cmd += 1
            target = root / script
            if not target.is_file():
                bad.append(f"{f.name}: {script} is not in the tree")
                continue
            src = target.read_text(encoding="utf-8", errors="replace")
            for flag in (t for t in args.split() if t.startswith("-")):
                if f'"{flag}"' not in src and f"'{flag}'" not in src:
                    bad.append(f"{f.name}: {script} knows no {flag}")
    if bad:
        return Check("workflows", False, "; ".join(bad))
    tracking = "each tracked" if tracked is not None else "tracking not asked (no repository here)"
    return Check("workflows", True,
                 f"{len(files)} workflow{'s' if len(files) != 1 else ''}, {tracking}; "
                 f"{n_cmd} python command{'s' if n_cmd != 1 else ''}, every script in the tree "
                 f"and every flag known")


def checks(root: Path = ROOT, tag: str | None = None, cutting: str = "",
           record_only: bool = False) -> list[Check]:
    """Every check, in order. `record_only` leaves the three that need the
    ground the suites ran on (TERMINAL_ONLY) unrun and says so, rather than
    running them against a checkout's mtimes and calling the answer a verdict.
    """
    edited = newest_edit(root)
    out: list[Check] = []
    if record_only:
        why = ("the operator's terminal proves this; a checkout carries no "
               "mtimes, so it cannot be asked here")
        out += [Check(n, True, why, ran=False) for n in TERMINAL_ONLY[:2]]
        out.append(buildmap(root))
        out.append(Check(TERMINAL_ONLY[2], True, why, ran=False))
    else:
        out += suites(root, edited)
        out.append(buildmap(root))
        out.append(standup(root, edited))
    out.append(law(root))
    out.append(manifest(root))
    out.append(spec(root, tag, cutting))
    out.append(daybook(root))
    out.append(handoff(root, tag=cutting))
    out.append(mark(root, cutting))
    out.append(tasks(root, tag, cutting))
    out.append(pins(root, cutting))
    out.append(marks(root, cutting))
    out.append(remotes(root))
    out.append(Check("flows", True, FLOWS_WHY, ran=False) if record_only else flows(root))
    out.append(workflows(root))
    return out


def render(results: list[Check], version: str = "") -> str:
    head = f"THE RELEASE GATE{(' -- ' + version) if version else ''}"
    lines = [head, "=" * len(head)] + [c.line() for c in results]
    # NOT RUN IS COUNTED APART, ALWAYS. "PASSED 9 of 9" over three checks
    # nobody made is the one sentence this gate must never print.
    ran = [c for c in results if c.ran]
    left = [c for c in results if not c.ran]
    bad = [c for c in ran if not c.ok]
    lines.append("")
    if bad:
        lines.append(f"REFUSED: {len(bad)} of {len(ran)} -- "
                     + ", ".join(c.name for c in bad) + ". The tag is not cut.")
    else:
        lines.append(f"PASSED: {len(ran)} of {len(ran)}."
                     + ("" if left else
                        " The tag may be cut -- by the operator (RULE 6)."))
    if left:
        lines.append(f"NOT ASKED HERE: {len(left)} -- " + ", ".join(c.name for c in left)
                     + ". These are the operator's terminal's, and the mark is "
                       "not cut until they pass there (RULE 6).")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--check" not in argv:
        print(__doc__)
        return 2
    version = next((a for a in argv if a.startswith("v")), "")
    results = checks(ROOT, cutting=version, record_only="--record-only" in argv)
    print(render(results, version))
    return 0 if all(c.ok for c in results if c.ran) else 1


if __name__ == "__main__":
    raise SystemExit(main())
