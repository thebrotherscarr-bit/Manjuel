# What this estate refuses

Every refusal below is **arithmetic** — Python that runs before, or entirely
without, any model's judgement. None of them is a prompt asking a model to
behave. That distinction is the whole design: a prompt is a request, and a
request can be talked out of.

Each entry names the sitting that earned it. Nothing here was designed in
advance of a failure; every one of them exists because the estate did the
wrong thing once, in the record, and the record is in `logs/`.

Verify any of it yourself:

    python tests/test_manjuel.py     the strokes; every gate proven BOTH ways
    python law/law.py verify          the ledger; refuses a lying byte
    python tests/refusals.py --check  the tail of this file: every `Refused:` site
                                      in the code, listed off the code (2026-09-30)

---

## 1. Noise never wakes a seat

**Trigger.** The objective does not parse as language: mostly digits, no
word-like tokens, or fewer than half its tokens word-shaped.

**Action.** No seat is woken, no skill runs. The reply asks for a repeat.

**Why.** Sitting 22: keyboard mash raised `technical`, woke the Expert Coder,
and produced four stages of invented work about a request that meant nothing.
Seats improvise on noise, so noise is stopped before any seat sees it.

**Deliberately lenient:** one real word passes, and typos pass, because a typo
is still language.

---

## 2. Pasted material is refused before the Guardian reads it

**Trigger.** Injection markers in a `/paste` feed — instructions to ignore
prior instructions, attempts to re-instruct Manjuel, reaches for `.env` or
credentials, fishing for system prompts.

**Action.** The run is refused outright. **No seat reads the material**, and
the markers are named in the record.

**Why.** Sitting 39: an injection test feed sailed past the *model* Guardian
and moved Manjuel's hands — a skill ran, and 76 characters were spoken
aloud. A model gate rolls dice; this one does not. The Guardian model still
sits behind it for everything softer.

---

## 3. A seat may call only what it is cleared for

**Trigger.** A seat emits a tool call outside its `May Call:` line in
`agents/*.md`. **A seat with no such line may call nothing.**

**Action.** Refused at dispatch. Grant is by omission — an uncleared tool is
never even offered to the model.

**Why.** Before it existed, any seat could call anything. Counsel is *eyes,
never hands* (the operator's ruling, sitting 39), and that has to be enforced
rather than requested.

---

## 4. One write-path per Manjuel (LAW 8)

**Trigger.** A skill handler resolves a caller-supplied path. Every handler
that does so must declare it (`**Path Args:**`), and the gate checks the
declared argument at the single chokepoint in `SkillLibrary.execute()`.

**Action.** A path resolving outside its jail is refused, and the record says
`LAW 8 gate refused <skill>`.

**Why.** Five of twenty-six handlers were jailing their own paths privately,
and nothing could distinguish "this skill takes no path" from "this skill
forgot to jail one". A stroke reads `skills.py`'s own source and goes red if a
handler resolves a path without declaring it — because argument *names* lie:
`remember`'s `<filepath>` is a title, `rack_load`'s is a model tag.

---

## 5. Client data is sealed

**Trigger.** Any **one** of three tags on a file:

    a `vault/` path part          ·  a `.client.` in the name
    a `[[CLIENT]]` token in the first 2KB

**Action.** Refused by the indexer, the ground watcher, every reader
(`ground_read`, `read_file`) and every listing. A directory listing shows
`vault/ (N protected items — contents never listed)` — the count, never the
names.

**Why.** The operator's ruling, sitting 45: client data is of the highest
priority, never indexed, never used, never cross-referenced.

**Proven live, not merely asserted.** Sitting 61 ran a real semantic search
for a client's name against 3,601 chunks: five passages came back, **none from
the sealed world**, no vault path, no filename, no fragment. `index_roots.txt`
is the first line of that defence (the world is named in no root); the shield
is the second.

---

## 6. Keys are silent (LAW 9)

**Trigger.** A file named as a secret — `.env` and anything starting with it,
`secrets`, `credentials`, `id_rsa`, `apikey`, `token`, `*_secrets`, `*_key`,
and their kin — **by name, whatever the extension.**

**Action.** Never embedded, never indexed, never printed, never passed on a
command line where `ps` could read it.

**Why.** `.env` was being skipped by luck (no file extension), while `.yaml`,
`.ini` and `.cfg` *are* indexed — so a secrets file with one of those names
would have been embedded, and **an embedding cannot be unpublished.**

---

## 7. A claim about a file needs a read behind it

**Trigger.** A seat's output presents a named file's contents, and no reading
skill ran this turn.

**Action.** The claim is refused rather than delivered, and the fault is named
in the record.

**Why.** Sitting 56: "Can you read me the poem?" — one stage, no tools — and
the seat composed a new poem under the heading "Here is the content of
`poem_about_jesster.md`". The file existed and said something else. The
operator caught it, which is exactly the part that must not be the mechanism.

**Honest limits, stated in the code, not discovered later:** it catches a
claim that *names a file*; invention citing nothing passes. It proves a claim
**unsupported**, never false — which is enough, because LAW 5 says testimony
is not fact, and an unsupported claim of fact is what must not reach the
operator.

---

## 7b. A claim to have WRITTEN a file needs a writer behind it

**Trigger.** A seat says a file was saved, written, created or committed,
and no writing skill ran this turn.

**Action.** The claim is refused rather than delivered, and named in the
record.

**Why.** Sitting 70's closer: *"Yesterday, I compiled a poem about autumn,
saved it as 'poem.txt' in the Research folder, and successfully read it
back to you."* No yesterday, no file, no earlier reading — the one true
clause was that `speak` had run. The claim-check could not see it (that
wants a *contents* claim), nor the citation-check (that wants a search
result). Same arithmetic, new place: the turn's tool calls say whether any
writer ran.

**Same honest limits as §7:** it wants a NAMED file, so invention citing
nothing still passes, and it proves a claim **unsupported**, never false.

## 8. A cited search result must be a search result

**Trigger.** A seat's prose cites a path with a score, and this turn's search
returned no such result.

**Action.** The prose is withheld; the tool's own results stand alone.

**Why.** Sitting 61: the Router lifted a filename out of one result's *snippet*
and reported it as the top hit, carrying a *different* result's cosine — then
built a whole relationship between two unrelated things on that misread, and
the closer delivered it. Unlike uncited invention, this has ground truth: the
tool output is the exhaustive list of what exists this turn. Arithmetic.

---

## 9. The same call does not run twice

**Trigger.** A seat emits an identical `(skill, arguments)` twice in one turn.

**Action.** Not re-run. Told once that it already ran; if it repeats after
being told, the loop breaks — it is spinning.

**Why.** Sitting 63: one "remember the operator rules" request staged the same
rule three times, because the follow-up asked whether another skill was needed
and the Router answered by repeating itself. The step cap had been doing a
rule's job. This covers every skill — a doubled write or a doubled commit dies
here too.

---

## 10. Testimony is separated from fact at the line where they meet

**Trigger.** A seat writes prose after a tool result.

**Action.** The record splits them with a named boundary:
`--- <Seat> reading the above (testimony, not tool output) ---`.

**Why.** Sitting 63: a `memory.md` read came back with the file's headings
demoted to h5, and the Router's own summary above it demoted to h5 as well. In
the record the two were indistinguishable — a paraphrase read as file content.
Facts first, opinion after, and the record says which is which.

---

## 11b. A failure cannot be left out of the answer

**Trigger.** Any tool failed or was refused during a run.

**Action.** The delivery carries the list — what failed and why — appended
from what was recorded *as it happened*, whatever the closing seat wrote.

**Why.** Twice in two sittings a seat's prose contradicted its own record
without inventing anything: the Quartermaster read `15.0GB of ~15.0GB, ~0.0
headroom` and called the card "comfortable and functioning optimally"; the
closer delivered "no new issues or concerns" over a run holding a
326-second timeout under a THIS TOOL FAILED banner. **Omission, not
invention** — which is why the claim-check (nothing cited) and the
citation-check (no result quoted) both let it through.

The recompose is arithmetic and **not another seat**: a model summarising a
record and dropping the failures is the disease, so a second model
summarising would be more of it. It makes no judgement about the seat's
words and does not read them for all-clear language. The facts travel with
the answer every time, and a seat that reported them honestly is simply
corroborated.

## 11. A failed tool cannot be reported as a success

**Trigger.** A skill returns an error, refusal, or "cannot".

**Action.** The result is wrapped: `THIS TOOL FAILED — NOTHING WAS DONE. Do
not report success, contents, or findings from it.`

**Why.** Sitting 40: an errored read was narrated as "successfully opened" and
the file's contents were invented on top of the failure.

---

## 12. Manjuel never lands anything (LAW 6 / RULE 6)

**Trigger.** Any act that commits the operator: a git commit or push, a memory
entry, a spend.

**Action.** Prepared, staged, and handed over. **Never landed.** Memory
proposals are stamped `GENERATED` in `memory/pending.jsonl` and reach
`memory.md` only when the operator lands them with `/memory`. Remote git
(pull/push) is refused unless `MANJUEL_GIT_REMOTE=1` — a push cannot be
recalled once fetched, so it is the operator's act, not a seat's. Model
downloads (`rack_pull`) are off behind their own switch: they cross the
network and can move gigabytes onto the machine.

---

## 13. The ground is `Desktop\Research`, and nothing reaches outside it

**Trigger.** Any read, write, index root, or runtime dependency resolving
outside the ground.

**Action.** Refused. A stroke fails if any index root escapes Research, and
the workspace jail collapses traversal attempts.

**Why.** The operator's standing rule, written after this was broken: checking
counts as reaching, and a yes covers one act, once — never the next file,
never the next session. Full text in `CLAUDE.md`.

---

## 14. Everything is bounded

    tool loop        5 hops, and an identical call is not one of them
    review -> repeat ONE pass back through the tools when a review finds
                     the work unfinished; the second request is refused and
                     the gap is named to the operator instead
    skill execution  SKILL_TIMEOUT bounds the WAIT (not the work — stated
                     plainly in the code rather than hidden)
    speech           capped, and says so when it truncates
    seat output      Max Tokens per seat, declared in agents/*.md
    VRAM             a budget with headroom, foreign models never evicted

LAW 7: bounded everything. An unbounded thing on a single machine is an
outage waiting for a bad afternoon.

---

## 15. Code the coder emits is PARSED before it is written

**Trigger.** The Expert Coder declares a file. Before it lands, `ast.parse`
runs on it and the tree is walked.

**Action.** Refused, by proof and not by prompt, when the code: does not
parse (the syntax error and its line are named); imports `requests`,
`urllib`, `socket` or `http`; imports `importlib`; or calls `eval`, `exec`,
`__import__`, or anything with `shell=True`.

**Why.** RULE 4 says the estate is local. Until 2026-09-03 that was a
REQUEST — a line in CLAUDE.md obeyed by whichever model sat on the coder's
seat. `ast` makes it arithmetic. And a file that did not parse used to land
anyway, after which the Quality Evaluator reviewed it as prose, because it
reads what is on disk and cannot tell the difference.

**IT FAILS OPEN, DELIBERATELY.** A non-Python emission is NOT refused — it
lands with `landed UNINSPECTED -- not checked: x.md is not Python` in the
record. A gate that silently passes what it cannot read spends your trust
on a check that did not happen.

**Three honest limits, in the docstring rather than discovered later:**
`shell=True` is flagged on ANY call, not only subprocess's (over-refusing on
a write gate is recoverable; under-refusing is not). A module reached by
getattr, a `__builtins__` lookup, or an import spelled through a variable is
still uncaught — NARROWED, NOT SEALED. And it proves what the SOURCE says,
never what the code does when run; nothing here executes the file.

---

## 16. A large eviction from the index is refused

**Trigger.** A refresh finds documents under a root that `index_roots.txt`
no longer declares, and they are more than 25% of the corpus.

**Action.** Nothing is evicted. The count, the share, and the remedy are
reported: check `index_roots.txt`; run `index_ground rebuild` if it is right.

**Why.** Sitting 78: `worlds/manjuel` was removed from the roots and 91 of
801 documents from that world stayed in the index and kept answering,
because `prune()` asked only whether the FILE was gone and every file still
existed. Teaching it to ask about scope made a refresh destructive in a way
it had never been — a typo in a config file would silently empty a root on
the next run. So the guard performs the small correction and refuses the
large one. A bound is not a rule; this is the rule, and the bound is on the
mistake.

---

## 17. The manifest is checked against the code

**Trigger.** `python -m manjuel.us`.

**Action.** Every `us/*.us` record is compared to the thing it names:
declared-vs-present both ways for skills and seats, `wall` present, `writes`
against WRITING_SKILLS, `remote` against the gated set, `model` against the
seat, `source` exists, `may_call` against May Call, `permission.edit`
against write clearance, and `can_approve` FALSE EVERYWHERE. It REPORTS and
exits 0 — the manifest describes a ground the operator edits by hand, so an
assertion over it would go red because he added a skill.

**Why.** The manifest declared what every skill may reach and NOTHING
CHECKED IT. Twenty of thirty-five skills had no record at all; ten of eleven
seat records named a model the seat had not run in weeks; and the Router
declared `read: agent_workspace only` while cleared for `May Call: all`,
which includes every ground reader. A declaration nobody checks is a
promise, and LAW 5 applies to the manifest exactly as it applies to a seat.

**A check that cannot run says so.** With no rack reachable, the model-tag
comparison reports "not checked" rather than passing. A reconciler finding
nothing looks identical to a clean ground, and telling those apart is the
whole value.

## 18. A door's tool call is carried, never printed — and only the Router holds tools

**Sitting 84, 2026-09-04.** The first run on llama3.2 at the front door.
"review the changelog" raised no flag, the Router was skipped, and the
Steward delivered `<action>ground_read</action><filepath>rack.md</filepath>`
as its whole answer. The Steward has a May Call list; llama3.2 supports
native tools; the engine had handed it schemas; it called one, as a
tool-trained model does; the runtime rendered the call as the estate's
action block; and only the route stage executes action blocks. The ask
went nowhere and the markup went to the operator. phi4-mini had hidden the
hole for three days by mostly obeying "never answer with tool names".

**Two things, by the operator's ruling (option B: one executor):**

- A seat that is not the Router is **not handed tool schemas**, whatever
  its model supports and whatever its May Call says. Tools go to the seat
  that runs them.
- A non-Router seat that answers in markup anyway is **asking for a tool**:
  `needs_tool` rises, the skill it named becomes the Router's named tool,
  the arguments it gave are the floor under the Router's call, and the
  markup is stripped. The Router applies its own clearance — a door naming
  a skill the table may not call gets a refusal from the seat that holds
  the gate, not a silent run. A markup ask for something that is not a
  skill is dropped and named in the record.

`strip_control` now strips an action block from anything a person reads,
but ONLY when an `<action>` is present: the Expert Coder's bare
`<filepath>` declaration, which `land_code` reads after the strip, is
untouched. Stroked both ways and the schema half directly:
`test_a_door_that_calls_a_tool_hands_it_to_the_router`.

**What this is not.** It does not make the door a second executor (option
A, declined). One seat acts; the rest ask.

## 19. THE LAW GATE — every run passes through the law before any seat sits

**The operator's ruling, 2026-09-04:** "EVERY single call, no matter what,
runs THROUGH the law." The same rule he wrote for the hands that morning
(CLAUDE.md RULE 0), applied to the seats. Built the same day: `manjuel/lawgate.py`,
called first thing in `run_pipeline`, after the gibberish gate and before
intent decides anything.

**What it does, in order, on every run:**

1. **Walks the chain.** `law/chain.jsonl` is verified with the pen -- the
   same three walks `law.py verify` makes -- and every sealed law's
   fingerprint is checked against the file on disk. A law that does not
   verify refuses **every** run: "no seat sits on a law that cannot be
   trusted (LAW 4: a red blocks the road)." A ground with no ledger at all
   (a bare clone, a test workspace) is not a broken Manjuel; the gate says so
   in the record and runs on the rules alone.
2. **Checks the objective** against what a regex can decide: a reach
   outside the ground (`..`, a drive letter, `~`, `/home` -- RULE 1 / LAW
   8; the ground's own path is not a reach), a reach for a secret by name
   with a verb that would surface it (LAW 9), a reach across the wall while
   remote operations are off (`git push`, `ollama pull`, `pip install`,
   `curl` -- LAW 6 / RULE 4), and client material named by tag
   (`vault/`, `.client.` -- SITTING LAW 2). A hit refuses the run with the
   law named. No seat read it.
3. **Hands every seat the law as fact** -- a `## The law` block, the
   Manjuel verified, at which head, and which checks this request passed.
   Appended to the user prompt until 2026-09-07; in the SYSTEM role since
   (§20), where a small model does not recite it as content. A seat cannot
   claim it was not told; a reader of the transcript can see it was.
4. **Stamps the record**: `law: chain whole (4 links, head ...); objective
   passed 4 checks`, or the refusal, one note per run, machine-emitted.

**What it is not.** It decides what a regex can decide and nothing softer;
the Guardian, the claim-check, the citation-check and the recompose stand
behind it. It proves the laws are unchanged since sealing; it cannot prove
a seat obeyed them. It reads the objective; pasted material has its own
gate (§2). Stroked: `test_the_law_gate` -- a tampered law refuses every
run and no seat sits; each of the four checks fires on its shape and not
on a plain question; the operator's own path and a local commit pass;
every seat that sat saw the block; the record carries the stamp; a
ledger-less ground passes on the rules and says so.

---

## 20. THE CLAUDE.md SYSTEM, and THE RULING LOOP — what a seat is handed beside its prompt, and how long it may think

**The operator, 2026-09-07:** "make sure we are looking at how the
claude.md works and implementing that system into Manjuel", and, on
Manjuel: "expanding his context and letting him give some room for
thinking, but limit his turns ... kind of like the router is limited."

**The law in the SYSTEM role** (`pipeline.carried_blocks`, `_seat_for_call`).
§19's `## The law` block used to be appended to the USER prompt. Sittings
86 and 87 showed four seats reciting it back as content -- a small model
copies what sits beside the material. CLAUDE.md reaches the hand as
system text, never inside the operator's message; the seats get the same
shape now: the block rides beside the seat's own system prompt
(`dataclasses.replace` for this call; the registry's declaration is never
written). A BAKED seat has no system role and keeps the old shape. The
record keeps what rode in the system role (StepResult.prompt), so the
prompts companion still shows the seat was told.

**The ten, verbatim, for the court** (`lawgate.laws_text`, `Verdict.block(full=)`).
The hand reads 3KB of law every turn (RULE 0); a seat that RULES on the
record was reading sixty words about it. The court seats -- the ones the
advisory builder serves -- are handed the ten estate laws as sealed, read
from `law/ESTATE_LAWS.md` and never re-typed in code, labelled "not
material, not counsel, never quoted as either". The door, the Router and
the Guardian keep the short form; cost matters there.

**The standing** (`seatlog.standing_block`, `RunContext.standing`). CLAUDE.md
READ FIRST: "you begin with total amnesia; DAYBOOK's last entry is the
only file that carries intent." Every seat began with amnesia too, and
sitting 87's toll said so. The last DAYBOOK entry's **Standing**, **The
plan** and **Next session** lines, bounded to 1,800 characters, labelled
as record, built ONCE at sitting open and handed to the Steward and the
court on every run. Not the Router (budget; it routes). Read, never
generated: no DAYBOOK, no block.

**The partial-read stamp** (`pipeline.note_partial_read`, `unread_parts`,
`recompose`) -- SITTING LAW 1 for the seats. `windowed()` already said
"THIS IS NOT THE WHOLE FILE" in capitals; nothing carried it past the
seat. Now every read that returns a numbered window, a section, one
definition or the map is recorded as it happens, and the delivery ends
with READ IN PART, NOT WHOLE and the files named -- unless every numbered
part of the file was read this run, in which case it was read whole and
is not listed. Sitting 87 run 7: an answer from 12,000 of DESIGN.md's
63,000 characters, unmarked. Arithmetic over the tool's own first line.

**The ruling loop** (`pipeline._press_for_ruling`, `MAX_RULING_TURNS = 3`,
`runtime.chat(think=)`). Manjuel on gemma4:12b thought for 13–15k
characters twice and ruled on nothing; the court's delivery was the
salvage line. A seat that comes back with the salvage line is now asked
again -- the same prompt, its own deliberation appended as ITS OWN WORDS
(never as material), "RULE NOW", and Ollama's thinking switch OFF for the
retry -- up to three sittings in all. Then what it has stands and the
record says the turns were spent. The Router is never pressed: its loop is
the tool loop (§9). A runtime that cannot switch thinking off still gets
the bounded retry. Manjuel's window is 16384 (agents/manjuel.md).

**What it is not.** Moving the law to the system role is the first layer
against the recital; a guard that REFUSES a delivery reciting it is not
built, on purpose, until the next sittings are measured. The standing does
not refresh mid-sitting (RULE 9's shape: nothing moves under his hands).
The loop bounds turns, not seconds: three turns of a two-minute seat is
six minutes, and the cap is the operator's to raise or lower. Stroked:
`test_the_claude_md_system_and_the_ruling_loop` (48), `test_the_law_gate`
(prompt clean, soul told).

---

## 21. THE BOUNDS OF 2026-09-08 — a seat, a turn, one index build, and the tag

The operator, the same morning: "150 for steward 300 for the router 600
max for the whole system. there should never be more than 10 minutes
between a response, thats absurd." Every refusal here is arithmetic on a
clock or a lock; no model is asked.

- **A seat call past its bound is cut** (`runtime.SeatTimeout`). The
  bound is the seat's own `Timeout:` (agents/*.md, by model size: 150 /
  300 / 600, and the door's 180 by name -- ruled again 2026-09-28: "180
  for steward. 300 to route and 600 max per seat other than the court
  which requires a max of 900") or, for a seat that declares none, the
  ceiling `SEAT_TIMEOUT` = 600 (`MANJUEL_SEAT_TIMEOUT`). The refusal names
  the dial that would move THAT seat -- its own, the ceiling, or the
  turn's when the bound was what the turn had left. Two halves: httpx's read
  timeout for a call that answers nothing (connect held at 10s), and a
  wall clock on the stream that CLOSES it for a call that never stops --
  Ollama stops generating. One named refusal; `on-fail: skip` goes on
  without the seat. Earned: sitting 92, Jesster 760s then a 500.
- **A seat whose turn comes after the turn's deadline is not seated**
  (`pipeline.TURN_DEADLINE` = 600, `MANJUEL_TURN_DEADLINE`; or the
  pipeline's own `**Deadline:**` in pipelines.md, carried on the steps the
  book hands out -- the court's 900, 2026-09-29). Named in
  the record and in the delivery under OUT OF TIME (the recompose's third
  block, beside NOT EVERYTHING RAN and READ IN PART); a seat seated just
  before the line is cut to the seconds left (`_within_deadline`); a
  sub-run inherits its parent's clock; a run where nobody sat still
  delivers the block, from the Gate. Earned: sitting 95, `time align the
  logs`, 1858s with no seat past its bound.
- **A second index build while one runs is refused by name**
  (`skills._INDEX_BUSY`, held for the life of the build, refusal or not;
  `index_ground` and `embed_text` share it, and since 2026-09-29 the
  watcher's re-index at the turn boundary takes it or hands what changed
  back for the next turn -- it never waits). **A rebuild that cannot
  discard the old file is refused**, not pretended (`_open_index`).
  Earned: sitting 94, two builds on one vectors.db, `UNIQUE constraint
  failed: docs.path`, and a seat log that said "finished".
- **The tag is refused by name** (`tests/release.py --check`): suites
  green and after the newest edit, buildmap, the standup live, the law,
  the manifest, SPEC-vs-CHANGELOG, DAYBOOK closed, HANDOFF today, the
  hands ledger closed. Reads only. RUNBOOK "Before a tag".
- Smaller, the same day (the REPL read): Manjuel's own writes
  (`sessions/`, SEAT_LOG.md, memory.md, rack.md, the suites' stamps) no
  longer queue a re-embed every turn (`watch._SELF_WRITTEN`); a palette
  command whose Runs: is a command is refused before it re-enters the
  loop; `/chat` ends after three failed listens; a paid sitting is not
  closed twice; an exception nothing caught still closes the sitting;
  `git_pull`/`git_push` are writers for the write-claim check; one git
  read at open.

- **Seats that failed reach the delivery** (the recompose's fourth block,
  SEATS THAT FAILED, from StepResult.error) -- sitting 96's court said
  OUT OF TIME for Manjuel and nothing of Jesster's 577s.
- **A refused feed is withheld from the transcript** (`transcript.write`):
  the delivery is the refusal; the source is described, never copied.
  Earned: the injection case's payload in logs/, an index root.
- **An unknown skill name is answered by the Gate** with the nearest real
  names; no seat sits (`_unknown_skill_word`). Earned: sitting 95,
  `index_workspace rebuild`, the door answering the previous question.
- **`<keyword> <words>` is decided** for a reading or prompt skill --
  the words are the argument; a Takes: match decides too; a writer is
  never decided from words (`decided_call`, `named_by = "the words"`).
- **A prompt skill with only the order as payload is refused** before
  the model is called (`_run_prompt_skill`): "time align the logs" is a
  request for material, not material.
- **The brief's numbers are checked** against the facts the door was
  handed (`cli._unsourced`); the invented ones are named beneath.
- **The standup judges seats** (`tests/standup.py`): failed stages, OUT
  OF TIME, the seats a case names, the judge's last word, and THE NUMBER
  CHECK -- a number in the delivery from no tool result is a miss.
  (2026-09-14: and an error the ENGINE wrote counts as a source. A seat cut
  at its bound is quoted into the delivery under SEATS THAT FAILED, and that
  morning's court was faulted for the 92 and the 500 inside the bound's own
  message. A seat's numbers are judged exactly as before. Stroked:
  `test_the_engines_own_words_are_a_source`.)
- **The ruling loop is twelve** (`MAX_RULING_TURNS`, his number); the
  turn's clock is what keeps twelve honest.

Stroked: `test_the_seat_bound`, `test_the_turn_deadline`,
`test_the_loops_of_2026_09_08`, `test_the_release_gate`,
`test_the_p0_of_the_review`.

---

## 22. THE STORY AND THE HANDS (0.1.6, 2026-09-08) — what a seat is told about THIS sitting, and what a hand writes down about itself

- **The door and the court are handed THE SITTING STORY** -- every run of
  this sitting so far, read off the ledger line the engine wrote as each
  run ended (objective, seconds, tools, guards, seats that failed or ran
  out of time, the first line delivered), newest last, bounded at 1800
  characters; the oldest fold into a counted line that points at logs/
  and the index. Not the Router. Earned: sitting 93, "what happened? why
  did you suck so bad?" -> a search over the whole record -> "the
  operator doesn't have access to see previous outputs in this session."
- **A question about this sitting keeps the door** (`intent.asks_the_
  sitting`): a reader dispatch guessed from the words is withdrawn; a
  tool the operator named is still his order; with no story yet (the
  first run) nothing changes.
  the fingerprints of the rules as read, HEAD, the DAYBOOK entry and
  HANDOFF block read, the newest sitting seen; closed with HEAD, the
  files edited, the strokes, restart required or not. The brief prints
  the last hand; an OPEN hand is flagged; the release gate refuses a tag
  over an unclosed hand. Earned: 2026-09-08, a hand that ran `git
  status` before reading CLAUDE.md and left the lock the file warns of,
  and a record that held what the hand believed, never what it read.
- **A kind is one word** (`cli._ask_kind`); **`rack rebuild` has a door**
  (rack_sync's Says:); **a short question about the seat itself is
  conversation** (`asks_the_ground`: four words or fewer, addressed to
  "you"); **the Router is told it cannot write memory** (agents/router.md).

Stroked: `test_the_story_and_the_hands`.

---

## What this does NOT protect against

Stated plainly, because a security page that only lists wins is marketing.

- **Invention that cites nothing.** A seat can still state something false in
  ordinary prose with no file named and no result cited. Sitting 60 produced a
  confident paragraph about a real client's work, sourced from nowhere. The
  answer to that class is *dispatch* — a question about the ground now reaches
  a reader, so the void that invention fills is smaller — but the class is not
  closed and may not be closeable by arithmetic alone.
- **A model's judgement, where judgement is the job.** The Guardian, the
  Evaluator and the Router make calls a gate cannot make for them.
- **A PARTIAL read spoken as a whole one.** `windowed()` hands a big file
  over as "part 1 of 7 — THIS IS NOT THE WHOLE FILE" in capitals, with a map
  of the headings it did not show. The claim-check then asks only whether A
  READ RAN this turn — part 1 ran, so it passes, and a seat that saw 9% can
  speak about 100%. Named 2026-09-03 after an agent did exactly this to
  `parity.py` and was wrong twice in one turn. BUILT 2026-09-07 as the
  partial-read stamp (§20): the delivery now SAYS the read was partial.
  What is still not caught is the harder half -- a claim about what a read
  SAID with nothing tying it to the read (TASKS, Layer 7).
- **The operator.** Nothing here binds him, and it is not trying to. He is the
  one who lands, and the estate's honesty exists so that what he lands is
  informed.

---

## 23. An edit names one passage, and a run is not a shell

**Trigger.** `edit_file` is given an anchor that appears twice, or none, or an
edit that would leave a `.py` unparseable, or one that would leave it carrying
what the write door refuses (§24: a network import, `eval`/`exec`/`__import__`,
`importlib`, `shell=True` — since 2026-09-28, judged on the whole file as it
would stand), or a file whose line endings are already MIXED. `run_python` is
given something that is not a `.py`, or a file that is not there, or a script
that will not finish.

**Action.** Refused, and NOTHING IS WRITTEN — each refusal is checked by
reading the file back. The anchor refusal says HOW MANY times it matched, which
is the whole cure. A runaway child is killed at `MANJUEL_RUN_TIMEOUT` (60s) and
what it had already said is still reported.

**Why.** The coder emitted whole files, so at 8192 context a large file could
not be touched at all. An edit takes a fragment instead, and then the anchor
carries the weight the file used to: a fragment says WHAT but not WHERE. An
edit that picks among three matches is a write nobody authorised.

`run_python` exists because the only machine verdict in the coding circuit was
"does it parse", and a loop cannot steer on *compiles*. It is one interpreter
and one jailed path — **never a command from a model.** `inspect_code` already
refuses `shell=True` in code the coder lands (§15); a skill that offered a
shell would be the engine doing what it forbids its own seats.

And the child is handed an ALLOWLISTED environment, because `.env` is loaded
into this process and a child that inherited it could be made to print the
operator's keys by the very model that wrote the script. RULE 9 / §6 says keys
are never passed where something else can read them, and a subprocess is
something else. A stroke plants secrets and asks the child to find them; it
comes back `LEAKED []`.

**AND THE CHILD RUNS INSIDE A WALL** (2026-09-22, his word: "sandbox the
python"). The paragraph that stood here said the jail was the filesystem and
not the network. Half of that was optimistic: the jail was the PATH the skill
resolves and nothing more, so once the child was running it was an ordinary
Python process with the ordinary reach of one — it could read `.env` and every
other file in this ground, write anywhere the operator can write, open a
socket, and start a shell. **A model writes the file this runs.**

The wall now goes where the child is, and it is the same wall the skill
already draws: THE WORKSPACE IS THE WHOLE WORLD. Reads and writes stay inside
it; the interpreter may still read its own library, because otherwise it is not
a Python. Refused by name: the network (`socket`, `urllib`, and the protocol
modules — RULE 4), starting another process (`os.system`, `subprocess.Popen`,
`os.exec`/`spawn`/`fork`, `os.startfile`), importing `ctypes`, and any of the
`os`/`shutil` verbs aimed at a path outside the wall. A child stopped this way
comes back as **STOPPED BY THE JAIL**, with the reason, rather than a bare
`FAILED (exit 1)` with the cause at the bottom of a traceback.

It is a PEP 578 audit hook: stdlib (RULE 4 — nothing is downloaded), below the
names a script can rebind, and installed from `skills.py`'s own source passed on
the command line, which nothing in the workspace can edit.

**The honest limits,** written down rather than discovered later:

- **an audit hook is not a kernel sandbox.** CPython's own documentation says
  so. This shuts every route named above; it does not prove no route exists. A
  C extension already on this machine, or a CPython bug, is outside what any
  Python-level check can see. Narrowed, not sealed — the same words §15 uses
  about its own import walk, and for the same reason.
- **a symlink is not followed.** Paths are judged with `abspath`, not
  `realpath`, so a link INSIDE the workspace pointing out of it would be read.
  The child cannot make one (`os.symlink` is refused), so this is about a link
  the operator put there himself. `realpath` opens a handle on Windows, and a
  hook that opens files while judging an open is a hook that can recurse.
- **existence is not secrecy.** `os.stat` is not refused: a script may still
  learn that a path outside the wall exists. Reading its BYTES is what is shut,
  and that is the line RULE 7 draws.
- **`import ctypes` is refused at the IMPORT, not at the call,** and that was
  measured rather than chosen: on Windows `import ctypes` itself dlopens
  kernel32 to reach `GetLastError`, so refusing the `ctypes.*` events killed
  the import — and killed it as `AttributeError: kernel32`, because
  `LibraryLoader` turns the failure into one. A refusal nobody can read is not
  a refusal.

Stroked: `test_a_run_python_child_is_walled_into_the_workspace`, eleven routes
refused and five ways that must not fire (the stdlib still imports, the
workspace is still writable, a sibling module still imports, and an ordinary
exception is still `FAILED` and not the jail). By reversal — the wall switched
off — `read_up.py` came back `RAN`, with `MANJUEL_API_KEY=...` on its stdout.

---

## 24. The write door checks before it writes

**Trigger.** `write_file` is given `.py` content that will not parse, or that
imports the network, calls `eval`/`exec`/`__import__`, reaches `importlib`, or
passes `shell=True`.

**Action.** Refused, and NOTHING IS WRITTEN. The refusal names the line and the
syntax error, and says outright that a stray closing tag or a flag block from
the model's own answer counts as source here, because that is the usual cause.

**Why.** 2026-09-12, the coder flow's third live run. The seat's own markup
leaked into the payload and `calculate_sum.py` was written as sound code
followed by `</parameter>` and a `<flags>technical</flags>` block. It was
written happily; `run_python` then died of a SyntaxError, and the flow spent a
repair and a recheck on a fault that was already on disk before anything ran.

`edit_file` had refused exactly those bytes since the day it landed (§23) --
**two doors onto the same workspace and only one of them looked.**

**AND THE SAME STRUCTURAL GATE THE CODER'S LANDING RUNS** (2026-09-22). The
paragraph that stood here said "only `.py`, and only PARSING ... this is not
the structural gate the coder's own landing runs", and that sentence was the
hole restated. TWO DOORS write model-written Python into this workspace:
`land_code` puts the coder's emission through `inspect_code` (§15) — which
refuses a network import (RULE 4), `eval`/`exec`/`__import__`, a dynamic
`importlib`, and `shell=True` — while a seat calling `write_file` by name,
which every seat may, skipped all of it and landed the same bytes. **A gate one
door enforces and the other does not is a preference, not a gate.**

The parse check stays where it is, because its message is the earned one:
`inspect_code` names the line NUMBER, and the leaked-markup fault above is
recognised by the line's TEXT. Prose is still nobody's syntax to judge —
`inspect_code` fails open by name on anything that is not `.py`, which is the
same bound this door already drew.

**AND THE THIRD DOOR** (2026-09-28, the code safety pass before the coder is
let onto the tree). `edit_file` checked that the RESULT parsed and nothing
more, so an edit could bring into a file exactly what this door refuses to put
there — the same lesson, at the door the coder on the tree will use most. The
edit now goes through `inspect_code` too, judged on the whole file as it would
stand rather than on the fragment, because a fragment can complete an import
the file already half-carried. Stroked:
`test_the_edit_door_holds_the_same_line_as_the_write_door` — six edits refused
with the file's bytes unchanged, an ordinary edit still landing, prose still
unjudged, and the unparseable message still naming the line.

Stroked: `test_a_write_refuses_python_that_will_not_parse`, with the exact
bytes that leaked, and both ways -- a real `.py`, a `.md` carrying the same
markup, and an empty `.py` all still land. And
`test_both_doors_into_the_workspace_hold_the_same_line`: six refusals, nothing
written for any of them, and prose, ordinary Python and the earned
leaked-markup message all unchanged.

---

## 25. A mention is not a naming

**Trigger.** A one-word skill keyword appears in the objective as ordinary
English rather than as a request for that skill.

**Action.** No dispatch. The keyword must be NAMED, and what counts as naming
depends on what kind of word it is:

    a FUNCTION word     `when` -- it opens the objective, or it wears quotes.
                        Everywhere else it is grammar.
    a NUMBERED argument `sitting` -- a number sits beside it. The skill's own
                        markdown says so ("The sitting number alone, e.g. 63"),
                        so the rule is read off the declaration rather than a
                        list in Python.

**Why.** 2026-09-12. A coder-flow objective carried a brief reading "...when
executed, it should print 55", and intent dispatched the `when` skill -- a
transcript-window reader, woken to answer a question about a Python file, on
the strength of a subordinate clause. The match was not loose: `when` really is
a keyword.

`sitting` was the next one and needed a DIFFERENT question, because it is a
content word this estate says constantly -- CLAUDE.md and `law/` carry the bare
word 58 times ("while the operator's sitting is open", "the sitting laws").
Every one of those would have woken a transcript reader.

The numeric rule deliberately does NOT borrow the function-word rule's
"opens the objective" clause: `ALIASES` carries "the sitting", so "the sitting
laws bind any hand" opened with the form and read as a naming until a stroke
caught it. A WH-word at the front of a sentence IS the question; a content word
at the front is just a sentence.

Content-word keywords that declare no number are untouched -- `inspect`,
`remember`, `statistics` still dispatch from mid-sentence, and a stroke holds
that, because a rule against accidents must not make the deliberate case
harder.

Stroked: `test_a_keyword_that_is_grammar_must_be_named` and
`test_a_keyword_whose_argument_is_a_number_wants_one`, each both ways.

---

## 26. A turn that wanted hands and used none says so

**Trigger.** Intent read the objective as an ORDER TO ACT on something, the
Router was woken to choose the tool, and it chose none.

**Action.** The delivery carries `NO TOOL RAN`, machine-emitted: *nothing was
read, run or written this turn -- so any result in them came from a seat, not
from the estate.*

**Why.** The existing guard (§14's family: THE NAMED TOOL DID NOT RUN) compares
what intent NAMED against what was CALLED. When intent reads an objective as
action-shaped it names no tool -- "Router decides the tool" -- so if the Router
then decides on none, **both sides of that comparison are empty and no guard
fires at all.** 2026-09-12: such a turn delivered "The result is: 5050" for a
script nothing had run.

KEYED ON WHAT INTENT READ, NOT ON THE `needs_tool` FLAG. The first draft used
the flag and was too broad -- the flag is also raised by a write-shaped
objective and by a seat emitting `<flags>needs_tool</flags>`, and in those a
Router that decides no tool is needed may be perfectly right. It accused a
draft-review stroke whose fixture raises the flag by hand and needs no tool at
all. Narrow and certainly right beats broad and crying wolf.

NEVER ON A REFUSAL, for the reason every list here keeps that rule: when a gate
refuses, no tool runs and the refusal IS the answer.

Stroked: `test_a_turn_that_wanted_hands_and_used_none_says_so` -- fires on
action-shaped-with-no-call; silent on a turn that called something, on a
conversation, and on a refusal.

---

## What this does NOT protect against

Stated plainly, because a security page that only lists wins is marketing.

- **Invention that cites nothing.** A seat can still state something false in
  ordinary prose with no file named and no result cited. Sitting 60 produced a
  confident paragraph about a real client's work, sourced from nowhere. The
  answer to that class is *dispatch* — a question about the ground now reaches
  a reader, so the void that invention fills is smaller — but the class is not
  closed and may not be closeable by arithmetic alone.
- **A model's judgement, where judgement is the job.** The Guardian, the
  Evaluator and the Router make calls a gate cannot make for them.
- **A PARTIAL read spoken as a whole one.** `windowed()` hands a big file
  over as "part 1 of 7 — THIS IS NOT THE WHOLE FILE" in capitals, with a map
  of the headings it did not show. The claim-check then asks only whether A
  READ RAN this turn — part 1 ran, so it passes, and a seat that saw 9% can
  speak about 100%. Named 2026-09-03 after an agent did exactly this to
  `parity.py` and was wrong twice in one turn. BUILT 2026-09-07 as the
  partial-read stamp (§20): the delivery now SAYS the read was partial.
  What is still not caught is the harder half -- a claim about what a read
  SAID with nothing tying it to the read (TASKS, Layer 7).
- **A page that only breaks once somebody plays it** (2026-09-22, the maker's
  piece 3). Before a version is kept the page is loaded in a browser with no
  window and given a moment, so an uncaught error, a rejected promise, a failed
  load or a `console.error` in its SETUP is caught and sent back to the Coder
  for one bounded try. Nothing clicks, types or presses an arrow: a fault that
  needs the game to be played is not seen. This proves a page LOADS and runs its
  own setup without throwing — never that the game is any good. And the check
  FAILS OPEN by name: no browser, a launch that fails, or a page that never
  signals it loaded all save the version anyway and say the check did not run,
  because a gate that silently passes what it could not read is worse than no
  gate (§24's own rule). By his ruling the same day, a page that still errors
  after its one repair is saved too, with the error named in the report.
- **The operator.** Nothing here binds him, and it is not trying to. He is the
  one who lands, and the estate's honesty exists so that what he lands is
  informed.

---

## 27. The tree doors write on a line of work, and refuse the rest by name

**Trigger.** `ground_write` or `ground_edit` is given a path in the ground that
is a secret or `.env`, client data, under `worlds/`, inside any `.git/`, under
`law/`, one of the governing files (CLAUDE.md, .gitignore, .gitattributes,
index_roots.txt, agents/, skills/, pipelines.md, commands.md, .env.example),
the record or a runtime store (sessions/, logs/, index/, state/, flows/,
memory/, memory.md, SEAT_LOG.md, agent_workspace/), a proof stamp under
tests/, BUILDMAP.md, a binary, or under projects/; or the file's repository
stands on main or master or detached, or there is no repository; or the folder
does not exist; or the file is MIXED; or the .py would not parse or -- for an
edit -- would ADD what §24 refuses (2026-09-29: an edit is held to what it adds;
a file's own carrying, skills.py's loopback `urllib`, is said in the reply and
never refused; a whole file written must still be clean).

**Action.** Refused, and NOTHING IS WRITTEN. The refusal names the rule -- RULE
7, SITTING LAW 2, ESTATE LAW 2, LAW 8, RULE 8, RULE 6 -- and, for the main
line, the cure: open a line of work (`git_branch new` through the door, or
Lines of work on Version control) and write on it.

**Why.** His ruling, 2026-09-28: "yes, that's the whole idea of the coder, I
want to actually be able to write/read/modify files within the harness." Until
then a seat wrote only into `agent_workspace/`, the quarantine; `ground_read`
read the ground and nothing wrote it. The code safety pass before the doors
were opened named what the tree needs, and each is a refusal at ONE function
both doors call (`never_written`, `line_of_work`, `terminator_for`,
`checked_python`) rather than a habit at each door -- §24's lesson, made the
rule before the third and fourth doors existed.

THE MAIN LINE IS HIS (RULE 6): a write lands only on a branch that is not
main, judged by the NEAREST repository -- atlas/ carries its own `.git` inside
the ground, and a file under it is judged by atlas's line. Merging a line is
his own act, on his terminal. A FOLDER IS HIS TO PLACE (RULE 8): a seat makes none. THE TERMINATOR
IS THE FILE'S OWN, or its neighbours' for a new file, so a new .py beside LF
files is LF and a new root .md beside CRLF docs is CRLF (the ruling of
2026-09-03). `run_python` is NOT moved to the tree: its wall is the workspace,
and moved it would put `.env` inside the wall.

**And the Coder's own landing goes through them** (2026-09-28, the same day):
when the Expert Coder emits `<filepath>` with a folder in it, or a fenced
block that opens with `@@ OLD`, `land_code` hands the emission to
`ground_edit` or `ground_write` through the skill library rather than writing
it, and the door's reply rides on the seat's tool calls. The Coder gets no
door of its own; it gets these.

**The honest limits.** The never-written names are a list, and a list is
complete only until the ground grows a store it does not name; a new one is
added here by hand. The line-of-work rule reads git, so a ground with no
repository refuses rather than guesses. Nothing here is the hold queue or
RBAC: the tree doors are skills inside the engine, and the door's holds do not
see them -- what lands is gated by the branch and, once folded, by the coder's
flow and its gate.

Stroked: `test_the_tree_doors_write_on_a_line_of_work_and_refuse_by_name`
(60): no repository refuses; main refuses at both doors and names the cure; on
a line a new .py takes LF and a new root .md CRLF, and an edit keeps its own;
the gate at both doors; a folder that does not exist; sixteen never-written
names, each with the file as it was; a path out of the ground; MIXED at both
doors; atlas judged by its own line; `edit_file` unchanged in shape; both
doors in the writers' roster. By reversal: the names not asked, 30 red; the
line not asked, 9; the terminator not the neighbours', 1; the gate struck at
the write door, 2; at the edit door, 2.

## 28. The Coder's window on the tree opens for one passage, by name, or not at all

**Trigger.** The words ask for a CHANGE to a file in the ground -- a path with
a folder in it, a change verb, names in backticks -- and the engine cannot hand
the Expert Coder one passage: no name in backticks; none of the names is on the
file's map (a containing match is not the name -- `help` is not `helper`); the
passage is longer than one window; the file does not parse; the file has no
map (a .py is mapped by definition, a .md by heading, nothing else); a word
two headings contain; the file is a secret or client-tagged; the path leaves
the ground; the file is not there. Or the Coder answered for a file the window
was not on, or with a block far larger than the passage (neither the passage
rewritten nor an edit).

**Action.** The engine answers in the delivery, by name, ending "nothing sat",
and NO SEAT SITS -- not the Coder, not the Router. When the door refuses what
the Coder answered (the main line, a never-written name, an anchor that is not
there), the door's own refusal is the delivery: "Nothing landed -- ground_edit
said: Refused: ...". A Coder that answers in words is told the shape wanted.

**Why.** Four firings of `coder-tree` (2026-09-28) put one small change through
the estate and the seat that could make it never sat: the text was read as big,
the Router was woken directly and planned, and the front Steward who raises
`technical` was skipped. The window (`intent.wants_a_tree_change`,
`pipeline._tree_window`, `maker.tree_prompt`) puts the passage in front of the
one seat that can change it, and refuses everything it cannot put there exactly
-- because an edit is an exact quotation, and a passage the Coder cannot see
whole it cannot quote whole.

**The honest limits.** The window is a .py definition or module-level name, or
a .md section by heading (2026-09-29): the section runs through its subsections
to the next heading as deep or shallower, and a `#` at the start of a line inside
a fenced block reads as a heading, as it does for the reading window. A root
document is asked by its bare name only if it is there; the never-written names
(CLAUDE.md, pipelines.md, commands.md, memory.md, SEAT_LOG.md, BUILDMAP.md) are
still refused at the door. A request that names a tool is never the tree's
(§25's arithmetic), so a flow's attempt text must name none; a carried failed
pass, which quotes the door's name, rides as the turn's FEED instead (2026-09-29),
where the arithmetic never reads it and the Guardian reads it first. The window
hands the first name the map resolves, in the order the words gave them.

Stroked: `test_the_coders_window_on_the_tree` (59; 2026-09-29: the `<filepath>`
line optional, the passage rewritten whole, the outsized block, the door's delta
judgment -- R9 to R12 red). By reversal: the
arithmetic unplugged, 13 red; the whole file handed, 3; the landing not routed
to the door, 6; a containing match accepted, 5; and for the heading window, the
whole document handed, the window's-file wire unplugged, the root-document
guard removed and the headings not read, each red (CHANGELOG, 2026-09-29).

---

## 29. The workspace's reader serves the ground only to a seat cleared for it

`read_file` reads the workspace. Handed a path that NAMES the ground
(`ground/pipelines.md`, `research/...`) and is not in the workspace, it reads
the file through the ground reader's own handler (2026-09-29) -- so every
refusal that door makes is still made: a path that leaves the ground, a secret
(LAW 9), client data (SITTING LAW 2). And one of its own:

    Refused: 'ground/rack.md' names the GROUND, and this seat is cleared for
    the workspace's reader only. Nothing was read.

**Why.** Clearance is per skill (`May Call:`), and dispatch enforces it for
the skill that was CALLED. A reader that passed a call on to another reader
would hand a seat the second one's reach through the first one's clearance.

Stroked: `test_the_workspaces_reader_reads_the_ground_when_it_is_named` (14).
By reversal: the pass-on removed, the clearance check removed, the ground
outranking a workspace that holds the path -- each red.

## 30. A question put to nobody is not asked

A seat marked `On Fail: prompt` that fails asks `retry / skip / abort?`. On a
turn NOBODY ATTENDS -- the standup, a flow's node (the wire's `unattended`) --
the engine does not ask: it takes the default the prompt itself prints, skip,
and writes

    <Seat> failed and is marked on-fail: prompt, and nobody is at the prompt
    (an unattended turn) -- skipped, the prompt's own default

The failure is in the record and the delivery names the seat (SEATS THAT
FAILED). `On Fail: abort` still aborts. An attended turn is asked, as before,
and the answer is never supplied for him (RULE 6).

Stroked: `test_an_unattended_turn_is_not_asked` (11), and over the wire in
`test_the_headless_door`. By reversal: five, each red (CHANGELOG, 2026-09-29).

---

<!-- THE SITES: generated by `python tests/refusals.py` -- do not edit below -->

## THE SITES — every `Refused:` in the code, read off the code

32 refusals are written up above, by hand, each with the sitting that earned it. The code refuses at 89 sites. This tail lists every one -- module, line, and the words it says -- regenerated from the code by `python tests/refusals.py` so it cannot drift; `--check` in CI refuses a stale copy. A site is the code's fact; a section above is the account of why. Where a site's words name a law, a rule or a gate, the section is the one that names the same.

### manjuel/cli.py — 1 site

| line | says |
|---|---|
| 1752 | {exc}\n |

### manjuel/gitstate.py — 9 sites

| line | says |
|---|---|
| 387 | an absolute path is outside this ground ({rel}). |
| 392 | that path could not be resolved ({rel}). |
| 394 | that path resolves outside this ground ({rel}). |
| 455 | that file holds this estate's keys, and they are |
| 459 | this ground's git ignores {rel}, so it is not part |
| 516 | name the line of work. |
| 518 | a branch name may not begin with '-' -- git reads it |
| 522 | {name!r} is not a lawful branch name |
| 525 | {name!r} is not a lawful branch name. |

### manjuel/intent.py — 1 site

| line | says |
|---|---|
| 799 | `content` must be a |

### manjuel/pipeline.py — 2 sites

| line | says |
|---|---|
| 3454 | a sub-task may not start another sub-task |
| 3458 | {SUB_RUNS_MAX} sub-tasks have already run this |

### manjuel/skills.py — 76 sites

| line | says |
|---|---|
| 692 | `{name}` must be a PATH, and {raw!r} is a |
| 832 | {raw!r} is not a place in this ground. A world is a folder |
| 840 | that is not a world a seat may act in. Nothing under |
| 846 | {raw!r} is a file, not a world. A world is the folder a |
| 862 | {label} is not a repository of its own -- it is a folder |
| 1730 | '{path.name}' is a secret and is never read aloud (LAW 9). |
| 1732 | that is CLIENT DATA — tagged protected, never read |
| 1877 | {shown} is a SECRET by name. Nothing about it is read, |
| 1880 | {shown} is CLIENT DATA by tag. Never read into the chain, |
| 2055 | '{filename}' names the GROUND, and this seat is cleared |
| 2062 | that is CLIENT DATA — tagged protected, never read |
| 2143 | that content is not parseable Python -- |
| 2150 | {path.name} {why}. NOTHING WAS WRITTEN. This is the |
| 2181 | an index build is already running. |
| 2556 | {exc} |
| 2737 | {exc} |
| 2748 | {exc} |
| 2763 | {exc} |
| 2796 | git_cycle needs a commit message. The message is the |
| 2811 | git_cycle ships THIS ground and no other. What it |
| 2835 | the proofs could not be read |
| 2879 | this ground is not a git repository. |
| 2897 | the head did not move, so no |
| 3207 | '{tag}' is loaded but is NOT declared in this |
| 3225 | pulling reaches the network and can move gigabytes |
| 3251 | an index build is still running behind an earlier |
| 3332 | an index build is already running. |
| 3829 | this ground declares no MCP server. Declare one |
| 3840 | this ground declares no MCP server called |
| 3856 | the address declared for {name!r} is not on this |
| 3877 | {name} could not be read -- {err}. |
| 3903 | the arguments for {tool!r} must be a JSON |
| 3907 | the arguments for {tool!r} must be a JSON |
| 3915 | {raw[:80]!r} sits in that request |
| 3936 | {name} carries no tool called {tool!r}. |
| 3938 | {name} could not run {tool!r} -- {err}. |
| 3945 | {name}'s {tool!r} refused -- |
| 4005 | edit_file needs the file to edit as <filepath>, and |
| 4012 | {rel!r} is not a path this skill may touch ({exc}). |
| 4014 | there is no {path.name!r} in the workspace to edit. |
| 4033 | the edit needs exactly one `{_EDIT_OLD}` line and |
| 4046 | the text after `{_EDIT_OLD}` is empty; nothing to find. |
| 4048 | the old and new text are identical. Nothing to do. |
| 4064 | {path.name} has MIXED line endings, so an edit |
| 4072 | that passage is not in {path.name}. Nothing was |
| 4076 | that passage appears {hits} times in {path.name}, |
| 4093 | that edit would leave {path.name} unparseable |
| 4104 | that edit would leave {path.name} {added}. |
| 4218 | '{path}' is outside the ground. Nothing was written. |
| 4222 | '{rel.as_posix()}' is a secret, and keys are silent -- never |
| 4225 | that is CLIENT DATA -- tagged protected, never read into the |
| 4228 | a `.git/` is the history, and the history is git's to write |
| 4231 | {_NEVER_WRITTEN_TOP[parts[0]]}. Nothing was written. |
| 4233 | '{rel.as_posix()}' is a proof stamp, written by the suite that |
| 4237 | {_NEVER_WRITTEN_FILES[path.name.lower()]}. Nothing was written. |
| 4239 | '{path.name}' is a binary, and a binary is placed on the |
| 4263 | the ground is not under version control here, so a line of |
| 4268 | git could not be asked ({g.error}). Nothing was written. |
| 4272 | the repository at `{repo.name or repo}` stands {where}, and the |
| 4304 | that content is not parseable Python -- {exc.msg} at line |
| 4309 | {path.name} {why}. NOTHING WAS WRITTEN. This is the same |
| 4319 | {verb} needs the file as <filepath>, relative to the |
| 4323 | '{rel}' is outside the ground. Nothing was written. |
| 4340 | '{rel}' is a folder, not a file. Nothing was written. |
| 4342 | '{path.parent.name}/' is not a folder in the ground, and a seat |
| 4351 | {path.name} has MIXED line endings, so a write cannot keep what |
| 4372 | there is no '{rel}' in the ground to edit. ground_write makes a |
| 4563 | run_python needs the file to run as <filepath> -- a |
| 4568 | {rel!r} is not a path this skill may run ({exc}). |
| 4570 | run_python runs Python, and {path.name!r} is not a |
| 4573 | there is no {path.name!r} in the workspace to run. |
| 4594 | {path.name} did not finish inside {RUN_TIMEOUT:.0f}s |
| 4599 | {path.name} could not be started -- {type(exc).__name__}: {exc} |
| 4988 | the table reviews; it does not act. {why} |
| 4998 | {who} is not cleared to call '{key}'. |
| 5024 | '{action}' did not finish within |

<!-- /THE SITES -->
