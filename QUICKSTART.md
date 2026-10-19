# Quickstart

**THE BOOK, PART II: THE FIRST HOUR.** Part I (README.md) says what this is.
This part takes a fresh machine to a first job done by Steward in the glass,
in order. The exact build and start commands are Part III's (RUNBOOK.md,
"Starting the system") and are not copied here; this part says when to run
them. The REPL, for when the glass is down, is at the end.

## You need

- **Ollama** running locally (`ollama serve`; usually already a service).
- **Models for the seats you will use — YOURS TO CHOOSE, not a shopping list.**
  Nothing here requires a particular model. Every seat names its own tag in
  `agents/*.md`, and you may point them wherever you like: seven different
  models, or ONE small model in all seven slots. Boot refuses only when a seat
  names a tag you do not have, and it says which.

  So the floor is **one pull per DISTINCT tag named in `agents/*.md`, plus an
  embedder** — three or four gigabytes if you point the seats at one small
  model, thirty-seven if you copy the set below verbatim.

  **THE SHAPE IS WHAT MATTERS; THE TAGS ARE JUST HIS.** What the roster is
  really asking for is a size per JOB, and you fill the slots:

      the door        SMALL and fast. It greets, and it closes the turn. It is
                      spoken to on every single run, so latency here is the
                      whole feel of the thing.
      the router      A STEP UP, and it must think. This is the seat that reads
                      the shortlist and decides which tool runs; a model too
                      small stalls mid-deliberation and calls nothing.
      a coder         Whatever you actually code in. Slotted, not required --
                      drop the seat and the requirement goes with it.
      an overwatch    The long thinker that rules, refutes or reviews. It never
                      sits at the door, so it may be slow.
      the embedder    Small, and the ONE tag you cannot improvise: change it
                      and every vector already built means nothing.

  Add seats, remove them, point three of them at the same tag. The set below is
  the AUTHOR'S, tuned on his own machine over weeks, and it is an illustration
  of that shape rather than a bill of materials:

      ollama pull llama3.2                 # the Steward (front door), Neiro, Guardian, Morning Reviewer, Quartermaster
      ollama pull qwen3.5:4b               # the Router (thinking, tools), Quality Evaluator
      ollama pull phi4-mini                # Proofreader, Delivery Agent
      ollama pull qwen3.5:9b               # Reasoner, Deep Researcher
      ollama pull deepseek-r1:8b           # Jesster (the licensed fool)
      ollama pull gemma4:12b               # the Judge -- the court's ruling seat (thinks long; never at the door)
      ollama pull qwen2.5-coder:14b        # the Expert Coder and the lint skill (14b since 2026-09-30, B1)
      ollama pull nomic-embed-text-v2-moe  # index, drift, parity

  Parity references, optional: `gemma4:e4b`, `qwen2.5-coder:7b`, `qwen3-vl:8b`.
  **What each seat declares in `agents/*.md` is the truth; this list is not.**
  Change a seat's `Model Target:` and the requirement changes with it.

  **`OLLAMA_MODELS`** decides where the weights land. Unset, Ollama uses its
  default under your user profile. The author points it at another disk; if you
  do too, set it before pulling or the files go somewhere you did not mean.

  Boot refuses to start if a seat or skill names a tag you do not have, and
  says which. **The embedder is the exception**: nothing in `agents/` or
  `skills/` names it, so a wrong `EMBED_MODEL` boots clean and fails later
  at `index ground`. Changing it invalidates the index — rebuild with
  `index ground`, since each embedder's vectors mean nothing to another's.
- **Python 3.10+**. One dependency, and it is the only one:

      pip install ".[test]"     # from a clone. `ollama` runs it; `numpy`
                               # PROVES it -- tests/test_manjuel.py imports
                               # numpy outright, so plain `pip install .`
                               # succeeds and then dies mid-suite.

  That puts a `manjuel` command on PATH. `python manjuel.py` from the clone
  still works and is what the record's examples use.
- For voice only: `pip install sounddevice numpy`. Transcription looks for a
  compiled **whisper.cpp** binary with a `ggml-*.bin` beside it, and falls back
  to **faster-whisper** from a local HuggingFace cache.

  **NEITHER IS IN A CLONE.** `bin/` is gitignored — 144 MB of binaries and
  weights is not source and does not go in the record — and the HuggingFace
  cache lives in your user profile, not here. This file used to say the build
  was "already there, nothing to download", which was true only on the machine
  that built it. On a fresh clone, speaking works (Windows SAPI) and LISTENING
  does not until you supply one of the two. The boot report's VOICE line names
  which one it found, or says so plainly.

## What a fresh clone does NOT have, and why the first boot looks alarming

Everything below is deliberate. The record is untracked (his ruling
2026-09-08) and the binaries are not source, so a clone carries the CODE and
the DOCTRINE and nothing that was earned on someone else's machine.

    bin/              the whisper build. Listening is off until you supply one.
    index/            empty. `index ground` builds it; nothing works by meaning
                      until it does.
    logs/             no transcripts. Yours start at your first turn.
    sessions/         no sittings. Your first boot is sitting 1.
    agent_workspace/  made on demand.
    .env              copy `.env.example` and fill it in by hand. Without
                      `MANJUEL_GIT_REMOTE` the REPL's `/git` and the door's own
                      git tools will not send; `/drive ship` does not read
                      that wall (his cards are its gate; README.md, "The rules").
    atlas/            not in this repository. Clone it into the ground:
                      `git clone https://github.com/thebrotherscarr-bit/Atlas.git atlas`

**Your first boot will show a RED GATE, and that is correct.** It reads
something like `gate 3/6 -- REFUSED: strokes, smoke, standup`. Nothing is
broken: the gate refuses to call a thing proven that YOU have not proven. Run
them and it goes quiet:

    python tests/test_manjuel.py     the strokes
    python tests/smoke_cli.py        the REPL
    python tests/standup.py          the live set (needs the rack)

**The first brief you see is the AUTHOR'S, not yours.** DAYBOOK, HANDOFF and
TASKS are tracked — they are the intent of the work, and losing them would
leave a stranger with code and no reason for any of it. So your first sitting
opens with his last session, his open tasks, and a version note that predates
your clone. Read it as history. It becomes yours as you write into it.

**A suite tally may ship with the clone too.** `tests/last_run.json` is
tracked, so the boot report can quote numbers earned on the author's machine
and then mark them STALE against your files. Treat any tally you did not run
as hearsay — the estate's own rule is that a proof older than the code is not
a proof.

## The first hour, at the glass

**1. The glass's own needs.** Beyond Python and Ollama above: Go 1.26, Rust
and cargo, Git for Windows, PowerShell 7, the GitHub CLI `gh` (run `gh auth
login` once, by hand; `/drive ship` and the GitHub tab use it), and, for the
Aider tab, Aider in `aider/venv`. README.md, "Install", is the one list.

**2. Build the door and the glass**, once, and again after any change to
atlas's Go code or its page: RUNBOOK.md, "Starting the system", the three build
lines. The page is built into the glass's binary, so a changed page does
nothing until the glass is rebuilt and restarted, and placing a newly built
binary is the operator's own act.

**3. Start the stack, in this order:** Ollama (usually already a service), then
the door on 127.0.0.1:8090 with `--auth` (without it nothing can be held for
his card, and the glass is refused its own tools), then the glass on
127.0.0.1:8091, started from `atlas\webapp` (its data paths are relative to
it). Both read the same `ATLAS_SERVICE` wire from the environment of the shell
that starts them, never from a command line. RUNBOOK.md has each line. Nothing
starts by itself after a reboot, and nothing opens a sitting by itself.

**4. Open http://127.0.0.1:8091.** The first time, it asks for a name and a
PIN of four to eight digits, and remembers them (hashed) in
`atlas\webapp\data\user.json`; after that, the PIN. Five wrong PINs in a row
lock it for a minute. Forgot it: delete that file and reload.

**5. The front page** is one terminal and an Inspector. The terminal's tabs:
**Agent** (the engine: Steward and the council), **Bash** (Git Bash, as you;
a plain look runs at once, anything that writes asks first), **Python** (one
session that keeps its names), **PowerShell** (every line asks first), and
**Aider** (edits the files you name, on a line of work). Cards -- the
questions and the Approve/Deny asks -- sit in the dock at the foot of the
terminal in every tab. The bar at the top says whether the door answers,
whether an engine is open, and how many models the rack holds.

**6. Boot.** In the Agent tab, press Boot in the title (or type `/boot`). The
door opens the engine on this ground (about half a minute), warms the models
and prints the boot report: GROUND, RACK, RECORD, GATE, VOICE. The title then
says "sitting N". A first boot shows a red GATE (below); that is correct.

**7. A first look.** In the Bash tab type `git log --oneline -5`: it runs at
once and says "read". Type `touch x.txt` and it does not run: a card says "This
asks first" with Approve and Deny. Deny it. That is the gate, and it is the
same for every write in this system.

**8. A first door call.** In the Agent tab type
`mcp_call atlas git {}` -- the door's read of the repository, answered in one
line, no model asked. Type `mcp_call atlas suite_run {"set":"smoke"}` and the
door runs the smoke suite and the engine reads the tally back.

**9. A first job for Steward.** In the Agent tab, a job and the check that
decides it is done, for example:

    /drive Add a one-line docstring to enabled() in manjuel/ink.py | check: suites

What happens, in order: Steward reads what it needs (no card for a read); the
first write it wants comes as a red card -- "The Steward wants to run
ground_edit ... Approve? [y/n]" -- and on your yes it first opens a line of
work `drive-MMDD-HHMMSS` (main is never written); when it says it is done, the
CHECK runs, and only a passing check ends the job. Then one card offers to
commit, push, open a pull request and wait on CI; another, once CI is green,
to merge it on GitHub and delete the branch; then the ground goes back to main
and catches up. Finally a green card: "What is next?" -- type the next job, or
leave it blank to stop. Every `[y/n]` card is two buttons, Approve and Deny.

A job with no check runs and ends UNCHECKED, its change left unsaved;
`plan` and `each` refuse to run without one. RUNBOOK.md, "Steward drives",
has every mode.

**10. Close.** Type `/close` (or Close in the title). The engine writes the
sitting's close and pays the toll if a turn ran. An engine left idle closes
itself after 30 minutes; the title warns from 5. Lock the page with the icon by
your name.

## Without the glass: the REPL

    cd Desktop\Research
    python manjuel.py
    python manjuel.py --headless     # the same sitting as JSON lines on stdin/stdout
    python manjuel.py --ground worlds\NAME   # either, sitting inside a world (its own record)

Boot prints the report: GROUND, RACK (with real sizes and what is warm),
RECORD, GATE, VOICE. If a needed model is missing it says which and stops.
`/drive` and `mcp_call` lines do not exist in the REPL; everything else below
works in both.

### First five minutes

    what can you do            → the skill table, read from the harness
    what is in this repo       → the ground, live from disk
    git status                 → routed deterministically, no model guessing
    what ran yesterday         → the record for a period, from the stamps
    review sitting 47          → a sitting number resolved to its runs
    /chat                      → talk; it answers aloud; any key cuts it off
    /help                      → everything else, grouped

A period and a sitting are different questions: `when` reads a stretch of
clock, `sitting` reads a unit of work you declared by opening the REPL.

Paste material with `/paste` (the Guardian gates it before any seat reads
it). Land a ruling with `/remember`, or just say `remember that` -- the last
proposal or the last answer is shown back, you give it a kind, one y. Drop
outside files in `agent_workspace/` and say `inspect <name>` before anything
reads them. `/brief` says where the build is and what you said we are on.
Pay the sitting's toll with `/toll`.

## The two tests

    python tests/test_manjuel.py    # the strokes; no model needed
    python tests/smoke_cli.py        # drives the REPL end to end

Each prints its own tally when it finishes. That tally is the only honest
one — the suites grow with the system, so no count is written into a doc.

Both offline; the smoke takes about a minute and the strokes a few. Run them
after any edit to agents/, skills/ or manjuel/. Red blocks; the failing stroke
names what broke. Under SITTING LAW 11 they are run by Steward from the glass
-- as a job's check, or `mcp_call atlas suite_run {"set":"both"}` -- and the
lines above are what those run.

## Extending

- **New seat:** one file in `agents/` — model, `Wakes On:` flag, `Wakes:`
  anchor, prompt. `/reload`.
- **New tool:** one file in `skills/` — keyword, description, params. A
  `Model Target:` line makes it a prompt skill needing no Python; otherwise
  bind a handler in `manjuel/skills.py`. Startup refuses a manifest that
  advertises what cannot execute. A skill can also declare how it is
  reached and what it takes, so neither has to be carved into the engine:

      - **Says:** index, reindex, run the index
      - **Takes:** rebuild | from scratch -> content
- **New pipeline:** a block in `pipelines.md`. `/use <name>`.
- **New command:** a block in `commands.md` — `**Runs:**` is the objective
  (with `$ARGS` where what you type after the command belongs), and an
  optional `**Method:**` line makes everything after it a procedure that
  rides with the run and is shown to every seat. `/reload`. (Today a
  command runs in the REPL only: in the glass the engine stores what it would
  run and never runs it.)

## When the machine misbehaves

`RUNBOOK.md` — the rack unreachable, a stuck git lock, a full card, a stale
index, voice gone quiet, a red stroke. `REFUSALS.md` explains anything the
estate refused on purpose, and why.

## When a seat misbehaves

Every run is transcribed in `logs/` with per-stage timings, prompts kept
apart in `logs/_prompts/`; every Steward job is `logs/<stamp>_drive.md`, each
tool call and its whole result in order. Read the transcript before blaming a
seat — the record outranks any model's account of itself, including Manjuel's
own.
