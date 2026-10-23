# Manjuel

**THE BOOK OF THIS SYSTEM, PART I: WHAT IT IS.** Four files, read top to bottom,
are one book:

    Part I    README.md       what it is, how it was made, how it is built (this file)
    Part II   QUICKSTART.md   the first hour: install, start, the first job
    Part III  RUNBOOK.md      driving it every day, and keeping it running
    Part IV   INVENTORY.md    every part, one line each, then every part in full

Two appendices are generated from the code and never written by hand:
`BUILDMAP.md` (every function, by file and line; `python tests/buildmap.py`)
and `REFUSALS.md` (every refusal and the failure that earned it;
`python tests/refusals.py`). The law is in `law/`, the vision in `foundation/`,
and the history in `DAYBOOK.md` and `CHANGELOG.md`.

## What it is, in his words

"we built the recorder, its perfect, now we build the harness on top of it"
(SYSTEM_DESIGN.md). The harness is "a single simple driver that runs long
workflows and tool chains to make sure that basically whatever I ask can be
done. Fairly simple." The product, in SPEC's words, is a harness that makes
small local models SAFE TO USE and HONEST ABOUT THEMSELVES; in his, "a second
brain, a wholly agentic system that essentially runs all of my digital life",
and "an autonomous vibe-coding machine with all of the transparency we need set
on a local rack of models". The law exists "to firewall the agents from wrecking
things before they are ready". The bar for done is the wife test: "if my wife
can sit down at the PC, ask the system to make a type of software, game, etc.
and she can see the result" (SPEC 4.8).

Everything runs on this machine: no cloud service, no API key, no download at
runtime. Unplug the router and it still works -- that property is the point.
(One optional exception, off by default: a hosted model route for a parity
measurement run by name; RULE 4, amended 2026-10-02.)

## The four programs

| Program | What it is | Where it listens | Where it lives |
|---|---|---|---|
| **Ollama** | the rack: every local model the seats and the driver ask | 127.0.0.1:11434 | an installed service |
| **the door** (`atlas-mcp.exe`) | the tool server: every tool, the hold queue (his Approve cards), the shell gate, and the host of the engine | 127.0.0.1:8090 | `atlas/line/` (Go) |
| **the glass** (`atlas-webapp.exe`; Aurora in the doctrine) | the web page he works in: one terminal (Agent, Bash, Python, PowerShell, Aider tabs), the dock of cards, the Inspector; this PC only, opened with a PIN | 127.0.0.1:8091 | `atlas/webapp/` (Go, the page embedded) |
| **the engine** (Manjuel) | the council and the driver, in Python; the door starts one per world as a child process and speaks to it in JSON lines on its stdin and stdout | no port | `manjuel/` |

`atlas/` is a SEPARATE repository, cloned into this ground as `atlas`. Cloning
this repository alone gives the engine and no glass:

    core    https://github.com/thebrotherscarr-bit/Manjuel.git
    atlas   https://github.com/thebrotherscarr-bit/Atlas.git

## How it is driven: SITTING LAW 11

His words, 2026-10-16: "the system function and parity, tests and provers,
pipelines and workflows, EVERYTHING is to be run by Steward. EVERYTHING is to go
through the webapp." (`law/LAW_LEDGER.md`, entry 11; a draft below the seal
until he seals it on the Laws page.) So the operator types into the glass, and
three kinds of line do three different things:

1. **`/drive <job> | check: <command>` -- Steward drives.** The driver
   (`manjuel/serve.py`, the `/drive` section; model `qwen3.5:9b`) works the job
   through the engine's tools, one call at a time, until the CHECK passes --
   never until the model says so. Every write it wants is a red `[y/n]` card in
   the glass, and nothing writes without his Approve. Then it offers to commit,
   push, open a pull request, wait on CI and merge, each on its own card, and
   asks "What is next?". The modes (`plan`, `each`, `tidy`, `ship`) and every
   bound are in RUNBOOK.md, "Steward drives", and INVENTORY.md.
2. **`mcp_call atlas <tool> {json}` -- a door call, said plainly.** No seat
   reads it and no model narrates it: the engine asks the door, says in one
   line what it asked, waits for his click if the door holds the call, and
   says in one line what became of it.
3. **Anything else -- the council.** The seats sit in their running order
   (below), and the Router is the only one that may use tools.

The Steward who drives is not the Steward SEAT. The seat (`agents/steward.md`,
`llama3.2`) opens and closes an ordinary turn; the driver has its own
instructions (`DRIVE_SYSTEM`) and its own model. Both are Steward in the
doctrine: the intake that acts, with the operator holding the gate.

## How a typed line travels

1. The glass's Agent tab opens `GET /api/council/stream?objective=<line>`.
2. The glass passes it to the door's `/run/stream`; the door writes
   `{"cmd":"objective","text":<line>}` to the engine's stdin.
3. The engine (`Door.turn`, `manjuel/serve.py`) routes it, in this order:
   an empty line does nothing; `exit`/`quit` closes the sitting; `/drive` goes
   to the driver; a line leading with `mcp_call` goes to `door_call`; a topic or
   session cue; "pay the toll"; "remember that"; `@<seat>`; a `/command`; the
   rack unreachable is said so; otherwise the pipeline runs.
4. The engine answers in JSON-line events on stdout: `seat`, `token`, `think`,
   `tool`, `tool_result`, `report`, `needs_answer` (a card: the question and its
   colour), and one `delivery` at the end. The door streams them to the glass,
   which draws them; a card's answer goes back as `{"cmd":"answer"}`.
5. The sitting (`sessions/sessions.jsonl`) keeps one row per run, written when
   the sitting closes; the run's transcript goes to `logs/`.

## Install

Everything it needs, in one list. Part II (QUICKSTART.md) walks it in order,
and RUNBOOK.md, "Starting the system", builds and starts the door and the glass.

- **Python 3.10 or later** (CI runs 3.10 and 3.13 on Windows and Ubuntu; this
  machine runs 3.14), then `pip install ".[test]"` -- `ollama` to run, `numpy`
  to PROVE (the strokes import it outright, so a plain `pip install .` installs
  and then crashes the suite). It puts `manjuel` on PATH; `python manjuel.py`
  from a clone works too.
- **Ollama** on 127.0.0.1:11434, with the models `rack.md` declares:
  `llama3.2` (Steward seat, Security Guardian, Neiro, Quartermaster, Morning
  Reviewer), `qwen3.5:4b` (Router, Quality Evaluator), `qwen3.5:9b` (Reasoner,
  Deep Researcher, and THE DRIVER, which `rack.md` does not yet list),
  `phi4-mini` (Proofreader, Delivery Agent, four prompt skills),
  `deepseek-r1:8b` (Jesster), `gemma4:12b` (Judge), `qwen2.5-coder:14b` (Expert
  Coder, `lint_code`, and Aider), and the embedder `nomic-embed-text-v2-moe` (the
  index and the drift checks).
- **For the door and the glass:** Go 1.26 (both `go.mod` files); Rust and
  cargo (the `atlas` spine binary); Git for Windows (its Git Bash IS the Bash
  tab; a plain `bash` on PATH may be the WSL stub, which the door never uses);
  PowerShell 7 (the PowerShell tab); the GitHub CLI `gh`, SIGNED IN (`/drive
  ship` and the GitHub tab open, watch and merge pull requests with it);
  Aider 0.86.2 in a Python 3.10-3.12 venv at `aider/venv` (the Aider tab);
  whisper.cpp in `bin/` and Windows SAPI (voice); Edge or Chrome (the maker's
  page check).
- **`.env`** at the ground's root, never printed, never committed, never
  passed on a command line (RULE 7): the service wire `ATLAS_SERVICE` (the
  door and the glass must hold the same one), the door's address and key for
  the engine (`MANJUEL_MCP_ATLAS`, `MANJUEL_MCP_ATLAS_KEY`), and
  `MANJUEL_GIT_REMOTE`, the wall on sending. `.env.example` names every key;
  RUNBOOK.md's table of the dials says what each one does.

Windows-first: voice (SAPI out, whisper.cpp in) is Windows-bound and DEGRADES
ALONE -- boot reports GROUND / RACK / RECORD / GATE / VOICE separately, so a
machine without it boots, says so, and runs everything else.

The suites are offline and stubbed: no rack, no network, no GPU, no model.
`python tests/test_manjuel.py` (the strokes) and `python tests/smoke_cli.py`
(the smoke) run anywhere, and CI runs them, with the law's prover, the build
map's check and the standup's dry run, on Windows and Ubuntu on every pull
request and every push to main or a mark. Under SITTING LAW 11 they are run BY
STEWARD, through the glass: as a job's check (`/drive <job> | check: suites`
runs the strokes), or as a door call (`mcp_call atlas suite_run
{"set":"both"}`; the engine reads the tally back with its own `proved`). The
live standup -- the seats through nine fixed objectives on the rack, about
ninety seconds -- is `mcp_call atlas standup_run {"set":"morning"}`; it opens a
sitting of its own, so it refuses while one is open.

## How it was made

Every date below is in `DAYBOOK.md` and `CHANGELOG.md`, where each is told in
full.

- **2026-08-29** -- the chain is born, and the first standing rules are written
  after a session that broke them.
- **2026-09-01 to 09-04** -- the hash-chained law ledger; HANDOFF; the guards
  (recompose, claim and citation checks); `worlds/` untracked; pyproject and CI;
  a law gate on every run; only the Router holds tools; SPEC, BUILDMAP and the
  standup written; the first live standup; v0.1.0 to v0.1.4. His order for the
  next session: "RUN IT AND WRITE DOWN WHAT FEELS OFF."
- **2026-09-07 to 09-08** -- `inspect`, "remember that", the brief; seat and
  turn time limits; the release gate; his rhythm: "document build review
  document".
- **2026-09-09 to 09-12** -- the glass and the gate: every act through the
  panel; core and atlas split into two repositories; "the ARCHIVE never goes on
  github, EVER"; `mcp_call`; the coder flow fired for the first time; v0.1.6 to
  v0.1.11 "THE CODING UPDATE".
- **2026-09-14 to 09-23** -- optimisation; engines close after 30 idle
  minutes; the appendable law ledger sealed; the maker (the snake game); the
  glass's PIN lock; the maker's page check; the first lawful loop under LAW_003;
  v0.1.12 to v0.1.14.
- **2026-09-24** -- the diagnosis that turned the work: "a magnificent recording
  instrument with almost no actuators". RULE 11 (name the wire) the same day.
- **2026-09-25 to 10-02** -- the door armed with `--auth` and the hold queue;
  the standup and the suites run from the glass; the coder changes the harness
  end to end; the What's left page; the memory hash chain; the hosted parity
  route; the front page becomes one terminal; v0.1.15, v0.1.16.
- **2026-10-03 to 10-05** -- the Bash and Python tabs, the test pack, Aider
  behind the glass; RULES 12 to 14 and SITTING LAWS 7 to 10 (nothing published or
  signed without his word; everything runs on the glass; the work is done in
  his glass step by step on his approval); the Laws page; v0.2.0 to v0.2.2.
- **2026-10-06 to 10-13** -- everything on the front page; the GitHub tab; main
  protected (a change reaches it only through a pull request whose checks
  passed); v0.2.4, v0.2.5 "full GitHub integration"; INVENTORY measured line by
  line on the glass; the plan by office.
- **2026-10-14** -- the PPMI reader, the Judge (the ruling seat renamed), live
  thought on the glass.
- **2026-10-16** -- "if we get the nigel thing right, we dont need to keep
  adding in layer after layer": the harness becomes the plan. Steward drives
  (`/drive`, pull request 28); a door call said plainly (C77, pull request 29);
  SITTING LAW 11 entered as a draft; Steward does C71, the HANDOFF block and its
  own fixes on its own code, every write on his card (pull requests 32, 33).

## The council: what an ordinary turn looks like

Type, or speak (`/chat`). Before any model sees it, arithmetic decides: is
this language at all, does it name a tool ("git status", "who is manjuel"),
is it an *order* to search the ground, a question carrying a term worth
looking up, several acts in one sentence, or just talk. What matches is
dispatched; everything else falls through to conversation. Then the spine
runs:

    Steward  →  Router (when a tool is needed)  →  Steward

Two to four stages for an ordinary exchange. Since 2026-10-12 the Steward up
front answers a plain read itself, a call decided by arithmetic, with no
Router; and when the Reasoner or the Expert Coder answers, its words are the
delivery as written: the closing Steward does not sit to retell them, and the
engine adds what is still open from the record. Specialists rest on the rack and
are summoned by flag: paste untrusted material and the Security Guardian
gates it *first*; ask for code and the Expert Coder wakes, its file landed on
disk by the harness and reviewed; raise something genuinely hard and the
Reasoner (a 9b) takes the knot. A review that finds the work *unfinished*
rather than wrong can send it back through the tools once, carrying the
evidence. The conversation carries across turns, typed and voice sharing one
thread.

Ask it to MAKE something -- "make me a snake game", "build a tip calculator"
-- and none of that spine sits. The engine seats the Expert Coder alone,
checks the one web page it writes (whole, and loading nothing from the
internet), and saves it as version 1 of a project in `projects/`, a folder
with its own history. "Make it faster" is version 2; "go back" puts an
earlier version back as a new one, so nothing is lost. Every time, the answer
is the engine's plain report: what was made, where to open it, what to ask
next. The glass's Run tab (Inspector) lists every project with its versions
and plays its page beside the terminal in a sandboxed frame that reaches
nothing; "work on the snake game" picks one up and "put it down" sets it aside
-- words the engine answers itself, no seat sitting. SPEC 4.8 is what it does
and does not do yet.

The running orders are in `pipelines.md`; `default` is the one above. The
others: `court` (Security Guardian, Router when a tool is needed, Neiro,
Jesster, the Judge rules; read-only, a 900 s deadline; `/table <q>` seats it
for one question), `estate` (Security Guardian, Steward, Neiro, Jesster, Judge;
read-only and no tools), `brief` (for a pasted feed: Security Guardian,
Morning Reviewer, Delivery Agent) and `quick` (Security Guardian, Steward).
`/use <name>` switches. Fourteen seats are declared in `agents/`, one file
each; who wakes, on which flag, with which model, and how long each takes on
this machine is INVENTORY.md's.

Each seat is told the date and hour, so "written 2h ago" means something. A
file too big for any window arrives as part 1 of N with its own headings
mapped, and the seat can ask for the part it needs — because chaining cannot
widen a window, only cover more ground with each one.

## The rules the build enforces

- **Testimony is never fact.** Seat output cannot forge the record, the
  closer may only report work it can point to, search results declare their
  age and tense.
- **Facts are read, not generated.** Where am I, what can you do, what is on
  the card — answered by the harness from ground truth, never by a model.
- **Keys are silent.** `.env` is never printed, indexed, or passed on a
  command line. Secret-shaped files are refused by name.
- **The gate is his.** Every write Steward wants waits on a red `[y/n]`
  card, and runs only on his Approve; a writing call to the door from
  anything but his glass is held in the door's queue until he answers its
  card; a commit, a push and a merge are each a card of their own; a memory is
  landed only by him (`/memory`). His glass itself runs what he presses.
- **Where the gate stands today, read off the code (2026-10-16).** A job's
  `| check:` command runs with no card -- it is his own words, run as typed. A
  `/drive` job and a `mcp_call` line do not pass the pipeline's law gate, and
  the driver's sends (`git push`, `gh pr`) do not read `MANJUEL_GIT_REMOTE`:
  his cards are their gate. RUNBOOK.md, "Steward drives", says the same.
- **The ground is this folder.** Nothing reaches outside `Research`, and a
  test fails if anything tries.
- **A claim needs something behind it.** A seat that presents a file's
  contents with no read, or cites a search result the search never
  returned, is refused at the gate and the fault is named in the record.
- **Client data is sealed.** A `vault/` path, a `.client.` name or a
  `[[CLIENT]]` token — any one of the three, and the file is refused by
  the index, the watcher, every reader and every listing.

## The ground

`C:\Users\novad\Desktop\Research`, and nothing outside it (RULE 1). What git
tracks in this repository:

    manjuel.py     the entry point: `python manjuel.py` (the REPL),
                   `--headless` (JSON lines on stdin/stdout, how the door runs it),
                   `--ground <folder>` (sit inside another world)
    manjuel/       the engine, one module per job (each named below)
    agents/        one seat per file: model, clearances, wake condition, prompt
    skills/        one engine tool per file: keyword, model, description,
                   parameters, the phrases that name it
    pipelines.md   the running orders
    commands.md    the engine's own shortcut commands (`/morning`, `/sitting`,
                   `/covenant`; they run in the REPL only today)
    rack.md        the models, generated by `rack_sync` from what Ollama holds
    us/            the capability records: one `.us` per seat and route, and
                   `manjuel.us`, one record per skill (what it may touch)
    law/           THE LAW: the law files, the hash-chained ledger
                   `law/chain.jsonl`, and its prover (`python law/law.py verify`)
    foundation/    the vision: the founding papers and the doctrine, read-only
    prompts/       the engine's prompt records
    tests/         the strokes (`test_manjuel.py`), the smoke (`smoke_cli.py`),
                   the live standup, the release gate (`release.py`), the cut
                   (`cut.py`), the generators (`buildmap.py`, `refusals.py`,
                   `status.py`, `seatindex.py`), the test pack (`pack.py`), and
                   the proof stamps the suites write (`tests/last_run.json`,
                   `tests/last_run.md`, `tests/run_history.jsonl`)
    .github/       CI: `prove.yml` (the suites on every pull request and push)
                   and `release-gate.yml` (the gate on a mark)
    index_roots.txt  the folders and files the semantic index embeds
    pyproject.toml, LICENSE, .gitattributes, .gitignore, .env.example
    the root .md   this book (README, QUICKSTART, RUNBOOK, INVENTORY), SPEC
                   (what it IS and when it is DONE), SYSTEM_DESIGN, DESIGN,
                   BUILDPATH, TESTING, STATUS, WHATS_LEFT (everything
                   open, numbered; the glass's What's left tab reads it), TASKS
                   (his list, only what he put there), CHANGELOG, DAYBOOK,
                   HANDOFF, REFUSALS, BUILDMAP, agents.md, parity.md, CLAUDE.md
                   (the standing rules for any hand)

On disk and kept out of git (the `.gitignore` says why for each):

    atlas/         the door and the glass: its own repository
    .env           the keys
    worlds/        the estate's other worlds; never indexed, never read, never sent
    projects/      what the maker made: one folder per project, each its own
                   git repository
    sessions/      the sitting ledger and the conversation thread
    logs/          every run's transcript, every drive's record
    state/         the door's records for this world (the hold log first)
    flows/         the workflow specs, their versions, and every run's record
    memory.md, memory/   what he landed, its hash chain, what waits for him
    SEAT_LOG.md, SEAT_LOG_INDEX.md   the tolls
    index/         the semantic index (`index/vectors.db`)
    agent_workspace/   the seats' scratch folder
    aider/         Aider's venv and its runs
    bin/           whisper.cpp

Extending it is writing markdown: a new seat is one file in `agents/`, a new
tool one file in `skills/`, a new pipeline a block in `pipelines.md`. The
engine changes for none of these.

## The record: every file the system writes, and its shape

| File | Who writes it, when | One row or line |
|---|---|---|
| `sessions/sessions.jsonl` | the engine (`manjuel/seatlog.py`): a row when a sitting opens, the whole row again when it closes | `n, id, started, ground, git_start, runs[], ended, git_end, toll_paid, pid, closed_by`; each run `objective, pipeline, stages, failed, elapsed, transcript, tools[], guards[], seats_failed[], out_of_time[], delivery`. While a sitting is open its `ended` is `""`. |
| `logs/<YYYY-MM-DD_HHMMSS>_<slug>.md` | the engine, after every council run (`manjuel/transcript.py`); its prompts kept apart in `logs/_prompts` | each stage: the seat, `<elapsed>s · skills: … · drift …`, its words |
| `logs/<YYYY-MM-DD_HHMMSS>_drive.md` | the driver, when a job ends (`drive_record`) | a head (`# drive -- <goal>`, `- check:`, `- model:`, `- verdict:`, `- elapsed:`), then `## <n>. <tool>`, `args: …`, and the whole result indented four spaces |
| `logs/drive_ignore.jsonl` | the driver's `each` mode | `ts, task ("each:<sha1>"), item, verdict` |
| `state/holds.jsonl` (and `atlas/state/holds.jsonl`) | the door, before and after every held call and every shell, Aider and law act | `ts, what, id, tool, caller, project, rbac, note`; `what` is `held`, `approved_ran`, `approved_errored`, `denied`, `refused`, `crossed`, `shell_ran`, `shell_held`, `shell_refused`, `aider_ran`, `aider_refused`, `aider_undone`, `law_added`, `law_sealed`, … |
| `tests/last_run.json`, `tests/last_run.md`, `tests/run_history.jsonl` | the suites, and nothing else | per suite `state, passed, total, green, at, failures`; the history one line per run |
| `law/chain.jsonl` | `law/law.py` on his seal | one hash-chained link per sealed law file |
| `memory.md`, `memory/chain.jsonl`, `memory/pending.jsonl` | his `/memory` lands; a seat's `remember` only stages | the landed entry; `LAND by operator -> memory.md range:A-B sha256:H`; the staged proposal |
| `SEAT_LOG.md`, `SEAT_LOG_INDEX.md` | the toll at a sitting's close | `## <date> — sitting <n>`, what proved, what is thin, what is owed |
| `flows/runs.jsonl` | the door's flow runner | `start`, one `node` line per node (`status, pass, latency_ms, output, receipt`), `loop`, `stopped` (the verdict) |
| `index/vectors.db` | `index_ground`, `embed_text` | SQLite: `docs`, `chunks` (text and a float32 vector), `chunks_fts` |
| `atlas/webapp/data/webapp.db/traces.jsonl` | the glass, for every tool call it makes (six background reads excepted) | `id, agent_id, tool, input, output, hash, status, duration_ms, created_at` -- it grows without bound |

Every record is append-only or regenerated whole; a hand never edits a row.
How each one is read back -- `proved`, `sitting`, `when`, the standup, the
boot report -- is in RUNBOOK.md and INVENTORY.md.

## The engine's own commands, and the REPL without the glass

The glass's Agent tab sends every line to the engine, so the commands below
work there too -- except that `/drive` and a `mcp_call` line exist ONLY in the
headless engine the glass runs (`python manjuel.py --headless`), and the
engine's `commands.md` shortcuts and `/listen` run only in the REPL (the glass
stores what they would run and never runs it; RUNBOOK.md says so where it
matters). `python manjuel.py` on its own is the REPL: the same engine in a
terminal, for when the glass is down. `/help` prints the palette. The
commands, so none is only in the code (the REPL read of 2026-09-08 found eleven
that no doc named):

    talking     /chat  /say  /new  /resume  /paste  /table <q>  @<seat> <words>
    the record  /last  /remember  /memory  /git  /toll  /sittings  /brief
    the ground  /status  /index  /find <q>  /parity   (`inspect <name>` is a skill, typed as words)
    the rack    /models  /model <tag>|reset  /warm  /rack
    plumbing    /agents  /skills  /pipeline  /pipelines  /use <name>  /reload  /listen  /exit

`/model <tag>` runs every seat on one model for the sitting -- a
measurement, not a configuration; `rack.md` keeps the declared models.
`/table` seats the counsel on a question and the Judge rules; `@<seat>`
opens one seat alone, its own voice, the shared thread. Typing "remember
that" at the door lands a memory; "pay the toll" pays it.

`python manjuel.py --headless` opens the same sitting over stdin/stdout as
JSON lines (`manjuel/serve.py`): one `objective` per line in -- anything
the prompt takes -- and the turn out as events (`opened`, `run`, `seat`,
`token`, `think`, `tool`, `tool_result`, `report`, `needs_answer`, `delivery`,
`refused`, `aborted`, `cancelled`, `unreachable`, `command`, `closed`, and a
few more; RUNBOOK.md lists every one with its fields). Every question the REPL would ask at the keyboard
comes back as `needs_answer` and waits for an `answer`; nothing is
decided for you. (One turn is not asked: an objective sent with
`"unattended": true` -- a flow's node, where nobody is there to answer --
skips a failed seat marked `On Fail: prompt`, the prompt's own default,
and the record says so.) No socket: a front end runs the process and speaks on
its pipes. The door is that front end (atlas's `docs/SPEC_CONTROL_CENTER.md`
is its design record).

`python manjuel.py --ground worlds\NAME` (with or without `--headless`) sits
the engine inside a world: that folder's own `agents/`, `skills/`,
`pipelines.md`, `law/`, `sessions/` and `logs/`. A sitting opened there is
that world's, and this ground's record gains nothing. A path that is not a
directory is refused, never created.

The skills are `skills/*.md`; `/skills` lists them and
`skill_report` (ask "what can you do") reads them off the disk. The ones
no earlier doc named: `deep_research`, `ground_report`, `skill_report`,
`skill_search`, `list_directory`, `write_file`, `linear_regression`,
`subtask` (a scoped sub-run: depth 1, three per turn, the Router alone),
`edit_file` (one uniquely-anchored passage, not a whole file) and
`run_python` (one jailed script, bounded, blind to `.env`).

## Documents

The book, in reading order: this file; `QUICKSTART.md` (Part II, the first
hour); `RUNBOOK.md` (Part III, driving it and keeping it running);
`INVENTORY.md` (Part IV, every part, one line each and then in full). Then:

- `WHATS_LEFT.md` — everything still open, numbered, and the path we are on
  today (the glass's What's left tab)
- `DAYBOOK.md`    — the session book: what each working session was FOR,
  where it drifted, and the rulings it produced. (The check sequence at its
  top is the 2026-09 terminal one; today's is a job's check, RUNBOOK.md.)
- `REFUSALS.md`   — every gate: what it refuses, and the failure that earned it
- `TESTING.md`    — the tiers, how to run them, and the discipline
- `parity.md`     — what Manjuel is measured against, and how to read a score
- `RUNBOOK.md`    — Part III: starting the system, Steward driving, GitHub,
  the dials and bounds, and when the machine misbehaves
- `BUILDPATH.md`  — every module, what it owns, and the order it was built
- `STATUS.md`     — where the ground stands, printed from the record by `tests/status.py`
- `INVENTORY.md`  — every function of both repositories, its last live run and its time
- `DESIGN.md`     — the architecture record, including what was tried and superseded
- `SYSTEM_DESIGN.md` — the recorder, and the harness built on it (WHAT'S LEFT H31)
- `HANDOFF.md`    — the live operational record: patterns, fix log, rulings
- `CLAUDE.md`     — standing rules for any agent working in this ground
- `LICENSE`       — MIT

Built session by session, with every observed failure pinned by a test
before it was called fixed.
