"""Context compaction for Steward's driver: keep a long job inside its window.

A /drive job grows by one assistant turn and one or more tool results every
step, and each result can be up to DRIVE_RESULT_CHARS long (more the first time
a tool's whole skill file comes with it). At a 16384-token window a job of
thirty reads is already past the line, and Ollama does not refuse an
over-long prompt: it silently drops the OLDEST part of it, which is the system
prompt and the goal -- the two things the job cannot work without. So the
driver has to make room itself, before every call, in an order that loses the
least:

  1. PRUNE, with no model (Hermes; oh-my-pi's "shake"). The system prompt and
     the goal are kept whole, and so is the newest stretch of the job (40% of
     the window by default). Every older tool result is shortened to a one-line
     note naming the tool and its size, and, when a logs folder is given, the
     whole result is written there first so nothing is lost -- only moved out
     of the window. An older result that a LATER call of the same tool with
     the same arguments replaced is marked superseded: the model has the newer
     copy. No message is ever removed here, because Ollama pairs each tool
     result with the assistant turn that called it; only content shrinks.
  2. SUMMARISE, when pruning is not enough and a model is offered (opencode's
     fixed form; Pi's rule of 2000 characters per tool result in the prompt).
     Everything between the goal and the kept tail becomes ONE user message
     saying where the work stands. The tail starts at an assistant or user
     message, never at a tool result, so no result loses its call.
  3. CUT, when there is no model or it fails (Cline's basic strategy): the
     same span is dropped and a one-line marker says how many messages went.
     Deterministic and strictly smaller.

The line itself: the window less a reserve for the reply, 15% of the window
but never under 2048 tokens, and never more than 25% of it (opencode and
Cline both hold back a fixed slice for the answer). Tokens are counted as
characters / 4: crude, but the same on every machine and needing nothing
downloaded, and it errs high on the code and paths a job mostly carries.

The standard library only; Python 3.10.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

RESERVE_SHARE = 0.15          # of the window, held back for the reply
RESERVE_FLOOR = 2048          # tokens, never less than this ...
RESERVE_CAP = 0.25            # ... and never more than this share of the window
KEEP_SHARE = 0.40             # the newest part of the job, kept whole
SUMMARY_RESULT_CHARS = 2000   # each tool result, as the summary prompt shows it
CUT_RESULT_CHARS = 2000       # each kept tool result, when a cut alone is not enough
TRIMMED = "[an earlier result of "
SUPERSEDED = "[superseded by a later read of the same thing]"
SUMMARY_HEAD = "Where the work stands (a summary of the earlier steps):\n"
HEADINGS = (
    ("Objective", "What the work is for, in one or two lines."),
    ("Requirements", "What the goal and the check demand; limits the work must keep."),
    ("Decisions", "What was chosen and why, so it is not argued again."),
    ("Work State", "What is done, what is half-done, what failed and how."),
    ("Next Move", "The one next step, exactly."),
    ("Relevant Files", "At most 15 paths, one per line, each with why it matters."),
    ("Important Context", "Errors, refusals, numbers and facts that would cost a step to find again."),
)


def _get(msg, name):
    """A field of a message, whether it is a dict or an ollama Message."""
    if isinstance(msg, dict):
        return msg.get(name)
    return getattr(msg, name, None)


def _text(value) -> str:
    return value if isinstance(value, str) else ("" if value is None else str(value))


def _calls(msg) -> list:
    """Every tool call in an assistant message, as (name, arguments dict)."""
    out = []
    for call in (_get(msg, "tool_calls") or []):
        fn = _get(call, "function")
        if fn is None:
            continue
        name = _text(_get(fn, "name")).strip()
        args = _get(fn, "arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except ValueError:
                args = {"content": args}
        try:
            args = dict(args)
        except (TypeError, ValueError):
            args = {}
        out.append((name, args))
    return out


def _dumps(args) -> str:
    return json.dumps(args, ensure_ascii=False, sort_keys=True, default=str)


def _chars(msg) -> int:
    """What one message weighs: its content plus its calls' names and arguments."""
    n = len(_text(_get(msg, "content")))
    for name, args in _calls(msg):
        n += len(name) + len(_dumps(args))
    return n


def estimate(messages) -> int:
    """Tokens, as characters / 4 over every content and every call's arguments."""
    return (sum(_chars(m) for m in messages) + 3) // 4


def reserve_for(window: int) -> int:
    """Tokens held back for the reply: 15% of the window, at least 2048,
    at most 25% of the window."""
    window = int(window)
    return min(max(int(window * RESERVE_SHARE), RESERVE_FLOOR), int(window * RESERVE_CAP))


def _line(window: int) -> int:
    return int(window) - reserve_for(window)


def spill(text, logs, tag) -> str:
    """The whole of a text, written to logs/<YYYY-mm-dd_HHMMSS>_drive_result_<tag>.txt
    (CRLF, utf-8, as drive_record writes). Returns 'logs/<name>', or '' when it
    could not be written. Never raises, and never makes a folder."""
    try:
        folder = Path(logs)
        if not folder.is_dir():
            return ""
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(tag))[:60] or "result"
        stem = time.strftime("%Y-%m-%d_%H%M%S") + "_drive_result_" + safe
        name, k = stem + ".txt", 2
        while (folder / name).exists():
            name, k = f"{stem}-{k}.txt", k + 1
        body = _text(text).replace("\r\n", "\n")
        (folder / name).write_text(body, encoding="utf-8", newline="\r\n")
        return f"logs/{name}"
    except Exception:
        return ""


def _tool_message(msg, content: str):
    """A copy of a tool message with new content; the original is never changed."""
    if isinstance(msg, dict):
        out = dict(msg)
        out["content"] = content
        return out
    out = {"role": "tool", "content": content}
    name = _get(msg, "tool_name")
    if name:
        out["tool_name"] = name
    return out


def _tail_start(messages, keep_tokens: int) -> int:
    """Where the kept tail begins: the newest messages within keep_tokens (the
    newest one always), moved back to an assistant or user message so no tool
    result is kept without the call it answers. Never before index 2."""
    if len(messages) <= 2:
        return len(messages)
    budget, acc, start = keep_tokens * 4, 0, len(messages)
    for i in range(len(messages) - 1, 1, -1):
        acc += _chars(messages[i])
        if acc > budget and i < len(messages) - 1:
            break
        start = i
    while start > 2 and _get(messages[start], "role") == "tool":
        start -= 1
    return start


def _call_keys(messages) -> list:
    """For each message, the (tool, arguments) of the call a tool result answers,
    or None. Results are matched to their assistant turn's calls in order, by name."""
    keys, pending = [], []
    for m in messages:
        role = _get(m, "role")
        if role == "assistant":
            pending = [(n, _dumps(a)) for n, a in _calls(m)]
            keys.append(None)
        elif role == "tool":
            name = _text(_get(m, "tool_name"))
            hit = next((j for j, (n, _) in enumerate(pending) if n == name), None)
            keys.append(pending.pop(hit) if hit is not None else None)
        else:
            keys.append(None)
    return keys


def prune(messages, window: int, keep_tokens=None, logs=None):
    """(messages, note), with no model. System and goal whole, the newest
    keep_tokens (default 40% of the window) whole; every older tool result
    shortened to a note (spilled whole to logs first when logs is given), or
    marked superseded when a later call of the same tool with the same
    arguments replaced it. Never removes a message. note is '' when nothing changed."""
    messages = list(messages)
    keep = int(window * KEEP_SHARE) if keep_tokens is None else int(keep_tokens)
    start = _tail_start(messages, keep)
    keys = _call_keys(messages)
    last = {}
    for i, k in enumerate(keys):
        if k is not None:
            last[k] = i
    out = list(messages)
    trimmed = superseded = spilled = saved = 0
    for i in range(2, start):
        m = messages[i]
        if _get(m, "role") != "tool":
            continue
        body = _text(_get(m, "content"))
        if body.startswith((TRIMMED, SUPERSEDED)):
            continue                        # already done on an earlier step
        k = keys[i]
        if k is not None and last.get(k, i) > i:
            note = SUPERSEDED
            superseded += 1
        else:
            tool = _text(_get(m, "tool_name")) or "a tool"
            note = f"{TRIMMED}{tool}, {len(body)} chars, trimmed to keep the window"
            if len(body) <= len(note) + 40:
                continue                    # the note would weigh as much as the result
            if logs is not None:
                where = spill(body, logs, f"{i}_{tool}")
                if where:
                    note += f"; the whole of it is in {where}"
                    spilled += 1
            note += "]"
            trimmed += 1
        saved += len(body) - len(note)
        out[i] = _tool_message(m, note)
    if not (trimmed or superseded):
        return out, ""
    parts = []
    if trimmed:
        parts.append(f"trimmed {trimmed} earlier tool result{'s' if trimmed != 1 else ''}"
                     + (f" ({spilled} written whole to logs/)" if spilled else ""))
    if superseded:
        parts.append(f"marked {superseded} superseded by a later read of the same thing")
    return out, "; ".join(parts) + f", about {max(saved, 0) // 4} tokens freed"


def _render(messages) -> str:
    """The conversation as plain text for a summary: system prompts left out,
    each tool result cut to SUMMARY_RESULT_CHARS."""
    lines = []
    for m in messages:
        role = _text(_get(m, "role"))
        body = _text(_get(m, "content")).strip()
        if role == "system":
            continue
        if role == "tool":
            tool = _text(_get(m, "tool_name")) or "a tool"
            if len(body) > SUMMARY_RESULT_CHARS:
                body = body[:SUMMARY_RESULT_CHARS] + f" ...[cut; {len(body)} chars in all]"
            lines += [f"[result of {tool}]", body, ""]
            continue
        lines.append(f"[{role}]")
        if body:
            lines.append(body)
        for name, args in _calls(m):
            lines.append(f"(calls {name} {_dumps(args)})")
        lines.append("")
    return "\n".join(lines).strip()


def summary_prompt(messages) -> str:
    """The prompt that asks a model for a summary of the work so far, in
    opencode's fixed headings, from the conversation it is given."""
    form = "\n".join(f"## {h}\n{why}" for h, why in HEADINGS)
    return ("Write a summary of the work so far, for the one who will carry it on "
            "with no other memory of it. Use exactly these headings, in this order, "
            "with short plain lines under each:\n\n" + form + "\n\n"
            "Write only the summary. Call no tool. Say nothing the conversation "
            "does not say; where a heading has nothing, write 'none'.\n\n"
            "The conversation so far:\n\n" + _render(messages))


def _cut(head: list, tail: list, dropped: int, line: int):
    """head + a marker + tail, dropping the oldest whole turns of the tail while
    over the line, then cutting kept tool results. Returns (messages, dropped, cut)."""
    def build(n):
        if n <= 0:
            return head + tail
        return head + [{"role": "user", "content":
                        f"[{n} earlier message{'s' if n != 1 else ''} were cut here to keep "
                        "the window. The job's record in logs/ keeps every step whole.]"}] + tail
    while estimate(build(dropped)) > line:
        b = next((j for j in range(1, len(tail))
                  if _get(tail[j], "role") in ("assistant", "user")), None)
        if b is None:
            break
        dropped += b
        tail = tail[b:]
    cut = 0
    if estimate(build(dropped)) > line:
        kept = []
        for m in tail:
            body = _text(_get(m, "content"))
            if _get(m, "role") == "tool" and len(body) > CUT_RESULT_CHARS:
                m = _tool_message(m, body[:CUT_RESULT_CHARS]
                                  + f" ...[cut to keep the window; {len(body)} chars in all]")
                cut += 1
            kept.append(m)
        tail = kept
    return build(dropped), dropped, cut


def compact(messages, window: int, ask=None, logs=None):
    """(messages, note) that fit window - reserve_for(window). Unchanged with
    note '' when they already fit. Else prune; then, still over, summarise the
    span between the goal and the kept tail with ask (a callable prompt -> text),
    or, without ask or when it fails, cut that span. note says which."""
    messages = list(messages)
    line = _line(window)
    if estimate(messages) <= line:
        return messages, ""
    pruned, note = prune(messages, window, logs=logs)
    said = [note] if note else []
    if estimate(pruned) <= line:
        return pruned, "; ".join(said)
    keep = int(window * KEEP_SHARE)
    start = _tail_start(pruned, keep)
    head = pruned[:2]
    span = start - 2
    why = "no model was offered for a summary"
    if ask is not None and span > 0:
        try:
            text = _text(ask(summary_prompt(pruned[:start]))).strip()
        except Exception as exc:
            text, why = "", f"the summary failed ({type(exc).__name__}: {exc})"
        else:
            why = "the summary came back empty"
        if text:
            summed = head + [{"role": "user", "content": SUMMARY_HEAD + text}] + pruned[start:]
            if estimate(summed) < estimate(pruned):
                said.append(f"summarised {span} earlier message{'s' if span != 1 else ''} by the model")
                if estimate(summed) > line:
                    summed, gone, cut = _cut(summed[:3], pruned[start:], 0, line)
                    if gone or cut:
                        said.append(f"then cut {gone} more and shortened {cut} kept result(s)")
                    if estimate(summed) > line:
                        said.append("STILL over the line")
                return summed, "; ".join(said)
            why = "the summary was no smaller than what it would replace"
    elif span <= 0:
        why = "there was no span to summarise"
    out, gone, cut = _cut(head, pruned[start:], span, line)
    said.append(f"{why}; cut {gone} earlier message{'s' if gone != 1 else ''}"
                + (f" and shortened {cut} kept result(s)" if cut else ""))
    if estimate(out) > line:
        said.append("STILL over the line")
    return out, "; ".join(said)


# ---------------------------------------------------------------- the strokes

def _paired(messages) -> bool:
    """Every tool result follows (through other results) an assistant message."""
    prev = None
    for m in messages:
        role = _get(m, "role")
        if role == "tool" and prev not in ("assistant", "tool"):
            return False
        prev = role
    return True


def _job(pairs: int, result_chars: int = 4000, words: int = 0) -> list:
    """A synthetic /drive job: system, goal, then assistant turns each with one
    read_file call and its result."""
    msgs = [{"role": "system", "content": "You drive the work. " * 100},
            {"role": "user", "content": "Goal: make the thing.\nThe check that decides done: true"}]
    for i in range(pairs):
        msgs.append({"role": "assistant", "content": "w" * words,
                     "tool_calls": [{"function": {"name": "read_file",
                                                  "arguments": {"path": f"f{i}.py"}}}]})
        msgs.append({"role": "tool", "tool_name": "read_file",
                     "content": f"file {i}\n" + "x" * result_chars})
    return msgs


def _strokes() -> None:
    import shutil
    import tempfile

    assert reserve_for(16384) == 2457, reserve_for(16384)
    assert reserve_for(4096) == 1024
    assert reserve_for(200000) == 30000
    assert estimate([{"role": "user", "content": "abcd" * 10}]) == 10

    # A 60-message job over a 16384 window gets under the line, pairing intact.
    job = _job(29)
    assert len(job) == 60 and estimate(job) > _line(16384)
    out, note = compact(job, 16384)
    assert estimate(out) <= _line(16384), (estimate(out), note)
    assert len(out) == 60 and _paired(out) and note.startswith("trimmed"), note
    assert out[0] == job[0] and out[1] == job[1] and out[-1] == job[-1]
    assert job[2]["role"] == "assistant" and len(job[3]["content"]) > 4000   # input untouched
    again, note2 = prune(out, 16384)
    assert note2 == "" and again == out                                       # idempotent
    small = _job(2)
    assert compact(small, 16384) == (small, "")

    # A superseded read is marked; a different read is only trimmed.
    job = _job(10)
    job[4] = {"role": "assistant", "content": "",
              "tool_calls": [{"function": {"name": "read_file", "arguments": {"path": "f9.py"}}}]}
    out, note = prune(job, 16384, keep_tokens=2000)
    assert out[5]["content"] == SUPERSEDED, out[5]["content"][:80]
    assert out[3]["content"].startswith(TRIMMED) and "superseded" in note
    assert len(out) == len(job) and _paired(out)

    # Spill writes the whole result, CRLF, into the folder it is handed.
    tmp = tempfile.mkdtemp()
    try:
        out, note = prune(_job(10), 16384, keep_tokens=2000, logs=Path(tmp))
        assert "written whole to logs/" in note, note
        files = sorted(Path(tmp).iterdir())
        assert files and all("_drive_result_" in f.name for f in files)
        raw = files[0].read_bytes()
        assert raw.count(b"\r\n") == raw.count(b"\n") and raw.count(b"\r\n") >= 1
        assert "the whole of it is in logs/" in out[3]["content"]
        assert spill("x", Path(tmp) / "no-such-folder", "t") == ""
        assert not (Path(tmp) / "no-such-folder").exists()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Pruning cannot help when the weight is in the assistant's words: ask
    # failing falls back to a cut, strictly smaller, under the line, paired.
    job = _job(29, result_chars=50, words=3000)
    pruned, _ = prune(job, 16384)
    assert estimate(pruned) > _line(16384)

    def broken(prompt):
        raise RuntimeError("the model is away")
    out, note = compact(job, 16384, ask=broken)
    assert "summary failed" in note and "cut" in note, note
    assert estimate(out) < estimate(pruned) and estimate(out) <= _line(16384), note
    assert out[0] == job[0] and out[1] == job[1] and _paired(out)
    assert _get(out[3], "role") in ("assistant", "user")
    out, note = compact(job, 16384, ask=lambda p: "")
    assert "came back empty" in note and estimate(out) <= _line(16384)
    out, note = compact(job, 16384)
    assert "no model was offered" in note and estimate(out) <= _line(16384)

    # A summary that comes back replaces the span with one user message.
    asked = []

    def model(prompt):
        asked.append(prompt)
        return "## Objective\nmake the thing\n## Next Move\nread f28.py"
    out, note = compact(job, 16384, ask=model)
    assert "summarised" in note, note
    assert out[2]["role"] == "user" and out[2]["content"].startswith(SUMMARY_HEAD)
    assert _get(out[3], "role") == "assistant" and _paired(out)
    assert estimate(out) <= _line(16384)
    for h, _ in HEADINGS:
        assert f"## {h}" in asked[0]
    assert "You drive the work." not in asked[0]                  # no system prompt
    long_result = _job(1, result_chars=9000)
    assert "[cut; 9007 chars in all]" in summary_prompt(long_result)
