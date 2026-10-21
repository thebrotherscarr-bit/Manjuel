"""Schedules and goals: Steward's work that runs while nobody is at the glass.

WHY. A /drive job runs when he types it. Some work is wanted on a clock (the
docs checked every morning, the tidy every night) and some is wanted until it
is done (a goal worked every half hour until its check passes). Both need a
record that outlives the process: what to run, when it is next due, what the
last runs said, and whether the thing is still worth running. That record is
this module; the door reads it on its idle tick and runs what is due.

What it borrows, from the harness study:

  Hermes' cron      "every 30m", "every day at 18:00", "at 18:00", a five-field
                    cron line, a one-shot. A run missed while the machine was
                    off is run ONCE when it comes back, never once per slot it
                    missed (`missed` names them; `record` steps past them all).
  Cline's leases    a run in flight holds its row for LEASE_SECONDS with a
                    "lease" event, taken under a lock on the store, so two
                    processes never run the same row; a lease whose process
                    died runs out and the row is due again.
  OpenClaw's goals  a goal has a budget of runs, and is marked BLOCKED only
                    when the same blocker comes back BLOCK_AFTER runs running
                    -- one failure is weather, three of the same is a wall.
  Hermes' /goal     a goal is done only when its deterministic check passes:
                    the drive text must carry "| check: <command>".

ONLY `auto` RUNS UNWATCHED. A scheduled run has nobody to answer a card, and an
unanswered card is a no; an `ask` or plan job would have every write refused.
So the drive text is given `auto` when it names no approval word, and `ask` is
refused by name.

THE STORE. state/schedules.jsonl in the ground, append-only, one JSON row per
event ("add", "lease", "record", "drop"), each row carrying the whole schedule
as it stands after the event; the fold keeps the latest row per id. Rows end
CRLF and are synced to the disk, as the drive journal's are. No folder is ever
made here: a ground with no state/ folder is refused, and says so.

THE STORE NEVER TAKES THE DOOR DOWN. Nothing here raises: a store that cannot
be read is empty, a write that cannot land returns False, a lock that cannot be
had claims nothing.

A row:

  kind      "schedule" | "goal"
  id        six hex characters
  said      the /drive text it runs: "auto [mode] <goal> [| do: ..] [| check: ..]"
  every     seconds between runs, or null
  at        "HH:MM", daily, or null
  cron      "m h dom mon dow", or null
  once      an iso time, or null
  next      the iso time it is next due (null once it is not active)
  last      the iso time of its last run, or null
  runs      runs recorded
  verdicts  the last KEEP_VERDICTS verdicts, oldest first
  state     "active" | "done" | "blocked" | "dropped"
  made      the iso time it was added
  budget    a goal's runs before it is blocked (GOAL_BUDGET), or null
  lease     the iso time a run in flight holds it until, or null
  holder    who holds the lease, or null

Times are the machine's local time, to the second, with no zone.

The standard library alone.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

STORE = "schedules.jsonl"
FMT = "%Y-%m-%dT%H:%M:%S"
LEASE_SECONDS = 2 * 3600    # a run in flight holds its row this long
GOAL_EVERY = 1800           # a goal is worked every half hour
GOAL_BUDGET = 48            # ... for a day's worth of runs at most
KEEP_VERDICTS = 5
BLOCK_AFTER = 3             # the same non-passing verdict this many runs running
MIN_EVERY = 60              # nothing runs more often than once a minute
DONE_VERDICTS = ("passed", "shipped")
STATES = ("active", "done", "blocked", "dropped")
LOCK_AT = 0x40000000        # the byte locked on Windows: far past any row
USAGE = ("/schedule every 30m <drive text> | every 2h .. | every day at 18:00 .. | "
         "at 18:00 .. | cron \"*/15 * * * *\" .. | once 2026-10-22T09:00 ..;  "
         "/goal <drive text> | check: <command>")

_UNITS = {"s": 1, "sec": 1, "secs": 1, "second": 1, "seconds": 1,
          "m": 60, "min": 60, "mins": 60, "minute": 60, "minutes": 60,
          "h": 3600, "hr": 3600, "hrs": 3600, "hour": 3600, "hours": 3600,
          "d": 86400, "day": 86400, "days": 86400}


# ---------------------------------------------------------------------
# time
# ---------------------------------------------------------------------

def _now(now=None) -> datetime:
    """`now` as a plain local datetime to the second: None is the clock, a string
    is read as iso, an aware datetime is brought to local time."""
    if now is None:
        return datetime.now().replace(microsecond=0)
    if isinstance(now, str):
        now = datetime.fromisoformat(now.strip())
    if now.tzinfo is not None:
        now = now.astimezone().replace(tzinfo=None)
    return now.replace(microsecond=0)


def _iso(dt) -> str | None:
    return dt.strftime(FMT) if dt is not None else None


def _when(text):
    """An iso string as a datetime, or None where it is missing or unreadable."""
    try:
        return _now(text) if text else None
    except (TypeError, ValueError):
        return None


def duration(text) -> int | None:
    """Seconds in "30m", "2h", "1h30m", "1h 30m", "90 seconds", "2 hours", "hour",
    "day"; None for anything else."""
    s = str(text or "").strip().lower()
    if not s:
        return None
    if s in _UNITS:
        return _UNITS[s]
    pairs = re.findall(r"(\d+)\s*([a-z]+)", s)
    if not pairs or re.sub(r"\s+", "", s) != "".join(n + u for n, u in pairs):
        return None
    total = 0
    for n, u in pairs:
        if u not in _UNITS:
            return None
        total += int(n) * _UNITS[u]
    return total or None


def span(seconds) -> str:
    """Seconds said short: 1800 -> "30m", 5400 -> "1h30m", 86400 -> "1d"."""
    s, out = int(seconds or 0), ""
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60), ("s", 1)):
        if s >= size:
            out += f"{s // size}{unit}"
            s %= size
    return out or "0s"


# ---------------------------------------------------------------------
# cron: minute hour day-of-month month day-of-week
# ---------------------------------------------------------------------

_CRON = ((0, 59), (0, 23), (1, 31), (1, 12), (0, 7))


def _cron_field(spec: str, lo: int, hi: int) -> set:
    """One field: *, a value, a range a-b, a list a,b,c, and steps on any of them
    (*/15, 1-5/2, 10/5). Raises ValueError on anything else."""
    out = set()
    for part in spec.split(","):
        step = 1
        if "/" in part:
            part, raw = part.split("/", 1)
            step = int(raw)
            if step < 1:
                raise ValueError(f"a step of {step}")
        if part == "*":
            a, b = lo, hi
        elif "-" in part:
            x, y = part.split("-", 1)
            a, b = int(x), int(y)
        else:
            a = int(part)
            b = hi if step > 1 else a
        if not lo <= a <= b <= hi:
            raise ValueError(f"{part} is outside {lo}-{hi}")
        out.update(range(a, b + 1, step))
    return out


def cron_parse(expr: str) -> tuple:
    """(minutes, hours, days, months, weekdays, day_star, weekday_star). Weekdays
    count Sunday as 0 (and 7). Raises ValueError on a line that is not five fields."""
    fields = str(expr or "").split()
    if len(fields) != 5:
        raise ValueError(f"a cron line has five fields, not {len(fields)}")
    sets = [_cron_field(f, lo, hi) for f, (lo, hi) in zip(fields, _CRON)]
    if 7 in sets[4]:
        sets[4] = (sets[4] - {7}) | {0}
    return tuple(sets) + (fields[2].startswith("*"), fields[4].startswith("*"))


def cron_next(expr, after) -> datetime | None:
    """The first minute strictly after `after` that the cron line names, or None
    when it names none in the next five years ("0 0 30 2 *"). When both the day of
    the month and the day of the week are restricted, either one matching is a
    match, as in every cron since Vixie's."""
    try:
        mins, hours, days, months, dows, day_star, dow_star = cron_parse(expr)
    except ValueError:
        return None
    t = _now(after).replace(second=0) + timedelta(minutes=1)
    limit = t + timedelta(days=5 * 366)
    while t <= limit:
        if t.month not in months:
            t = datetime(t.year + (t.month == 12), t.month % 12 + 1, 1)
            continue
        dom_ok, dow_ok = t.day in days, (t.weekday() + 1) % 7 in dows
        if day_star and dow_star:
            ok = True
        elif day_star:
            ok = dow_ok
        elif dow_star:
            ok = dom_ok
        else:
            ok = dom_ok or dow_ok
        if not ok:
            t = (t + timedelta(days=1)).replace(hour=0, minute=0)
            continue
        if t.hour not in hours:
            t = (t + timedelta(hours=1)).replace(minute=0)
            continue
        if t.minute not in mins:
            t += timedelta(minutes=1)
            continue
        return t
    return None


def _daily(hhmm: str, after: datetime) -> datetime | None:
    """The first HH:MM strictly after `after`."""
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", str(hhmm or "").strip())
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        return None
    t = after.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0)
    return t if t > after else t + timedelta(days=1)


def next_after(row: dict, after) -> datetime | None:
    """When the row is next due after a run at `after`: every -> after + every;
    at -> the next HH:MM; cron -> the next minute it names; once -> never again."""
    after = _now(after)
    if row.get("once"):
        return None
    if row.get("cron"):
        return cron_next(row["cron"], after)
    if row.get("at"):
        return _daily(row["at"], after)
    if row.get("every"):
        return after + timedelta(seconds=int(row["every"]))
    return None


def interval(row: dict) -> int | None:
    """The row's gap between runs in seconds, around its `next`; None for a once."""
    if row.get("once"):
        return None
    if row.get("every"):
        return int(row["every"])
    if row.get("at"):
        return 86400
    if row.get("cron"):
        nxt = _when(row.get("next"))
        if nxt is None:
            return None
        after = cron_next(row["cron"], nxt)
        return int((after - nxt).total_seconds()) if after else None
    return None


# ---------------------------------------------------------------------
# parse
# ---------------------------------------------------------------------

def _take(text: str, n: int):
    """The first n words of `text` and the rest exactly as written, or None."""
    words, rest = [], str(text or "").lstrip()
    for _ in range(n):
        m = re.match(r"(\S+)\s*", rest)
        if not m:
            return None
        words.append(m.group(1))
        rest = rest[m.end():]
    return words, rest


def _drive_text(text: str, goal: bool) -> tuple:
    """(said, why): the drive text with `auto` in front, or (None, why it is refused).
    A goal must carry a check; a schedule without one is allowed and noted."""
    t = str(text or "").strip()
    if t.lower().startswith("/drive"):
        t = t[len("/drive"):].strip()
    if not t:
        return None, "no drive text: say what it runs. " + USAGE
    first = t.split()[0].lower()
    if first == "ask":
        return None, ("refused: `ask` with nobody watching makes every card a no; "
                      "a schedule runs `auto` only")
    said = t if first == "auto" else "auto " + t
    cut = said.lower().rfind("| check:")
    check = said[cut + len("| check:"):].strip() if cut >= 0 else ""
    body = (said[:cut] if cut >= 0 else said)[len("auto"):].strip()
    if not body:
        return None, "no goal: the drive text says nothing to do"
    if cut >= 0 and not check:
        return None, "an empty check: `| check:` must name a command"
    if goal and not check:
        return None, ("refused: a goal needs `| check: <command>` -- the check, "
                      "never the model, says it is done")
    if not check:
        return said, "noted: no check, so Steward's own word ends each run"
    return said, ""


def _row(kind, said, made, every=None, at=None, cron=None, once=None) -> dict:
    return {"kind": kind, "id": os.urandom(3).hex(), "said": said, "every": every,
            "at": at, "cron": cron, "once": once, "next": None, "last": None,
            "runs": 0, "verdicts": [], "state": "active", "made": _iso(made),
            "budget": GOAL_BUDGET if kind == "goal" else None, "lease": None, "holder": None}


def parse(text, now=None) -> tuple:
    """`/schedule <when> <drive text>` or `/goal <drive text>` -> (row, why), or
    (None, why it is refused). `why` is "" or a note when the row is good.

      /schedule every 30m <..>          every 2h, every 1h30m, every 90 minutes
      /schedule every day at 18:00 <..> daily; `at 18:00 <..>` says the same
      /schedule cron "*/15 * * * *" <..>
      /schedule once 2026-10-22T09:00 <..>
      /goal <..> | check: <command>     every GOAL_EVERY until the check passes

    The first run of a goal is due at once; of a schedule, at its first slot."""
    try:
        now = _now(now)
    except (TypeError, ValueError):
        return None, "no clock"
    split = _take(text, 1)
    if split is None:
        return None, USAGE
    head, rest = split[0][0].lower().lstrip("/"), split[1]

    if head == "goal":
        said, why = _drive_text(rest, goal=True)
        if said is None:
            return None, why
        row = _row("goal", said, now, every=GOAL_EVERY)
        row["next"] = _iso(now)
        return row, why

    if head != "schedule":
        return None, "not a /schedule or /goal. " + USAGE
    got = _take(rest, 1)
    if got is None:
        return None, USAGE
    word, rest = got[0][0].lower(), got[1]
    every = at = cron = once = None
    first = None

    if word == "every":
        day_at = _take(rest, 3)
        if day_at and [w.lower() for w in day_at[0][:2]] == ["day", "at"]:
            word, rest = "at", day_at[0][2] + " " + day_at[1]
        else:
            for k in (4, 3, 2, 1):
                got = _take(rest, k)
                if got and duration(" ".join(got[0])):
                    every, rest = duration(" ".join(got[0])), got[1]
                    break
            if every is None:
                return None, "every what? a span such as 30m, 2h, 1h30m, or `day at 18:00`"
            if every < MIN_EVERY:
                return None, f"refused: every {span(every)} is too often (once a minute at most)"
            first = now + timedelta(seconds=every)

    if word == "at":
        got = _take(rest, 1)
        hhmm = got[0][0] if got else ""
        first = _daily(hhmm, now) if got else None
        if first is None:
            return None, f"at what time? HH:MM, 00:00 to 23:59, not {hhmm!r}"
        at, rest = hhmm, got[1]
    elif word == "cron":
        s = rest.lstrip()
        if s[:1] in ("'", '"'):
            end = s.find(s[0], 1)
            if end < 0:
                return None, "the cron line's quote is never closed"
            expr, rest = s[1:end], s[end + 1:]
        else:
            got = _take(s, 5)
            if got is None:
                return None, "a cron line has five fields"
            expr, rest = " ".join(got[0]), got[1]
        try:
            cron_parse(expr)
        except ValueError as exc:
            return None, f"not a cron line ({exc}): {expr!r}"
        cron = " ".join(expr.split())
        first = cron_next(cron, now)
        if first is None:
            return None, f"the cron line {cron!r} names no time in the next five years"
    elif word == "once":
        got = _take(rest, 1)
        first = _when(got[0][0]) if got else None
        if first is None:
            return None, "once when? an iso time such as 2026-10-22T09:00"
        if first <= now:
            return None, f"refused: {_iso(first)} has already passed"
        once, rest = _iso(first), got[1]
    elif word != "every":
        return None, "when? " + USAGE

    said, why = _drive_text(rest, goal=False)
    if said is None:
        return None, why
    row = _row("schedule", said, now, every=every, at=at, cron=cron, once=once)
    row["next"] = _iso(first)
    return row, why


# ---------------------------------------------------------------------
# the store
# ---------------------------------------------------------------------

def _store(ground) -> Path:
    return Path(ground) / "state" / STORE


def _ready(ground) -> str:
    """"" when the ground has its state/ folder; else why nothing can be kept."""
    try:
        if (Path(ground) / "state").is_dir():
            return ""
    except (OSError, TypeError):
        pass
    return f"refused: no state/ folder in {ground}; none is made here"


def _write(ground, event: str, row: dict, now=None) -> bool:
    """Append one event row, flushed and synced. True when it reached the disk.
    Never raises; never makes a folder."""
    if _ready(ground):
        return False
    try:
        out = {"event": str(event), "ts": _iso(_now(now))}
        out.update(row)
        line = (json.dumps(out, ensure_ascii=False) + "\r\n").encode("utf-8", "surrogatepass")
        with open(_store(ground), "ab+") as f:
            end = f.seek(0, 2)
            if end:                         # a row cut short by a crash: begin afresh
                f.seek(end - 1)
                if f.read(1) != b"\n":
                    line = b"\r\n" + line
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception:
        return False


def _rows(ground) -> list:
    """Every whole event row, in order. A row cut short is skipped."""
    out = []
    try:
        data = _store(ground).read_bytes()
    except (OSError, TypeError):
        return out
    for raw in data.split(b"\n"):
        raw = raw.strip(b"\r")
        if not raw:
            continue
        try:
            row = json.loads(raw.decode("utf-8", "surrogatepass"))
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(row, dict) and row.get("id"):
            out.append(row)
    return out


def fold(ground) -> dict:
    """{id: row}: the latest event per id, in the order the ids were first added."""
    out = {}
    for r in _rows(ground):
        out[str(r["id"])] = {k: v for k, v in r.items() if k not in ("event", "ts")}
    return out


class _Lock:
    """The store held by one process at a time, for a read-fold-write. On Windows a
    byte far past the rows is locked (msvcrt retries for ten seconds); elsewhere the
    file is flocked. `ok` is False when it could not be had."""

    def __init__(self, ground):
        self.ground, self.f, self.ok = ground, None, False

    def __enter__(self):
        try:
            self.f = open(_store(self.ground), "ab+")
            if os.name == "nt":
                import msvcrt
                self.f.seek(LOCK_AT)
                msvcrt.locking(self.f.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(self.f.fileno(), fcntl.LOCK_EX)
            self.ok = True
        except Exception:
            self.ok = False
        return self

    def __exit__(self, *exc):
        try:
            if self.f is not None and self.ok:
                if os.name == "nt":
                    import msvcrt
                    self.f.seek(LOCK_AT)
                    msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self.f.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        try:
            if self.f is not None:
                self.f.close()
        except Exception:
            pass
        return False


def _valid(row) -> str:
    """"" for a row the store can keep; else why not."""
    if not isinstance(row, dict):
        return "not a row"
    if row.get("kind") not in ("schedule", "goal"):
        return "a row is a schedule or a goal"
    said = str(row.get("said") or "")
    if said.lower().split()[:1] != ["auto"]:
        return "refused: a scheduled run is `auto` only"
    if row["kind"] == "goal" and "| check:" not in said.lower():
        return "refused: a goal needs `| check: <command>`"
    timed = [k for k in ("every", "at", "cron", "once") if row.get(k)]
    if len(timed) != 1:
        return "a row has one of every, at, cron, once"
    if _when(row.get("next")) is None:
        return "a row needs its next time"
    return ""


# ---------------------------------------------------------------------
# the API
# ---------------------------------------------------------------------

def add(ground, row, now=None) -> tuple:
    """Keep a parsed row: (row as kept, "") or (None, why it was refused)."""
    why = _ready(ground) or _valid(row)
    if why:
        return None, why
    try:
        row = dict(row)
        row.setdefault("made", _iso(_now(now)))
        with _Lock(ground) as lock:
            if not lock.ok:
                return None, "the store is held by another process; try again"
            have = fold(ground)
            while not row.get("id") or row["id"] in have:
                row["id"] = os.urandom(3).hex()
            if not _write(ground, "add", row, now):
                return None, "the store could not be written"
        return row, ""
    except Exception as exc:
        return None, f"not kept: {exc}"


def drop(ground, ident, now=None) -> tuple:
    """Stop a row: (row, "") or (None, why). The record of it stays."""
    why = _ready(ground)
    if why:
        return None, why
    try:
        with _Lock(ground) as lock:
            if not lock.ok:
                return None, "the store is held by another process; try again"
            row = fold(ground).get(str(ident or "").strip())
            if row is None:
                return None, f"no schedule or goal {ident!r}"
            row.update(state="dropped", next=None, lease=None, holder=None)
            if not _write(ground, "drop", row, now):
                return None, "the store could not be written"
        return row, ""
    except Exception as exc:
        return None, f"not dropped: {exc}"


def _leased(row, now) -> bool:
    until = _when(row.get("lease"))
    return until is not None and until > now


def due(ground, now=None) -> list:
    """The active rows due at `now`, oldest first, each now leased to this process
    for LEASE_SECONDS: another process asking gets none of them, and neither does
    this one until `record` lets go or the lease runs out. Each row comes back at
    most once per tick, however many slots it missed."""
    if _ready(ground):
        return []
    try:
        now = _now(now)
        holder = f"{os.getpid()}-{os.urandom(2).hex()}"
        out = []
        with _Lock(ground) as lock:
            if not lock.ok:
                return []
            for row in fold(ground).values():
                nxt = _when(row.get("next"))
                if row.get("state") != "active" or nxt is None or nxt > now or _leased(row, now):
                    continue
                row.update(lease=_iso(now + timedelta(seconds=LEASE_SECONDS)), holder=holder)
                if _write(ground, "lease", row, now):
                    out.append(row)
        return sorted(out, key=lambda r: r.get("next") or "")
    except Exception:
        return []


def missed(ground, now=None) -> list:
    """The active rows more than one interval late: the machine was off, or the door
    was. Each is run ONCE (it is in `due` too), and `record` steps past every slot
    it missed -- Hermes' catch-up, never a burst of make-up runs."""
    try:
        now = _now(now)
        out = []
        for row in fold(ground).values():
            nxt, gap = _when(row.get("next")), interval(row)
            if row.get("state") != "active" or nxt is None or gap is None or _leased(row, now):
                continue
            if (now - nxt).total_seconds() > gap:
                out.append(row)
        return out
    except Exception:
        return []


def record(ground, ident, verdict, now=None):
    """A run's end: the row as it now stands, or None. Runs + 1, the verdict kept
    (the last KEEP_VERDICTS), the lease let go, and the next time set from now.
    A goal whose verdict passed is done; a goal whose last BLOCK_AFTER verdicts are
    the same non-passing one is blocked, and so is one that spent its budget; a
    once is done."""
    if _ready(ground):
        return None
    try:
        now = _now(now)
        said = str(verdict or "").strip() or "none"
        with _Lock(ground) as lock:
            if not lock.ok:
                return None
            row = fold(ground).get(str(ident or "").strip())
            if row is None:
                return None
            row["runs"] = int(row.get("runs") or 0) + 1
            row["last"] = _iso(now)
            row["verdicts"] = (list(row.get("verdicts") or []) + [said])[-KEEP_VERDICTS:]
            row.update(lease=None, holder=None)
            if row.get("state") == "active":
                tail = [v.strip().lower() for v in row["verdicts"][-BLOCK_AFTER:]]
                if row.get("kind") == "goal":
                    if said.lower() in DONE_VERDICTS:
                        row["state"] = "done"
                    elif len(tail) == BLOCK_AFTER and len(set(tail)) == 1:
                        row["state"] = "blocked"
                    elif row.get("budget") and row["runs"] >= int(row["budget"]):
                        row["state"] = "blocked"
                if row["state"] == "active":
                    nxt = next_after(row, now)
                    if nxt is None:
                        row["state"] = "done"      # a once, or a cron line with no time left
                    row["next"] = _iso(nxt)
                else:
                    row["next"] = None
            if not _write(ground, "record", row, now):
                return None
        return row
    except Exception:
        return None


def _describe(row) -> str:
    if row.get("once"):
        return "once " + str(row["once"])
    if row.get("cron"):
        return 'cron "' + str(row["cron"]) + '"'
    if row.get("at"):
        return "daily at " + str(row["at"])
    return "every " + span(row.get("every"))


def listing(ground) -> str:
    """Every schedule and goal, active first, one line each."""
    why = _ready(ground)
    if why:
        return why
    rows = list(fold(ground).values())
    if not rows:
        return "no schedules or goals"
    rows.sort(key=lambda r: STATES.index(r.get("state")) if r.get("state") in STATES else 9)
    lines = []
    for r in rows:
        verdicts = r.get("verdicts") or []
        last = verdicts[-1] if verdicts else "-"
        nxt = r.get("next") or "-"
        lease = "  (running)" if r.get("lease") else ""
        lines.append(f"{r.get('id', '?'):<7} {r.get('kind', '?'):<9} {r.get('state', '?'):<8} "
                     f"{_describe(r):<24} next {nxt:<19}  runs {r.get('runs', 0):<3} "
                     f"last {last}{lease}")
        lines.append("        " + str(r.get("said") or ""))
    return "\n".join(lines)


# ---------------------------------------------------------------------
# the proof
# ---------------------------------------------------------------------

def _strokes() -> None:
    """The module's own proof, in a throwaway ground with its own state/ folder."""
    import shutil
    import tempfile
    now = datetime(2026, 10, 21, 12, 7, 30)        # a Wednesday
    tmp = Path(tempfile.mkdtemp(prefix="schedule_"))
    try:
        # durations
        assert duration("30m") == 1800 and duration("2h") == 7200 and duration("1h30m") == 5400
        assert duration("1h 30m") == 5400 and duration("90 minutes") == 5400
        assert duration("hour") == 3600 and duration("2 hours auto") is None and duration("2x") is None
        assert span(5400) == "1h30m" and span(86400) == "1d"

        # the cron evaluator
        assert cron_next("*/15 * * * *", now) == datetime(2026, 10, 21, 12, 15)
        assert cron_next("*/15 * * * *", datetime(2026, 10, 21, 12, 15)) == datetime(2026, 10, 21, 12, 30)
        assert cron_next("0 9 * * 1-5", now) == datetime(2026, 10, 22, 9, 0)         # Thursday
        assert cron_next("0 9 * * 1-5", datetime(2026, 10, 23, 10, 0)) == datetime(2026, 10, 26, 9, 0)
        assert cron_next("30 18 1,15 * *", now) == datetime(2026, 11, 1, 18, 30)
        assert cron_next("0 0 1 1 *", now) == datetime(2027, 1, 1, 0, 0)
        assert cron_next("0 12 13 * 5", now) == datetime(2026, 10, 23, 12, 0)        # dom OR dow
        assert cron_next("0 0 * * 7", now) == datetime(2026, 10, 25, 0, 0)          # 7 is Sunday
        assert cron_next("5-10/5 2 * * *", now) == datetime(2026, 10, 22, 2, 5)
        assert cron_next("0 0 30 2 *", now) is None
        for bad in ("* * * *", "60 * * * *", "*/0 * * * *", "a * * * *", "5-1 * * * *"):
            try:
                cron_parse(bad)
                raise AssertionError(f"{bad!r} parsed")
            except ValueError:
                pass

        # parse: every form
        r, why = parse("/schedule every 30m fix the docs | check: python -c pass", now)
        assert r["kind"] == "schedule" and r["every"] == 1800 and why == ""
        assert r["said"] == "auto fix the docs | check: python -c pass"
        assert r["next"] == "2026-10-21T12:37:30" and r["state"] == "active" and r["runs"] == 0
        r, _ = parse("/schedule every 2h auto plan tidy the docs | check:  a  |  b", now)
        assert r["every"] == 7200 and r["said"] == "auto plan tidy the docs | check:  a  |  b"
        r, _ = parse("/schedule every day at 18:00 tidy", now)
        assert r["at"] == "18:00" and r["every"] is None and r["next"] == "2026-10-21T18:00:00"
        r, why = parse("schedule at 09:00 ship nightly", now)
        assert r["at"] == "09:00" and r["next"] == "2026-10-22T09:00:00" and why.startswith("noted")
        r, _ = parse('/schedule cron "0 9 * * 1-5" auto audit | check: python -c pass', now)
        assert r["cron"] == "0 9 * * 1-5" and r["next"] == "2026-10-22T09:00:00"
        r, _ = parse("/schedule cron */15 * * * * audit", now)
        assert r["cron"] == "*/15 * * * *" and r["said"] == "auto audit"
        r, _ = parse("/schedule once 2026-10-22T09:00 /drive run it", now)
        assert r["once"] == "2026-10-22T09:00:00" and r["said"] == "auto run it"
        g, _ = parse("/goal fix the map | check: python -c pass", now)
        assert g["kind"] == "goal" and g["every"] == GOAL_EVERY and g["next"] == "2026-10-21T12:07:30"
        assert g["budget"] == GOAL_BUDGET
        for bad in ("/goal fix the map", "/schedule every 30m ask fix it", "/schedule every 10s x",
                    "/schedule every fortnight x", "/schedule at 25:00 x", "/schedule once 2026-10-20T09:00 x",
                    '/schedule cron "0 0 30 2 *" x', "/schedule every 30m", "/drive x", "",
                    "/schedule every 30m x | check:", "/schedule sometimes x"):
            row, why = parse(bad, now)
            assert row is None and why, f"{bad!r} was taken"

        # no state/ folder: refused, nothing made
        bare = tmp / "bare"
        bare.mkdir()
        row, why = add(bare, g, now)
        assert row is None and "state/" in why and not (bare / "state").exists()
        assert due(bare, now) == [] and record(bare, "x", "passed", now) is None

        ground = tmp / "ground"
        (ground / "state").mkdir(parents=True)
        assert listing(ground) == "no schedules or goals"

        # add, due, lease, record
        s, _ = parse("/schedule every 30m fix | check: python -c pass", now)
        s, why = add(ground, s, now)
        assert s and not why
        assert due(ground, now) == []                                   # not yet
        later = now + timedelta(minutes=31)
        got = due(ground, later)
        assert [x["id"] for x in got] == [s["id"]] and got[0]["lease"] and got[0]["holder"]
        assert due(ground, later) == [], "a leased row was handed out twice"
        assert due(ground, later + timedelta(seconds=LEASE_SECONDS + 1)), "a dead lease never ran out"
        done = record(ground, s["id"], "failed", later + timedelta(minutes=2))
        assert done["runs"] == 1 and done["lease"] is None and done["state"] == "active"
        assert done["next"] == "2026-10-21T13:10:30" and done["verdicts"] == ["failed"]
        raw = _store(ground).read_bytes()
        assert raw.count(b"\r\n") == raw.count(b"\n") == len(_rows(ground))

        # a goal is done when its check passes
        g, _ = parse("/goal fix the map | check: python -c pass", now)
        g, _ = add(ground, g, now)
        assert [x["id"] for x in due(ground, now)] == [g["id"]]
        r = record(ground, g["id"], "failed", now)
        assert r["state"] == "active" and r["next"] == "2026-10-21T12:37:30"
        r = record(ground, g["id"], "passed", now + timedelta(minutes=30))
        assert r["state"] == "done" and r["next"] is None and r["runs"] == 2

        # ... blocked after three of the same failure, not after three different ones
        b, _ = add(ground, parse("/goal x | check: exit 1", now)[0], now)
        for v in ("failed", "error", "failed"):
            assert record(ground, b["id"], v, now)["state"] == "active"
        assert record(ground, b["id"], "failed", now)["state"] == "active"
        assert record(ground, b["id"], "failed", now)["state"] == "blocked"
        assert fold(ground)[b["id"]]["verdicts"] == ["failed", "error", "failed", "failed", "failed"]
        assert b["id"] not in [x["id"] for x in due(ground, now + timedelta(days=1))]

        # ... and when its budget is spent
        k, _ = add(ground, dict(parse("/goal y | check: exit 1", now)[0], budget=2), now)
        assert record(ground, k["id"], "failed", now)["state"] == "active"
        assert record(ground, k["id"], "error", now)["state"] == "blocked"

        # a once is done after its run
        o, _ = add(ground, parse("/schedule once 2026-10-21T13:00 run it", now)[0], now)
        assert [x["id"] for x in due(ground, datetime(2026, 10, 21, 13, 0))] == [o["id"]]
        assert record(ground, o["id"], "nothing", datetime(2026, 10, 21, 13, 1))["state"] == "done"

        # catch-up: five hours late is one run, then the next slot after now
        c, _ = add(ground, dict(parse("/schedule every 30m catch up", now)[0],
                                next="2026-10-21T07:00:00"), now)
        a, _ = add(ground, dict(parse("/schedule at 06:00 morning", now)[0],
                                next="2026-10-19T06:00:00"), now)
        late = [x["id"] for x in missed(ground, now)]
        assert c["id"] in late and a["id"] in late and s["id"] not in late
        got = [x["id"] for x in due(ground, now)]
        assert got.count(c["id"]) == 1 and got.count(a["id"]) == 1
        assert missed(ground, now) == [], "a leased row was reported missed"
        assert record(ground, c["id"], "passed", now)["next"] == "2026-10-21T12:37:30"
        assert record(ground, a["id"], "passed", now)["next"] == "2026-10-22T06:00:00"
        assert c["id"] not in [x["id"] for x in due(ground, now)]
        assert missed(ground, now) == []

        # drop, listing, a row cut short by a crash
        d, why = drop(ground, s["id"], now)
        assert d["state"] == "dropped" and not why and drop(ground, "nope", now)[0] is None
        assert s["id"] not in [x["id"] for x in due(ground, now + timedelta(days=1))]
        with open(_store(ground), "ab") as f:
            f.write(b'{"event": "record", "id": "zz')
        assert record(ground, a["id"], "failed", now)["runs"] == 2
        assert all(r.get("id") != "zz" for r in _rows(ground))
        text = listing(ground)
        assert g["id"] in text and "blocked" in text and "dropped" in text and "daily at 06:00" in text
        assert text.index("active") < text.index("blocked") < text.index("dropped")

        # a bad row is refused at the door of the store
        assert add(ground, dict(g, said="ask fix it"), now)[0] is None
        assert add(ground, dict(g, said="auto fix it"), now)[0] is None             # a goal, no check
        assert add(ground, dict(s, every=None), now)[0] is None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
