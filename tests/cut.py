#!/usr/bin/env python3
"""THE RELEASE'S OWN STEPS (2026-10-05, his word: "make the release one workflow").

The release flow (flows/release.json) runs these through the door's
`release_step`, his gates between them, and his Bash tab can run any one:

    python tests/cut.py bump vX.Y.Z     the pins (pyproject.toml, manjuel/__init__.py),
                                        atlas's version files (its own version.ps1,
                                        set and then sync), and both changelogs
                                        folded under the mark
    python tests/cut.py index           the toll index rebuilt after the live check
    python tests/cut.py check vX.Y.Z    STATUS.md printed, then the release gate:
                                        every line ok but `remotes` and `ci`, which
                                        wait on the send
    python tests/cut.py ci vX.Y.Z       GitHub's runs waited for in both
                                        repositories (twenty minutes at most for
                                        each commit), on HEAD and on the mark once
                                        it is cut, then the gate: every line ok
    python tests/cut.py record vX.Y.Z   where the marks sit: "(tag on <sha>)" on
                                        both headings, and the mark on BUILDPATH's
                                        ladder and its list of the marks, by side;
                                        then STATUS.md printed again when the gate
                                        says the record left it older than what it
                                        reads, so the record's save carries it

Every step can be run again: a ground already where a step leaves it is said
so and left alone, so a release that stopped is fired again from the start.
Exit 0 when the step did what it says, 1 when it refused, 2 when it was not
asked properly. NOTHING HERE SAVES, SENDS OR CUTS: those are the door's own
git_commit, git_push and git_tag, each past a gate that grants it (RULE 6,
RULE 12). Every file keeps the line ends it has (CLAUDE.md, B3).
"""
from __future__ import annotations

import re
import subprocess
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import release  # noqa: E402  -- the gate's own readers: one meaning of "the gate passed"

MARK_RE = re.compile(r"^v\d+\.\d+\.\d+$")
STEPS = {"bump": True, "index": False, "check": True, "ci": True, "record": True}  # step -> names a mark
SENT_LATE = ("remotes", "ci")    # what waits on the send when `check` asks
WAIT_S = 20 * 60                 # how long `ci` waits on one commit's runs, at most
POLL_S = 60                      # how often it asks while they run: GitHub answers sixty an hour
LADDER = "## The ladder, 2026-09-30"
HELD = "THE MARKS AS GIT HOLDS THEM"


class Refused(Exception):
    """A step that will not do what it was asked, and why."""


def read(p: Path) -> tuple[str, str]:
    """The file's text with LF ends, and the end it was written with."""
    raw = p.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), ("\r\n" if "\r\n" in raw else "\n")


def write(p: Path, text: str, nl: str) -> None:
    p.write_bytes(text.replace("\n", nl).encode("utf-8"))


def pin(text: str, number: str) -> str:
    """The first `version = "..."` or `__version__ = "..."` line set to the
    number: the line release.pins reads."""
    return re.sub(r'(?m)^((?:version|__version__)\s*=\s*")[^"]+(")',
                  lambda m: m.group(1) + number + m.group(2), text, count=1)


def has_heading(text: str, head: str) -> bool:
    """Whether a line is the mark's heading: `## v0.2.2 ...` or `## [v0.2.2] ...`."""
    return any(ln == head or ln.startswith(head + " ") for ln in text.split("\n"))


def fold(text: str, unreleased: str, head: str, stamp: str) -> str:
    """The changelog with the mark's heading put under its Unreleased heading,
    so what was unreleased stands under the mark. A mark with nothing under
    Unreleased is refused: a number with nothing behind it."""
    lines = text.split("\n")
    if unreleased not in lines:
        raise Refused(f"no {unreleased!r} heading to fold under")
    at = lines.index(unreleased)
    nxt = next((i for i in range(at + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    if not any(ln.strip() for ln in lines[at + 1:nxt]):
        raise Refused(f"nothing under {unreleased!r} -- write what the mark carries first")
    return "\n".join(lines[:at + 1] + ["", f"{head} — {stamp}"] + lines[at + 1:])


def bump(root: Path, mark: str, stamp: str, run=subprocess.run) -> list[str]:
    """Both pins and both changelogs moved to the mark, then atlas's version
    files through its own version.ps1. The changelogs are judged before a byte
    is written, so one with nothing under Unreleased leaves the ground as it was."""
    number = mark[1:]
    said: list[str] = []
    writes: list[tuple[Path, str, str]] = []
    for rel in ("pyproject.toml", "manjuel/__init__.py"):
        text, nl = read(root / rel)
        new = pin(text, number)
        if new != text:
            writes.append((root / rel, new, nl))
        said.append(f"{rel}: {number}" + ("" if new != text else ", already"))
    for rel, unreleased, head in (("CHANGELOG.md", "## Unreleased", f"## {mark}"),
                                  ("atlas/CHANGELOG.md", "## [Unreleased]", f"## [{mark}]")):
        p = root / rel
        if not p.is_file():
            said.append(f"{rel}: not on this ground")
            continue
        text, nl = read(p)
        if has_heading(text, head):
            said.append(f"{rel}: already folded under {head}")
            continue
        writes.append((p, fold(text, unreleased, head, stamp), nl))
        said.append(f"{rel}: folded under {head} — {stamp}")
    for p, text, nl in writes:
        write(p, text, nl)
    atlas = root / "atlas"
    if (atlas / "version.ps1").is_file():
        version = atlas / "VERSION"
        have = version.read_text(encoding="utf-8").strip() if version.is_file() else ""
        for verb in ([["set", number]] if have != number else []) + [["sync"]]:
            q = run(["pwsh", "-NoProfile", "-NonInteractive", "-File", "version.ps1", *verb],
                    cwd=str(atlas), capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
            if q.returncode != 0:
                raise Refused(f"atlas's version.ps1 {' '.join(verb)} refused: "
                              + (q.stdout + q.stderr).strip()[-600:])
        said.append(f"atlas: version files at {number}" + (", already" if have == number else "")
                    + ", every pin in step")
    return said


def index(root: Path, run=subprocess.run) -> tuple[bool, str]:
    """The toll index rebuilt: a live check tolls a sitting, and a stale index
    reds the suites."""
    q = run([sys.executable, str(root / "tests" / "seatindex.py")], cwd=str(root),
            capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    return q.returncode == 0, (q.stdout + q.stderr).strip()


def print_status(root: Path, run=subprocess.run) -> tuple[bool, str]:
    """STATUS.md printed by tests/status.py: before the gate in `check`, and again
    in `record` when the record it wrote left the page older than what it reads."""
    q = run([sys.executable, str(root / "tests" / "status.py")], cwd=str(root),
            capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
    if q.returncode != 0:
        return False, "STATUS.md could not be printed: " + (q.stdout + q.stderr).strip()[-600:]
    return True, (q.stdout or "").strip()


def check(root: Path, mark: str, run=subprocess.run) -> tuple[bool, str]:
    """STATUS.md printed, then the gate for the mark: every line ok but the two
    that wait on the send."""
    ok, why = print_status(root, run)
    if not ok:
        return False, why
    results = release.checks(root, cutting=mark)
    bad = [c.name for c in results if c.ran and not c.ok]
    hard = [n for n in bad if n not in SENT_LATE]
    text = release.render(results, mark)
    if hard:
        return False, text + f"\n\nCHECK REFUSED for {mark}: " + ", ".join(hard)
    late = [n for n in bad if n in SENT_LATE]
    return True, text + f"\n\nCHECK PASSED for {mark}" + (" -- " + ", ".join(late) + " wait on the send" if late else "")


def wait_ci(root: Path, at: str = "HEAD", wait_s: int = WAIT_S, sleep=time.sleep,
            clock=time.monotonic, ask=None):
    """GitHub's verdict on `at` in both repositories, asked again while a run
    is still going, a run is missing or GitHub did not answer -- until the
    wait is spent."""
    ask = ask or release.ci
    end = clock() + wait_s
    while True:
        c = ask(root, ask=True, at=at)
        going = (not c.ran) or "is still" in c.why or "holds no run for this commit" in c.why
        if not going or clock() >= end:
            return c
        sleep(POLL_S)


def sits_on(d: Path, mark: str) -> str:
    """The commit a mark sits on, short, or "" when it is not cut there."""
    try:
        q = subprocess.run(["git", "rev-parse", "--short=7", f"{mark}^{{commit}}"], capture_output=True,
                           text=True, cwd=str(d), timeout=30, stdin=subprocess.DEVNULL)
    except Exception:
        return ""
    return q.stdout.strip() if q.returncode == 0 else ""


def ci(root: Path, mark: str) -> tuple[bool, str]:
    """GitHub green on HEAD -- and on the mark, once it is cut -- in both
    repositories, then the gate for the mark with every line ok."""
    said, green = [], True
    for at in ["HEAD"] + ([mark] if sits_on(root, mark) else []):
        c = wait_ci(root, at)
        said.append(f"GitHub on {at}: {c.why}")
        green = green and c.ok and c.ran
    results = release.checks(root, cutting=mark)
    bad = [c.name for c in results if c.ran and not c.ok]
    said.append(release.render(results, mark))
    if not green or bad:
        why = ", ".join((["GitHub's runs"] if not green else []) + bad)
        return False, "\n".join(said) + f"\n\nCI REFUSED for {mark}: {why}"
    return True, "\n".join(said) + f"\n\nCI GREEN and the gate passed for {mark}"


def unparen(title: str) -> str:
    """A title without the parenthesis it closes on, nested ones and all."""
    if not title.endswith(")"):
        return title
    depth = 0
    for i in range(len(title) - 1, -1, -1):
        depth += {")": 1, "(": -1}.get(title[i], 0)
        if depth == 0:
            return title[:i].rstrip()
    return title


def themes(text: str, head: str) -> str:
    """What a mark carries, in its entries' own titles: the `### ` lines under
    its heading, without the side (`core:`, `atlas:`) or the closing note."""
    lines = text.split("\n")
    at = next((i for i, ln in enumerate(lines) if ln == head or ln.startswith(head + " ")), None)
    if at is None:
        return ""
    titles = []
    for ln in lines[at + 1:]:
        if ln.startswith("## "):
            break
        if ln.startswith("### "):
            titles.append(unparen(re.sub(r"^(?:core|atlas): ", "", ln[4:].strip())))
    return "; ".join(t for t in titles if t)


def tag_heading(text: str, head: str, sha: str) -> str:
    """The mark's heading with "(tag on <sha>)" written on it, once."""
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln == head or ln.startswith(head + " "):
            if "(tag on " not in ln:
                lines[i] = f"{ln} (tag on {sha})"
            return "\n".join(lines)
    raise Refused(f"no heading {head!r} to record the mark on")


def ladder_entry(mark: str, day: str, theme: str) -> list[str]:
    """A mark's lines on BUILDPATH's ladder, as the ladder writes them."""
    body = textwrap.wrap(theme or "(no entry under its heading)", 44)
    return [" " * 11 + f"{mark:<9}{day}  {body[0]}"] + [" " * 32 + b for b in body[1:]]


def held_entry(lines: list[str], last: int, mark: str, sha: str) -> None:
    """The mark put on the last line of a side's list of the marks as git holds
    them, four to a line as the list is written."""
    entry = f"{mark:<8}{sha}"
    if len(re.findall(r"\b[0-9a-f]{7}\b", lines[last])) < 4:
        lines[last] += "    " + entry
    else:
        lines.insert(last + 1, " " * 11 + entry)


def plan(text: str, mark: str, day: str, core: tuple[str, str], atlas: tuple[str, str] | None) -> str:
    """BUILDPATH with the mark on its ladder and on its list of the marks as git
    holds them, by side, each side (sha, theme). A side whose commit BUILDPATH
    already names is left alone."""
    lines = text.split("\n")
    todo = {name: side for name, side in (("core", core), ("atlas", atlas)) if side and side[0] not in text}
    if not todo:
        return text

    def find(start: int, test) -> int:
        return next(i for i in range(start, len(lines)) if test(lines[i]))

    try:
        lad = find(0, lambda ln: ln.startswith(LADDER))
        a_lad = find(lad, lambda ln: ln.startswith("    atlas  v"))
        end_lad = find(a_lad, lambda ln: not ln.strip())
        # The list BELOW the ladder: an earlier day's list of the marks stands
        # above it under the same words, and it is history (LAW 1).
        held = find(end_lad, lambda ln: ln.startswith(HELD))
        c_tab = find(held, lambda ln: ln.startswith("    core   "))
        a_tab = find(c_tab, lambda ln: ln.startswith("    atlas  "))
        end_tab = find(a_tab, lambda ln: not ln.strip())
    except StopIteration:
        raise Refused("BUILDPATH's ladder or its list of the marks is not where the record keeps it")
    # From the bottom up, so each place found above still stands where it was.
    if "atlas" in todo:
        held_entry(lines, end_tab - 1, mark, todo["atlas"][0])
    if "core" in todo:
        held_entry(lines, a_tab - 1, mark, todo["core"][0])
    if "atlas" in todo:
        lines[end_lad:end_lad] = ladder_entry(mark, day, todo["atlas"][1])
    if "core" in todo:
        lines[a_lad:a_lad] = ladder_entry(mark, day, todo["core"][1])
    return "\n".join(lines)


def heading_day(text: str, head: str) -> str:
    """The day the mark's heading names, or today."""
    for ln in text.split("\n"):
        if ln == head or ln.startswith(head + " "):
            m = re.search(r"\d{4}-\d{2}-\d{2}", ln)
            if m:
                return m.group(0)
    return datetime.now().strftime("%Y-%m-%d")


def record(root: Path, mark: str) -> list[str]:
    """Where the marks sit, written into the record: both headings and BUILDPATH
    -- and STATUS.md printed again after them when the gate's own reader says the
    page is now older than the record it reads, so the record's save carries a
    page the flow's last read passes. `check` printed it at the first gate and this
    step writes CHANGELOG after it: v0.2.5's run ended FAIL on `status` alone for
    that (2026-10-10)."""
    core_sha = sits_on(root, mark)
    if not core_sha:
        raise Refused(f"{mark} is not cut in the core yet -- the record follows the cut")
    atlas_dir = root / "atlas"
    has_atlas = (atlas_dir / ".git").exists()
    atlas_sha = sits_on(atlas_dir, mark) if has_atlas else ""
    if has_atlas and not atlas_sha:
        raise Refused(f"{mark} is not cut in atlas yet -- the record follows the cut")
    said: list[str] = []
    writes: list[tuple[Path, str, str]] = []
    log, nl = read(root / "CHANGELOG.md")
    day, theme = heading_day(log, f"## {mark}"), themes(log, f"## {mark}")
    new = tag_heading(log, f"## {mark}", core_sha)
    if new != log:
        writes.append((root / "CHANGELOG.md", new, nl))
    said.append(f"CHANGELOG.md: {mark} on {core_sha}")
    atlas_side = None
    if has_atlas:
        a_log, a_nl = read(atlas_dir / "CHANGELOG.md")
        atlas_side = (atlas_sha, themes(a_log, f"## [{mark}]"))
        new = tag_heading(a_log, f"## [{mark}]", atlas_sha)
        if new != a_log:
            writes.append((atlas_dir / "CHANGELOG.md", new, a_nl))
        said.append(f"atlas/CHANGELOG.md: {mark} on {atlas_sha}")
    path, p_nl = read(root / "BUILDPATH.md")
    new = plan(path, mark, day, (core_sha, theme), atlas_side)
    if new != path:
        writes.append((root / "BUILDPATH.md", new, p_nl))
    said.append(f"BUILDPATH.md: {mark} on the ladder and on the list of the marks, by side")
    for p, text, end in writes:
        write(p, text, end)
    if release.status(root).ok:
        said.append("STATUS.md: already printed after the record it reads")
    else:
        ok, why = print_status(root)
        if not ok:
            raise Refused(why)
        said.append("STATUS.md: printed again, after the record it reads")
    return said


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    step = argv[0] if argv else ""
    mark = argv[1] if len(argv) > 1 else ""
    if step not in STEPS or len(argv) != (2 if STEPS[step] else 1) or (STEPS[step] and not MARK_RE.match(mark)):
        print(__doc__)
        return 2
    try:
        if step == "bump":
            said = bump(ROOT, mark, datetime.now().strftime("%Y-%m-%d %H:%M"))
            print("\n".join(said + [f"BUMPED to {mark}"]))
            return 0
        if step == "record":
            print("\n".join(record(ROOT, mark) + [f"RECORDED {mark}"]))
            return 0
        ok, text = {"index": lambda: index(ROOT), "check": lambda: check(ROOT, mark),
                    "ci": lambda: ci(ROOT, mark)}[step]()
        print(text)
        return 0 if ok else 1
    except Refused as exc:
        print(f"REFUSED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
