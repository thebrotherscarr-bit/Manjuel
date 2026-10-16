# SYSTEM_DESIGN — the recorder, and the harness built on it

*Rewritten 2026-10-16 on the operator's word: "Rewrite the system design and launch_plan. Supersede spec 8.2, on my
word"; of the business it once centred on, "That's being left completely out, overwrite, my word approved"; and of the
plan, "This is the plan, we are doing the harness. we built the recorder, its perfect, now we build the harness on top of
it." The design it replaces, "the software side of the NAS" (2026-09-08), stands in git at `36bf8c3`. The goal it serves
is WHAT'S LEFT H31; the order it is built in is atlas's LAUNCH_PLAN.md.*

---

## 0. The one sentence

**The recorder keeps everything that happens on this machine, provably; the harness on top of it lets one driver,
Steward, carry out what the operator asks through tools that cannot act past his card, and stops only when a check says
the job is done.**

One person, one machine, one folder (`Desktop\Research`), a rack of local models. Not a service, not multi-user, not
hosted (SPEC 1).

---

## 1. The recorder — built

The core repository (Manjuel) and the record it keeps. Everything here exists and is held by the suites.

| part | what it keeps | where |
|---|---|---|
| the law | the sealed laws on a hash chain, walked before any model reads a word; a tampered law refuses every run | `law/`, `manjuel/lawgate.py` |
| every run | a transcript per run: each seat's words and every tool call, the prompts kept apart | `logs/`, `manjuel/transcript.py` |
| every sitting | a numbered ledger line, and a toll at close | `sessions/sessions.jsonl`, `SEAT_LOG.md`, `manjuel/seatlog.py` |
| memory | landed by the operator's hand only, sealed on a hash chain beside it | `memory.md`, `manjuel/memory.py` |
| the engine's checks | a claim of a read or a write with nothing behind it refused; a citation the search never returned refused; every failed tool and partial read appended to the answer; a number no tool returned stamped | `manjuel/pipeline.py`, `REFUSALS.md` |
| the door's record | every held call, approval, denial and refusal | `state/holds.jsonl` in each world |
| the proof | the strokes and the smoke offline on every change; the live check on the rack; the release gate before every mark; GitHub on every pull request | `tests/`, `.github/workflows/` |
| the plan | what is open, and where we are working today | `WHATS_LEFT.md` |

The recorder answers "what happened, and can I trust it?" It is finished in the sense the operator means: the record is
whole, sealed where it must be, and nothing a model says outranks it.

---

## 2. What runs around it — built

**The door** (`atlas/line`, atlas-mcp on 127.0.0.1:8090): about 95 tools over MCP. It decides from outside any model, by
who is calling, never by what a model says: a call that writes, from anything but the operator's glass, is held as a
card until he answers it; roles are judged by the transport's identity; a secret, a path outside the ground and client
material are refused by name. It carries the gated shell (Bash, Python and PowerShell), Aider behind its wall,
`file_edit`, git with pull requests, the suites and the live check, and the flow engine (steps, gates, checks and
bounded returns).

**The glass** (`atlas/webapp`, atlas-webapp on 127.0.0.1:8091, Aurora): one terminal with its tabs (Agent, Bash, Python,
PowerShell, Aider), an Inspector beside it, and the dock at its foot where every card waits for his click. Each seat's
thinking streams live and folds when the seat speaks. It opens with his PIN and answers this computer only.

**The engine** (`manjuel.py --headless`, raised by the door for an open world): a council of small seats declared in
markdown (`agents/`), tools as skills (`skills/`), running orders in `pipelines.md`. A request is read by arithmetic
first (the regex layer and the PPMI reader), a model last.

**The rack**: Ollama on 127.0.0.1:11434, the models on disk (`rack.md` is derived from it), one 16 GB card (RX 6800 XT),
one call at a time. rack_unload frees the card of a model this ground declares.

The Rust workspace in atlas (`atlas/core`, `atlas/store`, `atlas/apps/atlas`) stays, by the operator's ruling of
2026-10-02 (B14): the door no longer calls it; atlas-door does, and every release ships it.

---

## 3. The harness — being built (WHAT'S LEFT H31)

The operator's words, 2026-10-16: "A single simple driver that runs long workflows and tool chains to make sure that
basically whatever I ask can be done. Fairly simple."

**The driver is Steward**, the body that acts (SPEC 8.4), doing what it was designed for. One seat, one loop:

    a goal, typed in the Agent tab, with its check named
       -> Steward picks a tool (the engine's skills, the door's tools) and calls it
       -> the door runs it, or holds it for his card when it writes
       -> the result goes back to Steward, and it goes on
       -> it stops when the check passes, or when its budget runs out
       -> the change is kept on a line of work, or reset
       -> the report is written from the record, never from the model's account of itself

**The model never says it is done; the check does.** That is how the models stay inside the system, and it is the shape
an open-source loop called Nigel showed to work: a coding agent's change is kept only when a check passes and the thing
asked about is gone.

The law it runs under is LAW_003, THE LOOP (sealed; his word of 2026-09-17): a loop is lawful only with all three bounds --
a ceiling declared where a reader meets it, a stop a machine checks over evidence the machine emitted itself, and every pass
in the record, the failed ones included -- and the gate stands at the end: the loop stops to ask leave to land, never to try
again. His card on every write (below) is stricter than that, by his word.

| piece | the design | his word |
|---|---|---|
| the job | a task that names its check: the suites, a named test, a file that must say a thing, a line GitHub must hold | "the checks are named by tasks or some other trackable" |
| the tools | the basics first: read, write (every write on his card), measure (sizes, counts, the suites), locate (list, find, search); code edits handed to Aider, every run on his card | "the tools it needs to see for basics, like read write measure locate"; his card on Aider, 2026-10-16 |
| the budget | a ceiling against a runaway, not a race: generous passes and minutes, each run's spend written down (LAW_003) | "we dont need to push for speed initially, we can optimize after we get function" |
| the model | qwen3.5:9b, already on the rack; Nemotron 3.5 Bolt, an open model built for tool calling, only if the run logs show the 9B failing | his card; SITTING LAW 3 |
| the door | `aider_run` callable by the driver, every run parked for his card | "the door change, i siad it, we do it" |
| the set-up | C71 first: the engine's call to the door gives up at 295 s (the skill's bound, less five) and the strokes take about 313 s, so the suites, the check for code, must come back with their tally | "let's get set up for success" |

**What it replaces.** The coding loop (D18), workflows started from a sentence (H23) and the system's own task lists
(H25) close with it. Much of the routing and the relay of seats exists because small models were weak; once the
driver's numbers show a layer is not needed, the layer is folded, never deleted (LAW 1; SPEC 1: "every guard in it is
named after a failure that actually happened").

**Proved by three real jobs, live on his glass:** C71 itself; a save and send of a finished line; and the boot's gate
finding no HANDOFF block for the day (HANDOFF's finding (bb), 2026-10-14).

---

## 4. The walls — how the harness stays inside the system

1. **Decided outside the model.** The door judges every call by its transport; the law gate judges the objective before
   any model sees it; refusals are named and logged. A model cannot talk its way past any of them.
2. **His card on every write.** Saves, sends, edits, Aider runs and shell lines that change something wait in the dock
   (RULE 6). Publishing is his word in chat, each time (RULE 12).
3. **A check decides done.** The driver's own claim counts for nothing (LAW 5).
4. **The record writes the report.** What ran, what changed, what the check said; the honesty gate on every answer is
   the next piece of the core (H30).
5. **The operating system's cage, later and his call.** Microsoft's MXC (generally available since about 2026-10-07)
   and NVIDIA's OpenShell hold an agent's process inside limits the operating system enforces. They would sit under the
   door's shell and Aider; today those walls are the door's own, and Aider's is an audit hook, which the record says is
   not a kernel sandbox.

---

## 5. One job, end to end

    He types: "fix C71: a strokes run asked through the door must come back with its tally" -- the check: the strokes,
    asked through Steward
      1  Steward reads: the skill's bound, the door's wait, the call site (locate, read)
      2  Steward opens a line of work (a card)
      3  Steward hands the edit to Aider (a card); the edit lands on the line
      4  Steward runs the check: the strokes through the door; red goes back to step 3, green goes on
      5  Steward saves the line (a card) and sends it (a card)
      6  the pull request and the merge are his press on the GitHub tab
      7  the report: what was read, what changed, the check's tally, the cards he answered -- each a line in the record

---

## 6. Constraints

- **Local first.** Ollama is the route; a hosted model only on a route he turned on, for what he named (RULE 4 as
  amended). No cloud service, no telemetry.
- **One machine, one card.** Windows 11, a 16 GB RX 6800 XT, one call at a time.
- **One executor.** One seat runs tools (SPEC 1); the driver is that seat.
- **The gate is his.** Commits, sends, merges, marks and spends are his click (RULE 6, RULE 12).
- **Everything on the glass.** Every proof and every step where he can watch (RULE 13, RULE 14).
- **Simple.** His word: "i want this to be simple, it is already becoming complex." A new layer needs a measured failure
  behind it.

---

## 7. Trade-offs

| decision | chosen | over | why | cost |
|---|---|---|---|---|
| who drives | one driver in a loop | the relay of seats | a job is finished by one hand that keeps going, and one model stays loaded | the driver's model must hold a long chain of tool calls |
| the driver's model | local first (qwen3.5:9b) | a bigger or a hosted model now | SITTING LAW 3; private; free | it may fail on long chains: Bolt, or a route, on a measured need |
| who says done | a named check | the model's word | a model can claim anything; a check cannot | every job needs a check written with it |
| the walls | the door's own (holds, refusals, roles) | the operating system's cage now | built, proved, and his to watch | not a kernel sandbox: MXC or OpenShell later, his call |
| breadth | the loop first | chat channels, skill markets, installers | his target is that whatever he asks gets done | fewer ways in, for now |

---

## 8. What to revisit as it grows

- **The window**: a long chain is where a seat's window matters (C70's step (2); H20's cache and truncation).
- **Memory that comes back** (H2 to H4), so the driver starts from what was decided before.
- **The honesty gate** (H30), so the report and the record never part.
- **The cage**: MXC or OpenShell under the door's shell and Aider.
- **A seat on a route** (H8), only on a measured need.
- **The long view** stays his (SPEC 8.1): "like a second brain, a wholly agentic system that essentially runs all of my
  digital life". The harness is the road to it.
