# INVENTORY

Everything the system can do, one line each: the list v0.2.6 is measured against (WHAT'S LEFT I2). Every line is run live on
his glass and its time written down, or ruled; the same list carries into v0.2.7, where what earlier versions promised is checked
against it.

Written 2026-10-10, the first pass, broad on purpose: read off the disk (agents/, pipelines.md, skills/, commands.md and the
engine's own palette in manjuel/cli.py, flows/) and off the door (its tool list, the seats, the flows and the rack, as the door
answers them), and the glass's tabs and pages off its own code. A line names a thing that exists today; nothing here is planned.

**How to read a line.** The handle (S1, K12, T40, ...) is how the measure step names it. "live run" is the sitting, or the glass's
own check, in which the line last ran live during v0.2.6, with ok or FAULT and a word on what was seen; it is empty until it has run.
"time" is how long it took there. A line nobody can run live is ruled, and the ruling is written on it.

**His rulings for v0.2.6 (2026-10-10, on his cards).** This file at the root. A live run on his glass for every line, strokes
aside. All four parts below in the first pass. One card per measuring sitting.

**The steps.** (1) This inventory. (2) The measure: every line run live, one card per sitting, its time written down; the live
check 9 of 9 with the review panel inside its turn, and the session test (R1) against sitting 345, among them. (3) Each fault and
each slow route mended or ruled, one piece at a time. (4) The v0.2.6 cut through the release flow, finishing COMPLETE.

## 1. The council

### Seats (agents/, 14)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| S1 | Deep Researcher | qwen3.5:9b · stage transform · racked, summoned by its flag | sitting 370: sat for deep_research; FAULT: it answered with the law-court meaning, not the ground's court | 119.1 s (the turn) |
| S2 | Delivery Agent | phi4-mini:latest · stage deliver · wakes on deliver · stands in brief | sitting 369: ok, delivered the brief | 54.8 s (the brief) |
| S3 | Expert Coder | qwen2.5-coder:14b · stage transform · wakes on technical · racked, summoned by its flag | sitting 375: ok, handed the Router's package -- all of pipelines.md (12,915 characters), then lint_code's result -- and answered from it; its fix saved in the workspace as scratch.py | 187.1 s; 297.9 s (the turns, his card in the second) |
| S4 | Jesster | deepseek-r1:8b · stage gate · stands in estate, court | sitting 368: ok, counsel in /table (drifted 0.537); 369 estate; FAULT in 366: past its 600 s bound in the court | 779 s (the table) |
| S5 | Manjuel | gemma4:12b · stage gate · stands in estate, court | sitting 368: ok, ruled /table (drifted 0.541); ruled estate in 369; FAULT in 366: past its bound in the court | 779 s (the table) |
| S6 | Morning Reviewer | llama3.2:latest · stage transform · stands in brief | sitting 369: ok, compressed the feed for the brief | 54.8 s (the brief) |
| S7 | Neiro | llama3.2:latest · stage transform · stands in estate, court | sittings 366, 368 and 369: ok, counsel in the court, the table and estate | 399 to 900 s (the turns) |
| S8 | Proofreader | phi4-mini:latest · stage transform · wakes on prose · racked, summoned by its flag | sitting 373: woken on his word at a green card ("proofread this sentence" raised prose); FAULT: it mended "too" and kept "their" for "they're" | 134.8 s (the turn, with his card) |
| S9 | Quality Evaluator | qwen3.5:4b · stage gate · wakes on drifted, review · racked, summoned by its flag | sitting 369: ok, summoned on "drifted" in the brief, PASS | 54.8 s (the brief) |
| S10 | Quartermaster | llama3.2:latest · stage transform · wakes on rack · racked, summoned by its flag | sitting 373: ok, "give me the rack report" raised rack and a green card asked him; woken on his word, and rack_report answered | 51.6 s (the turn, with his card) |
| S11 | Reasoner | qwen3.5:9b · stage transform · wakes on hard · racked, summoned by its flag | sitting 375: ok, woken on his card and handed the Router's package -- three skill_search results, 8,052 characters -- and building its answer from them; the riddle from his words alone, 5 cents; cut at its 1400 tokens twice | 378.9 s; 98.2 s (the turns, his cards in them) |
| S12 | Router | qwen3.5:4b · stage route · when needs_tool · stands in default, court | sitting 375: ok, told which seat waits behind it and its ways up read from the seat files; named no task in any of the three turns that asked it (the fallback held); ran skill_search three times on one ask | 31.2 to 378.9 s (the turns) |
| S13 | Security Guardian | llama3.2:latest · stage guard · wakes on has_feed, suspicious · stands in brief, estate, court, quick | sittings 366 to 370: ok, SAFE wherever it sat; the three gates refused at once | at once at the gates |
| S14 | Steward | llama3.2:latest · stage transform · stands in default, estate, quick | sittings 373 and 374: ok, it answers its own reads ("list the skills", inspect); FAULT: it still retells earlier turns, once with its own instructions, and it turned skill_report's 45 skills into 43 | 8.6 to 20.5 s (its own reads) |

### Pipelines (pipelines.md, 5)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| P1 | default | The everyday turn: the Steward answers first and closes; tools, code and documents go through the seats between; each turn is tagged by its level, which may bring the Router or a big seat | sitting 376: ok, an ask at each level -- the Steward alone, the Router, the Reasoner on his card, a workflow's job run as the Reasoner's; FAULT: a big seat's turn left the closing Steward 48 s of the 600-second deadline | 2.6 to 661.5 s |
| P2 | brief | For a pasted feed: the Morning Reviewer compresses it, and it is delivered as a written briefing. | sitting 369: ok, the feed briefed by four seats | 54.8 s |
| P3 | estate | Every seat runs, the deliberate way: inquire, hold the whole, refute, then rule. | sitting 373: the search its words chose set aside and no tool run (369's fault mended); FAULT: the Steward described itself, not the covenant, and Manjuel ruled that SUPPORTED after six and a half minutes on gemma4:12b | 590.7 s |
| P4 | court | The review panel: every counsel is heard, then Manjuel rules; its turn may take 900 s. | sitting 366: FAULT, Jesster and Manjuel past their bounds, Neiro's last word; 368: /table ruled with all five | 900 s; 779 s |
| P5 | quick | One seat past the gate, for a throwaway question. | sitting 373: ok, "two plus two" said four; the search its words chose set aside, with no Router to run it | 3.9 s |

### Skills (skills/, 45): what a seat can call

| # | name | what it does | live run | time |
|---|---|---|---|---|
| K1 | classify_sentiment | Classifies one piece of human feedback on three axes at once: Tone, Urgency and Intent. | sitting 370: ok | 61.5 s |
| K2 | decompose_task | Breaks a large objective into an ordered sequence of small, individually checkable steps. | sitting 373: ok, called by its own words ("break this into small checkable steps") | 96.5 s |
| K3 | deep_research | Runs an intensive deep-dive analytical evaluation on a complex subject payload using a specialized reasoning sub-agent. | sitting 370: FAULT, ran, and answered the law-court meaning | 119.1 s |
| K4 | edit_file | Replaces ONE exact passage in a file that is already in the workspace, so a large file can be changed without rewriting it whole. | sitting 373: ok, a write the Router decides: its first call failed on the edit's form, its second changed measure.py | 38.1 s |
| K5 | embed_text | Adds or refreshes a single workspace file in the semantic index immediately, without a full sweep. | sitting 373: called by its own words, and refused the ground file (it embeds a workspace file, as it says); FAULT: the Router then rebuilt the whole index unasked | 291.4 s |
| K6 | extract_facts | Pulls hard facts out of long or dense text - quantities, dates, names, and explicit quotes - and drops everything else. | sitting 373: ok, called by its own words | 53.4 s |
| K7 | git_commit | Stages every change in the ground and commits it locally with a message. | RULED (his card): the saves are his | — |
| K8 | git_cycle | Runs the FULL version-control cycle in one act: refuses to ship on red or stale STROKES or SMOKE, and reports the tag's four other proofs without ... | RULED (his card): the saves and sends are his | — |
| K9 | git_init | Starts version control in this ground if it is not already a repository. | RULED (his card): the repositories stand | — |
| K10 | git_pull | Fast-forwards this ground from its remote. | RULED (his card): main comes down on his card | — |
| K11 | git_push | Sends local commits to the remote. | RULED (his card): the sends are his | — |
| K12 | git_status | Reports the repository state - branch, current commit, whether the ground is clean or dirty, and whether remote operations are permitted. | sitting 366: ok, in the live check | 147.6 s (the turn) |
| K13 | ground_edit | Replaces ONE exact passage in a file that is already in the ground itself — source in manjuel/ or atlas/line/, a test, a doc — on a LINE OF WORK, so ... | RULED (his card): a change to the ground is a piece's | — |
| K14 | ground_list | Lists what is actually in the ground (the Research folder) right now — the total listed, then top-level folders with counts, and files. | sitting 366: ok | 7.4 s |
| K15 | ground_read | Reads one file from the ground (the Research folder) as it is on disk right now — pipelines.md, memory.md, a seat's own file, source in manjuel/. | sitting 366: ok; read in part in 367 and 368 | 9.6 s |
| K16 | ground_report | States where the chain is standing: the ground path, the agent workspace, the active session, and what is resident on the card right now. | sitting 370: ok | 33.2 s |
| K17 | ground_write | Writes one WHOLE file into the ground itself — source in manjuel/ or atlas/line/, a test under tests/, a doc — at a path relative to the ground, on ... | RULED (his card): a change to the ground is a piece's | — |
| K18 | index_ground | Builds or refreshes the semantic index over the configured roots (see index_roots.txt). | sitting 368: ok, through /index | 84.3 s |
| K19 | inspect | Reports the FACTS about a file before anything reads it — size, real type by its first bytes, line terminator, line count, first line, when it was ... | sitting 374: ok, the file the words name, read by the Steward; mended on his card after 373 took the whole sentence as its file | 8.6 s |
| K20 | linear_regression | Fits a trendline through a series of numbers using ordinary least squares and projects the next few steps. | sitting 370: ok | 15.5 s |
| K21 | lint_code | Reads a block of source and reports likely defects - syntax errors, unhandled exceptions, unused imports, off-by-one and resource leaks. | sitting 370: ok, found the bug | 85.4 s |
| K22 | list_directory | Lists all available files currently sitting inside the workspace directory. | sitting 370: ok; its raw output in the answer | 130.1 s |
| K23 | mcp_call | Calls one tool on a LOCAL MCP server this ground declares. | sitting 370: ok, the door's muster | 17.3 s |
| K24 | proved | Reports what the suites last proved and when — the stroke and smoke tallies, whether they are STALE against the current code, any failures with ... | sitting 370: ok; FAULT in 367: not called for the strokes, and the figure was wrong | 28.2 s |
| K25 | rack_list | Reports every model installed on this machine, which of them are currently loaded in VRAM, their sizes, and which are declared by this ground versus ... | sitting 366: ok | 22.6 s |
| K26 | rack_load | Brings a model into VRAM now so the next call to it is instant. | sitting 370: ok, phi4-mini loaded | 48.3 s |
| K27 | rack_pull | Downloads a model that is not yet installed. | RULED (his card): downloads | — |
| K28 | rack_report | Reports the observed state of the rack - models installed, loaded in VRAM, declared by this ground, missing, and the VRAM budget. | sitting 370: ok | 66.2 s |
| K29 | rack_sync | Pulls a current list of models from Ollama and rewrites rack.md - what is installed, what is loaded, what this ground declares, what is declared but ... | sitting 368: ok, through /rack | 1.3 s |
| K30 | rack_unload | Frees VRAM by evicting a loaded model. | sitting 373: ok, called by name; nothing to free | 15.4 s |
| K31 | read_file | Reads the raw text content of a specific file inside the workspace. | sitting 373: ok, asked alone ("read the file measure.py from the workspace") | 17.8 s |
| K32 | remember | Proposes a note to carry into later sessions - a decision, a ruling, a correction, something learned. | sitting 370: ok, a note proposed; dropped on his card | 149.7 s |
| K33 | run_python | Runs ONE Python file from the workspace and reports what it said — the verdict (RAN, FAILED with the exit code, or STOPPED BY THE JAIL), its stdout ... | sitting 373: ok, called when asked; it printed "the measure ran here 4" | 18.5 s |
| K34 | search_transcripts | Searches THE RECORD by meaning - what HAPPENED. | sitting 370: ok | 50.5 s |
| K35 | semantic_search | Searches the indexed ground by meaning rather than keywords, returning the matching passages with their file, location and similarity score. | sitting 373: set aside in quick and estate, where no Router can run it; FAULT: chosen for a sum and for a riddle | 50.0 s (366) |
| K36 | sitting | Resolves a SITTING NUMBER to the runs it held and the transcript path of each one, read from the paid record in SEAT_LOG.md. | sitting 370: ok | 54.5 s |
| K37 | skill_report | Lists every skill the chain can actually execute, with what each one does — read from the loaded library, never generated. | sitting 373: ok, called by its own words, and "list the skills" read by the Steward | 16.1 s; 20.5 s |
| K38 | skill_search | Finds which of this chain's skills bear on a subject, and reports each one's own description in full — read from skills/*.md, never summarised. | sitting 373: ok, called by its own words; on a tie with skill_report, put to him on an amber card | 28.8 s; 112.3 s (the tie) |
| K39 | speak | Read text aloud through the machine's own speech engine. | sitting 370: ok, spoke; slow | 154 s |
| K40 | statistics | Computes n, mean, median, min, max, standard deviation and variance over a series of numbers. | sitting 370: ok | 28.5 s |
| K41 | subtask | Hands ONE scoped piece of work to a fresh run with its own context, and returns only its result. | sitting 370: ok, a fresh run; its answer retold another turn | 253.6 s |
| K42 | symbols | Where a name is DECLARED in this ground, read straight off the disk — file and line for every def, class, func, type or exported binding, in Python, ... | sitting 370: ok | 20.4 s |
| K43 | time_align | Parses loose task lists or historical log entries and aligns them onto an ordered timeline. | sitting 370: ok | 58.9 s |
| K44 | when | Lists what ran in a WINDOW OF TIME, read from the transcript stamps in logs/. | sitting 373: ok, called by its own words | 33.7 s |
| K45 | write_file | Writes text, scripts, or markdown data to a file inside the workspace. | sitting 370: ok, measure.py in the workspace | 39.8 s |

### Commands (the engine's palette, 31, and commands.md's own, 3): typed as /name

| # | name | what it does | live run | time |
|---|---|---|---|---|
| M1 | chat | voice chat: talk, it answers aloud, any key cuts it off | sitting 368: FAULT, heard nothing three times and ended itself | 32.1 s |
| M2 | say | speak deliveries: on, off, or words now | sitting 368: ok, he heard it | 3.1 s |
| M3 | new | drop the conversation thread | sitting 368: ok, the thread dropped | 1.3 s |
| M4 | resume | pick up the previous sitting's thread | sitting 368: "no saved thread to resume", though 367 ran six turns (seen) | 2.0 s |
| M5 | paste | stage source material for the next objective | sittings 368 and 369: ok, the material staged through the council's card | 1.4 s |
| M6 | table | round-table: counsel hears a question, the Court rules | sitting 368: ok, all five sat and Manjuel ruled | 779 s |
| M7 | @<seat> | address one seat directly | sitting 368: ok, @steward answered; its flag word printed under the answer | 2.4 s |
| M8 | last | reprint the previous answer | sitting 368: ok ("no previous run" in a fresh sitting) | 1.9 s |
| M9 | remember | land an entry in memory.md (confirms first) | sitting 368: ok, one line landed on his card (the memory chain 9 links); 370: refused on his card | 1.4 s |
| M10 | memory | review what seats proposed; land or drop | sittings 368 and 370: ok; the seat's proposal dropped on his card | 1.9 s |
| M11 | git | the repository: state, diff, branches, commit, push | sitting 368: ok, the state | 1.9 s |
| M12 | toll | pay this sitting's toll | RULED: paid by /close in sittings 367 to 370 | — |
| M13 | sittings | past sittings | sitting 368: ok | 9.0 s |
| M14 | brief | where the build is and what you said we are on | sitting 368: ok | 5.9 s |
| M15 | status | boot report: ground, rack, record, gate, voice | sitting 367: ok | 4.8 s |
| M16 | index | refresh the semantic index | sitting 368: ok, refreshed with the embedder | 84.3 s |
| M17 | find | search the ground by meaning | sitting 368: ok | 1.4 s |
| M18 | parity | chain against bare calls; hosted asks a hosted head, saying first what leaves | sitting 368: ok, local: 11 scored 0.48 to 0.73, the unsafe one refused; "NOT EVERYTHING RAN read_file" | 19.5 min |
| M19 | models | VRAM plan for this pipeline | sitting 368: ok | 2.0 s |
| M20 | model | one model for all or one seat, or reset | sitting 368: ok, set and reset | 2.0 s |
| M21 | warm | load this pipeline's models now | sitting 368: ok ("already warm") | 2.2 s |
| M22 | rack | resurvey Ollama, rewrite rack.md | sitting 368: ok, rack.md rewritten | 1.3 s |
| M23 | agents | list seats, models, stages | sitting 368: ok | 1.9 s |
| M24 | skills | list skills and binding status | sitting 368: ok | 2.3 s |
| M25 | pipeline | the active running order, spine and rack | sitting 368: ok | 1.9 s |
| M26 | pipelines | all declared pipelines | sitting 368: ok | 1.9 s |
| M27 | use | switch pipeline | sittings 368 and 369: ok, switched and back | 1.6 s |
| M28 | reload | re-read agents/, skills/ and commands.md | sitting 368: ok | 1.9 s |
| M29 | listen | speak one question (superseded by chat) | sitting 368: FAULT, a click, then words he did not say (n on his card) | 10.5 s |
| M30 | help | the palette; a word filters it | sitting 368: ok | 1.5 s |
| M31 | exit | quit | RULED: quits the engine; /close is used | — |
| M32 | morning | his own (commands.md): the morning look-around, repo state, then what changed lately | sitting 368: FAULT, it prints its expansion and nothing runs | 1.9 s |
| M33 | sitting | his own (commands.md): review a sitting from the record, what ran and what it proves | sitting 368: FAULT, it prints its expansion and nothing runs | 1.9 s |
| M34 | covenant | his own (commands.md): cite the covenant from the founding record | sitting 368: FAULT, it prints its expansion and nothing runs | 1.3 s |

## 2. The door's tools (atlas-mcp, 95)

Each is called by the glass (a tab, a button, Registry & Docs' Call) or by the council (mcp_call); a writing call from anything but his glass waits on its card.

| # | name | what it does | live run | time |
|---|---|---|---|---|
| T1 | aider_run | the operator's own Aider, run on the files he names: it copies them into a scratch folder, runs Aider headless on the copies behind a wall (no ... | RULED (his card, 18:03): runs on a line of work; measured the next time a piece uses it | — |
| T2 | aider_status | whether Aider can run in this world now and with what: installed, its version, the coding seat's model and window, whether the rack has the model, ... | glass 17:59: ok, 0.86.2, the coding seat's model, rack up | 142 ms |
| T3 | aider_undo | take one Aider run back: the files it changed are put back as they were, if nothing has changed them since. | RULED (his card, 18:03): as aider_run | — |
| T4 | ask_steward | the weighed ruling with receipts, never raw model output. | glass 18:05: FAULT, refused: "no engine wired for project research" (the door runs without --engine) | 10 ms |
| T5 | auth_key_create | mint a scoped API key; plaintext returns once (N6) | RULED (his card, 18:03): changes who may call | — |
| T6 | auth_key_list | list live keys with hashes withheld (N6) | glass 17:59: ok, 1 live key | 5 ms |
| T7 | auth_key_revoke | fold a key: flagged, kept for audit (N6) | RULED (his card, 18:03): changes who may call | — |
| T8 | auth_key_scope | set which carried tenants a live key carries, the list replaced whole. | RULED (his card, 18:03): changes who may call | — |
| T9 | auth_verify | check a key against a tenant store. | glass 17:59: ok, a made-up key refused ("not a key") | 3 ms |
| T10 | chat_cancel | end an in-flight send; no partial answer is kept (N1) | glass 17:59: ok, nothing in flight, nothing claimed | 4 ms |
| T11 | chat_list | read one session's turns, isolated by session (N1) | glass 17:59: ok | 3 ms |
| T12 | chat_send | ask in a session; whole witnessed answer or refusal (N1) | glass 18:05 (his card): ok, "ready" from llama3.2 | 197 ms |
| T13 | chat_sessions | list opened chat sessions in first-seen order (N1) | glass 17:59: ok, none open then | 5 ms |
| T14 | chat_start | open a chat session with a receipted id (N1) | glass 18:05 (his card): ok, c-20261011-010545-581bf527 | 10 ms |
| T15 | check_the_wall | judge a path before acting; quote the law on refusal | glass 17:59: ok, CLAUDE.md inside the wall | 4 ms |
| T16 | env_close | close the world's sitting properly and reap its engine | sitting 365: ok, closed and tolled at 15:19:52 | not timed |
| T17 | env_list | which worlds have an engine open, and which are being sat in elsewhere | glass 17:59: ok, none open | 6 ms |
| T18 | env_open | open the Manjuel engine inside a world. | sitting 365: ok, opened at 15:15:07 | not timed |
| T19 | file_edit | the operator's own exact edit of one text file in this world: the path, the exact old text and the new text are plain fields; it sets the seats (agents/) and the skills (skills/) too, while no sitting is open | glass 2026-10-12, 08:51 to 11:12: ok, seven skill files and two seats set with no sitting open, then the engine, a stroke and this record, each landed on his Approve, on a red card since the glass of that morning | about 5 s with his click |
| T20 | flow_cancel | end a live run; reached nodes stand (N2) | glass 17:59: ok, a made-up run: nothing live, nothing claimed | 4 ms |
| T21 | flow_compare | two runs side by side, node by node (N2) | glass 17:59: ok, smoke's two runs IDENTICAL | 33 ms |
| T22 | flow_get | read one flow spec version (N2) | glass 17:59: ok, smoke v1 | 5 ms |
| T23 | flow_list | list flows with latest versions, and name any .json under flows/ that cannot be read as one (N2) | glass 17:59: ok, 7 flows, two retired | 8 ms |
| T24 | flow_replay | re-fire a run's spec and inputs under a fresh id (N2) | not run: not chosen on his card (18:03) | — |
| T25 | flow_resume | carry a paused run on with continue/stop (N2) | sitting 371: ok, version-bump's gate continued and coder-tree's stopped, each on his card | 8.3 s (continue); at once (stop) |
| T26 | flow_run | fire a flow; gates pause, evals steer, budget binds (N2) | glass 18:05 (his card): ok, smoke COMPLETE; at 11:4x a fire of the retired coder refused in its own words | 280 ms |
| T27 | flow_runs | list runs for a flow, newest last (N2) | glass 17:59: ok | 11 ms |
| T28 | flow_save | fold a new flow spec version; history kept whole (N2). A gate's grants must name writing tools this door carries; a spec carrying retired (why, in ... | 11:45: ok, coder v14 and version-tag v4 saved, at once with no card (fault 54) | not timed |
| T29 | flow_status | waterfall: nodes, elapsed, budget bar, verdict (N2) | glass 17:59 and 18:05: ok | 11 ms |
| T30 | get_in_line | standing law + line + road + log-tail for a carried project | glass 17:59: ok | 9 ms |
| T31 | git | the world's repository as it stands now: branch, head, dirty counts, upstream, and whether remote operations are walled | glass 17:59: ok, main at f8a4948, clean | 716 ms |
| T32 | git_branch | the lines of work: list them (which one you are on, which is the main line, which have been sent), or open, switch to, land (onto the main line, ... | glass 17:59: ok, list; its writes measured at the next save and send | 318 ms |
| T33 | git_commit | save this world's work: stages everything (or only the files named, one per line) and records it under a message you write | not run in v0.2.6 yet: the saves went through the Bash tab; measured at the next save | — |
| T34 | git_diff | what actually changed: one file's change served whole, or the whole tree's. | glass 17:59: ok, nothing changed | 208 ms |
| T35 | git_pr | pull requests, the one GitHub-side object his ruling of 2026-10-07 let into the door: list a world's open pull requests with their checks as one ... | glass 17:59: ok, list; merge of core 11 on his card (14:17) | 837 ms |
| T36 | git_pull | fetch and catch up, fast-forward only. | not run in v0.2.6 yet: main came down through the Bash tab; measured at the next | — |
| T37 | git_push | send saved work to the remote; refuses by name while the estate's wall is shut, and says so when it binds a branch to origin for the first time | not run in v0.2.6 yet: the sends went through the Bash tab; measured at the next send | — |
| T38 | git_remote | where this world sends: each remote by name, its host, and whether the estate's wall is open | glass 17:59: ok | 135 ms |
| T39 | git_tag | the marks a version is cut at: list them with what GitHub has, cut one at a commit whose declared version it must equal, send one to GitHub by name, ... | glass 17:59: ok, list, asking GitHub; its cut and send at the v0.2.6 cut | 2689 ms |
| T40 | hold_answer | approve or deny one parked call by id. | cards 204 to 207, 18:16 to 18:25: ok, each held run ran with it | 44 to 610 ms |
| T41 | hold_list | the writing calls parked waiting for the operator's hand, and whether holding is armed at all | glass 17:59: ok, armed, none held | 4 ms |
| T42 | law_add | the operator's own hand: set a law -- one numbered entry appended to law/LAW_LEDGER.md, BELOW its seal, as a draft until he seals it. | RULED (his card, 18:03): changes the law | — |
| T43 | law_seal | the operator's own hand: seal the ledger as far as it is written (law.py seal on law/LAW_LEDGER.md) -- what is below the seal becomes law and is ... | RULED (his card, 18:03): changes the law | — |
| T44 | law_status | the laws as the chain holds them: every law file, how far it is sealed, what is draft below the ledger's seal, and the chain's own verdict (law.py ... | glass 17:59: ok, the chain proves whole, 10 links | 146 ms |
| T45 | list_doctrine | carried doctrine by name, read-only. | glass 17:59: ok, 1 document | 5 ms |
| T46 | memory | cited answers from local memory, or refusal (F1-01) | glass 17:59: ok, refused with no cited memory ("never invented") | 4 ms |
| T47 | mesh_chain | rewalk every pen plus the head: EMPTY/INTACT/FLIP/TAMPER/FORGERY (B2) | glass 17:59: ok, INTACT, head EMPTY | 3 ms |
| T48 | mesh_cite | cite chain hashes by a signed cite entry (B2) | glass 18:04 (his card): FAULT, its schema names targets but the code reads cites; with cites, an actor not enrolled refused | 8 ms |
| T49 | mesh_enroll | bind a mesh voice: actor -> verifying key (B2) | RULED (his card, 18:03): changes who may post | — |
| T50 | mesh_post | post one signed message on the channel chain (B2) | RULED (his card, 18:03): needs an enrolled actor | — |
| T51 | mesh_read | read the channel-head index or one actor's chain (B2) | glass 17:59: ok, nothing yet | 4 ms |
| T52 | muster | declared projects roll call | glass 17:59: ok, 2 carried | 9 ms |
| T53 | projects | what the maker made: every project under projects/ with its versions read from its own history, or one project's page as it stands (or as a version ... | glass 17:59: ok, 13 projects | 963 ms |
| T54 | prompt_compare | run two versions over the same input, diff honestly (N4) | glass 18:05 (his card): FAULT, versions given as the strings it declares compared v2 with v2, silently; as numbers v1 against v2, IDENTICAL | 7588 ms |
| T55 | prompt_eval | score a prompt over a dataset, exact-match (N4) | not run: wants evals/<name>.json and research has no evals/ (a folder is his to make) | — |
| T56 | prompt_get | read one prompt version with receipt (N4) | glass 17:59: ok, an unknown name refused | 4 ms |
| T57 | prompt_list | list prompts with latest versions (N4) | glass 17:59: ok | 4 ms |
| T58 | prompt_run | render a prompt and measure one answer (N4) | glass 18:05 (his card): ok, measure-ready v2 "ready", the load included | 13927 ms |
| T59 | prompt_save | fold a new prompt version; history kept whole (N4) | glass 18:04 (his card): ok, measure-ready v1 and v2 | 21 ms |
| T60 | proofs | what this world has PROVED, from its own record: the suites' stamp, every live standup, the parity history | glass 17:59: ok | 43 ms |
| T61 | rack_ask | routed ask, witnessed to the ledger (F1) | glass 18:05 (his card): ok, llama3.2 "ready", witnessed to the rack ledger | 332 ms |
| T62 | rack_list | live tier ladder of lawful local voices (F1) | glass 17:59: ok, 11 voices | 26 ms |
| T63 | rack_open | expanded context bundle at a depth (F1) | glass 17:59: ok | 43 ms |
| T64 | rack_plan | VRAM fit check for a model set before it runs (N3) | glass 17:59: ok, every model asked: OVER, 97 of 15 GB | 21 ms |
| T65 | rack_pull | pull a model into the loopback rack behind confirm (N3) | RULED (his card, 18:03): downloads | — |
| T66 | rack_sync | re-list the loopback rack with a sync receipt (N3) | glass 17:59: ok | 25 ms |
| T67 | rack_warm | verify a voice is present and report its footprint (N3) | glass 17:59: ok, llama3.2 footprint 4.34 GB | 31 ms |
| T68 | read_doctrine | one document whole with sha256 receipt. | glass 17:59: ok, README.md with its sha256 | 5 ms |
| T69 | read_handoffs | SEAT_LOG (or the manifest 'log' path) whole, with sha256 receipt(s) | glass 17:59: ok, SEAT_LOG whole with its sha256 | 70 ms |
| T70 | read_plan | HLD/LLD/road documents by name; absent name denied honestly | glass 17:59: FAULT, in research all five plan names map to atlas's documents and none reads; in atlas, road ok (23 ms) | 5 ms |
| T71 | records | the estate's own documents sorted by what they are (doctrine, record, spec, agents, commands, skills, logs). | glass 17:59: ok, 153 documents | 17 ms |
| T72 | release_step | one of the release's own steps, run by the core's tests/cut.py in this world: bump the pins, atlas's version files and both changelogs to a mark. | measured at the v0.2.6 cut (step 4) | — |
| T73 | remember | sole write tool; testimony stamped generated; staged for operator ascend | glass 18:04 (his card): ok, staged for his ascend | 6 ms |
| T74 | run_answer | answer what the run asked; the gate crossing the wire, never a default | sittings 368 to 370: ok, each council question answered on his cards (the paste, /listen, /remember, /memory) | about 1 s each |
| T75 | run_cancel | interrupt the turn in flight; the sitting stays open | glass 17:59: ok, refused with no engine open | 3 ms |
| T76 | run_start | run one objective through the council. | sitting 365: ok, one turn delivered | 234 s |
| T77 | seat_ask | @seat single-seat ask; model is a measurement (N4) | glass 18:05 (his card): FAULT, refuses every seat in research as not declared, its own example "@manjuel" included | 5 ms |
| T78 | seats | the world's own seat declarations and the pipelines they stand in, from agents/ and pipelines.md | glass 17:59: ok, 14 seats | 8 ms |
| T79 | shell_run | the operator's own typed shell, run in this world: a Git Bash command or a Python entry (Python keeps its names between entries). | holds 202 to 208, 17:38 to 18:30: ok, a commit and push, the versions, a line opened | 41 ms to 4.3 s |
| T80 | standup_run | run the estate's live standup in this world -- the morning set (default), the court, or all -- and hand back its tally and report. | sitting 366: ok, the live check with the review panel, 9 of 10 met (the court missed) | 1157 s |
| T81 | state_matrix | state = fold(record) index of the named project | glass 17:59: ok; road and state absent (read_plan's map) | 7 ms |
| T82 | suite_run | run the estate's own suites in this world -- the strokes, the smoke, or both (default) -- one after the other with the python the door runs the ... | the glass, 2026-10-12 07:21, drawn as it ran (a `door>` entry in the terminal, a running row in the Run tab's Door calls): ok, 3772 of 3772 and 72 of 72 | 237 s |
| T83 | team_history | read the bridge record, filtered, newest last (N5) | glass 17:59: ok, nothing yet | 5 ms |
| T84 | team_ingest | verify + store one inbound platform envelope (N5) | not run: not chosen on his card (18:03) | — |
| T85 | team_send | send one guarded message to discord/slack/whatsapp (N5) | RULED (his card, 18:03): leaves the machine | — |
| T86 | team_status | platform presence + last sends, never secrets (N5) | glass 17:59: ok, all three disconnected | 3 ms |
| T87 | tenant_list | list all registered tenants and their roles | glass 17:59: ok | 4 ms |
| T88 | tenant_rbac_assign | assign a role to an agent in a tenant's RBAC policy | RULED (his card, 18:03): changes who may call | — |
| T89 | tenant_rbac_check | check if an agent has permission for a tool under a tenant's RBAC policy | glass 17:59: ok, allowed in open mode | 6 ms |
| T90 | tenant_trust | grant or revoke cross-tenant trust (delegation of specific tools) | RULED (his card, 18:03): changes who may call | — |
| T91 | tenant_trust_list | read recorded cross-tenant delegations (N6) | glass 17:59: ok, none recorded | 4 ms |
| T92 | town_beat | run one town scheduling cycle on this ground (N2) | glass 18:04 (his card): ok, 0 issued | 9 ms |
| T93 | town_status | read the board: tasks, worked set, open orders (N2) | glass 17:59: ok, 0 tasks | 4 ms |
| T94 | us_to_vc | convert a .us declaration to a W3C Verifiable Credential | glass 17:59: ok, seat_steward.us as a credential | 4 ms |
| T95 | verify_chain | chain verdict via tools/chain_verify.py, the Python spine: EMPTY/INTACT/FLIP/TAMPER (SKIPPED where rows carry no hash) | glass 17:59: FAULT, FLIP on all 10 links of law/chain.jsonl, where law_status proves the chain whole | 144 ms |

## 3. The glass (atlas-webapp)

### The terminal's tabs (5)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| G1 | Agent | the council: a line typed here is a turn; boot, close and the gate are here too; its questions come as cards colored by what they are for -- amber to pick a tool, green to wake a seat -- and an edit or a command waits on a red one | sittings 373 and 374: ok, 20 asks with /boot, /use and /close around them; an amber card on a tie, a green card for each of four racked seats, each answered on his click | under 1 s; a card waits on him |
| G2 | Bash | Git Bash as you; a plain look runs at once, anything that writes waits on its card | the glass all day: ok, a plain look at once, a write on its card (holds 202 to 208); git --version parked as a write (card 204): the gate reads it as an option that moves git | 67 ms to 4.3 s |
| G3 | Python | one Python session per world that keeps its names; the rest waits on its card | card 205, 18:25: ok, 3.14.7 | 41 ms |
| G4 | PowerShell | PowerShell 7 as you; every line waits on its card, up to 300 s | card 206, 18:25: ok, 7.6.6 | 603 ms |
| G5 | Aider | Aider edits the files you name, on a line of work, with the coding seat's model | RULED (his card): runs on a line of work; measured the next time a piece uses it | — |

### The Inspector's tabs (10): every other page's address opens one of these

| # | name | what it does | live run | time |
|---|---|---|---|---|
| G6 | Run | the last turn: its stages and seats, the floor (each seat's own words), the tool calls and the wire; Door calls, every call the glass makes as it goes and comes back, with how many it keeps of how many were made; and the Projects card | glass 2026-10-12, 07:50 to 07:56: ok after a mend on his card -- its count read "300 since this page opened" with 604 made; seen after it: "the newest 5 of 17 since this page opened", the page's keep at 5 for that check; the suites' run among its rows; the Projects card | 657 ms |
| G7 | What's left | WHATS_LEFT.md, counted, searchable, read again in place | glass 18:13: ok, 26 open | 158 ms |
| G8 | Aider Pair | Aider's state, the files in the chat, the recent runs and their Undo | glass 18:13: ok, installed, no files in the chat | 155 ms |
| G9 | GitHub | each world's repository: save, send, take, lines of work, marks, pull requests; every change in a world | glass 18:13: ok, both repositories | 156 ms |
| G10 | Audit Ledger | what the build has proved, the live check, the engine's report, the estate, the evals scored by hand, the transcripts; drawn again when the suites or the live check end | glass 2026-10-12 07:51: ok, the suites (07:25, 3772 of 3772 and 72 of 72, drawn again on its own when they ended) and the live check 9 of 10 (2026-10-10 19:01), its three reads back | 20 ms |
| G11 | Workflows | the flow builder: the flows, a flow's steps and edges, Save, Fire, the gates, the runs waiting on him | glass 18:13: ok, the 7 flows, two retired | 155 ms |
| G12 | Laws | every law and how far the chain seals it; a law set as a draft; the ledger sealed | glass 18:13: ok, the chain proves whole | 315 ms |
| G13 | Settings | the door's address, the evals pass mark, the messaging bridge | glass 18:13: ok, the door's address | 161 ms |
| G14 | Registry & Docs | the door's tools with Call, the seats with their files and prompts, the documents by kind | glass 18:13: ok, the 95 tools with Call | 156 ms |
| G15 | Rack | the local voices on the rack, by tier | glass 18:13: ok, 11 voices in 3 tiers | 155 ms |

### The front page's parts, and the pages still standing (10)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| G16 | the bar | the doors, the status line (door, engine, rack), Pages, the Inspector, who is signed in, Lock | glass 18:14: ok, no engine, Pages, the Inspector, who is signed in | drawn |
| G17 | the dock | every card waiting for his hand, pinned at the foot of the terminal, in every tab | holds 200 to 210: ok, every card pinned there and answered there | — |
| G18 | the play frame | the page the maker made, played beside the terminal | glass 18:15: ok, countdown-timer-2 played beside the terminal, sandboxed by its own policy (the glass cannot reach into it), then put away | 188 ms |
| G19 | the mic | local whisper: speech into the line, nothing sent on his behalf | glass 20:47: FAULT, "heard nothing — is the right input device selected?" (his word: not working for now) | — |
| G20 | the hints and history | Try: lines per tab; the arrow keys walk what was typed | glass 18:14: ok, the Try: lines drawn; the up arrow brought back the last command | at once |
| G21 | the palette | Ctrl K: every page and act by name | glass 18:14: ok, Ctrl K opens it with Boot and eleven pages; Esc closes it | under 1 s |
| G22 | the lock | the PIN at the door of the glass, and Lock | RULED: not pressed; unlocking takes his PIN | — |
| G23 | Trace Log | every tool call the glass made, one opened whole, and an eval scored by hand on it | RULED from its data (his card): the traces answer, the newest 100; FAULT: nothing on the front page links to it (not Pages, not the palette) | — |
| G24 | Messages | the team bridge: what crossed, with receipts, and a guarded send | RULED from its data (his card): the bridge answers (team_status, team_history); FAULT: nothing on the front page links to it | — |
| G25 | Playground | versioned prompts, a single seat asked, honest compares and evals | RULED from its data (his card): the prompts answer (measure-ready v1 and v2); FAULT: nothing on the front page links to it | — |

## 4. Flows, the rack and the outside parts

### Flows (flows/, 7)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| F1 | coder (v14) | the coder on a change, with send-backs; 5 nodes, budget 1800 s; RETIRED: superseded by coder-tree | 11:4x, on his card: ok, a fire refused as retired, in its own words | — |
| F2 | coder-tree (v5) | the coder on the harness itself, on a line of work, behind his gate; 11 nodes, budget 3600 s | sitting 371: stopped at its first gate on his card; FAULT: the brief named tests/HANDOFF.md and a different change | 9.7 s (the brief) |
| F3 | release (v5) | a version's cut, through pull requests, inside his three gates; 44 nodes, budget 14400 s | measured at the v0.2.6 cut (step 4) | — |
| F4 | smoke (v1) | the smallest flow: proves the engine runs one; 2 nodes, budget 300 s | glass 18:05 (his card): ok, COMPLETE, f-20261011-010546-275e214e | 200 ms |
| F5 | version-bump (v1) | moves the version pins; 3 nodes, budget 900 s | sitting 371: ok, COMPLETE: 0.2.5 read, his gate continued, re-read; a first fire was cancelled under his /chat | 51.6 s |
| F6 | version-tag (v4) | cut and send a mark; 8 nodes, budget 900 s; RETIRED: superseded by the release flow | RULED: retired at 11:45, superseded by the release flow; not fired | — |
| F7 | wife-test (v1) | her three lines, as a flow; 5 nodes, budget 900 s | sitting 371: ok, COMPLETE: the game made, "a game I can play", the thanks | 100.9 s |

### The rack's models (Ollama, 11)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| R1 | llama3.2:latest | 2.0GB, llama family | glass 18:05: ok, "ready" through prompt_run, rack_ask, chat_send and smoke | 0.2 s; 13.9 s with its load |
| R2 | nomic-embed-text-v2-moe:latest | 1.0GB, nomic-bert-moe family | sittings 366 to 370: ok, every search and /index (1816 documents) | 84.3 s (/index) |
| R3 | phi4-mini:latest | 2.5GB, phi3 family | sittings 369 and 370: ok, the Delivery Agent and rack_load | 48.3 s (rack_load) |
| R4 | deepseek-r1:8b | 5.2GB, qwen3 family | sitting 368: ok, Jesster in /table and /parity's judgement case; FAULT in 366: past 600 s | 167.5 s (/parity) |
| R5 | gemma4:12b | 7.6GB, gemma4 family | sitting 368: ok, Manjuel ruled /table; FAULT in 366: past its bound | 779 s (the table) |
| R6 | qwen2.5-coder:7b | 4.7GB, qwen2 family | glass 18:10 (rack_ask, his card): ok, "ready" | 13.0 s with its load |
| R7 | qwen3-vl:8b | 6.1GB, qwen3vl family | glass 18:11 (rack_ask, his card): ok, "ready", the slowest | 75.6 s with its load |
| R8 | qwen3.5:4b | 3.4GB, qwen35 family | sittings 366 to 370: ok, the Router and the Quality Evaluator; slow | up to 300 s |
| R9 | qwen3.5:9b | 6.6GB, qwen35 family | sitting 370: ok, the Deep Researcher; /parity's thinking cases | 119.1 s |
| R10 | gemma4:e4b | 9.6GB, gemma4 family | glass 18:12 (rack_ask, his card): ok, "ready" | 21.2 s with its load |
| R11 | qwen2.5-coder:14b | 9.0GB, qwen2 family | sitting 367: ok, the Expert Coder made the timer page; /parity's code case | 46.4 s |

### Outside parts (8)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| O1 | Ollama | the rack itself, on 127.0.0.1:11434 | glass 17:59: ok, answers on 127.0.0.1:11434 (rack_list; rack_ask from llama3.2 at 18:05) | 26 ms, an ask 332 ms |
| O2 | whisper.cpp | speech in: bin/whisper-cli.exe and its model | sitting 368: FAULT, /listen transcribed a click, then words he did not say | 10.5 s |
| O3 | Windows SAPI | speech out | sitting 368: ok, /say heard by him; speak in 370 | 3.1 s |
| O4 | Aider 0.86.2 | the pair programmer, in aider/venv (a Python 3.11) | glass 17:59: ok, aider_status reads 0.86.2 with the coding seat's model; a run is ruled for now (his card) | 142 ms |
| O5 | git | both repositories, through the door | card 204, 18:16: ok, git version 2.55.0.windows.5 | 83 ms |
| O6 | gh | the GitHub CLI the door's pull requests go through | holds 194 and 195, 17:25: ok, the failed run's log of pull request 14 read | 7.1 s |
| O7 | Python | the engine (manjuel.py) | card 205, 18:25: ok, 3.14.7 in the Python tab; the suites ran on it at 17:36 | 41 ms |
| O8 | the Rust spine | atlas.exe: every atlas trade, and the proof legs that need it | card 207, 18:25: ok, atlas/target/debug/atlas.exe --help lists its commands | 259 ms |
