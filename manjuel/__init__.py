"""manjuel -- local multi-agent pipeline driven by agents.md."""

__version__ = "0.1.13"

# THE OLD DIALS STILL TURN. Renamed from chainkit 2026-09-09 at the
# operator's word. Twenty-two CHAINKIT_* names are documented in RUNBOOK's
# dial table and may sit in a .env or a shell that predates the rename; a
# dial that silently stops working is worse than one that is gone. Each is
# honoured once, at import, and only when its MANJUEL_ twin is unset.
def carry_old_dials():
    """Map any CHAINKIT_* to its MANJUEL_* twin. Idempotent: only an
    UNSET twin is written, so calling it twice costs nothing.

    CALL IT AGAIN AFTER .env IS READ. This runs once at import, which sees
    only what the shell held before the process started -- and .env is read
    later, in cli.main and serve.main. Measured 2026-09-09:
    CHAINKIT_GIT_REMOTE=1 in a .env was applied by dotenv and its twin was
    still unset, so the dial did nothing. .env.example documented exactly
    those names, which made the estate's own example the way to produce a
    dead dial.
    """
    import os
    carried = []
    for k, v in list(os.environ.items()):
        if not k.startswith('CHAINKIT_'):
            continue
        new = 'MANJUEL_' + k[len('CHAINKIT_'):]
        if not os.environ.get(new):
            os.environ[new] = v
            carried.append(k)
    return carried


_carry_old_dials = carry_old_dials      # the old private name still answers
OLD_DIALS_CARRIED = carry_old_dials()


# THE MODULES THAT TAKE A DIAL WHEN THEY ARE IMPORTED (2026-09-15). Every door
# imports them before it reads `.env` -- cli.main, serve.main and the standup
# all load the file after `from manjuel import ...` has run -- so a dial written
# in `.env` reached the environment and was never read, so dotenv could report
# ".env: set MANJUEL_SEAT_TIMEOUT" over a seat bound that never moved.
_DIAL_MODULES = ("runtime", "skills", "pipeline", "voice")


def read_dials():
    """CALL THIS AFTER .env IS READ, in place of carry_old_dials: it carries
    the old CHAINKIT_ names first, then has every engine module already
    imported read its dials again. A module not yet imported reads them itself
    when it is. Returns what the carry carried."""
    import sys
    carried = carry_old_dials()
    for name in _DIAL_MODULES:
        module = sys.modules.get(f"{__name__}.{name}")
        if module is not None:
            module.read_dials()
    return carried
