"""A `.env` beside the work, honored and never printed.

LAW 9: "Keys are silent. A `.env` beside the work is honored, never printed,
copied, or committed." So this reads the file, sets what is missing, and
reports only KEY NAMES -- never a value, not even in an error.

What a .env here CAN change
---------------------------
Anything manjuel itself reads, because manjuel reads it at ITS startup:

    MANJUEL_KEEP_ALIVE=30m      how long Ollama holds a model (per-request)
    MANJUEL_NO_WARM=1           skip warming models on launch
    MANJUEL_GIT_REMOTE=1        allow git pull/push

(`MANJUEL_OLLAMA_HOST` stood in this list until 2026-09-29. Nothing has ever
read it: the runtime binds the rack on this machine's own loopback, and RULE 4
keeps it there. A dial named in a docstring and read by nothing is a promise
the code does not keep.)

What it CANNOT change
---------------------
`OLLAMA_NUM_PARALLEL` and `OLLAMA_MAX_LOADED_MODELS` are read by the `ollama
serve` PROCESS when IT starts. Setting them here puts them in manjuel's
environment, which the already-running server never reads. Writing them in a
.env and believing they took effect is worse than not setting them, so if they
appear here manjuel says plainly that they were ignored and where they belong.

An existing environment variable always wins: the shell you launched from is a
more deliberate act than a file you wrote once.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

# Set by the ollama server at its own startup. We can read these to compare
# intent against reality, but setting them from here does nothing.
SERVER_ONLY = {
    "OLLAMA_NUM_PARALLEL",
    "OLLAMA_MAX_LOADED_MODELS",
    "OLLAMA_KEEP_ALIVE",
    "OLLAMA_HOST",
    "OLLAMA_MODELS",
    "OLLAMA_FLASH_ATTENTION",
}


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def load(path: Path) -> tuple[list[str], list[str], list[str], str]:
    """Read `path` into the environment.

    Returns (applied, already_set, server_only, unread): three lists of KEY
    NAMES, and -- when the file is THERE AND COULD NOT BE READ -- the kind of
    fault that stopped it, else "". No value is returned, logged, or raised.

    A `.env` THAT CANNOT BE READ IS SAID SO (2026-09-29). This answered three
    empty lists for a file it could not read, exactly what it answers for no
    file at all, so the boot printed nothing and every dial in it stood at its
    default with no word that it had. The likeliest cause on this machine is
    the ordinary one: PowerShell's `>` writes UTF-16, which is not UTF-8 text.

    AND A BYTE-ORDER MARK IS NOT PART OF A NAME. PowerShell's `-Encoding UTF8`
    writes one; read as plain UTF-8 it became the first three bytes of the
    first key, which was then set under a name nothing reads and REPORTED as
    set. `utf-8-sig` reads both shapes.
    """
    applied: list[str] = []
    already: list[str] = []
    server: list[str] = []

    path = Path(path)
    if not path.exists():
        return applied, already, server, ""

    try:
        text = path.read_text(encoding="utf-8-sig")
    except Exception as exc:
        # The KIND of fault only: a message can carry what was in the file.
        return applied, already, server, type(exc).__name__

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.lower().startswith("export "):
            line = line[7:].lstrip()

        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue

        if key in SERVER_ONLY:
            # Honest about the limit rather than silently doing nothing.
            server.append(key)
            continue
        if key in os.environ:
            already.append(key)
            continue

        # A TRAILING COMMENT IS NOT PART OF THE VALUE (his ruling 2026-09-30,
        # WHAT'S LEFT B8): `KEY=value # note` reads as `value`. Only ` #`
        # after whitespace, and only on an unquoted value -- a `#` inside a
        # value with no space before it stays (keys can hold one), and a
        # quoted value is taken whole.
        v = value.strip()
        if not (len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'"):
            v = re.split(r"\s+#", v, 1)[0].rstrip()
        os.environ[key] = _unquote(v)
        applied.append(key)

    return applied, already, server, ""


def report(applied: list[str], already: list[str], server: list[str],
           unread: str = "") -> list[str]:
    """Lines to print. Key names only -- never a value (LAW 9)."""
    out: list[str] = []
    if unread:
        out.append(f"  .env: PRESENT BUT NOT READ ({unread}) -- nothing in it was "
                   f"set, so every dial stands at")
        out.append( "        its default or the shell's. It must be UTF-8 text; "
                    "PowerShell's `>` writes UTF-16.")
    if applied:
        out.append(f"  .env: set {', '.join(sorted(applied))}")
    if already:
        out.append(f"  .env: {', '.join(sorted(already))} already in the "
                   f"environment, left alone")
    if server:
        out.append(f"  .env: {', '.join(sorted(server))} IGNORED — the ollama "
                   f"server reads those at its own startup,")
        out.append( "        so setting them here does nothing. Set them where "
                    "Ollama launches, then restart it.")
    return out
