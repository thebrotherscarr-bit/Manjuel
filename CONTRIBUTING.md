# Contributing

## Run the suites first

    pip install ".[test]"   # the [test] extra is not optional for the
                           # strokes: one of them imports numpy outright.
    python tests/test_manjuel.py && python tests/smoke_cli.py
    python law/law.py verify
    python tests/buildmap.py            regenerate BUILDMAP.md after a code change
    python tests/standup.py             the seats, live -- read the report

Both suites are **offline and stubbed**: no rack, no network, no GPU, no
model. If a change makes them need a live model, that is the regression —
the offline property is a promise this project makes publicly, and CI runs
both on Windows and Ubuntu, Python 3.10 and 3.13, on every push.

`law.py verify` walks the hash-chained ledger. It is not in CI on purpose:
a fork with a re-terminated law file should fail on a real terminal, where
it means something, and not in a job that cannot tell tampering from a
checkout artifact.

## The rule that shapes everything else

**No agent lands anything.** Not a commit, not a memory entry, not a push,
not a config change. Agents prepare; a person lands. That is RULE 6 in
`CLAUDE.md` and LAW 6 in the ledger, and it is not a setting.

If a change would let Manjuel commit, approve, or write outside its
declared wall, it is not a feature with a flag — it is a different project.

## Every guard is named after the failure that earned it

Read `REFUSALS.md`. Twenty-six numbered refusals (plus 7b and 11b), each with the sitting number of the
run that produced it. That is the house style, and it is the contribution
standard:

- **Reproduce, then guard.** A stroke goes red BEFORE the fix, not after.
- **Stroke it both ways.** Every guard needs a case that fires and a case
  that must NOT. A guard proved only on what it refuses might refuse
  everything. Most bugs found in this repo were found that way.
- **Rewrite a superseded stroke, never delete it.** Note why it moved and
  keep the guard. See `test_the_chain_writes_declared_newlines` — the
  ruling reversed and the guard survived.
- **Report over gate, for anything that reads the corpus.** `logs/` grows
  every sitting, so an assertion over it goes red because someone used the
  CLI. `audit_record.py` and `manjuel/us.py` both report and exit 0.

## Name the wire — "what would go red if this came unplugged?"

This is RULE 11, and it is the section to read if you have written working
software and never been taught how the pieces are held together. It is the
least glamorous layer there is and it is where this estate's faults live.

**A wire** is one built thing connected to another so that breaking the
connection is LOUD. A module is not finished when it works. It is finished
when something would go red if it came unplugged. Ask that question of
anything you build, and if the answer is "nothing", you are not done.

### The three places a signal can arrive

Use the earliest one that will carry it. Each step later costs more and
depends on somebody remembering to run something.

**1 — write time.** You cannot even express the wrong thing. When the
engine's `Run` took a bare `model string` and grew a second head field, the
fix was a `Head` TYPE rather than a sixth argument: the compiler then
pointed at every call site by itself. Nobody had to remember them.

**2 — run time.** The wrong thing is expressible and refused the moment it
is attempted. `skills.py`'s clearance check — a seat asks for `write_file`
and is told *"not cleared to call"*. The law gate. The LAW 8 path jail.

**3 — check time.** The wrong thing happens and something later says so.
`manjuel/us.py`, `tests/buildmap.py --check`, `tests/release.py --check`.

A comment is a fourth tier and it is not wiring at all.

### A convention is not a wire

This is the one to internalise, because every fault the 2026-09-24 review
turned up was the same shape: **a convention doing a type's job.**

| the fault | the convention holding it |
|---|---|
| `inspect`'s LAW 9 and SITTING LAW 2 refusals vanish from the delivery, read as a success on the wire, AND prime the drift checker | a refusal must begin with the word `Refused` |
| the same test copied into six places, one of them missing a word | the six copies match |
| every tool's arguments published as required | "optional" means one `?` — and the reader wanted two |
| the Proofreader never woke, for weeks, green the whole time | `Wakes On:` names a flag something raises |

None of those is a typo. Each is a rule held in a person's head and checked
by nothing. `inspect`'s refusal would need no convention at all if there
were one function that built the prefix: you could not write an invisible
refusal, because you could not write a refusal without going through the
thing that makes it visible.

### One source per fact

Cohesion is not correctness; it is **one place holding each fact, and
everything else derived from it.** That is already this ground's second
architecture rule — *the record is the truth, everything else is
`fold(record)`* — and `BUILDMAP.md` and `rack.md` are two working examples.
Three catalogues of the same gates, two copies of one helper, six copies of
one tuple: none of those is a bug today, and copies always drift.

### LOOSE

`us.py`'s third finding, beside GAP and DRIFT: **declared, correct, and read
by nothing.** A GAP and a DRIFT each have two sides that disagree, so either
side can raise them. A LOOSE agrees with everything — right vocabulary,
right spelling, file present — and moves nothing. It gates a tag, because a
declaration nobody reads is a promise and this ground does not ship
promises.

### The four that earned this section, all in one week

Each was a piece the operator named, built correctly, proved by reversal,
and written into the CHANGELOG. Each was connected to nothing:

- `cli.py`, `registry.py` and `serve.py` moved; `BUILDMAP.md` is generated
  FROM them and was never regenerated. `buildmap --check` is in CI.
- the flags check surfaced a real fault; the STROKE was taught to allow for
  it and the release GATE, reading the same report, was not — so the gate
  went red and nothing said so, because it is deferred at boot and absent
  from CI.
- `flow_run` learned to name a model; `run_start`, one layer down, did not.
- a doc line the record itself said to fix *"when serve.py is next
  touched"* — touched twice that week, read by nobody.

Not carelessness. **Nothing connected "you moved `cli.py`" to "regenerate
the map."** That sentence is the whole of what this section is about, and
`RULE 10` is why it is easy to miss: a seam is never the piece that was
named, so under Rule 10 alone the wire is invisible by construction.

## Adding a skill

1. `skills/<name>.md` — Action Keyword, Description, Parameters Needed.
   Parameters Needed may only name `content` and `filepath`: the Router
   answers in three tags and there is no fourth, so an argument outside those
   is offered to a model that has no way to send it. A stroke refuses it.
2. A handler in `manjuel/skills.py`, registered with `@skill("<name>")`.
3. **A record in `us/manjuel.us`** declaring what it may reach: `wall`,
   `writes`, `remote`. Write `wall` by reading your own handler; do not
   infer it. `python -m manjuel.us` will tell you if you skipped this.
4. A stroke that executes it.

Startup refuses, by name, a skill file with no handler and a pipeline
naming a seat no file declares. It will tell you which.

## Adding a hook

A hook is a skill that declares WHEN it fires. One more line in its own
markdown, read by the same parser as `**Says:**` and `**Takes:**`:

    - **Hooks:** before_tool | after_tool

Those two points are the whole set. A point the engine does not fire is
dropped rather than installed — startup names it, because a hook that looks
installed and never runs is worse than one that is refused.

The hook is handed the action it is firing around as `<content>`, and then:

- **it cannot change the answer.** Its return value is discarded. A hook that
  could rewrite a tool's result would be testimony becoming fact (LAW 5).
- **it cannot fire a hook.** While one runs, calls take the plain path. An
  unbounded tree is what LAW 7 exists to refuse.
- **it cannot take the turn down.** A broken hook is named on the library, not
  raised into the run.

With nothing declaring `**Hooks:**`, the engine behaves exactly as it did
before hooks existed — which is why landing them moved no stroke.

## Adding a seat

`agents/<name>.md` declares model, stage, on-fail, when, context, timeout, voice, prompt —
and `May Call` if it holds tools. A seat with no `May Call` holds none: it
reads nothing, writes nothing, reaches nothing. That is most of the roster
and it is deliberate.

Then `us/chain_<name>.us`. `permission` is **derived** from `May Call` plus
each named skill's wall — never written beside it. Writing it separately is
how the Router came to declare `read: agent_workspace only` while cleared
for `all`.

## The toll

At the end of a sitting the REPL offers a toll into `SEAT_LOG.md`. The
observed half — runs, stages, timings, git state — is machine-written. The
judgment half (`WHAT PROVED / IS THIN / IS OWED`) is yours and is never
generated.

**Not paying it is a legitimate outcome.** A sitting that closes without a
toll gets an honest entry saying the judgment was never stated, rather than
an invented one. Nothing is blocked by an unpaid toll. Pay it when you have
something to say; the record is worth more when it is not padded.

## Platform

Windows-first. `manjuel/voice.py` (SAPI out, whisper.cpp in) and parts of
`registry.py` are Windows-bound, and `bin/` carries Windows binaries.

**Voice degrades alone.** `boot.py` reports GROUND / RACK / RECORD / GATE /
VOICE separately, so a machine with no voice boots, says so, and runs
everything else. The suites do not need it. Nothing else is platform-bound.

## What this project will not take

- A listening socket, a chat-platform bridge, or an always-on daemon. The
  comparable systems' exposure findings all require one; this binds nothing
  and serves nothing, and that is the position rather than a gap.
- A model that writes its own seat prompts, commit subjects, or memory
  entries. Models propose into a pending file; a person lands.
- A dependency. There is one. Adding a second needs an argument.
