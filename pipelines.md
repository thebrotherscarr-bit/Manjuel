# Pipelines

The order seats run in. This file is the source of truth — adding a pipeline is
editing this file and running `/reload`, never a code change. Switch with
`/use <name>`; `default` is what a sitting starts on.

**Most seats rest, and racked seats are not written here at all.** A seat with
`Wakes On:` in its own file sits off the spine entirely and is summoned when
its flag is raised -- the same way a model sits cold on the rack and a skill
sits unbound in `skills/` until it is called. The spine below holds only what
runs every time. `Wakes: first | after <Seat> | last` says where it slots in.

A pipeline may give its own turn more or less time than the rest: a line
reading `**Deadline:**` and a number of seconds, on its own in the pipeline's
section with no bullet in front of it, is how long ONE TURN on that pipeline
may take. A pipeline that declares none takes the dial, `MANJUEL_TURN_DEADLINE`
(600). Only `court` declares one.

A seat named here must exist in `agents/`, or startup refuses and names it.
A parenthetical is a note the parser ignores -- UNLESS it says `when: <flag>`, which is a step-level condition that overrides the seat's own `When:` (`when: always` seats it unconditionally). Otherwise `When:` lives on the seat.

## Pipeline: default

**The Steward bookends it.** He answers first — cordially, and honest about
what he cannot do himself. If the work needs a tool, code or a document, he
says so and hands off. Then he comes back and tells you plainly what came of
it, in the same voice.

1. Steward
2. Router                (when: needs_tool)
3. Steward               (when: worked)

**The rest are racked.** They are not listed here because they do not belong
to this order -- they belong to a condition. Each declares its own summons in
`agents/`, and the engine pulls it in when the flag is raised:

| seat | wakes on | slots in |
|---|---|---|
| Security Guardian | `has_feed`, `suspicious` | first |
| Expert Coder | `technical` | after Router |
| Reasoner | `hard` | after Router |
| Quality Evaluator | `drifted`, `review` | after Router |
| Proofreader | `prose` | last |
| Delivery Agent | `deliver` | last |

Adding a specialist is writing one file in `agents/` with a `Wakes On:` and a
`Wakes:` line. This file does not change.

**The guard is gated on provenance, not on suspicion.** When you type a
question at your own terminal there is nothing to guard against — you are the
trust boundary, and paying 7s to be protected from yourself on every "hi" is a
tax with no payer. So the guard runs when UNTRUSTED material is present:

- `has_feed` — you pasted source material. It is checked BEFORE the Steward
  reads it, so a refusal still means no later seat ever saw it. That is a real
  gate.
- `suspicious` — the Steward saw something wrong in what a skill pulled off
  disk and summoned the guard. This is a REVIEW, not a gate: he has already
  read it. Weaker by construction, and worth having anyway, because the
  alternative is nobody looking at fetched content at all.

- an ordinary question: **Steward** alone
- with pasted source: **Guardian → Steward → ...**
- needing a tool: **Steward → Router → [skill] → Steward**
- a request to MAKE something ("make me a snake game"): **Expert Coder** alone,
  whatever the pipeline -- the engine routes it and saves the page (the maker,
  in the worked examples below)

## Pipeline: brief

For a pasted feed. The Morning Reviewer compresses noise to its core before
anything else reads it, and the result is delivered as a written briefing.

1. Security Guardian
2. Morning Reviewer
3. Delivery Agent   (when: always)

## Pipeline: estate

Every seat runs — the deliberate Manjuel, not the everyday one: inquire, hold the
whole, refute, then rule.

**Manjuel is last, here as in `court`.** Until 2026-09-01 this pipeline ran him
third of the counsel (`agents.md` and this file disagreed on the ordinal until
2026-09-04; the fact is the same: ahead of Jesster), so the Court ruled on counsel it had not yet heard —
recorded as an open discrepancy in `agents.md` and closed by operator ruling.
THE LAW's court model is the order: counsel lays what it saw, the Court weighs
it, and a ruling made before the last counsel spoke is a ruling on a partial
record.

1. Security Guardian
2. Steward
3. Neiro
4. Jesster
5. Manjuel

## Pipeline: court

THE LAW's order — the court hears every counsel, then rules. Manjuel last.

**The table reviews; it never acts.** The Router here may reach only the
reading skills — search, ground_read, git_status and their kin. Anything
that changes the ground is refused at the table, by the engine, whatever
any seat asks for. Counsel has eyes, not hands.

**Deadline:** 900

One turn at the table may take 900 seconds where every other turn takes 600.
His ruling, 2026-09-28, the evening the court was measured cut at its turn
(sitting 285: Jesster stopped at 552 s and the judge never seated): "600 max
per seat other than the court which requires a max of 900". No seat here may
take more than 600 of them by itself.

1. Security Guardian
2. Steward
3. Router      (when: needs_tool)
4. Neiro
5. Jesster
6. Manjuel

## Pipeline: quick

One seat past the gate. For a throwaway question.

1. Security Guardian
2. Steward

## Worked examples — what a turn looks like when it goes right

Written 2026-09-04 on the operator's word, after sitting 84 delivered a raw
tool call as an answer. This section is COMMENTARY: the parser stops at the
heading above it and everything here sits in fences. It exists so that a
hand -- or a seat reading this file through `ground_read` -- can see what
the moves are and what the engine does with each one.

### The moves a seat has

Every seat writes plain words. Beside the words, a seat has exactly these
signals, and the ENGINE acts on them -- a seat never acts on its own:

```
<flags>needs_tool</flags>       any seat. "This needs a tool." Wakes the Router.
                                Say in one line what for; the flag is stripped
                                before anyone reads the sentence.
<action>skill</action>          THE ROUTER ONLY. Runs that skill, feeds the
<filepath>x</filepath>          result back, bounded at 5 hops, duplicates
<content>payload</content>      refused. From any other seat this is a REQUEST:
                                since sitting 84 the engine carries it to the
                                Router as needs_tool and strips it. Nothing
                                but the Router executes.
SAFE  /  UNSAFE: <reason>       the Security Guardian only. UNSAFE stops the run.
PASS                            the Quality Evaluator only. Keeps the draft as is.
NEEDS: <the missing thing>      the Quality Evaluator. Sends the run back through
                                the Router ONCE, evidence carried, not a summary.
<filepath>name.py</filepath>    the Expert Coder only, followed by a fenced
```python ... ```                block. The ENGINE writes the file (inside the
                                workspace jail, after the AST gate) and raises
                                `review`. The seat never writes.
```

And these lines are the ENGINE's, never a seat's -- they appear in the
transcript and the delivery whatever the words around them say:

```
law: chain whole (4 links, head ...)        THE LAW GATE, first on every run:
     objective passed 4 checks              the ledger verified, the request
                                            checked (REFUSALS §19). A refusal
                                            here means no seat sat.
THIS TOOL FAILED — NOTHING WAS DONE.        a skill errored or was refused
Tool NOT re-run: git_status                 the dedup: same call twice in a RUN
                                            (a WRITE reopens the reads, so a
                                             status after a commit still runs)
NOT EVERYTHING RAN. N tools failed...       the recompose, appended to the delivery
note: <Seat> claimed the contents of x.md;  the claim-check: a file cited, no read
      no read ran this turn.
--- Router reading the above (testimony, not tool output) ---
```

### What the delivery is

The delivery is the LAST seat that produced output. It is not a summary
made by the engine and it is not a vote. So on `default`:

- no tool needed: the door answered, nobody else sat, **the door's answer
  IS the delivery.** That is one seat speaking once, not parroting.
- a tool ran: the closing Steward sits (`when: worked`) and tells you what
  came of it in plain words. That closing seat is the one that must READ
  the tool result rather than the previous seat's prose -- the closing-seat
  seam in DAYBOOK Session 4 is every time it did not.
- the door answered in markup: until sitting 84 that markup WAS the
  delivery. Now the Router runs and the closing Steward delivers.

### `default`, a plain question — one seat

```
operator   morning, what's on the board?

Steward    (llama3.2)  Morning. Nothing new on the board since yesterday's
           toll — the parity run is still owed. Want me to pull the task
           list?
           [no flags]  → Router skipped (needs_tool never rose)
                       → closing Steward skipped (nothing worked)

delivery   = the Steward's words above.
```

### `default`, a question that needs a tool — three seats

```
operator   what's uncommitted in the git?

Steward    Let me have the Router check the tree. <flags>needs_tool</flags>
           engine: flag read, stripped. "Let me have the Router check the tree."
                   goes to the record.

Router     (qwen3.5:4b)
           <action>git_status</action>
           engine: runs git_status →
                   git: master@63fab9e  DIRTY (4 changed, 0 untracked)
           Router: (reads it) Four files changed, nothing untracked.
           engine: flag `worked` set (a tool ran)

Steward    (closing, when: worked) Four files are changed and nothing is
           untracked — the tree is dirty at 63fab9e. Commit when you like.

delivery   = the closing Steward's words. The tool line is in the transcript.
```

The same run when the door answers in markup instead (sitting 84's shape):

```
Steward    <action>ground_read</action><filepath>rack.md</filepath>
           engine: NOT the Router → carried: needs_tool raised, named tool
                   = ground_read, filepath = rack.md as the floor; markup
                   stripped; record notes "answered with a tool call
                   instead of words -- carried to the Router, not printed".
Router     runs ground_read (or refuses it, if the door named something the
           table may not call) …
Steward    (closing) delivers in words.
```

### `default`, code — the coder wakes, the evaluator reads what landed

```
operator   write a function that returns the cosine of two float lists

Steward    That's the Expert Coder's. <flags>needs_tool technical</flags>
Router     no skill needed for writing code → no action; prose: "handing to
           the coder".
Expert Coder  (qwen2.5-coder:7b, wakes on `technical`, after Router)
           <filepath>cosine.py</filepath>
           ```python
           def cosine(a, b): ...
           ```
           engine: AST gate parses it; no network import, no eval → LANDS in
                   agent_workspace/cosine.py; flag `review` raised.
Quality Evaluator (qwen3.5:4b, wakes on `review`)  reads the file ON DISK.
           PASS                      → draft kept
           or NEEDS: a zero-magnitude guard   → back through the Router once
Steward    (closing) "cosine.py is in the workspace; it returns 0.0 when
           either list has no magnitude."
```

### A make request — the maker: the engine routes, the Coder only writes

Added 2026-09-21 (SPEC 4.8, DESIGN 14.15). No spine seat sits: the ENGINE
reads the request by arithmetic, seats the Expert Coder alone, checks what it
writes and saves it as a version of a project. Whatever pipeline is in use, a
make request goes this way. Live, sitting 258, from the dashboard:

```
operator   Make me a simple snake game I can play.

engine     law: chain whole ...
           maker: a request to MAKE something ('simple snake game') -- the
           Expert Coder writes it as one page, the engine saves it as a
           project with its own history
Expert Coder  (qwen2.5-coder:7b, the ONLY seat; 15.4s)
           <filepath>index.html</filepath>
           ```html
           <!DOCTYPE html> ... the whole game ... </html>
           ```
           engine: a WHOLE page (it reaches </html>)? loads NOTHING from the
                   network (RULE 4)? -> saved as projects/snake-game/
                   index.html, VERSION 1: a commit in the project's OWN
                   repository. The ground's history is not touched.
Maker      (the engine, no model)  Made snake-game -- version 1. It is one
           page, index.html (93 lines) ... To try it, open
           projects\snake-game\index.html in your browser. What next? ...

operator   make it faster
Expert Coder  handed the page as it stands and "THE CHANGE ASKED FOR: make it
           faster"; answers the whole page back (10.8s) -> VERSION 2
Maker      Changed snake-game -- version 2: make it faster ...

operator   go back
Maker      NO SEAT SITS (0.6s): git brings version 1 back and saves it as
           VERSION 3 -- snake-game is back to version 1, saved as version 3,
           so nothing was lost. Its versions: 1, 2, 3 ...

delivery   = the Maker's report, every time: facts read off the disk, never a
           seat's account of them.
```

NOT the maker's, and run the ordinary way: "write a poem", "make a note",
"write a python script" (the Coder's own path, into the workspace), a question
about making ("how do I make a game?"), and anything that names a tool. A page
the check refuses -- cut off before `</html>`, or loading from the internet --
is not saved, and the report says why in words. A change is only read while
the sitting has a project in hand; a new sitting starts with none.

PICKING ONE UP, AND PUTTING IT DOWN (piece 2, 2026-09-21). Both are the
engine's answer too, and no seat sits for either. The Dashboard's project list
sends the first words; a person can type either:

```
operator   work on the snake-game project     (or "work on the snake game",
                                               "switch to the calculator",
                                               "open ...", "go back to ...")
Maker      Working on snake-game now -- it is at version 2. Its versions: ...
           Ask for a change in plain words and it becomes version 3; say
           "put it down" when you are done with it.
           delivery.project = "snake-game"   (how the glass knows)

operator   put it down                        (or "put the project down",
                                               "I'm done with it", "close
                                               the project" -- the WHOLE request)
Maker      Put snake-game down. It is kept exactly as it is -- version 2, in
           projects\snake-game\ -- and nothing is in hand now.
           delivery.project = ""
```

Words that name no project fall through as they always did ("open the pod bay
doors", "go back to version 1" still goes back); words that say "project" and
name none are told what there is; two projects answering to one word are both
named and neither is picked. "put it down lower" is still a change, and "put
it back" still goes back.

### `court`, a judgement — four heads, then a ruling

```
operator   /use court
           should gemma sit at the front door?

Security Guardian (llama3.2)  SAFE            (only if a feed was pasted)
Steward    frames it; raises needs_tool if the record should be read.
Router     reads: rack_list, semantic_search "front door" — READ-ONLY at
           the table; a writing skill is refused by the engine here.
Neiro      (llama3.2, the warden)   what the record shows, sourced.
Jesster    (deepseek-r1:8b, the licensed fool)   the strongest case AGAINST.
Manjuel    (gemma4:12b, rules last)  Supported / Missing / Ruling, citing
           what Neiro and Jesster actually said — not what the Router
           asserted without a tool behind it (sitting 82's fault).

delivery   = Manjuel's ruling, with the recompose block appended if any
           tool was refused.
```

A court that fits in VRAM is 15GB; this one is 20GB. The engine evicts and
reloads between seats. That is the price of four heads and is paid on
purpose (memory.md, 2026-09-04).

### What every seat is handed, every run

The clock (`## Now`), appended by the engine after the seat's own prompt.
The law (`## The law`) and, for the door and the court, the standing
(what this sitting is for, from DAYBOOK's last entry) -- carried in the
SYSTEM role beside the seat's own prompt since 2026-09-07, because seats
recited the law block as content when it sat in the user prompt. The
court is handed the ten estate laws verbatim; every other seat the short
form. Facts, not instructions from a model: when it is, that the laws
verified and the request passed the gate, and what the sitting is for.

### What a seat must NOT do

```
answer with a tool name or a flag and nothing else   ("ground_list")
restate the previous run's delivery as this run's    (the seam)
report success over a THIS TOOL FAILED line          (the recompose catches it;
                                                      do not make it)
name a file's contents with no read this turn        (the claim-check refuses it)
invent an operator: / steward: dialogue              (class d; there is one
                                                      operator and he is typing)
```

### The coding loop, and what closes it

Written 2026-09-11, when the loop stopped being one pass.

THE MOVES WERE ALREADY THERE. A `technical` objective wakes the Expert Coder;
it emits a `<filepath>` and one fenced block and calls nothing itself; the
harness parses that BEFORE writing it (`inspect_code`, REFUSALS 15), lands it
in the workspace, and raises `review`; the Quality Evaluator wakes on that and
may answer `NEEDS: <the one thing>`, which sends the run back through the
Router ONCE with the evidence carried rather than a summary.

WHAT WAS MISSING WAS A VERDICT AND AN EDIT. The only machine answer in that
circuit was "does it parse", and a loop cannot steer on `compiles`. So:

```
run_python <file>   the verdict. RAN, or FAILED with the exit code, and both
                    streams. One interpreter, one jailed path, never a command
                    from a model. The child is bounded and cannot see .env.
edit_file  <file>   the fix, as a fragment rather than a rewrite. The anchor
                    must match EXACTLY ONCE or the edit is refused with the
                    count -- at 8192 context a seat cannot hold a large file
                    to rewrite it, and an anchor that matches twice does not
                    say which.
```

THE ROUTER RUNS BOTH, not the coder. `agents/expert_coder.md` has no
`May Call:` line at all, so it calls nothing: it writes, and the Router edits
and runs. That is the same separation the estate has everywhere -- the seat
with the most hands has the tightest law.

### The `coder` flow — when one send-back is not enough

The Evaluator's `NEEDS:` is ONE pass back inside a single turn. For work that
wants more than that, the shape below is a flow, gated, across turns:

```
brief ──→ attempt ──→ verify ──→ verdict ──pass──→ land (gate)
            ▲                       │
            └─────────fail──────────┘   a RETURN: at most 2, because `attempt`
                                        declares `loops: 2`; at the ceiling the
                                        fail is a fail and the run stops FAIL
```

    brief     ask    turn the hand's one line into ONE concrete task: the
                     exact .py filename, what a run should print, and that the
                     file is run with NO ARGUMENTS so it must exercise its own
                     cases
    attempt   run    write what that task asks for, at the filename it names --
                     and, on a pass after a return, read `{{fail_attempt}}`:
                     the verdict that sent it back and what `verify` said on
                     that pass. `loops: 2`.
    verify    run    run the file that task names, report exactly what it said
    verdict   eval   on `verify`, expecting `{{expect}}` -- the marker the HAND
                     named when it fired the flow; its fail-edge returns to
                     `attempt`, its pass-edge reaches the gate
    land      gate   nothing has reached the estate; carry on, or stop here.
                     Its title says how many passes it took (`{{pass_attempt}}`)

Five nodes, budget 1800s, folded as v13 on 2026-09-28. THE RETRY IS A BOUNDED
RETURN (LAW_003): `verdict`'s fail-edge sends the run back to `attempt`, whose
`loops` is the ceiling -- declared on the node returned to, where a reader
meets it, and read by the runner and nowhere else. Each return re-does the
WORK (attempt, then verify) and never re-scores an answer; every pass and every
return is on the record with a `loop` line between them, and `flow_status`
renders each; the budget binds every pass. Versions 1 to 12 unrolled one repair
into `repair -> recheck -> proof` and are kept on disk; twelve of their
nineteen runs paused at the gate, the rest failed. Every node runs inside the
workspace jail and the flow ends at a GATE, because landing is the operator's
act and nothing else (RULE 6).

THE ONE EVAL ASKS ABOUT THE REQUIREMENT, NOT ABOUT EXECUTION, and that is the
whole correction of 2026-09-12. It used to be `check`, expecting `RAN:` -- and
a flow fired at a real task went GREEN over code that did the opposite of what
the objective said, because `run_python` had exited 0 and nothing asked whether
the work was right. A green on wrong code is worse than a red: the green is
what a reader trusts.

Three wirings were tried and two were wrong, each corrected by an actual run:

    liveness gating correctness   a task whose correct behaviour is a NON-ZERO
                                  EXIT fails a `RAN:` gate. A correct refusal
                                  exits 1.
    two evals as recorders        an eval is a GATE, never a passive recorder.
                                  `run.go`: `if !hasFailEdge(...) { return
                                  VerdictFail }` -- an eval that fails with no
                                  fail edge stops the whole run, so a
                                  "recording" eval killed the run before the
                                  judging one could fire.

So: ONE eval, on the requirement. Liveness is not a second gate -- it is
evidence, and `--- WHAT THE TOOLS SAID ---` already puts it in front of any
reader at the gate.

AND THE CHECK READS THE EVIDENCE, NEVER THE PROSE. A `run` node's answer
is two things: what the seats said, and `--- WHAT THE TOOLS SAID ---`,
the machine's own verdict lines with each tool's output under them. The
eval scores the second and not the first, because prose QUOTES
requirements and prose NEGATES them -- on 2026-09-12 a check for
`FIB6: 8` passed on the sentence "printed FIB6: 0, which is not the
expected output of FIB6: 8", and passed again on a node that had merely
echoed its own objective. The answer is still what a person reads at the
gate; it is simply not what decides.

AND THE EXPECTATION IS ONLY AS GOOD AS THE OBSERVABLE THE OBJECTIVE NAMES. A
run whose code was CORRECT still failed, because the hand wrote `Refused` and
the program printed `Refusing`; `contains` is exact and case-sensitive and did
what it was told. The cure is a spec -- name the marker in the objective, match
it in the expectation -- not fuzzy matching, which would put back the
laundering this exists to stop.

AND THE REPAIR PATH IS JUDGED TOO, which it was not until 2026-09-12.
`recheck ──→ land always` meant a run that failed its requirement, repaired and
rechecked arrived at the hand with NO judgement of the repaired work -- the same
fault as the original green-on-wrong-code, moved one edge down. `proof` holds
the repair to the SAME expectation.

`proof` HAS NO FAIL EDGE, and that is deliberate. An eval that fails with no
fail edge stops the run, and there is nothing to steer to anyway: the retry is
unrolled, so there is no second repair. Work that still does not meet the
requirement must not be OFFERED for landing. So the verdict now means
something -- PAUSED is "it passed, your hand decides", FAIL is "it did not" --
and nothing is thrown away either way: every attempt is still in the workspace
with what each run said.

THE SHAPE IS WRITTEN HERE BECAUSE THE FLOW ITSELF IS NOT IN THE RECORD.
`flows/` is the engine's runtime store and is gitignored -- specs, their folded
history and runs.jsonl. A flow worth keeping is one a reader can rebuild from
the record; the instance on disk is state, and state does not travel.

### The `coder-tree` flow — the coder on the harness itself, on a line of work

His ruling, 2026-09-28: "yes, that's the whole idea of the coder, I want to
actually be able to write/read/modify files within the harness." The `coder`
flow above writes in the workspace; this one writes the ground -- manjuel/,
tests/ -- and the estate's own suites are the check. Folded as v1 the same day,
the last piece of the code safety pass.

```
brief ──→ open (gate: grants git_branch) ──pass──→ line ──→ attempt ──→ strokes ──→ strokes_ok
                                                           ▲                          │ pass
                                                           │                          ▼
                                                           │                        smoke ──→ smoke_ok ──pass──→ land (gate) ──pass──→ save
                                                           │                                    │
                                                           └──────────── fail (either check) ───┘      attempt declares `loops: 2`
```

    brief       ask    ONE concrete change to the harness: the files, as paths
                       relative to the ground, what changes, and the stroke or
                       check that will show it worked
    open        gate   HIS HAND opens the line: `continue` grants `git_branch`
                       to the node after it, and nothing on main moves
    line        run    a spelled-out door call, decided by arithmetic:
                       `git_branch new {{line}}` -- the door moves the ground
                       onto the line
    attempt     run    v4 (2026-09-29): the objective ALONE, through the Coder's
                       window -- the Expert Coder handed the passage by name,
                       its edit through `ground_edit` (the tree doors refuse the
                       main line and the never-written names by themselves).
                       No brief and no carried failed pass in the TEXT: either
                       can name a door and shut the window. The failed pass
                       rides as the turn's FEED instead (the runner hands
                       `fail_attempt` over as source material, same day), and
                       the Coder reads it FIRST, under "THE LAST PASS FAILED",
                       above the passage and the change (his ruling). `loops: 2`
    strokes     run    a spelled-out `suite_run` (strokes); the suite stamps its
                       own proof
    strokes_ok  eval   on `strokes`, expecting `green · exit 0` in the tools
                       block -- the head the door reads off the stamp; fail
                       RETURNS to `attempt`
    smoke       run    a spelled-out `suite_run` (smoke)
    smoke_ok    eval   the same, on `smoke`; fail returns to `attempt`
    land        gate   the strokes and the smoke green on the line: save it
                       there? Merging to main is his merge on his terminal (v5)
    save        run    `git commit: "{{message}}"` -- the council's own commit,
                       on the line, the message his (MESSAGE_IS_THE_OPERATORS)

Ten nodes, budget 3600s. Inputs: `objective`, `line`, `message`. THE LOOP IS
LAW_003'S: the ceiling on `attempt`, read by the runner; the stop is the door's
own head off the suites' stamp, machine-emitted, never a seat's account; every
pass on the record. THE GATE STANDS AT THE ENDS, NOT INSIDE: his hand opens the
line and his hand saves on it, and nothing between asks him. What the doors
refuse by themselves (REFUSALS §27) the flow never has to: a write on main, a
governing file, a folder that does not exist. `run_python` is not in this flow
on purpose -- the suites are the run, and they run through the door.

FIRED ONCE, 2026-09-28 (run `f-20260928-201849-a7674117`, sitting 288): the
line opened on his hand, the loop returned twice and stopped FAIL at the
ceiling, and the record found two wires short -- the core's door call waits
60 s while the strokes take 150, and the map of a large file does not name a
module-level assignment, so the coder never reached its passage. CHANGELOG
carries the account; both are his to order.

V2, THE SAME DAY: a `changed` check on the attempt -- its tools block must
carry a tree door's "on line of work" reply, else the run returns to the
attempt -- because the second run reached `land` in one pass with nothing
changed and every check green; the attempt is handed the operator's objective
verbatim beside the brief; the brief is told never to ask for more.

    changed     eval   on `attempt`, expecting a tree door's reply (`on line
                       of work ``) in the tools block; fail returns to `attempt`

Eleven nodes, thirteen edges. FIRED TWICE MORE (runs two and three): the wires
hold and the loop steers, and the seats do not act -- the Router plans the
two-call edit and stops at the plan, the Expert Coder lands only in the
workspace, and the Steward claims an edit that never happened.

V3, THE SAME EVENING: the Coder now lands on the tree (`land_code` hands a
path with a folder, or an `@@ OLD` block, to `ground_edit`/`ground_write`,
the door's reply on the Coder's own tool calls), so the attempt is spoken to
THAT shape: read the passage by name, then answer with `<filepath>` (the path
in the ground) and one fenced `@@ OLD`/`@@ NEW` edit, never the whole file
and never the workspace doors; the turn is judged on whether a door reports
the edit, which is what `changed` reads. Same nodes and edges as v2.

FIRED A FOURTH TIME (v3): the Expert Coder never sat -- a big objective wakes
the Router directly and skips the front Steward, so `technical` is never
raised -- and the Router stalled at the map while the Steward, of all seats,
emitted the Coder's shape. What comes next is the Coder's window on the tree:
the Coder woken by arithmetic and handed the passage, as the maker hands it a
page (CHANGELOG, for his word).

THE CODER'S WINDOW, THE SAME NIGHT: a change to a named file in the ground (a
folder in the path, a change verb, the passage in backticks) is read by
arithmetic before any other route (`intent.wants_a_tree_change`); the Expert
Coder sits ALONE, handed the passage as it stands off the file's own map
(`_tree_window`, the name resolved exactly), and the door's reply is the
delivery. MEASURED: v3's attempt text names `ground_read` and the workspace
doors, so on it `names_a_tool` fires first and the window never opens -- fired
as it stands, v3 would still wake the Router. A v4 whose attempt carries the
objective, the brief and the failed pass and names no tool is his to order;
not folded here.

V4, FOLDED 2026-09-29 as the glass (v3 kept): the attempt is `{{objective}}`
alone; `changed` expects "line of work `" (the tail both doors' replies share;
the eval reads the tools block alone); the brief trimmed of tool names. Same
nodes and edges. FIRED (run five, sitting 292): FAIL at the ceiling, and for
the first time the Coder sat on every pass, through the window -- the edit
right with no `<filepath>` line; the dict rewritten whole; the edit exact and
the door refusing it for what skills.py already carried. All three built the
same day (CHANGELOG): the file is the window's, a block with no markers is the
passage rewritten whole, and the door judges what an edit ADDS. The failed
pass was not carried in the text on purpose -- it quotes the door's name --
and since the same evening it rides as the turn's FEED, which the arithmetic
never reads and the Coder is shown (CHANGELOG, "carry the failed pass without
the door's name"). An objective typed for this flow must name no tool ("the
founding documents" names `semantic_search`).

FIRED A SIXTH TIME (v4, the three fixes in the engine): COMPLETE in one pass,
315 s -- the line opened at his gate, the Coder handed the passage answered it
rewritten whole, the door landed the one line, the strokes (3135/3135) and the
smoke (72/72) green through the door, and his hand at `land` had the council
save it on `tree-foundation-6` (`ba0e61a`). The flow is proven live; merging
the line is his merge on his terminal -- Version control has no such click, and
v5, folded the same day, says so at the `land` gate (CHANGELOG, 2026-09-29).

FIRED A SEVENTH TIME (v5, the failed pass riding as the feed) on a change whose
first pass the door refuses by design (`import socket`, RULE 4): FAIL at the
ceiling -- the carry held live (the feed, the Guardian first, the Coder shown
the refusal) and the seat repeated the refused block on both retries. The
mechanism is proven; a seat that changes course on a refusal is his ruling
(CHANGELOG, 2026-09-29).

FIRED AN EIGHTH TIME (v5, the refusal first in the Coder's prompt, his ruling
built): the same three passes -- refused, repeated, then a malformed block --
FAIL at the ceiling. The seat's floor is measured (SITTING LAW 3); moving the
Expert Coder's seat is his ruling (CHANGELOG, 2026-09-29).
