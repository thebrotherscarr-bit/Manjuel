"""Guards for Steward's loop: when to warn, when to stop, when to try again.

The driver (serve.py `_drive_job`) asks the model for calls until a check
passes or the budget is spent. The budget alone is a poor brake. A small model
that has lost its way does not wander -- it repeats: the same read with the
same arguments, or two calls in turn (read, edit, read, edit), each one
answered the same way, until forty steps are gone and nothing moved. And a
model whose every call is refused, turn after turn, is not going to be saved
by the next turn either. Those are the two loops this file names, with the
numbers the proven harnesses settled on:

  SAME CALL     three in a row is a warning put to the MODEL, in words it can
                act on; five is a stop. (OpenHands' stuck detector and
                opencode's doom-loop guard both stop on a short run of
                identical calls; three and five leave room for a re-read.)
  A CYCLE       a run of two to four calls repeated -- A,B,A,B -- is warned
                when it has come round twice and stopped at the third time.
  FAILED TURNS  a turn in which EVERY call failed counts; any success clears
                the count; three in a row is a stop. (Cline's mistake limit.)

The third thing here is RETRY. A model call can fail for a reason that has
nothing to do with the job -- Ollama reloading, a socket reset, a 503 -- and
one such blip ends the job today. Ollama also answers a malformed tool call
with status 500 (WHAT'S LEFT C126), and a second sample is usually well
formed. Those are tried again with a doubling wait. A 404 (no such model), a
400 (a bad request) or a ValueError is the same on every try, so it is not.

A call to `done` is never counted as a repeat: the check decides done, and a
model that claims it twice is answered by the check, not by this file.

Standard library only; nothing here touches the network or the disk.
"""

from __future__ import annotations

import json
import re
import time

from .context import FAILED_HEADS

# The numbers (see the docstring for where they come from).
WARN_REPEATS = 3        # identical calls in a row before the model is warned
STOP_REPEATS = 5        # identical calls in a row before the job is stopped
FAILED_TURNS = 3        # turns in a row where every call failed
CYCLE_MAX = 4           # the longest repeating run of calls that is looked for

DONE = "done"


def failed(result) -> bool:
    """True when a tool's result is a refusal or an error: it begins with one of
    FAILED_HEADS, the one list the loop, the recompose and the wire all read."""
    return str(result).lstrip().startswith(FAILED_HEADS)


def call_key(name: str, args) -> str:
    """One string per call: its name and its arguments as canonical JSON, keys
    sorted, so {"a":1,"b":2} and {"b":2,"a":1} are the same call."""
    try:
        said = json.dumps(args if args is not None else {}, sort_keys=True,
                          ensure_ascii=False, separators=(",", ":"), default=str)
    except (TypeError, ValueError):
        said = repr(args)
    return f"{name}:{said}"


class CallGuard:
    """Watches one job's calls and turns. see_call before a call runs,
    see_result after it, end_turn when the model's turn is through.

    Each check returns (level, text): level is '' (carry on), 'warn' (put the
    text to the model with the tool's result) or 'stop' (end the job; the text
    says why, for the report)."""

    def __init__(self, warn: int = WARN_REPEATS, stop: int = STOP_REPEATS,
                 failed_turns: int = FAILED_TURNS, cycle_max: int = CYCLE_MAX):
        if not 1 <= warn <= stop:
            raise ValueError("CallGuard needs 1 <= warn <= stop")
        self.warn = warn
        self.stop = stop
        self.failed_turns = failed_turns
        self.cycle_max = max(2, cycle_max)
        self.reset()

    def reset(self) -> None:
        """Forget everything: a new job, or a fresh start inside one."""
        self.calls: list[str] = []          # every key seen this job, done excluded
        self.names: list[str] = []          # the matching tool names, for the words
        self.turn: list[bool] = []          # this turn's results: True = failed
        self.bad_turns = 0                  # turns in a row where every call failed

    # -- calls -------------------------------------------------------------

    def _run(self) -> int:
        """How many identical calls end the history."""
        if not self.calls:
            return 0
        last, n = self.calls[-1], 0
        for key in reversed(self.calls):
            if key != last:
                break
            n += 1
        return n

    def _cycle(self) -> tuple[int, int]:
        """(period, rounds) of the shortest repeating run of 2..cycle_max calls
        that ends the history, or (0, 0). rounds counts whole times round:
        A,B,A,B is (2, 2); A,B,A,B,A,B is (2, 3). A run of one call repeated is
        not a cycle -- that is _run's."""
        h = self.calls
        for p in range(2, self.cycle_max + 1):
            if len(h) < 2 * p or len(set(h[-p:])) < 2:
                continue
            k = 0                       # trailing calls that match the call p back
            for i in range(len(h) - 1, p - 1, -1):
                if h[i] != h[i - p]:
                    break
                k += 1
            rounds = (k + p) // p
            if rounds >= 2:
                return p, rounds
        return 0, 0

    def see_call(self, name: str, args) -> tuple[str, str]:
        """Record a call the model has asked for, before it runs. 'stop' means
        do not run it."""
        if name == DONE:
            return "", ""
        self.calls.append(call_key(name, args))
        self.names.append(name)
        run = self._run()
        if run >= self.stop:
            return "stop", (f"stopped: the same call ({name}) {run} times in a row "
                            f"with the same arguments")
        if run >= self.warn:
            return "warn", (f"You have made the same call {run} times in a row and got "
                            f"the same result; do something different or call done.")
        p, rounds = self._cycle()
        if rounds:
            seq = ", ".join(self.names[-p:])
            if rounds >= 3:
                return "stop", (f"stopped: the same {p} calls ({seq}) round "
                                f"{rounds} times in a row")
            return "warn", (f"You are going round in a cycle: the same {p} calls ({seq}) "
                            f"twice in a row, with the same results. Do something "
                            f"different or call done.")
        return "", ""

    # -- results and turns -------------------------------------------------

    def see_result(self, name: str, failed: bool) -> None:
        """Record how a call in this turn came out (failed=True for a refusal
        or an error; `failed(result)` above reads it)."""
        self.turn.append(bool(failed))

    def end_turn(self) -> tuple[str, str]:
        """Close the model's turn. A turn in which every call failed counts; a
        turn with any success clears the count; a turn with no results (only a
        done, say) leaves it as it was."""
        turn, self.turn = self.turn, []
        if not turn:
            return "", ""
        if all(turn):
            self.bad_turns += 1
        else:
            self.bad_turns = 0
        if self.bad_turns >= self.failed_turns:
            return "stop", (f"stopped: every call failed in {self.bad_turns} turns "
                            f"in a row")
        return "", ""


# -- retry --------------------------------------------------------------------

# Never worth a second try: the same input fails the same way.
_NEVER = (KeyboardInterrupt, EOFError, ValueError, TypeError)
_NEVER_WORDS = re.compile(r"not found|\b404\b|\b400\b", re.IGNORECASE)
_AGAIN_WORDS = re.compile(r"connect|timeout|timed out|reset|\beof\b|overloaded|"
                          r"\b50[023]\b|internal", re.IGNORECASE)


def retryable(exc: BaseException) -> bool:
    """True for a failure the next try may not meet: a connection, a timeout, a
    reset, an EOF on the wire, an overloaded or 500/502/503 server (Ollama's 500
    is how a malformed tool call surfaces, C126). False for an interrupt, an
    EOFError, a ValueError or TypeError, and anything 'not found', 404 or 400."""
    if isinstance(exc, _NEVER):
        return False
    text = f"{type(exc).__name__}: {exc}"
    if _NEVER_WORDS.search(text):
        return False
    status = getattr(exc, "status_code", None)
    if isinstance(status, int):
        if 400 <= status < 500:
            return False
        if status >= 500:
            return True
    if isinstance(exc, (ConnectionError, TimeoutError)):
        return True
    return bool(_AGAIN_WORDS.search(text))


def retry(fn, tries: int = 3, base: float = 2.0, cap: float = 30.0,
          sleep=time.sleep, report=None):
    """fn(), tried up to `tries` times in all. A retryable failure waits
    base * 2**i seconds (never more than cap) and tries again, saying so once
    through report(line); anything else, or the last failure, is raised."""
    tries = max(1, int(tries))
    for i in range(tries):
        try:
            return fn()
        except Exception as exc:
            if i + 1 >= tries or not retryable(exc):
                raise
            wait = min(cap, base * 2 ** i)
            if report is not None:
                report(f"  try {i + 1} of {tries} failed ({type(exc).__name__}: {exc}); "
                       f"trying again in {wait:g}s")
            sleep(wait)
    raise AssertionError("unreachable")     # the loop returns or raises


# -- a deadline ---------------------------------------------------------------

class Bound:
    """A deadline: Bound(seconds) from now. .spent() is seconds gone, .left()
    seconds remaining (never below zero), .over() True once it has passed."""

    def __init__(self, seconds: float, clock=time.monotonic):
        self.seconds = float(seconds)
        self.clock = clock
        self.started = clock()

    def spent(self) -> float:
        return self.clock() - self.started

    def left(self) -> float:
        return max(0.0, self.seconds - self.spent())

    def over(self) -> bool:
        return self.spent() >= self.seconds


# -- strokes ------------------------------------------------------------------

def _strokes() -> None:
    """The guards on concrete cases. Raises AssertionError on the first wrong one."""
    # Five identical calls: '' '' warn warn stop; argument order does not matter.
    g = CallGuard()
    seen = [g.see_call("file_read", {"path": "a.py", "n": 1}) for _ in range(2)]
    seen += [g.see_call("file_read", {"n": 1, "path": "a.py"}) for _ in range(3)]
    assert [lv for lv, _ in seen] == ["", "", "warn", "warn", "stop"], seen
    assert "same call 3 times" in seen[2][1] and "call done" in seen[2][1], seen[2]
    assert "5 times" in seen[4][1], seen[4]

    # done never counts, and a different call breaks the run.
    g = CallGuard()
    for _ in range(4):
        g.see_call("done", {"summary": "x"})
    assert g.calls == []
    g.see_call("a", {}); g.see_call("a", {}); g.see_call("b", {})
    assert g.see_call("a", {}) == ("", "")

    # An A,B cycle: warned at twice round, stopped at three times round.
    g = CallGuard()
    got = [g.see_call(n, {"f": n}) for n in "ABAB"]
    assert [lv for lv, _ in got] == ["", "", "", "warn"], got
    assert "cycle" in got[3][1] and "A, B" in got[3][1], got[3]
    assert g.see_call("A", {"f": "A"})[0] == "warn"
    lv, text = g.see_call("B", {"f": "B"})
    assert lv == "stop" and "3 times" in text, (lv, text)

    # A three-call cycle; and a broken cycle is forgotten.
    g = CallGuard()
    got = [g.see_call(n, {}) for n in "ABCABC"]
    assert [lv for lv, _ in got][-1] == "warn" and "3 calls" in got[-1][1], got
    assert g.see_call("D", {}) == ("", "")

    # Three turns in which every call failed: a stop naming the count.
    g = CallGuard()
    for i in range(3):
        g.see_result("file_edit", True)
        g.see_result("file_read", True)
        lv, text = g.end_turn()
        assert lv == ("stop" if i == 2 else ""), (i, lv)
    assert "3 turns" in text, text

    # One success resets the count; an empty turn leaves it alone.
    g = CallGuard()
    g.see_result("x", True); g.end_turn()
    g.see_result("x", True); g.end_turn()
    g.see_result("x", True); g.see_result("y", False)
    assert g.end_turn() == ("", "") and g.bad_turns == 0
    g.see_result("x", True); g.end_turn()
    assert g.end_turn() == ("", "") and g.bad_turns == 1
    g.reset()
    assert g.bad_turns == 0 and g.calls == []

    # failed() reads FAILED_HEADS.
    assert failed("  Refused: no") and failed("Error: x") and not failed("Wrote a.py")

    # retryable: what is and is not worth a second try.
    assert retryable(ConnectionResetError("reset by peer"))
    assert retryable(TimeoutError("timed out"))
    assert retryable(RuntimeError("status 500: internal server error"))
    assert retryable(RuntimeError("503 Service Unavailable"))
    assert retryable(RuntimeError("model is overloaded"))
    assert retryable(OSError("unexpected EOF"))
    assert not retryable(RuntimeError("404 page not found"))
    assert not retryable(RuntimeError("model 'x' not found, try pulling it first"))
    assert not retryable(RuntimeError("400 bad request"))
    assert not retryable(ValueError("connection"))
    assert not retryable(EOFError())
    assert not retryable(KeyboardInterrupt())
    assert not retryable(RuntimeError("a plain bug"))

    class Status(Exception):
        def __init__(self, text, status_code):
            super().__init__(text)
            self.status_code = status_code
    assert retryable(Status("tool call parse", 500))
    assert not retryable(Status("bad", 400))

    # retry: succeeds on the second try, one report, a fake sleep of base.
    slept, said, calls = [], [], []

    def flaky():
        calls.append(1)
        if len(calls) == 1:
            raise ConnectionError("connection refused")
        return "ok"
    assert retry(flaky, sleep=slept.append, report=said.append) == "ok"
    assert len(calls) == 2 and slept == [2.0] and len(said) == 1, (calls, slept, said)
    assert "connection refused" in said[0], said

    # retry: a 404 is raised at once, never slept on.
    slept, calls = [], []

    def missing():
        calls.append(1)
        raise RuntimeError("404 model not found")
    try:
        retry(missing, sleep=slept.append)
    except RuntimeError as exc:
        assert "404" in str(exc)
    else:
        raise AssertionError("a 404 was swallowed")
    assert len(calls) == 1 and slept == [], (calls, slept)

    # retry: the waits double and are capped, and the last failure is raised.
    slept, said = [], []

    def down():
        raise ConnectionError("connection refused")
    try:
        retry(down, tries=4, base=10.0, cap=25.0, sleep=slept.append, report=said.append)
    except ConnectionError:
        pass
    else:
        raise AssertionError("the last failure was not raised")
    assert slept == [10.0, 20.0, 25.0] and len(said) == 3, (slept, said)

    # Bound: a deadline on a fake clock.
    now = [100.0]
    b = Bound(60, clock=lambda: now[0])
    assert b.spent() == 0 and b.left() == 60 and not b.over()
    now[0] = 145.0
    assert b.spent() == 45 and b.left() == 15 and not b.over()
    now[0] = 170.0
    assert b.left() == 0 and b.over()
