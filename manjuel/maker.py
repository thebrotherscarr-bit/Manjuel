"""THE MAKER -- "make me a snake game", and the bookkeeping nobody thinks about.

THE OPERATOR, 2026-09-21: "the true test is if my wife can sit down at the PC,
ask the system to make a type of software, game, etc. and she can see the
result, play the game, try the software" -- and the same afternoon, "the whole
thing running in the webapp, and able to see what the system is doing live,
while it kind of hand-holds for you and does its own version control, project
management and all that stuff that no one thinks about."

WHAT THE ESTATE DID WITH THAT REQUEST BEFORE THIS EXISTED -- sitting 257, the
same day, three runs, every one of them on the record:

    "Make me a simple snake game I can play."    30s, nothing made. The door
        role-played a text snake game; the Router reasoned "write the game file
        first, then test it" and listed the workspace; the Coder never woke.
    "Write ... snake.html ..."                   17s. write_file saved a 0-BYTE
        file: a game does not fit the Router's 900 tokens, and it thought
        about waking the Coder and did not.
    the `coder` flow, on a piece a script can prove   FAIL after 4 of 8 steps.

Every guard held and every failure was named. The fault was the ROUTE: the one
seat able to write a whole program sat off the path, reachable only through a
flag that two small models, twice, did not raise.

SO THE ENGINE ROUTES, AND A MODEL ONLY WRITES. intent.wants_making reads a
make request by arithmetic, the run's spine becomes the Expert Coder alone --
no door to role-play, no Router to plan and not act -- and the Coder is handed
one job: one complete, self-contained web page. What it answers is checked here
by arithmetic, and saved here by the engine, never by the seat (its manifest
still reads "holds no tools", and that stays true).

A PROJECT IS A FOLDER WITH ITS OWN HISTORY. `projects/<name>/` in the ground
(his ruling, 2026-09-21: "projects folder in Research is fine"), ignored by the
core's own git, each project its own repository. Every change is a version --
a commit INSIDE THE PROJECT, never in the ground -- with a plain-English note;
and "go back" is a NEW version that restores an old one, so nothing is
rewritten and nothing is thrown away (LAW 1; LAW 8, "history is immutable").
He asked for exactly this: the system "does its own version control".

WHY A WEB PAGE. It plays in any browser with nothing installed; the browser is
a real sandbox for code a model wrote, which this Windows machine does not give
a script cheaply; and a small local coder is at its best on one page. Nothing
it loads may come from the internet (RULE 4) -- REFUSED here by arithmetic, not
requested in a prompt and hoped for.

PIECES 1 AND 2 OF 3 (BUILDPATH, "The maker"). Piece 2 is the page on the
glass: the door's `projects` tool reads each project's own history for the
Dashboard's list and serves a page into a sandboxed preview, and the words
below (`find`, the pick-up and put-down reports) are how a project is picked up
from that list -- or put down -- in a sitting. Not here yet, and named so
nobody mistakes it for forgotten:
    3  the check: the page loaded in a browser with no window, and any error
       sent back to the Coder before a version is kept
Until then `page_from` checks only what arithmetic can: that it IS a whole
page, and that it reaches for nothing outside this machine. It proves a page is
well-formed and local, never that it works -- nothing here runs it.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import gitstate

PROJECTS = "projects"
PAGE = "index.html"

# WHO SIGNS A PROJECT'S VERSIONS. Set on each project's OWN repository at birth,
# so a version can be saved on a machine with no git identity at all (a CI
# runner has none) and so the history says plainly that the machine made it.
# The ground's repository is never touched by this.
AUTHOR_NAME = "manjuel (the maker)"
AUTHOR_EMAIL = "maker@localhost"

# THE CODER'S WINDOW. A change is made by handing the Coder the whole page and
# taking a whole page back, so the page is in the window twice. At the Coder's
# 8192 tokens (agents/expert_coder.md) that is about 12,000 characters of page
# before the answer would be cut off -- and a cut-off page is refused below
# rather than saved, so this bound only says it sooner, and plainly.
CHANGE_LIMIT = 12_000

# THE SITTING'S PROJECT, by ground. One process is one sitting (serve.py and
# cli.py both), so this lives exactly as long as the sitting it belongs to, and
# a new sitting starts with none: "make it faster" in a fresh sitting is not
# guessed at. An older project is picked up by name ("work on the snake game",
# which the glass's project list sends) and put down the same way ("put it
# down") -- piece 2.
_CURRENT: dict[str, Path] = {}


class MakerRefused(Exception):
    """Why nothing was saved, in a sentence a person can read."""


def _key(ground) -> str:
    return str(Path(ground).resolve()).lower()


def current(ground) -> Path | None:
    """The project this sitting is working on, or None."""
    p = _CURRENT.get(_key(ground))
    return p if p is not None and (p / ".git").is_dir() else None


def set_current(ground, project) -> None:
    _CURRENT[_key(ground)] = Path(project)


def forget(ground=None) -> None:
    """Drop the sitting's project (all of them with no ground). The suites."""
    if ground is None:
        _CURRENT.clear()
    else:
        _CURRENT.pop(_key(ground), None)


# ---------------------------------------------------------------------
# the name
# ---------------------------------------------------------------------

_FILLER = frozenset("""
a an the simple little small basic quick fun cool nice new tiny easy very
really super my our your me us i you we can could that which who just
""".split())


def name_for(what: str) -> str:
    """A folder name from the words that named the thing: "simple snake game"
    -> `snake-game`. Letters, digits and hyphens only, so it is a safe path on
    every machine and can never be a way out of projects/."""
    words = [w for w in re.findall(r"[a-z0-9]+", (what or "").lower())
             if w not in _FILLER]
    name = "-".join(words[-4:])[:40].strip("-")
    return name or "project"


def _free(root: Path, name: str) -> Path:
    """`name`, or `name-2`, `name-3`... -- a project is never made on top of
    another one."""
    p = root / name
    n = 2
    while p.exists():
        p = root / f"{name}-{n}"
        n += 1
    return p


# ---------------------------------------------------------------------
# the page: what the Coder answered, checked by arithmetic
# ---------------------------------------------------------------------

_FENCE = re.compile(r"```[A-Za-z0-9_+-]*[ \t]*\r?\n(.*?)```", re.DOTALL)
_DOC_START = re.compile(r"(?i)<!doctype\s+html|<html[\s>]")
_DOC_END = re.compile(r"(?i)</html\s*>")

# REACHING OUTSIDE THIS MACHINE. Every way a page can LOAD something from
# elsewhere that a regex can see: a src on anything that fetches, a stylesheet
# link, a CSS url() or @import, a script import, fetch/XMLHttpRequest, a socket.
# An <a href> to a website is NOT here -- a link loads nothing until a person
# clicks it. HONEST LIMIT: a URL assembled at runtime from pieces is not seen;
# this closes the ordinary routes, it does not seal the page.
_OUTSIDE = re.compile(r"""(?ix)
      <(?:script|img|iframe|audio|video|source|embed|track|input)\b[^>]*?
          \bsrc\s*=\s*["']?\s*(?:https?:)?//
    | <link\b[^>]*?\bhref\s*=\s*["']?\s*(?:https?:)?//
    | \burl\(\s*["']?\s*(?:https?:)?//
    | @import\s+(?:url\()?\s*["']?\s*(?:https?:)?//
    | \bimport\b[^;\n]{0,120}?\bfrom\s*["'](?:https?:)?//
    | \b(?:fetch|import)\s*\(\s*["'](?:https?:)?//
    | \bXMLHttpRequest\b
    | \bnew\s+(?:WebSocket|EventSource)\s*\(
""")


def page_from(answer: str) -> tuple[str, str]:
    """(the page, "") -- or ("", why it is not one).

    ARITHMETIC ONLY, in three questions: is there a page in the answer (a
    fenced block that opens like HTML, or failing a fence the answer from its
    `<!DOCTYPE html>` on); is it WHOLE (it reaches `</html>` -- a page the
    window cut off is the commonest way a long answer fails, and saving half a
    game is worse than saving none); and does it reach outside this machine.
    """
    text = answer or ""
    body = ""
    for m in _FENCE.finditer(text):
        if _DOC_START.search(m.group(1)):
            body = m.group(1)
            break
    if not body:
        s = _DOC_START.search(text)
        if not s:
            return "", ("the Coder's answer held no web page -- nothing in it "
                        "opens like one (<!DOCTYPE html> or <html>)")
        body = text[s.start():]
    ends = list(_DOC_END.finditer(body))
    if not ends:
        return "", ("the page stops before its end (there is no </html>), which "
                    "is what an answer that ran out of room looks like")
    body = body[:ends[-1].end()]
    hit = _OUTSIDE.search(body)
    if hit:
        shown = " ".join(hit.group(0).split())[:80]
        return "", (f"the page reaches outside this machine ({shown}), and a page "
                    f"made here must work with nothing but this computer (RULE 4)")
    return body.replace("\r\n", "\n").strip("\n") + "\n", ""


# ---------------------------------------------------------------------
# the project: a folder with its own history
# ---------------------------------------------------------------------

def _is_project(project: Path) -> bool:
    """The project's OWN repository, and nothing else, answers for it.

    LOAD-BEARING. projects/ sits inside the ground, and the ground is itself a
    repository: git asked about a folder with no `.git` of its own walks UP
    and answers for the ground. Every read and write below asks this first, so
    the maker can never read the ground's history as a project's, or commit
    into it.
    """
    return (Path(project) / ".git").is_dir()


def new_project(ground, name: str) -> Path:
    """Make `projects/<name>/` with its own empty history and its own signer."""
    root = Path(ground) / PROJECTS
    root.mkdir(exist_ok=True)
    project = _free(root, name)
    project.mkdir()
    # NOT gitstate.init: it asks "is this already a repository?" first, and
    # inside the ground the answer is yes -- the ground's.
    for args in (["init"],
                 ["config", "user.name", AUTHOR_NAME],
                 ["config", "user.email", AUTHOR_EMAIL]):
        rc, _out, err = gitstate._write(args, project)
        if rc != 0:
            raise MakerRefused(f"the project's history could not be started "
                               f"({' '.join(args[:2])}: {err or 'git failed'})")
    if not _is_project(project):
        raise MakerRefused("the project's history could not be started")
    return project


def versions(project) -> list[tuple[int, str, str]]:
    """[(version number, short sha, its note)], oldest first."""
    project = Path(project)
    if not _is_project(project):
        return []
    try:
        rc, out = gitstate._run(["log", "--reverse", "--format=%h%x09%s"], project)
    except RuntimeError:
        return []
    if rc != 0:
        return []
    rows = []
    for line in (l for l in out.splitlines() if l.strip()):
        sha, _, note = line.partition("\t")
        rows.append((len(rows) + 1, sha.strip(), note.strip()))
    return rows


def page_of(project) -> str:
    try:
        return (Path(project) / PAGE).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _note(text: str, cap: int = 72) -> str:
    one = " ".join((text or "").split())
    return one if len(one) <= cap else one[:cap - 3].rstrip() + "..."


def _commit(project: Path, subject: str, sitting: str = "") -> str:
    if not _is_project(project):
        raise MakerRefused("that folder has no history of its own, so nothing "
                           "was saved into it")
    body = "Saved by the maker" + (f", sitting {sitting}" if sitting else "") + "."
    try:
        return gitstate.commit(project, f"{subject}\n\n{body}")
    except gitstate.GitRefused as exc:
        raise MakerRefused(f"the version could not be saved: {exc}")


def save_version(project, page: str, note: str, sitting: str = "") -> int:
    """Write the page and save it as the project's next version. Returns its
    number. The page is written CRLF, as the ground's writers are."""
    project = Path(project)
    n = len(versions(project)) + 1
    (project / PAGE).write_text(page.replace("\r\n", "\n"), encoding="utf-8",
                                newline="\r\n")
    out = _commit(project, f"Version {n}: {_note(note)}", sitting)
    if out.startswith("Nothing to commit"):
        raise MakerRefused("the page came back exactly as it was, so there is "
                           "no new version to save")
    return n


def restore(project, target: int = 0, sitting: str = "") -> tuple[int, int]:
    """Go back to version `target` (0 = the one before this) by saving it
    AGAIN, as a new version. Returns (the new version's number, target).
    History is only ever added to: the version gone back from stays, and can
    itself be gone back to."""
    project = Path(project)
    vs = versions(project)
    now = len(vs)
    if not now:
        raise MakerRefused("this project has no versions yet")
    if target == 0:
        target = now - 1
    if target < 1:
        raise MakerRefused("there is nothing before version 1 to go back to")
    if target > now:
        raise MakerRefused(f"there is no version {target} -- this project has "
                           f"versions 1 to {now}")
    if target == now:
        raise MakerRefused(f"version {now} is the one you have now")
    sha = vs[target - 1][1]
    rc1, then = gitstate._run(["ls-tree", "-r", "--name-only", sha], project)
    rc2, have = gitstate._run(["ls-files"], project)
    rc, _out, err = gitstate._write(["checkout", sha, "--", "."], project)
    if rc != 0 or rc1 != 0 or rc2 != 0:
        raise MakerRefused(f"version {target} could not be brought back "
                           f"({err or 'git failed'})")
    for extra in sorted(set(have.splitlines()) - set(then.splitlines())):
        if extra.strip():
            gitstate._write(["rm", "-q", "--", extra], project)
    out = _commit(project, f"Version {now + 1}: back to version {target}", sitting)
    if out.startswith("Nothing to commit"):
        raise MakerRefused(f"the page you have now is already the same as "
                           f"version {target}")
    return now + 1, target


# ---------------------------------------------------------------------
# the list: picking a project up by name (piece 2)
# ---------------------------------------------------------------------

def projects(ground) -> list[Path]:
    """Every project in the ground, by name: a folder under projects/ with a
    history of its own. A folder without one is not a project and is not
    listed -- the same test every read above makes first."""
    root = Path(ground) / PROJECTS
    try:
        return sorted((p for p in root.iterdir() if p.is_dir() and _is_project(p)),
                      key=lambda p: p.name)
    except OSError:
        return []


def find(ground, words: str) -> list[Path]:
    """The projects these words name. The one whose folder name they make
    ("the snake game" -> snake-game, the rule that named it), or failing that
    every project whose name holds all of the words ("snake" finds
    snake-game). Empty when they name none. Two or more is for the person to
    choose between; nothing here picks one of them on a guess."""
    said = [w for w in re.findall(r"[a-z0-9]+", (words or "").lower())
            if w not in _FILLER and w not in ("project", "projects")]
    if not said:
        return []
    have = projects(ground)
    key = name_for(" ".join(said))
    exact = [p for p in have if p.name == key]
    if exact:
        return exact
    want = set(key.split("-"))
    return [p for p in have if want <= set(p.name.split("-"))]


# ---------------------------------------------------------------------
# what the Coder is asked, and what the person is told
# ---------------------------------------------------------------------

RULES = (
    "- ONE file: the HTML, its CSS and its JavaScript all inside it. No other "
    "files.\n"
    "- Nothing from the internet: no <script src=\"http...\">, no CDN, no web "
    "fonts, no images or sounds from a URL, no fetch. It must work with no "
    "network at all.\n"
    "- It must work by opening the file in a browser. Put short instructions on "
    "the page itself (\"Arrow keys to move\", \"Click to start\").\n"
    "- Complete: every function it calls is defined, and it ends with </html>.\n")

_SHAPE = (f"Answer with exactly this, and nothing after it:\n"
          f"<filepath>{PAGE}</filepath>\n```html\n...the whole page...\n```")


def coder_prompt(make: dict, objective: str) -> str:
    """The Coder's one job for this turn: a whole page, new or changed."""
    if make.get("kind") == "change":
        return (f"Here is the page as it stands -- version {make.get('version')} "
                f"of \"{make.get('name')}\":\n\n```html\n"
                f"{str(make.get('page') or '').rstrip()}\n```\n\n"
                f"THE CHANGE ASKED FOR: {(objective or '').strip()}\n\n"
                f"Rewrite the WHOLE page with that change made, and change "
                f"nothing else.\n{RULES}\n{_SHAPE}")
    return (f"Make this, as ONE complete, self-contained web page:\n\n"
            f"{(objective or '').strip()}\n\n{RULES}"
            f"- Small and finished beats big and half-done.\n\n{_SHAPE}")


def _where(project) -> str:
    return f"{PROJECTS}\\{Path(project).name}\\{PAGE}"


def report_made(project, lines: int) -> str:
    name = Path(project).name
    return (f"Made {name} -- version 1.\n\n"
            f"It is one page, {PAGE} ({lines} lines), in {PROJECTS}\\{name}\\ "
            f"with its own history. To try it, open {_where(project)} in your "
            f"browser.\n\n"
            f"What next? Ask for a change in plain words -- \"make it faster\", "
            f"\"add a score\" -- and it becomes version 2. \"Go back\" returns to "
            f"an earlier version, and nothing is ever thrown away.")


def report_changed(project, n: int, lines: int, was: int, note: str) -> str:
    name = Path(project).name
    return (f"Changed {name} -- version {n}: {_note(note)}\n\n"
            f"{PAGE} is now {lines} lines (it was {was}). Open {_where(project)} "
            f"again to see it.\n\n"
            f"Say \"go back\" to return to version {n - 1}, or ask for the next "
            f"change.")


def report_back(project, n: int, target: int) -> str:
    name = Path(project).name
    listing = "\n".join(f"  {i}  {note.split(': ', 1)[-1]}"
                        for i, _sha, note in versions(project)[-6:])
    return (f"{name} is back to version {target} -- saved as version {n}, so "
            f"nothing was lost.\n\nIts versions:\n{listing}\n\n"
            f"Open {_where(project)} to see it.")


def report_unsaved(why: str) -> str:
    return (f"Nothing was saved: {why}.\n\n"
            f"The Coder's whole answer is in this run's record. Ask again, or say "
            f"it a different way.")


def report_too_big(project, size: int) -> str:
    return (f"Nothing was changed: {Path(project).name}'s page is {size:,} "
            f"characters, and a change is made by rewriting the whole page -- "
            f"which the Coder's window cannot hold past about "
            f"{CHANGE_LIMIT:,}. That is a limit of this first version of the "
            f"maker, not of your request.")


def report_picked(project, already: bool = False) -> str:
    name = Path(project).name
    vs = versions(project)
    head = (f"You are already working on {name}" if already
            else f"Working on {name} now")
    if not vs:
        return (f"{head}. It has no versions yet -- nothing was ever saved "
                f"into it.\n\nSay \"put it down\" to set it aside.")
    listing = "\n".join(f"  {i}  {note.split(': ', 1)[-1]}"
                        for i, _sha, note in vs[-6:])
    return (f"{head} -- it is at version {len(vs)}.\n\nIts versions:\n"
            f"{listing}\n\nOpen {_where(project)} to see it. Ask for a change "
            f"in plain words and it becomes version {len(vs) + 1}; say \"put it "
            f"down\" when you are done with it.")


def report_put_down(project) -> str:
    name = Path(project).name
    return (f"Put {name} down. It is kept exactly as it is -- version "
            f"{len(versions(project))}, in {PROJECTS}\\{name}\\ -- and nothing "
            f"is in hand now.\n\nAsk for something new to be made, or say "
            f"\"work on {name}\" to pick it up again.")


def _named(have) -> str:
    return ", ".join(p.name for p in have)


def report_nothing_in_hand(have) -> str:
    listing = (f" The projects here: {_named(have)}." if have
               else " There are no projects here yet.")
    return (f"No project is in hand, so there is nothing to put down.{listing}")


def report_which(found) -> str:
    return (f"More than one project answers to that: {_named(found)}. Say "
            f"which one -- \"work on {found[0].name}\".")


def report_no_such(words: str, have) -> str:
    if not have:
        return (f"There is no project called \"{words}\" -- there are no "
                f"projects here yet. Ask for something to be made: \"make me a "
                f"snake game\".")
    return (f"There is no project called \"{words}\". The projects here: "
            f"{_named(have)}.")
