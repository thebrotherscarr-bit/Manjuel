# WHAT'S LEFT

Everything still open, in one place, in plain words.

Written by hand on 2026-09-29 from the record: TASKS.md (all 35 open boxes), SPEC.md section 4
(all 5 OPEN lines), HANDOFF.md (09-28 and 09-29), DAYBOOK.md (session 18), CHANGELOG.md and
STATUS.md. The source is named at the end of every line.

Every line has a number. Say the number to order the work: "do C10".

This file is the list behind the webapp's **What's left** page. Read it there: the page counts
the lines, finds words in them, and names any line it cannot number.

---

## A. Stops the release right now

The release is core **v0.1.16** and atlas **v0.1.9**. Neither tag is cut.

- **A2. The release check has not passed.** Last result: 14 lines ok, 1 refused (the live
  check, fixed since: see A1 under Done). *(STATUS)*
- **A3. The two tags are not cut.** Core v0.1.16 and atlas v0.1.9, from the dashboard's Version
  control page, after A2. *(HANDOFF 09-29)*
- **A4. GitHub's automatic tests were red on Windows.** Fixed here on 2026-09-29 and waiting
  on GitHub's next run to confirm. The test counted browsers the instant a page check ended, and
  counted other runs' browsers too. It now counts only its own and gives them 20 seconds to
  close. *(HANDOFF 09-28, CHANGELOG)*
- **A5. The atlas v0.1.8 release on GitHub is still a draft.** It waits for you to publish it.
  *(HANDOFF 09-28)*

---

## B. Decisions only you can make

Nothing here gets built until you say which way.

- **B1. The coding model.** qwen2.5-coder:7b was shown "this was refused, do not answer it again"
  and gave the same refused code again, 3 times out of 3 (runs seven and eight). Move the coding
  seat to another model, or leave it? *(HANDOFF 09-29)*
- **B2. The front-door model.** llama3.2 makes up numbers, repeats the question back as its
  opinion at the review panel, and once read its own instructions out as the answer. Wrong
  numbers get stamped now, but the model still does it. Replace it, or leave it? *(SPEC 4.7)*
- **B3. Line endings.** The rule says CRLF everywhere. The disk is mostly LF (143 LF, 32 CRLF,
  counted 09-14). Convert the files, or change the rule to LF? *(SPEC 4.5)*
- **B4. Laws with nothing enforcing them.** ESTATE LAW 2 (originals are read-only) is only a
  comment: the tools can still reach `worlds/`. ESTATE LAWS 3 and 4 have no mechanism at all.
  Build the enforcement, or accept it as is? *(SPEC 4.4)*
- **B5. The client-name scrub.** Done everywhere except the local branch `pre-strip-master`,
  which you ruled to keep. SPEC still marks the line OPEN. Mark it done? *(SPEC 4.5)*
- **B6. Should the rack report tool be allowed at the review panel?** It is read-only, but it
  wakes a model each time, and `rack_list` already gives the same numbers. *(TASKS)*
- **B7. Should the front door speak at the review panel at all?** Four panels running, its
  opinion was the question repeated back in 0.4 seconds, and the panel ruled on that. *(TASKS)*
- **B8. The `.env` reader keeps a comment after a value as part of the value.** Strip it, or
  leave it? *(TASKS)*
- **B9. RULE 9's wording is out of date.** It says every changed text file is re-indexed. The
  watcher now re-indexes only the listed folders. The new wording is yours. *(TASKS)*
- **B10. The Router's prompt says "the objective names the skill X"** even when the engine picked
  the tool and you never named it. The new wording is yours. *(TASKS)*
- **B11. The hardening work has no version number.** Six things were pushed from 0.1.9 to 0.1.10
  and never shipped. Which version carries them? *(TASKS)*
- **B12. The two sitting laws (5 and 6).** TASKS still lists them open. SPEC says they were
  sealed on 2026-09-21. It looks done and needs your tick. *(TASKS, SPEC 4.4)*
- **B13. SEAT_LOG numbering.** 14 gaps and 10 duplicate numbers. You asked for "sorted and
  numbered", but the log is append-only. The proposal was a generated sorted index beside it.
  Which did you mean? *(SPEC 4.5)*
- **B14. Simplifying the system.** Proposed today, nothing decided: retire the unused atlas code
  (the Rust part is 35 files, 8,887 lines), one table for reading intent instead of several,
  fewer seats, a shorter record. *(today's conversation)*

---

## C. Bugs and problems, known and not fixed

### The models misbehaving

- **C1. The Router passes whole sentences to file tools as if they were paths.** Partly fixed on
  09-07. The habit remains. *(TASKS, in hand)*
- **C2. When a tool fails, the Router writes about the next step instead of doing it.** Needs
  measuring before anything is built. *(TASKS)*
- **C3. The front door answers "what does the covenant say?" from the law text in its own
  prompt,** not from the file. This is the same question that fails in A1. *(TASKS)*
- **C4. The law text leaks into answers.** First fix built (it rides in the system role). A guard
  that refuses an answer reciting it is not built. *(TASKS, in hand)*
- **C5. The front door copies internal labels into answers:** "Router produced:", "The operator
  asked:". *(TASKS)*
- **C6. The closing step once read its own instruction back as the answer.** *(TASKS)*
- **C7. The model list answer dropped a model:** eleven installed, ten listed. *(TASKS)*
- **C8. A model can say it used a tool when it did not.** The Steward claimed an edit that never
  happened. No check catches it. *(HANDOFF 09-28)*

### The engine

- **C11. The drift score prints "no usable source"** when the check was never switched on. There
  is dead code beside it in `drift.py`. Half fixed. *(TASKS)*
- **C13. The review panel does not fit its time limit.** On 09-28 it scored 0 of 1: one seat was
  cut at 552 seconds and the judge never got a turn. *(HANDOFF 09-28, TASKS)*
- **C14. A failing seat asks "retry / skip / abort?"** An automated flow cannot answer, so the
  run dies. *(HANDOFF 09-28)*
- **C15. The file watcher's re-index can run on top of an index build already running.** *(TASKS)*
- **C16. The workspace file reader cannot read the rest of the ground.** *(TASKS)*
- **C17. An idle close is logged as a "Dashboard Close".** The log has no field for why, and the
  idle warning does not mention the 30-minute close. *(TASKS)*
- **C18. `run_start` cannot choose a model head.** `flow_run` can. *(HANDOFF 09-28)*
- **C19. The live check's greeting case cannot tell a real answer from a recited one.**
  *(HANDOFF 09-28)*
- **C20. A dozen small honesty fixes:** an unreadable `.env` is not reported, `MANJUEL_OLLAMA_HOST`
  is never read, dead code, and others. *(TASKS, "small honesty")*
- **C21. `history_block` has a limit nothing uses,** and some work done every turn could be done
  once. *(TASKS)*
- **C30. The engine does not say when a model's reply was cut off by a full window.** The
  rack reports it; the transcript only said "(deliberation only, no conclusion reached)". That
  is how A1 hid for a day. *(found 2026-09-29, CHANGELOG)*

### The dashboard and the tool server (atlas)

- **C22. SECURITY. The dashboard listens on every network address (port 8091),** not only this
  machine, and nothing calls its login gate. Ollama listens on every address too. Measured
  09-17, not re-checked. *(TASKS)*
- **C23. `GetAgent` hands back a pointer that can race with `UpsertAgent`.** And `Run.check` reads
  a 502 error as "no engine open". *(TASKS)*
- **C24. `/run/listen` can stall** (the same bug was fixed in `/run/stream`), and `/chat/stream`
  keeps writing after the browser has gone. *(TASKS)*
- **C25. The dashboard forgets a paused flow when the page reloads.** *(HANDOFF 09-28)*
- **C26. The Tools page's Call button uses a pop-up** that the desktop app's browser dismisses.
  *(HANDOFF 09-28)*
- **C27. A finished turn's bubble stays marked "live".** *(TASKS)*
- **C28. The dashboard says closing always pays its toll,** in three places. It does not.
  *(TASKS)*
- **C29. "The two banner literals".** Listed as open in HANDOFF 09-28 with no detail there.
  *(HANDOFF 09-28)*

---

## D. Built but not finished, or not hooked up

- **D1. The time limits you ruled are not set.** Steward 180 seconds, review panel 900. *(DAYBOOK s18)*
- **D2. The "make me a game" test, run as a flow, makes nothing.** Two runs on 09-28: both
  times the make step read files and talked. *(HANDOFF 09-28)*
- **D3. The flows `coder` and `version-tag` have been fired and have never finished
  successfully.** *(STATUS)*
- **D4. The flow builder has no box for loops.** A looping flow has to be saved as JSON.
  *(HANDOFF 09-28)*
- **D5. The dashboard has no button for the live check.** *(DAYBOOK s18)*
- **D6. Version control has no merge button.** Merging a work branch into main is done in the
  terminal. *(HANDOFF 09-28)*
- **D7. The tool server's 85 tools have no permission records.** *(HANDOFF 09-28)*
- **D8. REFUSALS.md documents 28 refusals. The code has 66.** They are not linked.
  *(HANDOFF 09-28)*
- **D9. The release check does not read GitHub's test result.** *(HANDOFF 09-28)*
- **D10. STATUS.md is not in the search index list,** so the system cannot find it by search.
  *(today's conversation)*
- **D11. The self-test suite is one third done.** Part 1 landed. Part 2 (a test-case generator)
  and part 3 (REFUSALS.md findable by search) are not scheduled. *(TASKS, in hand)*
- **D12. atlas: the `release.yml` fix rides with the next version,** and no draft release was
  made for v0.1.5. *(TASKS)*
- **D13. The front-end agent handoff plan** is named and not written. *(DAYBOOK s18)*
- **D14. "The map's how-to-ask"** is named and not written. *(DAYBOOK s18)*
- **D15. This list is kept by hand.** The webapp's page names a line with no number or a
  number used twice. Nothing warns anyone when the list is simply out of date.

---

## E. Never tested for real

- **E1. The wife test.** Someone who is not you sits at the dashboard, asks it to make something
  in her own words, and uses the result with no help. All three pieces are built. The test has
  not been run. *(SPEC 4.8)*
- **E2. An idle close of a session that actually ran something.** *(TASKS)*
- **E3. Whether the Router listing the scratch folder means it is unsure.** Needs enough runs to
  tell. *(TASKS)*

---

## F. Paperwork that is out of date

- **F1. The plan is three weeks old.** SPEC section 8.2 and BUILDPATH's version ladder stop at
  2026-09-17. Four core versions and three atlas versions were cut after that. *(CHANGELOG)*
- **F2. Four version headings in CHANGELOG name old commit numbers,** from before the history
  rewrite of 09-21: v0.1.13, v0.1.12, v0.1.11, 0.1.7. The 0.1.9 heading names none. *(STATUS)*
- **F3. DAYBOOK has no entry for 09-10 or 09-11,** and Session 8's "next session" line is in a
  form the reader cannot parse. *(TASKS)*
- **F4. SPEC has no section for the coder changing the system's own files.** *(DAYBOOK s18)*
- **F5. HANDOFF 09-28's "Still open" paragraph lists two things that were built later the same
  day:** the key shown in the hold queue, and the crossed gate. *(HANDOFF 09-28)*
- **F6. TASKS.md has boxes that are half done and still open:** the sitting laws (B12);
  "rack_report facts-only" (done) beside "the door at court" (open, B7); "the client token"
  (done, B5) beside "CRLF or LF" (open, B3). Only you tick a box. *(TASKS)*
- **F7. TASKS.md boxes for work finished on 2026-09-29 are still unticked:** the false refusal
  (C10) and the card that cannot say "over" (C12). Both are under Done below. Only you tick a
  box. *(TASKS)*

---

## G. The release checklist, in order

Already done: version numbers set (0.1.16 and 0.1.9), both changelogs folded, STATUS.md printed,
both main branches sent to GitHub (core `f8203d1`, atlas `86ba8f8`).

- [x] 1. Find out why the Router quits early, and fix it (A1)
- [x] 2. Run the live check until it is 9 of 9
- [ ] 3. Run the release check for v0.1.16 on your terminal: every line ok
- [ ] 4. Run atlas's proof
- [ ] 5. Cut and send the tag v0.1.16 (core) from Version control
- [ ] 6. Cut and send the tag v0.1.9 (atlas) from Version control
- [ ] 7. Publish the atlas v0.1.8 draft on GitHub, or drop it (A5)
- [ ] 8. Look at GitHub's tests after the tag (A4)

---

## Done

Finished lines, newest first. A number is never used again.

- **A1. The live check fails 1 of 9.** DONE 2026-09-29. The Router is sent every tool's
  description on every turn. That request had grown to 8,182 tokens in a window of 8,192, so it
  had about ten tokens to answer in; the two tools added on 09-28 filled it. Its window is
  16,384 now (the Quality Evaluator's too, because they share a model). Live check: 9 of 9
  (sitting 298). A test now goes red before the request outgrows the window again.
  *(CHANGELOG, "The Router's window")*
- **C9. The Router's prompt fills 7,526 of its 8,192-token window.** DONE 2026-09-29 with A1.
  Measured at 8,182 that day; the window is 16,384 now. *(CHANGELOG)*
- **C10. A refusal message says something false.** DONE 2026-09-29. A refused tool is called a
  writer only when it is one; the rest are told "is not cleared for the table". The TASKS box is
  yours to tick (F7). *(CHANGELOG)*
- **C12. The GPU memory report cannot say "over".** DONE 2026-09-29. An overcommitted card says
  "OVER by ~0.5GB", and every size says whether it is on disk or in memory. The TASKS box is
  yours to tick (F7). *(CHANGELOG)*

---

## The words

| Plain word here | The name in the record |
|---|---|
| live check | the standup (`tests/standup.py`) |
| release check | the gate (`tests/release.py`) |
| tests | the strokes and the smoke (`tests/test_manjuel.py`, `tests/smoke_cli.py`) |
| review panel | the court |
| front door | the Steward seat (llama3.2) |
| tool-picking model | the Router seat (qwen3.5:4b) |
| coding model | the Expert Coder seat (qwen2.5-coder:7b) |
| dashboard | the glass (`atlas-webapp`, port 8091) |
| tool server | the door (`atlas-mcp`, port 8090) |
| session | a sitting |
| tag | a mark |
| work branch | a line of work |

## How this page is kept

By hand, in this one file. Whoever finishes something moves its line to a section named
`## Done` at the foot of this file, with the date, in the same pass. Whoever finds something new
adds it under its letter, with the next number, in plain words. Numbers are never reused.
