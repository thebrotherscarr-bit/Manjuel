# INVENTORY

**THE BOOK, PART IV: EVERY PART.** Parts I to III (README, QUICKSTART, RUNBOOK) say what the system is and how it is driven.
This part is the reference: sections 1 to 4 below list every part one line each, with its last live run and its time; section 5,
"Every part, in full", gives each one a card in the doctrine's own form (foundation/doctrine/S6_THE_FIELD_OPS_SKILLS.md) --
AUTHOR (what it is and why), USE (the exact call, every argument, an example), CARE (what it reads and writes, whether it waits
on his card, every refusal in its own words), MAINTENANCE (where it lives), TIME (only what was measured), USES (when to reach
for it, and when not) -- deep enough that the part could be rebuilt from its card. Section 5 was read off the code on
2026-10-16, every file in full; where a card says "as it stands", that is what the code does today, faults included.

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
| S3 | Expert Coder | qwen2.5-coder:14b · stage transform · wakes on technical · racked, summoned by its flag | sitting 377: ok, woken on his card after the Router's lint_code and handed its package; its fix was the delivery as written -- the file named, the code, "saved in the workspace" from the record -- and the Quality Evaluator passed it | 36.6 s (its sitting); 377.7 s (the turn, his card in it) |
| S4 | Jesster | deepseek-r1:8b · stage gate · stands in estate, court | sitting 368: ok, counsel in /table (drifted 0.537); 369 estate; FAULT in 366: past its 600 s bound in the court | 779 s (the table) |
| S5 | Judge | gemma4:12b · stage gate · stands in estate, court | sitting 368: ok, ruled /table (drifted 0.541); ruled estate in 369; FAULT in 366: past its bound in the court | 779 s (the table) |
| S6 | Morning Reviewer | llama3.2:latest · stage transform · stands in brief | sitting 369: ok, compressed the feed for the brief | 54.8 s (the brief) |
| S7 | Neiro | llama3.2:latest · stage transform · stands in estate, court | sittings 366, 368 and 369: ok, counsel in the court, the table and estate | 399 to 900 s (the turns) |
| S8 | Proofreader | phi4-mini:latest · stage transform · wakes on prose · racked, summoned by its flag | sitting 373: woken on his word at a green card ("proofread this sentence" raised prose); FAULT: it mended "too" and kept "their" for "they're" | 134.8 s (the turn, with his card) |
| S9 | Quality Evaluator | qwen3.5:4b · stage gate · wakes on drifted, review · racked, summoned by its flag | sitting 377: ok, woken on review after the Expert Coder's file landed and passed it, on the second turn of its ruling loop; cut at its 700 tokens | 18.1 s (its sitting) |
| S10 | Quartermaster | llama3.2:latest · stage transform · wakes on rack · racked, summoned by its flag | sitting 373: ok, "give me the rack report" raised rack and a green card asked him; woken on his word, and rack_report answered | 51.6 s (the turn, with his card) |
| S11 | Reasoner | qwen3.5:9b · stage transform · wakes on hard · racked, summoned by its flag | sitting 377: ok, woken on his card; its two paragraphs were the delivery as written, the closing Steward not seated; cut at its 1400 tokens, its visible answer whole | 360.1 s (the turn, his card in it) |
| S12 | Router | qwen3.5:4b · stage route · when needs_tool · stands in default, court | sitting 375: ok, told which seat waits behind it and its ways up read from the seat files; named no task in any of the three turns that asked it (the fallback held); ran skill_search three times on one ask | 31.2 to 378.9 s (the turns) |
| S13 | Security Guardian | llama3.2:latest · stage guard · wakes on has_feed, suspicious · stands in brief, estate, court, quick | sittings 366 to 370: ok, SAFE wherever it sat; the three gates refused at once | at once at the gates |
| S14 | Steward | llama3.2:latest · stage transform · stands in default, estate, quick | sitting 377: ok, its closing answer written from this turn alone (no conversation, story or standing in its prompt), and not seated after a big seat; at the front it kept the conversation and answered the follow-up, 45 files; FAULT: at the front it narrated a flag it raised, the flag stripped ("I raise `` to enable the chain") | 8.6 s (the follow-up at the door); 46.7 s (a tool turn) |

### Pipelines (pipelines.md, 5)

| # | name | what it does | live run | time |
|---|---|---|---|---|
| P1 | default | The everyday turn: the Steward answers first and closes from this turn alone; tools, code and documents go through the seats between, and a big seat's answer is the delivery as written; each turn is tagged by its level, which may bring the Router or a big seat | sitting 377: ok, the Reasoner's and the Expert Coder's answers delivered as written, a tool turn closed from this turn alone, a follow-up answered at the door; FAULT: the Router wrote the fix itself before the Expert Coder sat | 8.6 to 377.7 s |
| P2 | brief | For a pasted feed: the Morning Reviewer compresses it, and it is delivered as a written briefing. | sitting 369: ok, the feed briefed by four seats | 54.8 s |
| P3 | estate | Every seat runs, the deliberate way: inquire, hold the whole, refute, then rule. | sitting 373: the search its words chose set aside and no tool run (369's fault mended); FAULT: the Steward described itself, not the covenant, and Manjuel ruled that SUPPORTED after six and a half minutes on gemma4:12b | 590.7 s |
| P4 | court | The review panel: every counsel is heard, then the Judge rules; its turn may take 900 s. | sitting 366: FAULT, Jesster and Manjuel past their bounds, Neiro's last word; 368: /table ruled with all five | 900 s; 779 s |
| P5 | quick | One seat past the gate, for a throwaway question. | sitting 373: ok, "two plus two" said four; the search its words chose set aside, with no Router to run it | 3.9 s |

### Skills (skills/, 46): what a seat can call

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
| K46 | use_record | The engine's own after-tool hook: one line per use in logs/uses.jsonl (the tool, whether it answered, how long, who called), which skill_report weighs. Never called by name. | not run live yet (built 2026-10-19, WHAT'S LEFT H32) | -- |
| K47 | triage_binary | What a file IS, read off its bytes alone: its type by its first bytes (ELF, PE, Mach-O, WASM, ZIP and its kin, PDF...), its entropy overall and per 4 KB (packed or encrypted), its strings by kind; a secret-looking string is counted, never printed. From his REA Studio. | not run live yet (built 2026-10-21, the harness study) | -- |

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

### Steward, the driver, and the plain door call (manjuel/serve.py, added 2026-10-16): typed in the glass's Agent tab

| # | name | what it does | live run | time |
|---|---|---|---|---|
| D1 | /drive <goal> \| check: <command> | one job, worked through the tools until the check passes; every write on his card; then the send on his cards | 2026-10-16, sitting 401: ok, C71 done by Steward on its own code (logs/2026-10-16_193305_drive.md); sitting 403: NOT DONE, LAUNCH_PLAN 4 in plain words, the budget spent reading (logs/2026-10-16_210001_drive.md) | 717.5 s; the budget |
| D2 | /drive plan <goal> \| check: <command> | the goal broken into 2 to 8 items, each its own job, then the whole checked | not run live yet (its strokes only) | — |
| D3 | /drive each <command> \| do: <prompt> \| check: <command> | one job per item the command lists; done only when the check passes and the command no longer lists it | 2026-10-16: ok, 3 items (logs/2026-10-16_143318_drive.md) | 62.5 s |
| D4 | /drive tidy | every branch merged into main deleted, here and on GitHub, both repositories, on one card | 2026-10-16: ok, three runs, the last closing drive-1016-201509 | 90.5 s, 12.7 s, 6.9 s |
| D5 | /drive ship <message> [\| check: <command>] | the work on disk saved on a line, sent, a pull request opened or reused, CI waited on, merged on his card | 2026-10-16: ok, pull requests 28 to 33 (the last, 33, in sitting 403) | 776.7 s to 1973.1 s |
| D6 | mcp_call atlas <tool> {json} | a door call said plainly: one line before, the wait on his card if the door holds it, one line after; no seat | 2026-10-16, sitting 403: ok, git_branch switch and git_pull on his cards | 6.4 to 8.4 s plus his click |

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
| T33 | git_commit | save this world's work: stages everything (or only the files named, one per line) and records it under a message you write | 2026-10-14, sitting 381: ok, held for his card and run through the council's door call, atlas's line `streaming` saved (`96f1dd8`) | not timed |
| T34 | git_diff | what actually changed: one file's change served whole, or the whole tree's. | glass 17:59: ok, nothing changed | 208 ms |
| T35 | git_pr | pull requests, the one GitHub-side object his ruling of 2026-10-07 let into the door: list a world's open pull requests with their checks as one ... | glass 17:59: ok, list; merge of core 11 on his card (14:17) | 837 ms |
| T36 | git_pull | fetch and catch up, fast-forward only. | 2026-10-16, sittings 402 and 403: ok, a plain door call held for his card, main brought down after pull request 33 | 6.4 to 8.4 s with his click |
| T37 | git_push | send saved work to the remote; refuses by name while the estate's wall is shut, and says so when it binds a branch to origin for the first time | 2026-10-14, sitting 381: ok, held for his card, both repositories' `streaming` sent for the first time, the upstream set and said | not timed |
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
| T82 | suite_run | run the estate's own suites in this world -- the strokes, the smoke, or both (default) -- one after the other with the python the door runs the ... | the glass, 2026-10-12 07:21, drawn as it ran (a `door>` entry in the terminal, a running row in the Run tab's Door calls): ok, 3772 of 3772 and 72 of 72; 2026-10-16: asked through the engine, the strokes ran past its 295 s wait (sittings 384 to 396) until C71 read them back off their own stamp | 237 s (both); the strokes about 313 s |
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

---

## 5. Every part, in full

Read off the code on 2026-10-16, every file named read whole. File references are written file:line. "As it stands" marks
what the code does today where that differs from what its own words say.

### 5.1 The engine's skills: what every skill shares

**A skill is one file in skills/ and, unless it is a prompt skill, one handler in manjuel/skills.py.** The loader (skills.py:4641-4684)
reads these lines of each skills/*.md:

    **Action Keyword:**    the skill's name (a file without one is skipped, with a warning)
    **Model Target:**      a model: makes it a PROMPT SKILL, run by a model with the file as its rules and no Python
                           (a bare name gets ":latest")
    **Description:**       what it does: the text the model is shown
    **Parameters Needed:** <filepath>...</filepath>, <content>...</content>: the tags are the arguments it declares, and
                           the words between the tags are each argument's description
    **Path Args:**         arg -> workspace|ground: an argument that is a PATH, and the jail it must stay inside
    **Says:**              the phrases that name it (split on , | or newline; one over 45 characters, or ending in ".",
                           is warned of)
    **Takes:**             words | words -> content|filepath: words that fill an argument without a model
    **Hooks:**             before_tool | after_tool (none is declared today, so the hook machinery never runs)

At start the library checks itself (skills.py:4686-4722): a file with neither a handler nor a Model Target is an ERROR; a
handler with no file, and an unknown hook point, are warnings. `/skills` shows them (+ bound, ! fault).

**What a model is shown of a skill.** The pipeline's Router sees `summary` (the description to 112 characters, the arguments to
80; skills.py:407-427) and a shortlist (the six best matches at 300 characters, then every other name; skills.py:4737-4793).
Steward, the driver, sees `tool_schemas` (skills.py:4806-4885): the description, whitespace collapsed, to 400 characters; one
property per declared argument (Path Args, Takes and the Parameters Needed tags), each described by the author's words to 200
characters, or, with none, "the path this skill acts on, relative to the <jail>" / "the <arg> this skill acts on"; `required` is
always empty. As it stands, ten skills' descriptions are cut mid-sentence at 400 for the driver: edit_file, ground_edit,
ground_write, inspect, mcp_call, proved, run_python, search_transcripts, symbols, when.

**How a call is read from a model's reply** (skills.py:5093-5146): `<action>name</action>`, `<filepath>...</filepath>` and
`<content>...</content>` (content runs to the LAST `</content>`). With no `<action>`, JSON of the form `{"name"|"function":
name, "parameters"|"arguments": {...}}`, of which only filepath and content are kept. Steward's calls arrive as tool calls with
the same two arguments. Every handler is `_<name>(env, args) -> str`, registered with `@skill("name")` (skills.py:345-352).

**The order of checks on every call** (SkillLibrary.execute and _call, skills.py:4951-5031):

1. Hooks (none declared: straight through).
2. Counsel mode (`env.review_only`, the court and the table): a skill not in REVIEW_ONLY_SKILLS is refused -- "Refused: the
   table reviews; it does not act. {why} Reading skills available: {...}.", {why} being "'{name}' changes things, and counsel
   has eyes, not hands." for a writer, else "'{name}' is not cleared for the table."
3. Clearance (`env.caller_allowed`, a seat's May Call, or the driver's offered set): "Refused: {who} is not cleared to call
   '{name}'. Cleared: {...}. Hand it to a seat that is."
4. The path gate (gate_paths, skills.py:655-730), only on Path Args that are not empty:
   - three or more words with no "/", "\" or ".": "Refused: `{arg}` must be a PATH, and {raw!r} is a description of one.
     Name the folder or file itself — `agents`, `manjuel/intent.py`, `pipelines.md` — or leave it empty to take the default.
     Nothing was run." (As it stands this also refuses ground_read's SECTION NAME when it has three words or more --
     "drive (lines 1376-1420)" -- and its advice is wrong for that field.)
   - "Refused [LAW 8]: '{name}' declares an unknown jail {jail!r} for <{arg}>. Known jails: workspace, ground."
   - "Refused [LAW 8]: <{arg}> '{raw}' is an absolute path, and so is outside the {jail}. Give a path relative to it. Nothing was done."
   - "Refused [LAW 8]: <{arg}> '{raw}' could not be resolved ({T}: {exc}), so it cannot be shown to be inside the {jail}. Nothing was done."
   - "Refused [LAW 8]: <{arg}> '{raw}' resolves outside the {jail}. Nothing was done."
   - in the ground only: "Refused [ESTATE LAW 2]: <{arg}> '{raw}' is under {worlds/|a vault/}, another world's, closed until the
     operator points at it (ESTATE LAW 2, SITTING LAW 2). Nothing was done."
5. A prompt skill goes to its runner (below) and returns from there -- so, as it stands, the skill bound in step 7 never
   covers a prompt skill.
6. An unknown name: "Error: '{name}' is not a known skill. Available: {...}"
7. The handler runs in a thread, waited on for MANJUEL_SKILL_TIMEOUT (300 s): past it, "Refused: '{name}' did not finish
   within {N}s and the run has stopped waiting (LAW 7: bounded everything). It may still be running behind this. Nothing it
   did is reported here. Raise the bound with MANJUEL_SKILL_TIMEOUT if this skill is legitimately slow." (Python cannot kill
   the thread; it keeps running.) A handler that raises: "Skill '{name}' raised {T}: {exc}".

**The prompt-skill runner** (skills.py:5034-5086), shared by classify_sentiment, decompose_task, extract_facts, lint_code and
time_align: the payload is content, else filepath (as literal text: no file is opened), else the request. With none: "Error:
{name} needs a <content> payload." When the payload came from the request and is under eight words: "Error: {name} was given
no material -- only the order {payload!r}. Paste the text into <content>, or name a file in the workspace with <filepath>."
The model is seated as Agent(name, Model Target, stage "transform"); its system prompt is the whole skill file plus "\n\nFollow
the rules above exactly. Output only what they ask for: no preamble, no sign-off, no conversational filler."; the user turn is
the "## Now" block (the date and hour) and the payload. A failure: "{name} failed: {exc}".

**The sets, and what membership changes:**

    REVIEW_ONLY_SKILLS (skills.py:454-471)   semantic_search, search_transcripts, ground_read, ground_list, ground_report,
        read_file, list_directory, git_status, rack_list, skill_report, extract_facts, classify_sentiment, statistics,
        sitting, when, skill_search, symbols, proved, inspect. Callable in counsel; offered to the driver; set aside when a
        request is about writing; the words after the name become content with no Router; counts as a read for the
        "you quoted a file nobody read" check.
    WRITING_SKILLS (skills.py:477-495)       write_file, remember, embed_text, git_commit, git_init, git_cycle,
        index_ground, rack_sync, git_pull, git_push, edit_file, ground_write, ground_edit. In /drive each asks his card first
        (run_python and mcp_call are asked the same way); never decided without the Router; the manifest check holds each
        to its record's `writes`.
    MESSAGE_IS_THE_OPERATORS (skills.py:509) git_commit, git_cycle: a message he puts in quotes becomes content, and a
        world named beside it filepath, with no Router.
    DRIVE_NEVER (serve.py:537-539)           never offered to the driver: git_commit, git_cycle, git_push, git_pull,
        git_init, remember, rack_sync, rack_load, rack_unload, rack_pull, index_ground, embed_text, speak.
    DRIVE_HANDS (serve.py:541-542)           offered to the driver, each on his card: ground_write, ground_edit, write_file,
        edit_file, run_python, mcp_call.
    REMOTE_SKILLS (us.py:45)                 git_pull, git_push, rack_pull (the manifest check only; as it stands git_cycle,
        which pushes, is missing from it).
    Skills with no arguments are decided with no Router unless they write: git_status, proved, ground_report,
    skill_report, list_directory, rack_list.

**The dials skills read:** MANJUEL_SKILL_TIMEOUT 300; MANJUEL_RUN_TIMEOUT 60; MANJUEL_GIT_REMOTE off (1, true, yes, on);
MANJUEL_RACK_PULL off; MANJUEL_MCP_<NAME> and MANJUEL_MCP_<NAME>_KEY; MANJUEL_VRAM_GB 15; MANJUEL_LOG_HORIZON_DAYS 45. Git
reads wait 5 s and git writes 60 s (gitstate.py:44, 186). As it stands, several skills run `git status --porcelain`
(git_status, git_commit, git_cycle, ground_write, ground_edit, through gitstate.read).

### 5.2 The engine's skills, one card each (alphabetical)

#### classify_sentiment (skills/sentiment_classifier.md; prompt skill, phi4-mini)
- **AUTHOR** "Classifies one piece of human feedback on three axes at once: Tone, Urgency and Intent." For tagging inbound text.
- **USE** content = the single message. It answers exactly four lines: `TONE: Positive|Neutral|Negative|UNCLEAR`, `URGENCY:
  1-5`, `INTENT: Billing|Technical|General|UNCLEAR`, `EVIDENCE: <the shortest quote>`.
- **CARE** Reads and writes nothing. In REVIEW_ONLY_SKILLS. Refusals: the prompt-skill runner's (5.1). No engine bound.
- **MAINTENANCE** skills/sentiment_classifier.md:1-13; the runner, skills.py:5034-5086.
- **TIME** sitting 370: 61.5 s.  **USES** one message at a time; not batches, not long documents.

#### decompose_task (skills/task_decomposer.md; prompt skill, phi4-mini)
- **AUTHOR** "Breaks a large objective into an ordered sequence of small, individually checkable steps."
- **USE** content = the objective. It answers an optional `<thinking>` block, then numbered lines "Verb ... -> DONE WHEN:
  <observable result>". Says: break this into, small checkable steps, break it into steps, break this down into steps.
- **CARE** Reads and writes nothing. In no set: counsel refuses it. Its rules forbid doing the task.
- **MAINTENANCE** skills/task_decomposer.md:1-8; the runner.  **TIME** sitting 373: 96.5 s.  **USES** planning before building.

#### deep_research (skills/deep_research.md; handler)
- **AUTHOR** "Runs an intensive deep-dive analytical evaluation on a complex subject payload using a specialized reasoning
  sub-agent." It hands the question to the Deep Researcher seat (agents/deep_researcher.md, qwen3.5:9b).
- **USE** content = the question (else filepath, else the request).
- **CARE** Reads and writes nothing; wakes the seat. Not in any set: counsel refuses it; not offered to the driver. Sends
  "Investigate the following in depth:\n\n{payload}" and answers "Deep research findings:\n{answer}". Refusals: "Error:
  deep_research needs a <content> payload."; "Error: no 'Deep Researcher' agent defined in agents.md."; "Deep research
  failed: {exc}". Bounded at 300 s.
- **MAINTENANCE** skills.py:3560-3583.  **TIME** sitting 370: 119.1 s (FAULT: the law-court meaning).
- **USES** hard open questions; not file lookups (symbols, ground_read, semantic_search).

#### edit_file (skills/edit_file.md; handler; writes the workspace)
- **AUTHOR** "Replaces ONE exact passage in a file that is already in the workspace, so a large file can be changed without
  rewriting it whole."
- **USE** filepath = a file in agent_workspace/; content = a line `@@ OLD`, the exact text, a line `@@ NEW`, its replacement.
  Example: filepath probe.py, content "@@ OLD\nprint(1)\n@@ NEW\nprint(2)".
- **CARE** Writer (asks his card under /drive); filepath jailed to the workspace. In order: "Refused: edit_file needs the file
  to edit as <filepath>, and the passage as <content> in the two-marker shape: a line `@@ OLD`, the exact text to replace, a
  line `@@ NEW`, then what replaces it."; "Refused: {rel!r} is not a path this skill may touch ({exc})."; "Refused: there is
  no {name!r} in the workspace to edit. write_file makes a new file; edit_file changes one that is already there."; "Refused:
  the edit needs exactly one `@@ OLD` line and one `@@ NEW` line after it. Found {h} and {n}. ..."; "Refused: the text after
  `@@ OLD` is empty; nothing to find."; "Refused: the old and new text are identical. Nothing to do."; "Refused: {name} has
  MIXED line endings, so an edit cannot preserve what it already has. ..."; "Refused: that passage is not in {name}. Nothing
  was written. Read the file and quote it exactly -- whitespace and all."; "Refused: that passage appears {k} times in {name},
  and an anchor that matches more than once does not say which. Quote more around it until it is unique."; for a .py, "Refused:
  that edit would leave {name} unparseable -- {msg} at line {n}. Nothing was written." and "Refused: that edit would leave
  {name} {what it adds}. Nothing was written. ..." (the code check refuses importing requests, urllib, socket, http or
  importlib, calling eval, exec or __import__, and shell=True). Success: "Edited {name} at line {L}: {a} line(s) replaced by
  {b}, file now {x} lines (was {y}). Terminator kept: CRLF|LF." Trailing newlines are stripped from both passages.
- **MAINTENANCE** skills.py:3982-4021; _edit_passage 4024-4049; _apply_passage 4052-4120; the code check pipeline.py:389-517.
- **TIME** sitting 373: 38.1 s.  **USES** scratch files; not the ground's source (ground_edit), not new files (write_file).

#### embed_text (skills/embed_text.md; handler; writes the index)
- **AUTHOR** "Adds or refreshes a single workspace file in the semantic index immediately, without a full sweep."
- **USE** filepath = a workspace file.
- **CARE** Writer; never offered to the driver; one index build at a time. "Error: missing <filepath> parameter."; "Error:
  workspace file '{name}' not found."; "Error: '{name}' is empty; nothing to embed."; "Refused: an index build is still running
  behind an earlier call ..."; "Index refused: {exc}" (an embedder mismatch among them); "Embedding failed: {exc}"; "'{name}' is
  unchanged since it was last indexed; nothing to do."; success "Indexed '{name}' with nomic-embed-text-v2-moe:latest: {chunks}
  passages.\n  index now: {docs} docs / {chunks} chunks\n  searchable via semantic_search." As it stands a non-text file or one
  over 256,000 bytes is reported as "0 passages", not refused. The index: SQLite `meta` (schema "2", embed_model, fts_built),
  `docs` (path, root, sha256, chars, indexed_at), `chunks` (doc, ord, start, text, a normalized float32 vector, label, stamp,
  session), `chunks_fts` (FTS5); chunks of 1,200 characters overlapping by 200, at most 200 per file; markdown chunks headed
  "[{file} > {heading path}]".
- **MAINTENANCE** skills.py:2160-2208; the lock 3245-3256; manjuel/vectors.py.  **TIME** sitting 373: 291.4 s (a FAULT then).
- **USES** making one new file searchable now; not a folder (index_ground).

#### extract_facts (skills/fact_extractor.md; prompt skill, phi4-mini)
- **AUTHOR** "Pulls hard facts out of long or dense text - quantities, dates, names, and explicit quotes - and drops everything else."
- **USE** content = the text. It answers a table "Fact | Value | Quoted from", or "NO FACTS FOUND". Says: extract the facts,
  pull the facts out, the hard facts in.
- **CARE** No disk. In REVIEW_ONLY_SKILLS. The runner's refusals.  **MAINTENANCE** skills/fact_extractor.md:1-8.
- **TIME** sitting 373: 53.4 s.  **USES** before compressing a long document; not short text.

#### git_commit (skills/git_commit.md; handler; writes a repository)
- **AUTHOR** "Stages every change in the ground and commits it locally with a message. This is local versioning - it does not
  reach any remote."
- **USE** The reliable form is his own words: `git commit: "add X"` or `git commit in atlas: "..."` (the quoted message and
  the world are taken with no Router). As it stands `<content>` is NOT the message: the subject is his quoted message, else his
  words with "git commit" stripped, else "chain: <changed top-level paths>", else "chain commit (no subject given)"; a subject
  under 4 characters, a skill's name, words that only describe committing, the previous subject, or one snake_case word is
  thrown away. filepath names the repository ("", ".", "ground", "research", "here", "this ground" = the ground).
- **CARE** Runs `git add -A` then commit. Writer; never offered to the driver; jailed to the ground. Trailer: "{c} changed, {u}
  untracked" and "sitting: {session}". Refusals: "Refused: {raw!r} is not a place in this ground. ..."; "Refused: that is not a
  world a seat may act in. ..."; "Refused: {raw!r} is a file, not a world. ..."; "Refused: {label} is not a repository of its
  own -- ..."; from git, "this ground is not a git repository (git_init first)", a lock message (a lock older than 120 s is
  called stale), "a commit needs a message". Answers "Nothing to commit; the ground is clean." or "Committed {short} on
  {branch}: {msg}" plus "Those {c} changed and {u} untracked were WHAT WENT IN, not what remains. ..."
- **MAINTENANCE** skills.py:2538-2569; the world 819-866; the subject 2372-2535; gitstate.commit (manjuel/gitstate.py:272-306).
- **TIME** git calls 0.02 s once stdin is closed (gitstate.py:56-57).  **USES** a local save by his word; not a send.

#### git_cycle (skills/git_cycle.md; handler; commits and pushes)
- **AUTHOR** "Runs the FULL version-control cycle in one act: refuses to ship on red or stale STROKES or SMOKE ... commits ...
  pushes, and then VERIFIES the remote actually moved."
- **USE** content = the message (used word for word, as it stands with none of git_commit's checks), or his words `git cycle
  "msg"`. Only this ground.
- **CARE** Reads tests/last_run.json, tests/run_history.jsonl, SPEC, CHANGELOG, DAYBOOK and HANDOFF through tests/release.py;
  commits, then pushes (needs MANJUEL_GIT_REMOTE). Never offered to the driver. Only strokes and smoke stop it (green, not
  running, stamped after the newest edit); the other checks are printed for the tag. In order: "Refused: git_cycle needs a
  commit message. ..."; "Refused: git_cycle ships THIS ground and no other. ..."; "Refused: the proofs could not be read ...
  Nothing ships unproven."; "...REFUSED: {names}. Nothing was committed and nothing was pushed."; "Nothing to commit; the
  ground is clean. No commit, no push."; "Refused at the commit: {exc}"; "Refused: the head did not move, so no commit was
  made. Nothing was pushed."; "Committed at {head}, NOT PUSHED: {exc}"; then the landing proof: "they agree: the work is on the
  remote." / "** THEY DISAGREE: the push did not land. **" / "** the remote head could not be read; the push is UNVERIFIED **".
  On main GitHub refuses the push; the save on main stays.
- **MAINTENANCE** skills.py:2766-2923.  **TIME** not measured.  **USES** the older road; under SITTING LAW 11 `/drive ship`.

#### git_init (skills/git_init.md)
- **AUTHOR** "Starts version control in this ground if it is not already a repository. Safe to call when unsure."
- **USE** no arguments, or filepath = a folder.
- **CARE** Runs `git init`. Writer; never offered to the driver. As it stands it cannot start a repository in a folder
  inside the ground (git says it is already in a work tree). Answers "Already a repository.", git's output, or "Initialised an
  empty repository."; failures "Refused: {err or 'git init failed'}".
- **MAINTENANCE** skills.py:2725-2737; gitstate.py:195-202.  **TIME** not measured.  **USES** a brand-new top-level ground.

#### git_pull (skills/git_pull.md)
- **AUTHOR** "Fast-forwards this ground from its remote. Refused unless the operator has enabled remote operations."
- **USE** no arguments, or filepath = atlas.
- **CARE** `git pull --ff-only`. Writer, remote; never offered to the driver. "Refused: remote operations are off. A pull
  rewrites this ground from somewhere the operator does not control, so it is not something a seat may start. Set
  MANJUEL_GIT_REMOTE=1 to allow it."; "Refused: this ground is not a git repository"; git's error, or "git pull failed";
  success, git's output or "Up to date."
- **MAINTENANCE** skills.py:2740-2748; gitstate.py:309-322.  **TIME** not measured.  **USES** catching up while the wall is open.

#### git_push (skills/git_push.md)
- **AUTHOR** "Sends local commits to the remote. Refused unless the operator has enabled remote operations."
- **USE** no arguments, or filepath = atlas. A bare `git push`: the branch must already follow a remote.
- **CARE** Writer, remote; never offered to the driver. "Refused: remote operations are off. A push leaves this machine and
  cannot be recalled once fetched, so it is the operator's act. Set MANJUEL_GIT_REMOTE=1 to allow it."; on main or master that
  origin has: "Refused: {branch} is on GitHub, and GitHub takes a change to it only through a pull request whose checks have
  passed. ..."; success, git's output or "Pushed."
- **MAINTENANCE** skills.py:2751-2763; gitstate.py:344-391.  **TIME** not measured.  **USES** sending a line; never main.

#### git_status (skills/git_status.md)
- **AUTHOR** "Reports the repository state - branch, current commit, whether the ground is clean or dirty, and whether remote
  operations are permitted. Read-only."
- **USE** no arguments, or filepath = atlas.
- **CARE** Runs git rev-parse, `git status --porcelain` (as it stands; the index-lock risk his rules name) and git log -1. In
  REVIEW_ONLY_SKILLS; no Router. Lines: "git: {branch|DETACHED}@{short}  DIRTY ({c} changed, {u} untracked)" or "...  clean";
  "(counts are AS OF THIS INSTANT; ...)"; "last commit: {subject}"; "{c} changed, {u} untracked -- git_commit WILL include all
  {n} of them (it runs `add -A` first). Untracked does not mean excluded."; "remote operations: ALLOWED|OFF"; a lock line.
- **MAINTENANCE** skills.py:2240-2277; gitstate.read.  **TIME** sitting 366: 147.6 s (the turn).  **USES** before a save.

#### ground_edit (skills/ground_edit.md; handler; writes the ground, on a line of work)
- **AUTHOR** "Replaces ONE exact passage in a file that is already in the ground itself ... on a LINE OF WORK."
- **USE** filepath = a file relative to the ground (manjuel/intent.py, tests/test_x.py, a doc); content = `@@ OLD` / the exact
  text / `@@ NEW` / the replacement, as edit_file. The repository must stand on a branch other than main or master (the driver
  opens `drive-MMDD-HHMMSS` first when it is on main).
- **CARE** Writer: his card under /drive. In order: "Refused: ground_edit needs the file as <filepath>, relative to the ground
  (e.g. manjuel/intent.py or tests/test_x.py)."; "Refused: '{rel}' is outside the ground. Nothing was written."; the NEVER
  WRITTEN list -- a secret ("Refused: '{rel}' is a secret, and keys are silent -- never written by a seat (RULE 7). Nothing was
  written."), client data ("Refused: that is CLIENT DATA -- ..."), `.git/` ("... the history is git's to write (LAW 8) ..."),
  the top folders worlds, law, foundation, agents, skills, sessions, logs, index, state, flows, memory, projects,
  agent_workspace, bin ("Refused: {reason}. Nothing was written."; agents and skills are open to the driver alone, Steward's
  /drive, since 2026-10-19 -- WHAT'S LEFT H5 -- and every seat is still refused), the proof stamps tests/last_run.json, last_run.md,
  run_history.jsonl, last_audit.md ("... a seat never writes its own proof ..."), the files CLAUDE.md, .gitignore,
  .gitattributes, index_roots.txt, pipelines.md, commands.md, .env.example, memory.md, SEAT_LOG.md, BUILDMAP.md, and binaries
  .exe .dll .bin .pyc .pyd .so .bundle .obj ("... a binary is placed on the operator's allowance, never written by a seat
  ..."); then the line: "Refused: the ground is not under version control here, ..."; "Refused: git could not be asked
  ({err}). Nothing was written."; "Refused: the repository at `{name}` stands {detached|on `main`}, and the main line is the
  operator's (RULE 6). Open a line of work first -- `git_branch new <name>` through the door, or Lines of work on the GitHub tab
  -- and write on it. Nothing was written."; "Refused: there is no '{rel}' in the ground to edit. ground_write makes a new file;
  ground_edit changes one that is already there."; then the edit, as edit_file, its answer ending " On line of work `{branch}`;
  unsaved until git_commit lands it there." (As it stands its file does not name foundation/ among what it refuses.)
- **MAINTENANCE** skills.py:4365-4380; _tree_target 4315-4330; never_written 4211-4241 (lists 4177-4208); repo_of 4244-4254;
  line_of_work 4257-4276.  **TIME** sitting 401: three edits in C71's 717.5 s job.
- **USES** source and doc changes on a line; not the workspace, never main.

#### ground_list (skills/ground_list.md)
- **AUTHOR** "Lists what is actually in the ground (the Research folder) right now — the total listed, then top-level folders
  with counts, and files. Quote the total."
- **USE** content = a folder (agents), or empty for the top level.
- **CARE** Reads directory entries only. In REVIEW_ONLY_SKILLS; jailed to the ground. Skips dot-names, __pycache__, secrets
  and client-tagged names; a vault shows as "vault/  ({n} protected items — contents never listed)"; worlds/ shows its count
  only. More than one word: "Error: a folder NAME was expected here, not a sentence. Got {rel[:60]!r}. ..."; "Error: '{rel}' is
  not a folder inside the ground. Call ground_list with no content to see what is." Header: "Contents of {where}, live from
  disk (read-only) -- {n} entr(y|ies) listed ({d} folder(s), {f} file(s)):"; folders "name/  ({n} items)", files "name  ({bytes:,}
  bytes)".
- **MAINTENANCE** skills.py:877-942.  **TIME** sitting 366: 7.4 s.  **USES** what is in the repository; the workspace is list_directory.

#### ground_read (skills/ground_read.md)
- **AUTHOR** "Reads one file from the ground (the Research folder) as it is on disk right now ... Read-only, refuses secrets,
  stays inside the ground."
- **USE** content = a path for the whole file (pipelines.md); or filepath = the file and content = the part: a definition's
  BARE name (`SkillLibrary.execute`, `drive_check`), a part number (2), or a heading's text. With nothing, the file named in
  the request, then the last file named in the conversation.
- **CARE** Read-only; refuses secrets and client material (a `[[CLIENT]]` marker in the first 2,048 bytes). In
  REVIEW_ONLY_SKILLS; both arguments are path-gated (5.1, step 4: a name with three words or more, "drive (lines 1376-1420)", is
  refused before the handler runs). Refusals: "Error: name the file, relative to the ground (e.g. pipelines.md)."; "Error: '{rel}'
  is outside the ground; only Research is readable."; "Refused: '{name}' is a secret and is never read aloud (LAW 9)."; the client
  refusal; not a file -- the cure when one file of that name exists ("A file of that name IS in the ground: `{f}` -- call
  ground_read with <filepath>{f}</filepath>."), a list when several do, else "Error: '{rel}' is not a file in the ground."; "Read
  error: {exc}". A file up to 12,000 characters comes back whole ("{rel} as on disk right now:"); a bigger .py comes back as
  "THIS IS THE MAP, NOT THE FILE": its definitions and top names, any one fetched whole by name ("`{name}`, lines A-B of N (a
  WHOLE definition, not a character range)"; as it stands the name lookup ignores case, so `drive` returned the class `Drive`); a
  bigger other file as "part N of M" (12,000 characters each) or a section by its heading.
- **MAINTENANCE** skills.py:1703-1754; windowed 1057-1144; _windowed_python 950-1039; find_by_name 611-640.
- **TIME** sitting 366: 9.6 s.  **USES** the current text of a real file; by meaning is semantic_search.

#### ground_report (skills/ground_report.md)
- **AUTHOR** "States where the chain is standing: the ground path, the agent workspace, the active session, and what is
  resident on the card right now. Deterministic."
- **USE** no arguments.  **CARE** Reads the environment and the rack's resident list. REVIEW_ONLY; no Router. Lines "ground
  :", "workspace     : … (seat scratch -- writes land here)", "session       :", "workspace has : {n} item(s)", "resident now  :".
- **MAINTENANCE** skills.py:1999-2019.  **TIME** sitting 370: 33.2 s.  **USES** "where are we".

#### ground_write (skills/ground_write.md; handler; writes the ground, on a line of work)
- **AUTHOR** "Writes one WHOLE file into the ground itself ... on a LINE OF WORK."
- **USE** filepath = the file; content = the whole file. The folder must already exist.
- **CARE** As ground_edit's target, never-written and line checks, and: "Refused: '{rel}' is a folder, not a file. Nothing was
  written."; "Refused: '{parent}/' is not a folder in the ground, and a seat makes no folder -- a new folder is the operator's
  to place (RULE 8). Nothing was written."; for .py, "Refused: that content is not parseable Python -- {msg} at line {n}. ...
  NOTHING WAS WRITTEN. ..." and "Refused: {name} {why}. NOTHING WAS WRITTEN. ..." (the WHOLE file is checked, so as it stands it
  cannot rewrite a file that already carries what the check refuses, skills.py's own urllib among them); mixed line endings
  refused. Line endings: the file's own; a new file takes its first sibling's with the same suffix, else LF. Answers "Wrote
  {rel} on line of work `{branch}`: {n} lines, new file|replaced whole, terminator CRLF|LF. It is unsaved until git_commit lands
  it on that line; the main line moves only by the operator's hand."
- **MAINTENANCE** skills.py:4333-4362; checked_python 4292-4312; terminator_for 4279-4289.  **TIME** not measured.
- **USES** new source or test files on a line; edits to big files are ground_edit's.

#### index_ground (skills/index_ground.md; writes the index)
- **AUTHOR** "Builds or refreshes the semantic index over the configured roots (see index_roots.txt)... Say `rebuild` to
  discard the old vectors."
- **USE** empty for a refresh; content "rebuild" for a full rebuild. As it stands the rebuild words (rebuild, reindex, from
  scratch, start over, fresh) are matched as plain substrings anywhere in the request, so "refresh the index" REBUILDS it
  ("refresh" contains "fresh").
- **CARE** Reads every root in index_roots.txt; writes index/vectors.db (a rebuild deletes it and its -wal and -shm). Writer;
  never offered to the driver; one build at a time. "Error: no readable roots. ... Edit index_roots.txt (one path per line).";
  the busy refusals; "Index refused: rebuild refused: {file} is held open by another process or a build still running ...";
  "Indexing failed: {exc}". Report: "REBUILT|Refreshed with {model}.", roots, scanned, embedded, unchanged, oversized, absent,
  "index now", up to ten errors. Limits: 4,000 files, 256,000 bytes a file, 200 chunks a file; transcripts older than 45 days
  skipped; the prune will not evict more than a quarter of the corpus (as it stands that refusal is not shown in the report).
- **MAINTENANCE** skills.py:3313-3398; _wants_rebuild 3282-3300; manjuel/vectors.py:517-726.
- **TIME** sitting 368: 84.3 s.  **USES** after files change, or after the embedder changes; one file is embed_text.

#### inspect (skills/inspect.md)
- **AUTHOR** "Reports the FACTS about a file before anything reads it — size, real type by its first bytes, line terminator
  ... how many injection markers the hard gate finds in it. Never its contents."
- **USE** filepath = the file (the workspace is tried first, then the ground). With no path: what is new in the workspace since
  the sitting opened (up to 20 files).
- **CARE** Reads up to 2,000,001 bytes, git ls-files, the index. Writes nothing. REVIEW_ONLY. "Error: name the file to
  inspect, or leave it out for what is new in the workspace."; "Refused [LAW 8]: '{rel}' is an absolute path; ..."; "Error:
  '{rel}' is outside the ground; only Research is inspectable."; "Error: '{rel}' is not a file in the workspace or the
  ground.{hint}"; "Refused: {shown} is a SECRET by name. ..."; "Refused: {shown} is CLIENT DATA by tag. ..." Lines: where, size,
  type, modified, git, index, and for text the line count, terminator, first line, injection markers, then "to read it:".
- **MAINTENANCE** skills.py:1934-1971; inspect_file 1840-1914; manjuel/intent.py:963-975.  **TIME** sitting 374: 8.6 s.
- **USES** before reading anything from outside.

#### linear_regression (skills/linear_regression.md)
- **AUTHOR** "Fits a trendline through a series of numbers using ordinary least squares and projects the next few steps."
- **USE** content = the numbers; x is 0..n-1. As it stands EVERY number in the text is data (years and labels too).
- **CARE** No disk; not in REVIEW_ONLY (counsel refuses it). "Error: missing <content> -- give the numbers to fit."; "Cannot
  fit: {exc}" (no numbers given; no numbers found; over 10000; fewer than 2 points). Answers the fit, the trend, R² in bands
  (0.9, 0.5), the next three steps and a caveat.
- **MAINTENANCE** skills.py:2926-2960; manjuel/mathkit.py:136-163, 202-226.  **TIME** sitting 370: 15.5 s.

#### lint_code (skills/syntax_lint.md; prompt skill, qwen2.5-coder:14b)
- **AUTHOR** "Reads a block of source and reports likely defects ... Use before code is saved."
- **USE** content = the source. At most five findings, each "• Line / • Bug / • Severity / • Patch".
- **CARE** No disk; in no set. The runner's refusals. Its own rules call it unverified.
- **MAINTENANCE** skills/syntax_lint.md:1-13.  **TIME** sitting 370: 85.4 s.  **USES** a quick read of code; not a proof.

#### list_directory (skills/list_directory.md)
- **AUTHOR** "Lists all available files currently sitting inside the workspace directory."
- **USE** no arguments.  **CARE** Reads the workspace's top level. REVIEW_ONLY; no Router. As it stands it filters NOTHING
  (secret and client names are listed; ground_list filters both). "Contents of the agent workspace (agent_workspace/) --
  scratch files only, NOT the whole repository:\n - name", "Empty: …", "Directory error: {exc}".
- **MAINTENANCE** skills.py:2022-2033.  **TIME** sitting 370: 130.1 s.  **USES** the scratch folder only.

#### mcp_call (skills/mcp_call.md; asks his card under /drive)
- **AUTHOR** "Calls one tool on a LOCAL MCP server this ground declares."
- **USE** content = `atlas <tool> {json}` (empty: the request). Callers other than the Router may pass server and tool
  directly. The server is a whole word naming a MANJUEL_MCP_<NAME> dial; the tool is the LONGEST name on the server's roster
  that appears as a whole word in the line, the JSON included (keep other tool names out of the arguments); the arguments are
  the first `{` to the last `}`, parsed as JSON (not an object: {}).
- **CARE** HTTP JSON-RPC to the declared address, loopback only (127.0.0.1, ::1, [::1], localhost), with "Authorization: Bearer
  <MANJUEL_MCP_<NAME>_KEY>"; neither is ever printed. Wire: tools/list, initialize (protocol 2025-06-18), tools/call. Waits
  MANJUEL_SKILL_TIMEOUT less 5 (295 s). Not in WRITING_SKILLS; counsel refuses it. Refusals: "Refused: this ground declares no
  MCP server. ..."; "Refused: this ground declares no MCP server called {name!r}. ..."; "Refused: the address declared for
  {name!r} is not on this machine, and the estate is local (RULE 4). ... Nothing was sent."; "Refused: {name} could not be read
  -- {err}."; "Refused: {name} carries no tool called {tool!r}. It carries: …"; "Refused: {name} could not run {tool!r} --
  {err}."; "Refused: {name}'s {tool!r} refused -- {text}"; "{name}'s {tool!r} ran and returned nothing."; the three JSON refusals.
  A door that holds the call answers "HELD: ..." (5.3); as a plain line in the Agent tab it goes to door_call, which waits.
- **MAINTENANCE** skills.py:3781-3947; helpers 3613-3779.  **TIME** sitting 370: 17.3 s; door_call 6.4 to 8.4 s.

#### proved (skills/proved.md)
- **AUTHOR** "Reports what the suites last proved and when — the stroke and smoke tallies, whether they are STALE against the
  current code ..."
- **USE** no arguments.  **CARE** Reads tests/last_run.json (per suite: state, passed, total, green, at, failures) and the
  last four lines of tests/run_history.jsonl; runs the manifest check (us.reconcile). Writes nothing. REVIEW_ONLY; no Router.
  Says: "No suite has ever stamped this ground. ..."; "tests/last_run.json is unreadable -- re-run the suites."; "DID NOT FINISH
  -- a crash or a kill. Not a number anyone earned." (also while a run is still going); "...and the ground has CHANGED SINCE.";
  "A suite is RED -- read tests/last_run.md, not the scrollback."; then the manifest lines and what the suites do not cover.
  door_call reads a long suites run back through it (C71).
- **MAINTENANCE** skills.py:2572-2696.  **TIME** sitting 370: 28.2 s.  **USES** "are we green", and after a suite_run.

#### rack_list (skills/rack_list.md)
- **AUTHOR** "Reports every model installed on this machine, which of them are currently loaded in VRAM, their sizes, and which
  are declared by this ground versus held by another client. Read-only."
- **USE** no arguments.  **CARE** Reads Ollama's model list. REVIEW_ONLY; no Router. "Rack unreachable: {exc}"; "{n} models
  installed, {m} loaded in VRAM:", per model LOADED, size on disk, size in memory, "declared here"; a warning for another
  client's models; the price of waking each seat; the card line with its headroom or "OVER by". Budget 15 GB.
- **MAINTENANCE** skills.py:2997-3066; manjuel/vram.py.  **TIME** sitting 366: 22.6 s.  **USES** what is on the card.

#### rack_load (skills/rack_load.md)
- **AUTHOR** "Brings a model into VRAM now so the next call to it is instant."
- **USE** content = the model.  **CARE** VRAM only; in no set; never offered to the driver. "Error: name the model to load,
  e.g. <content>qwen3.5:4b</content>"; "'{tag}' is not installed. rack_pull would fetch it."; "'{tag}' is already loaded.";
  "Loaded '{tag}' in {s:.1f}s."; "Load failed: {exc}".
- **MAINTENANCE** skills.py:3178-3191.  **TIME** sitting 370: 48.3 s.  **USES** warming a cold seat.

#### rack_pull (skills/rack_pull.md)
- **AUTHOR** "Downloads a model that is not yet installed. Reaches the network ... refused unless the operator has explicitly
  enabled it."
- **USE** content = the model.  **CARE** Network and gigabytes, through Ollama; never offered to the driver. "Error: name the
  model to pull."; "Refused: pulling reaches the network and can move gigabytes onto this machine. That is the operator's
  call. Set MANJUEL_RACK_PULL=1 to allow it, or run: ollama pull {tag}"; "'{tag}' is already installed."; "Pulled '{tag}': …";
  "Pull failed: {exc}". Bounded at 300 s.
- **MAINTENANCE** skills.py:3217-3233.  **TIME** not measured (RULED: downloads are his).  **USES** rarely; `ollama pull` by hand.

#### rack_report (skills/rack_report.md)
- **AUTHOR** "Reports the observed state of the rack ... FACTS ONLY ... Ask for a judgement in the question ... and the
  Quartermaster reads the same inventory beside it."
- **USE** content = the question ("is there room for the coder?").  **CARE** Reads Ollama; wakes the Quartermaster seat only
  when the question asks for a judgement (manjuel/intent.py:357-365). Not REVIEW_ONLY. rack_list's lines plus "Declared by this
  ground / Declared but NOT installed / VRAM budget / Question", then either "(FACTS ONLY -- no seat was asked to read them.
  ...)" or "--- OBSERVED ABOVE ... BELOW IS THE QUARTERMASTER'S READING (a seat's words, LAW 5) ---", or "(Quartermaster
  unavailable: {exc})".
- **MAINTENANCE** skills.py:3069-3140.  **TIME** sitting 370: 66.2 s.  **USES** room and advice questions.

#### rack_sync (skills/rack_sync.md; rewrites rack.md)
- **AUTHOR** "Pulls a current list of models from Ollama and rewrites rack.md."
- **USE** no arguments (`/rack` runs it).  **CARE** Writes rack.md whole, CRLF. Writer; never offered to the driver. "Could not
  survey the rack: {exc}". rack.md: "# The Rack", a "Declared by this ground" table, "Declared but missing", "Installed but
  unused", "In VRAM but not ours". As it stands its change list calls every installed-but-unused model "new since last sync" on
  every sync, and it does not list the driver's qwen3.5:9b use.
- **MAINTENANCE** skills.py:3143-3175; manjuel/rack.py.  **TIME** sitting 368: 1.3 s.  **USES** after a model is pulled or removed.

#### rack_unload (skills/rack_unload.md)
- **AUTHOR** "Frees VRAM by evicting a loaded model. ... Refuses to unload a model this ground does not declare."
- **USE** content = the model.  **CARE** VRAM only; never offered to the driver. "Error: name the model to unload."; "'{tag}' is
  not loaded; nothing to free."; "Refused: '{tag}' is loaded but is NOT declared in this ground, so it belongs to another
  client. Unloading it would cost them a reload. The operator can do it by hand."; "Unloaded '{tag}', freeing about {X}GB.";
  "Unload failed: {exc}".
- **MAINTENANCE** skills.py:3194-3214.  **TIME** sitting 373: 15.4 s.  **USES** a full card.

#### read_file (skills/read_file.md)
- **AUTHOR** "Reads the raw text content of a specific file inside the workspace."
- **USE** filepath = a workspace file; content = a part number or a heading. A filepath beginning "ground/" or "research/" is
  handed to ground_read, the answer prefixed "(`{f}` names the ground, so it was read from the GROUND, by ground_read's own
  rules; `read_file` reads the workspace.)".
- **CARE** Prints a one-line facts stamp first. REVIEW_ONLY; jailed to the workspace. As it stands it checks for client
  material but NOT for secret names (the stamp is dropped and the read goes ahead). "Error: missing <filepath> parameter.";
  "Refused: '{f}' names the GROUND, and this seat is cleared for the workspace's reader only. Nothing was read."; the client
  refusal; "'{f}' is a DIRECTORY, not a file -- nothing was read. It contains: ..."; "Error: workspace file '{f}' not found.";
  "Read error: {exc}".
- **MAINTENANCE** skills.py:2036-2087.  **TIME** sitting 373: 17.8 s.  **USES** the scratch folder's files.

#### remember (skills/remember.md; stages, never lands)
- **AUTHOR** "Proposes a note to carry into later sessions ... The entry is STAGED, not remembered."
- **USE** content = the note; filepath = a short title (not a path; else the first eight words).
- **CARE** Appends one line to memory/pending.jsonl: `{title, body, provenance: "GENERATED", session, run, stamp, kind: "note"}`.
  He lands it with `/memory` into memory.md, each landing sealed on memory/chain.jsonl as "LAND by operator -> memory.md
  range:A-B sha256:H". Writer; never offered to the driver. "Error: missing <content> parameter -- nothing to remember.";
  "Proposed for memory: {title!r}\n  staged as GENERATED, NOT yet remembered.\n  {n} entr(y|ies) pending -- the operator lands
  them with /memory." (The door's own `remember` writes a different store, state/remembered.jsonl.)
- **MAINTENANCE** skills.py:2211-2237; manjuel/memory.py.  **TIME** sitting 370: 149.7 s.  **USES** rulings worth keeping.

#### run_python (skills/run_python.md; asks his card under /drive)
- **AUTHOR** "Runs ONE Python file from the workspace and reports what it said ... This is not a shell."
- **USE** filepath = a .py in the workspace.
- **CARE** A child process jailed to the workspace, given only the environment Python needs; it may write inside the
  workspace; 60 s (MANJUEL_RUN_TIMEOUT), then killed. The jail refuses writes outside the workspace, reads outside it and
  Python's own library, network modules, starting processes, and ctypes. "Refused: run_python needs the file to run as
  <filepath> -- a bare name inside the workspace, e.g. probe.py."; "Refused: {rel!r} is not a path this skill may run ({exc}).";
  "Refused: run_python runs Python, and {name!r} is not a .py file. There is no general runner here on purpose."; "Refused:
  there is no {name!r} in the workspace to run. Write it first."; "Refused: {name} did not finish inside 60s and was stopped
  (LAW 7: bounded everything). ..."; "Refused: {name} could not be started -- {T}: {exc}". Verdicts STOPPED BY THE JAIL, RAN,
  FAILED (exit N); stdout and stderr to 4,000 characters each.
- **MAINTENANCE** skills.py:4538-4620; the jail 4443-4531.  **TIME** sitting 373: 18.5 s.
- **USES** "does it run"; not the suites (a job's check runs those).

#### search_transcripts (skills/search_transcripts.md)
- **AUTHOR** "Searches THE RECORD by meaning - what HAPPENED. Both the transcripts of past runs and the append-only ledgers ..."
- **USE** content = the question (empty: the request).  **CARE** Reads the index over logs/ and CHANGELOG, HANDOFF, SEAT_LOG,
  DAYBOOK, TASKS, REFUSALS, memory.md, BUILDMAP. REVIEW_ONLY. "Error: no query given and no objective to borrow one from.";
  "Index refused: {exc}"; "Error: the index is empty. Run index_ground first."; "Query embedding failed: {exc}"; "No passages
  matched {q!r}." Ranking: the 8 best passages, at most 2 a document; meaning (vectors) and exact words (FTS) merged, the best 2
  exact hits always kept; +0.06 foundation/ or memory.md, +0.03 us/ or agents/, -0.03 manjuel/ or tests/, up to +0.04 for
  recent files; the top 5 shown, each snippet to 240 characters.
- **MAINTENANCE** skills.py:3427-3442; shared 3445-3557; manjuel/vectors.py:730-864.  **TIME** sitting 370: 50.5 s.
- **USES** what was decided or what ran; not what the code says.

#### semantic_search (skills/semantic_search.md)
- **AUTHOR** "Searches the indexed ground by meaning rather than keywords ... Requires index_ground to have been run."
- **USE** content = the subject.  **CARE** As search_transcripts, over the SOURCES only (no transcripts, no ledgers). As it
  stands its file and its header still say "past runs".
- **MAINTENANCE** skills.py:3422-3424.  **TIME** sitting 366: 50.0 s.  **USES** doctrine, code and specs by meaning.

#### sitting (skills/sitting.md)
- **AUTHOR** "Resolves a SITTING NUMBER to the runs it held and the transcript path of each one, read from the paid record in
  SEAT_LOG.md."
- **USE** content = the number (the first integer in content, filepath or the request).
- **CARE** Reads SEAT_LOG.md (headings "## <date> — sitting <n>"; run lines numbered, the next line ending in "logs/….md").
  REVIEW_ONLY. "Error: name the sitting by number, e.g. <content>63</content>."; "Error: SEAT_LOG.md is not in the ground; no
  sittings recorded."; "No toll for sitting {n} is in SEAT_LOG.md. The record runs to sitting {max}. ..." Answers the head, the
  seat's line, the runs, then "Read any of those with ground_read ...".
- **MAINTENANCE** skills.py:1155-1223.  **TIME** sitting 370: 54.5 s.  **USES** "review sitting N"; a period is `when`.

#### skill_report (skills/skill_report.md)
- **AUTHOR** "Lists every skill the chain can actually execute, with what each one does — read from the loaded library, never
  generated."
- **USE** no arguments.  **CARE** REVIEW_ONLY; no Router. "Error: the skill library is not attached to this run.", or "The
  chain executes {n} skills:" and "  {name:20} {first sentence, to 110 characters}".
- **MAINTENANCE** skills.py:1974-1996.  **TIME** sitting 373: 16.1 s.  **USES** "what can you do".

#### skill_search (skills/skill_search.md)
- **AUTHOR** "Finds which of this chain's skills bear on a subject, and reports each one's own description in full ... Nothing
  is executed."
- **USE** content = the subject. A question about a tool is sent here by itself.
- **CARE** REVIEW_ONLY. As it stands it does not give descriptions in full: each is cut to 700 characters, top five only.
  Scoring: each query word over two letters found by substring, plus 6 for an exact name. "Error: the skill library is not
  available here."; "Error: name what you want the chain to do, e.g. <content>read a file</content>."; "No skill in this ground
  matches {q!r}. The chain has {n} of them; `skill_report` lists every one." It ends "These are DESCRIPTIONS, read from the
  files. Nothing was run."
- **MAINTENANCE** skills.py:1340-1391.  **TIME** sitting 373: 28.8 s.  **USES** which tool does X.

#### speak (skills/speak.md)
- **AUTHOR** "Read text aloud through the machine's own speech engine."
- **USE** content = the text.  **CARE** Starts Windows' speech (PowerShell SAPI) with the text through a temporary file named
  in an environment variable, deleted after; spoken text to 1,200 characters; 180 s. Never offered to the driver. "Error:
  missing <content> -- nothing to say."; "Cannot speak: {exc}"; "Nothing speakable in that text."; "Spoke {n} characters aloud.
  What was said:\n\n{text}".
- **MAINTENANCE** skills.py:2699-2722; manjuel/voice.py:263-353.  **TIME** sitting 370: 154 s.  **USES** when he asks to hear it.

#### statistics (skills/statistics.md)
- **AUTHOR** "Computes n, mean, median, min, max, standard deviation and variance over a series of numbers."
- **USE** content = the numbers (as it stands every number in the text counts).  **CARE** No disk. REVIEW_ONLY. "Error: missing
  <content> -- give the numbers."; "Only {n} number found; need at least 2."; "Cannot compute: {exc}". Sample deviation and
  variance (n-1), six significant figures.
- **MAINTENANCE** skills.py:2963-2982.  **TIME** sitting 370: 28.5 s.

#### subtask (skills/subtask.md)
- **AUTHOR** "Hands ONE scoped piece of work to a fresh run with its own context, and returns only its result."
- **USE** content = the whole piece of work, stated so that a run that cannot see this conversation can do it.
- **CARE** A Router-only sub-run; no nesting; three a turn; inside the 300 s skill bound. Counsel refuses it. "Error: sub-tasks
  are not available here — this skill was called outside a running chain."; "Error: name the sub-task, ... It must be ONE piece
  of work, stated whole: the sub-task cannot see this conversation."; "Error: a sub-task needs an objective to work on.";
  "Refused: a sub-task may not start another sub-task (depth 1). ..."; "Refused: 3 sub-tasks have already run this turn, which
  is the cap. Answer with what they returned."; "The sub-task failed: {T}: {exc}". Answers "Sub-task: …\nTools it ran: …\n---
  what it returned (another seat's words, LAW 5) ---\n…".
- **MAINTENANCE** skills.py:1677-1700; manjuel/pipeline.py:4020-4098.  **TIME** sitting 370: 253.6 s.

#### symbols (skills/symbols.md)
- **AUTHOR** "Where a name is DECLARED in this ground, read straight off the disk — file and line for every def, class, func,
  type or exported binding, in Python, Go and JavaScript."
- **USE** content = the name; empty for a map of the ground (the 25 files most named by others).
- **CARE** Reads up to 1,500 code files of up to 400,000 bytes, skipping .git, __pycache__, node_modules, .venv, venv, target,
  dist, build, index, logs, agent_workspace, worlds, vault and dot-folders. REVIEW_ONLY. "The ground could not be mapped: {T}:
  {exc}"; "No code files in this ground declare anything this can read."; "Nothing in this ground DECLARES {want!r}. ..." Hits
  "  {rel}:{line}   {kind} {name}" (up to 20), then "Named in {k} other file(s): …".
- **MAINTENANCE** skills.py:1590-1674; helpers 1422-1587.  **TIME** sitting 370: 20.4 s.  **USES** "where is X defined".

#### time_align (skills/time_aligner.md; prompt skill, phi4-mini)
- **AUTHOR** "Parses loose task lists or historical log entries and aligns them onto an ordered timeline."
- **USE** content = the entries, pasted. It answers a table "When | Item | Certainty", dated from the "## Now" block, undated
  items marked NO DATE.
- **CARE** No disk; in no set. The runner's refusals (asked for "the logs" with no material it refuses: sitting 95 spent 900 s
  twice before that refusal existed).
- **MAINTENANCE** skills/time_aligner.md:1-7.  **TIME** sitting 370: 58.9 s.  **USES** ordering dated text; not "the logs" by name.

#### use_record (skills/use_record.md; the engine's own after-tool hook)
- **AUTHOR** "The engine's own after-tool hook: after every skill or tool call it appends one line to logs/uses.jsonl ... It is
  never called by name."
- **USE** none: it fires after every call through the library's execute, handed the tool, ok or failed, and milliseconds.
- **CARE** In ENGINE_HOOKS, so it runs past a seat's clearance; it writes only when the library was loaded for a sitting
  (record_uses, set in cli's Session.load). Called by name: "Refused: use_record is the engine's own after-tool hook ...
  Nothing was written."; else "Not recorded: this library was not loaded for a sitting."; "Not recorded: no tool named, or
  no logs/ folder in this ground."; "Error: the use of {tool} could not be written: {exc}"; "Recorded: {tool}". Each line
  carries ts, tool, ok, ms, caller and session. skill_report reads it: "Use, from logs/uses.jsonl (since {first}):", then
  "  {name:20} used {n}, failed {f}, median {m} ms" and "  never used: ...".
- **MAINTENANCE** skills.py: _use_record, _uses_weighed, ENGINE_HOOKS, the library's execute and _call.  **TIME** not
  measured yet.  **USES** every call, read back through skill_report.

#### when (skills/when.md)
- **AUTHOR** "Lists what ran in a WINDOW OF TIME, read from the transcript stamps in logs/."
- **USE** content = today, yesterday, this week, this month, recently (0, 1, 7, 30, 3 days back), "the last N days", or
  YYYY-MM-DD. As it stands "what ran last week" and "ran between", which its file advertises, are refused.
- **CARE** Reads logs/*.md names only (YYYY-MM-DD_HHMMSS_slug.md). REVIEW_ONLY. "Error: name the period. Understood: today,
  yesterday, this week, this month, recently, 'the last N days', or a date as YYYY-MM-DD. ..."; "No logs/ folder in the ground;
  nothing has been transcribed."; "Nothing ran {label} — no transcript in logs/ carries a date in that window (...). That is the
  record being empty, not a search failing."
- **MAINTENANCE** skills.py:1245-1330.  **TIME** sitting 373: 33.7 s.  **USES** periods; a numbered sitting is `sitting`.

#### write_file (skills/write_file.md; writes the workspace)
- **AUTHOR** "Writes text, scripts, or markdown data to a file inside the workspace. A `.py` is checked before it is written
  ... Prose is not judged."
- **USE** filepath = the name; content = the whole file.
- **CARE** Overwrites without asking; as it stands always writes CRLF; makes no folder. Writer (his card under /drive); jailed
  to the workspace. "Error: missing <filepath> parameter."; for .py the parse and code-check refusals ("... NOTHING WAS WRITTEN.
  ..."); "Write error: {exc}"; "Saved to workspace: {name}".
- **MAINTENANCE** skills.py:2090-2157.  **TIME** sitting 370: 39.8 s.  **USES** scratch files; the ground is ground_write's.

**Skills that do one job between them** (read off the code): write_file and ground_write, edit_file and ground_edit (one
place each; the two edits share their functions); read_file and ground_read (read_file hands a "ground/" path over);
list_directory and ground_list; rack_list and rack_report (the report runs the list); git_cycle and git_status + git_commit +
git_push; skill_report and skill_search; semantic_search and search_transcripts (one handler, two corpora); proved and
git_cycle's proof check (two rules for "stale"); deep_research and subtask; inspect and read_file's stamp.

### 5.3 The door (atlas-mcp): how it is served, and what every call goes through

**The process.** `atlas-mcp.exe --http 127.0.0.1:8090 --auth --tenant research=<ground> --tenant atlas=<ground>/atlas
--default-project research --manjuel "python <ground>/manjuel.py"` (RUNBOOK, "Starting the system"). Flags (atlas/line
cmd/atlas-mcp/main.go:50-79): --http (empty: stdio), --auth, --auth-service (or ATLAS_SERVICE), --manjuel, --tenant name=path
(repeatable), --engine name=cmd, --default-project, --atlas-bin, --prove, --describe, --version. Holds are armed exactly when
--auth is on. SIGINT or SIGTERM closes every engine before it exits.

**The routes** (internal/httpserver/httpserver.go:56-103): GET /health -> {"status":"ok","server":"atlas-mcp","version",
"auth"}; GET /tools -> {"tools":[{name, description, inputSchema}]} (no gate); POST /rpc; GET /chat/stream, /run/stream,
/run/listen (server-sent events); GET /run/state (the engine's facts); GET /metrics (Prometheus text). /rpc takes JSON-RPC 2.0,
one request per line (a 1 MiB buffer growing to 16 MiB): `initialize` -> {protocolVersion "2025-06-18", capabilities {tools},
serverInfo, instructions}; `notifications/initialized` (no reply); `tools/list`; `tools/call` {"name", "arguments"}; anything
else -32601 "unknown method %q". A result is {"content":[{"type":"text","text":<out>}]}, with "isError":true and the tool's
own words when it failed; -32700 "parse error"; -32602 "unknown tool %q". As it stands every argument is published as a JSON
string described "the ground this call names", while some tools read numbers, booleans or objects (rack_pull's confirm, the
prompt and flow `version`, rack_open's depth, mesh_read's last and reveal, chat_list's last; prompt `vars` and flow_save's
`spec` must be JSON INSIDE a string).

**The auth gate** (--auth; on tools/call only; httpserver.go:181-213, auth.go:133-156): auth_verify stays open; no or an
unknown bearer -32001 "401: a bearer key rides Authorization — strangers get nothing"; the service bearer (constant-time equal
to ATLAS_SERVICE) is the GLASS (Service); a tenant key whose tenants do not carry the project -32003 "403: key %s does not
carry project %q" or "403: unknown project — not a carried tenant". Keys are checked against each tenant's state/auth.json:
shape atl_ and 32 hex, id k- and 8 hex, HMAC-SHA256 key derivation, 210,000 rounds, domain "atlas-auth-v1". The caller is
named by the transport, never by the arguments; as it stands a keyed caller is named by its key id (k-ae2e9481 is the
council's), not its key's name.

**The order of one call** (Registry.Call, internal/tools/tools.go:229-308): (1) an unknown tool -> ErrUnknownTool; (2) the
reserved arguments __caller and __registry are stripped; (3) the project resolves (empty: the default) -- "unknown project %q:
not a carried tenant"; (4) a ServiceOnly tool from anything but the glass writes a `refused` row and errs "refused: %q is the
operator's own hand, offered to his glass alone and to no seat, agent or other client (RULE 6); if this IS his glass, the door
has to run with --auth to tell"; (5) does it write? (a tool with a Reads list reads when `action` is empty or listed); (6) not
the glass -> RBAC (open mode, no roles assigned, allows all; otherwise the role and the roles it implies, the tool, `*`, then
the kinds; an unassigned caller is denied) -- "rbac: caller %q (role %q) denied tool %q: %s"; (7) holds armed, a write, not the
glass, not hold_answer or hold_list: a flow gate's hand over this tool lets it through (a `crossed` row), otherwise it is
PARKED; (8) it runs.

**Three kinds, used on every card below:** R, a reader: runs at once for any caller RBAC allows. W, a writer: from the glass it
runs at once; from the engine or any keyed caller, with --auth, it is HELD for his card; with holds off it runs for anyone. S,
ServiceOnly: the glass alone; every other caller is refused by step 4 and never gets a card. The seven S tools: shell_run,
aider_run, aider_undo, law_add, law_seal, file_edit, git_pr.

**How a held call works, end to end** (internal/tools/holds.go):

1. Parked: an id `hold_<unix ms>_<sequence>_<tool>`; the tool, its arguments, the caller, the project, the time, an RBAC line,
   kept in memory (a door restart drops it) and written FIRST as a line of the held world's state/holds.jsonl:
   `{"ts","what":"held","id","tool","caller","project","rbac"}`.
2. The caller is told (text, not an error): "HELD: %q writes, and this call did not come from the operator's own glass (%s).
   Nothing has been written.\n\nIt is parked as %s and waits for his hand -- RULE 6: ... He answers it on the card at the foot of
   the front page's terminal (or on the GitHub page), or with hold_answer.\n\nDo not retry this call and do not work around it.
   Say plainly that it is waiting."
3. The glass polls hold_list every 3 s and draws a card for each (secrets withheld). shell_run and file_edit park themselves
   the same way.
4. His Approve or Deny calls hold_answer {id, decision}. Deny writes `denied`. Approve runs the PARKED arguments in the held
   world, as "operator via hold <id>" with the glass's standing, without going back through RBAC or the hold, and writes
   `approved_ran` (or `approved_errored`, its note the error). Other rows: `refused` (no world), `vanished` (the tool gone).
5. The original caller hears nothing more on the wire. The engine's door_call watches the hold logs for the id and says the
   outcome in one line; a seat that called mcp_call inside a council turn only ever has the HELD text.
6. Also in the log: `crossed_<ms>_<tool>` (a gate's hand; note "run <run> gate <gate>"), `refused_<ms>_<tool>` (ServiceOnly),
   and the shell's, Aider's and the law's own rows.

### 5.4 The door's tools, one card each (in the order the door registers them)

From the Agent tab a tool is `mcp_call atlas <tool> {json}`; from the glass's page, `App.tool('<tool>', {...})`, or Registry &
Docs' Call. Every tool takes `project?` (the tenant; empty is the default, research). [err] marks a refusal that comes back as
an error (from the Agent tab: "Refused: atlas's '<tool>' refused -- <text>"); the rest come back as answers. Handlers are in
atlas/line/internal/tools/ unless named otherwise.

#### get_in_line (T30) · R
- **AUTHOR** "standing law + line + road + log-tail for a carried project".  **USE** `{"project":"atlas"}`.
- **CARE** Reads <home>/AGENTS.md (first 4,000 characters), THE_ROAD.md or else STATE_OF_BUILD.md (4,000), and the last 40
  lines of SEAT_LOG.md's first 40,000 characters (or a file list when it is a folder); paths may be moved by
  <home>/line.manifest.json (neither ground has one). Answers the standing law, "-- LINE (name) --", "-- ROAD --", "-- LOG
  TAIL --", to 60,000 characters ("[truncated at the 60000-character law]"); a missing part is named ("[no line document carried
  for %q]", "[no road document carried for %q]", "[no handoffs carried for %q]", "[handoffs dir %s empty]"), never an error.
- **MAINTENANCE** tools.go:525-532; orient/orient.go:48-110.  **TIME** 9 ms.  **USES** orienting at a start.

#### verify_chain (T95) · R
- **AUTHOR** "chain verdict via tools/chain_verify.py, the Python spine: EMPTY|INTACT|FLIP|TAMPER (SKIPPED where rows carry no hash)".
- **USE** `{"path":"sessions/sessions.jsonl"}` (path required).
- **CARE** Finds tools/chain_verify.py walking up to five levels from the door's binary, its working directory and the home;
  runs `<python> <script> chain verify <path>` in the home, 30 s; a non-zero exit is [err] with its output. As it stands the path
  is not jailed. [err] "verify_chain needs a path"; "verify_chain: tools/chain_verify.py is not beside this door; ..."; "REFUSED
  — <python> did not finish inside 30s. Nothing is claimed."
- **MAINTENANCE** tools.go:534-563.  **TIME** 144 ms (FAULT then: FLIP on all 10 links where law_status proves them whole).
- **USES** a hash chain's verdict; the law chain is law_status's.

#### muster (T52) · R
- **AUTHOR** "declared projects roll call".  **USE** `{}`.  **CARE** The door's tenants: "%d carried projects:" and a name a
  line. Never refuses.  **MAINTENANCE** tools.go:565-576.  **TIME** 9 ms.  **USES** which grounds the door carries.

#### read_handoffs (T69) · R
- **AUTHOR** "SEAT_LOG (or the manifest 'log' path) whole, with sha256 receipt(s)".  **USE** `{}`.
- **CARE** The whole file, no cap: "<name> · sha256 <hex>\n\n<body>"; a folder, each file so. [err] "no handoffs path
  configured for project %q"; "handoffs missing for %q: %s".
- **MAINTENANCE** tools.go:578-583, 3242-3282.  **TIME** 70 ms.  **USES** the toll record whole; the tail is get_in_line's.

#### list_doctrine (T45) · R
- **AUTHOR** "carried doctrine by name, read-only; absent name denied honestly".  **USE** `{}`.
- **CARE** The files in doctrine/ and foundation/: "THE CARRIED LAW — %d documents, read-only:" and a name a line, or "The hold
  is empty — no doctrine carried for project %q."  **MAINTENANCE** tools.go:585-590, 3284-3304.  **TIME** 5 ms.

#### read_doctrine (T68) · R
- **AUTHOR** "one document whole with sha256 receipt; absent name denied honestly".  **USE** `{"name":"LAW_001"}` (required).
- **CARE** Matches the name lower-cased, with ".md", or without its extension: "<file> (<dir>) · sha256 <hex>\n\n<text>", to
  60,000 characters ("[truncated honestly at %d characters — the whole document is on disk under sha256 %s]"). [err]
  "read_doctrine needs a name — try list_doctrine first"; "No such document in the hold for %q: %s. An absent name is denied
  honestly — try list_doctrine."  **MAINTENANCE** tools.go:592-597, 3306-3344.  **TIME** 5 ms.
- **USES** doctrine and foundation only; law/*.md comes through `records`.

#### check_the_wall (T15) · R
- **AUTHOR** "judge a path before acting; quote the law on refusal".  **USE** `{"path":"../Archive"}`.
- **CARE** By the letters only (no links followed): "INSIDE the wall: %s\nWithin %q — a seat may work here under the standing
  law." or "REFUSED — outside the wall: %s\n\"<the wall law>\" Prepare a packet instead; only the operator lands work outside."
  [err] "check_the_wall needs a path".  **MAINTENANCE** tools.go:599-604, 3346-3375.  **TIME** 4 ms.

#### git (T31) · R
- **AUTHOR** "the world's repository as it stands now: branch, head, dirty counts, upstream, and whether remote operations are walled".
- **USE** `{}`.  **CARE** Local git only, 5 s each: rev-parse, log -1, `status --porcelain` (as it stands without
  GIT_OPTIONAL_LOCKS=0, the index-lock risk), rev-list against the upstream, remote. JSON: world, is_repo, note, branch, head,
  subject, when, changed, untracked, dirty, files (up to 40 porcelain lines), upstream, ahead, behind, remotes, why_not_send (on
  main), remote_allowed, remote_note. The wall is MANJUEL_ (or CHAINKIT_) GIT_REMOTE in the environment, else in <home>/.env or
  <home>/../.env; 1, true, yes, on. Not a repository: {"is_repo":false,"note":"not a repository -- nothing to commit, and
  nothing to lose"}.
- **MAINTENANCE** tools.go:606-611; gitstate.go:31-135.  **TIME** 716 ms.  **USES** is the tree dirty, may it send.

#### git_diff (T34) · R
- **AUTHOR** "what actually changed: one file's change served whole, or the whole tree's; a file git has never seen comes back
  as its contents, said plainly".
- **USE** `{"file":"manjuel/serve.py"}`, or `{}` for the whole tree.
- **CARE** 10 s a git call; 60,000 bytes ("...(<what> is N bytes; this is the first 60000)"). No file: the staged diff and the
  unstaged diff, or "Nothing has changed since the last save." A file: "Refused: an absolute path is outside this world.";
  "Refused: that path resolves outside this world."; .env or .env.*: "Refused: that file holds this estate's keys, and they are
  never printed (RULE 7). Nothing was read."; an ignored file: "Refused: this world's git ignores <rel>, so it is not part of
  what changed -- ..."; a new file: "This file is new -- git has never seen it, so there is nothing to compare it against. Its
  contents:\n\n<file>"; "That file has no recorded change, and could not be read: <err>"; "not a repository -- nothing to review".
- **MAINTENANCE** tools.go:613-618; gitstate.go:231-323.  **TIME** 208 ms.  **USES** look before saving.

#### git_commit (T33) · W
- **AUTHOR** "save this world's work: stages everything (or only the files named, one per line) and records it under a message
  you write".
- **USE** `{"message":"fix X","files":"a.py\nb.py"}` (message required; files optional, one per line). HELD from the Agent tab.
- **CARE** Is it a repository; a message; every file jailed; `git add -A` (or `add -- <paths>`) 60 s; `diff --cached
  --name-only` 30 s; `commit -m` 120 s; `rev-parse --short HEAD`. "Saved %d file%s as %s: %q". Refusals: "Refused: this world is
  not a repository -- there is nothing to save, and nothing to lose."; "Refused: a save needs a message saying what it is.
  Nothing was staged."; "Refused: an absolute path is outside this world (%s)."; "Refused: that path resolves outside this world
  (%s)."; "Refused: nothing was staged -- <git's first line>"; "Nothing to save: the tree already matches the last save.";
  "Refused: the save did not land -- <git's first line>".
- **MAINTENANCE** tools.go:623-628; gitctl.go:107-151.  **TIME** ran 2026-10-14 (sitting 381), not timed.  **USES** the GitHub tab's Save.

#### git_push (T37) · W
- **AUTHOR** "send saved work to the remote; refuses by name while the estate's wall is shut, and says so when it binds a branch
  to origin for the first time".
- **USE** `{}`.  **CARE** The network. Is it a repository; the wall; the branch; main that origin has (refused: a pull
  request only); `push [--set-upstream origin <branch>]` 300 s. "Sent %s to origin.\n\n%s" plus "This branch had never been sent
  before; it now follows origin/%s." or "Nothing to send: the remote already has everything here." Refusals: "Refused: Sending
  is OFF. The estate's wall (MANJUEL_GIT_REMOTE) is shut, so nothing here reaches the remote. That dial is the operator's alone
  -- this door reads it and never opens it."; "Refused: this world has no branch to send (no commits yet)."; "Refused: %s is on
  GitHub, and GitHub takes a change to it only through a pull request whose checks have passed. ..."; "Sending refused by the
  remote -- <first>\n\n<out>".
- **MAINTENANCE** tools.go:630-635; gitctl.go:157-201.  **TIME** ran 2026-10-14 (sitting 381), not timed.  **USES** the GitHub tab's Send.

#### git_pull (T36) · W
- **AUTHOR** "fetch and catch up, fast-forward only; refuses over unsaved work, and refuses to join two histories that both moved".
- **USE** `{"project":"research"}`.  **CARE** The network; the wall; unsaved work; `pull --ff-only` 300 s. "Refused: Fetching
  is OFF. ..."; "Refused: there is unsaved work here. Save it first -- a fetch over a dirty tree is how work goes missing.";
  "Fetching refused -- <first>\n\nThis pulls fast-forward only: if this world and the remote have both moved, joining them is
  your call, not the door's.\n\n<out>"; "Already in step: the remote has nothing this world does not."; "Fetched and caught up.".
- **MAINTENANCE** tools.go:637-642; gitctl.go:208-229.  **TIME** 2026-10-16, sitting 403: ran on his card.
- **USES** bringing main down after a merge.

#### git_branch (T32) · W (list reads)
- **AUTHOR** "the lines of work: list them (...), or open, switch to, land (onto the main line, fast-forward only, from the main
  line, over saved work), or close one".
- **USE** `{"action":"list"}` (the default) | `{"action":"new","name":"fix-x"}` (also open) | switch (use) | land | close
  (delete).
- **CARE** A name may not be empty, begin with "-", carry a space or .. ~ ^ : ? * [ \ @{, or end in "/" or ".lock": "Refused:
  name the branch.", "Refused: a branch name may not begin with '-' -- git would read it as a flag.", "Refused: %q is not a lawful
  branch name (%q is not allowed).". list -> {world, on, branches:[{name, current, main, upstream, sent, when, subject}],
  why_not_land?}. new -> `switch -c`, "Opened %q and moved you onto it. It exists only here until you send it." switch ->
  "Refused: there is unsaved work here. Save it first, or it follows you onto the other line and confuses both." or "You are now
  on %q." land (refused onto main where GitHub has it) -> "Refused: the main line is not landed onto itself."; "Refused: you
  are standing on %q. Move to %q first (switch), then land %q onto it."; "Refused: there is no line named %q here."; "Refused: %q
  cannot land as a fast-forward -- ..."; "Landed %q onto %q, fast-forward. ..." close (`branch -d`) -> "Refused: you are standing
  on that line. Move to another one first."; "Refused: %q holds work that is not on any other line. Closing it would lose that
  work. Merge it first, or close it yourself with `git branch -D %s` if you mean to discard it."; "Closed %q. Its work is already
  on another line." Unknown: "Refused: %q is not something this does. ..."
- **MAINTENANCE** tools.go:644-649; gitctl.go:832-997.  **TIME** 318 ms (list).  **USES** lines of work; needed before aider_run.

#### git_pr (T35) · S
- **AUTHOR** "pull requests, the one GitHub-side object his ruling of 2026-10-07 let into the door: list ...; open one from the
  line of work he stands on into the main line ...; or merge one on GitHub by its number, or by its line ... as a merge commit
  ... Behind the same wall as every send (GIT_REMOTE). His glass alone may call it".
- **USE** `App.tool('git_pr', {action:'merge', number:33, wait:10})`; action list | open | merge; number (a number, or digits
  with or without "#"); line; wait (whole minutes 0 to 30). From the Agent tab: refused (S).
- **CARE** Runs `gh` (GH_PROMPT_DISABLED=1, GH_PAGER=cat, NO_COLOR=1, GH_NO_UPDATE_NOTIFIER=1), behind the wall. list -> `gh
  pr list --state open --json number,title,headRefName,baseRefName,url,statusCheckRollup` (30 s) -> {"pull_requests":[{number,
  title, line, into, url, checks none|pending|failed|passed}]}. open -> refused when on no line, on main, over unsaved work, or
  when GitHub's copy of the line differs ("Refused: GitHub does not have %q exactly as it stands here. Send it first, then open
  the pull request."); then `gh pr create --base <main> --head <line> --title <last subject> --body "The saves on <line>:..."`.
  merge -> reads the pull request (`gh pr view`), re-reads every 30 s up to `wait` minutes, and merges `gh pr merge <n> --merge
  --match-head-commit <oid>` (120 s) only when it is open, into the main line, every check passed and no conflict; then brings
  main down. Its refusals name each case: "no checks have run", "checks are still running", "checks FAILED. Mend the line, send
  it again, and merge when they pass.", "conflicts with %q", "is %s, not open", "goes into %q, not the main line %q", "gh did
  not say which save ..."; success "Merged pull request #%d on GitHub as a merge commit: %q, %s into %s."
- **MAINTENANCE** tools.go:651; gitpr.go:341-374.  **TIME** 837 ms (list).
- **USES** the GitHub tab's Pull requests; Steward's own send uses `gh` directly.

#### hold_list (T41) · R (exempt from holds)
- **AUTHOR** "the writing calls parked waiting for the operator's hand, and whether holding is armed at all".
- **USE** `App.tool('hold_list', {}, true)`; the glass polls it every 3 s. project is ignored (every tenant's queue).
- **CARE** Disarmed: {"armed":false,"held":[],"why_not":"The door was started WITHOUT --auth, so it cannot tell a seat from the
  glass and nothing is being held. Restart it with --auth and a service wire to arm this."}. Armed, not the glass: "Refused: the
  hold queue is the operator's. This asks who is calling, and the answer was not his glass." Armed, the glass:
  {"armed":true,"held":[{id, tool, caller, project, when, args}]} in id order, a declared secret or any atl_ value shown as
  "[withheld: a secret; the parked call keeps it]". "Refused: the hold queue is not reachable from here."
- **MAINTENANCE** tools.go:653-658; holds.go:295-349.  **TIME** 4 ms.  **USES** the dock. The engine cannot read it (door_call
  watches the hold logs instead).

#### hold_answer (T40) · W (exempt from holds; the glass's alone, checked inside)
- **AUTHOR** "approve or deny one parked call by id; the operator's act alone, and it runs exactly the call that was parked".
- **USE** `App.tool('hold_answer', {id:'hold_1792…_181_git_branch', decision:'approve'})`; decision approve | deny.
- **CARE** In order: "Refused: the hold queue is not reachable from here."; "Refused: answering a hold is the operator's act
  alone, and this call did not come from his glass. RULE 6."; "Refused: name the hold to answer, e.g. id=hold_1757..."; "Refused:
  a hold is answered approve or deny, got %q."; "Refused: no hold called %s is waiting. It may have been answered already, or
  the door restarted -- a restart drops the queue, and a dropped hold means the call never ran."; "Refused: %s carries no world
  to run in, so %q was not run and nothing was written."; "Denied %s. %q was not run and nothing was written."; "Refused: %q no
  longer exists at this door, so the held call cannot be run."; "Approved %s and %q errored: %v\n\n%s"; "Approved %s. %q
  ran:\n\n%s". One row to the held world's state/holds.jsonl.
- **MAINTENANCE** tools.go:660-665; holds.go:351-423.  **TIME** 44 to 610 ms.  **USES** the cards' Approve and Deny only.

#### shell_run (T79) · S (and parks its own writing lines)
- **AUTHOR** "the operator's own typed shell, run in this world: a Git Bash command or a Python entry (Python keeps its names
  between entries). A plain look runs at once; anything that writes, deletes, installs, reaches the network, or saves or sends
  work waits for his approval; a secret, client material or a path outside the ground is refused by name. His glass alone may
  call it".
- **USE** `App.tool('shell_run', {shell:'bash', command:'ls law'})`; shell bash | python | pwsh (powershell); command up to 8000
  characters; timeout seconds (default 30, at most 300; the page sends 300); reset (python only).
- **CARE** Answers one JSON: {shell, state ran|held|refused, class read|write|refused, why[], hold, approved, exit, ms,
  timed_out, truncated, output (64 KiB, every secret value shown "[withheld: a secret]"), note, command}. In order: the glass
  only ("refused: the shell is the operator's own hand and is offered to his glass alone"); the shell named ("refused: name the
  shell, bash, python or pwsh (got %q)"); "refused: nothing to run -- type something"; "longer than 8000 characters; it is not an
  entry, it is a file"; THE CHAIN: when law/chain.jsonl and law/law.py exist, `python law/law.py verify` (60 s, cached on law/'s
  names, sizes and times) must pass, else "THE CHAIN: the law does not verify -- <note>. No run proceeds on a law that cannot be
  trusted"; then the gate (5.6) judges read, write or refused; a write parks a card; a read runs. Bash is Git Bash (found by the
  git on PATH; "Git Bash is not installed here (Git for Windows ships it); a plain `bash` on this PATH may be the WSL stub, which
  the door never uses"), run as `bash -c 'eval "$ATLAS_SHELL_COMMAND"'`; pwsh as `pwsh -NoProfile -NonInteractive -Command ...
  Invoke-Expression $env:ATLAS_SHELL_COMMAND` (every line parks); python is one long session per world judged by its own syntax
  tree, never by running it. The child gets a built environment (system variables plus GIT_OPTIONAL_LOCKS=0,
  GIT_TERMINAL_PROMPT=0, GIT_PAGER=cat, PYTHONDONTWRITEBYTECODE=1, PYTHONUTF8=1, PYTHONIOENCODING=utf-8, NO_COLOR=1), no keys;
  the home as its folder; its whole tree killed past the timeout. Rows: shell_refused, shell_held, shell_ran (note "<shell>
  <class> exit=<n> <ms>ms: <command>").
- **MAINTENANCE** tools.go:673-678; shell.go:338-509; shellgate.go; shellpy.go.  **TIME** 6,934 runs: median 61 ms, slowest the
  300 s cap.  **USES** his typed look or change; never a seat's.

#### aider_run (T1) · S (runs at once, no card)
- **AUTHOR** "the operator's own Aider, run on the files he names: it copies them into a scratch folder, runs Aider headless on
  the copies behind a wall (...), and writes the changed files back only while the world stands on a line of work, only if every
  Python file still parses; the answer carries the diff, what Aider said and a run id to take it back with. His glass alone may
  call it".
- **USE** `App.tool('aider_run', {message:'rename x to y', files:'manjuel/a.py'})`; message up to 4000 characters; files 1 to 4
  (newline, comma or ";"); context up to 4 read-only files; timeout default 600 s, at most 1200.
- **CARE** Answers {state, class, why[], run, model, line, changed:[{file, new, added, removed}], diff (64 KiB), withheld, said
  (16 KiB), tokens, ignored[], guarded[], exit, ms, timed_out, truncated, note}. Each file: the shell's refusals, the jail, the
  never-written list (law, agents, skills, state, sessions, logs, flows, memory, worlds, .git, binaries, proof stamps,
  CLAUDE.md...), on a repository standing on a line of work (not main, not detached), at most 64 KiB, UTF-8, one line ending.
  Aider must be in aider/venv; the model is the coding seat's (agents/expert_coder.md, Model Target and Context, default 8192),
  on the loopback rack; one run at a time; the model warmed (keep 10 minutes, 180 s). Aider runs in a scratch git folder behind
  a Python audit-hook wall (writes only to its scratch, home, temp and history; nothing read from the ground or the profile;
  loopback only; no child processes); the wall must announce "ATLAS-AIDER-GUARD <nonce> armed" or the run is thrown away.
  Changes are diffed, every .py must parse, every target must still match its bytes from before; then all are written or none.
  runs/<id>/ keeps before/, after/ and manifest.json (the newest 30). Refusals in why[], among them "nothing to ask: write what
  Aider should change"; "name the files Aider may change: it works on the files it is given, and none were"; "...the main line is
  the operator's (RULE 6): open a line of work first ..."; "Aider is not installed in this world: there is no aider/venv here
  ..."; "the coding seat's model %q is not on this machine's rack; Aider drives local models only (RULE 4)"; "an Aider run is
  already going; wait for it, one model is in the memory"; "THE WALL did not announce itself, ... nothing was written". Success
  note: "Written on the line of work `%s`; unsaved until git_commit saves it there. ..." Rows aider_ran, aider_refused.
- **MAINTENANCE** tools.go:687-692; aider.go:776-1175; aiderguard.go:49-223.  **TIME** 34 writing runs: 9.8 to 433 s, most 60
  to 260 s; two timeouts at 600 s.  **USES** a small model edit to up to four small files on a line; not for seats.

#### aider_undo (T3) · S (runs at once)
- **AUTHOR** "take one Aider run back: the files it changed are put back as they were, if nothing has changed them since; his
  glass alone may call it".  **USE** `{run:'a20261007-231845-1427'}` (shape a, 8 digits, -, 6 digits, -, 4 hex).
- **CARE** Each file must still hash to its "after" value; it restores from before/ or removes new files (not all-or-nothing);
  marks the manifest undone; row aider_undone. "name the run to take back, as the run's own id (a1234...); got %q"; "no record of
  run %s (a run's record is kept for the last 30 runs; an older one is git's to take back)"; "run %s was already taken back at
  %s"; "%s is not as Aider left it (it has changed since, or is gone), so taking the run back would lose what came after; take
  back the later run first, or use git"; "the copy of %s as it was, kept beside run %s, is missing or does not match its record".
- **MAINTENANCE** tools.go:693-698; aider.go:1199-1278.  **TIME** not measured.  **USES** reverting one Aider run before a save.

#### aider_status (T2) · R
- **AUTHOR** "whether Aider can run in this world now and with what: installed, its version, the coding seat's model and
  window, whether the rack has the model, whether the world stands on a line of work, and the last runs".
- **USE** `App.tool('aider_status', {}, true)`.  **CARE** {installed, version, folder, model, context, rack silent|up, on_rack,
  busy, line, on_line, max_files 4, max_context 4, budget_kb, runs (the last 8), why[]}. It runs git and asks Ollama (its comment
  says it starts nothing).  **MAINTENANCE** tools.go:699-704; aider.go:1311-1372.  **TIME** 142 ms.  **USES** the Aider tab's title.

#### file_edit (T19) · S (always parks first)
- **AUTHOR** "the operator's own exact edit of one text file in this world: ... the old text must appear exactly once; the file
  keeps its own line endings; the first call writes nothing and parks itself with the change line by line, and it writes only
  when he approves that card and the file still gives exactly that change. ... His glass alone may call it".
- **USE** `App.tool('file_edit', {filepath:'manjuel/x.py', old:'a = 1', new:'a = 2'})` -> held; his Approve writes.
- **CARE** Answers {state held|written|refused, filepath, hold, why[], change[] ("at line N", "- old…", "+ new…"), note}.
  Refusals: "the old text is empty: name the exact passage to replace"; "the old and the new text are the same: there is
  nothing to change"; "name the file as filepath, relative to this world"; the jail, the shell's refusals and the never-written
  list (agents/ and skills/ files ARE allowed); "an engine is open on %q (sitting %s): nothing in this ground is edited while the
  operator's sitting is open (SITTING LAW 5): close it first"; "%q has an open sitting (...)"; "there is no such file: file_edit
  changes a file that is already there"; "that is a folder, not a file"; over 4 MiB; "the file is not UTF-8 text"; "the file mixes
  two line endings, so an edit cannot keep what it has"; "the old text is not in the file exactly as given: nothing was written";
  "the old text appears %d times: give a longer passage that appears once"; disarmed, "the door was started without --auth, so
  no card can be shown: nothing was written". On his Approve the change is worked out again: "the file has changed since the
  card was shown: nothing was written. Ask again", else "Wrote %s, keeping its %s line endings. The suites are his to run."
- **MAINTENANCE** tools.go:706; edit.go:150-268.  **TIME** about 5 s with his click.  **USES** one exact change while no sitting is open.

#### law_status (T44) · R
- **AUTHOR** "the laws as the chain holds them: every law file, how far it is sealed, what is draft below the ledger's seal,
  and the chain's own verdict (law.py verify); and why the two writing tools would refuse right now, if they would".
- **USE** `{}`.  **CARE** Reads law/ and law/chain.jsonl; runs `<python> law/law.py verify` (30 s). A link is a chain row of
  kind "link" whose doc's first line reads "(COUNSEL|RULING|DIRECT|REFUSED) by <who> -> law/<file>.md sha256:<64 hex>[ bytes:N]".
  ok = law.py exits 0 and says "the law chain proves whole: N links, head H". Per file: "not on the chain", "changed since
  sealed", "partly sealed" (with draft_bytes) or "sealed". JSON {world, ok, verdict, links, head, files:[{name, bytes,
  fingerprint, state, sealed_bytes?, draft_bytes?, kind?, by?, links?}], draft_bytes, sitting_open, why?}; why is the writers'
  refusal now: an open engine or sitting (SITTING LAW 5), no law/law.py, no law/LAW_LEDGER.md. [err] "this world carries no law/
  folder: <err>".
- **MAINTENANCE** tools.go:712-717; law.go:45-285.  **TIME** 146 ms.  **USES** before law_add or law_seal.

#### law_add (T42) · S (runs at once; his click is the decision)
- **AUTHOR** "the operator's own hand: set a law -- one numbered entry appended to law/LAW_LEDGER.md, BELOW its seal, as a draft
  until he seals it. Refused while a sitting is open and over a chain that does not prove whole; the chain is walked again after
  the append and the entry is taken back if it refused. His glass alone may call it".
- **USE** `App.tool('law_add', {title, text, from})` (the Laws page): title one line of 3 to 120 characters, text 20 to 8000,
  from up to 600.
- **CARE** Normalises the words (CR LF to LF; no control characters but newline and tab; trailing blanks trimmed); takes the law
  lock; refuses an open sitting; verifies the chain; the ledger must end in a newline and carry no CR; numbers the entry one past
  the highest "## N. "; appends "\n---\n\n## N. <title>\n\n```\nentered:  YYYY-MM-DD, on the operator's word\nfrom:     <from,
  else his word, through the glass's Laws page>\n```\n\n<text>\n"; verifies again and truncates back if it refuses. Answers
  {state added|refused, entry?, title?, why?, draft_bytes}. Refusals: "the words carry a control character or are not text"; "the
  title is one line of 3 to 120 characters"; "the law is 20 to 8000 characters; this one is %d"; "where it came from is at most 600
  characters"; "a line that opens like a heading (## ...) or is a bare --- would split the entry in two; indent it or reword it";
  the four writers' refusals; "the chain does not prove whole right now, and nothing is laid on a chain that refuses: ..."; "the
  ledger does not end on a line break, or carries a carriage return: it is a file to fix by hand, not by appending"; "the chain
  refused after the entry was written, so it was taken back: ...". Rows law_added ("entry N :: <title>"), law_refused.
- **MAINTENANCE** tools.go:718-723; law.go:289-413.  **TIME** not measured.  **USES** setting a law as a draft (entry 11, SITTING
  LAW 11, was set this way on 2026-10-16).

#### law_seal (T43) · S (runs at once)
- **AUTHOR** "the operator's own hand: seal the ledger as far as it is written (law.py seal on law/LAW_LEDGER.md) -- what is
  below the seal becomes law and is frozen; an entry sealed is changed only by a new entry that amends it. Refused while a
  sitting is open and when nothing is below the seal. His glass alone may call it".
- **USE** `App.tool('law_seal', {note})`; note one line, up to 240 characters (empty: "sealed from the glass's Laws page,
  YYYY-MM-DD").  **CARE** The law lock; the writers' refusals; the chain must prove whole; draft bytes must exist; runs
  `<python> law/law.py seal LAW_LEDGER.md --note <note>` (30 s). {state sealed|refused, sealed_to?, draft_bytes, verdict?, why?}.
  "the note is one line of plain text, at most 240 characters"; "the chain does not prove whole right now, and nothing is sealed
  over a chain that refuses: ..."; "nothing is written below the ledger's seal, so there is nothing to seal"; "law.py would not
  seal: ...". Rows law_sealed ("ledger sealed to byte N :: <note>"), law_refused.
- **MAINTENANCE** tools.go:724-729; law.go:415-468.  **TIME** not measured.  **USES** making drafts law; never editing a sealed one.

#### git_tag (T39) · W (list reads)
- **AUTHOR** "the marks a version is cut at: list them with what GitHub has, cut one at a commit whose declared version it must
  equal, send one to GitHub by name, or remove one that never left this machine".
- **USE** `{"action":"cut","name":"v0.2.6","message":"..."}`; action list (default) | cut (new) | send (push) | remove (delete);
  name; message; at (a commit, default HEAD).
- **CARE** list: for-each-ref (15 s), and while the wall is open `ls-remote --tags origin` (30 s, the network) -> {world,
  tags:[{name, at, when, subject, sent, sendable, why_not?, removable, why_not_remove?}], declared, declared_by, next,
  sent_known}. cut: the name must be vMAJOR.MINOR.PATCH ("Refused: name the mark, e.g. v0.1.5.", "Refused: %q does not begin
  with 'v'. ...", "Refused: %q is not vMAJOR.MINOR.PATCH -- ...", "Refused: %q carries %q, which is not a number. ..."); a
  message ("Refused: a mark needs a message saying what this version is. ..."); a commit; not already a mark ("Refused: %s already
  exists here, on %s. A mark is never moved -- ..."); on the main line ("Refused: %s is not on the main line (%s). ..."); a clean
  tree at HEAD ("Refused: there is unsaved work here. ..."); the version declared at that commit (VERSION, else pyproject.toml)
  must equal the name ("Refused: the mark and the ground disagree. ...") and every version stamp there must agree ("Refused: %s
  says %s, but not every version stamp at that commit agrees -- ..."); then `tag -a <name> -m <message> <sha>` -> "Cut %s at %s
  (%q), against %s saying %s.\n\nIt is on this machine only -- sending it is a separate button." send: the wall; the mark exists;
  its commit is on origin's main ("Refused: %s is on %s, and origin's main line does not carry that commit -- ..."); `push origin
  refs/tags/<name>` (300 s, never --tags) -> "Sent %s to origin." remove: only a mark GitHub does not have ("Refused: GitHub has %s.
  ... Cut the next number instead."; "Refused: this door cannot tell whether GitHub already has %s. ..."); `tag -d`.
- **MAINTENANCE** tools.go:731-736; gitctl.go:250-820.  **TIME** 2689 ms (list, asking GitHub).  **USES** the release's marks.

#### git_remote (T38) · R
- **AUTHOR** "where this world sends: each remote by name, its host, and whether the estate's wall is open".  **USE** `{}`.
- **CARE** `git remote -v` (15 s) -> {world, remotes:[{name, url, host}], remote_allowed}. As it stands `url` is returned whole,
  any user:token@ in it included.  **MAINTENANCE** tools.go:738-743; gitctl.go:1031-1083.  **TIME** 135 ms.

#### records (T71) · R
- **AUTHOR** "the estate's own documents sorted by what they are (doctrine, record, spec, agents, commands, skills, logs); a kind
  listed, or one document served whole with a sha256 receipt".
- **USE** `{"name":"law/LAW_LEDGER.md"}` or `{"kind":"agents"}` or `{}`.
- **CARE** Only *.md, not recursive, in the root, law/ (doctrine, sealed), agents/, skills/ and logs/ (the newest 60 only).
  Root kinds: doctrine CLAUDE.md; record CHANGELOG, DAYBOOK, HANDOFF, SEAT_LOG, TASKS, memory; spec SPEC, SPEC_CONTROL_CENTER,
  DESIGN, SYSTEM_DESIGN, BUILDMAP, BUILDPATH, RUNBOOK, QUICKSTART, README, TESTING, CONTRIBUTING, REFUSALS, parity, rack;
  commands commands, pipelines, agents; else other. A name is matched only against that listing, never joined to a path. {world,
  count, kinds:[...]} | {world, kind, count, documents} | {world, name, kind, sha256, bytes, modified, sealed, text}. [err] "record
  %q is listed but unreadable: ..."; "no record named %q in %s. Kinds carried: ..."; "no kind %q in %s. Kinds carried: ...".
- **MAINTENANCE** tools.go:745-750; records.go:61-276.  **TIME** 17 ms.  **USES** reading any estate markdown, the sealed laws too.

#### seats (T78) · R
- **AUTHOR** "the world's own seat declarations and the pipelines they stand in, from agents/ and pipelines.md".  **USE** `{}`.
- **CARE** Each agents/*.md: name (its first "## " heading, else the file), every "- **Key:** value" field, the prompt (after an
  empty System Prompt field), and which pipeline steps name it (from pipelines.md's "## Pipeline: <name>" blocks, "when: X" in a
  step's note). {world, seats:[{file, name, fields{}, field_order[], prompt?, prompt_chars?, stands_in:[{pipeline, step, note?,
  when?}]}], seats_error?, pipelines_error?}. No refusals.
- **MAINTENANCE** tools.go:752-757; seats.go:36-159.  **TIME** 8 ms.  **USES** the seat cards; a seat is changed with file_edit.

#### proofs (T60) · R
- **AUTHOR** "what this world has PROVED, from its own record: the suites' stamp, every live standup, the parity history".
- **USE** `App.tool('proofs', {}, true)`.  **CARE** tests/last_run.json whole (suites); tests/run_history.jsonl's standup rows;
  sessions/parity_history.jsonl; sessions/sessions.jsonl folded by n (sittings, tolled, runs, still_open, the last 12);
  SEAT_LOG.md's toll headings; logs/standup_* names; cached by size and time. Each piece may be missing ("never run in this
  world", "unreadable: <err>"). No refusals.
- **MAINTENANCE** tools.go:759-764; proofs.go:41-274.  **TIME** 43 ms.  **USES** the proof panels; the engine's `proved` reads the
  same stamp.

#### projects (T53) · R
- **AUTHOR** "what the maker made: every project under projects/ with its versions read from its own history, or one project's
  page as it stands (or as a version was)".
- **USE** `{"action":"page","name":"snake","version":2}`; action list (default) | page; name lowercase letters, digits and
  hyphens; version a number (empty or 0: as it stands).
- **CARE** Every folder on the way a plain folder (no links); every git call names the project's own history (`--git-dir
  <dir>/.git --work-tree <dir>`, 10 s). list -> {world, count, projects:[{name, versions:[{n, sha, note, when}], bytes, lines,
  updated, error?}]}, newest first; page -> {world, name, version, sha, bytes, text} (index.html, up to 1 MiB). [err] "projects
  takes action list or page, not %q"; "no project named %q -- ..."; "REFUSED -- %q is a link, not a folder inside projects/.
  ..."; "%q is a folder with no history of its own, so it is not a project"; "a version is a whole number, not %v"; "%s has no
  index.html of its own yet"; "there is no version %d -- %s has versions 1 to %d".
- **MAINTENANCE** tools.go:769-774; projects.go:46-297.  **TIME** 963 ms.  **USES** the maker's pages and versions; never edits.

#### state_matrix (T81) · R
- **AUTHOR** "state = fold(record) index of the named project".  **USE** `{}`.
- **CARE** Reads THE_ROAD.md, STATE_OF_BUILD.md and SEAT_LOG.md (or the manifest's): "THE MATRIX — state = fold(record)\n  road
  <N bytes|absent>\n  state <…>\n  log <…>" and JSON {project, equation, rows:[{key, present, bytes, head}]}. Never refuses.
- **MAINTENANCE** tools.go:776-781, 3377-3425.  **TIME** 7 ms.  **USES** whether a ground carries a road, a state and a log.

#### read_plan (T70) · R
- **AUTHOR** "HLD/LLD/road documents by name; absent name denied honestly".  **USE** `{"which":"road"}` (required).
- **CARE** The manifest's plans, then road -> THE_ROAD.md, state -> STATE_OF_BUILD.md, catalog -> THE_CATALOG.md, acceptance ->
  ACCEPTANCE.md, charter -> CHARTER.md, then plans/<which>: "<name> · sha256 <hex>\n\n<body>". [err] "read_plan needs a name —
  e.g. road, state, catalog, acceptance, charter, or a plans/ path"; "No such plan %q for project %q. ..."; "plan %q present in the
  map but unreadable: %s".  **MAINTENANCE** tools.go:783-788, 3550-3566; tenant.go:135-176.  **TIME** 5 ms (FAULT in research:
  none of the five names reads).  **USES** atlas's plans.

#### ask_steward (T4) · W
- **AUTHOR** "the weighed ruling with receipts, never raw model output; one-shot under the ask lock".  **USE** `{"question":"..."}`.
- **CARE** Needs `--engine name=cmd` (not --manjuel), which the door is not started with, so as wired today it refuses: "ask_steward
  has no engine wired for project %q: nothing to wake. The operator wires one with --engine." Others: "ask_steward needs a
  question — he cannot weigh the empty string"; "REFUSED — ask_steward will not boot or forward to a read-only ground (estate/,
  secondbrain/, manjuel core). ..."; "REFUSED — the weighing did not finish inside 600 seconds; ..."; "REFUSED — the engine did not
  answer (exit %v): %s"; "REFUSED — the engine said nothing".
- **MAINTENANCE** tools.go:790-795, 3427-3511.  **TIME** 10 ms (the refusal).  **USES** none today; run_start and /drive are the roads.

#### remember (T73) · W
- **AUTHOR** "sole write tool; testimony stamped generated; staged for operator ascend" (as it stands the words are stale: the
  door has forty-odd writers).  **USE** `{"text":"..."}`.
- **CARE** Appends {"ts","testimony":true,"project","text"} to <home>/state/remembered.jsonl under the ask lock: "REMEMBERED
  (testimony, staged for operator ascend) — <ts> · sha256 <hex>\n<text>". [err] "remember needs some text to hold". Nothing in the
  door reads that file back; the engine's memory is memory.md (the `remember` skill and /memory).
- **MAINTENANCE** tools.go:797-802, 3513-3548.  **TIME** 6 ms.  **USES** none over the engine's own memory path.

#### mesh_enroll (T49) · W
- **AUTHOR** "bind a mesh voice: actor -> verifying key (B2)".  **USE** `{"member":"steward","pub":"<128 hex>"}`; member
  lowercase (a-z 0-9 _ . -), pub 64 bytes of hex, a curve point.
- **CARE** Writes <home>/state/mesh/members.json {actor:{pub, mark}} (0600, atomic); the same key again is a no-op. "ENROLLED %q
  on channel %q · mark %s". [err] "mesh_enroll needs a member id and a pub (64 bytes hex)"; "refused: actor %q is not a mesh name
  (lowercase id)"; "refused: pub for %q is not 64 bytes hex"; "refused: pub for %q is not a curve point"; "refused: %q already
  bound to another key — re-keying rides an operator epoch note, never a rewrite".
- **MAINTENANCE** tools.go:808-813, 3628-3641; mesh/store.go:73-107.  **TIME** not measured.

#### mesh_post (T50) · W
- **AUTHOR** "post one signed message on the channel chain (B2)".
- **USE** `{"actor":"steward","to":"@channel","text":"..."}`; to a member | @channel | @everyone; mode open (default) | sealed;
  kind mesh (default) | cite | reconcile | breach_attempt; cites (16, 40 or 64 hex).
- **CARE** Signs with MESH_KEY_<ACTOR> from the door's environment; the actor is the caller's word. Appends
  state/mesh/chains/<actor>.jsonl and head.jsonl (ledger.jsonl when sealed); an entry's hash is sha256(previous ‖ canonical body).
  "POSTED n=%d · <hash16> · head <hash16>\n  face: <first 160 | (sealed: ciphertext at rest)>". [err] "mesh_post needs text and
  to (a member, @channel, or @everyone)"; "mesh_post needs an actor — every message names its pen"; "REFUSED — chan %q is not your
  ground %q. ..."; "refused: kind %q is not a mesh kind"; "refused: every message says what it is — empty text posts nothing";
  "refused: actor %q is not enrolled — mesh_enroll first"; "refused: destination %q is not this estate — egress is a packet, not a
  message"; "refused: citation %q is not a hash (16/40/64 hex)"; "refused: citation %q names nothing in channel %q".
- **MAINTENANCE** tools.go:815-820, 3643-3677; mesh/store.go:177-337.  **TIME** not measured.

#### mesh_read (T51) · R
- **AUTHOR** "read the channel-head index or one actor's chain (B2)".  **USE** `{"actor":"steward","last":5}`; reveal (a boolean)
  opens sealed entries with the door's keys -- as it stands any allowed caller may.  **CARE** "n=%d %s %s -> %s · <hash16>\n
  <face300 | WITHHELD: why>" or "channel %q holds nothing yet".  **MAINTENANCE** tools.go:822-827, 3686-3709.  **TIME** 4 ms.

#### mesh_chain (T47) · R
- **AUTHOR** "rewalk every pen plus the head: EMPTY|INTACT|FLIP|TAMPER|FORGERY (B2)".  **USE** `{}`.
- **CARE** "MESH <overall> — <detail>\n  <chain> <verdict>…".  **MAINTENANCE** tools.go:829-834; store.go:437-499.  **TIME** 3 ms.

#### mesh_cite (T48) · W
- **AUTHOR** "cite chain hashes by a signed cite entry (B2)".  **USE** as it stands the hashes must be sent as `cites` (the
  schema says `targets`, which the code never reads): `{"actor":"steward","cites":"<hash>","text":"why"}`.
- **CARE** As mesh_post with kind cite: "CITED %d target(s) at n=%d · %s · head %s". [err] "mesh_cite needs targets (hash cites) and
  text saying why"; "mesh_cite needs an actor — every cite names its pen".  **MAINTENANCE** tools.go:836-841, 3732-3760.
- **TIME** 8 ms (FAULT: the argument name).

#### rack_list (T62) · R
- **AUTHOR** "live tier ladder of lawful local voices (F1)".  **USE** `App.tool('rack_list', {}, true)`.
- **CARE** GET <OLLAMA_HOST, loopback only>/api/tags (10 s): "THE RACK — lawful local voices (%d), loopback only\n  scout
  (≤3GB):\n    - name · X.XGB · family…" (scout up to 3 GB, voice up to 8 GB, mind above), or "THE RACK — <err>: nothing
  fabricated." [err] "refused: OLLAMA_HOST %q is not a door" / "... is not loopback — the rack never reaches outward".
- **MAINTENANCE** tools.go:845-850, 1708-1718; rack/rack.go:60-154.  **TIME** 26 ms.  **USES** what models exist.

#### rack_ask (T61) · W
- **AUTHOR** "routed ask, witnessed to the ledger (F1)".  **USE** `{"question":"...","voice":"llama3.2:latest"}`.
- **CARE** The guard first (an injection poke blocks; email, SSN, card, key and phone redacted; flags kept); the voice named,
  else the first speaking voice on the ladder; `/api/generate` (600 s, under the global ask lock); appends
  state/rack_ledger.jsonl {ts, kind "rack_ask", voice, question, answer, flags}. "voice %s answered (witnessed %s)[ [flags:
  …]]:\n<answer>". [err] "rack_ask needs a question — no voice is asked nothing"; "refused: I read that as an attempt to move my
  gate. ... (matched: \"…\")"; "refused: voice %q is not on the rack — nothing fabricated"; "refused: voice %q is an embedding
  model, not a speaking voice"; "refused: no speaking voice on the rack"; "voice %q left the answer unfinished — refused, not
  truncated"; "voice %q said nothing — refused".
- **MAINTENANCE** tools.go:854-859, 1725-1763; rack/ask.go; guard/.  **TIME** 332 ms (llama3.2).  **USES** one bare-model question.

#### rack_open (T63) · R
- **AUTHOR** "expanded context bundle at a depth (F1)".  **USE** `{"voice":"llama3.2:latest","depth":2}` (depth a NUMBER, 1 to 3).
- **CARE** "CONTEXT BUNDLE — %s at depth %d (%s)" and the voice's card; depth 2 adds the ladder and the last five ledger lines;
  depth 3 the get_in_line pack. [err] "refused: depth is 1, 2, or 3"; "refused: voice %q is not on the rack — nothing fabricated".
- **MAINTENANCE** tools.go:864-869, 1767-1833.  **TIME** 43 ms.

#### memory (T46) · R
- **AUTHOR** "cited answers from local memory, or refusal (F1-01)".  **USE** `{"question":"toll"}`; voice.
- **CARE** Filters state/rack_ledger.jsonl (the voice exactly; the question as a substring, any case); none given, the latest:
  "ENVELOPE — %q (%d cited)" and up to five. [err] "refused: the ledger is empty — no cited memory."; "refused: no cited memory for
  %q — never invented, never uncited."  **MAINTENANCE** tools.go:873-878; rack/memory.go.  **TIME** 4 ms.
- **USES** recalling rack_ask answers; not memory.md.

#### rack_plan (T64) · R
- **AUTHOR** "VRAM fit check for a model set before it runs (N3)".  **USE** `{"voices":"llama3.2:latest,qwen3.5:4b"}` or models
  as a JSON string [{name, size}] (up to 64).
- **CARE** Budget 15e9 bytes; graph overhead 1.5e9; context 4096; cache bytes a token scout 200k, voice 500k, mind 1M. "VRAM PLAN
  — FITS|OVER · total …GB / budget …GB", the rows, "evict to fit: …". [err] "rack_plan models must be JSON [{name,size}]: %s";
  "refused: rack_plan caps at 64 models"; "refused: model needs a name and a non-negative size"; "refused: voice %q is not on the
  rack — nothing fabricated".  **MAINTENANCE** tools.go:881-886, 1846-1897; rack/vram.go:13-33.  **TIME** 21 ms.

#### rack_pull (T65) · W
- **AUTHOR** "pull a model into the loopback rack behind confirm (N3)".  **USE** `App.tool('rack_pull', {model:'x', confirm:true})`
  (confirm a JSON true; the string "true" is refused).
- **CARE** The network; needs MANJUEL_RACK_PULL; POST /api/pull, up to 30 minutes holding the global ask lock (every tenant's rack,
  chat, prompt, remember, mesh and team writes wait). "PULLED %q into the loopback rack." [err] "rack_pull needs a model name";
  "refused: rack_pull needs confirm=true — downloads are the operator's hand"; "refused: rack_pull needs MANJUEL_RACK_PULL=1 -- in
  the environment, or in this world's .env"; "pull failed for %q: %s"; "pull refused for %q (status %d): %s".
- **MAINTENANCE** tools.go:887-892, 1899-1936.  **TIME** not measured (RULED: downloads are his).

#### rack_warm (T67) · R
- **AUTHOR** "verify a voice is present and report its footprint (N3)". As it stands it loads nothing.  **USE** `{"voice":"x"}`.
- **CARE** "WARM %q · tier %s · %.2fGB · footprint %.2fGB[ (capabilities silent: …) | (embedding-only: routes refuse it, warmth is
  storage)]". [err] "rack_warm needs a voice"; "refused: voice %q is not on the rack — nothing fabricated".
- **MAINTENANCE** tools.go:893-898, 1938-1968.  **TIME** 31 ms.

#### rack_sync (T66) · R
- **AUTHOR** "re-list the loopback rack with a sync receipt (N3)".  **USE** `{}`.  **CARE** The ladder and "SYNCED %d voices.";
  writes nothing (the engine's rack_sync rewrites rack.md).  **MAINTENANCE** tools.go:899-904, 1970-1981.  **TIME** 25 ms.

#### chat_start (T14) · W
- **AUTHOR** "open a chat session with a receipted id (N1)".  **USE** `{"voice":"llama3.2:latest"}`; actor.
- **CARE** Appends state/chat.jsonl {ts, kind "chat_open", session, actor, voice}; session id c-YYYYMMDD-HHMMSS-<8 hex>. "SESSION
  %s opened on %q — every turn carries a receipt".  **MAINTENANCE** tools.go:908-913; chat/chat.go:74-94.  **TIME** 10 ms.

#### chat_send (T12) · W
- **AUTHOR** "ask in a session; whole witnessed answer or refusal (N1)".  **USE** `{"session":"c-…","question":"…"}`; the glass
  streams through /chat/stream.
- **CARE** The session's shape (not that it was opened); the guard; the route; a streamed answer (600 s, under the ask lock);
  witnessed to the rack ledger; appends {ts, kind "chat_turn", n, session, actor, voice, question, answer, receipt (sha256 of
  session, question, answer, ts), flags}. "n=%d voice %s answered · receipt %s\n<answer>". [err] "chat_send needs a session — open
  one with chat_start"; "refused: session %q breaks the shape law (c-YYYYMMDD-HHMMSS-hex8)"; "chat_send needs a question — no voice
  is asked nothing"; the guard's and the rack's refusals.  **MAINTENANCE** tools.go:914-919; chat.go:128-194.  **TIME** 197 ms.

#### chat_list (T11) · R
- **AUTHOR** "read one session's turns, isolated by session (N1)".  **USE** `{"session":"c-…","last":5}` (last a number).
- **CARE** With no session, as it stands every session's turns. "n=%d %s · %s · receipt %s\n  Q: <200>\n  A: <500>" or "session %q
  holds nothing yet — silence is honest".  **MAINTENANCE** tools.go:920-925.  **TIME** 3 ms.

#### chat_cancel (T10) · R (never held)
- **AUTHOR** "end an in-flight send; no partial answer is kept (N1)".  **USE** `{"session":"c-…"}`.
- **CARE** "session %s cancelled — the stream ends, no partial answer is kept" or "session %s has nothing in flight — nothing
  cancelled, nothing claimed". [err] "chat_cancel needs a session".  **MAINTENANCE** tools.go:926-931.  **TIME** 4 ms.

#### chat_sessions (T13) · R
- **AUTHOR** "list opened chat sessions in first-seen order (N1)".  **USE** `{}`.  **CARE** "SESSIONS — %d opened:" and a line each,
  or "no sessions yet — open one with chat_start".  **MAINTENANCE** tools.go:932-937.  **TIME** 5 ms.

#### prompt_save (T59) · W
- **AUTHOR** "fold a new prompt version; history kept whole (N4)".  **USE** `{"name":"brief","body":"Say {{x}}"}`; name lowercase
  (a-z 0-9 _ -, up to 64); description.
- **CARE** Writes prompts/<name>.md ("---\nname: …\nversion: N\ndescription: …\n---\n<body>"), moves the old latest to
  prompts/<name>.v<k>.md, rewrites prompts/manifest.json {"prompts":{name:{latest, versions}}}. "SAVED %s v%d — history folds whole,
  nothing rewritten". [err] "refused: prompt name %q breaks the name law (lowercase, digits, - _, max 64)"; "refused: prompt body is
  empty — nothing is stored".  **MAINTENANCE** tools.go:942-947; play/play.go:131-159.  **TIME** 21 ms.

#### prompt_get (T56) · R
- **AUTHOR** "read one prompt version with receipt (N4)".  **USE** `{"name":"brief","version":2}` (version a NUMBER; a string
  reads as the latest).  **CARE** "%s v%d · sha256 %s\n<description>\n\n<body>". [err] "no such prompt: %s — try prompt_list"; "no
  such prompt version: %s v%d — try prompt_list".  **MAINTENANCE** tools.go:948-953.  **TIME** 4 ms.

#### prompt_list (T57) · R
- **AUTHOR** "list prompts with latest versions (N4)".  **USE** `{}`.  **CARE** "PROMPTS — %d template(s):" or "no prompts yet —
  save one with prompt_save".  **MAINTENANCE** tools.go:954-959.  **TIME** 4 ms.

#### prompt_run (T58) · W
- **AUTHOR** "render a prompt and measure one answer (N4)".  **USE** `{"name":"brief","vars":"{\"x\":\"hi\"}"}` (vars a JSON
  object INSIDE a string); version; voice.
- **CARE** Fills {{var}} ("refused: missing var: %s — nothing is guessed"); the guard, the route, the ask (600 s), witnessed;
  appends prompts/runs.jsonl {id r-…, ts, kind "prompt_run", prompt, version, voice, override, input, output, receipt, latency_ms,
  eval_count}. "RUN %s · %s v%d · voice %s · %dms ... · receipt %s\n<output>". [err] "prompt vars must be a JSON object: %s".
- **MAINTENANCE** tools.go:960-965; play.go:346-379.  **TIME** 13927 ms (with the model's load).

#### prompt_compare (T54) · W
- **AUTHOR** "run two versions over the same input, diff honestly (N4)".  **USE** `{"name":"brief","vera":1,"verb":2}` (NUMBERS:
  given as strings both read as the latest, which compared v2 with v2 in v0.2.6's measure).  **CARE** Two prompt_runs: "COMPARE %s
  v%d vs v%d: IDENTICAL|DIFFER" with both answers.  **MAINTENANCE** tools.go:966-971.  **TIME** 7588 ms.

#### prompt_eval (T55) · W
- **AUTHOR** "score a prompt over a dataset, exact-match (N4)".  **USE** `{"name":"brief","dataset":"smoke"}` (evals/<dataset>.json,
  [{input:{}, expected}], up to 100 cases). Research has no evals/ folder.
- **CARE** Each case is appended to prompts/runs.jsonl with its score: "EVAL %s v%d over %q: %d/%d pass" and a PASS or FAIL line each.
  [err] "prompt_eval needs a dataset — evals/<name>.json"; "no such dataset %q — try evals/<name>.json"; "dataset %q is empty or
  unparsable — nothing is scored"; "refused: datasets cap at 100 cases".  **MAINTENANCE** tools.go:972-977; play.go:450-497.

#### seat_ask (T77) · W
- **AUTHOR** "@seat single-seat ask; model is a measurement (N4)".  **USE** `{"question":"@cal what holds"}` or
  `{"seat":"cal","question":"..."}`.
- **CARE** Reads agents/<seat>.us (up to 2,000 characters) as context; a measured ask; appended to prompts/runs.jsonl as
  seat_ask. As it stands research has no agents/*.us, so every seat there is refused: "refused: seat %q is not declared — enroll
  first, nothing fabricated". Others: "refused: seat_ask needs @seat addressing (e.g. \"@manjuel what holds\")"; "seat_ask needs a
  question — no seat is asked nothing".  **MAINTENANCE** tools.go:978-983; play.go:384-429.  **TIME** 5 ms (the refusal).

#### town_beat (T92) · W
- **AUTHOR** "run one town scheduling cycle on this ground (N2)".  **USE** `{}`.
- **CARE** Reads <home>/ops/{workorders,properties,inspections}.jsonl (not in research); appends state/town/tasks.jsonl and
  worked.jsonl; every filing REVIEW. "BEAT on %q: issued %d · filed %d · held %d — every filing REVIEW".
- **MAINTENANCE** tools.go:987-992; town/.  **TIME** 9 ms.  **USES** the trade ground; quiet here.

#### town_status (T93) · R
- **AUTHOR** "read the board: tasks, worked set, open orders (N2)".  **USE** `{}`.  **CARE** "TOWN on %q: %d tasks (%d worked) · %d
  open orders" and the REVIEW lines.  **MAINTENANCE** tools.go:993-998, 2287-2319.  **TIME** 4 ms.

#### flow_save (T28) · W
- **AUTHOR** "fold a new flow spec version; history kept whole (N2). A gate's `grants` must name writing tools this door carries;
  a spec carrying `retired` (why, in words) is a flow the door fires no more, every version of it kept".
- **USE** `{"name":"x","spec":"{\"nodes\":[...],\"edges\":[...]}"}` (spec a JSON STRING: {nodes, edges, budget_s?, retired?}).
- **CARE** A node: name, kind (ask | prompt | seat | memory | eval | gate | run | aider | tool), voice, question, prompt, version,
  vars, seat, method, node (an eval's subject), expected, match (equals | contains), title, retries 0-5, grants (gates only),
  loops 0-5, files (aider), tool and args (tool). An edge: {from, to, when always | pass | fail}. Validation (flow/flow.go:249-426):
  exactly one start, no cycles but a bounded eval fail-return, an aider node needs a granting gate, every grant a WRITING tool the
  door carries. Writes flows/<name>.json, the old one moved to flows/<name>.v<k>.json; default budget 600 s. "SAVED flow %s v%d —
  history folds whole, nothing rewritten". [err] "flow_save needs a name and a spec JSON {nodes, edges, budget_s?}"; "flow spec
  must be JSON: %s"; "refused: gate %q grants %q, which is not a tool this door carries"; "refused: gate %q grants %q, which does
  not write -- a grant carries the hand past the holds, and a reader is never held"; the validator's "refused: …".
- **MAINTENANCE** tools.go:1003-1010, 2330-2377; flow/flow.go:249-630.  **TIME** not timed.  **USES** defining a workflow
  (flows/release.json is the release).

#### flow_get (T22) · R
- **AUTHOR** "read one flow spec version (N2)".  **USE** `{"name":"release","version":3}` (a number).  **CARE** The spec,
  indented. [err] "no such flow: %s — try flow_list"; "no such flow version: %s v%d — try flow_list"; "flow %s is corrupt: %s".
- **MAINTENANCE** tools.go:1011-1016.  **TIME** 5 ms.

#### flow_list (T23) · R
- **AUTHOR** "list flows with latest versions, and name any .json under flows/ that cannot be read as one (N2)".  **USE** `{}`.
- **CARE** "FLOWS — %d:\n  - name vN · K nodes · budget Ss[ · retired: …]", then "UNREADABLE — %d (not hidden; fix or remove the
  file):", or "no flows yet — fold one with flow_save".  **MAINTENANCE** tools.go:1017-1022, 2389-2422.  **TIME** 8 ms.

#### flow_run (T26) · W
- **AUTHOR** "fire a flow; gates pause, evals steer, budget binds (N2)".
- **USE** `App.tool('flow_run', {name:'release', inputs:{mark:'v0.2.6'}})`; inputs an object or a JSON string; version; voice;
  voices (seat -> model).
- **CARE** The world's flow lock (one run at a time); validation; retired refused; a run id f-YYYYMMDD-HHMMSS-<8 hex>; nodes in
  order. Gates PAUSE until flow_resume; retries back off 1, 2, 4, 8 s; an eval scores a run node's "--- WHAT THE TOOLS SAID ---"
  block; the budget is a deadline. A `run` node needs an open engine ("no engine is open on this world -- env_open first, then fire
  the flow. A `run` node will not start one behind your back"). A `tool` node calls a door tool as the one who fired it, a writing
  one only under the nearest gate's grant (flow_run, flow_resume and flow_replay are refused inside nodes). As it stands an
  `aider` node always refuses through the door (the door's engine has no Aider: "refused: this flow has no door wired, so an
  `aider` node has no Aider to ask..."). flows/runs.jsonl: start {run, flow, version, ts, kind "start", inputs, budget_s, spec,
  voice?, voices?}; node {run, ts, kind "node", node, nkind, status ok|fail|retry|paused|skipped, pass, latency_ms, output?,
  receipt (sha256 of run, node, output, ts)?, error?, attempt?, title?, grants?}; loop; stopped {verdict, elapsed_ms}. Verdicts
  COMPLETE, PAUSED, FAIL, OUT_OF_TIME, STOPPED. "RUN %s: %s · fired %d · %dms[ — resume with flow_resume continue|stop; nothing
  moves until the hand says so]" and the waterfall. [err] "refused: a run is moving on this world -- fire again once it stops, at a
  gate or at its end; nothing was fired"; "flow inputs must be a JSON object…"; "refused: flow %q is retired -- %s. …".
- **MAINTENANCE** tools.go:1023-1028, 2838-2881; flow/run.go:166-584.  **TIME** 280 ms (smoke COMPLETE).

#### flow_resume (T25) · W
- **AUTHOR** "carry a paused run on with continue|stop (N2)".  **USE** `{"run":"f-…","decision":"continue"}`.
- **CARE** continue writes `resumed` (with the gate's grants) and carries the gate's hand to the next segment; stop writes
  `resumed` and `stopped` STOPPED. "refused: a run is moving on this world, so there is no gate to answer -- ..."; "refused: resume
  decides continue|stop, got %q"; "no such run: %s"; "run %s carries no start — nothing to resume"; "run %s is not paused — only
  paused runs resume"; "refused: %s still has a `run` or `aider` node to fire (%s) and no engine is open on this world (env_open
  first). Nothing was resumed -- …"; [err] "flow_resume needs a run — see flow_runs".
- **MAINTENANCE** tools.go:1029-1034, 2883-2912; run.go:1019-1182.  **TIME** 8.3 s (continue).

#### flow_cancel (T20) · R (never held)
- **AUTHOR** "end a live run; reached nodes stand (N2)".  **USE** `{"run":"f-…"}`.  **CARE** "run %s cancelled — reached nodes
  stand, the rest never fire" or "run %s has nothing live — nothing cancelled, nothing claimed". [err] "flow_cancel needs a run".
  As it stands, being a reader, any allowed key may cancel his run.  **MAINTENANCE** tools.go:1035-1040.  **TIME** 4 ms.

#### flow_status (T29) · R
- **AUTHOR** "waterfall: nodes, elapsed, budget bar, verdict (N2)".  **USE** `{"run":"f-…"}`.  **CARE** "RUN … · flow … · budget Ns",
  a line a node (why, a gate's title and grants, "-> flow_resume run=… decision=continue|stop"), the loops, "elapsed …ms / Ns
  [####----] verdict: …". [err] "no such run: %s".  **MAINTENANCE** tools.go:1041-1046; run.go:1186-1309.  **TIME** 11 ms.

#### flow_compare (T21) · R
- **AUTHOR** "two runs side by side, node by node (N2)".  **USE** `{"runa":"f-…","runb":"f-…"}`.  **CARE** "COMPARE A vs B" and
  "node IDENTICAL|DIFFER|only in A|only in B".  **MAINTENANCE** tools.go:1047-1052; run.go:1320-1370.  **TIME** 33 ms.

#### flow_replay (T24) · W
- **AUTHOR** "re-fire a run's spec and inputs under a fresh id (N2)".  **USE** `{"run":"f-…"}`.  **CARE** Waits for the flow lock;
  the start line carries replay_of; flow_run's answer plus " · replay — same spec, same inputs, fresh id". [err] "flow_replay needs
  a run — see flow_runs"; "run %s carries no start — nothing to replay"; the retired refusal.
- **MAINTENANCE** tools.go:1053-1058; run.go:1436-1493.  **TIME** not run.

#### flow_runs (T27) · R
- **AUTHOR** "list runs for a flow, newest last (N2)".  **USE** `{"flow":"release"}`.  **CARE** "RUNS — %d:\n  <run> · flow <f> ·
  <verdict> · <ts>" or "no runs yet — fire one with flow_run".  **MAINTENANCE** tools.go:1059-1064.  **TIME** 11 ms.

#### team_send (T85) · W (leaves the machine)
- **AUTHOR** "send one guarded message to discord|slack|whatsapp (N5)".  **USE** `{"platform":"slack","channel":"general",
  "content":"…"}`; channel lowercase (a-z 0-9 _ -, up to 64).
- **CARE** The guard; a POST (30 s) to the address in state/chat_secrets.json (https, or loopback); appends state/team.jsonl {ts,
  direction "outbound", platform, channel, agent, content, receipt}. "SENT %s/%s · receipt %s". [err] "refused: unknown platform
  %q — discord|slack|whatsapp only"; "refused: channel %q breaks the channel law"; "team_send needs content — silence is not
  sent"; "refused: %s has no webhook in chat_secrets.json — connect it first, nothing sent"; "refused: whatsapp needs token + phone
  id in chat_secrets.json — nothing is sent unconfigured"; "refused: %s webhook must be https (loopback excepted)"; "%s did not
  answer: %s"; "%s refused the send (door %d) — nothing witnessed".
- **MAINTENANCE** tools.go:1069-1074; team/team.go:173-222.  **TIME** not run (RULED: it leaves the machine).

#### team_status (T86) · R
- **AUTHOR** "platform presence + last sends, never secrets (N5)".  **USE** `{}`.  **CARE** "TEAM BRIDGE on %q:\n  - platform:
  connected|disconnected · last send <ts|never>".  **MAINTENANCE** tools.go:1075-1080.  **TIME** 3 ms.

#### team_history (T83) · R
- **AUTHOR** "read the bridge record, filtered, newest last (N5)".  **USE** `{"channel":"general","last":20}`.  **CARE** A line a
  message with its receipt, or "the bridge holds nothing yet — silence is honest".  **MAINTENANCE** tools.go:1081-1086.  **TIME** 5 ms.

#### team_ingest (T84) · W
- **AUTHOR** "verify + store one inbound platform envelope (N5)".  **USE** `{"platform":"slack","body":"<raw json>","signature":
  "sha256=<hex>"}`.  **CARE** HMAC-SHA256 with the hook secret, constant time; dedupes on the platform's id; appends an inbound
  line. "CHALLENGE %s" / "duplicate delivery — already stored, never twice" / "INGESTED %s/%s · receipt %s". [err] "refused: bad
  webhook signature — nothing stored, nothing claimed".  **MAINTENANCE** tools.go:1087-1092; team.go:259-338.  **TIME** not run.

#### auth_key_create (T5) · W
- **AUTHOR** "mint a scoped API key; plaintext returns once (N6)".  **USE** `App.tool('auth_key_create', {name:'council',
  tenants:'research,atlas', key:'<a live key>'})`; key re-proves possession once any key exists.
- **CARE** Writes <home>/state/auth.json {keys:[{id, name, hash, salt, tenants, created, revoked?}]} (0600) and audits
  state/auth_audit.jsonl. "MINTED %s for %q on %q — copy it now, it never shows again\n<the key>" (if parked, the key goes to
  whoever approves). [err] "refused: key management names a live key — possession re-proved, like sudo"; "auth needs a name for the
  key — unnamed keys are not minted".  **MAINTENANCE** tools.go:1098-1103, 3065-3082; auth/auth.go:141-176.  **TIME** RULED.

#### auth_key_list (T6) · R
- **AUTHOR** "list live keys with hashes withheld (N6)".  **USE** `{}`.  **CARE** "KEYS on %q — %d live:" and a line a key, or "no
  live keys — the gate stands open (bootstrap)".  **MAINTENANCE** tools.go:1104-1109.  **TIME** 5 ms.

#### auth_key_revoke (T7) · W
- **AUTHOR** "fold a key: flagged, kept for audit (N6)".  **USE** `{"id":"k-…","key":"<a live key>"}`.  **CARE** Sets revoked and
  audits: "REVOKED %s on %q — folded, kept for audit". [err] "auth_key_revoke needs an id — see auth_key_list"; the re-proof
  refusal; "refused: no live key %q".  **MAINTENANCE** tools.go:1110-1115.  **TIME** RULED.

#### auth_key_scope (T8) · W
- **AUTHOR** "set which carried tenants a live key carries, the list replaced whole; possession re-proved like create and revoke,
  and the move audited (N6)".  **USE** `{"id":"k-…","tenants":"research,atlas","key":"<a live key>"}`.
- **CARE** "SCOPED %s %q on %q — it carries [%s] now; the move is in the audit line". [err] "auth_key_scope needs an id — see
  auth_key_list"; "auth_key_scope needs the tenants the key is to carry, e.g. research,atlas"; "refused: %q is not a carried tenant
  -- a key carries only grounds this door carries"; the re-proof refusal; "refused: no live key %q".
- **MAINTENANCE** tools.go:1116-1123.  **TIME** RULED.

#### auth_verify (T9) · R (open without a bearer)
- **AUTHOR** "check a key against a tenant store; the login door (N6)".  **USE** `{"key":"<a key>"}`.  **CARE** "VERIFIED %s on %q ·
  tenants [..]". [err] "refused: not a key"; "refused: unknown or revoked key".  **MAINTENANCE** tools.go:1124-1129.  **TIME** 3 ms.

#### tenant_trust_list (T91) · R
- **AUTHOR** "read recorded cross-tenant delegations (N6)".  **USE** `{}`.  **CARE** Reads state/trust.json: "TRUST — %d
  delegation(s):" or "TRUST — no delegations recorded (empty is honest, never fabricated)."  **MAINTENANCE** tools.go:1130-1135;
  trust/trust.go:93-104.  **TIME** 4 ms.

#### us_to_vc (T94) · R
- **AUTHOR** "convert a .us declaration to a W3C Verifiable Credential".  **USE** `App.tool('us_to_vc', {path:'agents/operator.us',
  project:'atlas'}, true)` (the glass's footer).
- **CARE** As it stands the path is not jailed. The credential JSON: did:atlas:<covenant>:<id>, issuer did:atlas:<covenant>:operator,
  the file's prose as credentialSubject.description. [err] "us_to_vc needs a path to a .us file"; "us_to_vc: no JSON block found in
  .us document"; "... invalid JSON in .us block: …"; "... can_approve must be explicitly stated as false"; "... can_approve must be
  false; true is refused"; "... invalid id format: %q"; "... the record declares no covenant, so no issuer can be minted in its
  namespace".  **MAINTENANCE** tools.go:1138-1149, 3763-3781; vc/vc.go.  **TIME** 4 ms.

#### tenant_list (T87) · R
- **AUTHOR** "list all registered tenants and their roles" (as it stands it prints counts, not roles).  **USE** `{}`.
- **CARE** "TENANTS — %d carried project(s):\n  - name · open mode|N assigned · K trust grant(s)[ (you are here)]".
- **MAINTENANCE** tools.go:1153-1160, 3786-3807.  **TIME** 4 ms.

#### tenant_rbac_assign (T88) · W
- **AUTHOR** "assign a role to an agent in a tenant's RBAC policy".  **USE** `{"actor":"k-ae2e9481","role":"steward"}`; role
  operator | steward | agent | guest, or a custom one.
- **CARE** Rewrites <home>/rbac.json whole. The FIRST assignment turns that tenant from open mode to enforced for every caller
  but the glass. "ASSIGNED role %q to agent %q in tenant %q". [err] "tenant_rbac_assign needs an actor"; "... needs a role"; "role %q
  does not exist"; "rbac assigned but failed to persist: %w".  **MAINTENANCE** tools.go:1162-1167; rbac.go:265-281.  **TIME** RULED.

#### tenant_rbac_check (T89) · R
- **AUTHOR** "check if an agent has permission for a tool under a tenant's RBAC policy".  **USE** `{"actor":"k-…","tool":"git_commit"}`.
- **CARE** Judges the tool's whole Writes flag: "ALLOWED — %s on %s (open mode)" / "ALLOWED — %s (role %q) on %s" / "DENIED — %s
  (role %q) on %s: %s". [err] "tenant_rbac_check needs an actor"; "... needs a tool"; "unknown tool: %q -- ...".
- **MAINTENANCE** tools.go:1169-1174.  **TIME** 6 ms.

#### tenant_trust (T90) · W
- **AUTHOR** "grant or revoke cross-tenant trust (delegation of specific tools)".  **USE** `{"from_project":"atlas","to_project":
  "research","tool":"records","action":"allow"}`.
- **CARE** Upserts <home>/state/trust.json; as it stands nothing enforces a grant, and its forbidden-verb check compares the whole
  tool name to bare verbs (so git_commit passes). "TRUST %s %s: %s → %s (witnessed state/trust.json · sha256 %s)". [err] "tenant_trust
  needs from_project"; "... to_project"; "... a tool"; "tenant_trust action must be 'allow' or 'deny', got %q"; "refused: %q is a
  forbidden verb — absent by construction, never delegable"; "unknown project %q: not a carried tenant (from_project|to_project)".
- **MAINTENANCE** tools.go:1176-1185, 3873-3909.  **TIME** RULED.

#### env_open (T18) · W
- **AUTHOR** "open the Manjuel engine inside a world; refuses a world already being sat in".  **USE** `App.tool('env_open', {})`
  (Boot does it).
- **CARE** Starts `<python> manjuel.py --headless --ground <home>` speaking JSON lines, and waits up to 120 s for `opened`; an
  engine already open is returned; a sitting left by a dead process is reaped. "OPENED %s · sitting %s · session %s\n  <git>\n
  rack reachable|UNREACHABLE · pipeline %s\n  seats: …". [err] "no engine wired: atlas-mcp was started without --manjuel …";
  "refused: %q is not a directory; a world is never created here"; "refused: %s -- %s. THE LINE will not open a second engine on a
  world whose record it cannot read"; "refused: %s has an open sitting (%d, opened %s). One engine per world -- a second would fork
  the ledger. …"; "the engine did not start: …"; "the engine did not open: …"; "the engine did not open inside 120s; it was closed
  cleanly so its world stays openable…".
- **MAINTENANCE** tools.go:1191-1207; engine/engine.go:306-428.  **TIME** about 31 s to `opened`.  **USES** Boot.

#### env_close (T16) · W
- **AUTHOR** "close the world's sitting properly and reap its engine".  **USE** `App.tool('env_close', {})` (/close does it).
- **CARE** A cancel if busy, then {"cmd":"close"}; 60 s, then a kill. "CLOSED %s -- the sitting is tolled and the engine reaped",
  or "… BUT THE ENGINE HAD TO BE KILLED after 60s. …". [err] "no engine is open on that world".
- **MAINTENANCE** tools.go:1209-1226; engine.go:758-801.  **TIME** not timed.

#### env_list (T17) · R
- **AUTHOR** "which worlds have an engine open, and which are being sat in elsewhere".  **USE** `{}`.  **CARE** "%d engine(s)
  open:\n  name · sitting N[ · WAITING ON AN ANSWER: …]\n\ncarried worlds:\n  name closed|engine open here|sat in elsewhere (sitting
  N, ts)".  **MAINTENANCE** tools.go:1228-1258.  **TIME** 6 ms.

#### run_start (T76) · W
- **AUTHOR** "run one objective through the council; the delivery with what actually ran. `voice` runs every seat on one model
  for this turn and `voices` names a model per seat over it (flow_run's two words); the declared targets are put back when the
  turn ends".  **USE** `{"objective":"…"}` (HELD from the Agent tab; the glass itself streams through /run/stream); feed; method;
  voice; voices.
- **CARE** Writes {"cmd":"objective","text",...} to the engine; one run a world. "WAITING on %q\n\n  <prompt>\n\nAnswer with
  run_answer. Nothing is assumed on your behalf (RULE 6)." or "<world> · <pipeline> · <s>s\n\n<text>\n\n--- what actually ran
  ---\n  tool … ok|FAILED\n  seat … …s …\n  transcript: …". [err] "run_start needs an objective"; "no engine is open on %q --
  env_open first"; "refused: the engine is waiting on an answer (%q). Answer it with run_answer before starting another turn -- the
  gate is yours, not the door's"; "this engine is closed".  **MAINTENANCE** tools.go:1260-1287; engine.go:580-649.  **TIME** 234 s.

#### run_answer (T74) · W
- **AUTHOR** "answer what the run asked; the gate crossing the wire, never a default".  **USE** `{"text":"skip"}`.
- **CARE** {"cmd":"answer","text"}. [err] "no engine is open on %q"; "refused: nothing is being asked, so there is nothing to answer".
  As it stands /run/stream?answer= does the same with no hold.  **MAINTENANCE** tools.go:1289-1304; engine.go:653-669.  **TIME** about 1 s.

#### standup_run (T80) · W
- **AUTHOR** "run the estate's live standup in this world -- the morning set (default), the court, or all -- and hand back its
  tally and report; it opens and tolls a sitting of its own, so it refuses while one is open here".
- **USE** `mcp_call atlas standup_run {"set":"morning"}` (held for his card); set morning | court | all.
- **CARE** Runs tests/standup.py [--court|--all] (30 minutes): "STANDUP %s on %q · <exit> · <tally>[ · report …]" and everything it
  printed. [err] "refused: the standup's sets are morning, court and all; %q is none of them"; "refused: the door was started
  without --manjuel, so it has no python to run the standup with"; "refused: %q carries no tests/standup.py -- …"; "refused: an
  engine is open on %q (sitting %s), and the standup opens a sitting of its own -- close it first (env_close)"; "refused: %q has
  an open sitting (%d, opened %s), and the standup opens one of its own".
- **MAINTENANCE** tools.go:1310-1317, 1434-1516.  **TIME** 1157 s (the live check with the court).  **USES** the live proof.

#### suite_run (T82) · R by declaration (it writes the suites' stamps, by design)
- **AUTHOR** "run the estate's own suites in this world -- the strokes, the smoke, or both (default) -- one after the other ...;
  the suites stamp their own proof (tests/last_run.json, run_history) and the head reads that stamp back, failures first".
- **USE** `mcp_call atlas suite_run {"set":"strokes"}` (runs at once); set strokes | smoke | both.
- **CARE** One suite run on the machine at a time; 30 minutes shared. "SUITES %s on %q · strokes: P/T green|RED · exit … · smoke:
  …", then each suite's failures (up to 60) and its last six lines. [err] "refused: the suites are strokes, smoke and both; %q is
  none of them"; "refused: the door was started without --manjuel, …"; "refused: %q carries no tests/%s -- …"; "refused: a suite is
  already running on this computer; one at a time, or the browser-count stroke reds for both". The engine waits 295 s for it; a
  longer run is read back through `proved` (C71).
- **MAINTENANCE** tools.go:1327-1334, 1518-1654.  **TIME** 237 s (both, 2026-10-12).  **USES** proving from the Agent tab.

#### release_step (T72) · W
- **AUTHOR** "one of the release's own steps, run by the core's tests/cut.py in this world: bump ...; rebuild the toll index;
  check the release gate; wait for GitHub's runs and check again; or record where a cut's marks sit".
- **USE** `{"step":"check","mark":"v0.2.6"}`; step bump | index | check | ci | record; mark vX.Y.Z (all but index).
- **CARE** `python tests/cut.py <step> [mark]` (45 minutes). [err] "refused: the release's steps are bump, index, check, ci and
  record; %q is none of them"; "refused: %s names its mark as vX.Y.Z, and %q is not one"; "refused: the door was started without
  --manjuel, …"; "refused: %q carries no tests/cut.py -- …"; "release step %s refused (%v):\n<out>".
- **MAINTENANCE** tools.go:1344-1351, 1372-1432.  **TIME** measured at a cut.  **USES** the release flow's tool nodes.

#### run_cancel (T75) · R (never held)
- **AUTHOR** "interrupt the turn in flight; the sitting stays open".  **USE** `App.tool('run_cancel', {})` (a turn's cancel).
- **CARE** {"cmd":"cancel"}: "CANCELLED -- the turn was interrupted; the sitting stands". [err] "no engine is open on %q"; "this
  engine is closed". As it stands any allowed key may cancel his turn.  **MAINTENANCE** tools.go:1353-1367; engine.go:731-748.
- **TIME** 3 ms.

**Door tools that do an engine skill's job:** git_commit, git_push, git_pull and the git_commit, git_push, git_pull skills;
git and git_status; remember and remember (two different stores); rack_list, rack_sync, rack_pull and their skills (the door's
rack_sync writes nothing); proofs and `proved`; file_edit and ground_edit / edit_file; shell_run's Python and run_python;
records / read_doctrine and ground_read / read_file.

### 5.5 The glass (atlas-webapp, on 127.0.0.1:8091)

**The server** (atlas/webapp; Go, the page embedded with go:embed). It reads ATLAS_WEB_PORT and ATLAS_SERVICE only; it listens
on 127.0.0.1 only; it talks to the door at the stored setting mcp_url (default http://127.0.0.1:8090); it waits 15 s on
/run/state and /tools and 30 minutes on a tool call or a stream. Every file it serves carries an ETag (sha256, 16 hex) and
`no-cache`; any other path gets index.html; an unknown /api path 404. Errors are {"error":"words"}. Sign-in is always on: open
without a session are /api/login, /api/health, /api/lock, /api/setup, /api/unlock, /hooks/* and every page path; everything else
needs the atlas_session cookie (HttpOnly, SameSite=Strict, twelve hours, kept in data/sessions.json across a restart), else /api
answers 401 {"error":"login required"} and a page 302s to /login.

**Its endpoints** (atlas/webapp/server/server.go:48-108):

    GET  /api/health                       {status, version, time, auth}
    GET  /api/agents, /api/agents/{id}; POST /api/agents        the stored agents (no page calls these)
    GET  /api/traces?agent=, /api/traces/{id}; POST /api/traces  the trace ledger (newest 100)
    GET  /api/evals?trace=; POST /api/evals {trace_id, name, score, passed, detail}   evals scored by hand
    POST /api/tools/call {tool, args, agent_id?, background?}   -> {output (the door's raw JSON-RPC answer), hash,
         duration_ms, trace_id?}: sent to <mcp_url>/rpc as tools/call with "Authorization: Bearer $ATLAS_SERVICE"; a trace is kept
         unless background AND the tool is muster, rack_list, proofs, projects, hold_list or aider_status
    GET  /api/tools                        the door's /tools
    GET  /api/search?q=                    (no page calls it)
    GET  /api/messages?channel=; POST /api/messages/send        the local message store
    GET  /api/settings/{key}; POST /api/settings/{key} {value}  the settings store (no checks on the server)
    GET  /api/events                       server-sent events, `data: {"type":T,"data":D}`; a heartbeat every 30 s
    /api/chat/sessions|session|start|send|stream                 the door's chat tools and /chat/stream
    GET  /api/council/stream?objective=...[&feed&method&project] or ?answer=...   the door's /run/stream; every line also on
         /api/events as type "council"
    GET  /api/council/state                the door's /run/state: {open, world, sitting, session, pending, started, stale,
         stale_file, code_changed, runs, last_run}
    GET  /api/council/listen?seconds=      the door's /run/listen (the mic)
    GET  /ws                               a WebSocket: in ping, chat.send; out pong, chat.token, chat.done, chat.error and
         every bus event (no page uses it)
    /api/prompts, /api/prompts/get|save|run|compare|eval, POST /api/seat/ask    the Playground's
    POST /api/town/beat, GET /api/town/status
    /api/flows, /api/flows/get|save|run|resume|status|compare|replay|runs       the Workflows tab's
    POST /api/team/send, GET /api/team/history|status, POST /hooks/{platform}    the team bridge
    POST /api/login {tenant, key}, POST /api/logout, GET /api/me, GET /api/lock, POST /api/setup, POST /api/unlock,
         POST /api/workspace/switch {tenant}
    GET  /api/projects/{name}/page[?v=N]   the maker's page, served under "sandbox allow-scripts allow-modals; default-src
         'none'; ... connect-src 'none'; frame-ancestors 'self'"
    GET  /metrics                          Prometheus text

**How the page talks.** Every call goes through API.get and API.post (static/js/api.js), each kept in API.calls (the newest 300)
and shown in the Run tab's Door calls. `App.tool(name, args, background)` unwraps the JSON-RPC answer, throws on an error or
isError, and returns its text. A turn is one EventSource on /api/council/stream (council.js), every engine event arriving as
`event: engine` (RUNBOOK, "The wire"). /api/events (one per tab) carries toasts and turns another window started; it reconnects
after 3 s. The page polls hold_list every 3 s while visible, and /api/council/state (and aider_status when the Aider tab is open)
every 30 s while no turn runs, and both again when the page becomes visible.

**What the page keeps.** localStorage "atlas.agent.hist": the lines typed, newest first, up to 100. sessionStorage
"atlas.run.last": the last turn. The server's settings: mcp_url, eval_threshold, boot.<world> {session, text} (the boot
report), thread.<world> {session, said (the last 6)}, maker.<world> {session, project}. In memory: Agent (mode, entries, holds,
holdState, aiderFiles, aiderRead, aiderLast, play, open, tab), Run (engineOpen, world, sitting, session, pending, started, runs,
lastRun, stale, turn), Chat, API.calls, Projects, Workflows, Flows.

**The front page.** One terminal and an Inspector (his word of 2026-10-02, against "some uber-complicated dashboard"); every
other address opens it with an Inspector tab open. The bar: the dot, ATLAS and the version; seven doors (Aider Pair, GitHub
with a count of unsaved or unsent work across the worlds, Audit Ledger, Workflows, Registry & Docs, Laws, Settings); the status
("door silent", "no engine" or "engine open", "rack N voices"); Pages; Inspector; his name and Lock (Lock posts /api/logout).

**The terminal.** Its title: the mode, `project:<world>`, and for the Agent tab "sitting N · age", an idle warning after 5
minutes ("closes itself at 30m idle"), "old code" when the engine's code changed since it opened, and Close; or "no engine" and
Boot. Mode buttons; the trash (or Ctrl+L) clears the screen only. The input: prompts `agent[world]>`, `bash[world]$`,
`py[world]>>>`, `ps[world]>`, `aider[world]>`; Up and Down walk the history; the mic; "?" shows the Try: hints (a hint RUNS at
once); Run. Prefixes work from any tab: "$ " or "! " is Bash, ">>> " is Python, "aider " is Aider. Each entry has a copy button.

- **Agent tab** -- a line is one engine turn (README, "How a typed line travels"). Refused on the page, nothing sent: a turn
  already running ("A turn is already running"); the council waiting on a question ("...Answer it first. Nothing was sent.");
  no engine ("No engine is open on <world>... Press Boot (or type /boot) first..."); the door silent. A live entry shows the seat
  or tool at work and a cancel (run_cancel); a seat's thought folds to "<seat> thought N s"; a failed tool or delivery shows "NOT
  EVERYTHING RAN" or "OUT OF TIME".
- **Bash tab** -- shell_run {shell:'bash', command, timeout:300}: a read runs at once ("read", "exit 0"); a write shows "This asks
  first" and a red card; a refusal is named. **Python tab** -- one session per world that keeps its names; `/reset` ends it.
  **PowerShell tab** -- every line waits on a card; it needs pwsh on the door's PATH. **Aider tab** -- the page answers /add path,
  /read path, /drop path|all, /files, /status, /undo [run], /help; any other line is an instruction to aider_run with the files in
  the chat; a run that wrote shows its diff and "Undo this run" (aider_undo, at once). Nothing commits.
- **/boot** (the page's own): env_close if one is open, env_open, `/warm` and `/status` through the council stream; the report
  kept in boot.<world>; a failed step prints "REFUSED: ...". **/close**: env_close (writes `ended`, pays the toll if a turn
  ran). **/clear**: the screen only.

**The dock** -- every card, pinned at the foot of the terminal in every tab: (1) the council's question: Approve and Deny for a
"[y/n]" question (answering "y" or "n"), otherwise a field and Answer, its
colour the question's; (2) a shell line that asks first: the line, why, Approve or Deny (hold_answer, its result landing in that
entry); (3) any call the door parked: "<tool> asks first", who asked, the world, when, the call (a file_edit shows its change),
Approve or Deny; (4) a note when the queue cannot be read or the door is unarmed ("NOTHING IS HELD, AND NOTHING CAN BE").
Nothing is answered but by his click or his words. A shell card whose hold left the queue turns "answered elsewhere".

**The Inspector's tabs:**

    Run              the last turn: Asked, Law gate, Seats, Tools, Needs you, Delivered; the seats with model, time and
                     ran/skipped/error; the floor (each seat's words); the tool calls; the wire (every event, raw if asked);
                     Door calls (every call this page made); Projects ("Work on this", "Put it down" type a sentence into the
                     Agent tab) and the play frame (the maker's page beside the terminal, scaled to 1000x720, sandboxed)
    What's left      WHATS_LEFT.md counted and listed, tiles per lettered section, a find box, "Read it again"
    Aider Pair       aider_status, the files in the chat (each with drop), the recent runs with Undo
    GitHub           per world: You are on, Sends to, Last save, Unsaved work, GitHub, Sending; a message box; Save the work
                     (git_commit), Send to GitHub (git_push), Take from GitHub (git_pull), Lines of work (git_branch), Version
                     marks (git_tag; send and remove need two presses), Pull requests (git_pr; Merge on GitHub needs two presses
                     and is live only when the checks passed); a changed file opens its git_diff. These run on his press, so
                     they are not held; a greyed button carries the door's reason
    Audit Ledger     what the build has proved (proofs), "Run the live check" (standup_run morning; not while an engine is
                     open; it opens a sitting of its own, 2 to 9 minutes), the engine's kept /status and "Read /status now",
                     the estate, the evals scored by hand, "List the newest" transcripts
    Workflows        the flows (Open, "Start one"), a flow's steps (+ ask, run, seat, prompt, memory, eval, gate) and edges
                     (always, pass, fail), its budget, Save (flow_save), "Fire it" (flow_run), "Carry it on" / "Stop it here"
                     (flow_resume), the runs waiting on him
    Laws             law_status's verdict; the drafts below the seal with "Seal the ledger..." then "Seal it" / "Not now"
                     (law_seal); "Set a law" (name, words, where it came from; law_add); CLAUDE.md's standing rules; the ledger;
                     each law file
    Settings         the door's address (http or https only; a wrong one cuts every call off) and the evals pass mark (0 to 1);
                     the messaging bridge
    Registry & Docs  the door's tools with Call (a JSON form; a writing tool called here runs as him, unheld); the seats with
                     their prompts and files; the documents by kind, each whole with its sha256
    Rack             rack_list: the voices by tier

Pages off the menu that still draw: /traces (the newest 100 traces; "+ Add Eval" with a 0-1 score, passed at or above the pass
mark), /messages (the bridge; a send goes out on one click, no card), /playground (the prompt registry). Addresses: /workflows,
/laws, /flows (the GitHub tab), /settings, /chat (the Run tab), /agents, /tools and /records (Registry & Docs), /evals (Audit
Ledger), /left (What's left), /dashboard (the front page). Ctrl+K opens the palette: every page, and Boot, Close, Reboot.

**The page's own helpers** (top-level in its script, reachable from the page's console):

    Agent.go(line)                    the one way a typed line goes in; the same gates as typing
    Agent.drive(tab, line, waitMs)    a line "as if typed" in that tab; waits (polling every 300 ms) until its entry stops
                                      running and returns {id, kind, state, exit, hold, class, why, truncated, out}; a line
                                      that parks returns state "held"; answers no card
    Agent.answer(text)                answers the council's question (Run.start({answer})); does nothing while a turn runs
    Agent.boot(), Agent.closeSitting(), Agent.council(words), Agent.door(tab)
    App.tool(name, args, background)  any door tool, as him (a writing one unheld); throws on a refusal
    Run.check(), Run.start({objective}|{answer}), Run.cancel() (run_cancel), Run.finish, Run.keep, Run.restore, Run.mirror,
    Run.hear / Run.stopHearing (the mic), and readers of the turn: absorb, seatOf, thoughtOf, failures, outOfTime, steps,
    nowLine, elapsed; Run.running, Run.pending (the card's question), Run.turn.events

**The PIN lock** (handlers/lock.go, session.go, static/js/lock.js). One user: a name of up to 40 characters and a PIN of 4 to 8
digits, kept as data/user.json {name, salt (16 bytes, hex), hash (PBKDF2-SHA256, 600,000 rounds, 32 bytes), rounds, created},
mode 0600, written to a temporary file and renamed. On load the page asks /api/me; on 401 it draws the lock and asks /api/lock:
"Welcome" (name, PIN, PIN again -> Start; taken only from this machine and only while no one is set up, else 409 "someone is
already set up here -- sign in instead"), "Hi, <name>" (PIN -> Unlock), or "The sign-in file needs a reset". A wrong PIN: 401
"that PIN is not it -- N tries left"; the fifth in a row: 429 for 60 s ("Too many tries. Try again in N seconds."; the count is in
memory, so a restart forgets it). Forgotten: delete data/user.json and reload.

**As it stands** (the glass's own words against its code, 2026-10-16, re-checked 2026-10-19): the running binary (built 12:16
that day, from a working tree that already had the Approve and Deny buttons, committed later as atlas c65cfdd) serves them;
nothing ever trims data/webapp.db/traces.jsonl (455 MB on the day), and every trace's status is written "ok" (WHAT'S LEFT
C116); fourteen old binaries sit beside the current one; the GitHub tab's own banner says "NOTHING HERE ACTS" above buttons that save, send and
take; the banner and two comments count four or "five" tabs and doors where there are five and seven; a "New trace recorded"
toast follows every non-background tool call; the Trace Log, Messages and Playground are linked from nothing on the front page.

### 5.6 The shell gate's rules (the door's shellgate.go, shell.go, shellpy.go; the Bash, Python and PowerShell tabs)

Checked in this order, on the whole line and again on every unquoted word:

**Refused by name** (no click lifts it): a NUL byte ("a NUL byte in the entry"); a key's shape -- atl_ and 32 hex, sk-..., Bearer
..., xox[bap]-, ghp_, AKIA... ("RULE 7: a key typed into a command; keys are silent and never ride a command line"); a secret
file's name -- .env*, id_rsa, id_ed25519, .netrc, .npmrc, .pypirc, or secret(s), credential(s), creds, token(s), keyfile,
apikey, api_key, *_secrets, *_key with a data extension ("LAW 9 / RULE 7: names a secret file (<name>); keys are silent"); vault/
or .client. ("SITTING LAW 2: names client material by tag; it is opened only when the operator points at it, by hand"); $HOME,
$USERPROFILE, $APPDATA, %USERPROFILE% and their like ("RULE 1: names a home directory; every read and write stays inside the
ground"); "..", a drive letter, ~/, a UNC path, or /home /users /etc /tmp /var /windows /usr /bin outside the ground ("RULE 1 / LAW
8: names a path outside the ground (<hit>...); every read and write stays inside Research"; a rooted word, "/sla" or "\r"
included, is refused the same way); a word beginning with ~; a pattern reaching hidden files ("LAW 9 / RULE 7: a pattern that can
reach hidden files, where the secrets live"). The ground's own path, in either spelling, and /dev/null are allowed.

**Runs at once (Bash only)**, when every command in the line, joined by ; && || |, is one of: ls dir pwd wc nl stat du df
basename dirname realpath readlink which type whoami uname echo printf true false : cut tr cat diff cmp grep egrep fgrep
sha256sum sha1sum md5sum test; file (not -C); head and tail (not -f or -F); sort (not -o or --compress-program); uniq (one
operand); date (only +format); hostname (no operands); find (not -delete, -exec, -execdir, -ok, -okdir, -fprint*, -fls); rg (not
--pre, --pre-glob, --hostname-bin, -z); and git's reads with no --output, --ext-diff or -O: status log diff show ls-files ls-tree
rev-parse rev-list describe blame shortlog grep cat-file show-ref for-each-ref name-rev merge-base check-ignore check-attr
diff-tree diff-index diff-files count-objects whatchanged version var verify-commit verify-tag annotate, branch and tag listing
only, remote [-v], stash list|show, worktree list, reflog [show], config --get|--list; git's global options --no-pager,
--no-optional-locks, --no-replace-objects only. A redirect only to /dev/null, from a file with <, or a 2>&1 duplication.

**Parks a card** (the card's why says which): deletes (rm rmdir del erase rd unlink shred); installs (pip pip3 pipx npm npx pnpm
yarn bun choco winget scoop apt apt-get brew gem conda uv); reaches the network (curl wget ssh scp sftp ftp nc ncat netcat telnet
ping nslookup dig tracert traceroute rsync); writes files (touch mkdir cp mv ln tee sed awk chmod chown truncate dd install tar zip
unzip 7z patch xargs); runs a program the gate cannot read (python python3 py node deno bash sh zsh pwsh powershell cmd make go
cargo dotnet java ruby perl php mvn gradle eval exec source . env command sudo nohup time nice start); any other command ("runs
X, which the gate cannot read as a plain look"); git's writes ("git push sends saved work to the remote", "git pull reaches the
network", "git commit changes the repository", ...); syntax it does not read -- $(...), backticks, ( ) subshells, &, here-docs,
process substitution, an unterminated quote, $'..', ;; ("uses shell syntax the gate does not read: ..."); a $VARIABLE; braces;
a redirect into a file; a shell keyword (if, for, ...); a program by path; a variable set before a command; a command word the
shell builds. Every PowerShell line parks.

**Python** is judged by its syntax tree, never run to judge it (20 s): constants, plain-data names, arithmetic, comprehensions,
lambdas, if/for/while/assert/pass, assignment to names or to subscripts of plain names, and calls to abs all any ascii bin bool
bytes chr complex dict divmod enumerate filter float frozenset hex int isinstance len list map max min oct ord pow print range repr
reversed round set slice sorted str sum tuple zip and the plain str/list/dict/set/int methods run at once; an import, def, class,
return/with/try/global/nonlocal, raise, any other call or method, an attribute, or a name that is not plain data parks a card. A
syntax error counts as a read (nothing would run). A run past its limit ends the session: "ran past N s: the session was ended,
and its names are gone".

### 5.7 The engine (manjuel): its modules, its routing, its commands, its seats

**The modules** (each file's own opening words): serve.py the headless door the glass runs, and the driver (/drive) and
door_call; cli.py the REPL and every slash command; pipeline.py the run itself -- routing, seats, gates; intent.py deterministic
routing by arithmetic on his words, before any model; seating.py racked seats and where they slot in; registry.py parses agents/
and pipelines.md; seatlog.py sittings, the toll, the standing and the story; transcript.py logs/ transcripts and their prompts;
context.py the state of one run; skills.py every skill, the path jails, the tree doors; runtime.py the Ollama transport;
routes.py the hosted route; lawgate.py the law gate every pipeline run passes first; maker.py "make me a game" projects;
memory.py memory.md and its hash chain; gitstate.py the core's own git; boot.py the boot report; doctrine.py whether the docs
still match the code; drift.py cosine drift between a stage's output and its source; vectors.py the semantic index; watch.py
reload and reindex when files change; parity.py the chain measured against a bare call; rack.py writes rack.md; vram.py the VRAM
plan; voice.py speech in and out; spelling.py deterministic spelling fixes; ink.py colour and spinner; dotenv.py reads .env
without printing it; mathkit.py numeric helpers; us.py the capability manifest's checker; __init__.py the version and the dials
read again after .env. Every function, by file and line: BUILDMAP.md.

**Door.turn's routing order** (serve.py:1951-2145), for every line the glass sends: an empty line does nothing; exit, quit or a
casual goodbye closes the sitting; the file changes the watcher saw are applied and skill calls are watched (the `tool` and
`tool_result` events); `/drive` -> the driver; a line leading with `mcp_call` -> door_call; a topic or session cue; "pay the toll"
or "the toll"; "remember that"; `@<seat>`; a `/command` (`/exit` closes); the rack unreachable -> `unreachable`; otherwise the
PIPELINE: the gibberish gate, the deadline, the LAW GATE, the maker, the tool-name readers, the ambiguity card (amber), the
unknown-skill gate, the routing branches, the level, the pasted-feed gate, the wake card (green), the summons, then the seats in
order (pipeline.py:2380-4016); after it the thread, the transcript, the ledger row, the spelling check and `delivery`.

**The sitting** (seatlog.py). Opening: the number is the highest n plus 1; a row {n, id, started, ground, git_start, runs,
ended, git_end, toll_paid, pid, closed_by} is appended; sittings left open by a dead process are closed and tolled first. Each run
is held in memory {objective, pipeline, stages, failed, elapsed, transcript, tools, guards, seats_failed, out_of_time, delivery}
and written only with the closing row. Closing: exit, a hang-up, 30 idle minutes, or /close from the glass; an unattended toll
when something ran and none was paid; then the door's `closed` event {why, sitting, runs, toll_paid}. As it stands a /drive SHIP
run is counted failed (only passed, tidy and clean count as not failed).

**The running orders** (pipelines.md; registry.py:315-396), with their measured times (the ledger):

    default   Steward -> Router (when needs_tool) -> Steward (when worked); other seats join on their flags     median 11.1 s
    brief     Security Guardian -> Morning Reviewer -> Delivery Agent; for a pasted feed; no tools               54.8 s
    estate    Security Guardian -> Steward -> Neiro -> Jesster -> Judge; read-only; no Router                    290 to 591 s
    court     Security Guardian -> Router (when needs_tool) -> Neiro -> Jesster -> Judge; read-only; 900 s       median 240 s
    quick     Security Guardian -> Steward                                                                       3.9 to 16.1 s

**How a seat comes to sit** (seating.py:182-232, pipeline.py): the running order is the spine; a seat with `Wakes On` rests on the
rack and joins when one of its flags rises (`first` to the next slot, `last` at the end, `after X` after X); a step's `when:` must be
among the raised flags or the seat rests; ONLY the Router (or a seat with stage `route`) is handed tools and may call them -- up
to five hops, a repeated call refused. The seats (agents/, their measured median times on this machine):

    Steward (llama3.2; 180 s; reads only; raises needs_tool, technical, hard, deliver, prose, suspicious)    2.6 s
    Router (qwen3.5:4b; every skill; when needs_tool)                                                        11.7 s
    Security Guardian (llama3.2; wakes first on has_feed or suspicious; SAFE or UNSAFE, anything else refused) 0.4 s
    Expert Coder (qwen2.5-coder:14b; after the Router on technical; holds no tools; its code is saved by the engine) 16.4 s
    Reasoner (qwen3.5:9b; after the Router on hard)                                                          173.8 s
    Quality Evaluator (qwen3.5:4b; on drifted or review; "PASS" keeps the draft, "NEEDS:" sends it back once) 18.9 s
    Proofreader (phi4-mini; last, on prose) 15.1 s; Delivery Agent (phi4-mini; last, on deliver) 13.8 s; Neiro (llama3.2) 2.1 s;
    Jesster (deepseek-r1:8b) 5.4 s; Judge (gemma4:12b; 16384 window) 142.8 s; Quartermaster (llama3.2; last, on rack) 5.1 s;
    Morning Reviewer (llama3.2; brief only) 42.1 s; Deep Researcher (qwen3.5:9b; only through deep_research)

As it stands a seat whose name has a space cannot be addressed with @ (`@deep researcher` asks for "deep"); the failure card's
"retry" does what "skip" does; the unknown-skill message still counts "thirty-seven" skills.

**The commands** (handle_command, cli.py:659-890; each ends a glass turn with a `command` event):

- **/help [words]** -- the palette, filtered; an unknown `/thing` is taken as a search ("nothing in the palette matches '<q>'.").
  It does not list /drive.
- **/pipelines, /pipeline, /use <name>, /agents, /skills, /reload** -- the running orders; the active one; switch ("  unknown
  pipeline '<x>'. Available: ..."); the seats; the skills (! marks a binding fault); read agents/, skills/ and commands.md again
  (the watcher does this between turns anyway).
- **/remember [words], /memory, and "remember that[: words]"** -- a memory: the words, else the newest seat proposal, else the
  last delivery; a kind (one word; three wrong answers fall back to the default); "  Land this in memory.md? [y/N]". /memory:
  "  [l]and  [d]rop  [s]top:". "nothing to remember yet -- no proposal, no delivery. Say `remember that: <the words>`."
- **/git [diff|branch|branch <n>|switch|close|commit <msg>|push|pull|remote|init|help]** -- every write asks [y/N]; push and pull
  behind MANJUEL_GIT_REMOTE; a push from main refused when origin has main; after a push "proven landed" or "IT DID NOT LAND".
- **/toll, "pay the toll"** -- asks "What proved?", "What is thin?", "What is owed?" (a bare yes or no is refused: "'<x>' is a
  yes/no, and this asks for words."), then "  Append this toll?"; appends SEAT_LOG.md and refreshes SEAT_LOG_INDEX.md.
- **/sittings, /status, /brief, /last** -- past sittings; the boot report; the Steward seat's brief from the record (any number
  or hash it says that is not in the facts is flagged); the last answer again.
- **/index, /find <q>, /rack, /models [GB], /model [<tag>|<seat> <tag>|reset], /warm** -- refresh the index; search by meaning;
  rack_sync; the VRAM plan; one model for every seat (or one seat) for this sitting only (agents/ is never written; "no seat named
  '<s>'. Nothing changed."; "'<tag>' is not installed. Nothing changed."); load this pipeline's models now (never evicting another
  client's: "not warming: ... belongs to another client").
- **/say, /chat, /listen, /paste, /new, /resume** -- speak deliveries; voice chat; one spoken question (as it stands it never runs
  in the glass); stage pasted material for the Security Guardian (lines ended by a single "."); drop or pick up the thread.
- **/table <q>** -- the court's seats on one question, read-only, the Judge ruling ("no `court` pipeline declared in
  pipelines.md"; "table adjourned.").
- **/parity [hosted]** -- the chain measured against bare calls; says what will leave and asks "run them? [y/N]"; writes
  logs/parity_<stamp>.md and sessions/parity_history.jsonl.
- **@<seat> <words>** -- one seat alone, no tools; kept out of the shared thread ("no seat called '<x>'. /agents lists them.").
- **commands.md's own: /morning, /sitting <n>, /covenant** -- run as typed objectives in the REPL; as it stands, in the glass the
  engine stores what they would run and never runs it, and a `**Method:**` line rides on the next, unrelated turn.
- **exit, quit, /exit** -- close the sitting (an unattended toll if anything ran).

**The flows** (flows/*.json, run by the door; their times from flows/runs.jsonl): smoke v1 (ask -> eval "ready"; COMPLETE 0.2 to
57.3 s); version-bump v1 (run -> gate -> run; COMPLETE about 50 s); wife-test v1 (make -> eval "RAN:" -> want -> eval -> talk;
COMPLETE 51.5 to 200.2 s); coder v14 (RETIRED, superseded by coder-tree); coder-tree v5 (brief -> open gate -> line -> attempt,
looping twice -> changed -> strokes -> strokes_ok -> smoke -> smoke_ok -> land gate -> save; 3600 s budget; one COMPLETE at 315.2
s); version-tag v4 (RETIRED, superseded by release); release v5 (the cut through pull requests inside three gates; 14400 s
budget; no COMPLETE yet).

**The model route** (us/route_anthropic.us; routes.py): off unless MANJUEL_ROUTE_ANTHROPIC_KEY is set by him; reached only by
`/parity hosted`; no seat sits on it.

### 5.8 How a use of a skill or a tool is recorded today

Before a use: the engine emits `{"event":"tool","action","args"}` on its wire for every skill call of a door turn (serve.py:422-443;
the glass draws it; it is not kept on disk); the door writes a `held` row before a held writing call; the driver asks his card
before every write (asked, not recorded). After a use: the `tool_result` event {action, failed (the answer begins Error, Refused or
Cannot), chars, head}; each Steward job's transcript (logs/<stamp>_drive.md: every step's arguments and whole result, no time
per step, written when the job ends); the sitting's run row (tools by name only); the glass's trace of every call it made itself
(its status always "ok"); the door's hold rows; a flow node's {status, pass, latency_ms}. The skill library's before_tool and
after_tool hooks (skills.py:230, 4887-4970) run on every call the driver makes, and no skill declares one. Per skill and tool,
what is written down is: its own file (skills/*.md: what Steward is shown, to 400 characters); its capability record
(us/manjuel.us: what it may touch); its handler's lines (BUILDMAP.md); one live run and its time (sections 1 to 4 above, by
hand); and this section's card.
