# THE LAW LEDGER

```
type:     DIRECT (sovereign law of the house) -- APPENDABLE
by:       the operator's word, 2026-09-21: "an appendable ledger that the
          hand can continue to iterate on as directed, that we can chain
          or seal when we would like"
cites:    covenant 65118a147dd49ed9 · SITTING_LAWS.md (laws 1-4, sealed) ·
          ESTATE_LAWS.md (naming) · CLAUDE.md (the standing rules)
sealed:   as far as `python law\law.py status` says, and no further
```

## How this file works

- It grows at the bottom, and only there. A hand appends an entry when
  the operator directs it, and only then (RULE 5b: talk is talk). Every
  entry says where its words came from.
- The operator seals it: `python law\law.py seal LAW_LEDGER.md`. That
  lays a DIRECT link on the chain whose anchor carries `bytes:N` -- the
  file's length at that moment -- and the fingerprint of those N bytes.
- Everything above the furthest seal is law, and frozen. Change one byte
  of it and the chain stops verifying, and the law gate refuses every run
  until the byte is put back (LAW 4: a red blocks the road).
- Everything below the furthest seal is DRAFT: on the operator's word it
  may be added to, reworded or struck. A draft is not sealed law -- and a
  rule copied here from CLAUDE.md binds there, as it always has.
- A sealed entry is changed by a new entry that amends it, sealed in its
  turn. The sealed words stay where they are, as the record of what was.
- `python law\law.py status` shows how far this file is sealed.
- Never `direct` this file. That binds every byte of it, and the first
  entry appended after would break the chain.

An entry's number is its place in this ledger, not a law's name. Each law
keeps the name it is cited by; where two names collide, the collision is
written down and the choice is the operator's.

## The laws housed in their own files

Sealed on the chain as of 2026-09-21. Each is read where it lives; this
ledger does not copy them.

    link 1   law/LAW_001_FOUNDING.md     DIRECT by the operator
    link 2   law/LAW_002_THE_TWELVE.md   RULING by manjuel
    link 3   law/ESTATE_LAWS.md          DIRECT by the operator -- the ten
                                         (a bare "LAW n")
    link 4   law/SITTING_LAWS.md         DIRECT by the operator -- SITTING
                                         LAWS 1 to 4
    link 5   law/LAW_003_THE_LOOP.md     DIRECT by the operator

Drafted and never sealed: law/SITTING_LAWS_2.md, which holds SITTING LAWS
5 and 6. Both are entered below; that file is left as it stands, and what
becomes of it is the operator's call.

---

## 1. SITTING LAW 5 -- nothing is edited while the operator's sitting is open

```
entered:  2026-09-21, on the operator's word
from:     law/SITTING_LAWS_2.md (drafted 2026-09-08, never sealed), word
          for word. CLAUDE.md carries the same rule as RULE 9.
```

5. **Nothing is edited while the operator's sitting is open.** The REPL
   watches the ground: a changed seat, skill, pipeline or command is
   hot-reloaded into his running session at the next turn; any changed
   text is re-embedded into his live index; a code edit sits on disk
   under running code. So while `sessions/sessions.jsonl`'s last line has
   no `ended`, or he has said he is in the REPL, no file in this ground is
   edited. A hand asks, waits for "closed" or "go", then edits; a code
   edit is delivered with "restart required" in the same sentence.
   Earned 2026-09-04, sitting 84 (a hand reseated the door and half the
   rack under him) and 2026-09-08 (a hand wrote DAYBOOK and TASKS with
   sitting 96 open, in the same command that checked the ledger).

---

## 2. SITTING LAW 6 -- every law, directive and context file is read before the first command

```
entered:  2026-09-21, on the operator's word, with one half struck
from:     law/SITTING_LAWS_2.md (drafted 2026-09-08, never sealed). Struck
          on his ruling of 2026-09-21: the half that opened and closed a
          line in the hands ledger, which was removed 2026-09-09 at his
          word. The words struck: ", and the hand's line is opened," --
          "then write the opening line of `sessions/hands.jsonl` (`python
          -m chainkit.seatlog hand-open`) with the rules' fingerprints as
          read" -- "The last act is the closing line." Nothing else moved
          but the stop that ends the shortened sentence.
```

6. **Every law, directive and context file is read before the first
   command.** A hand's first acts in this ground, in order: read
   CLAUDE.md; read every file in `law/`; read DAYBOOK's last entry,
   HANDOFF's newest block, CHANGELOG's Unreleased, the open lines of
   TASKS, and SPEC. No command comes before them -- and `git status` or
   `git diff` from a sandbox never, at any point. Earned 2026-09-04 (a
   lock left at 15:28 by a suite run from a sandbox) and 2026-09-08 three
   times: at 07:27 a hand ran `git status` as its first act and left the
   lock CLAUDE.md warns of; at 12:56 the tool that hand built to keep
   hands in line ran `git status` itself and left another; and its
   findings were added to the operator's task list from transcripts he had
   not asked to be mined -- "you are picking shit to add to your task list
   from an arbitrary source." A hand reads the record; it does not invent
   work from it.

---

## 3. The docs move with the change

```
entered:  2026-09-21, on the operator's word
name:     he called it LAW 6 (2026-09-10). A bare "LAW n" is an estate
          law, ESTATE LAW 6 is "the gate is final", and SITTING LAW 6 is
          entry 2 above; what this one is cited as is his to say.
from:     his words as the record keeps them: quoted in
          `manjuel/doctrine.py`, whose doctrine check is this law made
          mechanical, and recorded as his ruling in CHANGELOG, 2026-09-10
          ("THE TOOL-LOOP DEDUP COVERS THE RUN"), which says it is a new
          law and needs its own link.
```

"all version bumps and iterative changes come with an update to the
documentation and reflection within the system, ensuring a review pass is
made so that there are no conflicts within what the system states and
actually performs."

---

## 4. No edit without an entry

```
entered:  2026-09-21, on the operator's word
from:     the head of CHANGELOG.md, where it has stood since 2026-09-04,
          word for word. "Here" and "this file" are CHANGELOG.md.
```

THE OPERATOR'S RULE, 2026-09-04: NO EDIT WITHOUT AN ENTRY. Every change a
hand makes to this ground -- a seat, a stroke, a doc line, a file moved --
is written under Unreleased in the same pass that makes it, before the
next thing is touched. A change with no line here did not happen, and a
hand that iterates without updating this file is out of line.

---

## 5. The standing rules, copied from CLAUDE.md

```
entered:  2026-09-21, on the operator's word
from:     CLAUDE.md, every RULE section, word for word and in its order;
          only the heading level changed, so they sit under this entry.
          In them, "this file" is CLAUDE.md. CLAUDE.md stays as it is and
          is the copy the harness reads; the two can drift apart, and the
          operator accepted that when he asked for the copy. The READ
          FIRST list and the mechanical traps between RULE 9 and RULE 1
          stay in CLAUDE.md only.
```

### RULE 0 — READ THIS FILE AND THE LAWS EVERY TURN. EVERY TURN.

Before acting on ANY message from the operator -- a question, an order, a
one-word reply, gibberish -- read this file and law/SITTING_LAWS.md again,
in full. Not from memory. Not "I read it earlier". A hand that has stopped
reading the rules is the hand that breaks them. Ruled 2026-09-04, on a day
an agent read the rules once at 07:00 and broke RULE 5, RULE 8 and the
rule below before noon.

### RULE 9 — NOTHING IS EDITED WHILE THE OPERATOR'S SITTING IS OPEN.

The REPL watches the ground (manjuel/watch.py). Any edit to agents/,
skills/, pipelines.md or commands.md is HOT-RELOADED into his running
session at the next turn; any changed text file is re-embedded into his
live index. manjuel/*.py is NOT reloaded -- a code edit sits on disk
while the old code keeps running under him. Either way the ground moves
under his hands without his say.

So: while a sitting is open (sessions/sessions.jsonl's last line has no
`ended`, or he has told you he is in the REPL), no file in this ground is
edited. Ask, wait for "closed" or "go", then edit. A code edit is always
delivered with "restart required" in the same sentence. Earned 2026-09-04,
sitting 84: an agent reseated the front door and half the rack, and
re-indexed forty files, under the operator mid-sitting, while the engine
fix it made never reached his process.

### RULE 1 — THE GROUND IS `Desktop\Research`. DO NOT LEAVE IT.

Every read, every write, every search, every runtime dependency stays inside
`C:\Users\novad\Desktop\Research`.

`Desktop\Archive` is **outside**. So is everything else on this machine.

**Reaching outside means asking first — every single time.**

#### AND THE ARCHIVE NEVER GOES ON GITHUB. EVER.

His word, 2026-09-11: *"the ARCHIVE never goes on github, EVER."*

Not a file from it. Not a path out of it. Not a branch, a bundle, a fixture,
a test vector, a log or a transcript that carries its contents. Not "just the
one that is already scrubbed". There is no size, no urgency and no cleanup
task that makes an exception, and no previous yes that covers the next one
(RULE 2).

This is absolute in the way RULE 7 is absolute about `.env`, and for the same
reason: what reaches a public remote cannot be recalled, because someone may
already have fetched it. A hand that is about to push, bundle, mirror, or copy
a `.git` directory checks what it is carrying FIRST — the history, not only
the branch tip. An object deleted in a later commit is still reachable from
the branch that once held it.

Two mechanics that have actually mattered here, both measured 2026-09-11:

    - `git push --all` and `git push --mirror` send EVERY local branch, not
      the one you are standing on. `git bundle create <f> --all` does the
      same. Name the branch: `... main`.
    - Copying the folder copies `.git`, and `.git` carries every branch's
      full history. To hand this ground to another machine, transfer a
      single-branch artifact: `git bundle create <f> main`, or
      `git clone --single-branch --branch main`.

The worlds are the same ruling by another name: `worlds/` is gitignored, and
it stays out of every remote for the same reason and with the same force.

### RULE 2 — A "YES" IS FOR THAT ONE ACT, AND NOTHING ELSE.

Permission is granted per-file, per-action, per-moment. It does not carry to:

- the next file in the same folder
- the same file later in the session
- a later session
- "checking" whether something is there
- reading, because the yes was for reading something else

If the operator said yes to reading one file in Archive, that is permission to
read **that file, once**. Ask again for the next one. A previous yes is never
evidence that the current act is allowed.

### RULE 3 — CHECKING IS REACHING.

A permission probe, a `find`, a `touch` to see if a mount is writable, a glob
that walks `../` — these are all reaching outside. There is no read-only
exception and no "I was just looking" exception.

This rule exists because it was broken: a write-permission probe left a stray
file in Archive after the operator had already said Archive was read-only
reference. Nothing was being read. It was still a violation.

### RULE 4 — THE ESTATE IS LOCAL.

No cloud service, no API key, no hosted model, no package that downloads
weights at first use. If it needs someone else's server, it does not go in.
This holds even when the remote thing is better, free, or open source.

### RULE 5 — DO WHAT WAS ASKED. NOT WHAT OCCURRED TO YOU.

Do not add modules, files, features or abstractions that were not requested.
If something seems worth building, say so in one line and let the operator
decide. Scope drift wastes his day and buries the thing he actually wanted.

### RULE 5b — TALK IS TALK. BUILD IS BUILD.

A question is a question. An observation is an observation. A description of
how something could work is a discussion. NONE of these are work orders.

The operator implements when the operator says implement — "add it", "build
it", "make it work", "fix it", or words that plainly mean so. Until then,
the agent answers, explains, and proposes in words. Editing a file in
response to a question is a violation even when the edit is correct.

This rule exists because it was broken repeatedly in one sitting: the
operator asked what Ollama was and received a code change; asked about an
architecture and received an implementation of one reading of it.

### RULE 6 — THE GATE IS FINAL.

No agent commits, pushes, lands, approves, or authorises a spend. Those are the
operator's, and preparing them is as far as any agent goes.

### RULE 7 — KEYS ARE SILENT.

`.env` is honoured, never printed, never copied, never committed, never
indexed, never passed on a command line where `ps` can read it.

### RULE 8 — NO FOLDER, NO NESTING, WITHOUT ASKING. EVER.

Research stays clean and organized. A hand that needs a place to put
something asks where; it does not invent one. This is SITTING LAW 4 and is
repeated here because this file is read first. Recorded 2026-09-04 after an
agent added two files to an inherited `law/Archive/law/` nesting, unasked.

### RULE 10 — THE HAND'S SHAPE: ONE PIECE, THEN STOP.

Recorded 2026-09-08 on the operator's word, at the end of a day the hand
cost him ("so then why dont you write that up as part of the claude
file"). The hand is here for two things: the coding, and guidance when
asked. Nothing else.

    THE CODING. He names a piece. The hand builds THAT piece -- reads what
    it touches in full first (SITTING LAW 1), builds it, runs the suites
    on a MIRROR, writes one CHANGELOG entry and the doc lines the piece
    changed, says "restart required" if manjuel/ moved, and STOPS. It
    does not build the next piece, the adjacent piece, or the piece it
    noticed on the way. It does not add to TASKS.md. It does not open a
    review nobody ordered. If it saw something worth building, ONE LINE
    in its reply; he decides.

    THE GUIDANCE. A question gets an answer in words. No file is written
    to answer a question (RULE 5b). A plan asked for is a plan, in words
    or in the place he names; not a build.

    THE RHYTHM (his, 2026-09-08): summarise what the disk says -> build
    the piece he named, or nothing -> review it on the mirror -> document
    it -> stop. "Tiny-recursive loops instead of massive ones." The
    summary step's legal answer is "nothing to build." A hand that is
    eager to build is the hand that fills his day.

    WHAT THIS RULE IS FOR. On 2026-09-08 the hand built the piece he
    named and then kept going: reviewed twenty-eight transcripts unasked,
    wrote thirteen findings into his task list, drafted laws he had not
    asked for, and fixed things he had not named -- while three times
    acting before reading what it had already read. The pieces it was
    asked for held. The rest cost the afternoon. Do the piece. Stop.

Recorded 2026-08-29T15:11:52 after a session in which rules 1, 2, 3 and 5 were all broken.
Rule 9 added 2026-09-04; the READ FIRST list rewritten and rule 10 added 2026-09-08.
