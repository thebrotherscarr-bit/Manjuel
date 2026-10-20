# Last run

- **smoke** — 72/72 GREEN, 2026-10-20 11:47
- **strokes** — 4273/4283 RED, 2026-10-20 11:51

## strokes — 10 failed

### the run is routed to the decomposer first

`tests/strokes` — **test_several_acts_get_a_route_first:9491**

```
git_commit
```

### and the record says why it was decomposed

`tests/strokes` — **test_several_acts_get_a_route_first:9493**

```
(no detail reported)
```

### his rule: classify_sentiment by the PPMI reader: 'classify the sentiment of this feedb'

`tests/strokes` — **test_manjuel_reads_the_request:10919**

```
'classify_sentiment' '' False
```

### his rule: statistics by the PPMI reader: 'what are the mean, median and standa'

`tests/strokes` — **test_manjuel_reads_the_request:10919**

```
'statistics' '' False
```

### his rule: no tool by his words: 'propose a note for later sessions: t'

`tests/strokes` — **test_manjuel_reads_the_request:10919**

```
'remember' '' False
```

### in a turn, the reader's pick is the tool, chosen by the PPMI reader and said so

`tests/strokes` — **test_manjuel_reads_the_request:10936**

```
'skill_search' 'asks_about_a_tool' ['law: no ledger in this ground -- gate ran on the rules alone; objective passed 4 checks', 'intent: this ASKS ABOUT `statistics` rather than asking for it -- `skill_search` reads its declaration; `statistics` itself is NOT run', 'intent: `skill_search` chosen by asks_about_a_tool -- Router woken di
```

### ... the reading in the record, its score and the next best

`tests/strokes` — **test_manjuel_reads_the_request:10940**

```
['law: no ledger in this ground -- gate ran on the rules alone; objective passed 4 checks', 'intent: this ASKS ABOUT `statistics` rather than asking for it -- `skill_search` reads its declaration; `statistics` itself is NOT run', 'intent: `skill_search` chosen by asks_about_a_tool -- Router woken di
```

### a write the reader reads names no tool and wakes the Router to decide it

`tests/strokes` — **test_manjuel_reads_the_request:10946**

```
'remember' ['needs_tool', 'worked'] ['law: no ledger in this ground -- gate ran on the rules alone; objective passed 4 checks', "deadline: 0.0s at the card do not count -- the turn's clock stood still while it waited", 'intent: not sure between remember, when -- no answer at the card, so the best match, `remember`', 'intent: objective
```

### on a follow-up the reader's pick is withdrawn like any guess, and the door answers

`tests/strokes` — **test_manjuel_reads_the_request:10953**

```
'statistics' ['law: no ledger in this ground -- gate ran on the rules alone; objective passed 4 checks', 'intent: objective names `statistics` -- Router woken directly', 'level: Steward', 'intent: a follow-up -- the door is kept in front of the Router', "recompose: the named tool `statistics`, which did not run
```

### is_big_objective is credited with choosing `decompose_task`: 'read the rack, then write a no'

`tests/strokes` — **test_every_branch_that_chooses_a_tool_says_so:12269**

```
k stood still while it waited || rack: his words ask for the Reasoner (hard) -- no answer at the card, so it was not woken || recompose: the named tool `git_commit`, which did not run appended to the delivery; the closing seat's words were not the whole record
```

