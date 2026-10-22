"""His laws and rulings as notes his second brain indexes (F, 2026-10-22).

His words: "we can tie in the notes system to be able to diff or parse whatever ive
ruled before, and integrate that into the workflows for steward ... I will NEVER lose
any information again!"

Every law in law/ and every RULE in CLAUDE.md becomes one note in his notes, tagged
`ruling`, with a stable id, so his second brain's index can hand Steward the rulings that
bear on a job instead of the whole law being re-read every turn. `sync` writes them
through his notes kernel (the MCP server `notes`): a new ruling is created, a changed one
updated, an unchanged one left alone -- so a re-sync is safe.

THE CHAIN STAYS THE AUTHORITY. A note here is how a law is FOUND, never what makes it law:
the sealed chain (law/chain.jsonl) and the gates in code still decide, and a search that
misses a ruling never means the ruling does not apply. Every note says so on its last line.

stdlib only, Python 3.10.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# (file, the name a law in it is cited by)
SOURCES = (
    ("law/ESTATE_LAWS.md", "ESTATE LAW"),
    ("law/SITTING_LAWS.md", "SITTING LAW"),
    ("law/SITTING_LAWS_2.md", "SITTING LAW"),
    ("law/LAW_LEDGER.md", "LEDGER"),
    ("law/LAW_001_FOUNDING.md", "LAW 001"),
    ("law/LAW_002_THE_TWELVE.md", "LAW 002"),
    ("law/LAW_003_THE_LOOP.md", "LAW 003"),
    ("CLAUDE.md", "RULE"),
)
TAG = "ruling"
CATEGORY = "areas"
_HEAD = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
_ITEM = re.compile(r"^(\d+)\.\s+\*\*([^*]+)")     # a bold title may wrap onto the next line
_MIN_CHARS = 60
# The notes kernel's own rule for a note's id (kernel._ID_RE): an id it refuses is a ruling
# never stored, so every id is held to it here.
ID_RULE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
ID_MAX = 64
FOOT = ("Source: {src} -- the sealed chain (law/chain.jsonl) and the gates in code are the "
        "authority; this note is how the ruling is found.")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def _sections(text: str) -> list:
    """[(heading, level, lines)] for every ## or ### heading, in order."""
    out, head, level, lines = [], "", 0, []
    for line in text.splitlines():
        m = _HEAD.match(line)
        if m:
            if head:
                out.append((head, level, lines))
            head, level, lines = m.group(2), len(m.group(1)), []
        elif head:
            lines.append(line)
    if head:
        out.append((head, level, lines))
    return out


def units(ground) -> list:
    """Every ruling as {id, title, body, tags, source}: one per numbered law under a
    heading, else one per section; the ledger's copies of CLAUDE.md's rules are left to
    CLAUDE.md itself, so nothing is held twice."""
    ground = Path(ground)
    out, seen = [], set()
    for rel, cited in SOURCES:
        path = ground / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
        stem = Path(rel).stem.lower().replace("_", "-")
        for head, level, lines in _sections(text):
            if rel.endswith("LAW_LEDGER.md") and level == 3 and head.upper().startswith("RULE "):
                continue
            items, cur = [], None
            for line in lines:
                m = _ITEM.match(line)
                if m:
                    cur = [m.group(1), m.group(2), [line]]
                    items.append(cur)
                elif cur is not None:
                    cur[2].append(line)
            pieces = ([(f"{n}", f"{cited} {n}: {bold.strip()}", body) for n, bold, body in items] if items
                      else [("", head, lines)])
            for key, title, body_lines in pieces:
                body = "\n".join(body_lines).strip()
                if len(body) < _MIN_CHARS:
                    continue
                uid = ("ruling-" + _slug(f"{stem}-{key or head}"))[:ID_MAX].rstrip("-")
                if uid in seen:
                    tail = f"-{len(seen)}"
                    uid = uid[:ID_MAX - len(tail)].rstrip("-") + tail
                seen.add(uid)
                if not key and rel == "CLAUDE.md":
                    title = head
                out.append({"id": uid, "title": title[:160], "source": rel,
                            "body": f"{body}\n\n{FOOT.format(src=rel)}",
                            "tags": [TAG, stem]})
    return out


def sync(ground, server) -> dict:
    """Write every ruling into his notes through `server` (an open mcp_stdio.StdioServer on
    the notes kernel): created, updated, unchanged and failed, counted."""
    counts = {"created": 0, "updated": 0, "same": 0, "failed": []}
    for u in units(ground):
        try:
            have = server.call("notes_get", {"id": u["id"]})
            note = None
            if have and not have.startswith("Refused"):
                try:
                    note = json.loads(have)
                except ValueError:
                    note = None
            if not note:
                said = server.call("notes_create", {"id": u["id"], "title": u["title"], "body": u["body"],
                                                    "tags": u["tags"], "category": CATEGORY})
                if str(said or "").startswith("Refused"):
                    raise ValueError(said)
                counts["created"] += 1
            elif str(note.get("body") or "").strip() != u["body"].strip() or note.get("title") != u["title"]:
                said = server.call("notes_update", {"id": u["id"], "title": u["title"], "body": u["body"],
                                                    "tags": u["tags"]})
                if str(said or "").startswith("Refused"):
                    raise ValueError(said)
                counts["updated"] += 1
            else:
                counts["same"] += 1
        except Exception as exc:
            counts["failed"].append(f"{u['id']}: {type(exc).__name__}: {exc}"[:200])
    return counts


def _strokes() -> None:
    """On the real law files: many rulings, unique ids, the ones he cites by name found,
    the ledger's copies of CLAUDE.md left out, and every note naming the chain."""
    ground = Path(__file__).resolve().parent.parent
    got = units(ground)
    ids = [u["id"] for u in got]
    assert len(got) >= 25, len(got)
    assert len(ids) == len(set(ids)), "ids are unique"
    bad = [i for i in ids if not ID_RULE.match(i)]
    assert not bad, f"every id is one the notes kernel accepts: {bad[:3]}"
    titles = " | ".join(u["title"] for u in got)
    assert "SITTING LAW 5" in titles and "ESTATE LAW 9" in titles, titles[:400]
    assert sum(1 for u in got if u["source"] == "law/SITTING_LAWS.md" and u["title"].startswith("SITTING LAW")) >= 4, \
        "a law whose bold title wraps is still its own ruling"
    assert any(u["source"] == "CLAUDE.md" and u["title"].startswith("RULE 12") for u in got)
    assert not any(u["source"].endswith("LAW_LEDGER.md") and u["title"].upper().startswith("RULE ")
                   for u in got), "the ledger's copies are left to CLAUDE.md"
    assert all(u["body"].endswith(FOOT.format(src=u["source"])) and TAG in u["tags"] for u in got)

    class Fake:
        def __init__(self):
            self.notes, self.calls = {}, []

        def call(self, tool, args):
            self.calls.append(tool)
            if tool == "notes_get":
                n = self.notes.get(args["id"])
                return json.dumps(n) if n else "Refused: notes_get failed: no such note"
            if tool == "notes_create":
                if not ID_RULE.match(args["id"]):          # the kernel's own refusal
                    return "Refused: notes_create failed: bad id"
                self.notes[args["id"]] = dict(args)
            if tool == "notes_update":
                self.notes[args["id"]].update(args)
            return "{}"
    fake = Fake()
    first = sync(ground, fake)
    again = sync(ground, fake)
    assert first["created"] == len(got) and not first["failed"], first
    assert again["same"] == len(got) and again["created"] == again["updated"] == 0, again
    print(f"rulings strokes: {len(got)} rulings, created then left alone -- all held")


if __name__ == "__main__":
    _strokes()
