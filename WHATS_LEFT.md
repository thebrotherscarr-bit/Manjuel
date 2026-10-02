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


---

## B. Decisions only you can make

Nothing here gets built until you say which way.

- **B20. Aider on the glass: three things only you can give.** (1) Your yes to download it: the package
  `aider-chat` from PyPI, whose size is not known until it is resolved. (2) Where its environment lives:
  inside the ground (RULE 1), in a folder you name (RULE 8). (3) Which model drives it first: a local
  one, or the hosted route (the key is yours to place). Until you give them, H12 waits. *(your word
  2026-10-02)*
- **B19. Where do plugins live?** A plugin is a folder, and a hand makes no folder (RULE 8). Name the
  place, or say to put them under a folder that exists. Until you do, H9 waits. *(CLAUDE.md RULE 8;
  your word 2026-10-02)*


---

## C. Bugs and problems, known and not fixed

### The models misbehaving


### The engine


### The dashboard and the tool server (atlas)


---

## D. Built but not finished, or not hooked up


---

## E. Never tested for real

- **E1. The wife test.** Someone who is not you sits at the dashboard, asks it to make something
  in her own words, and uses the result with no help. All three pieces are built. The test has
  not been run. *(SPEC 4.8)*

---

## F. Paperwork that is out of date


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
- [x] 7. Publish the atlas drafts on GitHub, v0.1.8 and v0.1.9, or drop them (A5): published 2026-09-30 on your word; v0.1.7 is a draft too, unnamed, still one
- [x] 8. Look at GitHub's tests after the tag: green on both main branches (A4). The core
  tag's own run was red and was not read until later that day; fixed on main (C34)

---

## H. Not built yet: the second brain

Your word, 2026-10-02: "an autonomous second brain with hash chain verification and agentic
workflows, backed by ollama as a first route then secondarily through additional API as added, all
with a modules and plugin system ... a conversational assistant that evolves over time." What the
disk says is missing, in the order it is worth building. H1 is done (below).

- **H2. The assistant does not remember across sittings.** Each sitting starts from the DAYBOOK's
  standing block and its own story. What you said last week reaches a seat only if a seat thinks to
  search for it. Needed: at the start of a turn the engine reads the verified memory and hands the
  seats what bears on the turn, a ruling above a seat's testimony, each marked for what it is. A test
  holds it: a landed ruling shows in the next turn's context, and testimony arrives marked as
  testimony. *(SPEC 1; `manjuel/seatlog.py`)*
- **H3. Nothing notices what is worth remembering.** A seat stages a memory proposal only if it
  chooses to call `remember`. Needed: a bounded pass at the close of a sitting reads what was said and
  done and stages proposals (a correction, a preference, a decision), each citing the run it came
  from. You land or drop them with `/memory`; nothing lands by itself (ESTATE LAW 5 and 6).
  *(`skills/remember.md`)*
- **H4. Nothing consolidates what it remembers.** Memory only grows. Nothing merges two entries that
  say the same thing, marks a ruling as replaced by a later one, or summarises a month. Needed: a
  bounded pass (LAW_003) that proposes consolidations as new entries citing what they replace; nothing
  is deleted (ESTATE LAW 1). *(`law/LAW_003_THE_LOOP.md`)*
- **H5. It cannot change itself where you can check it.** Flows change the estate's own code on your
  click (`coder-tree`), but nothing turns a repeated correction into a proposed change to a seat's
  prompt or a skill, scores it before and after on the live check's cases, and brings it to you with
  the numbers. *(SPEC 4.9; `tests/standup.py`)*
- **H6. Only the law's ledger and now the memory are chained.** The sitting ledger, the flow runs, the
  proof history and the tolls are append-only by custom, not by a chain; and a chain deleted whole
  looks like a chain never begun. Needed: the same seal for each, the tolls first and one at a time,
  and the head of each witnessed outside the ground (a law link, or git) so a deletion is loud.
  *(measured 2026-10-02)*
- **H7. The door's chain checker cannot read the pen's chains.** `verify_chain` calls every entry of
  the law's own chain, and of the memory's, a FLIP (does not hash to its stored value), while
  `law.py verify` calls the law whole. The pen's links carry no `body_v` and the checker assumes the
  other form. Needed: teach it the pen's form, with the law's chain as a golden, so two independent
  walks agree. *(`atlas/tools/chain_verify.py`; CHANGELOG, "The memory has a chain")*
- **H8. A seat has one route: Ollama.** A hosted route exists (B18, 2026-10-02) and only parity uses it.
  The transport a seat uses is still `manjuel/runtime.py`, and the rack, the card monitor, the `.env`
  reader, the `.us` records, the server, the REPL and the boot all name Ollama. Needed before a seat can
  sit on a route: one route interface for seats (chat, list, what is loaded), an ordered route list per
  seat with a fall-back, and the preflight, the card monitor and the rack's report taught that a routed
  seat holds no VRAM. Built on a measured need (SITTING LAW 3) and your word, seat by seat; today a
  seat that names a route is reported by `us.py` and finds no model on the rack. *(the CLAUDE.md RULE 4
  amendment; SPEC 4.6)*
- **H9. There is no module or plugin system.** Seats, skills and flows are files, but a new tool that
  has code must be written into `manjuel/skills.py`, and the word "plugin" is in no code or doc of
  the core. Needed: a plugin is one folder with a manifest (name, version, what it reads and writes,
  whether it reaches out) holding its tools, seats and flows; installed by your landing, which lays a
  chain link pinning its bytes; the loader refuses a plugin whose bytes no longer match; removal
  folds, never deletes. Waits on B19 for the place. *(SPEC 1, "not a general agent framework")*
- **H10. Nothing runs unless you open a sitting or fire a flow.** The engine has no daemon, and a
  search of the tool server finds no scheduler or ticker. Needed: a scheduler in the tool server that
  fires named flows at stated times or on a trigger, each bounded by LAW_003, each outcome a proposal
  you land from the dashboard; the engine stays daemonless. A tool-server change: it needs a restart
  and your card to place the binary. *(BUILDPATH, "the position"; `law/LAW_003_THE_LOOP.md`)*
- **H11. Arrivals are listed, never taken in.** A file you drop in the workspace shows in the next
  sitting's brief and can be inspected and read. Nothing summarises it on arrival, links it to what is
  already remembered, or proposes a memory from it. Needed: an arrival pass that inspects each new
  file (never opening a secret or client file), summarises it, and stages a proposal citing it, which
  you land or drop. No new folder: the workspace is the inbox. *(SPEC 1, "the workspace";
  `manjuel/boot.py`)*
- **H12. Aider as a bounded editor behind the glass.** Your idea (10-02): a page on the glass that drives
  Aider, open source and proven at search-and-replace edits. The ground already has that loop: `ground_edit`
  (an `@@ OLD` / `@@ NEW` edit on a line of work only) and the `coder-tree` flow (a line of work, the
  strokes, the smoke, your Land click). So the question is whether Aider edits better with the models this
  machine has, and that is measured, not argued: the same coding tasks through `coder-tree` and through
  Aider on a scratch clone, auto-commit off, its update checks and analytics off, a local model first,
  scored by the same suites. If it wins, it becomes the flow's `attempt` engine and the page is a thin
  view over a door tool; every gate stays (the line of work, the suites, your click). A page costs a glass
  rebuild and your card to place the binary. Waits on B20. *(SPEC 4.9; `flows/coder-tree.json`)*
- **H13. Claude in the loop.** Your idea (10-02): a reasoning, planning and review agent beside the council.
  Two shapes, and the first needs nothing built: the door already lets an outside agent connect, with reads
  free and every write held for your decision on Version control, so Claude can be in the loop today through
  it (it needs a key minted for that connection). The second is the system calling Claude: the hosted route
  above, used by a counsel seat that reads, advises and never acts. That one waits on H8 and your word, seat
  by seat. *(RUNBOOK, "`--auth` and the service wire"; B18)*

---

## Done

Finished lines, newest first. A number is never used again.

- **B18. Hosted models: your rule says no, your words of 10-02 say yes.** RULED 2026-10-02 in chat ("let's do
  what I said then, set up a second set for parity, why not? I'm not scared of it") and BUILT the same day:
  RULE 4 is amended narrowly in CLAUDE.md (the paragraph stands; an AMENDED section under it says what is now
  allowed), one hosted route exists (`anthropic`, `us/route_anthropic.us`, off until its key is in `.env`),
  and `/parity hosted` is the second parity set, ten cases asked of a hosted head, saying first what would
  leave. No seat sits on it. It was proved on a real server on this machine; NOT yet against the real host,
  which needs your key and your command. *(CHANGELOG, "A second route")*
- **H1. The memory has no chain.** DONE 2026-10-02: every landing now seals itself on a hash chain
  beside memory.md, on the pen the law uses, and `memory.verify` names a changed byte, a cut, or a
  write that did not come through `land`. The memory already there was sealed once as "found", so the
  chain says plainly that nobody vouched for it. The boot and the REPL say the verdict.
  *(CHANGELOG, "The memory has a chain")*
- **D11. The self-test suite is one third done.** DONE 2026-10-02: Part 2 is built, `tests/matrix.py`,
  the phrasing matrix -- each ask said 1,444 ways (case, spacing, politeness, quotes, the other slash, a
  `./../` step, a rooted path in capitals, a secret asked in a question) through the law gate, the
  injection markers and the tool naming, none allowed to come out differently from the canonical
  phrasing. Built, it found five gaps in the first wall and they are closed (the tool layer's jail held
  behind all of them). Part 1 landed 09-03 and Part 3 was true by another road (09-29), so the line is
  whole. *(CHANGELOG, "The phrasing matrix")*
- **D3. The flows `coder` and `version-tag` have been fired and have never finished successfully.**
  RULED 2026-10-02: not a fault, nothing to fix. `coder` was superseded by `coder-tree` (COMPLETE 09-29)
  and stays as history -- every version of every flow is kept (ESTATE LAW 1) -- and the gate reports it
  truthfully as fired and never COMPLETE. `version-tag`'s one real failure was a mark that already
  existed; it finishes the day a real mark is cut through it, which is the next release's own act, and
  the gate keeps naming it ("fired, never COMPLETE") until then. Cut the next marks through it and its
  first COMPLETE closes the report. *(STATUS, flows/runs.jsonl)*
- **D7. The tool server's 85 tools have no permission records.** DONE 2026-10-02:
  `atlas/docs/TOOL_PERMISSIONS.md` is the record, read off the tool table and the shipped role policy by
  the functions that judge a call, and held current by a test (a tool added, a flag turned or a role
  changed fails it until the record is regenerated). Per tool: its tier, writes or reads, its reading
  actions, its secret arguments, whether a call from anything but the glass is held, and what each
  shipped role is told. It does not prove a tool's own claim to read only. *(atlas CHANGELOG, "The
  door's tools have permission records")*
- **D9. The release check does not read GitHub's test result.** DONE 2026-10-02: a new check, `ci`,
  asks GitHub for the newest run of each workflow on HEAD, for core and atlas, and refuses a run
  still going, a missing one, or a red one (naming the legs). Asked at a mark or with `--ci`; no key
  sent; `not here` when GitHub cannot be asked. Seen live: both repositories green.
  *(CHANGELOG, "The release check reads GitHub's verdict")*
- **C7. The model list answer dropped a model.** DONE 2026-10-02, and fixed rather than measured: the
  closing seat paraphrased the rack's listing and dropped the names (3, 0, 11, 8, 4, 0, 0 and 3 of
  eleven on 09-30; none at 09:48 today). When the objective names the listing tool and the closing
  words leave models out, the engine now appends the whole listing as the tool wrote it, and the live
  check holds the turn to the same function. Seen live (sitting 332): the Steward named 3 of 11 and
  the delivery carried all 11. *(CHANGELOG, "A rack answer is whole")*
- **C1. The Router passes whole sentences to file tools as if they were paths.** DONE 2026-10-02,
  on a recount: since 09-21 the refusal appears in one transcript of 416 (09-28 13:41, five times,
  the coder window's own instruction block) and in none of the 272 since 09-29, the coder-tree's
  finished runs included. The law gate refuses the sentence by name and the Router retries; nothing
  reached the disk. Reopen if it recurs in an ordinary turn. *(CHANGELOG, "C1 closed on a recount")*
- **B14. Simplifying the system.** RULED 2026-10-02: keep the Rust, close the line. The first half
  was BUILT 2026-10-01: the chain verdict is `atlas/tools/chain_verify.py` (29 of 29 goldens, 356 of
  356 canon vectors) and `verify_chain` runs it. The fold was not done: the Rust is the engine of
  `atlas-door` (every write is `atlas trade`), ships as `atlas.exe` in every release, and no defect
  was found in it. The rest of the 09-29 proposal (one intent table, fewer seats, a shorter record)
  was a discussion and is not on this list. *(CHANGELOG, "B14 closed: the Rust stays")*
- **F3. DAYBOOK has no entry for 09-10 or 09-11.** DONE 2026-10-01: Sessions 7a (09-10) and 7b
  (09-11) written from the CHANGELOG and the sitting ledger on your word of 09-30, each headed
  "written after the fact"; the other half, Session 8's "next session" line, was done 09-30. The
  line stayed open on this page until 09:35; moved now. *(DAYBOOK; the save `05274c2`)*
- **B16. A merge button on Version control (was D6).** RULED 2026-09-30 and BUILT 2026-10-01: a
  "Land onto main" button in the Lines-of-work box, behind a `land` action on the tool server --
  fast-forward only, from the main line, over saved work; everything else refused by name.
  *(atlas CHANGELOG, "`land`")*
- **B13. SEAT_LOG numbering.** RULED 2026-09-30 and BUILT 2026-10-01: SEAT_LOG_INDEX.md lists
  every toll in the order it was paid, with the gaps (53) and the duplicates (5) counted; the log
  itself is untouched. Refreshed at every toll since 2026-10-02 (`seatlog.pay`; `python
  tests/seatindex.py` runs it by hand) and held by a test.
  *(CHANGELOG, "The toll index")*
- **C13. The review panel does not fit its time limit.** DONE 2026-09-30, measured: with Jesster
  capped (B15) and the front door off the panel (B7), the court ran 561 seconds of its 900 --
  Jesster 207, the judge 317 and ruled inside the turn. 1 of 1, the first since 09-18.
  *(logs/standup_2026-09-30_155756.md)*
- **B15. The review panel's two thinking seats have no limit.** RULED and BUILT 2026-09-30:
  Jesster capped at 4,500 tokens, the measured middle of its finished answers; the judge as it
  was. *(CHANGELOG, "His rulings of the afternoon, built")*
- **B10. The Router's prompt says "the objective names the skill X".** RULED and BUILT
  2026-09-30: the prompt now says who chose the tool. *(CHANGELOG, "His rulings of the
  afternoon, built")*
- **B8. The `.env` reader keeps a comment after a value.** RULED and BUILT 2026-09-30: a trailing
  ` #` comment is dropped. *(CHANGELOG, "His rulings of the afternoon, built")*
- **B7. Should the front door speak at the review panel?** RULED 2026-09-30: no; the court is the
  three counsel and the judge. *(CHANGELOG, "His rulings of the afternoon, built")*
- **B6. Should the rack report tool be allowed at the review panel?** RULED 2026-09-30: no; it
  was never on the list and a test keeps it off. *(CHANGELOG, "His rulings of the afternoon,
  built")*
- **B4. Laws with nothing enforcing them.** RULED and BUILT 2026-09-30: every tool that reads or
  writes a path refuses `worlds/` and any `vault/` by name; LAWS 3 and 4 stay principles.
  *(CHANGELOG, "His rulings of the afternoon, built"; SPEC 4.4)*
- **B1. The coding model.** RULED 2026-09-30: the coding seat moves to qwen2.5-coder:14b; the
  coder flow is the measure. *(CHANGELOG, "His rulings of the afternoon, built")*
- **F6. TASKS.md has boxes that are half done and still open.** DONE 2026-09-30: every half
  ruled or built today (B12, B7, B5, B3) and the boxes ticked on your word. *(TASKS)*
- **A5. The atlas releases on GitHub are drafts.** DONE 2026-09-30: v0.1.8 and v0.1.9 published
  through your signed-in gh on your word. v0.1.7 is a draft too and was not named; it stays one
  until you say. *(CHANGELOG, "His rulings of the afternoon")*
- **B17. What DONE means for the coder changing the system's own files.** RULED 2026-09-30:
  confirmed as proposed; SPEC 4.9's line says so. Run six was the first of the two it asks for.
  *(SPEC 4.9)*
- **B12. The two sitting laws (5 and 6).** RULED 2026-09-30: ticked, entered in the law ledger
  on 09-21. *(TASKS)*
- **B11. The hardening work has no version number.** RULED 2026-09-30: v0.1.11 carries it, said
  under its heading. *(CHANGELOG, v0.1.11)*
- **B9. RULE 9's wording is out of date.** RULED 2026-09-30: the sentence now names the roots in
  index_roots.txt. *(CLAUDE.md)*
- **B5. The client-name scrub.** RULED 2026-09-30: SPEC 4.5's line is MET; `pre-strip-master`
  kept, never pushed. *(SPEC 4.5)*
- **B3. Line endings.** RULED 2026-09-30: the rule follows the disk -- root documents CRLF, code
  LF, nothing mixed -- and a test holds it. *(CLAUDE.md; CHANGELOG, "His rulings of the
  afternoon")*
- **B2. The front-door model.** RULED 2026-09-30: llama3.2 stays, with the guards on. *(SPEC 4.7)*
- **F7. TASKS.md boxes for work finished on 2026-09-29 are still unticked.** DONE 2026-09-30:
  ticked on your word, each with its date and entry. *(TASKS)*
- **C8. A model can say it used a tool when it did not.** DONE 2026-09-30, as far as a claim
  names a file: the check that refuses "I saved it as poem.txt" when nothing was saved now reads
  "edited", "updated", "modified", "changed" too -- the 09-28 shape. A claim that names no file
  is still speech (1 in 251 answers since 09-21). *(CHANGELOG, "An edit is a write")*
- **C6. The closing step once read its own instruction back as the answer.** DONE 2026-09-30.
  An answer that repeats a whole sentence of the seat's own instructions is thrown out and
  named, the way one that repeats the law block is. *(CHANGELOG, "Three lines on his word to
  finish")*
- **C33. At the review panel, two seats did another seat's job.** DONE 2026-09-30. A counsel
  seat that writes the ruling's heading is now named in the record (its words stand as
  counsel); the Router's half was already stamped. *(CHANGELOG, "Three lines on his word to
  finish")*
- **D2. The "make me a game" test, run as a flow, makes nothing.** DONE 2026-09-30. The cause
  was the words: the maker knew "make me a game" and not her "try making me a little game" or
  "i want a game i can play" (the test's own recorded messages), so her turns went to the
  ordinary pipeline and talked. The maker reads those forms now. Fired live from the dashboard:
  the flow completed in 52 seconds and made two playable pages, `projects/game` and
  `projects/game-2`. Her second message made a second game rather than changing the first;
  on your word to finish, "i want it ..." / "i dont want it ..." now change the thing in hand.
  *(CHANGELOG, "The maker reads her own words"; "Three lines on his word to finish")*
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
| coding model | the Expert Coder seat (qwen2.5-coder:14b) |
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
