"""MCP over stdio: a local tool server that is a program, not an address.

WHY THIS EXISTS. `mcp_call` could only dial a server that listens on
loopback HTTP (MANJUEL_MCP_<NAME>=<url>). Most MCP servers -- REA above all,
the reverse-engineering server in worlds/harnesses/rea -- do not listen at
all: they are a program you start, write JSON-RPC to on stdin, and read
answers from on stdout, one JSON object per line. So Steward could not reach
them. This module starts such a program, does the handshake, lists its
tools, calls one, and stops it again.

WHY IT IS WALLED. Starting a program is a bigger act than dialling a
loopback port, so the wall is in code (`admit`), not in good intentions:

  - A server is started ONLY when its program -- or, for node and python,
    the script that program runs -- resolves INSIDE the ground
    (C:\\Users\\novad\\Desktop\\Research). Anything else is refused by name
    and nothing is started (RULE 1: the ground is where the work lives).
  - The program gets a minimal environment: PATH, SYSTEMROOT, TEMP, TMP,
    USERPROFILE, APPDATA, LOCALAPPDATA, HOME, COMSPEC -- never the whole
    environment, never .env's keys (RULE 7), and never NODE_OPTIONS, which
    would let anything be loaded into node beside the declared script.
  - No shell. The command is split once, here, and handed over as a list.

WHY EVERY WAIT IS BOUNDED. A server that stops talking must become a
refusal a seat can read, never a turn that hangs (ESTATE LAW 7). So stdout
is read on its own thread into a queue and every wait is a queue wait with a
deadline; stderr is kept in a small ring buffer so that a server that dies
is reported with the last thing it said.

A server is declared as MANJUEL_MCP_<NAME>_CMD in .env, a command line:
    MANJUEL_MCP_REA_CMD=node worlds/harnesses/rea/node_modules/rea-agents/scripts/rea.mjs mcp
A relative script path is read from the ground.

stdlib only, Python 3.10.
"""

from __future__ import annotations

import collections
import json
import os
import queue
import shlex
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

GROUND = Path(__file__).resolve().parent.parent
PROTOCOL = "2025-06-18"
CLIENT = {"name": "manjuel", "version": "1"}

DIAL = "MANJUEL_MCP_"
CMD = "_CMD"
ENV_KEEP = ("PATH", "SYSTEMROOT", "TEMP", "TMP", "USERPROFILE", "APPDATA",
            "LOCALAPPDATA", "HOME", "COMSPEC")
# Interpreters whose SCRIPT is what must live in the ground, and the flags
# that would load code from somewhere other than that script.
_INTERP = {"node", "python", "python3", "pythonw", "py"}
_CODE_FLAGS = {"-e", "--eval", "-p", "--print", "-r", "--require", "--import",
               "--loader", "--experimental-loader", "-c", "-m"}
_VALUE_FLAGS = {"-X", "-W"}          # python flags whose next word is a value
_STDERR_LINES = 200
_EOF = object()


class StdioError(Exception):
    """The server could not be reached, died, or did not answer in time.
    The message is plain words a seat can read."""


def servers() -> dict:
    """{name: argv} for every MANJUEL_MCP_<NAME>_CMD in the environment.

    Split once with shlex -- posix=False on Windows, so a backslash in a
    path is a backslash, with the quotes that mode keeps stripped off."""
    out = {}
    for k, v in os.environ.items():
        if k.startswith(DIAL) and k.endswith(CMD) and v.strip():
            name = k[len(DIAL):-len(CMD)].strip().lower()
            if name:
                out[name] = split(v)
    return out


def split(line: str) -> list:
    """A command line as argv, without a shell."""
    if os.name == "nt":
        return [w[1:-1] if len(w) >= 2 and w[0] == w[-1] and w[0] in "\"'" else w
                for w in shlex.split(line.strip(), posix=False)]
    return shlex.split(line.strip())


# A SERVER'S OWN ROOT (2026-10-22, his card: "Default places", for his second brain). A server
# whose script lives outside the ground -- his notes kernel beside it on the Desktop -- is admitted
# only inside the root HE declares for that one server, MANJUEL_MCP_<NAME>_ROOT in .env (his to
# write: RULE 7). Every other server keeps the wall whole.
ROOT = "_ROOT"

# TOOLS REFUSED BY NAME, per server: what would change the machine or pull in local paths, never
# run through this door whoever calls -- a council seat's mcp_call carries no card.
REFUSED_TOOLS = {
    "notes": {"system_update", "system_install_desktop", "system_desktop_build",
              "import_folder", "ingest_path", "ingest_watch", "notes_remove"},
}


def declared_root(name: str) -> Path | None:
    """The root he declared for server `name`, or None."""
    v = os.environ.get(DIAL + name.upper() + ROOT, "").strip().strip("'\"")
    return Path(v) if v else None


def refused_tool(name: str, tool: str) -> str:
    """'' or the refusal, in plain words, of a tool this door never runs for `name`."""
    if tool in REFUSED_TOOLS.get(name.lower(), ()):
        return (f"Refused: {name}'s {tool!r} is never run through this door -- it changes the "
                f"machine or pulls in local paths; run it in its own app, by hand.")
    return ""


def _inside(p: Path, ground: Path) -> bool:
    try:
        return p.resolve().is_relative_to(ground.resolve())
    except (OSError, ValueError):
        return False


def admit(name: str, argv: list, ground: Path = GROUND) -> tuple:
    """(argv ready to run, "") or (None, refusal in plain words).

    THE WALL. The program -- or the script node/python runs -- must resolve
    inside the ground. The argv handed back carries absolute paths, so what
    was checked is exactly what is started."""
    if not argv:
        return None, f"Refused: {name}'s command is empty."
    prog = argv[0]
    found = shutil.which(prog) if not (os.sep in prog or "/" in prog) else None
    exe = Path(found) if found else (ground / prog if not Path(prog).is_absolute() else Path(prog))
    stem = exe.stem.lower() if found else Path(prog).stem.lower()
    if stem in _INTERP:
        if not found and not exe.is_file():
            return None, f"Refused: {name}'s program {prog!r} was not found."
        i = 1
        while i < len(argv) and argv[i].startswith("-"):
            if argv[i] in _CODE_FLAGS or argv[i].split("=", 1)[0] in _CODE_FLAGS:
                return None, (f"Refused: {name}'s command loads code with "
                              f"{argv[i]!r}; only a script inside the ground "
                              f"is started.")
            i += 2 if argv[i] in _VALUE_FLAGS else 1
        if i >= len(argv):
            return None, f"Refused: {name}'s command names no script for {prog!r} to run."
        script = Path(argv[i])
        if not script.is_absolute():
            script = ground / script
        root = declared_root(name)
        if not _inside(script, ground) and not (root is not None and _inside(script, root)):
            return None, (f"Refused: {name}'s script is outside the ground ({ground})"
                          + (f" and outside its declared root ({root})" if root is not None else "")
                          + "; nothing was started.")
        if not script.is_file():
            return None, f"Refused: {name}'s script {argv[i]!r} does not exist."
        return [str(exe), *argv[1:i], str(script.resolve()), *argv[i + 1:]], ""
    if not _inside(exe, ground) or not exe.is_file():
        return None, (f"Refused: {name}'s program {prog!r} is not inside the "
                      f"ground ({ground}); nothing was started.")
    return [str(exe.resolve()), *argv[1:]], ""


def minimal_env(extra: dict | None = None) -> dict:
    """The allowlist, and nothing else. NODE_OPTIONS is never passed."""
    env = {k: os.environ[k] for k in ENV_KEEP if os.environ.get(k)}
    env.update(extra or {})
    env.pop("NODE_OPTIONS", None)
    return env


class StdioServer:
    """One MCP server process, spoken to over newline-delimited JSON-RPC 2.0."""

    def __init__(self, argv, cwd=None, env=None, timeout=60):
        self.argv = list(argv)
        self.cwd = str(cwd or GROUND)
        self.env = minimal_env(env)
        self.timeout = float(timeout)
        self.proc = None
        self._q = queue.Queue()
        self._err = collections.deque(maxlen=_STDERR_LINES)
        self._id = 0
        self._wlock = threading.Lock()
        self._threads = []

    # -- life ------------------------------------------------------------
    def start(self):
        """Spawn, then initialize and notifications/initialized."""
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            self.proc = subprocess.Popen(
                self.argv, cwd=self.cwd, env=self.env, shell=False,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, creationflags=flags)
        except OSError as exc:
            raise StdioError(f"it could not be started ({exc.strerror or exc})")
        for fn in (self._read_out, self._read_err):
            t = threading.Thread(target=fn, daemon=True)
            t.start()
            self._threads.append(t)
        self.request("initialize", {"protocolVersion": PROTOCOL,
                                    "capabilities": {}, "clientInfo": CLIENT})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return self

    def close(self):
        """Close stdin, give it a moment, then terminate, kill, and reap."""
        p, self.proc = self.proc, None
        if p is None:
            return
        try:
            p.stdin.close()
        except OSError:
            pass
        try:
            p.wait(timeout=2)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:
                p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait(timeout=5)
        for s in (p.stdout, p.stderr):
            try:
                s.close()
            except OSError:
                pass
        for t in self._threads:
            t.join(timeout=2)

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.close()

    # -- the wire ----------------------------------------------------------
    def _read_out(self):
        for raw in iter(self.proc.stdout.readline, b""):
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            try:
                self._q.put(json.loads(line))
            except ValueError:
                self._err.append("(stdout, not JSON) " + line[:300])
        self._q.put(_EOF)

    def _read_err(self):
        for raw in iter(self.proc.stderr.readline, b""):
            self._err.append(raw.decode("utf-8", "replace").rstrip()[:500])

    def stderr_tail(self, n=12) -> str:
        return "\n".join(list(self._err)[-n:])

    def _dead(self) -> StdioError:
        code = self.proc.poll() if self.proc else None
        tail = self.stderr_tail()
        return StdioError(f"it exited (code {code})"
                          + (f"; it last said:\n{tail}" if tail else ", saying nothing"))

    def _send(self, msg: dict):
        if self.proc is None or self.proc.poll() is not None:
            raise self._dead()
        data = (json.dumps(msg) + "\n").encode("utf-8")
        try:
            with self._wlock:
                self.proc.stdin.write(data)
                self.proc.stdin.flush()
        except OSError:
            raise self._dead()

    def request(self, method: str, params: dict, timeout=None) -> dict:
        """Send one request and wait, bounded, for the answer with its id."""
        self._id += 1
        rid = self._id
        self._send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        wait = float(timeout if timeout is not None else self.timeout)
        deadline = time.monotonic() + wait
        while True:
            left = deadline - time.monotonic()
            if left <= 0:
                raise StdioError(f"it did not answer {method} inside {wait:.0f}s")
            try:
                msg = self._q.get(timeout=left)
            except queue.Empty:
                continue
            if msg is _EOF:
                self._q.put(_EOF)
                try:
                    self.proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass
                raise self._dead()
            if not isinstance(msg, dict):
                continue
            if "method" in msg and "id" in msg:      # the server asks us
                self._answer(msg)
                continue
            if msg.get("id") != rid:                 # a notification, or stale
                continue
            if msg.get("error"):
                err = msg["error"]
                raise StdioError("it refused: "
                                 + str(err.get("message") if isinstance(err, dict) else err))
            return msg.get("result") or {}

    def _answer(self, msg: dict):
        """A ping is answered; anything else the server asks is declined."""
        if msg.get("method") == "ping":
            self._send({"jsonrpc": "2.0", "id": msg["id"], "result": {}})
        else:
            self._send({"jsonrpc": "2.0", "id": msg["id"], "error": {
                "code": -32601, "message": "manjuel does not offer " + str(msg.get("method"))}})

    # -- MCP -----------------------------------------------------------------
    def list_tools(self, timeout=None) -> list:
        """[{name, description, inputSchema}], every page."""
        tools, cursor = [], None
        for _ in range(50):
            res = self.request("tools/list", {"cursor": cursor} if cursor else {}, timeout)
            for t in res.get("tools") or []:
                if isinstance(t, dict):
                    tools.append({"name": t.get("name"),
                                  "description": t.get("description") or "",
                                  "inputSchema": t.get("inputSchema") or {}})
            cursor = res.get("nextCursor")
            if not cursor:
                break
        return tools

    def call(self, name: str, arguments: dict | None = None, timeout=None) -> str:
        """The tool's text, joined. A tool that fails says so as a refusal."""
        try:
            res = self.request("tools/call", {"name": name, "arguments": arguments or {}},
                               timeout)
        except StdioError as exc:
            if str(exc).startswith("it refused"):
                return f"Refused: {name} failed: {exc}"
            raise
        text = "\n".join(str(b.get("text")) for b in (res.get("content") or [])
                         if isinstance(b, dict) and b.get("text")).strip()
        if res.get("isError"):
            return f"Refused: {name} failed: " + (text or "and said nothing about why.")
        return text


# ---------------------------------------------------------------------------
# strokes
# ---------------------------------------------------------------------------

_FAKE = r'''
import json, sys
for line in sys.stdin:
    m = json.loads(line)
    if "id" not in m:
        continue
    meth, rid = m["method"], m["id"]
    if meth == "initialize":
        r = {"protocolVersion": m["params"]["protocolVersion"], "capabilities": {"tools": {}},
             "serverInfo": {"name": "fake", "version": "0"}}
    elif meth == "tools/list":
        r = {"tools": [{"name": "echo", "description": "says it back",
                        "inputSchema": {"type": "object"}},
                       {"name": "boom", "description": "fails"}]}
    elif meth == "tools/call":
        n = m["params"]["name"]
        if n == "echo":
            sys.stderr.write("echoing\n"); sys.stderr.flush()
            r = {"content": [{"type": "text", "text": "said " + json.dumps(m["params"]["arguments"])}]}
        elif n == "boom":
            r = {"content": [{"type": "text", "text": "it broke"}], "isError": True}
        elif n == "die":
            sys.stderr.write("dying now\n"); sys.stderr.flush(); sys.exit(3)
        elif n == "hang":
            import time; time.sleep(30); continue
        else:
            print(json.dumps({"jsonrpc": "2.0", "id": rid,
                              "error": {"code": -32602, "message": "no tool " + n}}), flush=True)
            continue
    else:
        continue
    print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": r}), flush=True)
'''


def _strokes() -> int:
    import tempfile
    fails = []

    def check(label, ok, got=""):
        print(("ok   " if ok else "FAIL ") + label + ("" if ok else f"  -- {got!r}"))
        if not ok:
            fails.append(label)

    tmp = tempfile.mkdtemp(prefix="mcp_stdio_")
    try:
        script = Path(tmp) / "fake.py"
        script.write_text(_FAKE, encoding="utf-8", newline="\r\n")
        argv = [sys.executable, "-I", str(script)]
        with StdioServer(argv, cwd=tmp, timeout=20) as s:
            names = [t["name"] for t in s.list_tools()]
            check("lists the fake's tools", names == ["echo", "boom"], names)
            out = s.call("echo", {"a": 1})
            check("calls a tool and joins its text", out == 'said {"a": 1}', out)
            out = s.call("boom")
            check("isError is a refusal naming the tool",
                  out.startswith("Refused: boom failed: it broke"), out)
            out = s.call("nosuch")
            check("a JSON-RPC error is a refusal", out.startswith("Refused: nosuch failed"), out)
            t0 = time.monotonic()
            try:
                s.call("hang", timeout=1)
                check("a silent server is bounded", False, "no error")
            except StdioError as exc:
                check("a silent server is bounded",
                      "inside 1s" in str(exc) and time.monotonic() - t0 < 5, str(exc))
        with StdioServer(argv, cwd=tmp, timeout=20) as s:
            try:
                s.call("die")
                check("a dead server is reported", False, "no error")
            except StdioError as exc:
                check("a dead server is reported with its stderr",
                      "exited (code 3)" in str(exc) and "dying now" in str(exc), str(exc))
        check("closed and reaped", s.proc is None)

        # The wall: a script outside the ground is refused by name.
        ran, why = admit("fake", [sys.executable, str(script)])
        check("a script outside the ground is refused",
              ran is None and "outside the ground" in why, why)
        ran, why = admit("fake", [sys.executable, "-c", "print(1)"])
        check("python -c is refused", ran is None and "loads code" in why, why)
        ran, why = admit("fake", ["node", "-r", "x", "manjuel/mcp_stdio.py"])
        check("node -r is refused", ran is None, why)
        ran, why = admit("fake", [str(Path(tmp) / "x.exe")])
        check("a program outside the ground is refused",
              ran is None and "not inside the ground" in why, why)
        ran, why = admit("self", [sys.executable, "-I", "-X", "utf8", "manjuel/mcp_stdio.py"])
        check("a script inside the ground is admitted, made absolute",
              ran is not None and ran[-1] == str((GROUND / "manjuel/mcp_stdio.py").resolve()), why)

        # A ROOT HE DECLARES (2026-10-22, the second brain): a script outside the ground is
        # admitted inside that one server's own declared root, and nowhere else.
        os.environ["MANJUEL_MCP_FAKE_ROOT"] = tmp
        try:
            ran, why = admit("fake", [sys.executable, str(script)])
            check("a script inside the server's declared root is admitted",
                  ran is not None and ran[-1] == str(script.resolve()), why)
            ran, why = admit("other", [sys.executable, str(script)])
            check("another server's root admits nothing for this one",
                  ran is None and "outside the ground" in why, why)
            os.environ["MANJUEL_MCP_FAKE_ROOT"] = str(Path(tmp) / "sub")
            ran, why = admit("fake", [sys.executable, str(script)])
            check("a script outside the declared root is still refused",
                  ran is None and "outside the ground" in why and "declared root" in why, why)
        finally:
            os.environ.pop("MANJUEL_MCP_FAKE_ROOT", None)
        # TOOLS REFUSED BY NAME: the second brain's tools that change the machine or pull in
        # local paths never run through this door, whoever calls.
        why = refused_tool("notes", "system_update")
        check("the notes server's system_update is refused by name",
              why.startswith("Refused") and "system_update" in why, why)
        check("its reads and its notes pass",
              not refused_tool("notes", "notes_search") and not refused_tool("notes", "llm_ask")
              and not refused_tool("rea", "system_update"), "")

        # The environment is the allowlist only.
        os.environ["MANJUEL_STROKE_SECRET"] = "x"
        os.environ["NODE_OPTIONS"] = "--require evil"
        try:
            env = minimal_env()
            check("the environment is the allowlist",
                  set(env) <= set(ENV_KEEP) and "NODE_OPTIONS" not in env, sorted(env))
        finally:
            os.environ.pop("MANJUEL_STROKE_SECRET", None)
            os.environ.pop("NODE_OPTIONS", None)

        # servers() reads the _CMD dials.
        os.environ["MANJUEL_MCP_STROKE_CMD"] = 'node "a b/x.mjs" mcp'
        try:
            got = servers().get("stroke")
            check("servers() splits a _CMD dial, quotes stripped",
                  got == ["node", "a b/x.mjs", "mcp"], got)
        finally:
            os.environ.pop("MANJUEL_MCP_STROKE_CMD", None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{'ok' if not fails else 'FAILED'}: {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(_strokes())
