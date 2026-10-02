"""Memory: append-only, per-entry, tied to the session that produced it.

Three files, and the split is the point:

  memory.md            the LANDED record. Append-only (LAW 1). Indexed.
  memory/pending.jsonl entries a seat PROPOSED. Staged, not remembered.
  memory/chain.jsonl   the SEALS: one link per landing, on the law's own pen,
                       each holding the hash and the place of what it sealed.

A model calling `remember` stages; it does not land. The operator lands, and
is shown the entry before it goes in (LAW 6: the gate is final; "packets
prepare, the operator lands"). That keeps model testimony out of the record
unless a person put it there, without losing the proposal.

Entries carry their session and the run that produced them, so memory chunks
per entry rather than as one growing blob, and a retrieved line can be traced
back to the sitting it came from.

THE CHAIN (2026-10-02, WHAT'S LEFT H1; his word: "an autonomous second brain
with hash chain verification"). memory.md was append-only by custom, and the
law's own ledger was the one record on this ground that was chained. `land`
is the one place a landing is written (ESTATE LAW 8: one write-path per
chain), so it is the one place a link is laid. The pen is law/pen/links.py,
loaded read-only and never imitated; a link's whole document is one line,
"LAND by operator -> memory.md range:A-B sha256:H", the hash of the exact
bytes that landing appended and where they sit. No word of the memory rides
on the chain, so it can sit beside a record that is not tracked. `verify`
walks the pen's own check over the chain and then memory.md's bytes against
every seal in order: each byte belongs to exactly one link, so a changed
byte is named by the link it sits in, a cut file by the link it no longer
reaches, and a write that did not come through `land` by the bytes no link
has sealed.

WHAT THE CHAIN DOES NOT SAY. It does not say a person wrote a byte that was
there before the chain, or that arrived without a landing: those are sealed
as ADOPT by `memory`, a different verb and a different actor inside the hash,
so the chain says plainly that no one vouched for them and only watches them
from then on. It cannot tell a deleted chain from one never begun.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

MEMORY_FILE = "memory.md"
PENDING_FILE = Path("memory") / "pending.jsonl"
CHAIN_FILE = Path("memory") / "chain.jsonl"

LANDER = "operator"   # who lands: a person's act, always (LAW 6)
FINDER = "memory"     # who found bytes no landing wrote: no person vouches for them
_PEN_PATH = Path(__file__).resolve().parent.parent / "law" / "pen" / "links.py"

# The whole of a link's document: no words ride on this chain.
_ANCHOR_RE = re.compile(
    r"^(LAND|ADOPT) by ([A-Za-z0-9_-]+) -> memory\.md range:(\d+)-(\d+) sha256:([0-9a-f]{64})$")

GENERATED = "GENERATED"   # model testimony
OPERATOR = "OPERATOR"     # the operator's own word

# THE KIND (2026-09-07, the operator: "we can parse through the memories and
# sort them later on ... guidance decision ruling learning, etc."). One word
# on each entry, set by the operator at landing, so memory can be sorted by
# what it IS. `note` when he does not say.
KINDS = ("guidance", "decision", "ruling", "learning", "outcome", "note")
DEFAULT_KIND = "note"

HEADER = (
    "# Memory\n\n"
    "Append-only. One entry per sitting-worth of thought, newest at the bottom.\n"
    "Entries stamped GENERATED are model testimony and are not fact until the\n"
    "record proves them. Entries stamped OPERATOR are the operator's own word.\n"
)

# "## <iso stamp> - <title>"  (the separator may be an em dash or a hyphen)
_ENTRY_RE = re.compile(
    r"^##[ \t]+(?P<stamp>\d{4}-\d{2}-\d{2}T[0-9:+\-Z.]+)[ \t]*[—-][ \t]*(?P<title>.*?)[ \t]*$",
    re.MULTILINE,
)


def new_session_id(ts: float | None = None) -> str:
    dt = datetime.fromtimestamp(ts) if ts else datetime.now()
    return "S" + dt.strftime("%Y%m%d-%H%M%S")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Entry:
    title: str
    body: str
    provenance: str = GENERATED
    session: str = ""
    run: str = ""
    stamp: str = ""
    kind: str = DEFAULT_KIND

    def __post_init__(self):
        if not self.stamp:
            self.stamp = _now()
        if not self.title:
            self.title = " ".join(self.body.split()[:8]) or "untitled"
        self.kind = (self.kind or DEFAULT_KIND).strip().lower() or DEFAULT_KIND

    def render(self) -> str:
        lines = [f"\n## {self.stamp} — {self.title}", f"- provenance: {self.provenance}",
                 f"- kind: {self.kind}"]
        if self.session:
            lines.append(f"- session: {self.session}")
        if self.run:
            lines.append(f"- run: {self.run}")
        lines += ["", self.body.strip(), ""]
        return "\n".join(lines)

    def preview(self) -> str:
        head = f"  {self.stamp}  [{self.provenance}]  kind: {self.kind}"
        if self.session:
            head += f"  session {self.session}"
        body = self.body.strip()
        if len(body) > 500:
            body = body[:500] + " ..."
        return f"{head}\n  title: {self.title}\n\n" + "\n".join(
            "    " + l for l in body.splitlines()
        )


# ---------------------------------------------------------------------
# landing
# ---------------------------------------------------------------------


def land(ground: Path, entry: Entry) -> Path:
    """Append one entry to memory.md and seal it on the chain beside it. Never
    rewrites what is already there.

    THE LANDING IS NEVER BLOCKED BY ITS CHAIN. The entry is the operator's act
    and it is written. If the chain cannot be opened or written, this says so
    on stderr and `verify` stays red until the chain catches up (`adopt`): a
    seal that failed in silence would be the worst of the three outcomes."""
    ground = Path(ground)
    mem = ground / MEMORY_FILE
    if not mem.exists():
        mem.write_text(HEADER, encoding="utf-8", newline="\r\n")
    chain = None
    try:
        chain = _open_chain(ground)
        found = _adopt(chain, mem)
        if found and found[0] > 0:
            _say(f"memory.md held {found[1] - found[0]} bytes (from byte {found[0]}) that no "
                 f"landing wrote. They are sealed as ADOPTED, by `memory`, and the chain says so.")
    except Exception as exc:
        chain = None
        _say(f"the memory chain could not be opened ({type(exc).__name__}: {exc}). The entry "
             f"is landed; the chain is behind it, and verify says so until `adopt` catches it up.")
    start = mem.stat().st_size
    with mem.open("a", encoding="utf-8", newline="\r\n") as f:
        f.write(entry.render())
    if chain is not None:
        try:
            _seal(chain, mem, "LAND", LANDER, start, mem.stat().st_size, f"LAND:{entry.kind[:40]}")
        except Exception as exc:
            _say(f"the entry is landed but its seal could not be written "
                 f"({type(exc).__name__}: {exc}). Verify is red until `adopt` catches the chain up.")
    return mem


# ---------------------------------------------------------------------
# the chain
# ---------------------------------------------------------------------


def _say(text: str) -> None:
    """To stderr, looked up at the call: a landing that could not seal is said
    where the operator sees it, never swallowed."""
    print(f"  ({text})", file=sys.stderr)


_PEN = None


def _pen():
    """The proven pen, loaded read-only from the repository this code sits in
    (law.py and the law gate load it the same way). Never edited, never
    imitated: a chain format of our own would be a second one to verify."""
    global _PEN
    if _PEN is None:
        spec = importlib.util.spec_from_file_location("manjuel_memory_pen", str(_PEN_PATH))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _PEN = mod
    return _PEN


def _open_chain(ground: Path):
    return _pen().Chain(str(Path(ground) / CHAIN_FILE))


@dataclass
class Seal:
    n: int           # the link's number on the chain
    verb: str        # LAND: a person's landing. ADOPT: bytes found, vouched for by no one.
    actor: str
    start: int       # where the sealed bytes begin in memory.md
    end: int         # and where they end
    sha: str         # the sha256 of exactly those bytes


def _seals(chain) -> tuple[list[Seal], list[str]]:
    """(the seals, the faults in how links are written). A link whose document
    is not the one anchor line, or whose actor is not the name in it, is a
    fault: this chain carries seals and nothing else."""
    seals: list[Seal] = []
    bad: list[str] = []
    for e in chain.entries("link"):
        n = e["payload"].get("n", "?")
        m = _ANCHOR_RE.match(str(e["payload"].get("doc", "")).strip())
        if not m:
            bad.append(f"link #{n} is not a seal of memory.md (no canonical anchor line)")
        elif e.get("actor") != m.group(2):
            bad.append(f"link #{n} names {m.group(2)!r} in its anchor and {e.get('actor')!r} as its actor")
        else:
            seals.append(Seal(n, m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5)))
    return seals, bad


def _seal(chain, mem: Path, verb: str, actor: str, start: int, end: int, says: str) -> None:
    sha = hashlib.sha256(mem.read_bytes()[start:end]).hexdigest()
    chain.deposit(f"{verb} by {actor} -> {MEMORY_FILE} range:{start}-{end} sha256:{sha}",
                  _pen().OPEN, says, actor)


def _adopt(chain, mem: Path) -> tuple[int, int] | None:
    """Seal whatever memory.md holds past the chain's last seal, as ADOPT by
    `memory`. (start, end), or None when there is nothing past it."""
    seals, _bad = _seals(chain)
    covered = seals[-1].end if seals else 0
    size = mem.stat().st_size
    if size <= covered:
        return None
    _seal(chain, mem, "ADOPT", FINDER, covered, size, "ADOPT:found")
    return covered, size


def adopt(ground: Path) -> int:
    """Seal what memory.md holds that no link has sealed, as ADOPT by `memory`:
    a memory that predates its chain, or bytes a write put there that did not
    come through `land`. Returns the bytes adopted. This is how a chain
    begins, and how a lagging one catches up; it is never a landing, and the
    chain says so (the verb, and the actor `memory`, are in the hash)."""
    ground = Path(ground)
    mem = ground / MEMORY_FILE
    if not mem.is_file():
        return 0
    found = _adopt(_open_chain(ground), mem)
    return found[1] - found[0] if found else 0


@dataclass
class ChainState:
    ok: bool | None      # True: whole. False: broken, and `detail` names where. None: nothing to verify.
    detail: str
    links: int = 0
    head: str = ""
    strays: int = 0      # regions adopted AFTER the chain began: bytes that did not come through land

    def say(self) -> str:
        if self.ok is None:
            return self.detail
        if not self.ok:
            return f"BROKEN: {self.detail}"
        stray = (f", {self.strays} stray region{'' if self.strays == 1 else 's'} adopted"
                 if self.strays else "")
        return f"whole ({self.links} link{'' if self.links == 1 else 's'}{stray}, head {self.head[:12]})"


def verify(ground: Path) -> ChainState:
    """Walk the chain and memory.md against it. Reads only; writes nothing.

    Two walks: the pen's own over the chain (every hash, every weld), and
    memory.md's bytes against every seal in order. Every byte of memory.md
    belongs to exactly one link, so a changed byte is named by the link it sits
    in, a cut file by the link it no longer reaches, and bytes written without
    a landing by the count no link has sealed."""
    ground = Path(ground)
    mem, path = ground / MEMORY_FILE, ground / CHAIN_FILE
    try:
        if not mem.is_file():
            return ChainState(None, "no memory.md yet")
        if not path.is_file() or path.stat().st_size == 0:
            return ChainState(None, f"memory.md ({mem.stat().st_size} bytes) has never been "
                                    f"sealed; the first landing starts its chain")
        chain = _open_chain(ground)
        problems: list[str] = []
        ok, _n, detail = chain.verify()
        if not ok:
            problems.append(f"the pen's walk: {detail}")
        seals, bad = _seals(chain)
        problems += bad
        data = mem.read_bytes()
        pos = 0
        for s in seals:
            if s.start != pos:
                problems.append(f"link #{s.n}: bytes {s.start}-{s.end} do not meet the link before "
                                f"it, which ended at {pos}")
            if s.end <= s.start:
                problems.append(f"link #{s.n} seals no bytes ({s.start}-{s.end})")
            elif s.end > len(data):
                problems.append(f"link #{s.n} sealed bytes {s.start}-{s.end}, and memory.md is "
                                f"only {len(data)} bytes: it was cut")
            elif hashlib.sha256(data[s.start:s.end]).hexdigest() != s.sha:
                problems.append(f"link #{s.n} ({s.verb}, bytes {s.start}-{s.end}) MISMATCH: "
                                f"those bytes of memory.md were changed")
            pos = s.end
        if len(data) > pos:
            problems.append(f"memory.md holds {len(data) - pos} bytes (from byte {pos}) that no "
                            f"link has sealed: a write that did not come through land")
        strays = sum(1 for s in seals if s.verb == "ADOPT" and s.start > 0)
        return ChainState(not problems, "; ".join(problems) or "whole", len(seals), chain.head(), strays)
    except Exception as exc:                 # a chain that cannot be walked is not a whole one
        return ChainState(False, f"could not be walked: {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------
# staging
# ---------------------------------------------------------------------


def stage(ground: Path, entry: Entry) -> int:
    p = Path(ground) / PENDING_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\r\n") as f:
        f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
    return len(pending(ground))


def _read_pending(ground: Path) -> tuple[list[Entry], list[str]]:
    """(the proposals, the lines that could not be read), each in file order.

    A LINE THAT CANNOT BE READ IS KEPT, NOT SWALLOWED (2026-09-29). `pending`
    skipped one in silence, and `_write_pending` then rewrote the file from
    what HAD parsed -- so the first land or drop after a damaged line
    destroyed it, and a proposal a seat had staged was gone without a word
    in any record."""
    p = Path(ground) / PENDING_FILE
    if not p.exists():
        return [], []
    out: list[Entry] = []
    lost: list[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(Entry(**json.loads(line)))
        except Exception:
            lost.append(line)
    return out, lost


def pending(ground: Path) -> list[Entry]:
    return _read_pending(ground)[0]


def unread_pending(ground: Path) -> int:
    """How many lines of the pending file could not be read as a proposal.
    They are kept where they are; the operator is told the count."""
    return len(_read_pending(ground)[1])


def _write_pending(ground: Path, entries: list[Entry]) -> None:
    p = Path(ground) / PENDING_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    # What could not be read goes back as it was, after what could.
    lost = _read_pending(ground)[1]
    p.write_text(
        "".join(json.dumps(asdict(e), ensure_ascii=False) + "\n" for e in entries)
        + "".join(line + "\n" for line in lost),
        encoding="utf-8", newline="\r\n",
    )


def land_pending(ground: Path, index: int, countersign: bool = True,
                 kind: str = "") -> Entry | None:
    """Move one staged entry into memory.md. The operator's act, so the entry
    records that a person landed model testimony rather than silently
    promoting it to the operator's own word. `kind`, if given, is his word
    for what the entry is."""
    items = pending(ground)
    if not (0 <= index < len(items)):
        return None
    e = items.pop(index)
    if countersign:
        e.provenance = f"{GENERATED} (landed by OPERATOR)"
    if kind:
        e.kind = kind
    land(ground, e)
    _write_pending(ground, items)
    return e


def drop_pending(ground: Path, index: int) -> Entry | None:
    items = pending(ground)
    if not (0 <= index < len(items)):
        return None
    e = items.pop(index)
    _write_pending(ground, items)
    return e


# ---------------------------------------------------------------------
# reading back — per-entry chunking for the index
# ---------------------------------------------------------------------


def split_entries(text: str):
    """Split memory.md into one piece per entry.

    Returns (start_offset, text, label, stamp, session). Falls back to a single
    piece when the file has no entry headings, so a hand-written memory file
    still indexes rather than being skipped.
    """
    marks = list(_ENTRY_RE.finditer(text))
    if not marks:
        body = text.strip()
        return [(0, body, "", "", "")] if body else []

    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        block = text[m.start():end].strip()
        if not block:
            continue
        sess = re.search(r"^-[ \t]*session:[ \t]*(\S+)", block, re.MULTILINE)
        out.append(
            (
                m.start(),
                block,
                m.group("title").strip(),
                m.group("stamp").strip(),
                sess.group(1) if sess else "",
            )
        )
    return out
