# HARNESS STUDY

Seven open-source harnesses read against Manjuel and Steward, function by function, so Steward can run a job set and
forget inside a harness that is already proven, local and subscription free. WHAT'S LEFT H33, on your cards of
2026-10-20 ("Pause v0.2.6, study first", "Shallow clones, gitignored", "Source first, REA on your builds", "Adopt the
model-chooses loop") and of 2026-10-21: "not just that part, but ALL of the functionality of them"; v0.2.6 is "the
capabilities and functions part"; "Capability page first"; approval modes "Both, chosen per job"; Pi, oh-my-pi and
Hermes cloned; OpenClaw "just the parity ... diff it with REA"; I2's open pieces carried to v0.2.7; and your REA Studio
(`agent_workspace/`), "diff that as well".

How it was read: shallow clones at the tip of 2026-10-21 in `worlds/harnesses/` (gitignored, never sent); OpenClaw from
its published package (`openclaw` 2026.10.5, unpacked, nothing of it run) with REA 6.7.0's static analysis of its 21
core files beside it; eight read-only readers, one per harness and one for this ground; then seven more that tried to
refute every claim on this page against the source -- what did not survive is gone, and what was only partly true says
so. Each section ends with **Where**: the files it was read from (each harness's paths are under its own clone).

| Harness | What it is | Source |
|---|---|---|
| opencode | a coding agent; client and server; its harness in `packages/core` (v2), Effect, SQLite sessions | anomalyco/opencode |
| Cline | a coding agent turned SDK (`sdk/packages`), with a CLI, a hub daemon, VS Code as a thin host | cline/cline |
| OpenShell | NVIDIA's cage for someone else's agent: gateway, supervisor, sandbox, policy prover; an outer loop script, no model loop | NVIDIA/OpenShell |
| Pi | a small agent core with the coding tools beside it and extensions around it; TUI, print, JSON and RPC modes | earendil-works/pi |
| oh-my-pi | Pi forked and filled in: approval modes, sub-agents, memory, owned tool-call dialects, a Rust core | can1357/oh-my-pi |
| Hermes | Python; one agent core behind a CLI, desktop, web, editors, an API and about two dozen messaging adapters; learns skills | NousResearch/hermes-agent |
| OpenClaw | a gateway that owns chat channels, with its own embedded agent runtime (built on Pi) and plug-in harnesses | openclaw 2026.10.5 (npm) |
| REA Studio | your app: a browser reverse-engineering workbench with a local Ollama copilot (Vite, React) | your `agent_workspace/` |
| Manjuel and Steward | the ordinary turn (`run_pipeline`) and the driver (`/drive`, H31), the door and the glass | this ground |

---

## The short answer

Steward already has the right spine: the model chooses its tools, a check -- never the model -- says done, each job
works on a line of work that git can drop, and the walls stand around every skill. What all of these harnesses have and
Steward lacks is what lets a job run with nobody watching: an approval you give once for a whole job, calls and edits
repaired instead of fatal, a counter that stops a loop, a window that compacts, a job that survives a crash, the rules
and memory in its prompt, and its own model's tool-call form. One more, found on the way: `/drive` goes around the law
gate, the gibberish and injection gates and the Guardian that every ordinary turn passes through.

---

## 1. Approvals, and how many clicks a job costs (v0.2.6 piece 2)

- **OpenShell.** The best binding, for its network rules: an approval is a hash of exactly what was reviewed -- the rule,
  the policy now, the policy after, the keys involved -- and a stale one fails and must be fetched again. Its batch
  approval checks every pending rule against one snapshot and writes once, skipping anything flagged, stale or in
  conflict. A rejection carries your reason back to the agent, which revises and asks again. Manual by default.
- **opencode.** Allow, ask or deny per action and pattern, the last match winning; a deny always wins over a saved
  "always". "Always" saves a pattern and at once settles every other waiting ask it covers -- careful: for edits the
  pattern is everything, so one "always" allows every edit in the project for good. A reject with a message is feedback.
  Run with nobody at the screen, it rejects every ask unless told otherwise. A plugin hook can decide any ask.
- **Hermes.** Manual, smart or off; once, session or always. Floors hold even with everything off: deny patterns,
  protected instruction files, and deny by default when nobody is watching (cron, unattended); no answer in 300 seconds
  is a no. "Smart" judges only commands already flagged dangerous.
- **OpenClaw.** Exec modes deny, allowlist, ask, auto (a reviewer model; three denials go to a human) and full -- full is
  its default. An "always" is bound to the exact command and folder, and the program's hash and folder are checked again
  just before it runs. A cron job gets a standing grant bound to the job, command, folder and environment, which can
  expire. Approvals can be answered from a chat app; a typed "yes" never counts.
- **Cline.** Per tool, enabled and auto-approve (both on unless set); act, plan, yolo, zen; a task's approval is tied to
  one revision and goes stale when it is edited. Its approval channel for another process is a request file and a
  decision file, denied after five minutes. Its schedules run in yolo unless set.
- **oh-my-pi.** Always-ask, cached grants per file or folder, write, yolo (its default); per tool allow, prompt or deny;
  critical shell patterns always ask -- but its sub-agents always run in yolo.
- **Pi.** None built in, by design; an extension that answers "block" stops a call, and one that throws does too.
- **Steward.** Every write is its own red card showing the arguments cut to 120 characters, with no diff; the card waits
  with no bound, and an unattended `/drive` would wait forever. Plan and each already have one run card listing the
  items and the check, and one ship card covers commit, push, pull request and CI -- but the writes still ask one by one.
  An 11-call job is 11 write cards, then the ship card, the merge card and "What is next?".

**The gap:** one card for a job. Your ruling, "Both, chosen per job": a **plan card** -- the job's passages, files and
check shown whole with their diffs, bound by a hash of exactly that (OpenShell's idea, OpenClaw's re-check before it
runs), so a call that matches runs without a card and anything else parks; a stale plan is refused -- or **line-auto**,
chosen when you send the job: every write on its line of work runs, and git is the net. In both: the floors hold
(secrets, protected files, main, client material), the check is shown on the card before it runs, a card with no answer
is a no after a bound, and the send and the merge stay yours (RULE 12).

**Where:** OpenShell `crates/openshell-server/src/grpc/policy.rs`, `proto/openshell.proto`; opencode
`packages/core/src/permission.ts`, `permission/saved.ts`, `packages/cli/src/run/noninteractive.ts`; Hermes
`tools/approval_context.py`, `tools/approval_floors.py`; OpenClaw `docs/tools/exec-approvals.md`,
`dist/bash-tools.exec-runtime-*.mjs`; Cline `sdk/packages/shared/src/llms/tools.ts`,
`sdk/packages/core/src/tasks/agenda-task-manager.ts`, `sdk/packages/core/src/runtime/tools/tool-approval.ts`; oh-my-pi
`packages/coding-agent/src/tools/approval.ts`, `docs/tools/task.md`; Steward `manjuel/serve.py` (`drive_act`,
`_drive_brief`, `Door.ask`, `drive_items`, `drive_ship`).

## 2. A bad call, a bad edit, a loop (v0.2.6 piece 3)

- **Repairing a call.** Broken JSON mended: Cline (a full repair pass), oh-my-pi (up to three characters), Pi (inside
  strings only). Types mended against the schema -- "20" into 20, a string into a list: opencode, Hermes, Pi, oh-my-pi.
  A wrong tool name matched to the nearest: Hermes, oh-my-pi. A tool call written as plain text -- harmony and two other
  forms -- turned into a real call only when the name matches a real tool exactly: OpenClaw. The refusal echoes what was
  received (Pi names each bad field). A call cut off by the length limit is refused, never run: Pi, Hermes, opencode.
- **Matching an edit.** opencode: exact, then plain quotes, dashes and spaces, then trailing spaces -- the three tiers
  are about 60 lines. Pi and OpenClaw: exact, then a forgiving match spliced into the original, several edits per call.
  Hermes: nine strategies; a write refused if the file changed since it was read. OpenClaw, on a miss: the three closest
  lines, where they differ, and the file's own text -- and every write read back and checked byte for byte.
- **Stopping a loop.** Cline: the same call three times warns, five forces its failure limit; a turn where every call
  failed counts (6, or 3 in its CLI). Hermes: an identical streak of three, a cycle of up to four, counters that halt at
  5, 8 and 5 -- on when nobody is watching. OpenClaw: three identical tool errors in a row end the turn, always.
  oh-my-pi: five identical calls redirect it. Pi and opencode: none.
- **When the model call fails.** Retries with backoff everywhere (opencode 10, oh-my-pi 10, Hermes 3 then fallbacks then
  five timed cycles, Pi 3, Cline in three layers); an output cut off continued ("break it into smaller pieces").
- **Steward.** Arguments that fail to parse become `{"content": raw}`, and a call with no name is dropped without a word;
  an edit must match exactly once (line endings aside, and a `.py` must still parse); the driver counts nothing; a failed
  model call -- a malformed call among them (C126) -- ends the job, and in plan or each the whole run. The ordinary turn
  already refuses an identical call and stops at the second repeat.

**The gap:** repair with a named refusal; opencode's three tiers and OpenClaw's on-a-miss help; the ordinary turn's
repeat refusal and Cline's failed-turn counter carried into the driver, with a card at the limit; a retry on a failed
model call; a length-cut call refused.

**Where:** Cline `sdk/packages/shared/src/parse/json.ts`, `sdk/packages/core/src/runtime/safety/`; oh-my-pi
`packages/ai/src/utils/validation.ts`, `packages/ai/src/utils/tool-call-loop-guard.ts`; Pi `packages/ai/src/utils/`,
`packages/coding-agent/src/core/tools/edit-diff.ts`; opencode `packages/core/src/plugin/tool-input-repair.ts`,
`packages/core/src/tool/plugin/edit.ts`, `packages/core/src/session/runner/publish-llm-event.ts`; Hermes
`agent/turn_tool_validation.py`, `tools/arg_coercion.py`, `tools/fuzzy_match.py`, `agent/tool_guardrails.py`; OpenClaw
`dist/tools-*.mjs` (edit), `dist/tool-loop-detection-*.mjs`; Steward `manjuel/serve.py` (`drive_calls`, `_drive_job`),
`manjuel/skills.py` (`_apply_passage`), `manjuel/pipeline.py` (the tool loop's repeat refusal).

## 3. The model, and calls in its own tongue (v0.2.6 piece 4)

- **oh-my-pi.** Eleven owned tool-call dialects -- harmony (gpt-oss's own form), hermes, qwen3, xml and more -- 6,477
  lines: the tools are taken out of the request, a catalogue and the dialect's guide go into the prompt, the history is
  re-encoded, and a scanner turns the model's text back into real calls (harmony's is a 341-line state machine), aborting
  if the model starts writing its own tool result and escaping the dialect's tokens in untrusted text. It switches on
  only when a model is marked as having no tools, or when you choose it; for gpt-oss on Ollama it stays native.
- **OpenClaw.** The lighter version: a plain-text call in harmony or two other forms promoted to a real call only when
  its name is a real tool.
- **Hermes.** A managed llama.cpp sized to free VRAM and restarted on a crash; Ollama's window read so it is never left
  at 2,048.
- **Cline and opencode.** Ollama's own endpoint with the window set (Cline from the model's record; opencode reads the
  model's trained maximum from Ollama), 300 seconds allowed for a cold load (Cline).
- **Steward.** Ollama's native tools only; the window 16,384 unless set, never read from the model or the rack; the front
  Steward seat (llama3.2) and the driver (qwen3.5:9b) are two different models.

**The gap:** the "jsonify" you named -- a dialect layer Steward chooses per model, native first and harmony (or another)
when a model's native calls fail it, measured, not assumed; the window from the model and the rack (H34 knows the card);
one Steward, gpt-oss:20b measured against qwen3.5:9b first (SITTING LAW 3).

**Where:** oh-my-pi `packages/ai/src/dialect/`, `packages/catalog/src/identity/dialect.ts`,
`packages/ai/src/utils/harmony-leak.ts`, `docs/toolconv/`; OpenClaw `dist/src-*.mjs`, `dist/grammar-*.mjs`
(tool-call repair); Hermes `hermes_cli/local_runtime/`, `agent/agent_init_ollama.py`; Cline
`sdk/packages/llms/src/providers/vendors/ollama.ts`; opencode `packages/core/src/plugin/provider/ollama.ts`; Steward
`manjuel/serve.py` (`DRIVE_MODEL`, `DRIVE_CONTEXT`), `agents/steward.md`.

## 4. Context, and a full window (v0.2.6 piece 5)

- **Compaction.** opencode: at the window less 15 per cent (16,000 above a 32k window), a summary in a fixed form --
  objective, requirements, decisions, where the work stands, the next move, the files -- the newest 15,000 tokens kept;
  told the request is too long, it shrinks to 70, 50, then 35 per cent. Pi and OpenClaw: 16,384 held back, 20,000 kept,
  never cut at a tool result; OpenClaw writes memory down first and falls back to a summary-free cut if the summary times
  out. Cline: at nine-tenths, a summary by the same model, or a plain cut that must come out smaller. Hermes: old tool
  output pruned with no model first, then a summary (for a local window, at 75 per cent). oh-my-pi: a model-free shake
  first.
- **Big results.** Cut, the whole saved to a file, and the cut says where (opencode, Hermes, oh-my-pi, Pi's shell
  output); Cline keeps them in memory behind a link the model can read.
- **Few tools in the prompt.** Tools searched for instead of all listed (Pi, Hermes, OpenClaw -- on by itself for local
  models, with a lean set that drops the heaviest tools -- and opencode's code mode).
- **Rules and memory in the prompt.** AGENTS.md and its kin read up the tree (all of them); Hermes and OpenClaw add their
  MEMORY.md and USER.md, capped and frozen at the start so the cache holds.
- **Steward.** The history only grows in 16,384 (a skill file is added whole on first use); each result, a failed check's
  output among them, is cut at 4,000 characters; 3,000 characters carried between jobs; no laws, standing, story or
  landed memory in its prompt.

**The gap:** a model-free cut first, then a summary in opencode's form; results saved whole with the place named and the
read-on line first; the laws, the standing and the landed memory in the driver's prompt.

**Where:** opencode `packages/core/src/session/compaction.ts`, `packages/core/src/tool-output.ts`; Pi
`packages/coding-agent/src/core/compaction/compaction.ts`; OpenClaw `docs/concepts/compaction.md`,
`dist/agent-core-*.mjs`; Cline `sdk/packages/core/src/extensions/context/compaction.ts`; Hermes
`agent/context_compressor.py`, `tools/tool_result_storage.py`; oh-my-pi `packages/agent/src/compaction/shake.ts`;
Steward `manjuel/serve.py` (`_drive_job`, `DRIVE_*`).

## 5. A job that survives, and an undo (v0.2.6 pieces 3 and 5)

- **opencode.** Every prompt stored before it runs, every turn claimed as it starts; after a crash it resumes ("server
  restarted, continue"), up to ten times a turn -- at least once, so a side effect can repeat; background jobs recovered;
  a shadow git snapshot at the start and end of every step, and a revert.
- **Pi.** An experimental runtime (`pi-durable`) that saves the conversation, each turn and each call before anything is
  shown, and resumes unfinished work after a crash.
- **OpenClaw.** The main session resumes after a restart, always; a writer claim keeps a stale run from committing.
- **oh-my-pi.** A broken turn recovered up to three times; each task in its own copy-on-write copy of the folder (on
  Windows, ProjFS or a git worktree) whose result comes back as a diff -- an undo scoped to the job.
- **Cline and Hermes.** A checkpoint before a run's first write (Cline under its own git refs; Hermes in a shadow git) --
  each off unless set. Hermes keeps its background processes in a file for crash recovery.
- **Steward.** The job and its put-back bytes live only in memory, and its transcript is written only at the end; but
  each item of an each run is written down as it goes, and a passing item's commit stays on its line. The door's holds
  are logged but never reloaded after a restart.

**The gap:** the job written down as it goes -- each call, each card, the put-back bytes -- so a restart resumes it; the
line of work stays the undo.

**Where:** opencode `packages/core/src/session/execution/restart.ts`, `packages/core/src/snapshot.ts`,
`packages/core/src/session/revert.ts`; Pi `packages/durable/`; OpenClaw `docs/gateway/restart-recovery.md`; oh-my-pi
`crates/pi-iso/src/lib.rs`, `packages/coding-agent/src/session/turn-recovery.ts`; Cline
`sdk/packages/core/src/hooks/checkpoint-hooks.ts`; Hermes `tools/checkpoint_manager.py`, `tools/process_registry.py`;
Steward `manjuel/serve.py` (`Drive`, `drive_record`, `_drive_ignore`), atlas `line/internal/tools/holds.go`.

## 6. Sub-agents, and Steward as the face (v0.2.6 piece 7)

- **OpenClaw.** `sessions_spawn`: a child as its own session, its context isolated or forked, its own git worktree, five
  levels and eight at once; the child reports back up the chain.
- **Hermes.** `delegate_task`, one or a batch, ten at once, one level; a leaf may not delegate; a child in the background
  returns as a new turn; each child may get its own worktree.
- **oh-my-pi.** A `task` tool, a batch with a shared context, typed results, two levels, a request budget per child that
  stops it at one and a half times; bundled scout, reviewer and security-reviewer agents.
- **Cline.** `spawn_agent`, configured agents as markdown files each with its own model, and agent teams.
- **opencode.** A `subagent` tool, one level unless set, foreground or background, its own model, continued by its id.
- **Steward.** The council's seats sit in turn on an ordinary turn; the driver has no delegate tool, though `mcp_call` can
  reach the door's `seat_ask`, `run_start` and `flow_run` behind a card and a hold.

**The gap:** Steward calls the council's seats as his sub-agents -- a seat as a tool, its own model, a typed result -- one
at a time on one GPU, under the same approval mode as the job (oh-my-pi's children run in yolo; ours must not).

**Where:** OpenClaw `docs/tools/subagents/`, `dist/agent-limits-*.mjs`; Hermes `tools/delegate_tool_config.py`; oh-my-pi
`docs/tools/task.md`; Cline `sdk/packages/core/src/extensions/tools/team/`; opencode
`packages/core/src/tool/plugin/subagent.ts`; Manjuel `manjuel/pipeline.py`, `agents/*.md`, atlas
`line/internal/tools/tools.go`.

## 7. New skills, tools and connectors made native (v0.2.6 pieces 6 and 8)

- **One skill form for all.** `SKILL.md` -- Pi, opencode, Cline, Hermes, oh-my-pi and OpenClaw read the same files. A
  skill is listed by name and read whole only when used.
- **Hot reload.** opencode watches its skill, agent, command and plugin folders; Cline its skills, rules and workflows: a
  dropped file is native at once.
- **MCP.** Every coding harness here is an MCP client, over stdio and HTTP. OpenClaw also serves its tools to other
  agents over loopback, running its own approval chain on every call. REA is an MCP server over stdio.
- **Learning.** Hermes: every ten turns a background fork reviews the work and patches or writes skills; a curator
  archives stale ones, never deletes. OpenClaw: the same, on by default, every change undoable, and anything read from
  the network marks the turn untrusted for memory. oh-my-pi: a pipeline over past sessions writes a memory summary and
  new skills.
- **Steward.** Skills as markdown with their own phrases, a skill file read whole on first use (H32); `skill_report`
  already hands back how each tool was used; the door serves MCP but calls no outside MCP server, and `mcp_call` speaks
  HTTP to loopback only -- no stdio.

**The gap:** REA (and any stdio MCP server) callable through the door on your word; what was learned staged for your hand
to land (Hermes can stage memory and skill writes the same way; off by default there).

**Where:** Hermes `agent/background_review.py`, `agent/curator.py`, `tools/write_approval.py`; OpenClaw
`docs/tools/self-learning.md`, `dist/mcp-http.handlers-*.mjs`; oh-my-pi `docs/memory.md`; opencode
`packages/core/src/config/watch.ts`; Cline `sdk/packages/core/src/extensions/config/`; Manjuel `manjuel/skills.py`
(`_mcp_call`, `_skill_report`), atlas `line/internal/protocol/`.

## 8. Long jobs, schedules, and a done that is proved (after v0.2.6, unless you rule it in)

- **Hermes.** `/goal`: shell checks must pass before a judge may call it done -- our check, by another name; cron with a
  watchdog; background processes that report when they end.
- **OpenClaw.** Goals with a budget that may be called blocked only after the same blocker three turns running; cron,
  heartbeats, and a background command that wakes the agent when it ends; a 48-hour budget that pauses while a card waits.
- **oh-my-pi.** `/loop --until 'tests pass'`.
- **Cline.** A cron and event runner with leases, reports and a notes folder carried between runs.
- **OpenShell.** An outer loop where every cycle ends with a result line -- complete, waiting, blocked, a passing failure,
  a final one -- with backoff, a heartbeat, and its state written to a file.
- **Steward.** The check is the done; a goal job with no check is accepted "unchecked" and never committed; no schedule;
  `/drive` lives in one turn of the glass.

**Where:** Hermes `hermes_cli/goals.py`, `cron/`; OpenClaw `docs/tools/goal.md`, `docs/automation/cron-jobs.md`; oh-my-pi
`packages/coding-agent/src/modes/loop-limit.ts`; Cline `sdk/packages/core/src/cron/`; OpenShell
`scripts/agents/runtime/supervisor.sh`; Steward `manjuel/serve.py` (`DRIVE_SAID`).

## 9. The rails

- **OpenShell** is the only real cage: kernel-enforced on Linux, every network call checked per program, keys replaced
  by placeholders the agent never sees. On Windows its native form is "coming soon" and needs an Insider build of
  26300.8553 or later -- this machine is 26200 -- and lacks process rules; WSL 2 is experimental.
- **Hermes and OpenClaw** can run commands in containers with the network off; both scrub keys from the environment.
- **opencode, Cline, Pi, oh-my-pi** have no sandbox; their gates are permissions, or (Pi) extensions.
- **Steward.** Walls on every skill, a jailed `run_python`, never-written paths -- but `/drive` is handed to the driver
  before the ordinary turn's gibberish gate, law gate and Guardian, and its check runs unguarded.

**The gap:** the driver inside the same rails as the ordinary turn: the law gate on its goal and its writes, the check
shown before it runs.

**Where:** OpenShell `crates/openshell-sandbox/`, `crates/openshell-driver-mxc/README.md`, `docs/about/support-matrix.mdx`;
Hermes `tools/environments/local_env_policy.py`; OpenClaw `docs/gateway/sandboxing.md`; Steward `manjuel/serve.py`
(`Door.turn`, `drive_check`), `manjuel/pipeline.py`, `manjuel/lawgate.py`.

## 10. REA Studio

- **What it is.** A browser app, no server: a target list, a disassembly and trace view, and an Ollama copilot panel.
- **The Ollama agent.** One streamed `/api/chat` call to the local rack -- the system prompt, the history, temperature and
  `num_ctx` -- with no tools, no JSON mode and no loop; a reasoning model's `<think>` text is pulled out by hand and shown
  in a box you can open. Its setup pings `/api/tags`, lists the models, and sets the window (2,048 to 65,536) and the
  temperature.
- **What is real and what is not.** The file triage is real: entropy, the file type from its first bytes (ELF, WASM,
  Mach-O, PE, ZIP), printable strings sorted into URLs, secrets, crypto, paths and errors. The rest is staged: the
  `rea_*` MCP tools its prompt names do not exist, the five targets are hand-written fixtures, the sections of an imported
  file are invented from its size, and the REA command line is a toy that formats the fixtures. And when the call to
  Ollama fails, it says nothing: it streams a canned answer instead (`streamOllamaChat`, lines 187-193). The Gemini mode
  in its settings is not wired to anything; its page loads Google Fonts.
- **Steward.** Already has the real version of its agent: Ollama's chat with tools and streaming, a loop, cards, VRAM
  planning, and a refusal -- never an invented answer -- when a model fails. Neither has Ollama's own JSON mode:
  Steward still scrapes a plan's JSON out of prose.

**Worth taking:** the triage (about 120 lines of Python, a new read-only skill beside `inspect`, piece 8 and the REA
work of piece 6); the shape of its prompt -- the target's facts and first strings in a compact block -- for a
reverse-engineering seat; Ollama's `format` (JSON or a schema) in `runtime.chat`, so a plan and a call's arguments come
back as JSON by construction (piece 4's "jsonify"); and, if the glass ever shows reasoning, its collapsible box.
**Not taken:** the silent fallback to a canned answer -- the one thing our runtime exists to refuse -- and the invented
data.

**Where:** your `agent_workspace/rea-studio-—-reverse-engineer-anything-(ollama-desktop)/`: `src/utils/ollamaClient.ts`
(`streamOllamaChat`, `simulateReaResponse`), `src/utils/reaEngine.ts` (`buildOllamaSystemPrompt`),
`src/utils/binaryParser.ts`, `src/components/OllamaAgentPanel.tsx`, `src/components/OllamaConfigModal.tsx`; Steward
`manjuel/runtime.py` (`OllamaRuntime.chat`, `thinking_of`), `manjuel/serve.py` (`drive_plan`, `drive_calls`).

## 11. Not taken

- Anything that calls home: Pi's install ping and version check, OpenShell's anonymous telemetry, oh-my-pi's report filer,
  update check and telemetry export, Cline's telemetry, OpenClaw's daily version check (which records where it came from)
  and its node hosts' auto-update -- each on by default there, each off here (RULE 4).
- Cloud sessions, hosted routers and messaging gateways for now: the estate is local; messaging out already exists at
  the door.
- Allow-everything defaults: oh-my-pi's yolo and its yolo children, opencode's build agent, OpenClaw's full exec, Cline's
  yolo schedules; and opencode's ungated network inside code mode.

---

## The full feature list, against Steward (2026-10-21, his word: "diff the full feature list ... and add them")

Every feature the eight readers and seven verifiers found in opencode (oc), Cline (cl), OpenShell (os), Pi (pi),
oh-my-pi (omp), Hermes (he), OpenClaw (ocw) and REA Studio (rs), against Steward as he stands on 2026-10-21. HAVE:
built and proved. BUILD: built in this pass. NOT TAKEN: refused, with the reason.

| # | Feature | Who has it | Steward |
|---|---|---|---|
| 1 | The model chooses its tools in a loop | all but os | HAVE (/drive, the face) |
| 2 | A check, not the model, decides done | he (/goal), omp (goal audit), cl (submit verified) | HAVE |
| 3 | One approval for a whole job | os (batch), oc (always settles), he (batch ahead) | HAVE (plan card, auto, ask) |
| 4 | An "always" for the rest of the sitting | oc, he, omp, ocw | BUILD (`always` on a write card) |
| 5 | Per-tool allow / ask / deny rules | oc, cl, omp, ocw | BUILD (MANJUEL_DRIVER_ALLOW / _DENY) |
| 6 | A no that carries a reason back | oc, os | HAVE |
| 7 | No answer is a no; unattended denies | he, oc, cl, ocw | HAVE |
| 8 | Floors that hold in every mode | he, omp, ocw | HAVE (never_written, secrets, main) |
| 9 | Plan mode: read only, then a plan to approve | oc, cl, omp, pi | BUILD (`/drive propose`: reads, then a plan card) |
| 10 | JSON repair, type coercion, nearest tool name | pi, oc, he, omp, cl | HAVE |
| 11 | Plain-text tool calls promoted (harmony etc.) | ocw, omp | HAVE |
| 12 | A model's own tool-call dialect | omp | HAVE |
| 13 | A length-cut call never run | pi, he, oc | HAVE |
| 14 | A reply cut off by its length continued | oc, cl, he | BUILD |
| 15 | An empty reply retried, not taken for done | cl, he, omp | BUILD |
| 16 | Retry with backoff on a failed model call | all | HAVE |
| 17 | A fallback model when the first one fails | he, ocw, omp | BUILD (MANJUEL_DRIVER_FALLBACK) |
| 18 | Loop guard (identical calls, cycles) | cl, he, omp, ocw | HAVE |
| 19 | Failure guard (turns of nothing but failures) | cl, he | HAVE |
| 20 | Forgiving edit matcher | oc, pi, he, ocw, omp | HAVE |
| 21 | Several edits in one call | pi, ocw, omp | BUILD (repeated @@ OLD / @@ NEW pairs) |
| 22 | A multi-file patch, all checked before any is written | he (V4A), cl, oc, omp, ocw | BUILD (`apply_patch`) |
| 23 | Help on a missed edit (nearest lines, column) | ocw | HAVE |
| 24 | Read-back: what was written is checked byte for byte | ocw | BUILD |
| 25 | Stale-write guard: no overwrite of a file not read | he | BUILD |
| 26 | Lint after an edit | he, omp | BUILD (.py parse kept; .json parsed; .js `node --check`) |
| 27 | grep over the ground (regex) | all coding harnesses | BUILD (`ground_grep`) |
| 28 | Find files by pattern (glob) | all coding harnesses | BUILD (`find_files`) |
| 29 | A shell, gated | all coding harnesses | BUILD (`run_shell`: reads at once, the rest asks) |
| 30 | A todo list the model keeps | oc, he, omp, cl | BUILD (`todo`) |
| 31 | Ask the operator a question with choices | cl, he, ocw, omp, oc | BUILD (`ask_operator`) |
| 32 | Big results trimmed, the whole kept and named | oc, he, omp, pi | HAVE |
| 33 | Compaction in a fixed form, model-free first | oc, pi, cl, he, omp, ocw | HAVE |
| 34 | A small side model for summaries | cl, oc, he, ocw | BUILD (MANJUEL_SUMMARY_MODEL) |
| 35 | The window from the model and the card | he, cl, oc, ocw | HAVE |
| 36 | Rules, memory and standing in the prompt | all | HAVE |
| 37 | Tool search / deferred tools for a small window | pi, he, omp, ocw | NOT NEEDED (gpt-oss, 27 tools) |
| 38 | Sub-agents | oc, cl, he, omp, ocw | HAVE (delegate) |
| 39 | A batch of sub-agent tasks | he, omp, cl, ocw | BUILD (delegate `tasks`, one at a time on one GPU) |
| 40 | Sub-agents in their own copy of the folder | omp, he, ocw | NOT TAKEN (seats write nothing; the line of work is the copy) |
| 41 | The job written down; resume after a crash | oc, pi, ocw, he | HAVE |
| 42 | Undo the last turn's file changes | oc, cl, he, omp | BUILD (`/undo`) |
| 43 | Sessions saved and resumed | all | HAVE (sittings, thread.jsonl, /resume) |
| 44 | Schedules (cron) | he, cl, ocw | BUILD (`/schedule`) |
| 45 | Goals that persist until their check passes | he, ocw, omp | BUILD (`/goal`) |
| 46 | Background commands that report when done | oc, he, omp, cl | NOT YET (needs a long-lived runner) |
| 47 | Skills as markdown, read whole on first use | all | HAVE |
| 48 | Skills hot-reloaded | oc, cl | HAVE (the watcher, /reload) |
| 49 | MCP client, stdio and HTTP | all coding harnesses | HAVE (REA, 207 tools) |
| 50 | MCP server | he, ocw | HAVE (the door) |
| 51 | Hooks before and after a tool | pi, oc, cl, he, ocw | HAVE (skill hooks) |
| 52 | Learning staged for the operator | he, omp, ocw | HAVE (lessons) |
| 53 | Secrets entered masked, never seen by the model | ocw, os | BUILD (the secret card) |
| 54 | Messaging channels (Discord...) | he, cl, ocw | NEXT (Steward's own test, after the secret card) |
| 55 | Desktop app | he, oc, ocw | HAVE |
| 56 | Voice | he, omp, ocw | HAVE (speak, listen) |
| 57 | Binary triage | rs | HAVE (triage_binary) |
| 58 | Reverse engineering | rs (staged), REA | HAVE (REA through mcp_call) |
| 59 | Kernel sandbox | os | NOT TAKEN (Linux; Windows native needs an Insider build) |
| 60 | Web search and fetch | all but os | NOT TAKEN (RULE 4: the estate is local) |
| 61 | Telemetry, auto-update, phone-home | pi, os, omp, cl, ocw | NOT TAKEN (RULE 4) |
| 62 | Allow-everything defaults | omp, oc, ocw, cl | NOT TAKEN |

## The gaps, ranked by what we keep fighting

1. **A click for every write.** Piece 2: the plan card and line-auto, chosen per job, with a bound on every card.
2. **A slip costs the job.** Piece 3: repair, the forgiving matcher, the loop and failure counters, a retry, the
   written-down job.
3. **The driver outside the rails.** With piece 2: the law gate on the driver's goal and writes, the check shown first.
4. **The model's own form.** Piece 4: Ollama's JSON mode for plans and arguments, the dialect layer, the window from the
   rack, one Steward on gpt-oss:20b, measured.
5. **A full window.** Piece 5: the model-free cut, the summary, the laws and memory in the prompt.
6. **REA and the outside MCP servers.** Piece 6: stdio MCP through the door.
7. **Steward as the face, the council as his sub-agents.** Piece 7.
8. **What was learned, kept.** Piece 8: staged for your hand.

## What comes next, for your ruling

No code until you rule on this page. Then one piece at a time, each a Steward job whose check ends with the ship's step,
each gap declared first in its `.us` record so `us.py` shows it LOOSE until its wire is built.
