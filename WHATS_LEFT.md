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

The release is core **v0.1.16** and atlas **v0.1.9**. Both tags are cut and on GitHub
(2026-09-29). One thing is left, and it needs your GitHub sign-in.

- **A5. The atlas releases on GitHub are drafts.** v0.1.8 has waited since 09-25, and the
  v0.1.9 tag has started the workflow that drafts its release. Publishing a draft is done
  signed in to GitHub, which this hand is not. *(HANDOFF 09-28, GitHub)*

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
- **B15. The review panel's two thinking seats have no limit on how long an answer may be.**
  Jesster (deepseek-r1:8b) and the judge (gemma4:12b) each think until they stop by
  themselves or the clock cuts them. When Jesster finishes it takes 72 to 500 seconds; four
  times it never finished and was cut (760, 577, 552 and 600 seconds). The judge takes 100 to
  380 seconds when it finishes. With your limits set, the run of 2026-09-29 seated the judge
  with 289 seconds left and cut it there: 0 of 1 (C13). On 09-07 you ruled to give the judge
  room to think and to limit its turns, not its length, so a cap is yours to order.
  RECOMMENDED: give Jesster a maximum answer length, so the model server stops it and the
  engine asks once more for the ruling with thinking off (the mechanism built on 09-07), and
  leave the judge as it is. The other ways: a shorter time limit for Jesster alone (400 would
  leave the judge 490), or a smaller model in Jesster's seat.
  *(logs/standup_2026-09-29_162318.md, every court transcript in logs/)*
- **B16. A merge button on Version control (was D6).** Merging a work branch into main is
  still done in the terminal. The tool server refuses the word `merge` by its own founding
  law: the eight forbidden verbs (approve, ascend, merge, commit, push, delete, reject,
  promote) are absent from its table by construction, and a button needs a tool behind it.
  Saving and sending already exist under other names (`git_commit`, `git_push`), so this is
  your call, not the code's: allow a `git_branch` action that lands a line of work into main
  (fast-forward only, refused over unsaved work, like the others), or keep merging in the
  terminal. RECOMMENDED: allow it as a `git_branch` action named `land`, since it is a button
  you press yourself, like Save and Send. *(HANDOFF 09-28, tools.go)*
- **B17. What DONE means for the coder changing the system's own files (SPEC 4.9).** The
  section is written from the record with three MET lines; its OPEN line proposes the finish
  from your words of 09-28 and the loop law: a change asked for in one sentence from the
  dashboard, made on a work branch, proved green by the tests through the tool server, saved by
  the council, and landed on main by your click alone -- twice running, every step in the
  record. Confirm it, reword it, or strike it. *(SPEC 4.9, 2026-09-30)*

---

## C. Bugs and problems, known and not fixed

### The models misbehaving

- **C1. The Router passes whole sentences to file tools as if they were paths.** Partly fixed on
  09-07: the engine refuses the sentence by name. Measured 2026-09-30 over every transcript: 10
  of 97 file-tool calls before the fix, 28 of 261 in the fortnight after (the last ordinary one
  on 09-10), and 3 of 93 since 09-21 -- all three in one coder-flow run on 09-28, where the
  prompt's own instruction block was passed as the path. Gone from ordinary turns; three percent
  in the coder's. *(TASKS, in hand; CHANGELOG, "Three measurements the list asked for")*
- **C6. The closing step once read its own instruction back as the answer.** Measured
  2026-09-30: four times since 09-07 (a sentence of the front door's own instructions in the
  answer), two of them since 09-21. The live check's greeting case catches it since 09-29; the
  engine's new recital guard reads the law block only. *(TASKS; CHANGELOG, "Six more sightings
  given their numbers")*
- **C7. The model list answer dropped a model:** eleven installed, ten listed. Measured
  2026-09-30: of fourteen "what models are on the rack" turns, the answer named all eleven
  twice; today's eight named 3, 0, 11, 8, 4, 0, 0 and 3. The live check asks only that the tool
  ran and no number was invented. The model at the door is your B2. *(TASKS; CHANGELOG, "Six
  more sightings given their numbers")*
- **C8. A model can say it used a tool when it did not.** The Steward claimed an edit that never
  happened. No check catches it. Measured 2026-09-30: a claim with no tool call in the turn, 22
  of 634 answers before 09-07, 3 of 480 after, 1 of 251 since 09-21. Rare now; still no check.
  *(HANDOFF 09-28; CHANGELOG, "Six more sightings given their numbers")*
- **C33. At the review panel, two seats did another seat's job.** On 2026-09-29 (sitting 301)
  Neiro wrote "The Court's Ruling" itself, which is the judge's job, and the Router answered
  "No skill is needed" when the engine had chosen a search for it. The engine stamped the
  second one ("THE NAMED TOOL DID NOT RUN"); nothing catches the first. Measured 2026-09-30
  over all forty court runs: Neiro wrote a ruling heading of its own in 16, Jesster in 23 -- the
  rule, not the exception -- and the named-tool stamp fired in three. The judge still rules
  after them. *(logs/2026-09-29_160817_should_a_court_of_three_seats_run_on_one.md; CHANGELOG,
  "Six more sightings given their numbers")*

### The engine

- **C13. The review panel does not fit its time limit.** Measured again on 2026-09-29 with your
  limits set (900 for the panel, 600 a seat): 0 of 1. The judge got a turn this time, with 289
  seconds left, and was cut; Jesster ran its whole 600 and was cut. Your numbers are in and
  working, and they are not enough by themselves: the next step is your decision B15.
  *(logs/standup_2026-09-29_162318.md)*

### The dashboard and the tool server (atlas)


---

## D. Built but not finished, or not hooked up

- **D3. The flows `coder` and `version-tag` have been fired and have never finished
  successfully.** Read off the record 2026-09-30: `coder` (19 runs, none finished, last
  2026-09-21) was superseded by `coder-tree`, which finished on 2026-09-29 (run six, COMPLETE).
  `version-tag` (5 runs) last failed on 2026-09-28 because the mark it was told to cut,
  v0.1.15, already existed, so its check for "Cut v0.1.15 at" could not pass; the two before
  were stopped by hand. It can only finish at the next version, which is yours to cut. *(STATUS,
  flows/runs.jsonl)*
- **D7. The tool server's 85 tools have no permission records.** *(HANDOFF 09-28)*
- **D9. The release check does not read GitHub's test result.** It cost something on
  2026-09-29: the check passed 17 of 17 and the v0.1.16 tag was cut while GitHub's own run on
  that tag was red on every machine (C34, under Done). *(HANDOFF 09-28, GitHub run 170)*
- **D11. The self-test suite is one third done.** Part 1 landed. Part 2 (a test-case generator)
  is not scheduled: yours to order. Part 3 (REFUSALS.md findable by search) is true by another
  road since 2026-09-29: every root document is in the index list, held by a test, and the
  document now ends with every refusal site in the code (D8). *(TASKS, in hand)*

---

## E. Never tested for real

- **E1. The wife test.** Someone who is not you sits at the dashboard, asks it to make something
  in her own words, and uses the result with no help. All three pieces are built. The test has
  not been run. *(SPEC 4.8)*

---

## F. Paperwork that is out of date

- **F3. DAYBOOK has no entry for 09-10 or 09-11.** The other half is done (2026-09-30):
  Session 8's "next session" line is in the form the reader parses. The two missing days are
  in the CHANGELOG (0.1.9 and the hardening that followed it) and could be written from it;
  say so if you want them written. *(TASKS)*
- **F6. TASKS.md has boxes that are half done and still open:** the sitting laws (B12);
  "rack_report facts-only" (done) beside "the door at court" (open, B7); "the client token"
  (done, B5) beside "CRLF or LF" (open, B3). Only you tick a box. *(TASKS)*
- **F7. TASKS.md boxes for work finished on 2026-09-29 are still unticked:** the false refusal
  (C10), the card that cannot say "over" (C12), the drift note (C11), the watcher's re-index
  (C15), the workspace reader (C16), the small honesty list (C20) and the unused limit (C21).
  All are under Done below or marked done on their line. Only you tick a box. *(TASKS)*

---

## G. The release checklist, in order

Already done: version numbers set (0.1.16 and 0.1.9), both changelogs folded, STATUS.md printed,
both main branches sent to GitHub (core `f8203d1`, atlas `86ba8f8`).

- [x] 1. Find out why the Router quits early, and fix it (A1)
- [x] 2. Run the live check until it is 9 of 9
- [x] 3. Run the release check for v0.1.16: every line ok (16 of 16, 2026-09-29 15:10)
- [x] 4. Run atlas's proof (21 held, 14 absent, 0 broke, 2026-09-29)
- [x] 5. Cut and send the tag v0.1.16 (core) from Version control (on `e8aa9b5`)
- [x] 6. Cut and send the tag v0.1.9 (atlas) from Version control (on `b1059a1`)
- [ ] 7. Publish the atlas drafts on GitHub, v0.1.8 and v0.1.9, or drop them (A5)
- [x] 8. Look at GitHub's tests after the tag: green on both main branches (A4). The core
  tag's own run was red and was not read until later that day; fixed on main (C34)

---

## Done

Finished lines, newest first. A number is never used again.

- **D2. The "make me a game" test, run as a flow, makes nothing.** DONE 2026-09-30. The cause
  was the words: the maker knew "make me a game" and not her "try making me a little game" or
  "i want a game i can play" (the test's own recorded messages), so her turns went to the
  ordinary pipeline and talked. The maker reads those forms now. Fired live from the dashboard:
  the flow completed in 52 seconds and made two playable pages, `projects/game` and
  `projects/game-2`. Her second message made a second game rather than changing the first,
  because it opens with no change verb -- yours to say whether "want it ..." should count as
  one. *(CHANGELOG, "The maker reads her own words")*
- **C21. Some work done every turn could be done once.** DONE 2026-09-30, by measurement: the
  engine's own time is a hundredth of a second inside a run and a tenth of a second a turn
  outside it. Nothing to make once. *(CHANGELOG, "The turn's overhead, measured")*
- **C5. The front door copies internal labels into answers.** DONE 2026-09-30. Measured first
  (seven answers since 09-07, every one opening with a label -- one in this morning's live
  check), then fixed with the rule that already threw out a copied conversation: an answer that
  opens with "Router produced:", a turn label, "They asked:" or the conversation heading is
  thrown out and named in the record, and the real work's words stand in its place. *(CHANGELOG,
  "The scaffold parrot knows the labels the record actually leaked")*
- **C3. The front door answers "what does the covenant say?" from the law text in its own
  prompt, not from the file.** DONE 2026-09-30, by measurement: of 71 such turns on record, one
  answer recited the law block (this morning at 09:06, the case the new guard throws out), fifty
  carry a passage from a file or search result of the same turn, and every one of the fourteen
  since 09-29 searched first. *(CHANGELOG, "Six more sightings given their numbers")*
- **C2. When a tool fails, the Router writes about the next step instead of doing it.** DONE
  2026-09-30, by measurement: since 09-07, 56 of 80 failed tool calls were followed by another
  call in the same turn, which is what the TASKS box asked to see. Of the seven since 09-21 that
  were not, four could not be corrected by any retry (a mark that already exists), two were C1,
  and one had already retried once. Nothing built. The box is yours to tick. *(CHANGELOG, "Three
  measurements the list asked for")*
- **E3. Whether the Router listing the scratch folder means it is unsure.** DONE 2026-09-30, by
  measurement: it means a wrong call is coming, not a thin answer. Turns with the listing beside
  another tool had a tool fail 45% of the time against 13% without it; their answers were thin no
  more often (2% against 3%). The call stays, as the box says: it is the one visible tell.
  *(CHANGELOG, "Three measurements the list asked for")*
- **E2. An idle close of a session that actually ran something.** DONE 2026-09-30, for real:
  sitting 315 was opened from the dashboard, ran one turn at 09:20, and was left alone; at 09:50
  the engine closed it by itself, paid the toll, and wrote why on both the session record and
  the toll ("idle: no command in 30 minutes"). The TASKS box that names this is yours to tick.
  *(CHANGELOG, "An idle close of a sitting that ran something, fired live")*
- **C4. The law text leaks into answers.** DONE 2026-09-30. Measured first, as the task line
  asked: in the 910 turns since the first fix, two answers read the law block aloud (09-10, and
  the covenant question at 09:06 today) and the Router once; ten other sightings were tool
  results, not answers. Now an answer that repeats a whole sentence of the block is thrown out
  and named in the record, the way an answer that repeats the conversation scaffold is; an
  answer that merely mentions the law stands. The engine and the live check use one definition
  of "repeats". *(CHANGELOG, "A seat that reads the law block aloud is discarded")*
- **D15. This list is kept by hand.** DONE 2026-09-30, as far as a machine can help. A test
  now fails the suites, here and on GitHub, when a line has no number, a number is used twice or
  sits under the wrong letter, an open line already says DONE with a date, a line cites a
  CHANGELOG entry that is not there, or the release checklist's version is not the one set. The
  page still names its own faults in red. *(CHANGELOG, "The list of what is left has a wire")*
- **F1. The plan is three weeks old.** DONE 2026-09-30. Every theme in SPEC 8.2 carries a dated
  line saying where it stands today (two are met by the record, two wait on you), and BUILDPATH
  has the ladder of the versions cut since 09-17 -- five core and four atlas, one more of each
  than this line had counted -- with their dates, their words and the commit each mark sits on
  now. Nothing was rewritten. A test now fails the suites at the next version cut until the
  ladder names it. *(CHANGELOG, "The plan caught up to the record")*
- **F4. SPEC has no section for the coder changing the system's own files.** DONE 2026-09-30,
  with one line left to you: section 4.9 has three MET lines from the record and one OPEN line
  proposing what DONE means, from your words of 09-28 -- confirm or reword it (B17). *(SPEC 4.9)*
- **C31. Four old model processes from 2026-09-29 07:52 held about 4 GB of graphics memory.**
  DONE 2026-09-30 08:36. You restarted the Ollama app (its new process 31652); the four
  survived that, because they were nobody's children by then, and on your word I stopped
  exactly those four by pid (80252, 73948, 14820, 74884). The live check right after: 9 of 9
  in 131 seconds, against 505 to 613 seconds in the hour before. *(measured)*
- **D12. atlas: the `release.yml` fix rides with the next version, and no draft release was
  made for v0.1.5.** DONE by events, noted 2026-09-30: the fix rode with v0.1.7 (2026-09-23),
  and v0.1.8 and v0.1.9 both have drafts on GitHub waiting on you (A5). v0.1.5 never will; it
  is superseded. *(atlas CHANGELOG, GitHub)*
- **D8. REFUSALS.md documents 28 refusals. The code has 66. They are not linked.** DONE
  2026-09-30. The document now ends with a generated list of every refusal site in the code
  (module, line, words) with the two counts side by side (32 written up, 89 sites), kept
  current by a check the tests and GitHub both run. The hand-written part is untouched.
  GitHub's two older-Python legs then failed on one line of that script (a backslash in an
  f-string, which Python 3.10 refuses); fixed the same morning, the output unchanged.
  *(CHANGELOG, "REFUSALS.md and the code are joined"; "GitHub's 3.10 legs died at import")*
- **D14. "The map's how-to-ask".** DONE 2026-09-30. BUILDMAP.md opens with HOW TO ASK: the
  words that put a change to a named definition in front of the coding seat, with an example
  the engine itself is held to. *(CHANGELOG, "The map says how to ask")*
- **D13. The front-end agent handoff plan.** DONE, and it already was: it is the HANDOFF block
  of 2026-09-22, "THE HANDOFF — running this without a hand at the front" (what runs, the day's
  four acts, what only you can do, what a hand owes you, where the record is, the traps). The
  list line was stale. Its pids and counts are of that day; the day's own block is the
  current state. *(HANDOFF 09-22)*
- **F2. Four version headings in CHANGELOG name old commit numbers.** DONE 2026-09-30. Each
  keeps its old number and carries the one the version sits on since the history rewrite
  beside it; the 0.1.9 heading names its commit; the release check reads the new number and
  the status page now says all eight sit where they say. *(CHANGELOG, "The four headings")*
- **F5. HANDOFF 09-28's "Still open" paragraph lists two things built later that day.** DONE
  2026-09-30: a note under it says what was built when, and nothing above it changed.
  *(HANDOFF 09-28)*
- **C35. One atlas script's "check only" mode also writes.** DONE 2026-09-30. A verify with no
  database says so and writes nothing; the cutters' proof has a leg for it. *(atlas CHANGELOG)*
- **C17. The dashboard's idle warning does not mention the 30-minute close.** DONE 2026-09-30,
  both halves. The idle line now says the engine closes itself at 30 minutes idle and how many
  minutes are left. *(atlas CHANGELOG, "The glass's batch")*
- **C23. `GetAgent` hands back a pointer that can race with `UpsertAgent`; `Run.check` reads a
  502 as "no engine open".** DONE 2026-09-30, both. The store hands back a copy, and the
  dashboard now says "Door silent" when the tool server does not answer instead of offering
  to boot an engine. *(atlas CHANGELOG)*
- **C25. The dashboard forgets a paused flow when the page reloads.** DONE 2026-09-30. The
  Workflows page reads every run from the record on arrival and lists the paused ones under
  "Waiting on you", each one click from its waterfall and its two buttons. *(atlas CHANGELOG)*
- **C26. The Tools page's Call button uses a pop-up.** DONE 2026-09-30. Call asks in the page's
  own window now, with the tool's arguments listed; the eval scorer's three pop-ups went the
  same way, and a test refuses any pop-up in any script. *(atlas CHANGELOG)*
- **C27. A finished turn's bubble stays marked "live".** DONE 2026-09-30. A turn watched from
  another window ended on a word the pages did not listen for. *(atlas CHANGELOG)*
- **C28. The dashboard says closing always pays its toll.** DONE 2026-09-30, all three places:
  they say "no toll is owed" when no turn ran, which is what the engine does. *(atlas CHANGELOG)*
- **C29. "The two banner literals".** DONE 2026-09-30. They were the covenant hash typed by
  hand in the dashboard's sidebar and the TUI's banner; both read it from the operator's own
  declaration now. *(atlas CHANGELOG)*
- **D4. The flow builder has no box for loops.** DONE 2026-09-30. Every step that does work
  has one (0 to 5); checks and gates do not, because the engine refuses it there. *(atlas
  CHANGELOG)*
- **D5. The dashboard has no button for the live check.** DONE 2026-09-30. "Run the live check"
  stands beside "Boot an engine" when no engine is open. *(atlas CHANGELOG)*
- **C14. A failing seat asks "retry / skip / abort?"** DONE 2026-09-29, both halves. The
  engine does not ask on a turn nobody attends (the morning's half), and the tool server now
  tells it so for every step of a flow, so a flow no longer dies at that question: the seat is
  skipped, the question's own default, and the run says so. Any other question a flow's step
  raises still stops it, because that gate is yours. The tool server was rebuilt and
  restarted. *(atlas CHANGELOG, "The door's batch")*
- **C18. `run_start` cannot choose a model head.** DONE 2026-09-29. It takes `voice` (every
  seat on one model for the turn) and `voices` (a model per seat), the same two words as
  `flow_run`; a head it cannot read is refused in its own name and nothing runs. Tried live:
  one turn with the front door pinned to its own model, delivered in 6.4 s. *(atlas CHANGELOG)*
- **C24. `/run/listen` can stall, and `/chat/stream` keeps writing after the browser has
  gone.** DONE 2026-09-29, both. A capture now ends even when the tab that started it has
  closed, and the chat stream's tokens are written by the one goroutine that owns the socket,
  none of them after the browser has left. Two tests, each red with the old code. *(atlas
  CHANGELOG)*
- **C32. atlas's verifier scripts rewrite their test fixture on any word they do not know.**
  DONE 2026-09-29. It was twenty-four scripts, not eighteen: two of them are not named like
  the rest and were found by reading every script in the folder. All twenty-five (the flow
  script too) now refuse a word they do not know and write nothing. A new test runs each one
  with a nonsense word and checks that no fixture moved; it picks the scripts by what they do,
  not by their names. atlas's proof: 22 held, 14 absent, 0 broke. *(atlas CHANGELOG)*
- **C34. GitHub's tests were red twice and nobody had read them.** DONE 2026-09-29, both. The
  run on the v0.1.16 tag failed on every machine (a test asked about the `main` branch, and a
  tag is checked out without one), and the run on this evening's first push failed on Windows
  (a test of mine compared two spellings of one temp path). Both are fixed and both were
  reproduced here first. The release check passed 17 of 17 beside the first one, because it
  does not read GitHub: that is D9. *(CHANGELOG, GitHub runs 170 and 172)*
- **C20. A dozen small honesty fixes.** DONE 2026-09-29, all of them. A settings file
  (`.env`) that is there and cannot be read now says so at startup; three settings the
  example file offered and nothing read are struck from it; a damaged line in the list of
  proposed memories is kept and counted instead of destroyed; the law check notices a law
  file that was deleted; a session's closing note says where the ground stood whenever it
  moved; a model server that could not be reached is asked again instead of being written
  off; a drift check that did not run has no verdict; a broken spelling dictionary says it is
  broken; reading aloud has a time limit and cleans up after itself; four pieces of dead code
  are gone; the three lists of "pointing" words share one core. The TASKS box is yours to
  tick (F7). *(CHANGELOG, "The small honesty ...")*
- **C16. The workspace file reader cannot read the rest of the ground.** DONE 2026-09-29. Asked
  for a path that names the ground (`ground/pipelines.md`), it reads the file from the ground
  by the ground reader's own rules and says which reader answered. A seat not allowed the
  ground's reader is refused. The TASKS box is yours to tick (F7). *(CHANGELOG)*
- **C19. The live check's greeting case cannot tell a real answer from a recited one.** DONE
  2026-09-29. A reply that lifts a whole sentence (60 characters or more) from what the model
  was handed is now a miss, and the report quotes it. Seen live (sitting 304): the greeting was answered "Good morning." and met. *(CHANGELOG)*
- **D1. The time limits you ruled are not set.** DONE 2026-09-29. The front door's limit is 180
  seconds, no seat may take more than 600 (the judge's was 700), and one turn of the review
  panel may take 900 where every other turn takes 600. I read "the court ... 900" as the
  panel's whole turn, because that is the limit that cut it on 09-28; if you meant the judge's
  own call, say so and it is two numbers. A seat that is cut is now told which setting would
  have given it more time. The panel itself still fails: C13. *(CHANGELOG, "The limits he ruled")*
- **C30. The engine does not say when a model's reply was cut off by a full window.** DONE
  2026-09-29. It reads why the model stopped off the model server and says which limit cut the
  reply: the window full ("the prompt took 8182 of 8192 tokens and left 10 for the answer") or
  the seat's maximum answer length spent. The note is in the transcript, the session log and
  the live check's report. *(CHANGELOG, "A reply the rack cut")*
- **C11. The drift score prints "no usable source".** DONE 2026-09-29. The note says which of
  three things happened: the check was never switched on (nothing was pasted and no tool ran),
  the source was too short, or the embedding model could not be reached. The comments beside
  it say what the code does. Seen in both live runs. The TASKS box is yours to tick (F7).
  *(CHANGELOG)*
- **C15. The file watcher's re-index can run on top of an index build already running.** DONE
  2026-09-29. It takes the same lock the index builds take. If a build is running it does not
  wait: it keeps the changed files for the next turn and says so. The TASKS box is yours to
  tick (F7). *(CHANGELOG)*
- **D10. STATUS.md is not in the search index list.** DONE 2026-09-29. STATUS.md and
  WHATS_LEFT.md are both listed, and a test goes red if any document at the root is left off
  the list. Tried live (sitting 302): the index was refreshed and a search for this page's
  first line found this page first. *(CHANGELOG)*
- **A3. The two tags are not cut.** DONE 2026-09-29 15:27. Core v0.1.16 on `e8aa9b5` and atlas
  v0.1.9 on `b1059a1`, cut and sent from the Version control page on your standing word ("do
  the list top to bottom"). The release check passed 17 of 17 with the tag named, and the
  tag's own release check on GitHub passed. *(CHANGELOG)*
- **A4. GitHub's automatic tests were red on Windows.** DONE 2026-09-29. The test counted
  browsers the instant a page check ended, and counted other runs' browsers too. It counts
  only its own now and gives them 20 seconds to close. Two runs green since, all four legs. It
  was an on-and-off failure, so a red there again is worth a look. *(CHANGELOG, GitHub)*
- **A2. The release check has not passed.** DONE 2026-09-29 15:10. It passed 16 of 16 for
  v0.1.16: suites 3189/3189 and 72/72 on the ground, live check 9 of 9 (sitting 299), and every
  record line. *(STATUS)*
- **C22. SECURITY. The dashboard listens on every network address.** DONE, and already was.
  Measured 2026-09-29: the tool server (8090), the dashboard (8091) and Ollama (11434) all
  listen on 127.0.0.1 only, and the dashboard opens with a PIN since 09-21. The TASKS line was
  stale. *(measured)*
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

A test reads this file the way the page does and fails the suites -- here and on GitHub -- on a
line with no number, a number used twice or under the wrong letter, an open line that already
says DONE with a date, a line that cites a CHANGELOG entry that is not there, or a release
checklist whose version is not the one set (2026-09-30, D15).
