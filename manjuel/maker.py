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

ALL THREE PIECES (BUILDPATH, "The maker"). Piece 2 is the page on the glass:
the door's `projects` tool reads each project's own history for the Dashboard's
list and serves a page into a sandboxed preview, and the words below (`find`,
the pick-up and put-down reports) are how a project is picked up from that list
-- or put down -- in a sitting.

PIECE 3 IS THE CHECK THAT RUNS IT (2026-09-22). `page_from` proves a page is
WHOLE and LOCAL -- arithmetic over the bytes, and all arithmetic can prove. It
cannot prove the page WORKS, because nothing had run it: version 1 of the snake
game called `clearInterval(game)` with no `game` declared, and was saved. So
the page is now loaded in a browser with no window before a version is kept,
and what it throws goes back to the Coder for one more try. `run_page` and the
section it heads carry the how and the honest limits.

AND IT IS THE ESTATE'S FIRST LAWFUL LOOP (LAW_003, 2026-09-17, which made one
lawful and which nothing had yet used). Its three bounds, all three: a declared
ceiling (`REPAIRS`, and the loop that reads it is `pipeline._maker_prove`), a
stop condition a MACHINE checks (the browser's own error events -- never a
seat's account of its own work), and every pass in the record (each check is a
note; each repair is a step with the seat's answer in it).
"""

from __future__ import annotations

import http.server
import json
import os
import re
import shutil
import socketserver
import subprocess
import tempfile
import threading
import time
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
# the check that RUNS it (piece 3, 2026-09-22, his word: "let's build piece 3")
# ---------------------------------------------------------------------
#
# WHAT page_from PROVES, AND WHAT IT DOES NOT. It proves a page is WHOLE and
# LOCAL -- arithmetic over the bytes. It cannot prove the page WORKS, because
# nothing here ran it. Seen live 2026-09-21: version 1 of the snake game called
# `clearInterval(game)` with no `game` declared. Whole, local, saved, and
# broken -- harmless only because the Game Over alert reloaded the page.
#
# SO THE PAGE IS LOADED IN A BROWSER WITH NO WINDOW, and what it throws is sent
# back to the Coder for ONE more try (BUILDPATH, "The maker", piece 3). That
# makes this the estate's first lawful loop under LAW_003: a DECLARED CEILING
# (one repair, `REPAIRS`), a STOP CONDITION A MACHINE CHECKS (the browser's own
# error events, not a seat's account of its work), and EVERY PASS IN THE RECORD
# (the pipeline appends a step for the repair, and the notes carry both checks).
#
# THE BROWSER IS ALREADY ON THIS MACHINE (RULE 4, and his ruling 2026-09-22:
# Edge first, Chrome as fallback). Edge ships with Windows and cannot really be
# removed, so the check survives a machine where Chrome was uninstalled.
# NOTHING IS DOWNLOADED, and no browser is installed by this estate ever.
#
# HOW THE ERRORS COME BACK, and why it is not a debugging protocol. A browser
# cannot write a file, so the page is SERVED -- from `http.server` on 127.0.0.1
# with a port the OS picks -- and a small catcher is injected ahead of the
# page's own scripts, which POSTs every uncaught error, rejected promise,
# failed load and `console.error` back to that server. stdlib only: driving
# CDP would want a websocket client the standard library does not have, and a
# package for it is a dependency the whole estate would then carry.
#
# HONEST LIMITS, written down rather than discovered later:
#
#   IT SEES A MOMENT, NOT A GAME. The page is loaded, given `SETTLE` seconds
#   and closed. Nothing clicks, types or presses an arrow, so a fault that only
#   appears once someone plays is not caught. This proves a page LOADS and runs
#   its own setup without throwing; it does not prove the game is any good.
#
#   IT FAILS OPEN, by name. No browser found, a launch that fails, a page that
#   never signals it loaded -- each returns a REASON, and the caller saves the
#   version anyway and says the check did not run. A gate that silently passes
#   what it could not read is worse than no gate (`inspect_code`'s own ruling).
#
#   THE PAGE IS SERVED, NOT OPENED FROM DISK. `file://` and `http://` differ on
#   storage and module loading, so a page that works here could behave a little
#   differently opened from `projects\`. Serving is what lets the errors come
#   back at all, and it is the same way the glass shows a page (piece 2).
#
#   THE BROWSER IS THE BROWSER'S. Its own background chatter is suppressed by
#   the flags below as far as flags can; this estate does not audit Edge.

# The ceiling, and it is the whole of LAW_003's first bound: ONE repair pass.
REPAIRS = 1
# Seconds the page is given AFTER its load event, for setup that runs on a
# timer. Measured 2026-09-22: a clean page answers in ~2.2s end to end.
SETTLE = 1.2
# LAW 7, bounded everything: the whole check, browser launch included.
CHECK_BUDGET = 25.0
# What counts as BROKEN and buys the repair pass. A `console.error` is reported
# when it happens and does not spend the try: a page may print one on purpose,
# and these three are the ones that mean the page did not do what it meant to.
BREAKING = ("error", "promise", "resource")

# Edge first, Chrome second -- his ruling, 2026-09-22.
_BROWSERS = (
    (r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe", "Edge"),
    (r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe", "Edge"),
    (r"%ProgramFiles%\Google\Chrome\Application\chrome.exe", "Chrome"),
    (r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe", "Chrome"),
    (r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe", "Chrome"),
)


PROFILE_PREFIX = "maker-check-"
# Well past CHECK_BUDGET, so a check running RIGHT NOW is never swept out from
# under itself -- the sweep below judges by age and nothing else.
PROFILE_STALE = 600.0


def _drop_profile(path, tries: int = 6, gap: float = 0.4) -> bool:
    """Remove the browser's profile, waiting for the browser to let go of it.

    THE BACKSTOP, not the cure. The cure is that THE PAGE CLOSES ITSELF: the
    catcher calls `window.close()` after its beacon, and a headless Chromium
    whose last tab closes exits its whole tree on its own.

    EARNED THE DAY THIS WAS BUILT (2026-09-22), and the measurement is the
    reason the cure is where it is. `child.terminate()` kills the LAUNCHER
    only; Chromium's browser, renderers, GPU and crash handler are a process
    TREE that outlives it. Measured both ways on one page: with terminate
    alone, 16 processes still alive 5.5s later and the profile still locked --
    and across an afternoon of strokes, 138 leaked browser processes holding 17
    profiles, about 7 MB each. With `window.close()`, zero processes and the
    profile gone at once. This retry covers the page that never loaded, where
    there is no script left to close anything.
    """
    for _ in range(max(1, tries)):
        shutil.rmtree(path, ignore_errors=True)
        if not Path(path).exists():
            return True
        time.sleep(gap)
    return not Path(path).exists()


def _made_at(d: Path) -> float:
    """When a profile was made, read from ITS OWN NAME.

    NOT from its mtime, and that is the whole point. A profile still held by a
    browser is only PARTLY removed by a sweep, which updates the directory's
    mtime -- so a locked profile looked younger after every attempt and could
    never become stale enough to sweep. Measured 2026-09-22: 154 of them, none
    ever older than ten minutes by their own clock, because the sweep kept
    resetting it. A time in the name is a clock nothing here can touch.
    """
    try:
        return float(d.name[len(PROFILE_PREFIX):].split("-", 1)[0])
    except (ValueError, IndexError):
        try:                            # a name from before the time was in it
            return d.stat().st_mtime
        except OSError:
            return 0.0


def _sweep_profiles(older_than: float = PROFILE_STALE) -> int:
    """Remove profiles an earlier run could not, and say how many went.

    The page closing itself is the cure; this is the backstop, because a delete
    that fails anyway must never accumulate. Judged by AGE alone, so it cannot
    take a live check's profile, and bounded by the disk: one folder, one
    prefix.
    """
    gone, now = 0, time.time()
    try:
        entries = list(Path(tempfile.gettempdir()).glob(PROFILE_PREFIX + "*"))
    except OSError:
        return 0
    for d in entries:
        try:
            if not d.is_dir() or now - _made_at(d) < older_than:
                continue
        except OSError:
            continue
        shutil.rmtree(d, ignore_errors=True)
        gone += 0 if d.exists() else 1
    return gone


def browser() -> tuple[str, str]:
    """(the path to a headless-capable browser, its name), or ("", "").

    Read off the disk every call: a browser uninstalled between two turns must
    not be remembered as present. Nothing is installed and nothing downloaded.
    """
    for raw, name in _BROWSERS:
        p = os.path.expandvars(raw)
        if "%" not in p and Path(p).is_file():
            return p, name
    return "", ""


# The catcher. It is injected AHEAD of the page's own scripts and BEHIND the
# doctype -- content before `<!DOCTYPE html>` puts the browser in quirks mode,
# which would have this check testing a page the person will never see.
_CATCH = """<script>
(function(){
 function post(to,p){try{
  if(navigator.sendBeacon&&navigator.sendBeacon(to,p||''))return;
  var x=new XMLHttpRequest();x.open('POST',to,false);
  x.setRequestHeader('Content-Type','text/plain');x.send(p||'');}catch(e){}}
 function err(p){post('/__err',JSON.stringify(p));}
 window.addEventListener('error',function(e){
  err({kind:e.message?'error':'resource',line:e.lineno||0,
       text:String(e.message||('could not load '+((e.target&&(e.target.src||e.target.href))||'a file')))});},true);
 window.addEventListener('unhandledrejection',function(e){
  err({kind:'promise',line:0,text:String((e.reason&&e.reason.message)||e.reason)});});
 var ce=console.error;console.error=function(){
  err({kind:'console',line:0,text:Array.prototype.join.call(arguments,' ')});
  return ce.apply(console,arguments);};
 window.addEventListener('load',function(){setTimeout(function(){
  post('/__done');window.close();},SETTLE_MS);});
})();
</script>"""
_CATCH_LINES = _CATCH.count("\n")

_HEAD_OPEN = re.compile(r"(?i)<head\b[^>]*>")
_HTML_OPEN = re.compile(r"(?i)<html\b[^>]*>")
_DOCTYPE = re.compile(r"(?i)<!doctype\s+html[^>]*>")


def _inject(page: str, settle: float) -> tuple[str, int]:
    """(the page with the catcher in it, how many lines it pushed things down).

    The offset is subtracted from every reported line number, so the Coder is
    told where the fault is in ITS OWN page and not in the served copy.
    """
    catch = _CATCH.replace("SETTLE_MS", str(int(max(0.0, settle) * 1000)))
    for rx in (_HEAD_OPEN, _HTML_OPEN, _DOCTYPE):
        m = rx.search(page)
        if m:
            return page[:m.end()] + catch + page[m.end():], _CATCH_LINES
    return catch + page, _CATCH_LINES


def run_page(page: str, settle: float = SETTLE,
             budget: float = CHECK_BUDGET) -> tuple[bool, list[dict], str]:
    """Load `page` in a browser with no window. (loaded, faults, why-not).

    `why-not` is "" when the check really ran. Anything else is a reason it
    could not, and the caller saves anyway and says so -- this never blocks a
    version on its own inability to look.
    """
    exe, _name = browser()
    if not exe:
        return False, [], ("no browser was found on this machine to run it in "
                           "(Edge or Chrome); nothing was downloaded to get one")

    served, offset = _inject(page, settle)
    body = served.encode("utf-8")
    faults: list[dict] = []
    done = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):        # a check is not a web server's log
            pass

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n).decode("utf-8", "replace") if n else ""
            if self.path == "/__done":
                done.set()
            else:
                try:
                    row = json.loads(raw)
                except ValueError:
                    row = {"kind": "error", "line": 0, "text": raw[:400]}
                if isinstance(row, dict):
                    faults.append(row)
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    try:
        srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
    except OSError as exc:
        return False, [], f"the page could not be served to a browser ({exc})"
    srv.daemon_threads = True
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    _sweep_profiles()            # whatever an earlier run could not let go of
    # THE TIME GOES IN THE NAME. See `_made_at`: a directory's mtime is not a
    # clock a sweep can trust, because the sweep itself moves it.
    profile = tempfile.mkdtemp(prefix=f"{PROFILE_PREFIX}{int(time.time())}-")
    child = None
    why = ""
    try:
        try:
            child = subprocess.Popen(
                [exe, "--headless=new", "--disable-gpu", "--no-first-run",
                 "--no-default-browser-check", "--disable-extensions",
                 "--disable-background-networking", "--disable-sync",
                 "--disable-component-update", "--no-service-autorun",
                 "--user-data-dir=" + profile, f"http://127.0.0.1:{port}/"],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        except OSError as exc:
            return False, [], f"the browser would not start ({exc})"
        loaded = done.wait(max(1.0, budget))
        if not loaded:
            why = (f"the page never finished loading inside {budget:.0f}s, so "
                   f"what it does is still unknown")
    finally:
        if child is not None:
            child.terminate()
            try:
                child.wait(5)
            except subprocess.TimeoutExpired:
                child.kill()
        srv.shutdown()
        srv.server_close()
        _drop_profile(profile)

    for f in faults:                       # the Coder's own line numbers
        try:
            f["line"] = max(0, int(f.get("line") or 0) - offset)
        except (TypeError, ValueError):
            f["line"] = 0
    return (not why), faults, why


def breaking(faults) -> list[dict]:
    """The faults that mean the page did not do what it meant to."""
    return [f for f in (faults or []) if f.get("kind") in BREAKING]


def said_faults(faults, cap: int = 4) -> str:
    """The faults in one line a person can read. Deduped: a page that throws
    the same error on a timer throws it many times, and that is one fault."""
    seen, out = set(), []
    for f in faults or []:
        text = " ".join(str(f.get("text") or "").split())[:160]
        if not text or text in seen:
            continue
        seen.add(text)
        where = f" (line {f['line']})" if f.get("line") else ""
        out.append(text + where)
    more = f" and {len(out) - cap} more" if len(out) > cap else ""
    return "; ".join(out[:cap]) + more


def repair_prompt(page: str, faults, objective: str) -> str:
    """The Coder's ONE more try: its own page back, with what the browser said.

    The faults are quoted as the BROWSER's words, not described -- a seat told
    "it didn't work" guesses, and a seat given `game is not defined` at line 42
    fixes a line.
    """
    listing = "\n".join(
        f"  - {' '.join(str(f.get('text') or '').split())[:200]}"
        + (f"  (line {f['line']})" if f.get("line") else "")
        for f in (faults or [])[:8])
    return (f"This page was loaded in a browser and it reported errors. Here "
            f"is the page:\n\n```html\n{(page or '').rstrip()}\n```\n\n"
            f"WHAT THE BROWSER REPORTED:\n{listing}\n\n"
            f"Fix ONLY what those errors name. Change nothing else -- not the "
            f"look, not the rules of the game, not anything that was already "
            f"working. It was asked for: {(objective or '').strip()}\n\n"
            f"Rewrite the WHOLE page with the fix in it.\n{RULES}\n{_SHAPE}")


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


def _trouble(said: str) -> str:
    """The check's word, as a paragraph, or nothing at all.

    HIS RULING, 2026-09-22: a page that still errors after its one repair is
    SAVED and the report SAYS SO. She asked for a game and gets one she can
    open; `page_from` already refuses what is genuinely fatal, and the fault
    that started this piece was a real error in a perfectly playable game.
    """
    return f"\n\n{said}" if said else ""


def report_made(project, lines: int, trouble: str = "") -> str:
    name = Path(project).name
    return (f"Made {name} -- version 1.\n\n"
            f"It is one page, {PAGE} ({lines} lines), in {PROJECTS}\\{name}\\ "
            f"with its own history. To try it, open {_where(project)} in your "
            f"browser."
            + _trouble(trouble) + "\n\n"
            f"What next? Ask for a change in plain words -- \"make it faster\", "
            f"\"add a score\" -- and it becomes version 2. \"Go back\" returns to "
            f"an earlier version, and nothing is ever thrown away.")


def report_changed(project, n: int, lines: int, was: int, note: str,
                   trouble: str = "") -> str:
    name = Path(project).name
    return (f"Changed {name} -- version {n}: {_note(note)}\n\n"
            f"{PAGE} is now {lines} lines (it was {was}). Open {_where(project)} "
            f"again to see it."
            + _trouble(trouble) + "\n\n"
            f"Say \"go back\" to return to version {n - 1}, or ask for the next "
            f"change.")


def said_checked(ran: bool, why: str, faults, repaired: bool) -> str:
    """What the check found, for the person, in one paragraph -- or "" when it
    ran and the page was clean, which needs no words at all."""
    if not ran:
        return (f"One thing to know: it was not opened in a browser first -- "
                f"{why}. It is saved as it was written.")
    bad = breaking(faults)
    if not bad and not faults:
        return ""
    if not bad:
        return (f"It opened cleanly. One note from the browser: "
                f"{said_faults(faults)}.")
    head = ("It still reports an error after one repair"
            if repaired else "It reports an error")
    return (f"One thing to know: {head} -- {said_faults(bad)}. It is saved "
            f"anyway so you can see it; a page can report an error and still "
            f"play. Ask for a change in plain words and it can be fixed.")


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
