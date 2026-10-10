# Runbook

The machine misbehaving, not a seat misbehaving. For a seat that said
something wrong, read `logs/` — HANDOFF.md's *Debugging a sitting* is that
procedure, and it starts with **check the disk before the transcript**: a
seat's account of what it did is testimony (LAW 5); the file is the fact.

Run everything below from `Desktop\Research`.

**The morning, in one command.** `python tests\standup.py` runs the seats
through nine fixed objectives on the live rack, opens and tolls a sitting,
and writes `logs\standup_<stamp>.md`. About ninety seconds, and it runs
unattended. Read REVIEW THESE FIRST, then the deliveries; write what feels
off in TASKS.md.

    --court    the court alone: six seats, deepseek-r1 and gemma4, minutes.
               Out of the morning set on his ruling 2026-09-09 -- it was 73%
               of the run. (It was also the case that could stop at a question:
               a failed seat asked `retry / skip / abort?` of a run with no
               keyboard. Every standup run is UNATTENDED since 2026-09-29: such
               a seat is skipped, the prompt's own default, and the report
               names it.)
    --all      both sets.
    --only <name>   the cases whose name contains it, the court included --
                    naming one is asking for it.
    --dry      the harness on a stub, no models.

From the glass (since 2026-09-28): the door's `standup_run` tool (`set` =
morning, the default, `court` or `all`) runs this same script in the world
with the python the door runs the engine with, and hands back the tally line
and the report's path over everything it printed. It refuses while an engine
is open on the world or its ledger has an open sitting, because the standup
opens and tolls a sitting of its own. The suites go the same way: `suite_run`
(`set` = strokes, smoke, or both, the default) runs `tests\test_manjuel.py`
and `tests\smoke_cli.py` in the world one after the other, the suites stamp
`tests\last_run.json` as they always have, and the head reads that stamp
back. His ruling, 2026-09-28: a run from the glass whose record matches is
proof, and the release gate reads the same stamp either way.

Only a run of the WHOLE morning set is written to the record as suite
"standup"; anything less is "court" or "partial", so a one-case run cannot
satisfy the release gate. Where to look for anything it names: BUILDMAP.md.

**The wife test, mocked, and the record replayed -- run live.** Open the glass in the Browser pane, Boot on the front page, then
paste `python tests\pack.py --runner` into the page and call `window.__case(<python tests\pack.py --lines W2>)`: the page hands each
line to its own `go()`, waits for the answer, and stops at any question put to the person. `/close` pays the toll. Every case is a
sitting on the ledger. Then `python tests\pack.py --record 336=W1,337=W2,...` (sitting=case) judges those sittings from the
ledger, the transcripts and `projects\`, read-only, and writes `logs\pack_<stamp>.md` while no sitting is open. Read the
"Reviewer's notes" first (written by hand after a run), then the scorecards, then the turns. Commits, `git_cycle`, index rebuilds and
anything that speaks are not run live (`NOT_LIVE` in the pack). The same cases run in clones of the ground with
`--sandbox <a folder outside the ground>`; `--list` shows the cases, `--check` is the wire.

---

## Starting the system

Two processes and a browser. Neither starts by itself, and nothing opens a
sitting behind you.

**You need Go for this half.** The engine wants only Python and Ollama; these
two servers are Go, built from source. QUICKSTART's "You need" is the ENGINE's
list and does not name a Go toolchain, because nothing in the REPL wants one.
If `go version` answers, you are ready.

**And atlas is its own repository.** Since 2026-09-10 the core and atlas are
two repos sharing one ground (`atlas/` is gitignored by the core). Cloning the
core does NOT bring the dashboard: without atlas there is nothing here to
build, which is what a second machine finds first.

**So clone it, INTO the ground, at exactly `atlas`.** Every build path below
and the core's own `.gitignore` assume that name and that place.

    cd <YOUR-GROUND>
    git clone https://github.com/thebrotherscarr-bit/Atlas.git atlas

The core itself is `https://github.com/thebrotherscarr-bit/Manjuel.git`. Both
are public. Until 2026-09-11 this page told you atlas was a separate repo and
then gave no URL for it — a stop sign with nothing past it, which is the first
thing a second machine hits.

**Offline?** Make the bundle at transfer time, never ship a stale one:

    git bundle create atlas.bundle main          # run inside atlas/
    git clone atlas.bundle atlas                 # on the other machine

Use `main`, not `--all`. `--all` carries every local branch, and a local
branch can hold material that was deliberately kept off the remote.

**Build the Rust spine first.** `verify_chain` shells a Rust binary, and the
Go halves cannot prove themselves without it — `atlas/tests/prove.py` reports
every leg that needs it ABSENT, naming `cargo build -p atlas` as the command
that would answer. ABSENT is never a pass: those legs proved nothing.

Until 2026-09-11 this page said those legs went RED, and one of them really
did: `check_trade_parity` refused with a COMMAND rather than a missing path,
which prove.py's absence check did not recognise, so a fresh clone's first
battery reported a break on a tree where nothing was wrong. Both are fixed.

    cd atlas
    cargo build -p atlas        # -> atlas\target\debug\atlas.exe

Nothing needs to be told where it is: the door walks out from its own
location to find `target\{debug,release}\atlas.exe`. `--atlas-bin` and
`ATLAS_BIN` still override, and both win over the walk.

**Build them once.** Both binaries are `*.exe`, which `.gitignore` already
covers, so they live beside their own source and never reach a commit.

    cd atlas\line
    go build -o atlas-mcp.exe .\cmd\atlas-mcp
    cd ..\webapp
    go build -o atlas-webapp.exe .

Rebuild after any Go change. The webapp EMBEDS its own HTML, CSS and
JavaScript (`go:embed`), so a change to a page is not live until you rebuild
and restart it -- editing the file on disk does nothing to a running server.

**Start the door.** `atlas-mcp` is the MCP door: it serves the 89 tools and it
is the only thing that spawns a Manjuel engine. It holds `127.0.0.1:8090`.

    cd atlas\line
    .\atlas-mcp.exe --http 127.0.0.1:8090 --auth --tenant research=<PATH-TO-YOUR-GROUND> --default-project research --manjuel "python <PATH-TO-YOUR-GROUND>/manjuel.py" *> mcp.log

`<PATH-TO-YOUR-GROUND>` is the folder holding `manjuel.py` -- an ABSOLUTE
path, forward slashes, no trailing slash. This line carried the author's own
`C:/Users/novad/Desktop/Research` twice until 2026-09-10: it worked on exactly
one machine and pointed at nothing on any other.

`--tenant name=path` declares a world; repeat it for more. `--default-project`
is the one the dashboard uses when you do not name another. `--manjuel` is the
command the door runs to raise an engine -- `--headless` and `--ground` are
appended by the door itself, so do not add them.

**`--auth` and the service wire (since 2026-09-25).** With `--auth` the door
demands a bearer on every call and HOLDS a writing call from anything but the
glass until you decide it on its card, pinned at the foot of the front page's terminal (or on the GitHub page); without it, RULE 6 is a
sentence. A writing tool's reading action is not held: `git_tag list` and
`git_branch list` (their default, too) answer any bearer, while `cut`, `send`,
`remove`, `new`, `switch` and `close` wait for your hand (since 2026-09-28). A
secret a parked call carries (the auth verbs' re-proof `key`) is withheld where
the queue is shown and kept for the call. And a flow's gate may declare
`grants`: the writing tools your `continue` authorises for the nodes after it,
until the next gate. Those calls run instead of parking and are written to
`state/holds.jsonl` as `crossed`, naming the run and the gate -- `version-tag`'s
two gates grant `git_tag` (since 2026-09-28). Two secrets live in `.env` and nowhere else (RULE 7):
`ATLAS_SERVICE`, the same-computer wire the door and the glass share, and
`MANJUEL_MCP_ATLAS_KEY`, the bearer the council presents (minted once with
`auth_key_create` while the door was unarmed, for research alone; which
tenants a live key carries is moved with `auth_key_scope` -- the list replaced
whole, possession re-proved like create and revoke, the move audited, and from
any hand but the glass parked in the holds for yours -- since 2026-09-28).
Neither process reads `.env` itself: put the wire in the environment before
starting each one --

    $env:ATLAS_SERVICE = ((Get-Content .env | Where-Object { $_ -match '^ATLAS_SERVICE=' }) -replace '^ATLAS_SERVICE=','').Trim()

-- and never on a command line, where `ps` reads it. The boot line says which
state the door is in: `auth=true, holds ARMED` or `auth=false, holds off`.

**Start the glass.** `atlas-webapp` serves the dashboard on `:8091` and talks
to the door at `127.0.0.1:8090`.

    cd atlas\webapp
    .\atlas-webapp.exe *> web.log

    ATLAS_SERVICE=<wire> the door's service wire, from .env as above; the boot
                         line then says "service wire held"
    ATLAS_WEB_PORT=<n>   serve on another port
    OLLAMA_HOST=<url>    if the rack is not on the default loopback; a host with no port means
                         Ollama's own, 11434 (since 2026-10-03)

**Open it.** `http://127.0.0.1:8091`

The first time, it asks for your name and a PIN of 4 to 8 numbers; after that
it opens on a lock screen, and the sidebar's Lock button locks it again. It
answers this computer only (127.0.0.1) and keeps its door shut at every start
-- since 2026-09-21; before that it listened on every address with no gate at
all. The PIN is never stored, only a hash of it in `atlas\webapp\data\user.json`.

**The shell tabs (since 2026-10-03).** The front page's Bash and Python tabs run what you type through the door's
`shell_run`, which only the glass may call: the door has to run with `--auth`, or it cannot tell your glass from a
seat and answers the tool to no one. Bash is Git Bash, found by the `git` on the door's PATH (never the bare word
`bash`, which on this machine is the WSL stub); Python is the python the door runs the engine with, one session per
world that keeps its names until `/reset`, a runaway entry, or a door restart. A plain look runs at once; anything
that writes shows a card and waits for your click; a secret or a path outside the ground is refused by name. Every
run, hold and refusal is a line in that world's `state/holds.jsonl`. The command gets a built environment with none of
the door's keys, so one that needs a variable has to be told it. When starting the door from PowerShell, quote the
value of `--manjuel` as ONE argument (`--manjuel "python <ground>/manjuel.py"`): passed as an array element it is split
in two and the door refuses to start.

**Aider (since 2026-10-04).** The front page's Aider tab drives Aider through the door's `aider_run`, `aider_undo` and
`aider_status`; the first two only the glass may call, so the door has to run with `--auth` for the same reason as the
shell. Aider lives in `aider/` at the ground's root, which `.gitignore` keeps out of every save and the core's suites
skip: `aider\venv` is the pip install (`aider-chat` 0.86.2 and the 110 packages it needs, about 640 MB, fetched from
PyPI once, at install time, on his word of 2026-10-04) and `aider\work` is its home, its temp folder and one folder per
run (the last 30 are kept; a run's folder holds the instruction, Aider's own transcript, the files as they were, which
is what Undo restores, and the files as Aider left them). To install it again, with a Python 3.10 to 3.12 (it does not
run on newer ones): `python -m venv aider\venv`, then `aider\venv\Scripts\python.exe -m pip install aider-chat==0.86.2`.
Nothing downloads when it runs: the door starts it with a built environment (none of the door's keys), no analytics,
update check, URL scraping or shell suggestions, its model metadata as a file, and inside a wall (it writes only to the
run's own scratch folder, reaches nothing but this machine, and starts no other process; `atlas/CHANGELOG.md` has the
wall's honest limits). The model is the coding seat's own (`agents/expert_coder.md`: Model Target and Context): the door
loads it into Ollama at that window before Aider starts, and a file bigger than the window is refused up front, so
Aider cannot take most of the big modules (the measurement is WHAT'S LEFT B21's). The edit it makes lands only on a
line of work, unsaved: the suites and the Land click stay yours. A tree that is copied or tarred for a proof must leave
`aider/` out.

**Stop them.** They are servers; they run until stopped. Nothing is lost --
the engine already exits with every sitting, and both processes keep no state
of their own.

**BY PID AND PATH, NEVER BY NAME (2026-09-22).** A second `atlas-mcp.exe` has
been running on this machine since 2026-09-21 from `Desktop\Archive` -- outside
this ground and nothing to do with it -- and `Get-Process atlas-mcp` names it
too, so the line this page used to carry would have stopped somebody else's
door along with yours. Ask which is which, then stop the one you mean:

    Get-CimInstance Win32_Process -Filter "Name='atlas-mcp.exe' OR Name='atlas-webapp.exe'" |
        Select-Object ProcessId, ExecutablePath
    Stop-Process -Id <the pid whose path is under Desktop\Research>

The glass keeps its sessions across a restart, so stopping and starting it does
not sign you out; the door holds none, and a restart of it ends nothing but
itself -- close the sitting first if one is open.

## Running it from the dashboard

The pages, in the order the panel lists them:

    Dashboard   the launchpad. THE ENGINE card is first because nothing below
                it runs until one is open. Then the box you type in, the
                brief (silent when there is nothing to say), and THE
                REPOSITORY with its Commit and Push buttons. It repaints
                itself every 15s and says so when what it shows is stale.
                PROJECTS, under the run (2026-09-21): what the maker made,
                each with its versions and its page running in a sandboxed
                frame; "Work on this" and "Put it down" say the words for you.
                A page there has no storage of its own -- a game forgets its
                high score -- and opened from projects\<name>\ it keeps it.
    Chat        the same conversation, kept. The composer is disabled with
                the reason written under it when no engine is open.
    Agents      the fourteen seats as they declare themselves in agents/.
    Evals       the last run whole -- every seat, tool, result, timing --
                and evals scored by hand.
    Records     the estate's own memory: the suite and standup proof cards,
                the sittings, and 141 documents in seven kinds (doctrine,
                record, spec, agents, commands, skills, logs), each opening
                whole with a sha256 receipt.
    Settings    the dials.

**The loop, four clicks.**

    1. Boot            opens an engine AND a sitting. Nothing opens one for
                       you; a sitting nobody meant to start is what every
                       refusal in this system guards against.
    2. type and Run    the turn runs on the Dashboard, the answer lands under
                       the box, and the whole trace goes to Evals.
    3. Commit / Push   type the message in THE REPOSITORY's field first. Both
                       go THROUGH THE COUNCIL, not around it: the law gate
                       stamps the act, the Router runs `git_commit`, and the
                       commit body carries the sitting id. A button that
                       shelled out to git would be a second write-path past
                       everything the estate checks.
    4. Close sitting   writes `ended` and reaps the engine, and pays the toll
                       -- unattended -- if the sitting ran anything. A sitting
                       that ran nothing closes with no toll: sitting 220,
                       closed here 2026-09-14 with zero runs, reads
                       `toll_paid: false`. (Until that day this line said a
                       close always pays the toll.)
                       DO THIS. A sitting left open is what makes the next
                       Boot refuse.
                       AND IF YOU DO NOT, the engine does it for you: thirty
                       minutes with no command between turns and it closes
                       its own sitting exactly as this button does (serve.py
                       IDLE_CLOSE, 2026-09-16), and the next Boot opens a new
                       one. Never mid-turn, and never while the council is
                       waiting on your answer.
                       AND IF IT DIES, its sitting does not hold the world
                       (2026-09-22): the door reads the process the open
                       line names, and when that process is gone the next
                       Boot opens anyway and the new engine closes the old
                       line as it starts ("left open by a process that is
                       gone"). A hang-up is heard at once, and a fault or a
                       Ctrl-C in the engine's boot closes its sitting on the
                       way out.

**Or the whole turn in one act.** `git_cycle` is step 3's commit and push as a
single skill, with the proofs read first and the push verified after. Type it
on the Dashboard the way you would any objective, and give it the message --
that is the one part it cannot read off the ground:

    git_cycle: "what this commit is"

It does five things and reports what each one said:

    THE PROOFS            the six file-readable checks the boot report asks,
                          of which ONLY TWO GATE A COMMIT: strokes and smoke,
                          green AND fresh. A red or STALE one there REFUSES THE
                          SHIP by name and nothing is committed. The other four
                          -- standup, SPEC vs CHANGELOG, DAYBOOK, HANDOFF --
                          are read and PRINTED but do not stop a commit: a
                          commit does not cut a tag, close a session or end a
                          day, and it must never need a live rack. They are the
                          TAG's to answer; `python tests/release.py --check`
                          still wants all nine.
                          It does not RUN the suites -- spawning python inside
                          the engine is measured unsafe here -- it reads the
                          verdict they already left, which is why a proof older
                          than the code is refused.
    THE GROUND            what is about to be committed. Clean tree, no commit.
    THE COMMIT            the hash, or a refusal.
    THE PUSH              git's own output.
    THE PROOF IT LANDED   the local head and the remote head, side by side.
                          A push exiting 0 is not proof the remote moved; on
                          2026-09-10 one reported success while origin sat a
                          commit behind. These two lines are what closed that.

It refuses rather than guesses: no message, a red proof, nothing to commit, the
wall shut, not a repository -- each names itself and stops. Nothing half-runs.
On the main line GitHub refuses its push since 2026-10-09: main takes nothing
but a pull request whose checks have passed.

**Before you start, and before you tag.** Two read-only reports answer the two
questions that used to mean opening six files in order. Neither writes
anything, and neither is a skill — they are run directly:

    python -m manjuel.doctrine            where the estate stands
    python -m manjuel.doctrine --check    the doctrine check

`doc_pass` — the STATE of the record: which DAYBOOK entry is newest and whether
it was closed, whether there is a HANDOFF for today, how many CHANGELOG entries
stand under Unreleased, how many TASKS lines are still on the table, the
repository (head, dirty, local against remote, version), and whether the proofs
are green. It reads TASKS.md and NEVER writes it — a hand does not add work to
your list.

`doctrine_check` — whether the docs still describe what the system performs
(LAW 6): the law chain and any law drafted but unsealed (the appendable
`law/LAW_LEDGER.md` with how far its seal reaches); whether the skill
library agrees with the handlers behind it; whether every file holding the
version says the same number; any suite tally left standing in a living doc;
any backticked path that resolves to nothing. Every finding names its file and
line.

**WHY THEY ARE NOT SKILLS.** They were, for about an hour on 2026-09-10, and
the cost landed on the ROUTER'S SHORTLIST. Both describe the record, and this
estate's commonest question is about the record — so they outranked the right
answer on every doc question, and `semantic_search` stopped being offered at
all. A standup case green all morning went to no tool at 09:59: the Router
burned its whole thinking budget weighing them. Arithmetic that calls no model
and makes no judgement has no business in a roster the Router reads on every
turn. The operator named it: "you have too many knobs."

Both are arithmetic. Dated ledgers (HANDOFF, SEAT_LOG, DAYBOOK, CHANGELOG,
TASKS, REFUSALS, memory, BUILDMAP) are skipped on purpose — a number in a
ledger is a true record of its day, not a claim about now.

Push is disabled unless the wall is open (`MANJUEL_GIT_REMOTE` in `.env`) and
there is something to push; hover it and it says which.

**Asking for a change to the harness itself (2026-09-28).** Name the file
with its folder and the passage in backticks, with a change verb:

    In manjuel/skills.py, add `foundation` to the `_NEVER_WRITTEN_TOP` dict,
    one line beside the `law` entry.

The engine reads that by arithmetic -- no Router, no plan -- fetches
`_NEVER_WRITTEN_TOP` whole off the file's own map, and seats the Expert Coder
alone with it; what it answers goes through `ground_edit` and the delivery is
the door's own line. ON MAIN THE DOOR REFUSES (RULE 6): open a line of work
first (Lines of work in the GitHub tab, or the `coder-tree` flow's gate), and
merging it back is yours, from the GitHub tab (since 2026-10-09): save the line
and send it, open a pull request under Pull requests, and once every check on
it has passed, Merge on GitHub merges it there as a merge commit and brings the
new main line down to this machine. Until then the tab had no merge button and
the door no such verb, so it was your terminal's. Since the same day main takes
nothing else, in either repository: GitHub refuses a send to main that did not
come through a pull request whose checks have passed, yours included, and the
door refuses Land onto main, and a send of main, by name (WHAT'S LEFT I1's seventh step). The name must be exact and on the map (`help`
is not `helper`); a bare `.py` is the workspace, not the ground. A DOCUMENT IS
ASKED BY HEADING (2026-09-29), a root document by its bare name:

    In RUNBOOK.md, under `The dials`, say that MANJUEL_NO_WARM takes 1, true or yes.

The Coder is handed that section whole, through its subsections; `dials` alone
would be refused, because two headings here contain it. What it answers lands
on that file or nowhere -- an edit, or the passage rewritten whole; and a file
that already carries what the gate refuses (skills.py's loopback `urllib`)
still takes an edit that adds none of it. Type the request without a tool's
own words in it ("the founding documents" names semantic_search, and the
window shuts). REFUSALS §28 lists what the engine answers with no seat.

## Running it from the terminal instead

    python manjuel.py            the REPL -- the same engine, no glass
    python manjuel.py --version  what version this is
    python manjuel.py --help     the argument contract

The REPL opens its own sitting and prints the boot report: GROUND (seats,
skills, pipelines, and THE MAP OF THE CODE -- the ten files the rest of the
ground leans on hardest, with their top names, read off the disk at every
boot), RACK (what Ollama holds and what is warm), RECORD (index, memory,
transcripts, what the suites last proved), GATE (git, whether remote
operations are permitted, and the release gate's verdict) and VOICE. Every
block degrades on its own -- if the rack is unreachable that block says so and
the rest still prints, and the same is true of the map.

The map answers "where do I start" without anyone asking. To ask it something
narrower -- where one name is declared, and which files name it -- the skill
is `symbols <name>`; with no name it prints twenty-five files instead of ten.

**One engine per world.** The dashboard and the REPL both open a sitting on
`research`, so they refuse each other by design. Close one before opening the
other.

## The skills and the tools

Two different things, and it is worth keeping them apart.

**Skills** are what a SEAT can do -- 42 of them, declared as markdown in
`skills\`, hot-reloaded into a running session at the next turn. A seat asks
for one by keyword and the engine runs it; the law gate can refuse it, and a
refusal names the law. Read them on Records -> skills, or `commands.md` for
what can be asked for in words.

**Tools** are what ATLAS serves over MCP -- 82 of them, listed at
`http://127.0.0.1:8090/tools` and reachable from the glass through
`POST /api/tools/call`. They are read-only unless their declaration says
`Writes: true`. The ones the dashboard itself leans on:

    git       branch, head, dirty counts, upstream, whether remote is walled
    proofs    the suites, the standups, the parity runs and the sittings
    seats     the seat declarations, read from agents/ and pipelines.md
    records   the estate's documents by kind, one served whole with a receipt
    muster    the declared worlds
    rack_list what the rack holds
    projects  what the maker made: each project's versions, one page served whole

Thirty-one of the eighty-two have no page yet (counted 2026-09-17; `projects`, added
2026-09-21, has one -- the Dashboard's Projects card) -- the record and law readers,
the rack commands, the mesh, keys and tenants. They answer over MCP today; they
have no button.

## The dials

`.env` in this folder, gitignored and never printed. `.env.example` names every
one with what it does. The ones that change how a run behaves:
`MANJUEL_GIT_REMOTE` (the push wall), `MANJUEL_RACK_PULL` (may models be
downloaded), `MANJUEL_VRAM_GB`, `MANJUEL_KEEP_ALIVE`, `MANJUEL_SEAT_TIMEOUT`,
`MANJUEL_SKILL_TIMEOUT`. The older `CHAINKIT_` spellings still answer.

## When starting goes wrong

    "research has an open sitting (N, opened ...)"
        A sitting is open and the process that opened it is STILL RUNNING --
        a REPL on that world, or an engine this door did not start. Close it
        there. Since 2026-09-22 this is never a dead process's line: the door
        reads the pid the line names, and when that process is gone it opens
        the world and the new engine closes the old line as it starts. A line
        with no pid (only lines written before 2026-09-17 lack one) is never
        judged; if one is open with nothing behind it, it is closed by
        APPENDING a closing line, never by editing the one already written.

    the dashboard shows something that is not true
        It repaints every 15s and confesses when it is over a minute stale.
        If a page still looks old after a rebuild, that was the missing-ETag
        fault -- fixed 2026-09-09; every static file now revalidates.

    "mcp unreachable"
        The door is not running, or not on 8090. Check `atlas\line\mcp.log`.

    the glass is locked and the PIN is forgotten
        Delete `atlas\webapp\data\user.json` and reload the page: it asks for
        a name and a new PIN. Nothing else is lost -- the record lives
        elsewhere. "Too many tries" is five wrong PINs in a row; the lock
        opens again after a minute, and the screen counts it down.

    the rack is unreachable
        `ollama serve`. The boot report's RACK block says so and the rest of
        the report still prints.

## Manjuel will not start

**`RACK UNREACHABLE — the ground is open, the models are not.`**

Ollama is not running. The ground opened anyway on purpose: the record, the
palette, git state and the ground's own skills do not need models.

    ollama serve

It reconnects on the next turn — no restart needed. Ollama is *the* server
here (operator ruling, sitting 33); there is no fallback by design.

**`Missing model tags referenced by agents/ or skills/`**

A seat or skill declares a tag that is not installed. The boot report names
each one with its own pull command. Either pull it, or point that seat at a
tag you have — `agents/*.md`, one line, then `/reload`.

**Something else, at import.** Run the strokes: they need no model and no
network, and a parse error or a bad seat file shows up there in a second.

    python tests/test_manjuel.py

---

## Git will not commit

**`Unable to create '.git/index.lock': File exists`**

An interrupted `add` or `init` left a lock behind. Git never cleans these up.
Manjuel names it with its age and the exact removal command rather than
inventing a cure (that fix is from sitting 6). A lock older than two minutes
with no git process behind it is stale, not contended:

    del .git\index.lock

**Never run git writes from a sandboxed agent's shell.** A mount can create
files it cannot unlink, so a failed commit leaves exactly this lock behind and
blocks yours. Commits are the operator's act anyway (RULE 6).

**`remote operations are off`** on pull or push — that is not a fault. Remote
git is gated behind `MANJUEL_GIT_REMOTE=1`; a push cannot be recalled once
fetched, so it is yours to make, not a seat's.

**`git rev-parse timed out` from the headless door, on a ground that is
plainly a repository.** Fixed 2026-09-09; if it ever returns, this is why.
`subprocess.run()` with no `stdin` hands the child the PARENT's stdin. In the
REPL that is a console and harmless. Under `manjuel.py --headless` it is the
pipe `serve.Inbox` has a thread permanently blocked reading, and git never
returns — every call dies on its timeout, and `git_commit`/`git_push` then
refuse with "this ground is not a git repository" about a repository. Every
git call in `gitstate.py` now passes `stdin=DEVNULL`; two strokes hold it
there. Measured: 0.12s with no such thread, 5.02s with one, 0.02s with the
fix.

---

## The card is full / everything is slow

    run the rack          in the REPL — prices VRAM live, model by model

The card is 16GB and the resident set normally sits near the ceiling. Waking a
cold seat (the coder, or a world's agent) costs an eviction and the reload
that follows. That is the budget working, not a fault — but it explains a
sudden 7-second pause on the first code question of a sitting.

**Warm order is an operator ruling and is not to be retuned casually:** the
spine warms in the foreground at boot, the Reasoner on a background thread,
the coder stays lazy. One context size per model -- the largest any of its
seats declares (8192 for most; Manjuel's gemma4:12b runs at 16384 since
2026-09-07, because at 8192 the ruling never got a token; the Router's
qwen3.5:4b, and the Quality Evaluator beside it, at 16384 since 2026-09-29,
because the Router's request -- its prompt and every skill's declaration --
had filled 8192 and left it ten tokens to answer in).

To free VRAM deliberately:

    rack_unload <tag>     refuses a model this ground does not declare —
                          evicting someone else's model charges THEM the
                          reload, and that is not a cost a seat may spend

If a boot feels much slower than usual, check nothing else is holding the
card: `rack_list` marks models this ground never declared.

---

## The index is empty, stale, or missing something

    index ground          in the REPL — sweeps and reindexes

The boot report prints `index  N docs / M passages`. Empty means it has never
been built here; stale counts mean files changed since.

**A file you expect to be searchable is not.** In order of likelihood: it is
outside `index_roots.txt`; it is a suffix the indexer skips; it is refused as
a secret **by name** (see REFUSALS §6); or it is sealed client data (three
tags, REFUSALS §5). The last two are refusals working correctly and are not to
be "fixed".

**`index/.fuse_hidden*` files.** Corpses left by a mount when a file was
deleted while open. Harmless, hidden from Explorer, safe to remove — the index
is rebuildable by design:

    del /A index\.fuse_hidden*

**`Refused: an index build is still running behind an earlier call`.** A
build refused at the 300s skill bound keeps working (Python cannot kill
the thread); a second `index ground` while it runs would write the same
`vectors.db` -- sitting 94's `UNIQUE constraint failed: docs.path`. Wait,
or restart the REPL to end the first. **`rebuild refused: vectors.db is
held open`** is the same fact from the other side: nothing was discarded,
nothing was written.

**Removing a root from `index_roots.txt` (the prune note).** On the next
`index ground`, docs whose root is no longer declared are EVICTED from the
index. If that would evict more than 25% of the corpus (`ORPHAN_CEILING` in
vectors.py) the prune REFUSES and says so; run `index ground rebuild` to start
clean instead. Nothing on disk is touched either way — only the index.

---

## Voice does nothing

Everything voice degrades rather than crashes, so silence is the symptom.

- **No transcription:** whisper.cpp lives in `bin/`. Nothing is downloaded at
  runtime, ever (RULE 4) — if the build is missing, put it back; do not let
  anything fetch it.
- **No sound out:** SAPI voices are per-seat (`Voice:` in `agents/*.md`,
  matched as a substring). A name that matches nothing falls back silently.
- **It talks over you / will not stop:** any keypress cuts speech off. Long
  deliveries are capped and say so.

---

## A stroke is red

**Don't scroll the output.** Both suites write `tests/last_run.md`: each
suite's standing, then every failure with its detail, and nothing about the
ones that passed. That file is the whole conversation — open it, or hand it
over as-is.

Then read the failing line — it names what broke, in its own words. Then:

1. **Is it a real regression, or a superseded ruling?** A stroke that a new
   rule invalidates is evidence the rule bites. House discipline: **rewrite
   the stroke, note why, keep the guard** — never relax it. Several have moved
   that way (the traversal stroke, the Router's token cap, the tool-loop cap,
   the client-world fixtures).
2. **Fix at the cheapest layer that holds:** alias/gate in `intent.py` >
   skill output wording > prompt > model size. Model size is last and is the
   operator's call.
3. **Run both suites.** The smoke suite sat RED for days once while the
   strokes stayed green, because a fixture had not moved with the code:

       python tests/test_manjuel.py && python tests/smoke_cli.py

---

## Auditing the record itself

    python tests/audit_record.py       reads logs/, SEAT_LOG, sessions, memory

Not a test suite and it never gates anything — the corpus grows every
sitting, so a red over it would mean *you ran the CLI*, not that code broke.
It reports: malformed transcripts, dangling references, orphan prompt files,
unstamped memory, anything sealed that is not protected, and — the useful
part — every run in the record whose shape a gate now refuses (a delivery
claiming all-clear over a failed tool, a file's contents claimed with no
read, a citation the search never returned). Findings land in
`tests/last_audit.md` with their paths.

Run it after a stretch of sittings, or when you want to know whether a
guard you just built would have caught anything historically.

## A seat, or a turn, ran out of time

    [Jesster] seat call ran past the 600s bound (611s) and the run has
    stopped waiting for it ...
    OUT OF TIME. 2 seats did not sit this run because the turn's 600s
    deadline had passed: ...

Two bounds, both the operator's (2026-09-08; ruled again 2026-09-28: "180
for steward. 300 to route and 600 max per seat other than the court which
requires a max of 900"): ONE CALL to a seat may take at most its own
`Timeout:` (agents/*.md -- the Steward 180, the other llama3.2 seats 150,
phi4-mini 300, qwen3.5:4b 300, the 7-12b seats 600), and a seat that
declares none takes the ceiling `MANJUEL_SEAT_TIMEOUT` (600); ONE TURN may
take at most `MANJUEL_TURN_DEADLINE` (600), or what its pipeline declares for
itself in pipelines.md (`court` declares `**Deadline:** 900`) -- a seat whose
turn comes after that is not seated and is NAMED in the delivery, and a seat
seated just before it is cut to what is left. The refusal and the OUT OF TIME
block each name the dial that would move THAT seat or THAT turn: the seat's
own `Timeout:`, the ceiling, or the turn's deadline when the bound was what
the turn had left. Both are dials, neither is a fault: the seat that
hung is the fault, and its name is in the record. Raise the dial only for
a run that legitimately needs it (a parity sweep is many runs, each with
its own deadline; it needs nothing raised).

## A reply was cut short by the rack

    Router's reply was CUT by the rack: its window was FULL -- the prompt
    took 8182 of 8192 tokens and left 10 for the answer. Raise `Context:`
    in its seat file, or send it less

The rack ends every call by saying why it stopped, and `length` means the
rack stopped the model: the seat's window was full, or its `Max Tokens:` was
spent. The engine reads that off the rack (2026-09-29) and the note says
which. It is in the transcript, in the delivery's notes, in the sitting's
ledger line, and under GUARDS FIRED in the standup's report. A seat that
holds tools is sent every skill's declaration, so ITS window fills as skills
are added: `test_a_seat_that_holds_tools_has_room_to_answer` reds before the
rack does. Seats that share a model share a window (one context size per
model). A seat cut by the CLOCK is a different refusal, above.

---

## The dials, in one place

Every `MANJUEL_*` the code reads, with its default. Set in `.env` (the
boot report says which took effect) or the shell. Nothing else is a dial.

    MANJUEL_SEAT_TIMEOUT    600    the most a seat that declares no `Timeout:` may
                                   take, and the most any seat may declare (runtime.py)
    MANJUEL_TURN_DEADLINE   600    the most one turn may take, unless its pipeline
                                   declares its own `**Deadline:**` in pipelines.md --
                                   the court's 900 (pipeline.py, registry.py)
    MANJUEL_SKILL_TIMEOUT   300    the most one skill call is waited for (skills.py)
    MANJUEL_RUN_TIMEOUT     60     the most a `run_python` child may take before it
                                   is KILLED -- a real kill, not a wait (skills.py)
    MANJUEL_GIT_REMOTE      off    1 allows pull/push/rack_pull (gitstate.py)
    MANJUEL_RACK_PULL       off    1 allows `ollama pull` from a seat (skills.py)
    MANJUEL_KEEP_ALIVE      30m    how long Ollama holds a model after a call (runtime.py)
    MANJUEL_NO_WARM         off    1 skips warming the spine at boot (cli.py)
    MANJUEL_VRAM_GB         card   the budget the VRAM plan reasons against (vram.py)
    MANJUEL_LOG_HORIZON_DAYS 45    transcripts older than this leave retrieval; 0 = never (vectors.py)
    MANJUEL_NO_COLOR        off    1 turns the ink off (ink.py)
    MANJUEL_WHISPER_MODEL / _DIR / _CLI / _GGML   where speech-in looks (voice.py)
    MANJUEL_MCP_<NAME>      --     a LOCAL MCP server, callable as <NAME> by the
                                   `mcp_call` skill. Loopback only; anything else
                                   is refused by name and nothing is sent (skills.py)
    MANJUEL_ROUTE_ANTHROPIC_KEY  --  the key of the hosted route in us/route_anthropic.us (a later
                                   route's is MANJUEL_ROUTE_<NAME>_KEY). OFF without it: nothing is
                                   sent. With it, only `/parity hosted` uses the route, and it says
                                   what leaves and asks first (routes.py)

THREE NAMES THAT ARE NOT DIALS, struck from `.env.example` on 2026-09-29.
`MANJUEL_OLLAMA_HOST` was read nowhere -- the runtime binds 127.0.0.1:11434
(runtime.py), and RULE 4 keeps the rack on this machine. `MANJUEL_SPEAK_VOICE`
and `MANJUEL_SPEAK_FILE` are the names voice.py hands its OWN child process,
written over on every call; setting them did nothing. A stroke holds the
example to the code now: a dial it offers is one the code reads.

---

## A hosted route (2026-10-02)

RULE 4 was amended on the operator's word so that a model may be reached on a hosted route, on terms
that keep the rest of it whole. One route exists, `anthropic`, declared in `us/route_anthropic.us`.

    TO TURN IT ON   put MANJUEL_ROUTE_ANTHROPIC_KEY=<the key> in .env yourself, as a line of its
                    own, and restart. A hand never places a key, and nothing prints it.
    TO USE IT       `/parity hosted` in the REPL. It lists the cases, says exactly what will leave
                    this machine (the objective and feed of each, to the host named, and nothing
                    else), says the provider bills it, and asks. `/parity` alone never uses it.
    TO TURN IT OFF  take the line out of .env and restart. Without the key nothing is sent.
    WHAT IT WILL NOT DO   no seat sits on it; it refuses text the law would refuse as an
                    objective, the client tag and the value of any secret in the environment, by
                    name and without sending; a route on another machine must be https; a
                    redirect is never followed; one call, no retry, a time limit.

The model each hosted case names is what the route is asked for. If the provider refuses it (a model
your key does not reach, or one that was retired), the case reports the status and the kind of
error, and the run goes on; change the `**Model:**` line in parity.md to one the route serves.

---

## The hands ledger is gone (2026-09-09)

refusal over an open hand were removed at the operator's word: "we didnt
have it 3 days ago". It cost a ritual at both ends of every stretch of work
and bought a line nobody read.

The file itself STAYS on disk, unwritten -- LAW 1, nothing in the record is
deleted. `law/SITTING_LAWS_2.md` still carries SITTING LAW 6, whose second
half tells a hand to open a line that no longer exists; striking it is the
operator's act, not a hand's. He struck it 2026-09-21: SITTING LAW 6 stands
in `law/LAW_LEDGER.md` without that half, sealed the same morning, and
`SITTING_LAWS_2.md` is left as it stands.

---

## Where the ground stands

    python tests\status.py            writes STATUS.md at the root
    python tests\status.py --print    prints it; --no-gate leaves the gate's lines out

One page, printed from the record (2026-09-29): the marks and how far main stands
past them, the suites' stamp against the newest edit, the release gate's own
lines, SPEC section 4's OPEN lines, TASKS' open boxes, the surface, the ledger
and the day's entries, the pins. Nothing on it is typed by a hand; a count you
cannot find on disk is a bug in the page. Print it after the fold and before a
tag: the gate refuses a page older than the record it reads.

---

## Before a tag: the release gate

    python tests\release.py --check 0.1.11

One command, run ON YOUR TERMINAL before every tag, that refuses by name:
the suites green and stamped after the newest edit; buildmap clean; the
standup run LIVE and green after the newest edit; the law proves; the
manifest agrees with the disk; every SPEC section-4 line whose status
changed since the last tag has an Unreleased CHANGELOG line naming it;
DAYBOOK's last entry closed; a HANDOFF block for today; STATUS.md printed after
the record moved. It reads; it never writes. A REFUSED line is the
thing to do next, not a thing to argue with. PASSED means the tag may be
cut -- by you (RULE 6).

**AND THE MARK ITSELF (2026-09-17).** One mark per version,
`vMAJOR.MINOR.PATCH`, cut on the main line after the gate and sent BY NAME
from the GitHub tab -- never `git push --tags`, which sends every mark this
machine holds. Land the main line on GitHub first -- since 2026-10-09 only
through a pull request merged there once its checks have passed, which the
release flow (v5) does for a cut and for its record: the door refuses to send a
mark whose commit origin's main line does not already carry, and refuses to cut
one anywhere but the main line. The panel asks the door before it offers anything,
so a mark that may not go is greyed with the reason under it rather than after
the click. The seven steps are in BUILDPATH, "The marks, and how one is cut".

---

## The boot report says STALE

    proved   NNN/NNN strokes, NN/NN smoke   3h ago   ** STALE: the ground
                                                        changed since **

The suites last ran *before* the current code. The number is honest about the
past and says nothing about now. Re-run them. This is the report doing its
job, not an error.

`not run here yet` means no run has ever stamped `tests/last_run.json` on this
machine — the same instruction applies.

**If you saw this after EVERY green run, that was a bug, and it is fixed.**
Until 2026-09-10 the check took the newest `.py`/`.md` under `manjuel`,
`agents`, `skills` and `tests` with no exclusions — and `tests/last_run.md` is
a `.md` under `tests/` that the suite itself writes as it finishes. So the
ground always looked "changed since" the moment a run ended, and the line fired
every time. Measured: boot's newest edit was `tests/last_run.md` at 0.0s after
the run, while the release gate read the same tree as 86 seconds *older*.

The suites' own stamps (`last_run.md`, `last_run.json`, `run_history.jsonl`,
`last_audit.md`) are now excluded, which is the rule `tests/release.py` already
used. A stroke proves both copies agree, so they cannot separate again. **A
STALE line now means what it says.**

---

## A world will not answer

Worlds are addressed directly (`@name`) and are private by design: a direct
address is a closed-door visit, recorded in the transcript, never fed into the
conversation other seats read. If a world's seat has no `Wakes On:` line, it
will *never* be summoned by a flag — that is deliberate, not a fault.

Client data inside a world is sealed and stays sealed (REFUSALS §5). An empty
search result over sealed material is the correct answer, not a bug.
