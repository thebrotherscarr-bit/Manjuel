"""The drive journal: a /drive job written down as it happens, so a crash does
not lose it.

WHY. A Steward job lives in one process: the chat it has had with the model,
the steps it took, the bytes each file had before it wrote them, the line of
work it opened, the commits it made. Until now all of that was held in memory
and written to logs/ once, at the end (drive_record). A crash, a closed window
or a reboot halfway through a job lost the lot -- and worse, left files
written with no copy of what they were before, so nothing could put them back.

So every turn is written down BEFORE it is acted on or shown, the way opencode
stores every prompt and claims each turn before it runs, and Pi's durable
runtime saves each turn and call before it is shown. One JSON row per event in
logs/<YYYY-mm-dd_HHMMSS>_drive.jsonl, flushed and synced to the disk before
the call returns. A job that ends writes a "close" row. A journal with no
"close" row, whose process is gone, is a job that died; `unfinished` finds it
and `replay` folds it back into what the driver held, so it can be resumed --
the way OpenClaw resumes the main session after a restart.

THE JOURNAL NEVER TAKES THE JOB DOWN. A journal that can stop the work is
worse than none: `write` never raises, and a journal that could not be opened
(no logs/ folder, a full disk) quietly writes nothing. No folder is ever made
here; the journal lives in the logs/ folder it is handed, or nowhere.

NEVER RESUME WHAT MAY STILL BE RUNNING. A job's process that cannot be proven
gone is treated as alive. Two hands on one job is the failure this guards; a
job left unresumed costs only a re-run.

The rows (kind, then its fields):

  open       spec, model, pid, ts                 the first row, written by open()
  message    role, content, tool_name, tool_calls one chat message (message_dict)
  step       n, tool, args, result                result cut to STEP_CHARS
  before     repo, path, bytes                    the file before the job wrote it:
                                                  base64, or null for a new file
  repo       key, base, line                      where the job writes in a repo
  item_file  repo, path                           a file the item in hand wrote
  commit     repo, sha                            a commit the job made; the repo's
                                                  item files are saved with it
  card       prompt, answer                       a question put to him; prompt
                                                  cut to CARD_CHARS
  item       key, verdict                         an item's end: its files were
                                                  committed or put back
  close      verdict                              the job's end; never resumed after

The standard library alone. Lines end CRLF and are utf-8, as the rest of logs/.
"""

from __future__ import annotations

import base64
import json
import os
import time
from pathlib import Path

SUFFIX = "_drive.jsonl"
STEP_CHARS = 4000       # a step's result, as the journal keeps it
CARD_CHARS = 400        # a card's prompt, as the journal keeps it


def _plain(obj):
    """What json cannot carry, made plain: bytes as base64, a set as a sorted list,
    a Path or anything else as its text. Used as json.dumps(default=...)."""
    if isinstance(obj, (bytes, bytearray)):
        return base64.b64encode(bytes(obj)).decode("ascii")
    if isinstance(obj, (set, frozenset)):
        return sorted((_plain(x) if not isinstance(x, (str, int, float)) else x for x in obj), key=str)
    if isinstance(obj, tuple):
        return list(obj)
    if hasattr(obj, "model_dump"):          # a pydantic object, such as ollama's
        try:
            return obj.model_dump()
        except Exception:
            pass
    return str(obj)


class Journal:
    """One job's journal. Built by Journal.open; `path` is None when it could not be
    opened, and then every write is a quiet no-op."""

    def __init__(self, path):
        self.path = Path(path) if path else None
        self.closed = False

    @classmethod
    def open(cls, logs, spec: dict, model: str) -> "Journal":
        """A new journal in `logs`, its first row the job's spec, model and process.
        `logs` must already exist: no folder is made here."""
        try:
            logs = Path(logs)
            if not logs.is_dir():
                return cls(None)
            stamp = time.strftime("%Y-%m-%d_%H%M%S")
            path, i = logs / f"{stamp}{SUFFIX}", 1
            while True:
                try:
                    with open(path, "xb"):      # claimed, never two jobs in one file
                        pass
                    break
                except FileExistsError:
                    i += 1
                    path = logs / f"{stamp}_{i}{SUFFIX}"
            j = cls(path)
            j.write("open", spec=dict(spec or {}), model=str(model or ""), pid=os.getpid())
            return j
        except Exception:
            return cls(None)

    def write(self, kind: str, **fields) -> bool:
        """Append one row, flushed and synced. True when it reached the disk.
        Never raises."""
        if self.path is None:
            return False
        try:
            if kind == "step" and "result" in fields:
                fields["result"] = str(fields["result"] or "")[:STEP_CHARS]
            if kind == "card" and "prompt" in fields:
                fields["prompt"] = str(fields["prompt"] or "")[:CARD_CHARS]
            row = {"kind": str(kind), "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
            row.update(fields)
            line = (json.dumps(row, ensure_ascii=False, default=_plain) + "\r\n").encode("utf-8", "surrogatepass")
            with open(self.path, "ab+") as f:
                # A row cut short by a crash has no line end: begin a fresh line, or
                # this row would join it and be lost with it.
                end = f.seek(0, 2)
                if end:
                    f.seek(end - 1)
                    if f.read(1) != b"\n":
                        line = b"\r\n" + line
                f.write(line)           # append mode: always at the end
                f.flush()
                os.fsync(f.fileno())
            return True
        except Exception:
            return False

    def close(self, verdict: str) -> bool:
        """The job's last row. A closed journal is never resumed."""
        if self.closed:
            return False
        self.closed = True
        return self.write("close", verdict=str(verdict or ""))


def _field(obj, name):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def message_dict(msg) -> dict:
    """One chat message -- an ollama Message or a dict -- as a plain dict that json
    carries and ollama accepts back: role, content, tool_name, tool_calls (each its
    function's name and arguments). The model's thinking is dropped: it is not sent
    back, and it is the bulk of a long turn."""
    out = {"role": str(_field(msg, "role") or ""), "content": str(_field(msg, "content") or "")}
    name = _field(msg, "tool_name")
    if name:
        out["tool_name"] = str(name)
    calls = []
    for call in (_field(msg, "tool_calls") or []):
        fn = _field(call, "function")
        if fn is None:
            continue
        args = _field(fn, "arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except ValueError:
                args = {"content": args}
        try:
            args = json.loads(json.dumps(dict(args), ensure_ascii=False, default=_plain))
        except (TypeError, ValueError):
            args = {}
        calls.append({"function": {"name": str(_field(fn, "name") or ""), "arguments": args}})
    if calls:
        out["tool_calls"] = calls
    return out


def _rows(path):
    """Every whole row of a journal, in order. A row cut short by a crash is skipped."""
    out = []
    try:
        data = Path(path).read_bytes()
    except OSError:
        return out
    for raw in data.split(b"\n"):
        raw = raw.strip(b"\r")
        if not raw:
            continue
        try:
            row = json.loads(raw.decode("utf-8", "surrogatepass"))
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def alive(pid) -> bool:
    """Whether a process is running. True whenever that cannot be known: a job is
    never resumed while something may still be working it."""
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return True
    if pid <= 0:
        return True
    if pid == os.getpid():
        return True
    if os.name != "nt":
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except OSError:
            return True             # it exists and is not ours, or the answer is unknown
        return True
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.OpenProcess.restype = wintypes.HANDLE
        k32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        k32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
        k32.CloseHandle.argtypes = (wintypes.HANDLE,)
        h = k32.OpenProcess(0x1000, False, pid)         # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            err = ctypes.get_last_error()
            if err == 87:                                # ERROR_INVALID_PARAMETER: no such process
                return False
            return True                                  # access denied: it exists; else unknown
        try:
            code = wintypes.DWORD()
            if not k32.GetExitCodeProcess(h, ctypes.byref(code)):
                return True
            return code.value == 259                     # STILL_ACTIVE
        finally:
            k32.CloseHandle(h)
    except Exception:
        pass
    try:                                                 # no ctypes: ask tasklist
        import subprocess
        said = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH", "/FO", "CSV"],
                              capture_output=True, text=True, stdin=subprocess.DEVNULL,
                              timeout=10)
        if said.returncode != 0:
            return True
        rows = [ln for ln in said.stdout.splitlines() if ln.startswith('"')]
        if not rows:
            return False
        return any(f'"{pid}"' in ln for ln in rows)
    except Exception:
        return True


def unfinished(logs):
    """The newest journal in `logs` with no "close" row whose process is gone, or
    None. A journal with no readable "open" row is never offered."""
    try:
        found = sorted(Path(logs).glob("*" + SUFFIX), key=lambda p: p.name, reverse=True)
    except OSError:
        return None
    for path in found:
        rows = _rows(path)
        if not rows or rows[0].get("kind") != "open":
            continue
        if any(r.get("kind") == "close" for r in rows):
            continue
        if alive(rows[0].get("pid")):
            continue
        return path
    return None


def replay(path) -> dict:
    """Fold a journal back into what the driver held when it stopped.

    messages   the chat of the job in hand: from its last "system" message on (each
               job, and each item's job, begins its own chat with one)
    steps      every step, [n, tool, args, result]
    repos      {repo: {"base", "line"}}
    item_files {(repo, path)} the item in hand wrote and had not saved
    touched    {(repo, path)} the job ever wrote
    before     {(repo, path): bytes or None} the files' bytes before the item wrote
               them. A key here and not in item_files had its bytes kept but its
               write never confirmed: compare the disk to know whether it ran.
    made       {repo: [sha]}
    items      [[key, verdict]]
    last_n     the highest step number written
    """
    rows = _rows(path)
    head = rows[0] if rows and rows[0].get("kind") == "open" else {}
    out = {"spec": head.get("spec") or {}, "model": head.get("model") or "",
           "messages": [], "steps": [], "repos": {}, "item_files": set(), "touched": set(),
           "before": {}, "made": {}, "items": [], "last_n": 0}
    for r in rows[1:] if head else rows:
        kind = r.get("kind")
        if kind == "message":
            m = {k: r[k] for k in ("role", "content", "tool_name", "tool_calls") if k in r}
            if m.get("role") == "system":
                out["messages"] = []
            out["messages"].append(m)
        elif kind == "step":
            n = r.get("n") or 0
            out["steps"].append([n, r.get("tool", ""), r.get("args", ""), r.get("result", "")])
            if isinstance(n, int) and n > out["last_n"]:
                out["last_n"] = n
        elif kind == "before":
            raw = r.get("bytes")
            try:
                data = None if raw is None else base64.b64decode(raw)
            except (ValueError, TypeError):
                continue                    # bytes that cannot be read back are no copy at all
            out["before"][(str(r.get("repo", "")), str(r.get("path", "")))] = data
        elif kind == "repo":
            out["repos"][str(r.get("key", ""))] = {"base": r.get("base", ""), "line": r.get("line", "")}
        elif kind == "item_file":
            key = (str(r.get("repo", "")), str(r.get("path", "")))
            out["item_files"].add(key)
            out["touched"].add(key)
        elif kind == "commit":
            repo = str(r.get("repo", ""))
            out["made"].setdefault(repo, []).append(str(r.get("sha", "")))
            for key in [k for k in out["item_files"] if k[0] == repo]:
                out["item_files"].discard(key)
            for key in [k for k in out["before"] if k[0] == repo]:
                out["before"].pop(key)
        elif kind == "item":
            out["items"].append([r.get("key", ""), r.get("verdict", "")])
            out["item_files"] = set()
            out["before"] = {}
    return out


def mark_resumed(path) -> bool:
    """Close a dead job's journal so it is never resumed twice."""
    return Journal(path).close("resumed elsewhere")


def _strokes() -> None:
    """The journal's own proof: open, write, close, unfinished, replay, round trip."""
    import shutil
    import subprocess
    import sys
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="journal_"))
    try:
        # No folder: a quiet journal that writes nothing and makes nothing.
        none = Journal.open(tmp / "absent", {"goal": "x"}, "m")
        assert none.path is None and not none.write("step", n=1) and not (tmp / "absent").exists()

        spec = {"mode": "goal", "goal": "fix the docs", "check": "python -c pass"}
        j = Journal.open(tmp, spec, "qwen3.5:9b")
        assert j.path is not None and j.path.name.endswith(SUFFIX)
        crlf = b"line one\r\nline two\r\n"
        odd = b"\xff\xfe\x00bytes\x80 not utf-8\r\n"
        a, b, c = ("R", "R/a.md"), ("R", "R/b.bin"), ("R", "R/new.txt")
        j.write("message", **message_dict({"role": "system", "content": "old job"}))
        j.write("message", **message_dict({"role": "system", "content": "you drive"}))
        j.write("message", **message_dict({"role": "user", "content": "Goal: fix\r\nthe docs"}))
        j.write("message", **message_dict({
            "role": "assistant", "content": "", "thinking": "long thought",
            "tool_calls": [{"function": {"name": "file_edit", "arguments": '{"filepath": "a.md"}'}}]}))
        j.write("repo", key="R", base="main", line="drive-1021-120000")
        j.write("before", repo=a[0], path=a[1], bytes=crlf)
        j.write("before", repo=b[0], path=b[1], bytes=odd)
        j.write("before", repo=c[0], path=c[1], bytes=None)
        for k in (a, b, c):
            j.write("item_file", repo=k[0], path=k[1])
        j.write("step", n=7, tool="file_edit", args={"filepath": "a.md"}, result="Edited " + "x" * 5000)
        j.write("card", prompt="Approve? " + "y" * 900, answer="y")
        j.write("message", role="tool", tool_name="file_edit", content="Edited a.md")

        # Our own process holds it: never offered.
        assert unfinished(tmp) is None, "a live job was offered for resume"
        r = replay(j.path)
        assert r["spec"] == spec and r["model"] == "qwen3.5:9b"
        assert [m["content"] for m in r["messages"]] == ["you drive", "Goal: fix\r\nthe docs", "", "Edited a.md"]
        assert "thinking" not in r["messages"][2]
        assert r["messages"][2]["tool_calls"] == [{"function": {"name": "file_edit",
                                                               "arguments": {"filepath": "a.md"}}}]
        assert r["messages"][3]["tool_name"] == "file_edit"
        assert r["before"][a] == crlf and r["before"][b] == odd and r["before"][c] is None
        assert r["item_files"] == {a, b, c} == r["touched"]
        assert r["repos"] == {"R": {"base": "main", "line": "drive-1021-120000"}}
        assert r["last_n"] == 7 and len(r["steps"][0][3]) == STEP_CHARS
        rows = _rows(j.path)
        assert len(next(x for x in rows if x["kind"] == "card")["prompt"]) == CARD_CHARS
        assert j.path.read_bytes().count(b"\r\n") == len(rows) == j.path.read_bytes().count(b"\n")

        # A commit saves the repo's item files; an item's end lets go of the rest.
        j.write("commit", repo="R", sha="abc123")
        r = replay(j.path)
        assert r["made"] == {"R": ["abc123"]} and not r["item_files"] and not r["before"]
        assert r["touched"] == {a, b, c}
        j.write("before", repo="S", path="S/z", bytes=b"z")
        j.write("item_file", repo="S", path="S/z")
        j.write("item", key="item one", verdict="failed")
        r = replay(j.path)
        assert r["items"] == [["item one", "failed"]] and not r["item_files"] and not r["before"]

        # A dead process's journal is unfinished; a row cut short by the crash is skipped.
        dead = subprocess.run([sys.executable, "-I", "-c", "import os; print(os.getpid())"],
                              capture_output=True, text=True).stdout.strip()
        assert not alive(dead), "a finished process read as alive"
        assert alive(os.getpid()) and alive("not a pid") and alive(0)
        lost = tmp / ("2000-01-01_000000" + SUFFIX)
        lost.write_bytes(json.dumps({"kind": "open", "spec": spec, "model": "m", "pid": int(dead)}).encode()
                         + b"\r\n" + b'{"kind": "message", "role": "user", "content": "hi"}\r\n'
                         + b'{"kind": "step", "n": 3, "to')
        assert unfinished(tmp) == lost
        assert replay(lost)["messages"] == [{"role": "user", "content": "hi"}]
        assert replay(lost)["last_n"] == 0

        # Resumed once, never again; a closed journal is never offered.
        assert mark_resumed(lost) and unfinished(tmp) is None
        assert j.close("passed") and not j.close("passed")
        assert _rows(j.path)[-1]["kind"] == "close" and _rows(lost)[-1]["verdict"] == "resumed elsewhere"
        assert unfinished(tmp / "absent") is None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
