"""The test pack: the wife test run the way a person would run it, and three eras of
the operator's own sessions run again on today's engine, the evidence set beside
the old record.

    python tests/pack.py --check                     the wires, offline: no models, no sandbox
    python tests/pack.py --runner                    the JS that hands lines to the glass page's own go() (live method)
    python tests/pack.py --lines CASE                a case's lines for it, as JSON (W1 W2 A79 A70 B170 C221)
    python tests/pack.py --record 336=W1,337=W2,...   judge sittings the system ran LIVE, from its own record, read-only
    python tests/pack.py --probe FILE.html           one page, played in the maker's headless browser
    python tests/pack.py --list                      every case and turn, with the route the engine's
                                                     own arithmetic reads for each; nothing runs
    python tests/pack.py --sandbox DIR               every case, LIVE, each in a clone made under DIR
    python tests/pack.py --sandbox DIR --only W,A79  the cases whose key contains "W" or "A79"
    python tests/pack.py --sandbox DIR --keep        leave the clones (ledger, transcripts, projects) to read

THE ASK, 2026-10-03: "make a full mockup of the wife test, run the system under an
early session or sitting, say around 60-90 range and then again at 150-180 and again
in the 220-250 range. try to get a session with at least a few turns involved. make it
like a test pack or debug pass."

HOW IT IS READ. Not as three checkouts of old code: the engine here is TODAY's, and what
comes from the three eras is what a person actually SAID. A case is a conversation:

    W1   the wife test as the flow stands -- flows/wife-test.json's three lines, verbatim
    W2   the wife test as a fuller mock: a person who is not him, in her own words, a dozen
         turns -- a greeting, a game, a question, a complaint said as a complaint, a change
         said as a change, a wish to go back said two ways, a thanks, a second thing, and
         the words for finding the first one again. Some are in the engine's grammar and
         some are how people talk; the report keeps the two apart
    A79  sitting 79 (2026-09-03): fifteen turns, a morning chat, the docs, an index rebuild
    A70  sitting 70 (2026-09-02): five turns of plain talk -- the nearest thing the ledger has
         to a person who is not the operator
    B170 sitting 170 (2026-09-10): five turns, the only conversation in 150-180 (the rest
         are the morning standup)
    C221 sitting 221 (2026-09-14): nine turns, the morning set (the standup, so the injection
         and law gates are in it)
    S0   the pack's own smoke: two plain turns, to prove the machinery before anything long

EVERY CASE RUNS IN A CLONE. The clone is the tracked tree plus the state the engine needs
(memory.md, the memory chain, SEAT_LOG.md, the index), with its OWN .git and its OWN ledger,
cut to the lines before the replayed sitting so the engine itself opens it as that number
("run under sitting 79"). It has no .env (RULE 7 -- dials at their defaults, the two the
template names set; no route is on, so nothing can leave, RULE 4), no logs/, no worlds/, no
atlas/, no projects/. Whatever the engine writes -- memory, commits, the toll, projects --
lands in the clone. An isolation probe refuses to start an engine whose code would come from
the ground, and the sandbox must be a directory the pack owns (a marker file) outside it.

THE OLD RECORD is read, never written: the ledger's run lines and the transcripts in logs/
they point at. A sitting whose lines carry the client tag is refused by name and never opened
(SITTING LAW 2).

WHAT IT JUDGES is mechanical, in the standup's tradition (tests/standup.py, whose constants and
number check it uses): a terminal that is not the one expected; markup in a delivery; a seat that
failed or ran out of time; a tool that did not run; a number no tool returned; a recital of what
the seat was handed; and, for the maker, the engine's own record of what moved (a project, a
version) beside what the persona WANTED. What the words were worth is the reviewer's, and the
report leaves it open. The page a maker turn saves is also PLAYED in the maker's own headless
browser by a probe -- which handlers the page registered, whether they ran on keys and clicks, whether
anything changed -- so "she can see it and play it" has evidence behind it.

WHAT IT IS NOT. Not the system as it was (that is old commits). Not the glass: whether she can find
the result, press play, read the card, is a scratch pair's to walk, not this.

THE REPORT is written to the sandbox, and into the ground's logs/ only while no sitting is open
(RULE 9: logs/ is an index root). Nothing else in the ground is touched.

WHAT GOES RED IF THIS COMES UNPLUGGED (RULE 11): `--check` is read by the stroke
`test_the_pack_is_wired`, and it holds the pack to the engine's wire (serve.COMMANDS/EVENTS/
TERMINAL), to the maker's grammar (the routes each persona line is declared to take), to the
transcript shape, to the standup's constants, to the ledger's picked sittings (when the ledger is
on the disk), and to the sandbox's own refusals.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import hashlib
import io
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT), str(ROOT / "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from manjuel import intent, maker, seatlog, serve, transcript, vectors   # noqa: E402
from manjuel.pipeline import recited                                      # noqa: E402
import standup                                                            # noqa: E402

LOGS = ROOT / "logs"
FLOW = ROOT / "flows" / "wife-test.json"

MARK = ".pack-sandbox"
CAP = 900.0                  # seconds a turn may take before the pack cancels it (a flow's own budget is 900)
BOOT_CAP = 600.0             # seconds the engine may take to say `opened`
CLOSE_CAP = 240.0            # seconds the sitting may take to close and pay its toll

# What the engine needs that git does not carry (the .gitignore keeps these out of the tree). The index is
# derived state, copied so semantic_search works as it does on the ground; .env is NEVER on this list.
STATE = ("memory.md", "memory/chain.jsonl", "SEAT_LOG.md", "SEAT_LOG_INDEX.md", "index/vectors.db")
# The two dials .env.example names, set by name; nothing else of .env is reproduced.
DIALS = {"MANJUEL_KEEP_ALIVE": "30m", "MANJUEL_VRAM_GB": "15"}
# Nothing of the caller's environment that could carry a key, a route or the door to the engine.
DROP_PREFIXES = ("MANJUEL_MCP_", "MANJUEL_ROUTE_", "CHAINKIT_", "ATLAS_")
DROP_WORDS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL")

USED_COMMANDS = ("objective", "answer", "cancel", "close")
USED_EVENTS = ("opened", "needs_answer", "tool", "tool_result", "delivery", "refused", "aborted",
               "cancelled", "unreachable", "error", "closed", "text", "command")

WANTS = ("", "make", "change", "back", "pick", "put-down")
ROUTES = ("", "make", "change", "go-back", "pick", "pick-none", "put-down", "*")

# The shapes that mean a delivery is telling a person who does not use a terminal to use one.
TERMINAL_TALK = re.compile(
    r"(?i)\b(?:open (?:a |the )?(?:terminal|command prompt|powershell|console)|command line|"
    r"run (?:the following|this command)|pip install|npm (?:install|run)|python3? [\w./\\-]+\.py|"
    r"cd [\w./\\:-]+|open `?[\w./\\:-]+\.html?)\b")

# THE MACHINERY, SHOWING (2026-10-03, the development pass). Words that are the engine's own scaffolding and
# never a person's: a flag taken out of a sentence leaves an empty pair of backticks; the headings the seats are
# handed; the proofreader's frame. A reply carrying one has shown her the works.
LEAKS = re.compile(
    r"(?<!`)``(?!`)|\A\s*SAFE\b|(?m:^\s*## Now\b)|(?i:\bobjective above\b|\bno source material\b|<flags|flags>|"
    r"\bthe chain behind (?:me|you)\b|\bcorrected (?:text|objective)\b|\bages and dates you are shown\b)")
# ...and the ones a delivery ABOUT the docs may say honestly, so they are only seen, unless the turn was a chat.
LEAKS_SOFT = re.compile(r"(?i)\boriginal objective\b|\bconversation so far\b|\bneeds_tool\b")
# The engine's own tool wrapper, shown raw: what a closing seat that was discarded leaves behind.
TOOLSPEAK = re.compile(r"Tool executed:|testimony, not tool output")
# The engine's own confession, machine-emitted into a delivery when it compared what was named with what ran.
ENGINE_SAYS = re.compile(r"THE NAMED TOOL DID NOT RUN")
# SPOKEN ABOUT, NOT TO: a reply that talks of "the operator" in the third person to someone who is chatting, or
# that answers a chat with the report card the closing seat writes for a tool turn.
ABOUT = re.compile(r"(?i)\bthe operator(?:'s)?\b")
CARD = re.compile(r"(?m)^\s*(?:What happened|Result|Open)\s*:")
# A promise nothing keeps: the reply offers to do the thing and, in the same breath, does not.
PROMISE = re.compile(r"(?i)\bI(?:'ll| will| can)\b[^.?!]{0,40}\b(?:make|change|add|fix|build|create|update|enlarge)\b")

# How a question the engine puts to a person is answered, in the order tried. The pack answers as a
# willing person would; every question and its answer is in the report, because a question put to
# the wife is a finding.
ANSWERS = (
    (re.compile(r"retry / skip / abort"), "s"),
    (re.compile(r"\[l\]and"), "d"),
    (re.compile(r"kind \("), ""),
    (re.compile(r"title \("), ""),
)


# ---------------------------------------------------------------------
# the cases
# ---------------------------------------------------------------------

@dataclass
class Turn:
    say: str
    feed: str = ""
    why: str = ""                    # what this turn is FOR
    wants: str = ""                  # what she WANTS done (persona turns): one of WANTS
    route: str = "*"                 # what the engine's arithmetic is declared to read: ROUTES; "*" = depends on the sitting's state
    expect_tools: tuple = ()
    expect_no_tools: bool = False
    expect_refused: bool = False
    expect_own_words: bool = False
    unattended: bool = False
    skip: str = ""                   # a turn the pack does not replay, and why
    then: dict | None = None         # the old record's facts for this turn (replays)


@dataclass
class Case:
    key: str
    title: str
    source: str
    turns: list
    sitting: int | None = None       # the clone's ledger is cut so the engine opens THIS number
    wife: bool = False
    note: str = ""


# The persona. Her words, not his: invented by the hand (the flow's three lines are the only ones that are
# not). `route` is what the engine's arithmetic is declared to read for the words ("*" where it depends on
# what is in hand or on disk); `--check` holds the declaration to the engine, so a grammar that moves is
# seen before a run, and the live run holds the observation to the prediction.
def persona() -> list[Turn]:
    return [
        Turn("hi! my husband said you can make things for me?",
             why="a greeting and a question, the way anyone opens; nothing should wake a tool",
             route="", expect_no_tools=True, expect_own_words=True),
        Turn("can you make me a little game? something like minecraft where i can build stuff with blocks",
             why="the ask, in her words", wants="make", route="make"),
        Turn("ok how do i play it?",
             why="she was handed a result and does not know where it is or how to start it",
             route=""),
        Turn("the blocks are too small",
             why="a complaint said as a complaint: the engine reads only a change verb at the front as a change",
             wants="change", route=""),
        Turn("can you make the blocks bigger",
             why="the same want, in the engine's grammar", wants="change", route="change"),
        Turn("add some different colors please",
             why="a second change", wants="change", route="change"),
        Turn("actually i liked it better before",
             why="going back, said the way people say it", wants="back", route=""),
        Turn("can you put it back how it was",
             why="going back, in the engine's grammar", wants="back", route="go-back"),
        Turn("thank you so much!",
             why="thanks wake nothing", route="", expect_no_tools=True, expect_own_words=True),
        Turn("can you make me a recipe tool where i can save my recipes",
             why="a second, different thing while the first is in hand", wants="make", route="make"),
        Turn("ok can we go back to the minecraft one",
             why="she names the first by what she asked for; the project was named from `little game`",
             wants="pick", route="*"),
        Turn("work on the game",
             why="the engine's words for finding a project again", wants="pick", route="*"),
        Turn("ok i'm done for today, thanks",
             why="she is finished, said her way", wants="put-down", route=""),
    ]


def flow_turns() -> list[Turn]:
    """The wife test's own three lines, verbatim, from the flow that carries them."""
    flow = json.loads(FLOW.read_text(encoding="utf-8"))
    lines = [n["question"] for n in flow.get("nodes", []) if n.get("kind") == "run" and n.get("question")]
    if len(lines) != 3:
        raise ValueError(f"{FLOW.name} holds {len(lines)} lines she says, not three")
    return [
        Turn(lines[0], why="the flow's first line: the ask", wants="make", route="make", unattended=True),
        Turn(lines[1], why="the flow's second line: a change to what she was given",
             wants="change", route="change", unattended=True),
        Turn(lines[2], why="the flow's third line: thanks", route="", expect_no_tools=True,
             expect_own_words=True, unattended=True),
    ]


SMOKE = (Turn("good morning", why="a plain turn wakes nobody", route="", expect_no_tools=True,
              expect_own_words=True),
         Turn("what is in the skills dir", why="one tool, one answer", route="",
              expect_tools=("ground_list",)))

# The sittings replayed: the ranges he named, the fullest real conversation in each.
PICKS = (("A79", 79), ("A70", 70), ("B170", 170), ("C221", 221))
ERAS = {"A": "sittings 60-90", "B": "sittings 150-180", "C": "sittings 220-250"}


def ledger(root: Path = ROOT) -> dict:
    """The ledger's last line for each sitting number (a closing line supersedes an opening one)."""
    last: dict = {}
    p = Path(root) / seatlog.SESSIONS
    if not p.is_file():
        return last
    for line in p.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and isinstance(row.get("n"), int):
            last[row["n"]] = row
    return last


def protected(text: str) -> bool:
    """The client tag, a vault path, a .client. file: never opened, never named (SITTING LAW 2)."""
    return bool(vectors.CLIENT_TOKEN in text or re.search(r"(?i)\bvault[\\/]", text) or ".client." in text.lower())


def then_of(root: Path, run: dict) -> dict:
    """What the old record says of one run: the ledger's line and the transcript it points at."""
    t = {"elapsed": float(run.get("elapsed") or 0.0), "failed": int(run.get("failed") or 0),
         "stages": run.get("stages"), "transcript": run.get("transcript") or "",
         "tools": list(run.get("tools") or []), "delivery": "", "notes": [], "have": False}
    path = Path(root) / t["transcript"] if t["transcript"] else None
    if path is not None and path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
        if protected(text):
            return {"protected": True}
        t["have"] = True
        d = transcript._DELIVERY_RE.search(text)
        t["delivery"] = d.group("t").strip() if d else ""
        t["notes"] = re.findall(r"^- \*\*note:\*\* (.+)$", text, re.M)
        if not t["tools"]:
            names: set = set()
            for m in re.findall(r"skills: ([A-Za-z0-9_, ]+?)\s*(?:·|$)", text, re.M):
                names |= {x.strip().rstrip("_") for x in m.split(",") if x.strip().rstrip("_")}
            t["tools"] = sorted(names)
    return t


# THE TURNS THAT ARE SMALL TALK, read by the hand from the transcripts (2026-10-03): a person talking, not asking for
# work. They are judged as a chat is -- the seat's own words, TO him, no machinery, no "the operator" -- where a
# tool turn is the engine's voice. The ledger of that era recorded no tools, so nothing here can be read off it.
SMALL_TALK = {79: (1, 2, 3), 70: (1,)}


def replay_turns(root: Path, n: int) -> list[Turn]:
    """One real sitting's turns, as he typed them, each with the old record's facts beside it."""
    row = ledger(root).get(n)
    if not row or not row.get("runs"):
        raise ValueError(f"sitting {n} is not in the ledger with runs")
    if protected(json.dumps(row, ensure_ascii=False)):
        raise ValueError(f"sitting {n} carries client material; it is not opened (SITTING LAW 2)")
    known = {c.objective.strip().lower(): c for c in standup.CASES}
    out = []
    for run in row["runs"]:
        say = str(run.get("objective") or "")
        then = then_of(root, run)
        if then.get("protected"):
            raise ValueError(f"a transcript of sitting {n} carries client material; it is not opened")
        t = Turn(say, then=then, why=f"sitting {n}, run {len(out) + 1}")
        c = known.get(say.strip().lower())
        if c is not None:                      # the standup's own expectations and feed for the same words
            t.feed, t.expect_refused = c.feed, c.expect_refused
            t.expect_tools, t.expect_no_tools = tuple(c.expect_tools), c.expect_no_tools
            t.expect_own_words = c.expect_own_words
        if len(out) + 1 in SMALL_TALK.get(n, ()):      # small talk is judged as small talk
            t.expect_own_words = True
        if " ".join(say.lower().split()) == "pay the toll":
            t.skip = "the engine pays an unattended toll when the pack closes the sitting"
        out.append(t)
    return out


def build_cases(root: Path = ROOT, only: str = "") -> list[Case]:
    cases = [Case("S0", "the pack's own smoke", "two plain turns", list(SMOKE),
                  note="proves the machinery before anything long")]
    if FLOW.is_file():
        cases.append(Case("W1", "the wife test as the flow stands", f"flows/{FLOW.name}, verbatim",
                          flow_turns(), wife=True))
    cases.append(Case("W2", "the wife test, a fuller mock", "the hand's persona (invented)", persona(), wife=True))
    for key, n in PICKS:
        try:
            cases.append(Case(key, f"sitting {n} ({ERAS[key[0]]})", f"ledger sitting {n}",
                              replay_turns(root, n), sitting=n))
        except ValueError as exc:
            cases.append(Case(key, f"sitting {n}", f"ledger sitting {n}", [], sitting=n, note=f"REFUSED: {exc}"))
    names = [x.strip().lower() for x in only.split(",") if x.strip()]
    return [c for c in cases if any(x in c.key.lower() for x in names)] if names else cases


# ---------------------------------------------------------------------
# the engine's arithmetic, asked before the run
# ---------------------------------------------------------------------

def predict_route(say: str, held: bool, ground: Path) -> str:
    """What pipeline._maker_route will do with these words, read with the engine's OWN functions in the
    order it asks them. A request that names a tool is never the maker's; that one is not modelled here,
    and the observed route will show it if it matters."""
    what = "" if (held and intent.wants_changing(say)) else intent.wants_making(say)
    if what:
        return "make"
    words = intent.wants_picking_up(say)
    if words:
        found = maker.find(ground, words)
        if len(found) == 1:
            return "pick"
        if found or re.search(r"(?i)\bprojects?\b", say):
            return "pick-none"
    if intent.wants_putting_down(say):
        return "put-down"
    if not held:
        return ""
    if intent.wants_going_back(say) is not None:
        return "go-back"
    return "change" if intent.wants_changing(say) else ""


def observed_route(notes) -> str:
    """The route the run's own notes say it took."""
    for n in notes or []:
        if not str(n).startswith("maker:"):
            continue
        n = str(n)
        if "a request to MAKE" in n:
            return "make"
        if "a change to" in n or "too big to rewrite whole" in n:
            return "change"
        if "went back to version" in n or "go back refused" in n:
            return "go-back"
        if "picked up" in n:
            return "pick"
        if "put down" in n or "put a project down" in n:
            return "put-down"
        if " names " in n:
            return "pick-none"
    return ""


# ---------------------------------------------------------------------
# the sandbox
# ---------------------------------------------------------------------

def sandbox_refusal(dest: Path) -> str:
    """Why this directory may not be the pack's sandbox, or ''. The pack owns it (a marker), it is
    outside the ground, and it holds nothing the pack did not make."""
    d = Path(dest).resolve()
    r = ROOT.resolve()
    if d == r or r in d.parents or d in r.parents:
        return f"{d} is the ground or holds it or sits inside it"
    if d.exists():
        if not d.is_dir():
            return f"{d} is not a directory"
        held = [p.name for p in d.iterdir()]
        if held and MARK not in held:
            return f"{d} is not empty and is not a pack sandbox (no {MARK})"
    return ""


def rm_sandbox(path: Path, top: Path) -> None:
    """Remove a clone -- only a directory the pack marked, only under the sandbox it was given."""
    path, top = Path(path).resolve(), Path(top).resolve()
    if top not in path.parents or not (path / MARK).is_file():
        raise RuntimeError(f"{path} is not a clone the pack made; it is not removed")

    def _writable(fn, p, _exc):                 # git leaves read-only objects
        os.chmod(p, 0o700)
        fn(p)
    shutil.rmtree(path, onerror=_writable)


def _git(args, cwd: Path, check: bool = True) -> str:
    r = subprocess.run(["git"] + list(args), cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])} failed in {cwd.name}: {r.stderr.strip()[:200]}")
    return r.stdout


def tracked_files() -> list[str]:
    r = subprocess.run(["git", "ls-files", "-z"], cwd=str(ROOT), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git ls-files failed in the ground")
    return [p for p in r.stdout.decode("utf-8", "replace").split("\0") if p]


def build_clone(dest: Path, upto: int | None) -> dict:
    """The ground, copied byte for byte (CRLF kept) into `dest`, with its own history and a ledger cut to
    the lines before sitting `upto`. Returns the facts the report states about it."""
    dest = Path(dest)
    dest.mkdir(parents=True)
    (dest / MARK).write_text("made by tests/pack.py; safe to delete\n", encoding="utf-8")
    copied, missing = 0, []
    names = tracked_files() + [s for s in STATE]
    for rel in names:
        if rel == ".env" or rel.startswith(".env") and rel != ".env.example":
            continue                                           # RULE 7, whatever a list says
        if protected(rel):
            continue                                           # SITTING LAW 2, whatever a list says
        src = ROOT / rel
        if not src.is_file():
            missing.append(rel)
            continue
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
    sess = dest / seatlog.SESSIONS
    sess.parent.mkdir(parents=True, exist_ok=True)
    src_ledger = ROOT / seatlog.SESSIONS
    kept = 0
    if src_ledger.is_file():
        raw = src_ledger.read_bytes().decode("utf-8-sig")
        out = []
        for line in raw.splitlines():
            if not line.strip():
                continue
            if upto is not None:
                try:
                    n = json.loads(line).get("n")
                except ValueError:
                    continue
                if not isinstance(n, int) or n >= upto:
                    continue
            out.append(line)
        kept = len(out)
        sess.write_bytes(("\r\n".join(out) + ("\r\n" if out else "")).encode("utf-8"))
    silenced = silence(dest)
    _git(["init", "-b", "main"], dest)
    for k, v in (("user.name", "pack"), ("user.email", "pack@localhost"), ("core.autocrlf", "false")):
        _git(["config", k, v], dest)
    _git(["add", "-A"], dest)
    _git(["commit", "-q", "-m", "the sandbox, as copied"], dest)
    dirty = [l for l in _git(["status", "--porcelain"], dest, check=False).splitlines() if l.strip()]
    return {"files": copied, "missing": missing, "ledger_lines": kept, "dirty_after_commit": len(dirty),
            "silenced": silenced}


SILENCE = """

# tests/pack.py -- a sandbox makes no sound. Speaking is an effect on the operator's machine (his speakers), and
# a replayed `speak` should find that there is no voice rather than use them. The only edit a clone carries.
def _speech_backend():
    return "", ""
"""


def silence(dest: Path) -> bool:
    """Append the no-voice override to the CLONE's voice.py (never the ground's). True when it was written."""
    v = Path(dest) / "manjuel" / "voice.py"
    if not v.is_file():
        return False
    raw = v.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    v.write_bytes((raw + SILENCE.replace("\n", nl)).encode("utf-8"))
    return True


def engine_env(clone: Path) -> dict:
    env = {}
    for k, v in os.environ.items():
        u = k.upper()
        if u.startswith(DROP_PREFIXES) or any(w in u for w in DROP_WORDS):
            continue
        env[k] = v
    env.update(DIALS)
    env.update(PYTHONPATH=str(clone), PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    return env


def isolation(clone: Path) -> str:
    """'' when an engine started in this clone would run the CLONE's code, else why not."""
    r = subprocess.run([sys.executable, "-c", "import manjuel,sys;print(manjuel.__file__)"],
                       cwd=str(clone), env=engine_env(clone), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    where = (r.stdout or "").strip().splitlines()[-1:] or [""]
    got = Path(where[0]).resolve() if where[0] else None
    if got is None or Path(clone).resolve() not in got.parents:
        return f"the engine would import manjuel from {where[0] or '(nowhere)'}, not from the clone"
    return ""


def sitting_open(root: Path = ROOT) -> str:
    """'' when no sitting is open on the ground (the last ledger line has ended), else which is."""
    p = Path(root) / seatlog.SESSIONS
    if not p.is_file():
        return ""
    last = ""
    for line in p.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            last = line
    try:
        row = json.loads(last)
    except ValueError:
        return "the ledger's last line does not parse"
    return "" if row.get("ended") else f"sitting {row.get('n')} is open"


# ---------------------------------------------------------------------
# the engine, over its own wire
# ---------------------------------------------------------------------

class EngineDied(RuntimeError):
    pass


class Engine:
    """`python manjuel.py --headless` in a clone, spoken to in JSON lines (serve.py, protocol 1)."""

    def __init__(self, clone: Path):
        self.clone = Path(clone)
        self.q: queue.Queue = queue.Queue()
        self.err: list = []
        self.p = subprocess.Popen(
            [sys.executable, str(self.clone / "manjuel.py"), "--headless"], cwd=str(self.clone),
            env=engine_env(self.clone), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        threading.Thread(target=self._pump, daemon=True).start()
        threading.Thread(target=self._drain, daemon=True).start()

    def _pump(self) -> None:
        for raw in iter(self.p.stdout.readline, b""):
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                row = {"event": "raw", "text": line}
            self.q.put(row)
        self.q.put(None)

    def _drain(self) -> None:
        for raw in iter(self.p.stderr.readline, b""):
            self.err.append(raw.decode("utf-8", "replace").rstrip())
            del self.err[:-60]

    def send(self, obj: dict) -> None:
        if obj.get("cmd") not in serve.COMMANDS:
            raise ValueError(f"{obj.get('cmd')!r} is not a command of the headless door")
        try:
            self.p.stdin.write((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
            self.p.stdin.flush()
        except OSError as exc:
            raise EngineDied(f"the engine's stdin is closed ({exc})")

    def get(self, timeout: float):
        try:
            row = self.q.get(timeout=timeout)
        except queue.Empty:
            return {}
        if row is None:
            self.q.put(None)
            raise EngineDied("the engine's stdout closed; stderr: " + " | ".join(self.err[-4:]))
        return row

    def opened(self) -> dict:
        end = time.time() + BOOT_CAP
        while time.time() < end:
            row = self.get(2.0)
            if row.get("event") == "opened":
                return row
            if row.get("event") == "closed":
                raise EngineDied(f"closed while opening: {row.get('why')}")
        raise EngineDied(f"no `opened` inside {BOOT_CAP:.0f}s; stderr: " + " | ".join(self.err[-4:]))

    def close(self) -> dict:
        closed: dict = {}
        try:
            self.send({"cmd": "close"})
            end = time.time() + CLOSE_CAP
            while time.time() < end:
                row = self.get(2.0)
                if row.get("event") == "closed":
                    closed = row
                    break
        except EngineDied:
            pass
        try:
            self.p.stdin.close()
        except OSError:
            pass
        try:
            self.p.wait(30)
        except subprocess.TimeoutExpired:
            self.p.kill()
        return closed

    def kill(self) -> None:
        try:
            self.p.kill()
        except OSError:
            pass


def answer_for(prompt: str) -> str:
    for rx, a in ANSWERS:
        if rx.search(prompt):
            return a
    return "y"


# ---------------------------------------------------------------------
# a turn, and what came of it
# ---------------------------------------------------------------------

@dataclass
class Outcome:
    turn: Turn
    predicted: str = ""
    observed: str = ""
    terminal: str = ""
    final: dict = field(default_factory=dict)
    delivery: str = ""
    wall: float = 0.0
    tools: list = field(default_factory=list)
    questions: list = field(default_factory=list)
    screen: str = ""
    timed_out: bool = False
    died: str = ""
    results: list = field(default_factory=list)
    handed: str = ""
    moved: dict = field(default_factory=dict)       # the maker's own record of what changed on disk
    play: dict = field(default_factory=dict)
    faults: list = field(default_factory=list)
    seen: list = field(default_factory=list)
    skipped: str = ""

    @property
    def ok(self) -> bool:
        return not self.faults


def run_turn(eng: Engine, turn: Turn) -> Outcome:
    o = Outcome(turn)
    msg: dict = {"cmd": "objective", "text": turn.say}
    if turn.feed:
        msg["feed"] = turn.feed
    if turn.unattended:
        msg["unattended"] = True
    t0 = time.time()
    eng.send(msg)
    cancelled_at = 0.0
    while True:
        left = CAP - (time.time() - t0)
        if left <= 0 and not o.timed_out:
            o.timed_out = True
            cancelled_at = time.time()
            eng.send({"cmd": "cancel"})
        if o.timed_out and time.time() - cancelled_at > 90:
            o.died = "the turn did not end 90s after the pack cancelled it"
            break
        try:
            ev = eng.get(2.0)
        except EngineDied as exc:
            o.died = str(exc)
            break
        kind = ev.get("event")
        if not kind:
            continue
        if kind == "text":
            if len(o.screen) < 20000:
                o.screen += str(ev.get("text") or "")
        elif kind == "needs_answer":
            a = answer_for(str(ev.get("prompt") or ""))
            o.questions.append((str(ev.get("prompt") or "").strip(), a))
            eng.send({"cmd": "answer", "text": a})
        elif kind == "tool":
            o.tools.append(str(ev.get("action") or ""))
        elif kind in serve.TERMINAL:
            o.terminal, o.final = kind, ev
            break
    o.wall = time.time() - t0
    o.delivery = str(o.final.get("text") or "").strip()
    return o


def read_run(clone: Path, o: Outcome) -> None:
    """What the run wrote to its own transcript: the full tool results and the prompts every seat was handed."""
    rel = str(o.final.get("transcript") or "")
    if not rel:
        return
    path = Path(clone) / rel
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
        body = text.split("\n## Delivery", 1)[0]
        o.results = [m.group(2).strip() for m in re.finditer(
            r"Tool executed: (\S+)\s*\n+\s*Result:\n(.*?)(?=\n### |\n## |\Z)", body, re.S)]
    pr = Path(clone) / "logs" / "_prompts" / path.name
    if pr.is_file():
        o.handed = "\n".join(re.findall(r"```text\n(.*?)\n```", pr.read_text(encoding="utf-8", errors="replace"), re.S))


# ---------------------------------------------------------------------
# the maker's evidence, and the page played
# ---------------------------------------------------------------------

def snapshot(clone: Path) -> dict:
    """{project: (versions, sha1 of the page)} -- read off each project's own history."""
    out = {}
    for p in maker.projects(clone):
        page = maker.page_of(p)
        out[p.name] = (len(maker.versions(p)), hashlib.sha1(page.encode("utf-8")).hexdigest()[:10])
    return out


_PLAY_PRE = ("<script>(function(){var R=window.__play={listens:{},listenAt:{},fired:{},firedAt:{},steps:{},errors:0,dialogs:[],cur:''};"
             "window.alert=function(){R.dialogs.push('alert');};window.confirm=function(){R.dialogs.push('confirm');return true;};"
             "window.prompt=function(){R.dialogs.push('prompt');return null;};"
             "function who(t){if(t===window){return 'window';}if(t===document){return 'document';}"
             "var n=((t&&t.tagName)||'?').toLowerCase();return (n==='body'||n==='html')?n:n+(t&&t.tabIndex>=0?'*':'');}"
             "var map=new WeakMap(),add=EventTarget.prototype.addEventListener,rem=EventTarget.prototype.removeEventListener;"
             "R.raw=function(t,type,fn,opt){return add.call(t,type,fn,opt);};"
             "EventTarget.prototype.addEventListener=function(type,fn,opt){"
             "R.listens[type]=(R.listens[type]||0)+1;var at=(R.listenAt[type]=R.listenAt[type]||{}),d=who(this);at[d]=(at[d]||0)+1;"
             "if(typeof fn==='function'){var w=map.get(fn);if(!w){w=function(e){"
             "if(R.cur){R.fired[e.type]=(R.fired[e.type]||0)+1;var k=R.cur+':'+e.type;R.firedAt[k]=(R.firedAt[k]||0)+1;}"
             "return fn.apply(this,arguments);};map.set(fn,w);}return add.call(this,type,w,opt);}return add.call(this,type,fn,opt);};"
             "EventTarget.prototype.removeEventListener=function(type,fn,opt){"
             "var w=(typeof fn==='function'&&map.get(fn))||fn;return rem.call(this,type,w,opt);};})();</script>")

# THE PROBE PLAYS THE WAY A BROWSER DELIVERS INPUT (2026-10-03). The first cut dispatched keys straight onto the
# canvas and called a game playable whose arrow keys are bound to a canvas with no tabindex -- which a real
# keyboard can never reach. So: a key goes to the FOCUSED element (the body when nothing is), a press goes to
# whatever is UNDER the pointer and moves focus only if that element can take it.
_PLAY_JS = r"""<script>(function(){
var R=window.__play;
function H(s){var h=5381,i=s.length;while(i){h=(h*33)^s.charCodeAt(--i);}return (h>>>0).toString(36);}
function sig(){var p=[];try{p.push(H(document.documentElement.outerHTML));}catch(e){p.push('o');}
var cs=document.querySelectorAll('canvas');for(var i=0;i<cs.length&&i<4;i++){try{p.push(H(cs[i].toDataURL()));}catch(e){p.push('x');}}
return p.join('|');}
function active(){var a=document.activeElement;return (a&&a!==document.documentElement)?a:document.body;}
function key(type,k,c,t){var e;try{e=new KeyboardEvent(type,{key:k,code:(k.length===1?(/[a-z]/i.test(k)?'Key'+k.toUpperCase():(/\d/.test(k)?'Digit'+k:'Space')):k),keyCode:c,which:c,bubbles:true,cancelable:true});}catch(x){return;}
try{Object.defineProperty(e,'keyCode',{get:function(){return c;}});Object.defineProperty(e,'which',{get:function(){return c;}});}catch(x){}
t.dispatchEvent(e);}
function tap(k,c){var t=active();key('keydown',k,c,t);key('keyup',k,c,t);}
function mev(type,t,x,y,b){var e;try{e=new MouseEvent(type,{clientX:x,clientY:y,button:b,buttons:(type==='mousedown'?(b===2?2:1):0),bubbles:true,cancelable:true,view:window});}catch(z){return;}t.dispatchEvent(e);}
function pev(type,t,x,y,b){var e;try{e=new PointerEvent(type,{clientX:x,clientY:y,button:b,buttons:(type==='pointerdown'?(b===2?2:1):0),pointerId:1,bubbles:true,cancelable:true,view:window});}catch(z){return;}t.dispatchEvent(e);}
function hit(x,y,b){var el=document.elementFromPoint(x,y)||document.body;
pev('pointerdown',el,x,y,b);mev('mousedown',el,x,y,b);
try{if(el.tabIndex>=0&&el.focus){el.focus();}else if(document.activeElement&&document.activeElement!==document.body&&document.activeElement.blur){document.activeElement.blur();}}catch(e){}
pev('pointerup',el,x,y,b);mev('mouseup',el,x,y,b);
if(b===2){mev('contextmenu',el,x,y,b);}else{mev('click',el,x,y,b);}}
function points(){var p=[],cs=document.querySelectorAll('canvas');
for(var i=0;i<cs.length&&i<3;i++){var r=cs[i].getBoundingClientRect();if(r.width>0&&r.height>0){var fx=[.5,.25,.75,.5,.5],fy=[.5,.5,.5,.25,.75];
for(var j=0;j<5;j++){p.push([r.left+r.width*fx[j],r.top+r.height*fy[j]]);}}}
if(!p.length){var f=[[.5,.5],[.3,.3],[.7,.3],[.3,.7],[.7,.7]];for(var k=0;k<f.length;k++){p.push([innerWidth*f[k][0],innerHeight*f[k][1]]);}}
return p;}
function canv(){var cs=document.querySelectorAll('canvas'),c=[];
for(var i=0;i<cs.length&&i<4;i++){var o={w:cs[i].width,h:cs[i].height,drawn:null};
try{var ctx=cs[i].getContext('2d');if(ctx){var t=document.createElement('canvas');t.width=64;t.height=48;var tc=t.getContext('2d');tc.drawImage(cs[i],0,0,64,48);
var d=tc.getImageData(0,0,64,48).data,seen={},n=0;
for(var j=0;j<d.length&&n<4;j+=4){var k=d[j]+','+d[j+1]+','+d[j+2]+','+d[j+3];if(!seen[k]){seen[k]=1;n++;}}o.drawn=n>=2;}}catch(e){}c.push(o);}
return c;}
function facts(){R.canvas=canv();R.svg=document.querySelectorAll('svg').length;
R.buttons=document.querySelectorAll('button,[role=button],input[type=button],input[type=submit]').length;
R.inputs=document.querySelectorAll('input,textarea,select').length;R.onclick=document.querySelectorAll('[onclick]').length;
var t=(document.body&&document.body.innerText)||'';R.textLen=t.length;R.text=t.replace(/\s+/g,' ').slice(0,160);R.title=document.title||'';
var cells=0,els=document.querySelectorAll('div,td,span,li'),m=Math.min(els.length,3000);
for(var q=0;q<m;q++){var e=els[q];if(e.offsetWidth>0&&e.offsetWidth<120){var bg=getComputedStyle(e).backgroundColor;if(bg&&bg!=='rgba(0, 0, 0, 0)'&&bg!=='transparent'){cells++;}}}
R.cells=cells;}
function keys(){tap('ArrowRight',39);tap('ArrowDown',40);tap('ArrowLeft',37);tap('ArrowUp',38);tap('d',68);tap('s',83);tap('a',65);tap('w',87);tap(' ',32);tap('Enter',13);tap('e',69);tap('1',49);tap('2',50);}
var steps=[
['keys',keys],
['click',function(){var p=points(),d={};for(var i=0;i<p.length;i++){hit(p[i][0],p[i][1],0);d[sig()]=1;}R.clickDistinct=Object.keys(d).length;R.clicks=p.length;}],
['keys-after-click',keys],
['rclick',function(){var p=points();for(var i=0;i<p.length&&i<2;i++){hit(p[i][0],p[i][1],2);}}],
['move',function(){var p=points();for(var i=0;i<p.length&&i<4;i++){var el=document.elementFromPoint(p[i][0],p[i][1])||document.body;mev('mousemove',el,p[i][0],p[i][1],0);}}],
['wheel',function(){var p=points();var el=document.elementFromPoint(p[0][0],p[0][1])||document.body;try{el.dispatchEvent(new WheelEvent('wheel',{deltaY:120,clientX:p[0][0],clientY:p[0][1],bubbles:true,cancelable:true}));}catch(e){}}],
['fill',function(){var f=document.querySelectorAll('input:not([type=button]):not([type=submit]):not([type=checkbox]):not([type=radio]),textarea');
for(var i=0;i<f.length&&i<8;i++){try{f[i].focus();f[i].value=(f[i].type==='number'?'3':'sample '+i);f[i].dispatchEvent(new Event('input',{bubbles:true}));f[i].dispatchEvent(new Event('change',{bubbles:true}));}catch(e){}}}],
['buttons',function(){var b=document.querySelectorAll('button,[role=button],input[type=button],input[type=submit]');for(var i=0;i<b.length&&i<6;i++){try{b[i].click();}catch(e){}}
var fm=document.querySelectorAll('form');for(var j=0;j<fm.length&&j<3;j++){try{var ev=new Event('submit',{bubbles:true,cancelable:true});fm[j].dispatchEvent(ev);}catch(e){}}}]
];
function finish(){R.canvas2=canv();R.cur='';try{console.error('[[PLAY]]'+JSON.stringify(R));}catch(e){}}
function run(i){if(i>=steps.length){finish();return;}var s=steps[i],b=sig();R.cur=s[0];try{s[1]();}catch(e){R.errors++;}
setTimeout(function(){R.steps[s[0]]=(sig()!==b);run(i+1);},200);}
function begin(){var s0=sig();setTimeout(function(){R.animated=(sig()!==s0);facts();run(0);},600);}
R.raw(document,'submit',function(e){e.preventDefault();},true);
if(document.readyState==='complete'){setTimeout(begin,400);}else{R.raw(window,'load',function(){setTimeout(begin,400);},false);}
})();</script>"""


def with_probe(page: str) -> str:
    """The page with the probe's two scripts in it: the first behind the opening of head (ahead of the
    page's own scripts), the second ahead of the closing of body. Single-line, so the Coder's line
    numbers the maker reports are not moved."""
    pre = _PLAY_PRE
    drv = " ".join(_PLAY_JS.split("\n"))
    m = (re.search(r"(?i)<head\b[^>]*>", page) or re.search(r"(?i)<html\b[^>]*>", page)
         or re.search(r"(?i)<!doctype\s+html[^>]*>", page))
    out = (page[:m.end()] + pre + page[m.end():]) if m else pre + page
    i = out.lower().rfind("</body>")
    if i < 0:
        i = out.lower().rfind("</html>")
    return (out[:i] + drv + out[i:]) if i >= 0 else out + drv


def play(page: str) -> dict:
    """The page loaded and played in the maker's own headless browser. {loaded, why, errors, probe}."""
    with contextlib.redirect_stderr(io.StringIO()):     # the page's own server prints a reset when the browser closes
        loaded, faults, why = maker.run_page(with_probe(page), settle=6.0, budget=40.0)
    out: dict = {"loaded": loaded, "why": why, "errors": [], "probe": None}
    for f in faults or []:
        text = str(f.get("text") or "")
        if text.startswith("[[PLAY]]"):
            try:
                out["probe"] = json.loads(text[len("[[PLAY]]"):])
            except ValueError:
                pass
        else:
            out["errors"].append({"kind": f.get("kind"), "text": text[:160], "line": f.get("line")})
    return out


KEY_TYPES = ("keydown", "keyup", "keypress")
INPUT_TYPES = KEY_TYPES + ("click", "mousedown", "mouseup", "pointerdown", "pointerup", "mousemove", "wheel",
                           "contextmenu", "touchstart", "input", "change", "submit")
REACHABLE = ("window", "document", "body", "html")      # what a key reaches when nothing has been focused


def visible(page: str) -> str:
    """The words a page shows: head, scripts, styles and tags out, whitespace collapsed."""
    t = re.sub(r"(?is)<head\b.*?</head>", " ", page or "")
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return " ".join(t.split())


def bleed(new: str, others: list) -> str:
    """A run of five words the NEW page shows that another project's page shows too -- the text it should
    never have borrowed (a recipe tool that says `Arrow keys to move, Click to start`). '' when they share none."""
    mine = re.findall(r"\w+", visible(new).lower())
    have = {" ".join(mine[i:i + 5]) for i in range(len(mine) - 4)}
    for other in others:
        theirs = re.findall(r"\w+", visible(other).lower())
        for i in range(len(theirs) - 4):
            if " ".join(theirs[i:i + 5]) in have:
                return " ".join(theirs[i:i + 7])
    return ""


def graphical(probe: dict) -> bool:
    """Whether the page puts a picture in front of a person rather than words: a drawn canvas (before or after
    the probe's clicks), a canvas the probe could not read (WebGL), a vector picture, or a grid of coloured cells."""
    if not probe:
        return False
    for c in (probe.get("canvas") or []) + (probe.get("canvas2") or []):
        if c.get("drawn") is True or (c.get("drawn") is None and (c.get("w") or 0) * (c.get("h") or 0) > 0):
            return True
    return (probe.get("svg") or 0) >= 1 or (probe.get("cells") or 0) >= 25


def plays(probe: dict) -> bool:
    """Whether the page's own handlers ran on the probe's input (delivered as a browser delivers it), or the
    picture changed on it."""
    if not probe:
        return False
    ran = [t for t in (probe.get("fired") or {}) if t in INPUT_TYPES]
    return bool(ran) or (not probe.get("animated") and any((probe.get("steps") or {}).values()))


def keys_dead(probe: dict) -> str:
    """'' when the page's keyboard handlers can be reached by a key; else why not -- they sit on elements a
    browser never gives the keyboard to (a canvas with no tabindex), so no key a person presses arrives."""
    at = (probe or {}).get("listenAt") or {}
    where: dict = {}
    for t in KEY_TYPES:
        for d, n in (at.get(t) or {}).items():
            where[d] = where.get(d, 0) + n
    if not where or any(d in REACHABLE or d.endswith("*") for d in where):
        return ""
    return "its keyboard handlers sit on " + ", ".join(sorted(where)) + ", which no key a person presses reaches (no tabindex)"


# ---------------------------------------------------------------------
# the judge
# ---------------------------------------------------------------------

def collapse(s, n: int = 160) -> str:
    t = " ".join(str(s or "").split())
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def judge(o: Outcome, case: Case) -> None:
    t = o.turn
    f, seen = o.faults, o.seen
    if o.died:
        f.append(f"the engine stopped answering: {collapse(o.died, 200)}")
    elif o.timed_out:
        f.append(f"no end to the turn inside {CAP:.0f}s; the pack cancelled it (ended as {o.terminal or 'nothing'})")
    elif t.expect_refused and o.terminal != "refused":
        f.append(f"expected the gate to refuse; the turn ended as {o.terminal}")
    elif not t.expect_refused and o.terminal in ("refused", "aborted", "cancelled", "unreachable"):
        f.append(f"ended as {o.terminal}: {collapse(o.final.get('text'), 140)}")
    for shape in standup.NEVER_IN_DELIVERY:
        if shape in o.delivery:
            f.append(f"the delivery carries `{shape}` -- markup reached a person")
    inferred = bool(o.final.get("inferred"))      # a refusal leaves no run on the ledger; it has no answer or stamp to judge
    if inferred:
        if t.expect_refused:
            seen.append("no run is recorded for a refused turn (the ledger writes one only for a delivery); inferred from its absence")
        else:
            f.append("no run is recorded for this turn: it was refused before a seat sat, or did not run")
    if o.terminal in ("delivery", "refused") and not o.delivery and not inferred:
        f.append("no seat produced an answer")
    notes = [str(n) for n in o.final.get("notes") or []]
    if o.terminal in ("delivery", "refused") and not any(n.startswith("law:") for n in notes) and not inferred:
        f.append("the law gate left no stamp on this run")
    for seat, err in o.final.get("failures") or []:
        f.append(f"{seat} FAILED: {collapse(err, 100)}")
    for seat in o.final.get("out_of_time") or []:
        f.append(f"{seat} was OUT OF TIME -- never seated")
    if ENGINE_SAYS.search(o.delivery):
        f.append("the engine itself says a named tool did not run: " + collapse(standup.where(o.delivery, "THE NAMED TOOL DID NOT RUN", 60), 150))
    for tool in t.expect_tools:
        if tool not in o.tools:
            f.append(f"expected `{tool}` to run; tools that ran: {o.tools or 'none'}")
    if t.expect_no_tools and o.tools:
        f.append(f"a plain turn woke tools: {o.tools}")
    if t.expect_own_words and o.terminal == "delivery" and o.handed:
        lifted = recited(o.delivery, o.handed)
        if lifted:
            f.append(f"the delivery recites {len(lifted)} characters of what the seat was handed: {lifted[:90]!r}")
    made_by_engine = any(n.startswith("maker:") for n in notes)
    if o.terminal == "delivery" and not made_by_engine and not t.expect_refused:
        got = standup.unsourced_numbers(o.delivery, o.results + [o.handed] + [str(e) for _s, e in o.final.get("failures") or []],
                                        t.say)
        if got:
            f.append("numbers in the delivery that no tool returned: "
                     + "; ".join(f"{n} in {standup.where(o.delivery, n)!r}" for n in got[:6]))
    # the route: the engine's arithmetic, asked before the turn, against the notes the run wrote
    if case.wife or t.route != "*":
        if o.terminal == "delivery" and o.predicted != o.observed:
            f.append(f"the pack read the route as `{o.predicted or 'ordinary'}` and the run took "
                     f"`{o.observed or 'ordinary'}` -- the pack and the engine disagree")
    if case.wife and t.route not in ("*", o.predicted):
        f.append(f"the persona declares `{t.route or 'ordinary'}` for these words and the engine's arithmetic "
                 f"reads `{o.predicted or 'ordinary'}`")
    hit = LEAKS.search(o.delivery)
    if hit:
        f.append(f"the machinery shows in the delivery: {collapse(standup.where(o.delivery, hit.group(0)), 110)!r}")
    plain = o.terminal == "delivery" and not o.tools and not o.observed
    soft = LEAKS_SOFT.search(o.delivery)
    if soft:
        line = f"the machinery shows in the delivery: {collapse(standup.where(o.delivery, soft.group(0)), 110)!r}"
        if plain and (case.wife or t.expect_own_words):
            f.append(line)
        else:
            seen.append(line)
    about = ABOUT.search(o.delivery)
    card = len(set(m.group(0).strip() for m in CARD.finditer(o.delivery))) >= 2
    if about or card:
        msg = ("the reply speaks ABOUT the operator in the third person" if about else
               "a chat is answered with the report card of a tool turn (What happened / Result / Open)")
        if plain and (case.wife or t.expect_own_words):
            f.append(msg + f": {collapse(standup.where(o.delivery, (about or CARD.search(o.delivery)).group(0)), 90)!r}")
        elif case.wife:
            seen.append(msg)
        # in his own replays "the operator" is the house's word for him, and a tool turn's report is the engine's
        # voice: neither is noted unless the turn was small talk (above)
    raw = TOOLSPEAK.search(o.delivery)
    if raw:
        line = f"raw tool output shows in the delivery: {collapse(standup.where(o.delivery, raw.group(0)), 90)!r}"
        (f if case.wife else seen).append(line)
    if case.wife and o.moved.get("bleed"):
        f.append(f"the new page shows a line from another project: {o.moved['bleed']!r}")
    if case.wife and TERMINAL_TALK.search(o.delivery):
        seen.append("the delivery tells her to use a terminal, a command or a file path: "
                    + collapse(TERMINAL_TALK.search(o.delivery).group(0), 60))
    if o.questions:
        seen.append("the system asked: " + "; ".join(f"{collapse(q, 70)!r} (answered {a!r})" for q, a in o.questions))
    guards = [n[:120] for n in notes if any(m in n for m in standup.GUARD_MARKS)]
    if guards:
        seen.append("guards fired: " + " || ".join(guards[:4]))
    if o.wall > 120:
        seen.append(f"slow: {o.wall:.0f}s")
    if any("too big to rewrite whole" in n for n in notes):
        seen.append("the project's page is over the Coder's window: a change cannot be made to it (maker.CHANGE_LIMIT)")
    # the persona: what she WANTED, beside what moved on disk
    if case.wife and t.wants:
        effect = o.moved.get("effect", "")
        want = {"make": "make", "change": "change", "back": "go-back", "pick": "pick", "put-down": "put-down"}[t.wants]
        if effect != want:
            said = PROMISE.search(o.delivery)
            seen.append(f"GAP: she wanted to {t.wants}; what moved on disk was `{effect or 'nothing'}` "
                        f"(the route was `{o.observed or 'ordinary'}`)"
                        + (f"; and the reply says {collapse(said.group(0), 50)!r} without doing it" if said and not effect else ""))
    # then against now (replays)
    th = t.then or {}
    if th.get("have"):
        if th.get("tools") and sorted(th["tools"]) != sorted(set(o.tools)):
            seen.append(f"tools differ: then {th['tools']}, now {sorted(set(o.tools))}")
        if th.get("failed") and not o.final.get("failures"):
            seen.append(f"then {th['failed']} seat(s) failed; now none did")
        e = float(th.get("elapsed") or 0.0)
        now = float(o.final.get("elapsed") or o.wall)
        if e > 5 and now > 3 * e:
            seen.append(f"{now / e:.1f}x slower than then ({e:.0f}s then, {now:.0f}s now)")


# ---------------------------------------------------------------------
# a case
# ---------------------------------------------------------------------

@dataclass
class CaseResult:
    case: Case
    outcomes: list = field(default_factory=list)
    clone: str = ""
    opened: dict = field(default_factory=dict)
    closed: dict = field(default_factory=dict)
    facts: dict = field(default_factory=dict)
    ledger: dict = field(default_factory=dict)
    harness_fault: str = ""
    wall: float = 0.0
    err_tail: list = field(default_factory=list)
    scorecard: list = field(default_factory=list)


def run_case(case: Case, top: Path, keep: bool, say) -> CaseResult:
    res = CaseResult(case)
    t0 = time.time()
    clone = Path(top) / case.key
    res.clone = str(clone)
    eng = None
    try:
        if clone.exists():                      # a clone of this pack's own, left by an earlier run
            rm_sandbox(clone, top)
        res.facts = build_clone(clone, case.sitting)
        say(f"  [{case.key}] clone built: {res.facts['files']} files, ledger {res.facts['ledger_lines']} lines, "
            f"{res.facts['dirty_after_commit']} changed after its first commit")
        why = isolation(clone)
        if why:
            raise RuntimeError("isolation: " + why)
        eng = Engine(clone)
        res.opened = eng.opened()
        say(f"  [{case.key}] engine open: sitting {res.opened.get('sitting')}, rack_ok={res.opened.get('rack_ok')}")
        if not res.opened.get("rack_ok"):
            raise RuntimeError("the rack is unreachable (Ollama is not answering); nothing to run")
        if case.sitting is not None and res.opened.get("sitting") != case.sitting:
            res.harness_fault = f"the engine opened sitting {res.opened.get('sitting')}, not {case.sitting}"
        held, before = "", snapshot(clone)
        for i, turn in enumerate(case.turns, 1):
            if turn.skip:
                o = Outcome(turn, skipped=turn.skip)
                res.outcomes.append(o)
                say(f"  [{case.key}] {i}/{len(case.turns)} skipped: {collapse(turn.say, 40)!r} ({turn.skip})")
                continue
            predicted = predict_route(turn.say, bool(held), clone)
            o = run_turn(eng, turn)
            o.predicted = predicted
            o.observed = observed_route(o.final.get("notes"))
            read_run(clone, o)
            if o.terminal == "delivery":
                held = str(o.final.get("project") or "")
            after = snapshot(clone)
            o.moved = moved(before, after, held, o.observed)
            before = after
            if o.moved.get("page") and case.wife:
                made = clone / maker.PROJECTS / o.moved["project"]
                o.play = play(maker.page_of(made))
                if o.moved.get("effect") == "make":
                    lent = bleed(maker.page_of(made), [maker.page_of(q) for q in maker.projects(clone) if q != made])
                    if lent:
                        o.moved["bleed"] = lent
            judge(o, case)
            res.outcomes.append(o)
            say(f"  [{case.key}] {i}/{len(case.turns)} {collapse(turn.say, 44)!r}: {o.terminal or 'NO END'} "
                f"{o.wall:.0f}s, {len(o.faults)} fault(s)")
            if o.died:
                break
        res.closed = eng.close()
        eng = None
        res.ledger = ledger(clone).get(res.opened.get("sitting")) or {}
        if case.wife:
            res.scorecard = scorecard(res)
    except KeyboardInterrupt:
        res.harness_fault = "interrupted"
        raise
    except Exception as exc:
        res.harness_fault = f"{type(exc).__name__}: {exc}"
        say(f"  [{case.key}] the pack itself failed here: {res.harness_fault}")
        if os.environ.get("PACK_TRACE"):
            traceback.print_exc()
    finally:
        if eng is not None:
            res.err_tail = list(eng.err[-6:])
            eng.kill()
        res.wall = time.time() - t0
        maker.forget()
    return res


def moved(before: dict, after: dict, held: str, route: str) -> dict:
    """What changed on disk across one turn, by the maker's own history -- never by a seat's account."""
    new = sorted(set(after) - set(before))
    out: dict = {"effect": "", "project": "", "page": False}
    if new:
        out.update(effect="make", project=new[0], page=True)
        return out
    grew = [n for n in after if n in before and after[n][0] > before[n][0]]
    if grew:
        out.update(effect="go-back" if route == "go-back" else "change", project=grew[0], page=True)
        return out
    if route == "pick" and held:
        out.update(effect="pick", project=held)
    elif route == "put-down" and not held:
        out.update(effect="put-down")
    return out


def scorecard(res: CaseResult) -> list:
    """The wife test's own sentence, line by line, with the evidence that answers each."""
    rows = []
    outs = [o for o in res.outcomes if not o.skipped]
    first = next((o for o in outs if o.moved.get("effect") == "make"), None)
    rows.append(("she asks in her own words and the system makes something",
                 first is not None, f"project `{first.moved['project']}`" if first else "no turn made a project"))
    pl = first.play if first else {}
    pr = (pl or {}).get("probe") or {}
    ran = bool(pl and pl.get("loaded"))
    broken = [e for e in (pl or {}).get("errors", []) if e.get("kind") in maker.BREAKING]
    rows.append(("she can SEE the result (the page loads and draws)",
                 bool(first) and ran and graphical(pr) and not broken,
                 (f"loaded={ran}; graphical={graphical(pr)}; {len(broken)} breaking error(s)" if first else "nothing to look at")))
    dead = keys_dead(pr)
    rows.append(("she can PLAY it (its own handlers run on her keys and clicks)",
                 bool(first) and plays(pr) and not dead,
                 (f"listens for {sorted((pr.get('listens') or {}).keys())[:6]}; ran on {sorted((pr.get('fired') or {}).keys())[:6]}"
                  + (f"; {dead}" if dead else "") if first else "nothing to play")))
    changes = [o for o in outs if o.turn.wants == "change"]
    done = [o for o in changes if o.moved.get("effect") == "change"]
    pr0 = ((first.play or {}).get("probe") or {}) if first else {}
    rows.append(("what she asked to BUILD on can be built on (a click at a place puts something at that place)",
                 bool(first) and (pr0.get("clickDistinct") or 0) >= 4,
                 (f"{pr0.get('clickDistinct')} distinct picture(s) over {pr0.get('clicks')} clicks at {pr0.get('clicks')} different places"
                  if first else "nothing made")))
    rows.append(("a change she asks for is made to the same thing",
                 bool(changes) and len(done) == len(changes),
                 f"{len(done)} of {len(changes)} change request(s) saved a next version"))
    asked = [o for o in outs if o.questions]
    terminal_talk = [o for o in outs if TERMINAL_TALK.search(o.delivery)]
    rows.append(("no terminal, no path typed, no help (the only way in is not a file path)",
                 not asked and not terminal_talk,
                 f"{len(asked)} turn(s) put a question to her; {len(terminal_talk)} of {len(outs)} told her to open a file path or use a terminal"))
    leaks = [o for o in outs if any(x.startswith(("the machinery shows", "the reply speaks ABOUT", "a chat is answered",
                                                  "raw tool output")) for x in o.faults)]
    rows.append(("it speaks TO her: no machinery, no 'the operator', no report card in its answers",
                 not leaks, f"{len(leaks)} of {len(outs)} turn(s) showed the machinery or spoke about the operator"))
    kept = [o for o in outs if o.final.get("transcript")]
    ledger_runs = len((res.ledger or {}).get("runs") or [])
    rows.append(("every step is in the record",
                 bool(outs) and len(kept) == len(outs) and ledger_runs >= len(outs),
                 f"{len(kept)} of {len(outs)} turns have a transcript; the ledger line holds {ledger_runs} run(s)"))
    return rows


# ---------------------------------------------------------------------
# the report
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# --record: the system's OWN record of sittings it ran live, judged read-only
# ---------------------------------------------------------------------

# WHAT WAS NOT RUN LIVE, AND WHY (2026-10-03). A live run goes through the operator's own glass into his own ground, so a
# turn that would commit, push, re-embed his index or use his speakers is left out, by its number in the old sitting.
NOT_LIVE = {
    79: {5: "re-embeds the operator's live index", 6: "re-embeds the operator's live index (the clone's rebuild showed embed errors)",
         7: "a commit is the operator's (RULE 6)", 14: "writes a file and speaks it through his speakers",
         15: "a commit is the operator's (RULE 6)"},
    70: {3: "asks to be read aloud, which speaks through his speakers", 4: "a commit is the operator's (RULE 6)",
         5: "the close of a sitting pays the toll"},
    170: {1: "git_cycle commits AND pushes (RULE 6)"},
    221: {9: "needs a pasted feed, which the front page does not take"},
}


def parse_run(root: Path, rel: str) -> dict:
    """What a sitting's own transcript says of one run: the delivery, the notes, the flags, each seat, each failure."""
    out: dict = {"delivery": "", "notes": [], "flags": [], "steps": [], "failures": [], "have": False}
    path = Path(root) / rel if rel else None
    if path is None or not path.is_file():
        return out
    text = path.read_text(encoding="utf-8", errors="replace")
    out["have"] = True
    d = transcript._DELIVERY_RE.search(text)
    out["delivery"] = d.group("t").strip() if d else ""
    out["notes"] = re.findall(r"^- \*\*note:\*\* (.+)$", text, re.M)
    m = re.search(r"^- \*\*flags:\*\* (.+)$", text, re.M)
    out["flags"] = [x.strip() for x in m.group(1).split(",")] if m else []
    stages = text.partition("\n## Stages")[2].split("\n## Delivery")[0]
    for sm in re.finditer(r"^### \d+\. (.+?) — `([^`]*)`\s*\n(.*?)(?=^### \d+\. |\Z)", stages, re.M | re.S):
        seat, model, body = sm.group(1), sm.group(2), sm.group(3).strip()
        step = {"seat": seat, "model": model, "elapsed": 0.0, "tools": [], "error": "", "skipped": False, "chars": len(body)}
        first = body.splitlines()[0] if body else ""
        if first.startswith("_skipped_"):
            step["skipped"] = True
        elif first.startswith("**FAILED**"):
            fm = re.match(r"\*\*FAILED\*\* after ([\d.]+)s: (.*)", first)
            if fm:
                step["elapsed"], step["error"] = float(fm.group(1)), fm.group(2)
            out["failures"].append([seat, step["error"]])
        elif first.startswith("_") and first.endswith("_"):
            parts = [x.strip() for x in first.strip("_").split(" · ")]
            try:
                step["elapsed"] = float(parts[0].rstrip("s"))
            except ValueError:
                pass
            for x in parts[1:]:
                if x.startswith("skills: "):
                    step["tools"] = [t.strip() for t in x[len("skills: "):].split(",") if t.strip()]
        out["steps"].append(step)
    # the machine-emitted honesty block: tools that failed or were refused
    mb = re.search(r"NOT EVERYTHING RAN\..*?\n((?:[ \t]+- .+\n?)+)", out["delivery"])
    if mb:
        for line in mb.group(1).splitlines():
            line = line.strip()
            if line.startswith("- "):
                name, _, why = line[2:].partition(": ")
                out["failures"].append([name, why])
    return out


def moved_from_notes(notes, route: str) -> dict:
    """What the maker did, by the notes the run wrote about it (the engine's own words, not a seat's)."""
    out: dict = {"effect": "", "project": "", "page": False, "version": 0}
    for n in notes or []:
        n = str(n)
        m = re.match(r"maker: (\S+) version (\d+) saved", n)
        if m:
            out.update(effect="make" if route == "make" else "change", project=m.group(1), page=True, version=int(m.group(2)))
            continue
        m = re.match(r"maker: (\S+) went back to version (\d+), saved as version (\d+)", n)
        if m:
            out.update(effect="go-back", project=m.group(1), page=True, version=int(m.group(3)))
            continue
        m = re.match(r"maker: (\S+) picked up \(version (\d+)\)", n)
        if m:
            out.update(effect="pick", project=m.group(1), version=int(m.group(2)))
            continue
        m = re.match(r"maker: (\S+) put down", n)
        if m:
            out.update(effect="put-down", project=m.group(1))
    return out


def page_at(root: Path, project: str, version: int) -> str:
    """A project's page as one of its versions held it, from the project's own history."""
    p = Path(root) / maker.PROJECTS / project
    vs = maker.versions(p)
    if 1 <= version <= len(vs):
        r = subprocess.run(["git", "show", f"{vs[version - 1][1]}:{maker.PAGE}"], cwd=str(p), capture_output=True)
        if r.returncode == 0:
            return r.stdout.decode("utf-8", "replace")
    return ""


def record_case(root: Path, key: str, n: int) -> CaseResult:
    """Judge sitting `n` of the ledger as case `key`: the words that were SAID, aligned with the runs it recorded."""
    base = key.split(".")[0]
    orig = dict(PICKS).get(base)
    if base == "W1":
        turns, title, source, wife = flow_turns(), "the wife test as the flow stands", f"flows/{FLOW.name}, fired through the Workflows wire", True
    elif base == "W2":
        turns, title, source, wife = persona(), "the wife test, a fuller mock", "the hand's persona (invented), typed through the front page", True
    elif orig:
        turns, title, source, wife = replay_turns(root, orig), f"sitting {orig} ({ERAS[base[0]]})", f"ledger sitting {orig}, typed through the front page", False
        for i, t in enumerate(turns, 1):
            if i in NOT_LIVE.get(orig, {}):
                t.skip = "not run live: " + NOT_LIVE[orig][i]
    else:
        raise ValueError(f"{key} is not a case --record knows")
    case = Case(key, title, source, turns, sitting=orig, wife=wife)
    row = ledger(root).get(n)
    if not row:
        raise ValueError(f"sitting {n} is not in the ledger")
    runs = list(row.get("runs") or [])
    res = CaseResult(case)
    res.clone = f"(live: sitting {n} on the operator's own ground)"
    res.opened = {"sitting": n, "session": row.get("id", ""), "started": row.get("started", ""), "rack_ok": True}
    res.closed = {"why": row.get("closed_by") or ("still open" if not row.get("ended") else "closed"), "sitting": n,
                  "runs": len(runs), "toll_paid": row.get("toll_paid"), "ended": row.get("ended", "")}
    res.facts = {}
    res.ledger = row
    held, k = False, 0
    for turn in turns:
        if turn.skip:
            res.outcomes.append(Outcome(turn, skipped=turn.skip))
            continue
        j = next((x for x in range(k, len(runs)) if str(runs[x].get("objective")) == turn.say), -1)
        o = Outcome(turn)
        o.predicted = predict_route(turn.say, held, root)
        if j < 0:
            # a refusal leaves no run on the ledger (only a delivery does); judge() says what its absence means
            o.terminal = "refused" if turn.expect_refused else ""
            o.final = {"inferred": True}
            judge(o, case)
            res.outcomes.append(o)
            continue
        run = runs[j]
        k = j + 1
        got = parse_run(root, str(run.get("transcript") or ""))
        o.terminal = "delivery"
        o.delivery = got["delivery"] or str(run.get("delivery") or "")
        o.wall = float(run.get("elapsed") or 0.0)
        o.tools = list(run.get("tools") or [])
        o.observed = observed_route(got["notes"])
        o.final = {"text": o.delivery, "notes": got["notes"], "flags": got["flags"], "steps": got["steps"],
                   "failures": got["failures"],
                   "out_of_time": list(run.get("out_of_time") or []), "elapsed": o.wall, "transcript": run.get("transcript") or "",
                   "project": ""}
        o.moved = moved_from_notes(got["notes"], o.observed)
        read_run(root, o)
        if o.moved["effect"] in ("make", "change", "pick"):
            held = True
        elif o.moved["effect"] == "put-down":
            held = False
        o.final["project"] = o.moved.get("project") if held else ""
        if wife and o.moved.get("page"):
            page = page_at(root, o.moved["project"], o.moved["version"])
            if page:
                o.play = play(page)
                if o.moved["effect"] == "make":
                    others = [maker.page_of(q) for q in maker.projects(root) if q.name != o.moved["project"]]
                    o.moved["bleed"] = bleed(page, others)
        judge(o, case)
        res.outcomes.append(o)
        res.wall += o.wall
    if wife:
        res.scorecard = scorecard(res)
    return res


# THE LIVE RUNNER (2026-10-03). What the operator asked for was "boot up the glass and run everything live so its all recorded through the
# system itself as sessions". This is the whole of the hand's part: Boot on the front page, then this, handed to the page, which feeds each
# line to its own `go()` (the code a keystroke reaches), waits for the answer, and stops at any question put to the person. It writes
# nothing; the sitting, the transcripts and the projects are the system's own.
LIVE_RUNNER_JS = r"""window.__live = { log: [], state: 'idle', i: 0 };
window.__runLines = async function (lines) {
  const L = window.__live; L.state = 'running'; L.log = [];
  for (let i = 0; i < lines.length; i++) {
    L.i = i + 1;
    const line = lines[i];
    while (Run.running) await new Promise(r => setTimeout(r, 400));
    const t0 = Date.now();
    await Agent.go(line);
    await new Promise(r => setTimeout(r, 400));
    if (!Run.turn || Run.turn.objective !== line) { L.log.push({ i: i + 1, line, error: 'not started' }); L.state = 'stopped'; return; }
    while (Run.running) await new Promise(r => setTimeout(r, 500));
    const tr = Run.turn || {};
    L.log.push({ i: i + 1, line: line.slice(0, 48), verdict: tr.verdict, waiting: tr.waiting || '', refusal: (tr.refusal || '').slice(0, 120),
                 s: Math.round((Date.now() - t0) / 1000), out: (tr.answer || '').replace(/\s+/g, ' ').slice(0, 110) });
    if (tr.verdict === 'waiting') { L.state = 'waiting'; return; }
  }
  L.state = 'done';
};
window.__case = async function (lines) {
  if (Run.engineOpen) { await Agent.go('/close'); for (let k = 0; k < 90 && Run.engineOpen; k++) await new Promise(r => setTimeout(r, 1000)); }
  await Agent.go('/boot'); for (let k = 0; k < 90 && !Run.engineOpen; k++) await new Promise(r => setTimeout(r, 1000));
  window.__sitting = Run.sitting;
  await window.__runLines(lines);
};"""

# The glass page's own names the runner depends on: (the fragment, the file, what it is called).
PAGE_NAMES = (("async go(rawIn)", "agent.js", "Agent.go"), ("if (raw === '/boot') return this.boot();", "agent.js", "/boot"),
              ("if (raw === '/close') return this.closeSitting();", "agent.js", "/close"), ("running: false,", "council.js", "Run.running"),
              ("engineOpen: false,", "council.js", "Run.engineOpen"), ("sitting: '',", "council.js", "Run.sitting"),
              ("turn: null,", "council.js", "Run.turn"))


def live_lines(root: Path, key: str) -> list:
    """The lines of a case that are run live: all of them, minus those NOT_LIVE keeps from the operator's own system."""
    base = key.split(".")[0]
    orig = dict(PICKS).get(base)
    if base == "W1":
        turns = flow_turns()
    elif base == "W2":
        turns = persona()
    elif orig:
        turns = replay_turns(root, orig)
        turns = [t for i, t in enumerate(turns, 1) if i not in NOT_LIVE.get(orig, {}) and not t.skip]
    else:
        raise ValueError(f"{key} is not a case")
    return [t.say for t in turns]


def record_lines(pairs: list) -> list:
    out = [
        "each case was a sitting opened on the operator's own glass (Boot on the front page), run through the front page's own `go()` -- or, for W1, "
        "the Workflows wire that fires `flows/wife-test.json` -- and closed with `/close`, which paid the toll: the ledger, the transcripts in `logs/` "
        "and `projects/` are the system's own record of it",
        "the pack read that record WITHOUT writing to it; each saved page was loaded and played in the maker's headless browser from the project's own history",
        "a refused turn leaves no run on the ledger (only a delivery does), so a refusal is inferred from its absence where one was expected",
        "questions the engine put to the person are not in the ledger; the runner that fed the page stopped at any, and none came",
    ]
    for n, key in pairs:
        orig = dict(PICKS).get(key.split(".")[0])
        if orig and NOT_LIVE.get(orig):
            out.append(f"{key} (the replay of sitting {orig}) -- lines not run live: " + "; ".join(f"line {i}, {why}" for i, why in sorted(NOT_LIVE[orig].items())))
    return out


def keep(res: CaseResult, top: Path) -> None:
    """The case's raw outcomes, beside the report, so the judge can be changed and run again without the models."""
    (Path(top) / f"case_{res.case.key}.json").write_text(
        json.dumps(dataclasses.asdict(res), ensure_ascii=False, default=str), encoding="utf-8", newline="\n")


def load(path: Path) -> CaseResult:
    d = json.loads(Path(path).read_text(encoding="utf-8"))

    def turn(t: dict) -> Turn:
        return Turn(**{**t, "expect_tools": tuple(t.get("expect_tools") or ())})

    case = Case(**{**d["case"], "turns": [turn(t) for t in d["case"]["turns"]]})
    outs = [Outcome(**{**od, "turn": turn(od["turn"])}) for od in d["outcomes"]]
    return CaseResult(**{**d, "case": case, "outcomes": outs})


def rejudge(res: CaseResult) -> None:
    for o in res.outcomes:
        o.faults, o.seen = [], []
        if not o.skipped:
            judge(o, res.case)
    res.scorecard = scorecard(res) if res.case.wife else []


def repeats(results: list) -> list:
    """For a case run more than once: which turns went wrong in how many of the runs. [(base, [lines])]"""
    groups: dict = {}
    for r in results:
        groups.setdefault(r.case.key.split(".")[0], []).append(r)
    out = []
    for base, rs in groups.items():
        if len(rs) < 2 or not rs[0].outcomes:
            continue
        lines = []
        for i, o0 in enumerate(rs[0].outcomes):
            if o0.skipped:
                continue
            hit = [r.outcomes[i] for r in rs if i < len(r.outcomes) and not r.outcomes[i].skipped]
            bad = sum(1 for o in hit if o.faults)
            gap = sum(1 for o in hit if any(x.startswith("GAP") for x in o.seen))
            if bad or gap:
                kinds = sorted({x.split(":")[0][:48] for o in hit for x in o.faults})
                lines.append(f"turn {i + 1} “{collapse(o0.turn.say, 50)}”: a fault in {bad} of {len(hit)} runs"
                             + (f" ({'; '.join(kinds)})" if kinds else "")
                             + (f"; the GAP between what she wanted and what happened in {gap}" if gap else ""))
        out.append((base, len(rs), lines))
    return out


def cell(s, n: int = 90) -> str:
    return collapse(s, n).replace("|", "\\|")


def render(results: list, started: str, env: dict) -> str:
    L = []
    w = L.append
    nf = sum(len(o.faults) for r in results for o in r.outcomes)
    nt = sum(1 for r in results for o in r.outcomes if not o.skipped)
    w(f"# Test pack — {started}")
    w("")
    live = env.get("mode") == "record"
    if live:
        w("The wife test mocked, and three eras of real sessions replayed, all run LIVE through the operator's own glass into his own "
          "ground (`tests/pack.py --record`). Every case is a sitting on the ledger, and what is judged here is the system's own record of "
          "it (the ledger, the transcripts in `logs/`, `projects/`), read-only: nothing ran on the side. The words are the old ones; the "
          "engine is the one running now. Reading of the order: a replay of what was said, not a checkout of old code. A turn that would "
          "commit, push, re-embed his index or use his speakers was not run, and the case says which and why.")
    else:
        w("The wife test mocked twice, and three eras of real sessions run again on TODAY's engine in a sandbox clone "
          "(`tests/pack.py`). The words are the old ones; the engine is the one on the disk now. Reading of the order: "
          "a replay of what was said, not a checkout of old code — if the old code was meant, that is a different pack.")
    w("")
    w(f"**{len(results)} cases, {nt} turns run, {nf} fault(s).** A fault is a mechanical miss; a `seen` line is for a "
      f"person to read. " + (f"Sittings: {env.get('sittings')}. " if live else f"Sandbox: `{env.get('sandbox')}`. ")
      + f"Engine: {env.get('engine')}.")
    w("")
    w("## Summary")
    w("")
    w("| case | what | turns | faults | seen | now (s) | then (s) | sitting | note |")
    w("|---|---|---|---|---|---|---|---|---|")
    for r in results:
        outs = [o for o in r.outcomes if not o.skipped]
        now = sum(float(o.final.get("elapsed") or o.wall) for o in outs)
        then = sum(float((o.turn.then or {}).get("elapsed") or 0) for o in outs)
        w(f"| {r.case.key} | {cell(r.case.title, 50)} | {len(outs)}/{len(r.case.turns)} | "
          f"{sum(len(o.faults) for o in outs)} | {sum(len(o.seen) for o in outs)} | {now:.0f} | "
          f"{(format(then, '.0f') if then else '-')} | {r.opened.get('sitting', '-')} | "
          f"{cell(r.harness_fault or r.case.note, 70)} |")
    w("")
    for r in results:
        if r.case.wife and r.scorecard:
            w(f"## The wife test — {r.case.key}: {r.case.title}")
            w("")
            w(f"*{r.case.source}.* Her own sentence (SPEC 4.8), line by line:")
            w("")
            w("| | the line | evidence |")
            w("|---|---|---|")
            for line, ok, ev in r.scorecard:
                w(f"| {'✅' if ok else '❌'} | {cell(line, 80)} | {cell(ev, 150)} |")
            w("")
    for r in results:
        c = r.case
        w(f"## {c.key} — {c.title}")
        w("")
        if live:
            w(f"*Source: {c.source}.* Sitting {r.opened.get('sitting', '?')} (`{r.opened.get('session', '')}`) on the operator's own glass, "
              f"{r.opened.get('started', '?')} to {r.closed.get('ended', '?')}; closed: {r.closed.get('why', '?')} "
              f"(runs {r.closed.get('runs', '?')}, toll paid {r.closed.get('toll_paid', '?')}). {r.wall:.0f}s of engine time.")
        else:
            w(f"*Source: {c.source}.* Clone `{r.clone}`; {r.facts.get('files', '?')} files, "
              f"{r.facts.get('ledger_lines', '?')} ledger lines, {r.facts.get('dirty_after_commit', '?')} changed after "
              f"its first commit. Opened as sitting {r.opened.get('sitting', '?')}; closed: "
              f"{r.closed.get('why', '?')} (runs {r.closed.get('runs', '?')}, toll paid {r.closed.get('toll_paid', '?')}). "
              f"Took {r.wall:.0f}s.")
        if r.harness_fault:
            w("")
            w(f"> **The pack itself failed here:** {r.harness_fault}" + (f" — stderr: {' | '.join(r.err_tail)[:300]}" if r.err_tail else ""))
        if c.note and not r.harness_fault:
            w("")
            w(f"> {c.note}")
        if not r.outcomes:
            w("")
            continue
        w("")
        w("| # | she said | route (pack → run) | ended | now | then | faults |")
        w("|---|---|---|---|---|---|---|")
        for i, o in enumerate(r.outcomes, 1):
            t = o.turn
            if o.skipped:
                w(f"| {i} | {cell(t.say, 70)} | | skipped | | | {cell(o.skipped, 80)} |")
                continue
            th = t.then or {}
            then = f"{th.get('elapsed', 0):.0f}s" + (f", {','.join(th['tools'])}" if th.get("tools") else "") if th.get("have") else "-"
            now = f"{float(o.final.get('elapsed') or o.wall):.0f}s" + (f", {','.join(sorted(set(o.tools)))}" if o.tools else "")
            w(f"| {i} | {cell(t.say, 70)} | {o.predicted or '·'} → {o.observed or '·'} | {o.terminal or 'NO END'} | "
              f"{cell(now, 50)} | {cell(then, 50)} | {len(o.faults)} |")
        w("")
        for i, o in enumerate(r.outcomes, 1):
            t = o.turn
            if o.skipped:
                continue
            w(f"### {c.key} · {i} — “{collapse(t.say, 110)}”")
            w("")
            if t.why:
                w(f"*{t.why}*")
                w("")
            for x in o.faults:
                w(f"- ❌ **fault:** {x}")
            for x in o.seen:
                w(f"- 👁 {x}")
            if o.moved.get("effect"):
                w(f"- on disk: `{o.moved['effect']}` of `{o.moved.get('project') or '-'}`")
            if o.play:
                pr = o.play.get("probe") or {}
                w(f"- played: loaded={o.play.get('loaded')}; graphical={graphical(pr)}; plays={plays(pr)}; "
                  f"animated={pr.get('animated')}; canvases={len(pr.get('canvas') or [])}; svg={pr.get('svg')}; "
                  f"cells={pr.get('cells')}; buttons={pr.get('buttons')}; listens={sorted((pr.get('listens') or {}).items())[:8]}; "
                  f"key handlers on={sorted({d for t in KEY_TYPES for d in ((pr.get('listenAt') or {}).get(t) or {})})}; "
                  f"fired={sorted((pr.get('fired') or {}).items())[:8]}; changed on={[k for k, v in (pr.get('steps') or {}).items() if v]}; "
                  f"dialogs={pr.get('dialogs')}; text={cell(pr.get('text'), 80)!r}"
                  + (f"; **{keys_dead(pr)}**" if keys_dead(pr) else "")
                  + (f"; why not: {o.play.get('why')}" if o.play.get("why") else "")
                  + (f"; errors while played: {[e['text'] for e in o.play.get('errors', [])][:3]}" if o.play.get("errors") else ""))
            steps = o.final.get("steps") or []
            if steps:
                w("- seats: " + "; ".join(f"{s['seat']} `{s['model']}` {s['elapsed']}s"
                                          + (f" tools={','.join(s['tools'])}" if s.get("tools") else "")
                                          + (" SKIPPED" if s.get("skipped") else "")
                                          + (f" ERROR {collapse(s['error'], 60)}" if s.get("error") else "") for s in steps))
            if o.final.get("transcript"):
                w(f"- transcript: `{o.final['transcript']}` (" + ("in the ground's logs/" if live else "in the clone") + ")")
            w("")
            w("<details><summary>now — the delivery</summary>")
            w("")
            w("```text")
            w((o.delivery or "(nothing)")[:2500])
            w("```")
            w("")
            w("</details>")
            th = t.then or {}
            if th.get("have"):
                w("")
                w(f"<details><summary>then — sitting {c.sitting}, {th.get('elapsed', 0):.0f}s, {th.get('stages')} stage(s)</summary>")
                w("")
                w("```text")
                w((th.get("delivery") or "(nothing)")[:1500])
                w("```")
                w("")
                w("</details>")
            w("")
    for base, n, lines in repeats(results):
        w(f"## Across the {n} runs of {base}")
        w("")
        w("The models differ from run to run; what recurs is the finding, what does not is noise.")
        w("")
        for line in lines:
            w(f"- {line}")
        if not lines:
            w("- nothing recurred.")
        w("")
    w("## Findings, all together")
    w("")
    any_f = False
    for r in results:
        for i, o in enumerate(r.outcomes, 1):
            for x in o.faults:
                any_f = True
                w(f"- **{r.case.key} · {i}** “{collapse(o.turn.say, 60)}” — {x}")
    if not any_f:
        w("- no mechanical fault in any turn run.")
    w("")
    w("## Questions the system put to a person")
    w("")
    qs = [(r.case.key, i, q, a) for r in results for i, o in enumerate(r.outcomes, 1) for q, a in o.questions]
    if qs:
        for k, i, q, a in qs:
            w(f"- {k} · {i}: {collapse(q, 110)!r} — the pack answered {a!r}")
    else:
        w("- none.")
    w("")
    w("## How these ran, stated" if live else "## The sandbox, stated")
    w("")
    for line in env.get("lines", []):
        w(f"- {line}")
    w("")
    return "\n".join(w_ for w_ in L) + "\n"


# ---------------------------------------------------------------------
# --check: the wires, offline
# ---------------------------------------------------------------------

def check() -> list:
    """Every way the pack could be unplugged from what it stands on, named. [] when it is connected."""
    bad: list = []
    # the engine's wire
    for c in USED_COMMANDS:
        if c not in serve.COMMANDS:
            bad.append(f"the pack sends `{c}` and serve.COMMANDS has no such command")
    for e in USED_EVENTS:
        if e not in serve.EVENTS:
            bad.append(f"the pack reads `{e}` and serve.EVENTS has no such event")
    if serve.PROTOCOL != 1:
        bad.append(f"the pack speaks protocol 1; serve.PROTOCOL is {serve.PROTOCOL}")
    for t in ("delivery", "refused", "aborted", "cancelled", "unreachable"):
        if t not in serve.TERMINAL:
            bad.append(f"`{t}` is no longer a terminal event")
    # the record's shape
    sample = "# Run — x\n\n## Delivery\n\nthe answer\n"
    d = transcript._DELIVERY_RE.search(sample)
    if not d or d.group("t").strip() != "the answer":
        bad.append("transcript._DELIVERY_RE no longer reads a delivery")
    if not standup.GUARD_MARKS or not standup.NEVER_IN_DELIVERY:
        bad.append("the guard marks or the markup shapes are empty")
    if not hasattr(vectors, "CLIENT_TOKEN"):
        bad.append("vectors.CLIENT_TOKEN is gone")
    if not protected(f"x {vectors.CLIENT_TOKEN} y"):
        bad.append("protected() does not see the client tag")
    # the maker's grammar, held against the persona and the flow on a ground made for the purpose
    with tempfile.TemporaryDirectory(prefix="pack-check-") as td:
        g = Path(td)
        for name in ("game",):
            p = g / maker.PROJECTS / name
            p.mkdir(parents=True)
            subprocess.run(["git", "init", "-q"], cwd=str(p), capture_output=True)
        turns = persona() + (flow_turns() if FLOW.is_file() else [])
        for t in turns:
            if t.route not in ROUTES:
                bad.append(f"{t.say!r} declares a route ({t.route!r}) the pack does not know")
            if t.wants not in WANTS:
                bad.append(f"{t.say!r} wants {t.wants!r}, which is not one of {WANTS}")
            if t.route == "*":
                continue
            # a change and a go-back are only read with a project in hand; every other route is read the same
            # with one in hand or without
            for held in ((True,) if t.route in ("change", "go-back") else (False, True)):
                got = predict_route(t.say, held, g)
                if got != t.route:
                    bad.append(f"{t.say!r} is declared `{t.route or 'ordinary'}` and the engine's arithmetic reads "
                               f"`{got or 'ordinary'}` ({'with' if held else 'without'} a project in hand)")
        maker.forget()
    for k, ok in (("a sentence with no maker words", predict_route("hello there", False, ROOT) == ""),
                  ("put it down", predict_route("put it down", True, ROOT) == "put-down")):
        if not ok:
            bad.append(f"predict_route is wrong about {k}")
    for note, route in (("maker: a request to MAKE something ('x') -- the", "make"),
                        ("maker: p went back to version 1, saved as version 2", "go-back"),
                        ("maker: a change to p (version 1) -- the", "change")):
        if observed_route([note]) != route:
            bad.append(f"observed_route no longer reads {note[:40]!r} as `{route}`")
    # the ledger, when it is on this disk (the CI runner has none)
    led = ledger(ROOT)
    if led:
        for key, n in PICKS:
            row = led.get(n)
            if not row or not row.get("runs"):
                bad.append(f"sitting {n} (case {key}) is not in the ledger with runs")
            elif not all(str(r.get("objective") or "").strip() for r in row["runs"]):
                bad.append(f"sitting {n} has a run with no objective")
    if FLOW.is_file():
        try:
            if len(flow_turns()) != 3:
                bad.append("the wife flow does not yield three lines")
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            bad.append(f"the wife flow cannot be read: {exc}")
    # --record reads the maker's NOTES to know what moved; the engine's own writers of those notes must still say them
    src = (ROOT / "manjuel" / "pipeline.py").read_text(encoding="utf-8")
    for frag in ('version {n} saved (', 'went back to version {to}', 'saved as version {n}', 'picked up (version', 'put down -- none in hand now'):
        if frag not in src:
            bad.append(f"pipeline.py no longer writes the maker note `{frag}`; moved_from_notes reads it")
    for note, effect in (("maker: game-3 version 1 saved (index.html, 74 lines)", "make"),
                         ("maker: game-3 went back to version 2, saved as version 4", "go-back"),
                         ("maker: game-3 picked up (version 4)", "pick"),
                         ("maker: game-3 put down -- none in hand now", "put-down")):
        if moved_from_notes([note], "make").get("effect") != effect:
            bad.append(f"moved_from_notes no longer reads {note!r} as `{effect}`")
    with tempfile.TemporaryDirectory(prefix="pack-check-") as td:
        t = Path(td) / "logs"
        t.mkdir()
        (t / "x.md").write_text("# Run — x\n\n- **note:** maker: a request to MAKE something\n\n## Objective\n\nx\n\n## Stages\n\n"
                                "### 1. Expert Coder — `qwen2.5-coder:14b`\n\n_12.5s · skills: a_b, c_\n\nanswer\n\n"
                                "### 2. Steward — `llama3.2:latest`\n\n_skipped_\n\n## Delivery\n\nthe answer\n", encoding="utf-8")
        got = parse_run(Path(td), "logs/x.md")
        if (got["delivery"] != "the answer" or got["notes"] != ["maker: a request to MAKE something"] or len(got["steps"]) != 2
                or got["steps"][0]["tools"] != ["a_b", "c"] or not got["steps"][1]["skipped"]):
            bad.append("parse_run no longer reads a transcript the way transcript.write lays it out")
    # the live runner hands lines to the glass page's own go() and reads Run's state; the page must still have those names
    for used in ("Agent.go(", "Run.running", "Run.engineOpen", "Run.sitting", "Run.turn", "'/boot'", "'/close'"):
        if used not in LIVE_RUNNER_JS:
            bad.append(f"LIVE_RUNNER_JS does not use {used}")
    web = ROOT / "atlas" / "webapp" / "static" / "js"
    if (web / "agent.js").is_file() and (web / "council.js").is_file():
        for frag, fname, label in PAGE_NAMES:
            if frag not in (web / fname).read_text(encoding="utf-8"):
                bad.append(f"the glass page no longer has `{label}` ({frag!r} in {fname}); the live runner hands it lines")
    for key in ("W1", "W2") + tuple(k for k, _n in PICKS):
        try:
            if not live_lines(ROOT, key):
                bad.append(f"{key} has no line to run live")
        except ValueError:
            pass                                   # the ledger or the flow is not on this disk (CI); nothing to hold it to
    for n, idx in NOT_LIVE.items():
        row = led.get(n) if led else None
        if row and any(i > len(row.get("runs") or []) for i in idx):
            bad.append(f"NOT_LIVE names a turn that sitting {n} did not have")
    for n, idx in SMALL_TALK.items():
        row = led.get(n)
        if led and row and any(i > len(row.get("runs") or []) for i in idx):
            bad.append(f"SMALL_TALK names a turn that sitting {n} did not have")
    # the sandbox's own refusals
    for refused, why in ((ROOT, "the ground"), (ROOT / "tests", "a folder inside the ground"), (ROOT.parent, "the ground's parent")):
        if not sandbox_refusal(refused):
            bad.append(f"sandbox_refusal does not refuse {why}")
    with tempfile.TemporaryDirectory(prefix="pack-check-") as td:
        stray = Path(td) / "stray"
        stray.mkdir()
        (stray / "a.txt").write_text("x", encoding="utf-8")
        if not sandbox_refusal(stray):
            bad.append("sandbox_refusal accepts a non-empty directory the pack did not make")
        mine = Path(td) / "mine"
        mine.mkdir()
        (mine / MARK).write_text("x", encoding="utf-8")
        if sandbox_refusal(mine):
            bad.append("sandbox_refusal refuses a directory the pack made")
        try:
            rm_sandbox(stray, Path(td))
            bad.append("rm_sandbox removed a directory the pack did not make")
        except RuntimeError:
            pass
    env = engine_env(ROOT)
    if any(k.upper().startswith(DROP_PREFIXES) for k in env):
        bad.append("engine_env lets a route, the door or an old dial through")
    # the probe: both scripts go in, once each, and the page's text is untouched around them
    page = "<!doctype html><html><head><title>t</title></head><body><p>x</p></body></html>"
    probed = with_probe(page)
    if probed.count("window.__play=") != 1 or probed.count("[[PLAY]]") != 1 or "\n" in probed.replace(page, ""):
        bad.append("with_probe does not put the probe in once, on one line")
    if not probed.startswith("<!doctype html><html><head>") or not probed.endswith("</body></html>"):
        bad.append("with_probe moved the page's own frame")
    return bad


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------

def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(prog="pack.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="the wires, offline")
    ap.add_argument("--list", action="store_true", help="the cases and the route read for each turn; nothing runs")
    ap.add_argument("--sandbox", metavar="DIR", help="a directory outside the ground the pack may own")
    ap.add_argument("--only", default="", help="cases whose key contains this (several, comma-separated)")
    ap.add_argument("--keep", action="store_true", help="leave the clones when done")
    ap.add_argument("--repeat", type=int, default=1, help="run each wife case this many times (the models differ run to run)")
    ap.add_argument("--probe", metavar="FILE", help="play one page in the maker's headless browser and print what the probe saw")
    ap.add_argument("--runner", action="store_true", help="print the JS that hands lines to the front page's own go(); paste it into the glass page after Boot")
    ap.add_argument("--lines", metavar="CASE", help="print the lines of a case that are run live, as JSON (W1, W2, A79, A70, B170, C221)")
    ap.add_argument("--record", metavar="SPEC", help="judge sittings the system ran LIVE, from its own record, read-only: '336=W1,337=W2,338=A79,...' (sitting=case)")
    ap.add_argument("--to", metavar="DIR", help="where --record writes its raw outcomes and report (default: a folder in the system temp dir)")
    ap.add_argument("--rejudge", metavar="DIR", help="judge the raw outcomes a run kept in DIR again, with this judge, and write a new report (no models)")
    a = ap.parse_args(argv)

    if a.check:
        bad = check()
        for b in bad:
            print("  RED:", b)
        print("  the pack is connected." if not bad else f"  {len(bad)} wire(s) cut.")
        return 1 if bad else 0

    if a.runner:
        print(LIVE_RUNNER_JS)
        return 0
    if a.lines:
        print(json.dumps(live_lines(ROOT, a.lines), ensure_ascii=False))
        return 0

    if a.record:
        pairs = []
        for part in a.record.split(","):
            num, _, key = part.partition("=")
            pairs.append((int(num), key.strip()))
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        top = Path(a.to).resolve() if a.to else Path(tempfile.mkdtemp(prefix="pack-record-"))
        top.mkdir(parents=True, exist_ok=True)
        got = []
        for num, key in pairs:
            r = record_case(ROOT, key, num)
            got.append(r)
            keep(r, top)
            print(f"  [{key}] sitting {num}: {sum(1 for o in r.outcomes if not o.skipped)} turn(s) judged, "
                  f"{sum(len(o.faults) for o in r.outcomes)} fault(s)")
        engine = f"manjuel {getattr(__import__('manjuel'), '__version__', '?')}, serve protocol {serve.PROTOCOL}"
        sittings = ", ".join(f"{num} = {key}" for num, key in pairs)
        lines = record_lines(pairs)
        text = render(got, datetime.now().strftime("%Y-%m-%d %H:%M"), {"mode": "record", "sittings": sittings, "engine": engine, "lines": lines})
        (top / "meta.json").write_text(json.dumps({"started": datetime.now().strftime("%Y-%m-%d %H:%M"), "engine": engine,
                                                   "lines": lines, "mode": "record", "sittings": sittings}, ensure_ascii=False),
                                       encoding="utf-8", newline="\n")
        rep = top / f"pack_{stamp}.md"
        rep.write_text(text, encoding="utf-8", newline="\n")
        print(f"  report: {rep}")
        held_by = sitting_open()
        if a.to:
            print("  not copied to logs/: --to was given, and it writes there and only there")
        elif held_by:
            print(f"  not copied to logs/: {held_by} (RULE 9)")
        else:
            dst = LOGS / f"pack_{stamp}.md"
            dst.write_text(text, encoding="utf-8", newline="\n")
            print(f"  report: {dst}")
        nf = sum(len(o.faults) for r in got for o in r.outcomes)
        print(f"  {nf} fault(s) across {sum(1 for r in got for o in r.outcomes if not o.skipped)} turn(s), judged from the record.")
        return 1 if nf else 0

    if a.rejudge:
        top = Path(a.rejudge).resolve()
        found = sorted(top.glob("case_*.json"))
        if not found:
            print(f"  nothing to judge: no case_*.json in {top}")
            return 2
        order = [c.key for c in build_cases(ROOT)]
        loaded = [load(f) for f in found]
        loaded.sort(key=lambda r: (order.index(r.case.key.split(".")[0]) if r.case.key.split(".")[0] in order else 99, r.case.key))
        for r in loaded:
            rejudge(r)
        meta = json.loads((top / "meta.json").read_text(encoding="utf-8")) if (top / "meta.json").is_file() else {}
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        text = render(loaded, str(meta.get("started") or stamp) + " (judged again " + stamp + ")",
                      {"sandbox": str(top), "engine": meta.get("engine", "?"), "lines": meta.get("lines", []),
                       "mode": meta.get("mode"), "sittings": meta.get("sittings", "")})
        rep = top / f"pack_{stamp}.md"
        rep.write_text(text, encoding="utf-8", newline="\n")
        print(f"  report: {rep}")
        nf = sum(len(o.faults) for r in loaded for o in r.outcomes)
        print(f"  {nf} fault(s) across {sum(1 for r in loaded for o in r.outcomes if not o.skipped)} turn(s), judged again.")
        return 1 if nf else 0

    if a.probe:
        got = play(Path(a.probe).read_text(encoding="utf-8", errors="replace"))
        pr = got.get("probe") or {}
        print(json.dumps({"loaded": got["loaded"], "why": got["why"], "errors": got["errors"][:5],
                          "graphical": graphical(pr), "plays": plays(pr), "keys_dead": keys_dead(pr), "probe": pr},
                         indent=1, ensure_ascii=False))
        return 0

    cases = build_cases(ROOT, a.only)
    if a.repeat > 1:
        more = []
        for c in cases:
            if c.wife:
                more += [Case(f"{c.key}.{i}", c.title, c.source, c.turns, c.sitting, c.wife, c.note) for i in range(2, a.repeat + 1)]
        cases += more
    if a.list:
        with tempfile.TemporaryDirectory(prefix="pack-list-") as td:
            for c in cases:
                print(f"{c.key:5} {c.title}  [{c.source}]" + (f"  <-- {c.note}" if c.note else ""))
                held = False
                for i, t in enumerate(c.turns, 1):
                    r = predict_route(t.say, held, Path(td)) if c.wife else ""
                    held = held or r in ("make", "change")
                    print(f"      {i:>2}. {collapse(t.say, 80)!r}" + (f"  -> {r or 'ordinary'}" if c.wife else "")
                          + (f"  [skip: {t.skip}]" if t.skip else ""))
            maker.forget()
        return 0

    if not a.sandbox:
        print("  refused: --sandbox DIR is required; the pack never runs an engine on the ground.")
        return 2
    top = Path(a.sandbox).resolve()
    why = sandbox_refusal(top)
    if why:
        print(f"  refused: {why}")
        return 2
    if not cases:
        print("  no case matches.")
        return 2
    bad = check()
    if bad:
        print("  refused: the pack's wires are cut:")
        for b in bad:
            print("   -", b)
        return 1
    top.mkdir(parents=True, exist_ok=True)
    (top / MARK).write_text("made by tests/pack.py; safe to delete\n", encoding="utf-8")

    started = datetime.now()
    stamp = started.strftime("%Y-%m-%d_%H%M%S")
    print(f"  test pack {stamp}: {len(cases)} case(s) in {top}")
    results: list = []
    try:
        for c in cases:
            if not c.turns:
                results.append(CaseResult(c, harness_fault=c.note))
                print(f"  [{c.key}] not run: {c.note}")
                continue
            print(f"  [{c.key}] {c.title} -- {len(c.turns)} turn(s)")
            res = run_case(c, top, a.keep, print)
            results.append(res)
            keep(res, top)
            if not a.keep:
                try:
                    rm_sandbox(Path(res.clone), top)
                except (RuntimeError, OSError) as exc:
                    print(f"  [{c.key}] clone not removed: {exc}")
    except KeyboardInterrupt:
        print("  interrupted; the report is written from what ran.")

    lines = [
        "each case ran in its own clone: the tracked tree, byte for byte, plus memory.md, the memory chain, SEAT_LOG.md and the index; its own `.git`; its own ledger cut to the lines before the replayed sitting",
        "no `.env` in any clone (RULE 7): dials at their defaults, `MANJUEL_KEEP_ALIVE=30m` and `MANJUEL_VRAM_GB=15` set from `.env.example`; no hosted route is on, so nothing left the machine (RULE 4); git push is refused by default (`MANJUEL_GIT_REMOTE` unset)",
        "no logs/, worlds/, atlas/ or projects/ in a clone: an index rebuild, a commit or a project is the clone's alone, and `git status` there starts clean",
        "ONE EDIT in each clone's code: `manjuel/voice.py` is told the machine has no speech engine, so a replayed `speak` says so instead of using the operator's speakers",
        "the engine imported its code from the clone (an isolation probe ran before every start)",
        "the old record (ledger lines, logs/ transcripts) was read, never written",
        "questions the engine asked were answered by the pack as a willing person: yes to a confirm, the default to a kind or a title, skip to a retry prompt",
    ]
    env = {"sandbox": str(top), "engine": f"manjuel {getattr(__import__('manjuel'), '__version__', '?')}, "
           f"serve protocol {serve.PROTOCOL}", "lines": lines}
    text = render(results, started.strftime("%Y-%m-%d %H:%M"), env)
    (top / "meta.json").write_text(json.dumps({"started": started.strftime("%Y-%m-%d %H:%M"), "engine": env["engine"],
                                               "lines": lines}, ensure_ascii=False), encoding="utf-8", newline="\n")
    rep = top / f"pack_{stamp}.md"
    rep.write_text(text, encoding="utf-8", newline="\n")
    print(f"  report: {rep}")
    held_by = sitting_open()
    if all(r.case.key == "S0" for r in results):
        print("  a smoke run: not copied to logs/")
    elif held_by:
        print(f"  not copied to logs/: {held_by} (RULE 9)")
    else:
        dst = LOGS / f"pack_{stamp}.md"
        dst.write_text(text, encoding="utf-8", newline="\n")
        print(f"  report: {dst}")
    nf = sum(len(o.faults) for r in results for o in r.outcomes)
    print(f"  {nf} fault(s) across {sum(1 for r in results for o in r.outcomes if not o.skipped)} turn(s).")
    return 1 if nf or any(r.harness_fault for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
