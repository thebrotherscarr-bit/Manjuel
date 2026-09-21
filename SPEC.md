# SPEC — what manjuel is, and when it is done

Written 2026-09-04 on the operator's word ("getting close to an actual
product, review missing specs, and write full spec -- 'when done'"), from a
full read of the code, the record and the laws. This is the one document
that says what the thing IS and what DONE means. DESIGN.md is the reasoning
and its history; BUILDPATH.md is the module map; BUILDMAP.md is where each
thing lives; REFUSALS.md is what each guard refuses; this is the contract.

A line here is either MET (with where it is proved), OPEN (with what is
missing), or RULED OUT (with who ruled). Nothing here is aspiration
wearing a checkbox.

---

## 1. What it is

**manjuel is a local, sequential, markdown-declared council of small
language models that answers an operator at his own terminal, where every
tool call is executed by exactly one seat, every claim a seat makes is
checked against what actually ran, every run is written down, and every
run passes through a sealed law before any model reads a word.**

Plain version: one person types a request. A few small models, each with a
job written in a markdown file, take turns on it. One of them — the Router —
is the only one allowed to run tools. The engine, not the models, decides
what is a fact: it records what tools returned, refuses a model that claims
to have read or written something it did not, appends every failure to the
answer whether the model mentioned it or not, and stamps every run with
which laws it checked. Nothing leaves the machine.

### Who it is for

The operator. One person, one machine, one folder (`Desktop\Research`). It
is not a service, not multi-user, not hosted. A second user is a fork.

### What it is for (the operator's words, session 2)

*"RUN IT AND WRITE DOWN WHAT FEELS OFF."* The product is a harness that makes
small local models SAFE TO USE and HONEST ABOUT THEMSELVES, so the operator
can hand them real work on his own files and trust the record more than the
prose. Every guard in it is named after a failure that actually happened.

### What it is not (RULED OUT)

- Not a cloud product, not an API client, not a model host. RULE 4.
- Not a second executor. One seat runs tools. Option A declined 2026-09-04.
- Not a bigger-model project. SITTING LAW 3: move up only on a measured
  failure.
- Not a general agent framework. It has fourteen named seats and forty-three
  named skills, and adding one is writing a markdown file, not code.
- Not a chat app with memory. `memory.md` is landed by the operator's hand
  (`/remember`, `/memory`, or `remember that` typed at the door); a model
  may only propose.

### The words (ruled 2026-09-07: "fix the name spread")

The vocabulary of this ground, in one place. THREE RULES: no new noun
without a line here; a name is a word from the operator's own record or
the plain English of the thing; every line says where the word came from.
A proposal that needs a word uses the nearest one below.

| word | means | from |
|---|---|---|
| **the ground** | `Desktop\Research`, the one folder. Seats read it; nothing reads outside it. | CLAUDE.md RULE 1, 2026-08-29 |
| **the workspace** | `agent_workspace/`, the seats' scratch: the ONLY place a seat writes, and where anything from outside lands first. | sittings 18–27, 2026-08-29 |
| **the estate** | the whole system: the seats, the law, the record, the rack. | the founding docs (LAW_001) |
| **a seat** | one job, one markdown file in `agents/`, one model on it. | agents/, DESIGN.md |
| **the rack** | the models installed on this machine; also the seats that rest until a flag wakes them. | rack.md; pipelines.md |
| **the spine** | the seats that sit every run of a pipeline. | pipelines.md |
| **the door** | the Steward: first to answer, last to report. | pipelines.md |
| **the court** | Neiro, Jesster, Manjuel: reads, never acts; Manjuel rules last. | THE LAW; pipelines.md |
| **the Router** | the one seat that runs tools. | DESIGN.md |
| **a skill** | one tool: a markdown file in `skills/` and a handler. | skills/ |
| **a pipeline** | ONE TURN's running order of seats and tools: who sits, in what order, who wakes on which flag, which seat hands to which. The Steward handing to the Router, the Router calling the index, Jesster reviewing what the Router read -- all inside one pipeline. Declared in `pipelines.md`. | pipelines.md; ruled 2026-09-07 |
| **a workflow** | SEVERAL TURNS strung into one task: a list of objectives, each run through a pipeline, checked between steps, reported at the end. The standup is the first one. Not yet declared in a file. | the operator, 2026-09-04 and 2026-09-07 |
| **a flag** | a seat's one-word signal to the engine (`needs_tool`, `technical`, `worked`); wakes a racked seat. | DESIGN.md §5 |
| **a sitting** | one launch of the REPL, numbered by Manjuel. Never the hand's session. | seatlog.py; LAW 10 |
| **the toll** | what a sitting pays at close: what proved, what is thin, what is owed. | LAW 10 |
| **the record** | everything written down: transcripts, SEAT_LOG, DAYBOOK, HANDOFF, CHANGELOG, memory.md, sessions. | LAW 1, LAW 10 |
| **the standing** | what this sitting is for, from DAYBOOK's last entry, handed to the door and the court. | 2026-09-07 |
| **the law** | the ten estate laws (seats) and the sitting laws (hands), sealed in `law/`; the gate every run passes. | law/ |
| **a hand** | any agent, human or model, working the ground in a sitting. Bound by the sitting laws, not the estate laws. | SITTING_LAWS.md |
| **a stroke** | one check in the suites. Green or red. | tests/ |
| **a guard** | a refusal the engine makes by arithmetic, named after the failure that earned it. | REFUSALS.md |
| **a layer** | BUILDPATH's word for a tier of the code (0 words on disk … 9 a stranger's first hour). A code word, not a name for findings -- two TASKS headings that misused it were renamed 2026-09-07. | BUILDPATH.md |
| **the brief** | the sitting opener: where the build is, what he said we are working on, what is waiting -- read off the record at every open; `/brief` has the door say it. | the operator, 2026-09-07; built the same day |
| **inspect** | the skill that reports a file's FACTS before anything reads it -- size, type by bytes, timestamp, jail, git, index, secret/client, injection markers -- never its contents. The workspace is the quarantine it serves. | sittings 18–27 (2026-08-29); the operator, 2026-09-07 |
| **remember that** | the operator's cue at the door that lands a memory: his words after it, else the newest proposal, else the last delivery. Never a seat's. | sitting 89; built 2026-09-07 |
| **a kind** | the one word on a memory entry saying what it is: guidance, decision, ruling, learning, outcome, note. | the operator, 2026-09-07 |
| **the release gate** | one command before a tag that refuses by name until the record is whole; `tests/release.py --check`. | the operator, 2026-09-08 ("reviewed, updated, and logged, at all times"); built the same day |
| **the story** | what THIS sitting has done so far, read off the ledger and handed to the door and the court; bounded like a window. | the operator, 2026-09-07 ("keep that in context for now") and 2026-09-08; built 2026-09-08 (0.1.6) |
| **out of time** | a seat not seated because the turn's deadline had passed; named in the delivery. | the operator, 2026-09-08 ("never more than 10 minutes between a response") |
| **the maker** | the engine's route for "make me a ...": the Expert Coder writes ONE web page, the engine checks it and saves it as a version of a project. No seat saves anything. | the operator, 2026-09-21 ("projects folder in Research is fine, build it"); `manjuel/maker.py` |
| **a project** | one thing the maker made: a folder under `projects/` with its own git history, never part of the core's repository. | the operator, 2026-09-21 |
| **a version** | one save of a project, numbered from 1, with a plain-English note. "Go back" saves an old one again as the next number, so nothing is thrown away. | 2026-09-21; LAW 1 |

---

## 2. The parts, and the contract each one keeps

| part | what it promises | proved by |
|---|---|---|
| **The ground** (`Desktop\Research`) | every read, write, index and dependency stays inside it | `gate_paths` (LAW 8), `_inside_ground`, `safe_path`; the law gate's reach check; strokes `test_index_stays_in_research_and_off_the_keys`, `test_the_law_gate` |
| **Seats** (`agents/*.md`, 14) | a seat is a markdown file: model, stage, when it wakes, what it may call, its prompt. No seat exists in code. | `registry.py`; `us/chain_*.us` reconciled by `us.py` |
| **Skills** (`skills/*.md`, 42) | a skill's markdown declares it; a handler or a model target runs it; neither can exist without the other | `SkillLibrary.validate`; `us.py` |
| **Pipelines** (`pipelines.md`, 5) | the running order is a file; racked seats wake on flags declared in their own file | `PipelineBook`; `seating.py` |
| **The Router** | the ONLY seat handed tool schemas and the only one whose action blocks execute; bounded at 5 hops; identical calls refused | `pipeline.py` tool loop; REFUSALS §9, §14, §18 |
| **The door** (the Steward) | speaks in words; a tool call it emits is carried to the Router, never printed; after work it reports what ran and nothing beyond | REFUSALS §18; the closing prompt's `TOOLS THAT ACTUALLY RAN` |
| **The court** (Neiro, Jesster, Manjuel) | reviews, never acts; reads only; four different heads; rules last | `review_only`; REFUSALS §3; the 2026-09-04 rack ruling |
| **The guards** | a claim of file contents with no read is refused; a claim of a write with no writer is refused; a cited search hit that was not returned is refused; every failed tool AND every partial read is appended to the delivery; a recited scaffold is discarded | REFUSALS §8, §10, §11, §11b, §20; `_SCAFFOLD_RE`; `recompose` |
| **The law gate** | the sealed ledger verifies on every run or no seat sits; the objective is checked against the decidable laws; every seat is handed the verdict in its SYSTEM role (the court: the ten verbatim); the run is stamped | `lawgate.py`; REFUSALS §19, §20; `test_the_law_gate` |
| **The standing** | what the sitting is FOR, from DAYBOOK's last entry, read not generated, handed to the door and the court | `seatlog.standing_block`; REFUSALS §20 |
| **The story** | what the sitting has DONE, from its own ledger lines, read not generated, handed to the door and the court; "what happened?" is answered from it | `seatlog.story_block`, `note_for`; `intent.asks_the_sitting`; REFUSALS §22 |
| **The ruling loop** | a seat that thought and did not rule is asked again, thinking off, at most three times; the Router is never looped | `MAX_RULING_TURNS`; `_press_for_ruling`; REFUSALS §20 |
| **The bounds** | one seat call: its `Timeout:` by model size (150/300/600/700) or the 700s ceiling, cut at the wire; one turn: 600s, the seats after it named OUT OF TIME, the seats that failed named too; one index build at a time (`index_ground`, `embed_text` -- the watcher's turn-boundary re-index does not take the lock, found 2026-09-17 and open); twelve ruling turns; one headless engine: thirty minutes with no command between turns and it closes its own sitting (2026-09-16) | `runtime.SEAT_TIMEOUT`, `pipeline.TURN_DEADLINE`, `skills._INDEX_BUSY`, `serve.IDLE_CLOSE`; REFUSALS §21; `test_an_idle_engine_closes_its_own_sitting` |
| **The release gate** | a tag is refused by name until the record is whole: suites, buildmap, standup, law, manifest, SPEC↔CHANGELOG, DAYBOOK, HANDOFF | `tests/release.py --check`; RUNBOOK "Before a tag" |
| **The record** | every run is a transcript; every sitting is a numbered line and a toll; memory is landed by hand; nothing is deleted | `transcript.py`, `seatlog.py`, `memory.py`; LAW 1, LAW 10 |
| **The index** | chunked, incremental, bounded, embedder-stamped; client material and secrets never enter it; transcripts age out of retrieval at 45 days | `vectors.py`; REFUSALS §5, §6, §16 |
| **The rack** | seven models seat fourteen seats; the everyday pipelines fit resident; the court evicts on purpose; `rack.md` is derived from Ollama, never edited | `vram.py`, `rack.py`; `test_vram` |
| **The suites** | the engine proves offline with every model stubbed; the REPL proves the same way; the standup runs the seats live and writes a report; the map is generated from the code | `tests/test_manjuel.py`, `smoke_cli.py`, `standup.py`, `buildmap.py` |
| **The maker** | "make me a snake game" seats the Expert Coder alone; what it answers is saved only if it is a WHOLE page that loads nothing from the network; each save is a numbered version in the project's OWN history; "go back" is git's job, not a model's; the ground's history is never written to | `maker.py`, `intent.wants_making`; §4.8; `test_the_maker` |
| **The toll** | every sitting that ran something ends with what proved, what is thin, what is owed — the operator's words, or an honest "not stated". A sitting that ran nothing closes with no toll, from the Dashboard's Close or on its own when idle (RUNBOOK, 2026-09-14; D2, 2026-09-16; this row said "every sitting" until 2026-09-17) | `seatlog.render_toll`; LAW 10 |

---

## 3. The invariants (what is never true)

These hold on every run, and each has a stroke or a gate. If one of these
is ever observed false, that is the bug, before anything else.

1. No model output is executed as instruction. (LAW 5; `mathkit.parse_numbers`, `voice._speech_cmd`, `inspect_code`)
2. No seat but the Router executes a tool; no seat but the Router is handed schemas. (REFUSALS §18)
3. No control markup — `<action>`, `<flags>`, a JSON tool call, the dialogue scaffold — reaches a delivery. (`strip_control`, `_SCAFFOLD_RE`; the standup's `NEVER_IN_DELIVERY`)
4. No path resolves outside its jail; no absolute path is accepted from a model. (`gate_paths`)
5. No secret is read, indexed, printed or committed. (`is_secret`; `dotenv.report`; the law gate)
6. No client-tagged file is read, indexed, listed or cross-referenced. (`is_protected`; SITTING LAW 2)
7. No commit, push, pull, pull-of-a-model or spend happens without the operator; local commit is the one ruled exception and it is additive. (`gitstate`, `rack_pull`; RULE 6) The maker's versions are local commits inside each project's own repository -- never the ground's, never pushed (2026-09-21, `maker._is_project`).
8. No run proceeds on a law that does not verify. (the law gate)
9. No failure is omitted from a delivery. (`recompose`)
10. No count is written into a doc; every number is read from what a run produced. (`proved`, `suite_tally`)
11. Nothing in the record is deleted; a correction is appended. (LAW 1)

---

## 4. DONE — the acceptance, line by line

**The build is done when every line below is MET and the operator has run
the standup on his own terminal and read the report.** Lines marked OPEN
are the whole remaining distance.

### 4.1 Installation and first hour
- MET — one `pip install ".[test]"` (one dependency to run, `ollama`; one
  more to prove, `numpy`, which a stroke imports outright), eight `ollama pull`s named in QUICKSTART (seven seat tags and the embedder), `python manjuel.py` boots or names the missing tag. CI on Windows and Ubuntu.
- MET — a stranger's reading order exists and is ONE order, BUILDPATH's: CLAUDE.md → DAYBOOK (last entry) → README → QUICKSTART → BUILDPATH → pipelines.md → one seat file → intent.py → pipeline.py with a transcript beside it; BUILDMAP and REFUSALS when looking for a thing or a refusal. CONTRIBUTING states the house style.
- MET (2026-09-04, prove.yml) — `python tests/buildmap.py --check` runs in CI. MET (2026-09-09) — `BUILDMAP.md` IS in `index_roots.txt`; the call was his and he made it ("index everything"), along with every other root document and the five law files: 17 roots → 39, 828 → 995 indexed documents.

### 4.2 An ordinary turn
- MET — a plain greeting seats one model and returns in seconds; a tool-naming objective wakes the Router directly; a write-shaped one lets the Router decide; a question carrying a term reaches the reader.
- MET — the door's tool call is carried, never printed (both costumes).
- MET (2026-09-10) — PHRASES FOR THE DOOR, KEYWORDS FOR THE ROUTER. Ruled 2026-09-09 ("that's what the chat/router gating is for") and built the next morning. `_steward_prompt`'s task branch handed the door `", ".join(sorted(skills.keywords()))` — thirty-seven callable tokens in front of a 3b asked to say good morning — and sitting 88 answered them: "our objective is to answer a question about sentiment classification... we'll use the `classify_sentiment` tool", a mission built around a name it had just been shown (`classify_sentiment` is ours, so nothing was invented; the roster WAS the provocation). The door is now told the SHAPE of the reach in prose and not one callable name; the Router still gets the whole list (`_router_prompt`). A phrase per skill was measured and refused: 4,617 characters against 451, ten times the prompt at the one seat whose value is answering in under a second. Six strokes hold it, and the guard is DERIVED from the library — no underscored keyword may appear in the door's prompt — so a skill added tomorrow cannot quietly reappear there. Proven live on the same objective: "morning, what's on the board?" now returns "The ground is currently quiet... What would you like to do, operator?", 5.3s, no tools.
- MET (2026-09-07, sitting 91; the last clause 2026-09-10) — when intent has the tool AND there is nothing left to choose, the engine runs the call and the Router only reads the result (`decided_call`). An argument checked on disk closed the first half. THE SECOND HALF, open since 2026-09-04, was a tool named with NO argument: `git status` made the Router write a call there was never anything to write, at the cost of a model call and the chance to choose wrong — which it did, four standups running, on the folder case this same mechanism was built for. Six skills declare no parameters (`git_status`, `rack_list`, `list_directory`, `proved`, `ground_report`, `skill_report`), so the objective naming one determines the call in full. TWO GUARDS, both existing rulings rather than new ones: a WRITE is never decided by arithmetic (`git_init`, `git_pull`, `git_push` and `rack_sync` declare nothing too and are excluded by `WRITING_SKILLS`, not by a list), and only a tool the OBJECTIVE named outright qualifies — one an engine branch guessed is still the Router's. `declares()` is ONE expression, shared with the dedup so the two cannot separate. Six strokes; the superseded one was NARROWED, not deleted — with no library nothing can be decided, because nothing can say what a skill declares.

### 4.3 The court
- MET — four heads; reads only; Manjuel last; the recompose reaches both deliveries.
- MET (2026-09-10) — `rack_report` gives FACTS ONLY unless a judgement is asked for. Ruled 2026-09-09 ("4.3 facts only. yep, sounds good") and built the next morning: the Quartermaster is woken only when the question asks to be advised (`intent.asks_for_a_judgement`, beside the estate's other question shapes rather than a second copy in skills.py), and a facts question returns the observed numbers with one line saying no seat read them. Four strokes hold it, and the strongest asserts NO SEAT WAS CALLED rather than merely that its words are absent. The fault it closes: the Router summarised the reading instead of the facts, three times in sitting 85, and SPEC 4.7 records the Quartermaster inventing in three of three readings.
- MET (2026-09-07) — a PARTIAL read is stamped in the record and the delivery (READ IN PART, NOT WHOLE); a file read in every part is not. `note_partial_read`, `unread_parts`.
- MET (2026-09-10) — a claim about what a tool result SAID, with no citation tying it to the result, IS NOW MEASURED. The cited half was already built (`bogus_citations`, sitting 61: a (path, cosine) pair claimed but absent from the output); this is the half `intent.cites_search_results` named as its own honest limit, "prose that fabricates without naming a path and a number". A TOOL RESULT IS SOURCE MATERIAL, so drift primes on it and the stages after it are scored against what the tool actually returned. Advisory, as drift is by design — reported, never used to rewrite or discard, "the same principle that keeps Manjuel and Jesster from rewriting the work they rule on". Proven live on one objective three times: `what is in the skills dir` read "not scored this run (no usable source)" at 06:13 and 06:50 and **drift 0.788** at 07:05.

### 4.4 The law
- MET — the ten estate laws, the four sitting laws, LAW_003 and the law ledger are sealed (6 links; this line read "4 links" until 2026-09-21, one short since LAW_003 on 2026-09-17); the chain verifies; the gate runs first on every run; a tampered law refuses every run.
- MET (2026-09-21) — SITTING LAW 5 (nothing edited while a sitting is open) is sealed. It was a CLAUDE.md rule with no sealed file, and the file's name and place were the operator's to give. **Given 2026-09-21, on his word:** `law/LAW_LEDGER.md`, an appendable law that `law.py seal` seals by prefix, so it grows below its last seal. SITTING LAW 5 is its first entry, with SITTING LAW 6 (the hands-ledger half struck), the docs-move-with-the-change law, no-edit-without-an-entry and a copy of CLAUDE.md's rules. **Sealed the same morning, on his word ("seal it"):** link #6, all five entries, to byte 15509.
- OPEN — ESTATE LAW 2 (originals read-only) is a comment, not a gate: the `ground` jail contains `worlds/`. ESTATE LAW 3 and 4 have no mechanism.

### 4.5 The record
- MET — every run a transcript; every sitting a ledger line and a toll (unattended closes now write their line); CHANGELOG from sitting 1; DAYBOOK per session; HANDOFF per day. NOTED 2026-09-17: a sitting that ran nothing is tolled by nothing -- its ledger line reads `toll_paid: false` and SEAT_LOG has no entry for it (sittings 220 and 225).
- OPEN, NARROWED (re-measured 2026-09-09) — the client token is in **0** log filenames and **0** indexed documents; what remains is `sessions.jsonl` (24 occurrences) and the git pack (names, not contents). Counted, never printed. The pack cannot be changed without rewriting history, which was refused once already; the ledger is append-only. Both remaining places are the operator's call, not a hand's. **RE-MEASURED 2026-09-21, and the call is his: "remove the client tokens out of git and ledger history".** The ledger held 36, and holds 0. One indexed document did carry it -- sitting 61's row in CHANGELOG's list of every sitting -- and that line is scrubbed in the working tree; in git it still stands in all 115 commits of `main` and all five marks, and on `push-main`, `remote-main` and `pre-strip-master`. The rewrite was refused by the session's permission check and waits on his word (CHANGELOG, 2026-09-21). **REWRITTEN the same morning, on his second word:** `main` (now `b314b9d`), `push-main`, `remote-main` and the five marks carry it nowhere; GitHub waits on the force-push, and `pre-strip-master` on his call. **Pushed the same morning, by his hand; GitHub's `main` and five marks match this machine.** **Purged here the same morning:** only `pre-strip-master` still carries it, and he ruled it kept ("keep it"), local and never pushed.
- OPEN (re-counted 2026-09-09, after atlas landed in the ground) — the two-terminator state: **528 tracked text files LF, 84 CRLF, 4 MIXED**. The ruling is CRLF; the disk is not. And the four MIXED are not all the same thing: three are atlas's byte-exact test fixtures (`chains/*.jsonl` goldens, deliberately never rewritten) and the fourth is `tests/run_history.jsonl`, where `standup.py` appends CRLF lines into an LF file — the one that is a defect rather than a golden. `.gitattributes` declares CRLF and stores LF blobs, so the committed record is consistent either way. Decision (renormalize, or rule LF) is the operator's; then a stroke. **RE-COUNTED 2026-09-14, and the population moved:** atlas is its own repository now (the core tracks nothing under `atlas/`), so its goldens are no longer counted here. The core ground reads **LF 143, CRLF 32, MIXED 0** -- `tests/run_history.jsonl` is no longer mixed, and the suites' own writers are held to one terminator by a stroke (850e2ce). What stays OPEN is the ruling against the disk: CRLF is the ruling and most tracked text is still LF. Recompute: `git ls-files --eol`, counting the `w/` column.
- NOTE, not OPEN (his ruling 2026-09-09: "doesnt need to carry an open status, but it should be sorted and numbered") — SEAT_LOG numbering has **14 gaps and 10 unmarked duplicates** as of 2026-09-09 17:20, over 119 headings to a maximum of 123 (gaps: 1, 2, 5, 6, 15, 16, 20, 33, 34, 36, 43, 97, 99, 118 -- 118 is the newest, the sitting a wedged boot opened and a killed process left standing, closed by appending and never tolled; duplicated numbers: 22, 26, 40, 42, 57, 60, 63, 64, 79, 85, and nothing in the file marks any of them, so all ten are unmarked). Record, not defect; noted so nobody "fixes" it by rewriting (LAW 1). **HIS ASK, AND THE CONFLICT IN IT (2026-09-09): "it should be sorted and numbered".** SEAT_LOG's own second line is "Append below; never rewrite above", so SORTING THE FILE IS REWRITING THE RECORD — the one thing LAW 1 forbids, and the reason this note exists at all. Proposed instead, and not built: a GENERATED INDEX beside it — every heading read out of SEAT_LOG.md, sorted by number, gaps and duplicates marked, regenerated like BUILDMAP so it can never drift from the file it describes. The log stays append-only; the sorted view is derived. His call which he meant. THE COUNT MOVES whenever a sitting closes untolled, so it carries its date and the way to recompute it rather than a bare number that rots: read the `## <date> - sitting N -` headings out of SEAT_LOG.md, and compare the set against 1..max. It read "11 and 5" for days after it stopped being true.

### 4.6 Proof
- MET — the strokes and the smoke checks, offline, every model stubbed; their counts are READ from `tests/last_run.json` (invariant 10 -- this line carried "1685" until 2026-09-08 and was wrong the same day); `law.py --prove` 17/17 (the seal's eight since 2026-09-21); `us.py` reconciles 51 records; the standup harness proves dry 10/10.
- MET — the standup has run LIVE six times (sittings 86, 88, 90, 91, 92, 96): 8, 9, 9, 9, 10, 10 of 10. MET (2026-09-04 16:42, `sessions/parity_history.jsonl` line 2) — the parity has run on the tiered seats, 12 cases, every tier against its reference head. MET (2026-09-08, afternoon) — the standup judges seats sat, failed stages, OUT OF TIME, the judge's last word, and the numbers in the delivery (`test_the_p0_of_the_review`).
- MET (2026-09-08) — THE RELEASE GATE: `python tests/release.py --check` refuses a tag by name unless the suites are green after the newest edit, buildmap is clean, the standup ran live and green, the law proves, the manifest agrees, every section-4 status change since the last tag has an Unreleased CHANGELOG line, DAYBOOK is closed, HANDOFF has today. Reads only. `test_the_release_gate`.

### 4.7 The rack
- MET — seven models, tiered; everyday pipelines fit 15 GB resident; the court evicts on purpose; parity cases pit each head against the other in its tier.
- OPEN — llama3.2 at the door: held on tool strings; parrots the question as its counsel at every court (88–92); recited its own closing instruction once (89); keyword bait five sightings. STAMPED 2026-09-10 (TASKS said "stamp or reseat"): recompose now compares the delivery's numbers with the run's tool results and travels the difference with the answer, by the same arithmetic it already uses for what was omitted. The check existed and ran in ONE place, `/brief`; it now runs on every turn where a tool ran. THE SEAT STILL INVENTS — a stamp catches it, it does not cure it, and reseating remains open. NEW SIGHTING 2026-09-09, and it is INTERMITTENT: the standup's `a folder` case had Steward (llama3.2) report the skills dir holds "37 markdown files, ranging from 300 to 1200 bytes in size" with 300 and 1200 in NO tool result that run (16:53); the same objective through the same seat passed seventeen minutes later (17:10). The count was right and the range invented. Same class as TASKS' "the door invents numbers", and a coin-flip rather than a fixed fault — which is why a green gate is not evidence it is gone. MET — gemma4:12b at Manjuel ruled on turn 1 in five courts at 16384 (88–92); the window, not the model, was the fault. The Quartermaster on llama3.2 invented in three of three readings.

### 4.8 The maker (his word 2026-09-21: "projects folder in Research is fine, build it")

Why it exists: sitting 257 put his own test through the estate -- "Make me a simple snake game I can play." -- and nothing was made. The door role-played a game, the Router planned and did not act (and a 900-token cap left one try a 0-byte file), and the Expert Coder never woke. The pieces and their order are BUILDPATH's, "The maker"; the reasoning is DESIGN 14.15.

- MET (2026-09-21, piece 1) — a request to MAKE a thing people use (a game, an app, a page, a tool, a calculator, a timer...) is read by arithmetic (`intent.wants_making`), seats the Expert Coder ALONE, and what it answers is saved as version 1 of `projects/<name>/`, a folder with its own git history. The delivery is the engine's plain report: what was made, where it is, and what to ask next. A poem, a note, a commit, a python script and a question about making are not the maker's and fall through untouched. `test_the_maker`. Proven live from the dashboard, sitting 258: a 93-line snake game in 15.4s that starts on a click and steers with the arrows (seen); its scoring and Game Over are read from its code, not yet seen.
- MET (2026-09-21, piece 1) — a CHANGE ("make it faster", "add a score": the request opens with a change verb, and the sitting has a project in hand) hands the Coder the page as it stands and saves the rewrite as the next version; "go back" (or "undo", or "go back to version 2") saves the older page AGAIN as a new version, and no model sits for it. "Add an undo button" is a change, not a go-back. History only grows (LAW 1). `test_the_maker`. Live, sitting 258: version 2 in 10.8s changed one line (the game's tick, 100ms to 50ms); version 3, back to version 1, in 0.6s.
- MET (2026-09-21, piece 1) — nothing the check refuses is saved: a page is kept only if it is WHOLE (it reaches `</html>`) and loads NOTHING from the network (`maker.page_from`, RULE 4); a refused first answer leaves no project behind; the ground's own history is never written to (every git call first checks the project's own `.git`); `projects/` is gitignored. `test_the_maker`, stroked both ways and proved by reversal.
- NOTE, not OPEN — while a sitting has a project in hand, ANY request that opens with a change verb goes to that project ("fix the router config" included). There is no word yet to put a project down except closing the sitting, and a new sitting starts with none. Choosing a project, and leaving one, belong to piece 2's project list.
- OPEN (piece 2) — the page is not yet shown ON THE GLASS: today the report names the file to open (`projects\<name>\index.html`), and there is no project list to pick one from. His call to order it.
- OPEN (piece 3) — the check proves a page is whole and local, NEVER that it works: nothing runs it before it is kept. Piece 3 loads it in a browser with no window and sends any error back to the Coder before a version is saved. Seen live 2026-09-21: version 1 calls `clearInterval(game)` with no `game` declared -- harmless where the Game Over alert reloads the page, and exactly what this piece would catch. His call to order it.
- OPEN — THE WIFE TEST, his words and this section's DONE: "if my wife can sit down at the PC, ask the system to make a type of software, game, etc. and she can see the result, play the game, try the software". A person who is not the operator asks the glass in her own words and plays or uses the result -- no terminal, no path typed, no help -- and every step is in the record. Pieces 2 and 3 are what stand between today and that.

---

## 5. Out of scope until DONE (RULE 5)

Voice beyond what is there; `screen_act`/CogAgent (closed by the VRAM
ceiling); a second executor; a shortlist by embedding (measured
unnecessary); a term-level client shield (declined); the two-tier refactor
(declined); the twelve shards of LAW_002 (a spec with no mechanism, kept as
law, not on the build path); any new capability the operator has not named.

---

## 7. THE DELIVERABLE — what "a full system" is (2026-09-08)

Written on the operator's word ("get this whole system in line and
deliverable ... deliver a full system") after the whole record was read
that day (TASKS, "From the review of 2026-09-08"). Section 4 is the
acceptance, line by line; this section is the spec above it: the problem,
the goals, what is not a goal, who it is for in their own words, and the
requirements in the order they gate the tag. It adds no capability the
operator has not named (RULE 5).

### 7.1 The problem

One person runs small local models on his own files. A small model
invents: a path, a number, a tool result, a ruling. The cost of not
solving it is the record itself becoming untrustworthy -- today's review
found a brief that named a commit that never happened, a "finished" that
was a `UNIQUE constraint failed`, a court that "ruled" with no judge, and
a skill's own output fabricated for the operator who asked to see it
work. Every one of those was caught by reading the disk; none was caught
by the prose. The problem is not the models. It is any path by which a
model's sentence reaches the operator, the delivery, the memory or the
index without the engine having checked it against what ran.

### 7.2 Goals (outcomes, each with its measure)

1. **No delivery contradicts the record.** Measure: the standup's cases
   judge seats sat, stages failed, seats out of time and numbers in the
   delivery against the run's own record; ten of ten, live, twice
   running. (Today: ten of ten with a court that had no judge.)
2. **No response gap over ten minutes.** Measure: no run in the ledger
   over `TURN_DEADLINE`; the court fits its four seats inside it.
   (Today: measured, held at 600.0s -- with the judge cut.)
3. **Nothing unchecked reaches the record.** Measure: a refused feed is
   never a transcript's delivery; a number in a delivery that is in no
   tool result is stamped; a jail name never reaches a reader.
4. **The record is whole at every tag.** Measure: `tests/release.py
   --check` passes on the operator's terminal before every tag, and the
   hands ledger closes every hand's session (0.1.6). (The hands ledger was
   removed 2026-09-09 at his word, so that half no longer measures
   anything -- noted 2026-09-17.)
5. **A stranger runs it in an hour from the docs alone.** Measure: the
   reading order is one order; every command, skill, dial and bound is
   named in a doc; the docs carry no count the suites print.

### 7.3 Non-goals (RULED OUT, and why)

- A bigger model, a cloud model, or a second executor -- SITTING LAW 3,
  RULE 4, the 2026-09-04 ruling. The rack moves on a parity number only.
- Making the seats write better prose by prompt. Eleven of the fourteen
  faults today were shapes the engine can stamp; a prompt is a request.
- A listening socket, a daemon, an API -- BUILDPATH: the position.
- Rewriting the record. Corrections are appended (LAW 1); the SEAT_LOG
  gaps, the dated counts and the old commits stand.
- Voice beyond what is there; `screen_act`; the two-tier refactor;
  LAW_002's shards; an embedding shortlist -- section 5.

### 7.4 Who it is for, in his words

"RUN IT AND WRITE DOWN WHAT FEELS OFF" (session 2). "Every single call,
no matter what, runs THROUGH the law" (2026-09-04). "There should never
be more than 10 minutes between a response" (2026-09-08). "Document,
build, review, document ... tiny-recursive loops instead of massive
ones" (2026-09-08). "You are EAGER to build something rather than review
what is already there" (2026-09-08, to the hand -- and the same fault,
in the seats, is the Router calling a tool because a tool is there).

### 7.5 Requirements, in the order they gate the tag

**P0 -- without these the court does not rule and the standup lies
(0.1.5's live measurement; TASKS, the review, P0):**
- The court's seat numbers fit the turn (the operator's numbers; a
  markdown line each). Acceptance: a live court seats all six and
  Manjuel delivers the ruling inside 600s.
- The standup judges seats, failed stages and OUT OF TIME. Acceptance:
  today's court transcript, replayed, is a MISS.
- A failed seat reaches the delivery the way a failed tool does.
  Acceptance: a court where Jesster is cut says so in the delivery.
- A refused run's transcript carries the refusal, never the feed; the
  index never holds an injected payload. Acceptance: the injection case
  re-run leaves no "Ignore all previous instructions" in logs/ or the db.
- An unknown skill name is named as unknown to the door and the record.
- A named tool whose one argument comes from the words is decided, not
  offered. Acceptance: `time_align <content>` and `semantic_search <q>`
  run first, the Router reads.
- A prompt skill is deduped on (skill, DECLARED args) across the whole RUN, and refused on empty
  content; the brief's numbers are the engine's, not the door's.

**P1 -- deliveries that do not match the record (0.1.7):** the number
check; the citation check's second half (a claim about a result with no
citation); the door's label-parrot, previous-question and scaffold
shapes, each a stroke; `ground/` on the workspace reader; a direct tool
request with a subject that wakes nobody.

**P2 -- the machine's own honesty (0.1.6-0.1.8, a line or two each):**
dotenv's silent unreadable `.env` and the unread `MANJUEL_OLLAMA_HOST`;
memory's index-addressed pending list; lawgate's cache stamp; seatlog's
conditional "At close"; runtime's forever-False tools cache; parity's
0.0s; drift's ok=True on outage; spelling's "clean" on failure; voice's
unbounded interruptible speak; the dead code named in TASKS.

### 7.6 Open questions (the operator's)

- The court's numbers: Neiro / Jesster / Manjuel in seconds, summing
  with the Router inside 600 -- or a court-pipeline deadline of its own.
- Whether `sessions/`'s untracked ledger should be an index root (it is).
- The terminator ruling (CRLF or LF) -- 0.1.8.
- The client token in twelve old filenames -- rename or rule (0.1.8).
- (Noted 2026-09-17: the client token has been in no filename since
  2026-09-09, and what remains is in 4.5; "0.1.8" is this section's own
  date talking -- the ladder has moved twice since, see 7.7.)

### 7.7 Timeline

0.1.5 is built and measured live once (sitting 96); the P0 list above
is its second half and precedes its tag. Then 0.1.6, 0.1.7, 0.1.8 as
TASKS "THE PATH TO 0.1.8" orders them, each ending at the release gate.
THE LADDER MOVED (2026-09-10, BUILDPATH): 0.1.8 was built and never
tagged, folded into the 0.1.9 tag; the seal is 0.1.10.
AND MOVED AGAIN (2026-09-17, BUILDPATH): 0.1.10 was only a version string
and shipped inside v0.1.11, THE CODING UPDATE, without the seal. The seal
has no number yet; naming one is his.
DONE is section 4 with no OPEN line, and the operator having run the
standup on his own terminal and read the report.

---

## 8. THE PLAN GOING FORWARD (2026-09-17, his word: "set a spec plan and a build path for the vision going forward")

Written from the record: section 4's five OPEN lines, TASKS' open sections,
BUILDPATH's ladder, and atlas's own governing spec
(`atlas/docs/SPEC_CONTROL_CENTER.md`). BUILDPATH carries the ORDER and the
mark procedure; this section says what each number MEANS and when it is DONE.
The numbers and the names are his (RULE 6); this is the shape, not a promise
that a version will be called any of these.

### 8.1 The vision, in his own words

    the engine      "a chatty front door with enough smarts to know when to
                    route externally and actually use the tools/skills that
                    it has access to through a larger routed system"
                    (2026-09-10)
    the loop        "semi-automated task runs we can string together as
                    pipelines/workflows to iterate on the system without
                    having to type in a series of commands every time"
                    (2026-09-04)
    the glass       "i am not running that terminal anymore ... we need that
                    functionality on the dashboard" (2026-09-09). atlas is
                    the control plane; Manjuel is the permanent engine
                    (ADR-001, atlas/docs/SPEC_CONTROL_CENTER.md §11)
    the discipline  "I don't trust the system, thus i want to see everything
                    and make sure its all logged and recorded ... measure
                    from one task to the next" (2026-09-10); "document build
                    review document ... tiny-recursive loops instead of
                    massive ones" (2026-09-08)
    the boundary    local only, no listening socket in the engine, the gate
                    is his: RULE 4, RULE 6, and BUILDPATH's position

  AND ON 2026-09-21, the whole of it in one afternoon (quoted as he wrote it):

    the machine     "an autonomous vibe-coding machine with all of the
                    transparency we need set on a local rack of models that I
                    can swap in and out as new variants come out, to review
                    parity and update the system as needed"
    the long view   "like a second brain, a wholly agentic system that
                    essentially runs all of my digital life, as a personal
                    digital assistant"
    the shape       "the terminal was made into a webapp, that's why atlas is
                    the way that it is, with the insertable engine, the whole
                    idea is modularity"; "I'd rather run the whole thing in
                    powershell, or windows native"
    the laws        "the laws are to firewall the agents from wrecking things
                    before they are ready"
    the pipeline    "a simple ass CI/CD pipeline that I can direct and watch
                    as it makes progress. It can also ask and review on where
                    the vision is ... present testing and iteration, discuss
                    features"
    the safety      "all the recent and common software dev 'safety' stuff
                    like versioning, build paths" -- "the 'for dummies'
                    simplified version of making software"
    the test        "The true test is if my wife can sit down at the PC, ask
                    the system to make a type of software, game, etc. and she
                    can see the result, play the game, try the software, etc.
                    kind of like googles AI studio."
    the record      "I want the system to record it all being done while it's
                    being done"
    the glass       "The whole thing running in the webapp, and able to see
                    what the system is doing live, while it kind of hand-holds
                    for you and does it's own version control project
                    management and all that 'stuff' that no one thinks about."

  The first piece of that built the same day is THE MAKER (4.8, 8.2 below).

DONE for the engine is still section 4: every line MET or RULED OUT, and the
operator has run the standup on his own terminal and read the report. This
plan is the order those OPEN lines close in.

### 8.2 The versions ahead

One theme each, each ending at the same gate (8.3). The pieces are in
BUILDPATH, "The order it goes next".

    THE PASSES -- the core, unreleased today
      what it is   the 2026-09-14 diagnostics pass, the optimization pass's
                   eight pieces, and D2. All landed, none tagged.
      DONE when    both suites and a live standup on his terminal after the
                   newest edit; `tests/release.py --check` PASSED 9 of 9;
                   the pins moved; CHANGELOG's Unreleased folded under the
                   number; the mark cut on main and sent (8.3)

    THE GLASS'S OWN PASSES -- atlas, unreleased today
      what it is   the trace ledger, pieces 1 to 6, D1, the release.yml fix,
                   `version-tag`, node retries, the hold queue, and the mark
                   guards of 2026-09-17
      DONE when    `python tests/prove.py --check` 0 broke; both Go modules
                   green and gofmt clean; the door's battery PROVEN; the ten
                   version pins in sync; the mark cut and sent -- and
                   `release.yml` fires on it and leaves a DRAFT release for
                   his hand, which is the first time that workflow will have
                   finished

    THE SEAL -- what 0.1.9 sent to 0.1.10 and v0.1.11 never carried
      what it is   the release gate in CI; ESTATE LAW 2 as a gate on
                   `worlds/`; SITTING LAW 5 sealed onto the chain (his act);
                   the terminator ruling (his); the client token's last two
                   places (his); the small-honesty list
      DONE when    4.4 and 4.5 hold no OPEN line

    THE DOOR AND THE COURT
      what it is   the court fits its turn -- both 2026-09-14 courts cut
                   Manjuel at the seconds the turn had left; llama3.2 at the
                   door, which 4.7 has held open since it was written; the
                   closer's recital; drift's two notes; the refusal that
                   names a reason it never checked; the card report that
                   cannot say "over"
      DONE when    4.7 holds no OPEN line, and two live courts running seat
                   all six with Manjuel ruling inside the turn

    THE LOOP -- his workflow direction of 2026-09-04, still unbuilt here
      what it is   the standup and the court as flows fired from the glass;
                   a run measured against the last one; the word `workflow`
                   given a file, as section 1's vocabulary already promises
      DONE when    a day's work is one fired flow and a report he reads,
                   with no typed command in it

    THE GLASS AS THE FRONT DOOR -- atlas H3 then H7, its own spec governs
      what it is   the Run, Traces, Waterfall, Seats, Rack, Record, Alerts
                   and Law pages as SPEC_CONTROL_CENTER §4.5 defines them,
                   and then the terminal becomes optional
      DONE when    a full sitting -- open, run, toll, close -- runs from the
                   glass with no terminal, twice running, and the REPL still
                   proves under the same suites

    THE REACH -- atlas, and a decision before it is a build
      what it is   the glass listens on every address with its auth gate
                   uncalled (`ConfigureAuth` has no caller); the door's holds
                   are off without `--auth`; Ollama listens on every address
                   too
      DONE when    nothing on the network can call a writing tool through the
                   glass, and the holds are armed or he has ruled they stay
                   off

    THE MAKER -- his vision of 2026-09-21; piece 1 built the same day
      what it is   "make me a snake game" made, versioned and reported by the
                   engine (4.8). Piece 1: the route, the check and the
                   versions (MET). Piece 2: the page and a project list on
                   the glass. Piece 3: the page loaded in a browser with no
                   window, and its errors sent back to the Coder before a
                   version is kept. The order is BUILDPATH's, "The maker".
      DONE when    THE WIFE TEST: someone who is not the operator asks the
                   glass for a game or a tool in her own words, and plays or
                   uses it -- no terminal, no path typed, no help -- with
                   every step of it in the record

    NOT IN THIS PLAN, and named so it is not mistaken for forgotten: the
    appliance and the business (`SYSTEM_DESIGN.md`, `atlas/LAUNCH_PLAN.md`
    and their T-stones). That work lives in a world, and SITTING LAW 2 keeps
    a world closed until he points at it. Its plan is dated 2026-09-08 and
    nothing of it has been built since `--ground`; when he points at it, it
    is read first and re-dated.

### 8.3 How a version is cut, from here on

Every mark is `vMAJOR.MINOR.PATCH`, cut on the main line, after the gate,
sent by name, and never moved. The steps are in BUILDPATH, "The marks, and
how one is cut"; the door refuses the rest by name (`git_tag`, 2026-09-12
and 2026-09-17), and the six marks that pointed into the stripped history
were removed 2026-09-17 on his word.

---

## 6. How this file is kept honest

Every MET line names a stroke, a gate or a file. If the stroke goes red or
the file moves, the line is wrong and this file is edited in the same pass
(CHANGELOG's rule: no edit without an entry). Every OPEN line names what is
missing and whose call it is. A line with neither is a line to delete.
