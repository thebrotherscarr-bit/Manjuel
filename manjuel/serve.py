"""The headless door: the REPL's turn over stdin/stdout as JSON lines.

    python manjuel.py --headless
    python -m manjuel.serve

THE OPERATOR, 2026-09-08 (SPEC_CONTROL_CENTER.md P0-1): "im ok with that,
build it now and get it out of the way." A front end cannot press keys in a
REPL. This is the one extra way in: instructions arrive as JSON lines on
stdin, what happens goes out as JSON lines on stdout, humans get stderr.
NO SOCKET, no daemon, no API -- BUILDPATH's position is kept. The engine is
untouched: run_pipeline, the gates, the record and the toll are exactly the
REPL's, reached through cli.py's own functions, so a transcript written
through this door is the transcript the REPL would have written.

HOW THE REPL'S KEYBOARD AND SCREEN ARE REPLACED, without editing them:

  the screen   sys.stdout is swapped for a channel that turns every write
               into a `text` event. ink.enabled() reads isatty() off it,
               finds False, and switches colour and the spinner off -- the
               same plain text the suites see. Nothing in cli.py or
               pipeline.py stops calling print(); it just lands here.

  the keyboard builtins.input is swapped for a question over the wire: a
               `needs_answer` event with the prompt, then a wait for the
               client's `answer`. Every input() in cli.py (the toll's three
               questions, the memory kind, the confirms) and the one in
               pipeline.py (`retry / skip / abort?` for a seat marked
               On Fail: prompt) reaches the client this way. A `cancel`
               while a question is pending raises KeyboardInterrupt at the
               input() call, which is what Ctrl-C does there; a `close`
               raises EOFError, which is what Ctrl-D does.

  Ctrl-C       a `cancel` while a run is in flight raises KeyboardInterrupt
               in the main thread (_thread.interrupt_main), which the turn
               catches as "Run cancelled" -- the REPL's own path, and the
               transport is closed the way runtime._bounded_stream closes
               it.

THE STRUCTURED EVENTS ride beside the text. Two eyes, neither inside the
engine: the runtime is wrapped so a seat sitting is a `seat` event and its
streamed pieces are `token` events (control markup hidden between `<` and
`>`, the sink's own one-character rule), and each fragment of its thought,
as it arrives, a `think` event under the same rule -- handed on to the
engine, which keeps it for the transcript and nowhere else (2026-10-14,
WHAT'S LEFT C70: "the thinking models show their CoT as they go"); the
skill library's execute() is wrapped so a call is a `tool` event and its
return a `tool_result`. The run's `report` lines are `report` events. The
turn ends in exactly one of
`delivery` / `refused` / `aborted` / `cancelled` / `unreachable` / `error`,
carrying the record's own notes and per-seat facts (elapsed, tools, error,
skipped) -- read off the StepResults, never off a seat's words (LAW 5).

THE WIRE (protocol 1). One JSON object per line, UTF-8.

  in   {"cmd":"objective","text":"...","feed":"...?","method":"...?",
        "model":"...?","voices":{"seat":"tag"}?,"unattended":true?}
                                          `unattended` says NOBODY IS AT THE
                                          PROMPT for this turn (a flow's node):
                                          a seat marked On Fail: prompt that
                                          fails is skipped, the prompt's own
                                          default, and no needs_answer is sent
                                          for it. Only the literal `true` counts
                                          `model` runs THIS TURN's seats on
                                          one head; `voices` names a head per
                                          SEAT and is applied over it, so a
                                          parity can vary one voice and not
                                          the roster. Both put the declared
                                          targets back when the turn ends; an
                                          uninstalled tag or an unknown seat
                                          is `refused` by name before anything
                                          moves, never quietly ignored
       {"cmd":"answer","text":"..."}      the reply to a needs_answer
       {"cmd":"listen","seconds":N?}      capture one spoken turn; the
                                          text comes back as `heard` and
                                          is NOT run -- the hand sends it
       {"cmd":"cancel"}                   the run, or the pending question
       {"cmd":"close"}                    close the sitting (the toll is paid
                                          unattended if runs happened, as
                                          on exit)
  out  opened · text · run · report · seat · token · think · tool ·
       tool_result · needs_answer · heard · delivery · refused · aborted ·
       cancelled · unreachable · error · note · command · closed

EVERY TURN ENDS IN EXACTLY ONE TERMINAL EVENT: delivery for a pipeline
run, command for a `/command` or any other turn that finished without
running one, or refused / aborted / cancelled / unreachable. A client
pumps until one arrives, so a turn that ended silently hung the wire
forever -- which is what every command did until this was added.

AN ENGINE NOBODY USES CLOSES ITSELF (2026-09-16). With no command for
IDLE_CLOSE seconds -- thirty minutes -- between turns, the door closes the
sitting exactly as `close` does and emits `closed` unasked, the reason in
its `why`. Never mid-turn, and never while a needs_answer is waiting.

AND AN ENGINE THAT DIES HOLDS NOTHING (2026-09-22). A hang-up is heard at
once, by the loop and by every question after it -- never waited out. Every
exit after the sitting line closes the sitting: a fault or a Ctrl-C in the
boot, and an interrupt anywhere after it. And this door reaps as the REPL
does: a sitting left open by a process that is gone is closed before its
own opens, so THE LINE no longer finds a dead engine's world locked.

An `objective` is anything the REPL would take at its prompt: a plain
turn, a `/command`, `@seat words`, "pay the toll", "remember that". One
turn at a time, in order; an objective sent mid-run waits its turn. The
gate is still final: nothing here lands memory, pays an attended toll or
commits without an `answer` from the client's hand (RULE 6 / LAW 6).

WHAT IT IS NOT. Not a second executor, not a second engine, not
multi-session: one process, one ground, one sitting, one writer -- the
same shape as the REPL it stands beside. Environments (grounds under
worlds/<name>/) are THE LINE's to open, one door each (SPEC_CONTROL_CENTER
§4.2; this line read `agent_workspace/` until 2026-09-24 -- the ruling moved
them to worlds/ on the afternoon of 2026-09-08, and Appendix D11 has said
"a doc line to fix when serve.py is next touched" ever since. It was touched
twice in one week before anybody read the line that asked). Voice: ONE HALF crosses the wire, and one does not. `listen` (below)
captures a single spoken turn through voice.py -- the same compiled
whisper.cpp, the same vocabulary bias, the same call the REPL's /chat
makes -- because the engine runs on the operator's own machine and the
microphone is right there. What does NOT cross is /chat's interactive
loop: it reads the keyboard to cut off an answer mid-sentence, and a
keypress has no meaning down a pipe. A captured turn is returned, never
run: the hand sends it, or edits it first (RULE 6).
"""

from __future__ import annotations

import builtins
import json
import os
import queue
import sys
import threading
import time
import _thread
from pathlib import Path

PROTOCOL = 1

# The wire's vocabulary, spelled once so a stroke can hold the door to it.
COMMANDS = ("objective", "answer", "listen", "cancel", "close")
EVENTS = ("opened", "text", "run", "report", "seat", "token", "think", "tool",
          "tool_result", "needs_answer", "delivery", "refused", "aborted",
          "cancelled", "unreachable", "error", "note", "heard", "command",
          "closed")

# THE EVENTS THAT END A TURN. A client pumps until one of these arrives, so
# a turn that ends without one hangs it for the life of the process -- which
# is exactly what every `/command` did until 2026-09-09. `error` is NOT here:
# the inbox emits it non-terminally for a malformed command and the turn
# carries on.
TERMINAL = ("delivery", "refused", "aborted", "cancelled", "unreachable",
            "command")

# AN ENGINE NOBODY USES CLOSES ITS OWN SITTING (2026-09-16, his ruling on the
# optimization pass: "D2 30 minutes"). The record held 13.8 engine-hours of
# engines standing after their last turn -- 7.2 of them sitting 208's, 429
# minutes after its fourth run -- and 58 sittings that ran nothing; the
# Dashboard's amber "idle" line only helps while someone is looking at it.
# The door waits this long for the next command BETWEEN turns, then closes the
# sitting the way a client's `close` does. Never mid-turn (a turn does not wait
# on the inbox), never while a question is pending (ask() waits without a
# bound), and never in the REPL, which does not come through here. It is the
# runtime's default keep-alive too, so by then Ollama has let the seats' models
# go and a reboot costs little more than the next turn would have.
IDLE_CLOSE = 30 * 60

# The first characters of a tool result that mean it failed -- the
# pipeline's own test (pipeline.py, the tool loop) -- READ FROM THE ONE SOURCE
# since 2026-09-25, not repeated, so the event says what the record says by
# construction rather than by a copy kept in step.
from .context import FAILED_HEADS as _FAILED_HEADS  # noqa: E402
_RESULT_HEAD_CHARS = 400


_BOOT_T0 = time.time()


def _mark(stage: str) -> None:
    """One line of boot progress, on the REAL stderr.

    WHY THIS EXISTS (2026-09-10). A boot that hangs under THE LINE left no
    evidence anywhere: stdout is swapped for the wire, so every print became
    a `text` event the door discards while it waits for `opened`; stderr was
    empty; and the door's own timeout message named the symptom and not the
    place. Nine sittings died that way in one day and the only way to find
    the stage was to guess at it from outside.

    stderr is untouched by open_wire and THE LINE already keeps its tail
    (engine.go's ringBuffer) and now prints it when a boot fails, so this
    costs one line per stage and needs no file, no flag and no new plumbing.
    It can never break a boot: every failure here is swallowed on purpose --
    an instrument that can take the process down is worse than no instrument.
    """
    try:
        print("boot: %7.1fs  %s" % (time.time() - _BOOT_T0, stage),
              file=sys.__stderr__, flush=True)
    except Exception:
        pass


# ---------------------------------------------------------------------
# the wire
# ---------------------------------------------------------------------


class Wire:
    """JSON lines out, one per event, under a lock: the watcher, the
    background warm and a spinner (off, but still) share the process."""

    def __init__(self, out):
        self._out = out
        self._lock = threading.Lock()
        self.sent: int = 0
        # Whether a terminal event has gone out since the turn began. The
        # serve loop clears it at the start of a turn and closes any turn
        # that ended without one. Kept HERE rather than at each early
        # return in turn(): enumerating those fixes the four that exist and
        # misses the fifth someone adds.
        self.ended: bool = False

    def emit(self, event: str, **fields) -> None:
        if event in TERMINAL:
            self.ended = True
        row = {"event": event}
        row.update(fields)
        line = json.dumps(row, ensure_ascii=False, default=str) + "\n"
        with self._lock:
            try:
                self._out.write(line)
                self._out.flush()
            except Exception:
                pass                        # a closed pipe ends the door, below
            self.sent += 1


class TextChannel:
    """Stands where sys.stdout stood. Every write is a `text` event; there
    is no terminal, so isatty() is False and ink stays plain."""

    encoding = "utf-8"
    errors = "replace"

    def __init__(self, wire: Wire):
        self._wire = wire

    def write(self, s) -> int:
        s = str(s or "")
        if s:
            self._wire.emit("text", text=s)
        return len(s)

    def flush(self) -> None:
        return None

    def isatty(self) -> bool:
        return False

    def fileno(self):
        raise OSError("the headless door has no terminal")

    def writelines(self, lines) -> None:
        for l in lines:
            self.write(l)


class Inbox:
    """The client's lines, read on a thread so a `cancel` can reach a run
    that is busy in a model call. Malformed lines are answered with an
    `error` event and dropped -- never guessed at."""

    IDLE, RUNNING, ASKING = "idle", "running", "asking"

    def __init__(self, source, wire: Wire):
        self._source = source
        self._wire = wire
        self._q: "queue.Queue[dict | None]" = queue.Queue()
        self._state = self.IDLE
        self._lock = threading.Lock()
        self.closed = False
        self._thread = threading.Thread(target=self._pump, daemon=True,
                                        name="headless-inbox")

    def start(self) -> None:
        self._thread.start()

    def set_state(self, state: str) -> None:
        with self._lock:
            self._state = state

    def _pump(self) -> None:
        try:
            for raw in self._source:
                line = (raw or "").strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    self._wire.emit("error", text=f"not JSON: {line[:120]!r}")
                    continue
                if not isinstance(row, dict) or not isinstance(row.get("cmd"), str):
                    self._wire.emit("error", text=f"not a command: {line[:120]!r}")
                    continue
                cmd = row["cmd"].strip().lower()
                if cmd not in COMMANDS:
                    self._wire.emit("error",
                                    text=f"unknown cmd {cmd!r}; the wire takes "
                                         f"{', '.join(COMMANDS)}")
                    continue
                row["cmd"] = cmd
                with self._lock:
                    state = self._state
                if cmd == "cancel" and state == self.RUNNING:
                    # Ctrl-C, delivered to the thread that is in the model
                    # call. The turn's own except: KeyboardInterrupt does
                    # the rest, and the transport is closed on the way out.
                    _thread.interrupt_main()
                    continue
                self._q.put(row)
        except Exception as exc:                # the pipe died under us
            self._wire.emit("error", text=f"inbox: {type(exc).__name__}: {exc}")
        finally:
            self.closed = True
            self._q.put(None)                  # EOF: the client hung up

    def take(self, timeout: float | None = None) -> dict | None:
        """The next command, or None at EOF -- and None at every call after it.

        A HANG-UP IS REMEMBERED (2026-09-22). EOF used to be one None in the
        queue, and the first taker spent it. When a question was pending, that
        was ask(): it raised EOFError and the turn moved on, and the loop then
        waited the whole IDLE_CLOSE for a client that had already gone -- or,
        if the same turn asked again, waited on the queue forever, with its
        sitting open and nothing able to reap a process that was still alive.
        Once the pump has ended and nothing is queued, every take answers None
        at once: the second question and the loop both hear the hang-up."""
        if self.closed and self._q.empty():
            return None
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            return {"cmd": "_timeout"}

    def put_back(self, row: dict) -> None:
        self._q.put(row)


# ---------------------------------------------------------------------
# the eyes: seat / token and tool / tool_result, without touching the engine
# ---------------------------------------------------------------------


class _Runtime:
    """The runtime as it is, plus a `seat` event when a seat sits, `token`
    events as it speaks and `think` events as it thinks. Delegates
    everything else, so the Stub the suites use and the real OllamaRuntime
    both fit behind it."""

    def __init__(self, inner, wire: Wire):
        self._inner = inner
        self._wire = wire

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def chat(self, agent, user_prompt, stream_to=None, tools=None,
             think_to=None, think=None):
        self._wire.emit("seat", seat=agent.name, model=agent.model,
                        timeout=getattr(agent, "timeout", None),
                        streaming=stream_to is not None)
        sink = self._token_sink(agent.name) if stream_to is not None else None
        return self._inner.chat(agent, user_prompt, stream_to=sink, tools=tools,
                                think_to=self._think_sink(agent.name, think_to),
                                think=think)

    def _token_sink(self, seat: str, event: str = "token"):
        # SITTING 70's rule, kept: control markup is the seat's channel to
        # the ENGINE and never reaches a person live. A tag can be split
        # across pieces, so this is the sink's one-character state machine:
        # from `<` to `>` nothing is shown. A seat's thought takes the same
        # rule, sent as `think` (`_think_sink`, below).
        inside = [False]

        def sink(piece):
            shown = []
            for ch in str(piece or ""):
                if inside[0]:
                    if ch == ">":
                        inside[0] = False
                    continue
                if ch == "<":
                    inside[0] = True
                    continue
                shown.append(ch)
            text = "".join(shown)
            if text:
                self._wire.emit(event, seat=seat, text=text)
        return sink

    def _think_sink(self, seat: str, keep):
        """THE THOUGHT, LIVE (2026-10-14, WHAT'S LEFT C70; his words: "I would
        like the streaming of the processes instead of just chunks of text
        being dumped ... so i can actually see the turns within the
        terminal", and "the thinking models show their CoT as they go").
        runtime.chat hands each fragment of a seat's thought to think_to as
        it arrives; until C70 it crossed this door untouched, so a seat that
        thought for minutes drew nothing on the glass. Each fragment now goes
        on the wire as it arrives, a `think` event under the words' own
        markup rule, and is handed on to the engine's own think_to, which
        keeps it for the transcript (sitting 79) and nowhere else. Every
        seat's call is given one, whether its caller asked or not, so every
        seat's thought is seen."""
        show = self._token_sink(seat, "think")

        def sink(piece):
            show(piece)
            if keep is not None:
                keep(piece)
        return sink


def _watch_skills(skills, wire: Wire) -> None:
    """Wrap execute() on THIS library instance for THIS wire. /reload
    builds a new library, so the turn re-checks before every run."""
    if skills is None or getattr(skills, "_headless_wire", None) is wire:
        return
    # Wrap the library's OWN execute, never a previous wrap: one library
    # can outlive a wire (the suites drive several doors over one).
    inner = getattr(skills, "_headless_inner", None) or skills.execute

    def execute(action, args, env):
        wire.emit("tool", action=action,
                  args={k: str(v)[:200] for k, v in (args or {}).items()})
        result = inner(action, args, env)
        text = str(result or "")
        wire.emit("tool_result", action=action,
                  failed=text.lstrip().startswith(_FAILED_HEADS),
                  chars=len(text), head=text[:_RESULT_HEAD_CHARS])
        return result

    skills.execute = execute
    skills._headless_inner = inner
    skills._headless_wire = wire


# ---------------------------------------------------------------------
# the driver: Steward drives (WHAT'S LEFT H31)
# ---------------------------------------------------------------------
#
# His words, 2026-10-16: "A single simple driver that runs long workflows and
# tool chains to make sure that basically whatever I ask can be done. Fairly
# simple."; "the agent should just wait for the approval before ruling, and
# then should say what happened"; "checking what it did, verifying it, and then
# doing the whole CI pipeline? That is Nigel, I want that Parity!"; and "It
# needs to complete the tasks, close the branch, and then ask for what's next
# in the workflow, so it can have multi-step iterations."
#
# Nigel's shape (github.com/cdlewis/nigel), in this engine:
#
#   /drive <goal> | check: <command>
#       ONE JOB. The model works the goal through the skills, step by step; the
#       check -- never the model -- decides it is done. A pass shows what changed
#       and, on his answer, commits the job's own files on its line of work,
#       pushes, opens the pull request and waits on CI; green, it asks him to
#       merge, and his yes merges, deletes the branch on GitHub, closes the line
#       here and brings main up to date. A job whose check never passed puts its
#       own files back on his answer.
#
#   /drive plan <goal> | check: <command>
#       DECOMPOSE, WORK, RECOMPOSE. The model breaks the goal into a short list
#       of items for his answer; each item is its own job, committed when its
#       check passes and put back when it does not; then the whole is checked
#       once more and, on his answer, shipped as one pull request.
#
#   /drive each <command> | do: <prompt with $ITEM> | check: <command>
#       NIGEL'S LOOP. <command> lists the items (JSON or one per line); each is
#       worked with the prompt, and is done only when the check passes AND the
#       command no longer lists it. Every item worked is written to
#       logs/drive_ignore.jsonl and is not tried blindly again.
#
#   /drive tidy
#       THE CLEAN-UP his words asked for ("those branches just never got cleaned
#       up afterwards. that ALL needs to be done agentically"): every branch
#       already merged into main, here and on GitHub, in the ground and in
#       atlas/, listed and deleted on one answer. A local one goes only when git
#       lists it as merged into main (GitHub's main, once fetched); main and the
#       branch he stands on never go.
#
#   /drive ship <message> [| check: <command>]
#       THE SAVE AND SEND of work already on disk (H31's second proof job): in
#       the ground and in atlas/, what changed is listed, and on one answer each
#       repository's files become one commit under his message, on a line of
#       work opened from main; then the push, the pull request, CI and the merge
#       card, as for a job. A secret or a world on the list stops it before
#       anything is asked.
#
# Plan and each need a check: it is what decides each item. Then it asks what
# is next, and the answer is the next job in the same turn, with what the
# earlier jobs did carried into it (cut to DRIVE_CARRY_CHARS).
#
# Every write asks first and the loop waits on the answer, every time. A file
# that carries changes of his own is never written, so whatever the run commits
# or puts back is its own work alone; a put back restores the bytes it found. A
# push goes on his yes to the commit only when every commit going is one this
# run made on a line it opened; anything else is shown to him and asked for.
# The main line is never written; the merge is his click on its card (RULE 13).
# Each item has its own budget of steps and minutes. The report is built from
# the record of the steps, never from the model's account of them (LAW 5). It
# drives the skills the engine already has, through SkillLibrary.execute, so
# every law gate, jail and refusal they carry applies to it unchanged.


def _drive_dial(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name) or default)
    except ValueError:
        return float(default)


# His card, 2026-10-16: the driver starts on qwen3.5:9b (SITTING LAW 3).
DRIVE_MODEL = os.environ.get("MANJUEL_DRIVER_MODEL", "").strip() or "qwen3.5:9b"
DRIVE_STEPS = int(_drive_dial("MANJUEL_DRIVER_STEPS", 30))
DRIVE_MINUTES = _drive_dial("MANJUEL_DRIVER_MINUTES", 45)
DRIVE_ITEM_STEPS = int(_drive_dial("MANJUEL_DRIVER_ITEM_STEPS", 15))
DRIVE_ITEM_MINUTES = _drive_dial("MANJUEL_DRIVER_ITEM_MINUTES", 15)
DRIVE_ITEMS_MAX = int(_drive_dial("MANJUEL_DRIVER_ITEMS", 25))
DRIVE_CONTEXT = int(_drive_dial("MANJUEL_DRIVER_CTX", 16384))
DRIVE_CARRY_CHARS = int(_drive_dial("MANJUEL_DRIVER_CARRY", 3000))
# The check runs here with its own bound: the strokes take about 313 s, past
# the 295 s a door call waits (WHAT'S LEFT C71).
DRIVE_CHECK_SECONDS = _drive_dial("MANJUEL_DRIVER_CHECK_SECONDS", 900)
DRIVE_CI_SECONDS = _drive_dial("MANJUEL_DRIVER_CI_SECONDS", 1800)
DRIVE_CALL_SECONDS = 600.0
DRIVE_RESULT_CHARS = 4000
# Never offered to the model. Saving and sending are the run's own steps, on
# his answer (RULE 6, RULE 12); memory lands only through /memory (LAWS 5, 6).
DRIVE_NEVER = {"git_commit", "git_cycle", "git_push", "git_pull", "git_init",
               "remember", "rack_sync", "rack_load", "rack_unload", "rack_pull",
               "index_ground", "embed_text", "speak"}
# Offered beside the readers. Each of these asks him first (drive_act).
DRIVE_HANDS = {"ground_write", "ground_edit", "write_file", "edit_file",
               "run_python", "mcp_call"}
DRIVE_ASKS = ("run_python", "mcp_call")      # asked as the WRITING_SKILLS are
DRIVE_TREE = ("ground_write", "ground_edit")
DRIVE_MAIN = ("main", "master")
DRIVE_SUITES = "python tests/test_manjuel.py"
DRIVE_YES = ("y", "yes", "approve", "approved", "ok", "go")
DRIVE_STOP = ("", "stop", "no", "n", "done", "nothing", "exit", "quit")
DRIVE_IGNORE = "drive_ignore.jsonl"
DRIVE_USAGE = (
    "  /drive <goal> | check: <command>          one job, worked until the check passes\n"
    "  /drive plan <goal> | check: <command>     the goal broken into items, each its own job\n"
    "  /drive each <command> | do: <prompt with $ITEM> | check: <command>\n"
    "        one job per item the command lists; an item is done when the check\n"
    "        passes AND the command no longer lists it\n"
    "  /drive tidy                               every branch merged into main deleted, here and on GitHub\n"
    "  /drive ship <message>                     the work on disk saved, sent, through CI, merged on your card\n"
    "  plan and each need a check; \"suites\" as the check runs the strokes. Every\n"
    "  write asks first; after each job it asks what is next.")
DRIVE_SYSTEM = (
    "You are the Steward, driving one job to its end on the operator's machine. "
    "Work in steps: call one tool, read what it returned, then decide the next "
    "call. Use only the tools you are given, and never claim a result a tool did "
    "not return. A file in the ground (the code and the documents) is changed "
    "with ground_edit (one exact passage) or ground_write (a whole file); "
    "write_file writes only the workspace. Tools that write wait for the "
    "operator's approval; if he declines, find another way or call done. Do not "
    "write or run scripts to test your own work: the job's check runs by itself "
    "when you call done. When you believe the goal is met, call done with a "
    "one-line summary. Only a passing check ends the job; if it fails you are "
    "given its output -- fix what it names and call done again.")
DRIVE_PLAN_SYSTEM = (
    "You break one goal into a short list of small, separate items of work. Each "
    "item must be doable on its own and checkable by the same check. Reply with "
    "ONLY a JSON array of strings, two to eight of them, and nothing else.")
DRIVE_DONE_TOOL = {
    "type": "function",
    "function": {
        "name": "done",
        "description": ("Call when you believe the goal is met. The job's check "
                        "runs next; only a passing check ends the job."),
        "parameters": {
            "type": "object",
            "properties": {"summary": {"type": "string",
                                       "description": "one line: what was done"}},
            "required": [],
        },
    },
}
DRIVE_SAID = {
    "passed": "DONE: the check passed",
    "unchecked": "UNCHECKED: no check was named, so nothing proves the goal is met.",
    "budget": "NOT DONE: the budget ran out before the check passed.",
    "failed": "NOT DONE: the check did not pass.",
    "partial": "PART DONE: some items passed and some did not.",
    "nothing": "NOTHING TO DO: every item listed was tried before (logs/drive_ignore.jsonl).",
    "declined": "NOT RUN: the run was declined.",
    "tidy": "TIDY: every branch already merged into main is deleted.",
    "tidy_part": "TIDY: some branches could not be deleted (the record says which).",
    "clean": "TIDY: no branch merged into main is left, here or on GitHub.",
    "shipped": "SHIPPED: saved and sent; the steps say what CI and the merge did.",
    "unsent": "NOT SENT: saved on its line of work, but the send did not go through (the steps say why).",
}
DRIVE_REPOS = ("", "atlas")                  # the ground, and the door's repository inside it


class Drive:
    """One job's record. Everything the report says is read off this."""

    def __init__(self, goal: str, check: str, model: str):
        self.goal, self.check, self.model = goal, check, model
        self.steps: list = []        # [n, tool, args, result]
        self.n = 0
        self.verdict = ""            # a key of DRIVE_SAID, or error
        self.check_out = ""
        self.error = ""
        self.elapsed = 0.0
        self.transcript = ""
        self.report = ""
        self.repos: dict = {}        # repo -> {"base", "line"}: where the job wrote
        self.item_files: set = set() # (repo, path) the item in hand wrote, not yet saved
        self.touched: set = set()    # (repo, path) the run ever wrote
        self.before: dict = {}       # (repo, path) -> its bytes before the item wrote it (None: new)
        self.made: dict = {}         # repo -> the commits this run made there
        self.items: list = []        # [item, verdict]
        self.prs: list = []          # pull requests opened
        self.merged: list = []       # lines merged on his click


def drive_parse(said: str) -> dict:
    """'[plan|each|tidy|ship] <goal> [| do: <prompt>] [| check: <command>]' -> a spec.
    The fields are cut from the end, so a pipe inside a command stays in it."""
    text = str(said or "").strip()
    mode = "goal"
    for m in ("plan", "each", "tidy", "ship"):
        if text.lower() == m or text.lower().startswith(m + " "):
            mode, text = m, text[len(m):].strip()
            break           # the first word alone names the mode: "plan tidy the docs" is a plan
    check = do = ""
    cut = text.lower().rfind("| check:")
    if cut >= 0:
        text, check = text[:cut].strip(), text[cut + len("| check:"):].strip()
    cut = text.lower().rfind("| do:")
    if cut >= 0:
        text, do = text[:cut].strip(), text[cut + len("| do:"):].strip()
    if check.lower() in ("suites", "the suites", "strokes", "the strokes"):
        check = DRIVE_SUITES
    return {"mode": mode, "goal": text, "check": check, "do": do}


def _drive_yes(answer) -> bool:
    return str(answer or "").strip().lower() in DRIVE_YES


def drive_check(check: str, ground: Path) -> tuple:
    """The job's check, run in the ground. Exit 0 passes. Bounded."""
    import subprocess
    try:
        # stdin CLOSED: the engine's own stdin is the door's wire, and a check that
        # inherited it hung on it (2026-10-16, a one-line python -c, 400 s).
        p = subprocess.run(check, shell=True, cwd=str(ground), capture_output=True,
                           stdin=subprocess.DEVNULL,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=DRIVE_CHECK_SECONDS)
    except subprocess.TimeoutExpired:
        return False, f"the check ran past {DRIVE_CHECK_SECONDS:.0f}s and was stopped"
    out = ((p.stdout or "") + (p.stderr or "")).strip()
    tail = ("\n" + out[-DRIVE_RESULT_CHARS:]) if out else ""
    return p.returncode == 0, f"exit {p.returncode}" + tail


def _drive_run(argv, cwd, timeout: float = 120) -> tuple:
    """One command (git, gh) in a repository: (exit, output). stdin closed."""
    import subprocess
    try:
        p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           stdin=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, f"{argv[0]} ran past {timeout:.0f}s and was stopped"
    except OSError as exc:
        return 127, f"{argv[0]} could not start: {exc}"
    return p.returncode, ((p.stdout or "") + (p.stderr or "")).strip()


def drive_source(cmd: str, ground: Path) -> tuple:
    """The items a source command lists: JSON, or one per line. (items, why);
    items is None when the source itself failed, which never reads as empty."""
    import subprocess
    try:
        p = subprocess.run(cmd, shell=True, cwd=str(ground), capture_output=True,
                           stdin=subprocess.DEVNULL, text=True, encoding="utf-8",
                           errors="replace", timeout=DRIVE_CHECK_SECONDS)
    except subprocess.TimeoutExpired:
        return None, f"it ran past {DRIVE_CHECK_SECONDS:.0f}s"
    out, err = (p.stdout or "").strip(), (p.stderr or "").strip()
    if p.returncode == 1 and not out and not err:
        return [], ""                # grep's "nothing found": nothing left
    if p.returncode != 0:
        return None, f"exit {p.returncode}: {(err + ' ' + out).strip()[:400]}"
    if not out:
        return [], ""
    try:
        data = json.loads(out)
        return (data if isinstance(data, list) else [data]), ""
    except ValueError:
        return [l.strip() for l in out.splitlines() if l.strip()], ""


def _drive_key(item) -> str:
    return item if isinstance(item, str) else json.dumps(item, sort_keys=True, ensure_ascii=False)


def _drive_ignored(logs: Path, key: str) -> set:
    seen = set()
    p = Path(logs) / DRIVE_IGNORE
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if row.get("task") == key:
                seen.add(row.get("item"))
    return seen


def _drive_ignore(logs: Path, key: str, item: str, verdict: str) -> None:
    try:
        with open(Path(logs) / DRIVE_IGNORE, "a", encoding="utf-8", newline="\r\n") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "task": key,
                                "item": item, "verdict": verdict}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def drive_tools(skills) -> tuple:
    """The schemas the model is offered, and the set the library enforces."""
    from .skills import REVIEW_ONLY_SKILLS
    have = set(skills.keywords())
    allowed = ((set(REVIEW_ONLY_SKILLS) | DRIVE_HANDS) & have) - DRIVE_NEVER
    return skills.tool_schemas(allowed) + [DRIVE_DONE_TOOL], allowed


def _drive_field(obj, name):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def drive_calls(msg) -> list:
    """Every native tool call in a reply, as (name, args)."""
    out = []
    for call in (_drive_field(msg, "tool_calls") or []):
        fn = _drive_field(call, "function")
        if fn is None:
            continue
        name = str(_drive_field(fn, "name") or "").strip()
        args = _drive_field(fn, "arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except ValueError:
                args = {"content": args}
        if name:
            out.append((name, dict(args) if isinstance(args, dict) else {}))
    return out


def _drive_brief(args) -> str:
    text = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
    return text if len(text) <= 120 else text[:117] + "..."


def _drive_head(text) -> str:
    lines = [l for l in str(text or "").strip().splitlines() if l.strip()]
    if not lines:
        return "(empty)"
    first = lines[0].strip()
    return first if len(first) <= 160 else first[:157] + "..."


def _drive_target(env, args):
    """(repo, path, branch) of the file a tree write names, or None."""
    from .skills import _inside_ground, repo_of, unjail
    rel = unjail(str(args.get("filepath") or "").strip().strip("'\"`"))
    path = _inside_ground(env, rel) if rel else None
    repo = repo_of(env, path) if path is not None else None
    if repo is None:
        return None
    code, branch = _drive_run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    return repo, path, (branch.strip() if code == 0 else "")


def _drive_rel(repo, path) -> str:
    return Path(path).resolve().relative_to(Path(repo).resolve()).as_posix()


def _drive_by_repo(files) -> dict:
    by: dict = {}
    for repo, path in sorted(files):
        by.setdefault(repo, []).append(_drive_rel(repo, path))
    return by


def drive_act(name: str, args: dict, ctx, d) -> str:
    """One call. A writer waits for his answer first and runs only on a yes,
    every time. A tree write on the main line opens the job's own line of work
    first, in the same answer. A file that carries changes of his own is never
    written, so what the run commits or puts back is its own work alone."""
    from .skills import WRITING_SKILLS
    env = ctx.env
    allowed = getattr(env, "caller_allowed", None) or set()
    if name not in allowed:
        return f"Refused: '{name}' is not one of the driver's tools."
    tgt = _drive_target(env, args) if name in DRIVE_TREE else None
    key = (str(tgt[0]), str(tgt[1])) if tgt else None
    if tgt and tgt[2] in ("HEAD", ""):
        return (f"Refused: {tgt[0].name} is not on a branch (a detached HEAD), so there is no "
                f"line of work to write on. Nothing was written.")
    if key and key not in d.item_files:
        _, dirty = _drive_run(["git", "status", "--porcelain", "--", _drive_rel(*key)], tgt[0])
        if dirty.strip():
            return (f"Refused: {_drive_rel(*key)} carries changes that are not the Steward's (not "
                    f"saved, or not in git), so it is not written: what the run commits or puts "
                    f"back must be its own work alone. Nothing was written.")
    opening = ("drive-" + time.strftime("%m%d-%H%M%S")) if tgt and tgt[2] in DRIVE_MAIN else ""
    if name in WRITING_SKILLS or name in DRIVE_ASKS:
        where = (f" (first opening the line of work `{opening}` in {tgt[0].name})"
                 if opening else "")
        answer = ctx.ask(f"The Steward wants to run {name} {_drive_brief(args)}{where}\n"
                         f"Approve? [y/n] ")
        if not _drive_yes(answer):
            return f"Declined by the operator: {name} did not run."
    if opening:
        code, out = _drive_run(["git", "switch", "-c", opening], tgt[0])
        if code:
            return f"Refused: the line of work `{opening}` could not be opened: {out}"
        d.repos[key[0]] = {"base": tgt[2], "line": opening}
    if key and key not in d.item_files:
        try:
            d.before[key] = Path(key[1]).read_bytes() if Path(key[1]).is_file() else None
        except OSError as exc:
            return f"Refused: {_drive_rel(*key)} could not be read before it was written: {exc}"
    try:
        result = str(ctx.skills.execute(name, args, env) or "")
    except Exception as exc:
        return f"Refused: {name} failed in the engine ({type(exc).__name__}: {exc})."
    if key and result.lstrip().startswith(("Wrote", "Edited")):
        d.repos.setdefault(key[0], {"base": "", "line": tgt[2]})
        d.item_files.add(key)
        d.touched.add(key)
    return result


def _drive_job(d, task: str, check: str, ctx, max_steps: int, max_minutes: float) -> str:
    """One job, worked until its check passes or its budget is spent."""
    started = time.time()
    said_check = check or "none named: the job is unchecked and ends when you call done"
    before = f"What was done before in this sitting:\n{ctx.carry}\n\n" if ctx.carry else ""
    messages: list = [
        {"role": "system", "content": DRIVE_SYSTEM},
        {"role": "user", "content": f"{before}Goal: {task}\nThe check that decides done: {said_check}"},
    ]
    # Thinking is off by default: on 2026-10-16 one step after a write thought
    # for over three minutes. MANJUEL_DRIVER_THINK=1 turns it back on.
    think = os.environ.get("MANJUEL_DRIVER_THINK", "").strip().lower() in ("1", "true", "yes")
    steps = 0

    def spent() -> bool:
        return steps >= max_steps or time.time() - started > max_minutes * 60

    while True:
        if spent():
            ctx.report(f"  budget spent: {steps} steps, {(time.time() - started) / 60:.1f} min")
            return "budget"
        try:
            resp = ctx.client.chat(model=ctx.model, messages=messages, tools=ctx.tools,
                                   options={"num_ctx": DRIVE_CONTEXT},
                                   keep_alive=ctx.keep_alive, think=think)
        except Exception as exc:
            d.error = f"{type(exc).__name__}: {exc}"
            ctx.report(f"  the model call failed: {d.error}")
            return "error"
        msg = _drive_field(resp, "message")
        messages.append(msg)
        # Words with no call are a claim that the job is done; the check decides,
        # exactly as it does for an explicit done.
        calls = drive_calls(msg) or [("done", {"summary": _drive_head(_drive_field(msg, "content"))})]
        for name, args in calls:
            if spent():
                break
            steps += 1
            d.n += 1
            n = d.n
            if name == "done":
                summary = str(args.get("summary") or "").strip() or "(no summary)"
                if not check:
                    d.steps.append([n, "done", summary, "no check named"])
                    ctx.report(f"  [{n}] done: {summary} -- no check named")
                    return "unchecked"
                ctx.report(f"  [{n}] done claimed: {summary}; running the check")
                ok, out = drive_check(check, ctx.ground)
                d.check_out = out
                d.steps.append([n, "check", check, out])
                ctx.report(f"  [{n}] check {'PASSED' if ok else 'FAILED'}: {_drive_head(out)}")
                if ok:
                    return "passed"
                messages.append({"role": "tool", "tool_name": "done",
                                 "content": f"The check failed:\n{out}"})
                continue
            result = drive_act(name, args, ctx, d)
            d.steps.append([n, name, args, result])
            ctx.report(f"  [{n}] {name} {_drive_brief(args)} -> {_drive_head(result)}")
            messages.append({"role": "tool", "tool_name": name,
                             "content": result[:DRIVE_RESULT_CHARS]})


def _drive_changes(d) -> str:
    """What the item in hand changed, read off git."""
    parts = []
    for repo, rels in _drive_by_repo(d.item_files).items():
        _, stat = _drive_run(["git", "diff", "--stat", "--"] + rels, repo)
        new = [x for x in rels if _drive_run(["git", "ls-files", "--error-unmatch", "--", x], repo)[0]]
        parts.append(f"{Path(repo).name}:" + (("\n" + stat) if stat else "")
                     + "".join(f"\n new file: {x}" for x in new))
    said = "\n".join(parts)
    d.n += 1
    d.steps.append([d.n, "diff", "", said or "(no difference)"])
    return said


def _drive_commit_item(d, label: str, report) -> bool:
    """Commit exactly the item's own files on its line, under his git name. True
    when every commit landed; a file whose commit failed stays the item's, put
    out of the index again, so no close can carry it anywhere."""
    title = " ".join(str(label).split())
    title = title if len(title) <= 72 else title[:69] + "..."
    ok = True
    for repo, rels in _drive_by_repo(d.item_files).items():
        c1, o1 = _drive_run(["git", "add", "--"] + rels, repo)
        c2, o2 = _drive_run(["git", "commit", "-m", title, "--"] + rels, repo) if c1 == 0 else (c1, o1)
        d.n += 1
        d.steps.append([d.n, "commit", Path(repo).name, f"exit {c2}\n{o2}"])
        report(f"  [{d.n}] commit in {Path(repo).name}: exit {c2} -- {_drive_head(o2)}")
        if c2 == 0:
            _, sha = _drive_run(["git", "rev-parse", "HEAD"], repo)
            d.made.setdefault(repo, []).append(sha.strip())
            for k in [k for k in d.item_files if k[0] == repo]:
                d.item_files.discard(k)
                d.before.pop(k, None)
        else:
            ok = False
            if c1 == 0:
                _drive_run(["git", "reset", "-q", "--"] + rels, repo)
    return ok


def _drive_put_back(d, report, label: str = "") -> None:
    """Put back exactly the item's own files, byte for byte as they were before it
    first wrote them (Nigel's reset, held to them); a file it made is removed."""
    done, kept = [], set()
    for key in sorted(d.item_files):
        x = _drive_rel(*key)
        if key not in d.before:
            kept.add(key)
            done.append(f"{x}: NOT put back -- no copy of it was kept")
            continue
        try:
            if d.before[key] is None:
                Path(key[1]).unlink(missing_ok=True)
                done.append(f"{x}: removed (the Steward made it)")
            else:
                Path(key[1]).write_bytes(d.before[key])
                done.append(f"{x}: put back")
            d.before.pop(key)
        except OSError as exc:
            kept.add(key)
            done.append(f"{x}: NOT put back -- {exc}")
    d.item_files = kept
    d.n += 1
    d.steps.append([d.n, "put back", label, "\n".join(done) or "nothing to put back"])
    report(f"  [{d.n}] put back: {_drive_head(chr(10).join(done) or 'nothing')}")


def _drive_close_lines(d, report, keep_pushed: bool = False) -> None:
    """Back to the base each line was opened from, and the line closed here: an
    unpushed line only when it carries no commit; a pushed one always (its commits
    are on GitHub and in its pull request). A line where a file the run wrote
    still differs is kept, so nothing of the run's is carried onto the base."""
    for key, r in d.repos.items():
        base, line = r.get("base"), r.get("line")
        if not base or not line or r.get("closed") or r.get("kept"):
            continue
        repo = Path(key)
        code, ahead = _drive_run(["git", "log", "--oneline", f"{base}..{line}"], repo)
        pushed = r.get("merged") or _drive_run(["git", "rev-parse", "--verify", "--quiet",
                                                 f"origin/{line}"], repo)[0] == 0
        if code or (ahead.strip() and not (pushed and keep_pushed)):
            continue
        rels = sorted(_drive_rel(*k) for k in d.touched if k[0] == key)
        dirty = _drive_run(["git", "status", "--porcelain", "--"] + rels, repo)[1] if rels else ""
        if dirty.strip():
            d.n += 1
            d.steps.append([d.n, "close line", repo.name,
                            f"`{line}`: kept -- files the run wrote still differ:\n{dirty}"])
            report(f"  [{d.n}] line `{line}` in {repo.name}: kept, files the run wrote still differ")
            continue
        c1, o1 = _drive_run(["git", "switch", base], repo)
        c2, o2 = _drive_run(["git", "branch", "-D", line], repo) if c1 == 0 else (c1, o1)
        r["closed"] = c2 == 0
        d.n += 1
        d.steps.append([d.n, "close line", repo.name,
                        f"`{line}`: " + ("closed here, back on " + base if c2 == 0 else "kept -- " + o2)])
        report(f"  [{d.n}] line `{line}` in {repo.name}: " + ("closed" if c2 == 0 else "kept"))


def drive_ship(d, ctx, confirmed: bool = False) -> None:
    """The whole pipeline, on his answer: push each line the run committed on,
    open its pull request into the base it came from, wait on CI; green, ask him
    to merge, then close the line here. His yes to the commit covers the push
    only when the run opened the line and made every commit on it; anything else
    is listed and asked for. The merge is his click on its own card."""
    for key, r in d.repos.items():
        repo, base, line = Path(key), r.get("base") or "", r.get("line") or ""
        if r.get("closed") or not line or line in DRIVE_MAIN:
            continue
        into = base or "main"
        code, ahead = _drive_run(["git", "log", "--oneline", f"{into}..{line}"], repo)
        if code or not ahead.strip():
            continue
        ours = set(d.made.get(key, []))
        foreign = [s for s in _drive_run(["git", "rev-list", f"{into}..{line}"], repo)[1].split()
                   if s not in ours]
        if not confirmed or foreign or not base:
            note = f" {len(foreign)} of them were not made by this run." if foreign else ""
            answer = ctx.ask(f"Push `{line}` in {repo.name} ({len(ahead.splitlines())} commit(s)), "
                             f"open a pull request into {into} and wait on CI?{note}\n{ahead[:1500]}\n"
                             f"Approve? [y/n] ")
            if not _drive_yes(answer):
                d.n += 1
                d.steps.append([d.n, "ship", repo.name, f"declined: `{line}` keeps its commits here, unsent"])
                continue
        title = d.goal if len(d.goal) <= 72 else d.goal[:69] + "..."
        body = f"{d.goal}\n\nThe check: {d.check or '(none)'}\n\nCommits on the line:\n{ahead[:3000]}"
        # A line that already has an open pull request (a fix pushed on top of
        # it) keeps that one: gh refuses a second, and CI runs again on the push.
        code, seen = _drive_run(["gh", "pr", "view", line, "--json", "url,state", "-q",
                                 'select(.state == "OPEN") .url'], repo)
        open_pr = seen.strip() if code == 0 and seen.strip().startswith("https://") else ""
        steps = [("push", ["git", "push", "-u", "origin", line], 180)]
        if open_pr:
            d.prs.append(open_pr)
            d.n += 1
            d.steps.append([d.n, "pull request", line, f"already open: {open_pr}"])
            ctx.report(f"  [{d.n}] pull request: already open -- {open_pr}")
        else:
            steps.append(("pull request", ["gh", "pr", "create", "--base", into, "--head", line,
                                           "--title", title, "--body", body], 120))
        steps.append(("ci", ["gh", "pr", "checks", line, "--watch", "--interval", "20"],
                      DRIVE_CI_SECONDS))
        if not _drive_steps(d, ctx, repo, tuple(steps)):
            # The send or CI did not pass: the line stays here, so a fix can be
            # made on it and pushed on top of its pull request.
            r["kept"] = "its send or its CI did not pass"
            continue
        # THE MERGE IS HIS CLICK (RULE 13): CI is green, and the card asks.
        answer = ctx.ask(f"CI passed on `{line}` in {repo.name}. Merge its pull request into {into} "
                         f"and delete the branch on GitHub? [y/n] ")
        if not _drive_yes(answer):
            d.n += 1
            d.steps.append([d.n, "merge", repo.name, "declined: the pull request waits for him on GitHub"])
            continue
        if _drive_steps(d, ctx, repo, (
                ("merge", ["gh", "pr", "merge", line, "--merge"], 180),
                ("delete branch", ["git", "push", "origin", "--delete", line], 120))):
            r["merged"] = into
            d.merged.append(line)
    _drive_close_lines(d, ctx.report, keep_pushed=True)
    for key, r in d.repos.items():
        if r.get("merged") and r.get("closed"):
            _drive_steps(d, ctx, Path(key), (
                ("update " + r["merged"], ["git", "pull", "--ff-only", "origin", r["merged"]], 180),))


def _drive_steps(d, ctx, repo, steps) -> bool:
    """Run the pipeline's commands in order, each on the record, stopping at the
    first that fails. True when every one exited 0."""
    for label, argv, secs in steps:
        if label == "ci":
            time.sleep(15)              # the checks register a moment after the pull request
        code, out = _drive_run(argv, repo, secs)
        d.n += 1
        d.steps.append([d.n, label, " ".join(argv[:3]), f"exit {code}\n{out}"])
        ctx.report(f"  [{d.n}] {label}: exit {code} -- {_drive_head(out)}")
        if label == "pull request" and code == 0:
            url = next((w for w in out.split() if w.startswith("https://")), "")
            if url:
                d.prs.append(url)
        if code:
            return False
    return True


def drive_plan(goal: str, check: str, ctx) -> list:
    """DECOMPOSE: the goal as a short list of items, from the model."""
    before = f"What was done before in this sitting:\n{ctx.carry}\n\n" if ctx.carry else ""
    msgs = [{"role": "system", "content": DRIVE_PLAN_SYSTEM},
            {"role": "user", "content": f"{before}Goal: {goal}\nThe check every item must pass: {check or '(none)'}"}]
    try:
        resp = ctx.client.chat(model=ctx.model, messages=msgs, options={"num_ctx": DRIVE_CONTEXT},
                               keep_alive=ctx.keep_alive, think=False)
    except Exception as exc:
        ctx.report(f"  the plan could not be asked: {type(exc).__name__}: {exc}")
        return []
    text = str(_drive_field(_drive_field(resp, "message"), "content") or "")
    i, j = text.find("["), text.rfind("]")
    try:
        got = json.loads(text[i:j + 1]) if 0 <= i < j else []
    except ValueError:
        got = []
    if not isinstance(got, list):
        return []
    return [str(x).strip() for x in got if str(x).strip()][:DRIVE_ITEMS_MAX]


def _drive_single(d, ctx) -> None:
    """ONE JOB: worked; on a pass, what changed, then on his answer the whole
    pipeline; on no pass, its own files put back on his answer."""
    d.verdict = _drive_job(d, d.goal, d.check, ctx, DRIVE_STEPS, DRIVE_MINUTES)
    if d.verdict in ("passed", "unchecked") and d.item_files:
        said = _drive_changes(d)
        if d.verdict == "unchecked":
            return              # nothing proves it: the change stays, unsaved, for his eyes
        answer = ctx.ask(f"The check passed. Commit these {len(d.item_files)} file(s) on the line of "
                         f"work, push it, open a pull request and wait on CI?\n{said}\n"
                         f"Approve? [y/n] ")
        if not _drive_yes(answer):
            d.n += 1
            d.steps.append([d.n, "ship", "", "declined: the change stays unsaved on its line of work"])
        elif _drive_commit_item(d, d.goal, ctx.report):
            drive_ship(d, ctx, confirmed=True)
    elif not d.item_files:
        _drive_close_lines(d, ctx.report)       # a line opened for a write that never landed
    else:
        answer = ctx.ask(f"The check did not pass. Put back the {len(d.item_files)} file(s) the Steward "
                         f"changed, and close the line it opened?\nApprove? [y/n] ")
        if _drive_yes(answer):
            _drive_put_back(d, ctx.report)
            _drive_close_lines(d, ctx.report)
        else:
            d.n += 1
            d.steps.append([d.n, "put back", "", "declined: the job's changes stay as they are"])


def drive_items(d, spec: dict, ctx) -> None:
    """PLAN or EACH: the items, one job each, on his answer; each passing item
    committed on the run's line, each failing one put back; the whole checked
    once more and, on his answer, shipped as one pull request."""
    import hashlib
    mode, goal, check, do = spec["mode"], spec["goal"], spec["check"], spec["do"]
    key = ""
    if mode == "plan":
        items = drive_plan(goal, check, ctx)
        if not items:
            d.verdict, d.error = "error", "the model gave no list of items for the goal"
            return
    else:
        items, why = drive_source(goal, ctx.ground)
        if items is None:
            d.verdict, d.error = "error", f"the source command failed: {why}"
            return
        key = "each:" + hashlib.sha1((goal + "|" + do).encode("utf-8")).hexdigest()[:12]
    seen = _drive_ignored(ctx.logs, key) if key else set()
    todo = [(it, _drive_key(it)) for it in items]
    todo = [(it, k) for it, k in todo if k not in seen][:DRIVE_ITEMS_MAX]
    d.n += 1
    d.steps.append([d.n, "items", mode, "\n".join(k for _, k in todo) or "(none left)"])
    if not todo:
        d.verdict = "nothing"
        return
    listing = "\n".join(f"  {i}. {k[:140]}" for i, (_, k) in enumerate(todo, 1))
    answer = ctx.ask(f"The Steward will work {len(todo)} item(s), each its own job, each checked by: "
                     f"{check}\n{listing}\nOn a line of work of its own: an item that passes is "
                     f"committed there, one that fails is put back; each write still asks. "
                     f"Approve the run? [y/n] ")
    if not _drive_yes(answer):
        d.verdict = "declined"
        return
    passed = 0
    for i, (it, k) in enumerate(todo, 1):
        text = it if isinstance(it, str) else json.dumps(it, ensure_ascii=False)
        if mode == "each":
            task = do.replace("$ITEM", text).replace("$INPUT", text)
        else:
            task = f"Overall goal: {goal}\nDo this item now ({i} of {len(todo)}), and only this item: {text}"
        ctx.report(f"  item {i}/{len(todo)}: {k[:120]}")
        v = _drive_job(d, task, check, ctx, DRIVE_ITEM_STEPS, DRIVE_ITEM_MINUTES)
        if v == "passed" and mode == "each":
            again, why = drive_source(goal, ctx.ground)
            if again is None or k in {_drive_key(x) for x in again}:
                v = "still listed" if again is not None else "source failed"
                ctx.report(f"  item {i}: " + ("the source still lists it" if again is not None
                                              else f"the source failed ({why})") + ", so it is not done")
        if v == "passed" and d.item_files and not _drive_commit_item(d, text, ctx.report):
            v = "commit failed"
        if v == "passed":
            passed += 1
        elif d.item_files:
            _drive_put_back(d, ctx.report, k[:60])
        d.items.append([k, v])
        if v == "error":
            break               # the model is down: what was not worked is not marked tried
        if key:
            _drive_ignore(ctx.logs, key, k, v)
    if d.items and d.items[-1][1] == "error":
        d.verdict = "error"
        _drive_close_lines(d, ctx.report)
        return
    whole = True
    if passed:
        whole, out = drive_check(check, ctx.ground)
        d.check_out = out
        d.n += 1
        d.steps.append([d.n, "check (all)", check, out])
        ctx.report(f"  [{d.n}] the whole, checked once more: {'PASSED' if whole else 'FAILED'}")
    if passed == len(todo) and whole:
        d.verdict = "passed"
    elif passed and whole:
        d.verdict = "partial"
    else:
        d.verdict = "failed"
    if passed and whole:
        drive_ship(d, ctx)
    else:
        _drive_close_lines(d, ctx.report)


def drive_tidy(d, ctx) -> None:
    """TIDY: every branch already merged into main, here and on GitHub, listed
    and deleted on one answer (the head of this section)."""
    found = []
    for sub in DRIVE_REPOS:
        repo = Path(ctx.ground) / sub if sub else Path(ctx.ground)
        if not (repo / ".git").exists():
            continue
        trunk = next((b for b in DRIVE_MAIN
                      if _drive_run(["git", "rev-parse", "--verify", "--quiet", b], repo)[0] == 0), "")
        if not trunk:
            continue
        fetched = _drive_steps(d, ctx, repo, (
            ("fetch " + repo.name, ["git", "fetch", "--prune", "origin"], 120),))
        _, here = _drive_run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
        # Merged into GITHUB's main once fetched: his own main falls behind every merge made there.
        ref = ("origin/" + trunk) if fetched else trunk
        _, loc = _drive_run(["git", "branch", "--merged", ref, "--format=%(refname:short)"], repo)
        local = [b for b in loc.split() if b not in DRIVE_MAIN and b != here.strip()]
        remote = []
        if fetched:
            _, rem = _drive_run(["git", "branch", "-r", "--merged", "origin/" + trunk,
                                 "--format=%(refname:short)"], repo)
            remote = [b[len("origin/"):] for b in rem.split() if b.startswith("origin/")
                      and b[len("origin/"):] not in DRIVE_MAIN + ("HEAD",)]
        if local or remote:
            found.append((repo, trunk, local, remote))
    d.n += 1
    d.steps.append([d.n, "merged branches", "", "\n".join(
        f"{r.name}: here {', '.join(l) or '-'}; on GitHub {', '.join(m) or '-'}" for r, _, l, m in found)
        or "(none)"])
    if not found:
        d.verdict = "clean"
        return
    listing = "\n".join(f"  {r.name} (merged into {t}): here {', '.join(l) or '-'}; "
                        f"on GitHub {', '.join(m) or '-'}" for r, t, l, m in found)
    answer = ctx.ask(f"These branches are already merged into main:\n{listing}\nDelete them all, here and "
                     f"on GitHub? (only what git itself lists as merged into main goes) "
                     f"Approve? [y/n] ")
    if not _drive_yes(answer):
        d.verdict = "declined"
        return
    ok = True
    for repo, _, local, remote in found:
        for b in local:
            ok = _drive_steps(d, ctx, repo, (("delete " + b, ["git", "branch", "-D", b], 60),)) and ok
        if remote:
            ok = _drive_steps(d, ctx, repo, (("delete on GitHub", ["git", "push", "origin", "--delete"]
                                              + remote, 180),)) and ok
    d.verdict = "tidy" if ok else "tidy_part"


def drive_save(d, spec: dict, ctx) -> None:
    """SHIP: the work on disk saved and sent (the head of this section). Each
    repository's changed and new files become one commit under his message, on a
    line opened from main, and drive_ship takes it from there."""
    message = spec["goal"]
    # The check first: it may move files itself (a map regenerated, the suites'
    # stamps), and what it moved belongs in the save.
    if spec["check"]:
        ok, out = drive_check(spec["check"], ctx.ground)
        d.check_out = out
        d.n += 1
        d.steps.append([d.n, "check", spec["check"], out])
        ctx.report(f"  [{d.n}] check {'PASSED' if ok else 'FAILED'}: {_drive_head(out)}")
        if not ok:
            d.verdict = "failed"
            return
    found = []
    for sub in DRIVE_REPOS:
        repo = Path(ctx.ground) / sub if sub else Path(ctx.ground)
        if not (repo / ".git").exists():
            continue
        code, branch = _drive_run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
        branch = branch.strip() if code == 0 else ""
        files = set()
        for argv in (["git", "ls-files", "-m", "-z"], ["git", "ls-files", "--others", "--exclude-standard", "-z"]):
            files |= {f for f in _drive_run(argv, repo)[1].split("\0") if f.strip()}
        ahead = ""
        if branch not in DRIVE_MAIN + ("HEAD", ""):
            ahead = _drive_run(["git", "log", "--oneline", "main.." + branch], repo)[1].strip()
        if files or ahead:
            found.append((repo, branch, sorted(files), ahead))
    d.n += 1
    d.steps.append([d.n, "to save", "", "\n".join(
        f"{r.name} on {b}: {', '.join(fs) or '(no files)'}" + (f"; not on main yet:\n{a}" if a else "")
        for r, b, fs, a in found) or "(nothing)"])
    if not found:
        d.verdict, d.error = "error", "there is nothing to save or send, here or in atlas"
        return
    barred = [f"{r.name}/{f}" for r, _, fs, _ in found for f in fs
              if f.split("/")[0] == "worlds" or Path(f).name == ".env"
              or (Path(f).name.startswith(".env.") and not Path(f).name.endswith(".example"))]
    loose = [r.name for r, b, _, _ in found if b in ("HEAD", "")]
    if barred or loose:
        d.verdict = "error"
        d.error = "ship refuses, and nothing was saved: " + "; ".join(
            ([f"{', '.join(barred)} is a secret or a world, never sent"] if barred else [])
            + ([f"{', '.join(loose)} is not on a branch"] if loose else []))
        return
    listing = "\n".join(
        f"  {r.name} on {b}: " + (f"{len(fs)} file(s): {', '.join(fs[:30])}" + (" ..." if len(fs) > 30 else "")
                                  if fs else "no files")
        + (f"; {len(a.splitlines())} commit(s) not on main yet" if a else "") for r, b, fs, a in found)
    title = message if len(message) <= 72 else message[:69] + "..."
    answer = ctx.ask(f"Save and send this as \"{title}\"?\n{listing}\nEach repository's files become one commit "
                     f"on a line of work, then the push, a PR into main and CI; the merge asks again. "
                     f"Approve? [y/n] ")
    if not _drive_yes(answer):
        d.verdict = "declined"
        return
    ok = True
    for repo, branch, files, _ in found:
        key = str(repo)
        if branch in DRIVE_MAIN:
            line = "drive-" + time.strftime("%m%d-%H%M%S")
            if not _drive_steps(d, ctx, repo, (("open line " + line, ["git", "switch", "-c", line], 60),)):
                ok = False
                continue
            d.repos[key] = {"base": branch, "line": line}
        else:
            d.repos[key] = {"base": "", "line": branch}
        if files and _drive_steps(d, ctx, repo, (
                ("stage", ["git", "add", "-A", "--"] + files, 120),
                ("save", ["git", "commit", "-m", message, "--"] + files, 120))):
            d.made.setdefault(key, []).append(_drive_run(["git", "rev-parse", "HEAD"], repo)[1].strip())
        elif files:
            ok = False
            _drive_run(["git", "reset", "-q", "--"] + files, repo)
    if not ok:
        d.verdict = "failed"
        _drive_close_lines(d, ctx.report)
        return
    drive_ship(d, ctx, confirmed=True)
    d.verdict = "shipped" if d.prs else ("unsent" if d.made else "failed")


def drive(spec, *, skills, env, ground, ask, report,
          host: str = "http://127.0.0.1:11434", keep_alive: str = "30m",
          logs=None, client=None, model: str = DRIVE_MODEL, carry: str = "") -> Drive:
    """Work one /drive to its end (the head of this section)."""
    from types import SimpleNamespace
    if isinstance(spec, str):
        spec = drive_parse(spec)
    d = Drive(spec["goal"] or spec["mode"], spec["check"], model)
    started = time.time()
    ground = Path(ground)
    if client is None:
        import ollama
        client = ollama.Client(host=host, timeout=DRIVE_CALL_SECONDS)
    tools, allowed = drive_tools(skills)
    ctx = SimpleNamespace(skills=skills, env=env, ground=ground, ask=ask, report=report,
                          client=client, tools=tools, keep_alive=keep_alive, model=model,
                          logs=Path(logs) if logs else ground / "logs", carry=carry)
    kept = (getattr(env, "caller", ""), getattr(env, "caller_allowed", None),
            getattr(env, "objective", ""))
    env.caller, env.caller_allowed, env.objective = "driver", set(allowed), spec["goal"]
    mode = "" if spec["mode"] == "goal" else " " + spec["mode"]
    report(f"  drive{mode}: {spec['goal']}")
    report(f"  check: {spec['check'] or 'none named (unchecked)'} | model {model}")
    try:
        if spec["mode"] in ("plan", "each") and not spec["check"]:
            d.verdict, d.error = "error", f"{spec['mode']} needs a check (| check: <command>) to decide each item"
        elif spec["mode"] == "goal":
            _drive_single(d, ctx)
        elif spec["mode"] == "tidy":
            drive_tidy(d, ctx)
        elif spec["mode"] == "ship":
            drive_save(d, spec, ctx)
        else:
            drive_items(d, spec, ctx)
    except EOFError:
        raise                   # his close: the door's loop serves it after the delivery
    except Exception as exc:
        d.verdict, d.error = "error", f"{type(exc).__name__}: {exc}"
        report(f"  the driver stopped: {d.error}")
    finally:
        env.caller, env.caller_allowed, env.objective = kept
        d.elapsed = time.time() - started
        d.transcript = drive_record(d, ctx.logs)
        d.report = drive_report(d)
    return d


def drive_report(d: Drive) -> str:
    """What happened, read off the record alone."""
    said = f"STOPPED: {d.error}" if d.verdict == "error" else DRIVE_SAID.get(d.verdict, "STOPPED.")
    if d.verdict == "passed":
        said += f" ({d.check})." if d.check else "."
    lines = [f"Steward drove: {d.goal}", said]
    if d.items:
        ok = sum(1 for _, v in d.items if v == "passed")
        lines.append(f"Items: {ok} of {len(d.items)} passed.")
        lines.extend(f"  - {v}: {k[:120]}" for k, v in d.items)
    for url in d.prs:
        lines.append(f"Pull request: {url}" + (" (merged on his click)" if d.merged
                                               else " (the merge waits for him on GitHub)"))
    lines.append(f"{len(d.steps)} steps in {d.elapsed:.0f}s on {d.model}. From the record:")
    for n, name, args, result in d.steps:
        lines.append(f"  {n}. {name} {_drive_brief(args)} -> {_drive_head(result)}")
    if d.check_out and d.verdict != "passed":
        lines.append("The check's last output:")
        lines.extend("  " + l for l in d.check_out.strip().splitlines()[-12:])
    if d.transcript:
        lines.append(f"Record: {d.transcript}")
    return "\n".join(lines)


def drive_carry(d: Drive) -> str:
    """One line of what a job did, carried into the next."""
    pr = f"; pull request {d.prs[-1]}" if d.prs else ""
    files = sorted({str(s[2]) for s in d.steps if s[1] == "commit" and str(s[3]).startswith("exit 0")})
    return f"- {d.goal[:200]} -> {d.verdict}" + (f"; committed in {', '.join(files)[:200]}" if files else "") + pr


def drive_record(d: Drive, logs) -> str:
    """The whole job as a transcript in logs/, every result as it came back."""
    if logs is None:
        return ""
    try:
        logs = Path(logs)
        name = time.strftime("%Y-%m-%d_%H%M%S") + "_drive.md"
        body = [f"# drive -- {d.goal}", "", f"- check: {d.check or '(none)'}",
                f"- model: {d.model}", f"- verdict: {d.verdict}",
                f"- elapsed: {d.elapsed:.1f}s", ""]
        for k, v in d.items:
            body.append(f"- item {v}: {k}")
        for n, tool, args, result in d.steps:
            body += [f"## {n}. {tool}", "", "args: " + _drive_brief(args), "",
                     "    " + str(result or "").replace("\n", "\n    "), ""]
        (logs / name).write_text("\n".join(body) + "\n", encoding="utf-8", newline="\r\n")
        return f"logs/{name}"
    except Exception:
        return ""


def door_drive(door, said: str) -> None:
    """The /drive turn: job after job. Each job's report goes on the wire as it
    ends; then the driver asks what is next, and a blank answer (or "stop") ends
    the turn in one delivery. What earlier jobs did is carried into the next,
    cut to its newest DRIVE_CARRY_CHARS. His close on any card ends the turn the
    same way, and the door's loop serves the close after the delivery."""
    sess = door.sess

    def report(line):
        print(line)
        door.wire.emit("report", text=str(line))

    rt = sess.runtime
    started, carry, reports, last = time.time(), "", [], ""
    while True:
        spec = drive_parse(said)
        if (not spec["goal"] and spec["mode"] != "tidy") or (spec["mode"] == "each" and not spec["do"]):
            print(DRIVE_USAGE)
            reports.append(DRIVE_USAGE)
        else:
            try:
                d = drive(spec, skills=sess.skills, env=sess.env, ground=door.ground,
                          ask=lambda prompt: door.ask(prompt, color="red"), report=report,
                          host=getattr(rt, "host", None) or "http://127.0.0.1:11434",
                          keep_alive=getattr(rt, "keep_alive", None) or "30m",
                          logs=door.ground / "logs", carry=carry)
            except EOFError:
                break
            reports.append(d.report)
            last = d.transcript or last
            for line in d.report.splitlines():
                report(line)
            carry = (carry + "\n" + drive_carry(d)).strip()[-DRIVE_CARRY_CHARS:]
            try:
                sess.sitting.runs.append({
                    "objective": ("/drive " + said)[:300], "pipeline": "drive",
                    "stages": len(d.steps), "failed": 0 if d.verdict in ("passed", "tidy", "clean") else 1,
                    "elapsed": d.elapsed, "transcript": d.transcript,
                    "tools": sorted({str(s[1]) for s in d.steps}), "guards": [],
                    "seats_failed": [], "out_of_time": [], "delivery": d.report[:200]})
            except Exception:
                pass
        try:
            nxt = door.ask("What is next? Type the next goal (plan ..., each ..., tidy and ship ... work too), "
                           "or leave it blank to stop.", color="green")
        except EOFError:
            break
        said = str(nxt or "").strip()
        if said.lower() in DRIVE_STOP:
            break
        if said.lower().startswith("/drive"):
            said = said[len("/drive"):].strip()
    text = "\n\n".join(reports)
    took = time.time() - started
    print(f"\n--- delivery · {took:.1f}s ---\n")
    print(text)
    door.wire.emit("delivery", text=text, elapsed=round(took, 1),
                   transcript=last, pipeline="drive", flags=[], notes=[],
                   failures=[], verdicts=[], out_of_time=[], project="", steps=[])


# A DOOR CALL, SAID PLAINLY (WHAT'S LEFT C77). His words, 2026-10-16: "it
# shouldn't take 60 seconds to send a damn approval, and it doesnt make sense
# that after ive approved the card, the thing is still blabbering on. it sends
# the card before it even states what its doing it for." A line that leads with
# mcp_call names its server, its tool and its arguments: it is decided already,
# so no seat reads it and no model narrates it. The engine says in one line what
# it asks the door for, then makes the call; when the door holds it for his
# Approve, the engine waits on the door's own hold log for his answer and says
# in one line what became of it. Every line is the call's own words or the log's.
DOOR_WAIT_SECONDS = 900.0
DOOR_HOLD_LOGS = ("state/holds.jsonl", "atlas/state/holds.jsonl")
DOOR_OUTCOMES = {
    "approved_ran": "approved on your card, and it ran",
    "denied": "denied on your card; nothing ran",
    "refused": "refused by the door when it was answered; nothing ran",
    "crossed": "answered elsewhere first; nothing more ran",
}


def door_hold_wait(ground, hold: str, seconds: float = DOOR_WAIT_SECONDS, tick: float = 1.0) -> str:
    """Wait on the door's hold logs until the hold is answered: its outcome, or
    '' when no answer came in time."""
    deadline = time.time() + seconds
    while True:
        for rel in DOOR_HOLD_LOGS:
            p = Path(ground) / rel
            try:
                lines = p.read_text(encoding="utf-8").splitlines()[-400:] if p.is_file() else []
            except OSError:
                lines = []
            for line in reversed(lines):
                if hold not in line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get("id") == hold and row.get("what") not in (None, "", "held"):
                    return str(row.get("what"))
        if time.time() >= deadline:
            return ""
        time.sleep(tick)


def door_call(door, said: str) -> None:
    """The mcp_call turn: one line of what is asked, the call, and -- when the
    door holds it -- the wait on his card and one line of what became of it."""
    import re
    sess = door.sess

    def report(line):
        print(line)
        door.wire.emit("report", text=str(line))

    started = time.time()
    asked = said.strip()[len("mcp_call"):].strip()
    words = asked.split(None, 2)
    tool = words[1] if len(words) > 1 else "the call"
    report(f"  asking the door: {asked[:400]}")
    try:
        result = str(sess.skills.execute("mcp_call", {"content": asked}, sess.env) or "")
    except Exception as exc:
        result = f"Refused: mcp_call failed in the engine ({type(exc).__name__}: {exc})."
    held = re.search(r"parked as (hold_[A-Za-z0-9_]+)", result) if result.startswith("HELD") else None
    what = ""
    if held:
        hold = held.group(1)
        report(f"  the card is at the foot of the terminal ({hold}); waiting for your click")
        what = door_hold_wait(door.ground, hold)
        text = f"{tool}: " + (DOOR_OUTCOMES.get(what, what) if what else
                              f"no answer in {DOOR_WAIT_SECONDS / 60:.0f} minutes; the card stays in the dock") + "."
    elif tool == "suite_run" and "did not answer inside" in result:
        # C71: the door runs the suites on past the call's bound and stamps them
        # itself; the tally is the engine's own proved skill, read once the run
        # has finished -- never a second reader of the same stamp.
        report("  the suites run on past the call's bound; waiting on their own stamp")
        deadline = time.time() + DOOR_WAIT_SECONDS
        text = ""
        while time.time() < deadline:
            text = str(sess.skills.execute("proved", {}, sess.env) or "")
            if "DID NOT FINISH" not in text:
                break
            time.sleep(2)
        text = "suite_run: " + text
    else:
        text = result
    took = time.time() - started
    failed = text.startswith("Refused") or bool(held and what != "approved_ran")
    try:
        sess.sitting.runs.append({
            "objective": said[:300], "pipeline": "door", "stages": 1, "failed": int(failed),
            "elapsed": took, "transcript": "", "tools": ["mcp_call"], "guards": [],
            "seats_failed": [], "out_of_time": [], "delivery": text[:200]})
    except Exception:
        pass
    print(f"\n--- delivery · {took:.1f}s ---\n")
    print(text)
    door.wire.emit("delivery", text=text, elapsed=round(took, 1),
                   transcript="", pipeline="door", flags=[], notes=[],
                   failures=[], verdicts=[], out_of_time=[], project="", steps=[])


# ---------------------------------------------------------------------
# the door
# ---------------------------------------------------------------------


class Door:
    """One sitting, over one wire. `sess` is cli.Session or anything that
    stands where it stands (the suites hand in a stand-in)."""

    def __init__(self, sess, wire: Wire, inbox: Inbox, ground: Path | None = None,
                 closer=None, idle_close: float | None = None):
        from . import cli as _cli
        self.sess = sess
        self.wire = wire
        self.inbox = inbox
        self.ground = Path(ground) if ground else _cli.ROOT
        # What closes the sitting: cli._close (the toll, the ledger line,
        # "bye"). The suites hand in a stand-in so no stroke pays a toll
        # into the record it runs beside.
        self.closer = closer if closer is not None else _cli._close
        # How long the door waits for a command between turns before it closes
        # the sitting itself (IDLE_CLOSE). The suites hand in seconds.
        self.idle_close = IDLE_CLOSE if idle_close is None else float(idle_close)
        self.asked = 0
        # Whether the turn in hand was sent as `unattended` (the wire, above).
        self.unattended = False
        self._deferred: list[dict] = []
        if not isinstance(getattr(sess, "runtime", None), _Runtime):
            sess.runtime = _Runtime(sess.runtime, wire)

    # ---- the keyboard --------------------------------------------------

    def ask(self, prompt: str = "", color: str = "amber") -> str:
        """Stands where input() stood. One question, one answer, over the
        wire; a cancel here is Ctrl-C and a close is Ctrl-D, which is what
        every input() site in cli.py and pipeline.py already handles. The
        card's color rides with the question (2026-10-12, his word: amber for
        reads and approvals, green for moving up or waking a seat, red for
        code edits and file writes); input() itself asks amber."""
        self.asked += 1
        self.inbox.set_state(Inbox.ASKING)
        self.wire.emit("needs_answer", id=self.asked, prompt=str(prompt or ""),
                       color=color if color in ("amber", "green", "red") else "amber")
        try:
            while True:
                row = self.inbox.take()
                if row is None:
                    raise EOFError("the client hung up")
                cmd = row.get("cmd")
                if cmd == "answer":
                    return str(row.get("text") or "")
                if cmd == "cancel":
                    raise KeyboardInterrupt
                if cmd == "close":
                    self._deferred.append(row)
                    raise EOFError("closed while a question was pending")
                if cmd == "objective":
                    # Not an answer. Kept for after the question, in order.
                    self._deferred.append(row)
                    self.wire.emit("note",
                                   text="a question is pending (needs_answer); "
                                        "the objective waits until it is answered")
                    continue
        finally:
            self.inbox.set_state(Inbox.RUNNING)

    def _listen(self, row: dict) -> None:
        """One spoken turn, captured and transcribed, and NOT run.

        voice.listen() is the REPL's own call: it calibrates against the
        room, ends the turn when the operator goes quiet, transcribes on
        the compiled whisper.cpp and applies correct_hearing() so the
        estate's proper nouns survive. Nothing is reimplemented here; if
        the REPL can hear, so can the glass, and neither can drift.

        The text comes back as `heard` and stops there. A microphone that
        fired objectives at the council on its own would be a gate nobody
        holds, and a misheard word would run before he had read it.

        Every failure is voice.py's own sentence on an `error` event,
        which is NOT terminal on this wire: a bad capture ends the
        capture, never the sitting.
        """
        from . import voice
        seconds = voice.MAX_TURN_SECONDS
        try:
            asked = int(row.get("seconds") or 0)
            if asked > 0:
                seconds = min(asked, voice.MAX_TURN_SECONDS)
        except (TypeError, ValueError):
            pass
        try:
            said = voice.listen(
                seconds,
                report=lambda m: self.wire.emit("note", text=str(m).strip()))
        except voice.VoiceError as exc:
            self.wire.emit("error", text=str(exc))
            return
        except Exception as exc:                      # a dead device, a bad driver
            self.wire.emit("error", text=f"the microphone failed: {exc}")
            return
        self.wire.emit("heard", text=said)

    def _next(self) -> dict | None:
        if self._deferred:
            return self._deferred.pop(0)
        # Bounded: the one wait in this door that is not inside a turn.
        return self.inbox.take(timeout=self.idle_close)

    # ---- the loop ------------------------------------------------------

    def serve(self) -> int:
        """cli._loop's shape: take a turn, run it, until close or EOF."""
        from . import cli as _cli
        real_input = builtins.input
        builtins.input = self.ask
        # ...and the colored card's hook beside it (pipeline._ask, 2026-10-12).
        builtins.ask_card = self.ask
        try:
            while True:
                self.inbox.set_state(Inbox.IDLE)
                row = self._next()
                if row is None:
                    self._close("the client hung up")
                    return 0
                cmd = row.get("cmd")
                if cmd == "_timeout":
                    # Nothing came for IDLE_CLOSE: the client's own close, unasked.
                    span = (f"{self.idle_close / 60:g} minutes" if self.idle_close >= 60
                            else f"{self.idle_close:g} seconds")
                    print(f"\n  No command in {span} -- closing the sitting. "
                          f"(the record keeps)\n")
                    self._close(f"idle: no command in {span}")
                    return 0
                if cmd == "close":
                    self._close("closed by the client")
                    return 0
                if cmd == "listen":
                    self._listen(row)
                    continue
                if cmd == "cancel":
                    self.wire.emit("note", text="nothing is running; nothing to cancel")
                    continue
                if cmd == "answer":
                    self.wire.emit("note", text="no question is pending; the answer was dropped")
                    continue
                if cmd != "objective":
                    continue
                objective = str(row.get("text") or "").strip()
                feed = str(row.get("feed") or "")
                method = str(row.get("method") or "")
                # Per turn, and only the literal `true`: a turn that does not
                # say so is attended, as every turn was before 2026-09-29.
                self.unattended = row.get("unattended") is True
                # THE HEAD IS A PROPERTY OF THE TURN (2026-09-23, his ruling:
                # "let's do C first"). A caller may name the model this one
                # turn runs on, which is what makes two runs of the same
                # question comparable -- the flow says WHAT to ask and the run
                # says WHICH head, so a spec never has to carry a model name
                # and two conditions can never drift into two experiments.
                #
                # IT IS `/model`'s MECHANISM AND NOT A SECOND ONE: the whole
                # roster moves, `agents/*.md` is never written to, and the turn
                # puts it back.
                #
                # `voices` IS THE NARROWER ONE (2026-09-23, "then B underneath
                # it"): seat -> model, applied OVER `model`, so "everything on
                # X except the Steward on Y" is one turn and one record. A
                # parity of the Steward is a question about the Steward, and
                # moving the Router in the same breath makes the answer a fact
                # about two changes at once -- which is the caveat this
                # morning's parity carries.
                model = str(row.get("model") or "").strip()
                voices = row.get("voices") or {}
                restore = False
                if model or voices:
                    plan, why = self._head_plan(model, voices)
                    if why:
                        # NOTHING IS APPLIED BEFORE EVERYTHING IS CHECKED. A
                        # `voices` map refused halfway would leave the roster
                        # part-moved with no turn to put it back.
                        self.wire.emit("refused", text=why)
                        continue
                    for seat, tag in plan:
                        if seat is None:
                            self.sess.registry.override_model(tag)
                        else:
                            self.sess.registry.override_seat(seat, tag)
                    restore = True
                    self.wire.emit("note", text=(
                        f"this turn runs {self._head_words(plan)}; the declared "
                        f"targets in agents/*.md are untouched and come back "
                        f"when it ends"))
                if feed.strip():
                    self.sess.pending_feed = feed.strip()      # /paste's shape
                if method.strip():
                    self.sess.pending_method = method.strip()  # a command's method
                self.inbox.set_state(Inbox.RUNNING)
                self.wire.ended = False
                try:
                    if not self.turn(objective):
                        return 0
                    # A turn that ran no pipeline -- a /command, @seat, the
                    # toll, a remember cue, an empty line -- printed its
                    # words and returned. Nothing told the client it was
                    # over, and a client pumps until something does.
                    if not self.wire.ended:
                        self.wire.emit("command", text=objective)
                except KeyboardInterrupt:
                    # A cancel that landed after the model call returned --
                    # in the tail of the turn, or at a command. The turn is
                    # over either way; the sitting is not.
                    print("\n\nRun cancelled.\n")
                    self.wire.emit("cancelled", notes=[], seats=[])
                finally:
                    # A HEAD NAMED FOR ONE TURN LEAVES WITH IT. `sess.load()`
                    # re-reads agents/*.md and re-applies any standing /model
                    # the operator set by hand, so the next turn runs on what
                    # the ground declares -- an override that outlived its turn
                    # would make every run after it a measurement of something
                    # nobody asked for, and the record would not say so.
                    if restore:
                        self.sess.load()
        finally:
            builtins.input = real_input
            builtins.__dict__.pop("ask_card", None)

    # ---- the head this turn runs on ------------------------------------

    def _head_plan(self, model: str, voices) -> tuple[list, str]:
        """Read `model` and `voices` off the wire into a plan, or refuse.

        Returns `(plan, "")` or `([], why)`. A plan is an ordered list of
        `(seat_or_None, tag)`: `None` is the whole roster, and it comes first
        so a per-seat entry lands OVER it rather than under it.

        EVERYTHING IS CHECKED BEFORE ANYTHING IS APPLIED. A map refused on its
        third entry after moving the first two would leave the roster
        part-moved on a turn that never ran -- so there would be no `finally`
        to put it back and the next turn would silently measure the leftovers.

        THE RACK IS ASKED ONCE, for every tag at once. RULE 4: nothing is
        pulled at run time, so a tag the rack does not have must be refused
        here by name -- run anyway and it fails every seat one at a time with
        the cause four stages back. A rack that cannot be ASKED is refused the
        same way: unreachable is not agreed.
        """
        if not isinstance(voices, dict):
            return [], (f"`voices` must be an object of seat -> model, got "
                        f"{type(voices).__name__}; the turn was not run")
        named = [str(v or "").strip() for v in voices.values()]
        if model:
            named.append(model)
        if any(not t for t in named):
            return [], ("`voices` names a seat with an empty model; the turn "
                        "was not run rather than run on nothing")
        try:
            have = self.sess.runtime.installed_models(refresh=True)
        except Exception as exc:
            return [], (f"cannot reach the rack to check {sorted(set(named))} "
                        f"({exc}); the turn was not run rather than run on a "
                        f"head nobody confirmed")
        tagged = {t: (t if ":" in t else f"{t}:latest") for t in named}
        missing = sorted({tagged[t] for t in named if tagged[t] not in have})
        if missing:
            return [], (f"{', '.join(repr(m) for m in missing)} not installed, "
                        f"so this turn was not run (RULE 4: models are never "
                        f"pulled at run time). The rack has: "
                        f"{', '.join(sorted(have))}")
        # The seats are checked here too, and by the same rule: a typo that
        # quietly moved nothing would report a parity between a model and
        # itself, which is the one answer a parity must never be able to give.
        unknown = sorted(s for s in voices if not self.sess.registry.has(str(s)))
        if unknown:
            roster = ", ".join(sorted(a.name for a in self.sess.registry.all()))
            return [], (f"no seat named {', '.join(repr(s) for s in unknown)}, "
                        f"so this turn was not run. The roster is: {roster}")
        plan: list = []
        if model:
            plan.append((None, tagged[model]))
        for seat in sorted(voices, key=lambda s: str(s).lower()):
            plan.append((str(seat), tagged[str(voices[seat] or "").strip()]))
        return plan, ""

    @staticmethod
    def _head_words(plan: list) -> str:
        """The plan in the operator's words, for the `note` that says what
        this turn moved. The record has to name it or a parity's two runs are
        two numbers with nothing attached."""
        parts = [f"every seat on {tag}" if seat is None else f"{seat} on {tag}"
                 for seat, tag in plan]
        return ", then ".join(parts)

    def _close(self, why: str) -> None:
        st = self.sess.sitting
        # WHY, ON THE LEDGER LINE AND IN THE TOLL (2026-09-29). The `closed`
        # event has always carried the reason to the client; the record kept
        # none, so an engine that closed itself after thirty idle minutes and
        # one the operator closed from the Dashboard read the same afterwards.
        try:
            st.closed_by = str(why or "")
        except Exception:
            pass
        try:
            self.closer(self.sess)
        except Exception as exc:
            self.wire.emit("error", text=f"close: {type(exc).__name__}: {exc}")
        self.wire.emit("closed", why=why, sitting=getattr(st, "n", None),
                       runs=len(getattr(st, "runs", []) or []),
                       toll_paid=bool(getattr(st, "toll_paid", False)))

    # ---- one turn ------------------------------------------------------

    def turn(self, objective: str) -> bool:
        """One typed turn, cli._loop's body line for line (the REPL read of
        2026-09-08 is the reference; a divergence here is a bug here).
        Returns False when the turn closed the sitting."""
        from . import cli as _cli
        from . import transcript, spelling, voice
        from . import seatlog as _log
        from .context import RunContext
        from .drift import DriftChecker
        from .intent import wants_out
        from .pipeline import Aborted, Refused, run_pipeline
        from .runtime import BackendUnreachable, RuntimeError_
        from .skills import EMBED_MODEL

        sess = self.sess
        print(_cli.BAR)
        if not objective:
            return True
        print(f"Objective: {objective}")
        if objective.lower() in ("exit", "quit") or wants_out(objective):
            print(f"\n  Alright — closing the sitting. (the record keeps)\n")
            self._close("the objective asked out")
            return False

        _cli._apply_ground_changes(sess)
        _watch_skills(sess.skills, self.wire)

        # STEWARD DRIVES (WHAT'S LEFT H31): the goal goes to the driver, above.
        if objective.split(None, 1)[0].lower() == "/drive":
            door_drive(self, objective[len("/drive"):].strip())
            return True
        # A DOOR CALL, SAID PLAINLY (WHAT'S LEFT C77): a line that leads with mcp_call is
        # decided already, so no seat reads it -- door_call, in the driver's section.
        if objective.split(None, 1)[0].lower() == "mcp_call":
            door_call(self, objective)
            return True

        if _cli._topic_turn(sess, objective):
            return True

        low = objective.lower().strip()
        if "pay the toll" in low or low.rstrip(".!?") == "the toll":
            _cli._cmd_toll(sess, attended=True)
            return True
        cued, words = _cli.remember_cue(objective)
        if cued:
            _cli._cmd_remember_that(sess, words)
            return True

        if objective.startswith("@"):
            if _cli._address_seat(sess, objective):
                return True
        try:
            if _cli.handle_command(objective, sess):
                _watch_skills(sess.skills, self.wire)      # /reload rebuilt it
                return True
        except SystemExit:
            self._close("/exit")
            return False

        if not sess.rack_ok and not sess.rack_check():
            print("\n  The rack is still unreachable — `ollama serve`, then "
                  "just ask again.\n")
            self.wire.emit("unreachable", text="the rack is unreachable; no run")
            return True

        ctx = RunContext(objective=objective, feed=sess.pending_feed,
                         dialogue=_cli._dialogue_for(sess, objective),
                         method=sess.pending_method,
                         review_only=sess.pipeline_name in ("court", "estate"),
                         standing=getattr(sess, "standing", ""),
                         story=_log.story_block(sess.sitting),
                         unattended=bool(getattr(self, "unattended", False)),
                         # THIS DOOR IS THE GLASS'S (context.screen): what the maker
                         # makes is framed on a screen, so no file is to be opened
                         screen=True)
        sess.pending_feed = ""
        sess.pending_method = ""
        sess.last_run_ref = f"logs/{transcript.name_for(ctx)}"
        print("\nRunning pipeline...")
        self.wire.emit("run", objective=objective, pipeline=sess.pipeline_name,
                       transcript=sess.last_run_ref, feed_chars=len(ctx.feed),
                       review_only=ctx.review_only)

        def report(line):
            print(line)
            self.wire.emit("report", text=str(line))

        try:
            run_pipeline(
                ctx,
                sess.registry,
                sess.runtime,
                sess.skills,
                sess.env,
                steps=sess.pipeline,
                report=report,
                stream=True,
                drift=DriftChecker(sess.runtime, EMBED_MODEL),
            )
        except Refused as exc:
            print(f"\n  REFUSED: {exc}")
            print("  The run did not proceed. Nothing downstream saw this input.\n")
            self.wire.emit("refused", text=str(exc), notes=list(ctx.notes))
            return True
        except Aborted as exc:
            print(f"\nRun aborted: {exc}\n")
            self.wire.emit("aborted", text=str(exc), notes=list(ctx.notes))
            return True
        except KeyboardInterrupt:
            print("\n\nRun cancelled.\n")
            self.wire.emit("cancelled", notes=list(ctx.notes),
                           seats=[s.agent for s in ctx.steps])
            return True
        except BackendUnreachable as exc:
            print(f"\n{exc}\n")
            self.wire.emit("unreachable", text=str(exc))
            return True
        except RuntimeError_ as exc:
            print(f"\nRuntime error: {exc}\n")
            self.wire.emit("error", text=str(exc), notes=list(ctx.notes))
            return True

        sess.last = ctx
        _final = ctx.last_output().strip()
        if _final:
            sess.dialogue.append(("operator", ctx.objective, time.time()))
            sess.dialogue.append(("steward", _final, time.time()))
            _cli.save_thread(self.ground, sess.session, sess.dialogue)

        name = sess.pipeline_name
        logged = ""
        try:
            record, _ = transcript.write(ctx, self.ground / "logs", pipeline=name)
            logged = f"logs/{record.name}"
            where = f"  logged: {logged}"
            sess.sitting.runs.append(vars(_log.note_for(ctx, name, logged)))
        except Exception as exc:
            where = f"  (transcript not written: {exc})"

        print(f"\n--- delivery · {ctx.elapsed:.1f}s ---\n")
        body = ctx.last_output().strip()
        if body:
            result = spelling.check(body)
            if result.changed or result.fault:
                body = result.text
                ctx.notes.append(result.note())
        if not body:
            print("  (no seat produced an answer this run)")
            for n in ctx.notes:
                print(f"  - {n}")
        else:
            print(body)
        print()
        print(where)
        print()

        # WHAT THE TOOLS SAID, beside what the seats said about it. A client
        # scoring a turn -- a flow's eval node is the one that found this --
        # was left reading the delivery, which is a seat's paraphrase of the
        # run. The verdict lines are the machine's own words and were being
        # collected and thrown away at this boundary.
        from .context import tool_verdicts as _verdicts

        # THE PROJECT IN HAND after this turn (the maker, piece 2), by folder
        # name, or "" for none. It lives in this process's memory and nowhere
        # else, so the glass's project list learns which one is picked up from
        # here -- read off the maker, never off a seat's words.
        from . import maker as _maker
        try:
            _g = getattr(sess.env, "ground", None)
            _held = _maker.current(_g) if _g is not None else None
        except Exception:
            _held = None

        self.wire.emit(
            "delivery", text=body, elapsed=round(ctx.elapsed, 1), transcript=logged,
            pipeline=name, flags=sorted(ctx.flags), notes=list(ctx.notes),
            failures=[list(f) for f in ctx.failures],
            verdicts=_verdicts(ctx.steps),
            out_of_time=list(ctx.out_of_time),
            project=_held.name if _held is not None else "",
            steps=[{"seat": s.agent, "model": s.model, "elapsed": round(s.elapsed, 1),
                    "tools": list(s.tool_calls or []), "error": s.error or "",
                    "skipped": bool(s.skipped), "chars": len(s.output or ""),
                    "drift": s.drift, "drifted": bool(s.drifted)}
                   for s in ctx.steps])

        if sess.speaking and body:
            try:
                voice.speak(body, blocking=False, voice=_cli._voice_for(sess, ctx))
            except voice.VoiceError as exc:
                print(f"  (not spoken: {exc})")
                print()
        return True


# ---------------------------------------------------------------------
# main: cli.main's boot, then the door
# ---------------------------------------------------------------------


def open_wire(out=None, source=None) -> tuple[Wire, Inbox]:
    """The real stdout and stdin as the wire. stdout is swapped for the
    text channel HERE, before anything can ask ink whether it is a
    terminal."""
    real = out if out is not None else sys.stdout
    try:
        real.reconfigure(encoding="utf-8", errors="replace")   # type: ignore[attr-defined]
    except Exception:
        pass
    src = source if source is not None else sys.stdin
    try:
        src.reconfigure(encoding="utf-8", errors="replace")    # type: ignore[attr-defined]
    except Exception:
        pass
    wire = Wire(real)
    sys.stdout = TextChannel(wire)
    inbox = Inbox(src, wire)
    return wire, inbox


def main(argv: list[str] | None = None) -> int:
    from . import cli as _cli
    from . import dotenv
    from . import seatlog as _log
    from .skills import EMBED_MODEL

    wire, inbox = open_wire()
    inbox.start()
    _mark("wire open")

    # THE GROUND, first (cli.main's shape): `--ground <path>` sits the door
    # inside a world; a bad path is refused on the wire, never created.
    try:
        ground = _cli.ground_from_argv(sys.argv[1:] if argv is None else argv)
    except ValueError as exc:
        wire.emit("error", text=f"{_cli.GROUND_FLAG} refused: {exc}")
        wire.emit("closed", why="ground refused", sitting=None, runs=0,
                  toll_paid=False)
        return 1
    if ground is not None:
        _cli.set_ground(ground)
    ROOT = _cli.ROOT

    # cli.main, line for line, with the prints landing on the wire as text.
    print("\nManjuel -- local multi-agent pipeline (headless door)")
    if ground is not None:
        print(f"  ground: {ROOT}")
    # .env is read AFTER import: every dial a module took at import, and every
    # old CHAINKIT_ name, predates this line. read_dials carries the old names
    # and has those modules read their dials again, before the Session is built.
    from . import read_dials
    _dotenv_lines = dotenv.report(*dotenv.load(ROOT / ".env"))
    read_dials()
    for line in _dotenv_lines:
        print(line)

    _mark("dotenv read")
    sess = _cli.Session()
    door = Door(sess, wire, inbox, ground=ROOT)
    if not sess.load():
        wire.emit("error", text="the declarations did not load; see the text above")
        wire.emit("closed", why="declarations did not load", sitting=None,
                  runs=0, toll_paid=False)
        return 1
    _mark("declarations loaded")
    if not sess.rack_check():
        print("\n  RACK UNREACHABLE — the ground is open, the models are not.")
        print("  Start `ollama serve` whenever; Manjuel reconnects on the "
              "next turn.\n")
    elif not sess.preflight():
        wire.emit("error", text="preflight failed; see the text above")
        wire.emit("closed", why="preflight failed", sitting=None, runs=0,
                  toll_paid=False)
        return 1

    _mark("rack checked")
    # A LOCK HELD BY NOBODY IS RELEASED HERE TOO (2026-09-22). cli.main has
    # reaped since 2026-09-17; this door never did, and it is the one THE LINE
    # spawns -- so a crashed engine's line stood open until someone opened a
    # REPL on that world, and the door refused the world until then. Closes
    # ONLY what it can prove is dead: a recorded pid that no longer exists.
    try:
        _log.reap_orphans(ROOT, report=print)
    except Exception as exc:
        print(f"  (the orphan check could not run: {exc})")
    _log.record(ROOT, sess.sitting)
    _mark("sitting line written")
    # EVERY EXIT FROM HERE ON CLOSES THE SITTING (2026-09-22). The line above
    # is written before anything below can fail, and until today only
    # door.serve() was guarded: a fault in the git read, the warm, the
    # watcher, the boot report or the thread read left the sitting open with
    # no process behind it, and a Ctrl-C anywhere here -- or a cancel that
    # landed as a turn ended, which interrupt_main delivers the same way --
    # left manjuel.py's `sys.exit(130)` as the only close there was.
    try:
        return _open_and_serve(sess, door, wire, ROOT, EMBED_MODEL)
    except KeyboardInterrupt:
        print("\n  interrupted -- closing the sitting so the ledger does not hold it open.")
        if not sess.sitting.ended:
            door._close("interrupted")
        return 130
    except Exception as exc:
        # cli.main's shape: close the sitting so the ledger does not hold it
        # open, THEN show the fault whole.
        print(f"\n  !! unhandled: {type(exc).__name__}: {exc}")
        print("  closing the sitting so the ledger does not hold it open.")
        wire.emit("error", text=f"unhandled: {type(exc).__name__}: {exc}")
        try:
            if not sess.sitting.ended:
                door._close("unhandled fault")
        finally:
            raise


def _open_and_serve(sess, door: Door, wire: Wire, ROOT: Path, EMBED_MODEL: str) -> int:
    """Everything after the sitting line: the boot the REPL does, `opened`,
    then the door. main() guards all of it, so nothing here can leave the
    sitting open behind a dead process."""
    from . import cli as _cli
    from . import boot, gitstate, ink
    from . import watch as _watch
    from .skills import index_roots

    g0 = gitstate.read(ROOT)
    _mark("git read")
    print(f"  sitting {sess.sitting.n} · session {sess.session} · {g0.stamp()}")
    print()

    if os.environ.get("MANJUEL_NO_WARM", "").strip() not in ("1", "true", "yes"):
        if sess.rack_ok:
            _cli._cmd_warm(sess, quiet=True)
            sess._bg_warm = _cli._warm_reasoner_later(sess)
        sess.watcher = _watch.GroundWatch(ROOT, roots=index_roots(sess.env))
        if sess.watcher.start():
            print(ink.dim("  watching the ground — edits reload and reindex "
                          "themselves between turns"))
        else:
            sess.watcher = None
    _mark("warm + watcher done")

    for line in boot.report(sess, ROOT, EMBED_MODEL, git=g0):
        print(line)
    _mark("boot.report done")
    print()
    try:
        for line in boot.brief_facts(sess, ROOT, git=g0):
            print(line)
        print("  /brief has the door say it\n")
    except Exception as exc:
        print(ink.dim(f"  (the brief could not be read: {exc})\n"))
    _mark("brief done")
    origin, prior = _cli.load_thread(ROOT)
    _mark("thread read")
    if prior:
        print(f"  a thread from {origin} is on file "
              f"({len(prior) // 2} turns) — /resume picks it up")

    wire.emit("opened", protocol=PROTOCOL, sitting=sess.sitting.n,
              session=sess.session, git=g0.stamp(), rack_ok=bool(sess.rack_ok),
              pipeline=sess.pipeline_name, pipelines=sess.pipeline_names(),
              seats=[a.name for a in sess.registry.all()],
              commands=list(COMMANDS), events=list(EVENTS))

    _mark("OPENED emitted")
    return door.serve()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
