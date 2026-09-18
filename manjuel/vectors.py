"""Semantic index: chunked, incremental, passage-level retrieval.

Design notes that matter:

- CHUNKS, not documents. A whole-file vector is one average of everything the
  file says, which is why the first version needed a 4000-char cap and still
  retrieved poorly. Chunking removes the cap and returns the passage rather
  than just the filename.
- INCREMENTAL. Files are keyed by sha256; unchanged files are skipped. Without
  this, pointing at a large ground means re-embedding everything every run.
- READ-ONLY over source ground. Roots are read and never written. The index
  lives in manjuel's own ground (LAW 2: originals are read-only; packets
  prepare, the operator lands).
- BOUNDED (LAW 7). Caps on file size, file count, and chunks per file, so a
  stray root cannot run away.
- Vectors are stored L2-normalized, so cosine similarity is a plain dot
  product at query time.
- The embedder is stamped in `meta`. Vectors from two models are not
  comparable, so a model change invalidates the index and is refused rather
  than silently mixed.
"""

from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import struct
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import memory as _memory
from . import transcript as _transcript

SCHEMA_VERSION = "2"

# Bounds
MAX_FILE_BYTES = 256_000
MAX_FILES = 4000
MAX_CHUNKS_PER_FILE = 200
CHUNK_CHARS = 1200
CHUNK_OVERLAP = 200

TEXT_SUFFIXES = {".md", ".txt", ".us", ".py", ".json", ".jsonl", ".csv", ".rst", ".toml", ".yaml", ".yml", ".ini", ".cfg"}
# Keys are silent (LAW 9). `.env` happens to be skipped because it has no
# suffix, but `.yaml`, `.ini` and `.cfg` ARE indexed -- so a secrets file with
# one of those names would be embedded, and an embedding cannot be unpublished.
# Refused by NAME, explicitly, rather than left to a coincidence of extensions.
SECRET_NAMES = {".env", "env", "secrets", "secret", "credentials", "creds",
                "id_rsa", "id_ed25519", ".netrc", ".npmrc", ".pypirc",
                "keyfile", "apikey", "api_key", "token", "tokens"}


LOG_HORIZON_DAYS = 45


def _too_old_to_index(path) -> bool:
    """A transcript past the horizon is history, not a retrieval candidate.

    Set MANJUEL_LOG_HORIZON_DAYS=0 to index every transcript ever written.
    Nothing is deleted either way -- `sitting` and `when` read logs/ direct,
    by number and by date, and neither goes through the index.
    """
    import os as _os
    import time as _t
    from pathlib import Path as _P
    p = _P(path)
    parts = {x.lower() for x in p.parts}
    if "logs" not in parts:
        return False                      # standing documents never age out
    try:
        days = float(_os.environ.get("MANJUEL_LOG_HORIZON_DAYS",
                                     LOG_HORIZON_DAYS))
    except ValueError:
        days = LOG_HORIZON_DAYS
    if days <= 0:
        return False
    try:
        return (_t.time() - p.stat().st_mtime) > days * 86400
    except OSError:
        return False


def is_secret(path) -> bool:
    """Whether this file must never be embedded, whatever its extension."""
    from pathlib import Path as _P
    p = _P(path)
    name = p.name.lower()
    if name in SECRET_NAMES or name.startswith(".env"):
        return True
    stem = p.stem.lower()
    return stem in SECRET_NAMES or stem.endswith("_secrets") or stem.endswith("_key")


# CLIENT DATA — the operator's ruling, sitting 45: highest priority, never
# indexed, never used, never cross-referenced. Three tags, ANY one protects:
# a `vault` directory anywhere in the path; `.client.` anywhere in the name;
# a [[CLIENT]] token in the first bytes of the file. Refusal is HARD at
# every surface -- index, watcher, reads, listings, search -- so protected
# content can never reach a model, a transcript, the dialogue, or a recall.
CLIENT_TOKEN = "[[CLIENT]]"


def is_protected(path, peek: bool = True) -> bool:
    """Client-bearing by tag. Location, name, or content token."""
    from pathlib import Path as _P
    p = _P(path)
    if any(part.lower() == "vault" for part in p.parts):
        return True
    if ".client." in p.name.lower():
        return True
    if peek and p.is_file():
        try:
            with p.open("rb") as fh:
                head = fh.read(2048)
            if CLIENT_TOKEN.encode() in head:
                return True
        except OSError:
            pass
    return False


SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "blobs",
             "target", "dist", "build", ".mypy_cache", ".pytest_cache",
             # full prompts repeat the objective and feed once per stage;
             # indexing them floods retrieval with near-duplicate passages.
             "_prompts"}

try:                        # optional: exact same results, ~100x faster
    import numpy as _np
except Exception:
    _np = None


class IndexError_(Exception):
    pass


# THE LINE BETWEEN THE TWO CORPORA, in one place so nothing can draw it twice.
# logs/ is the transcripts; everything else is a source. index_roots.txt
# already draws this boundary in prose -- "what the chain IS", "what it is
# CONFIGURED as", "what it has DONE" -- and logs/ sits alone under the third.
def is_transcript(path) -> bool:
    """Is this indexed path a past run rather than a source?"""
    p = str(path).replace("\\", "/")
    return "/logs/" in p or p.startswith("logs/")


# THE APPEND-ONLY LEDGERS. Dated history that happens not to live under logs/.
# A CHANGELOG entry ABOUT the covenant is not the covenant, exactly as a
# transcript about it is not -- the ruling that split logs/ off drew the line
# in the right place and stopped one file short of the files that carry the
# same freight.
RECORD_FILES = frozenset({
    "CHANGELOG.md", "HANDOFF.md", "SEAT_LOG.md", "DAYBOOK.md",
    "TASKS.md", "REFUSALS.md", "memory.md", "BUILDMAP.md",
})


def is_record(path) -> bool:
    """Is this a ledger -- what HAPPENED -- rather than a source?

    MEASURED 2026-09-10, inside `sources` (transcripts already removed):

        code                908 chunks   36.0%
        THE LEDGERS         821 chunks   32.6%
        other docs          678 chunks   26.9%
        doctrine (sealed)   115 chunks    4.6%

    The record outweighed the doctrine SEVEN TO ONE, so a question about
    doctrine was answered from a corpus that is a third commentary and a
    twentieth scripture. `what does the covenant say` ranked TASKS.md first --
    on the chunk holding the task ABOUT that very failure -- and `what do the
    laws say` returned HANDOFF.md above SITTING_LAWS.md and ESTATE_LAWS.md.
    Asking the estate what its laws say handed back a status note about them.

    With these eight excluded the doctrine takes three of the top six on the
    first question and the three law files take 1-3 on the second. Nothing was
    weighted: the corpus was named correctly and the ranking followed.
    """
    p = str(path).replace("\\", "/")
    return p.rsplit("/", 1)[-1] in RECORD_FILES


# ---------------------------------------------------------------------
# chunking
# ---------------------------------------------------------------------


def chunk_text(text: str, size: int = CHUNK_CHARS, overlap: int = CHUNK_OVERLAP):
    """Split on blank lines, packing paragraphs up to `size` with overlap.

    Paragraph-aware so a chunk rarely cuts mid-sentence; the overlap keeps a
    passage that straddles a boundary retrievable from either side.
    """
    text = text.replace("\r\n", "\n")
    paras = [p for p in text.split("\n\n")]
    chunks: list[tuple[int, str]] = []
    buf, start = "", 0
    cursor = 0

    for p in paras:
        piece = p if not buf else buf + "\n\n" + p
        if len(piece) <= size or not buf:
            if not buf:
                start = cursor
            buf = piece
        else:
            chunks.append((start, buf))
            tail = buf[-overlap:] if overlap else ""
            start = cursor - len(tail)
            buf = (tail + "\n\n" + p) if tail else p
        cursor += len(p) + 2
        if len(chunks) >= MAX_CHUNKS_PER_FILE:
            break

    if buf.strip() and len(chunks) < MAX_CHUNKS_PER_FILE:
        chunks.append((start, buf))

    # A single paragraph longer than `size` is hard-split rather than dropped.
    out: list[tuple[int, str]] = []
    for st, c in chunks:
        if len(c) <= size * 2:
            out.append((st, c))
            continue
        for i in range(0, len(c), size):
            out.append((st + i, c[i:i + size]))
            if len(out) >= MAX_CHUNKS_PER_FILE:
                break
    return [(s, c.strip()) for s, c in out if c.strip()][:MAX_CHUNKS_PER_FILE]


# WHERE A PASSAGE SITS, CARRIED WITH IT (2026-09-17, his word: "chunk on
# structure and carry the heading path").
#
# A 1200-character window out of the middle of SPEC.md arrives with no idea
# that it is section 8.2, so the embedding is of the words alone and the hit
# cites "chunk 14 @ 18,400" -- a number nobody can navigate to. Naming the
# section in the chunk fixes both ends at once: the heading's words join the
# passage's in the vector, and the citation becomes somewhere a person can
# open.
#
# MARKDOWN ONLY, and that is not timidity. `windowed()` in skills.py learned
# this the hard way: a `#` in a .py file is a COMMENT, so treating one as a
# heading offered a module's docstring prose as navigable sections. Code is
# mapped by `ast`, where its real shape is -- never by this.
_MD_HEADING = re.compile(r"(?m)^(#{1,6})[ \t]+(.+?)[ \t]*$")


def heading_trail(text: str) -> list[tuple[int, int, str]]:
    """(offset, level, title) for every markdown heading, in file order."""
    return [(m.start(), len(m.group(1)), m.group(2).strip())
            for m in _MD_HEADING.finditer(text)]


def heading_path_at(trail: list, pos: int, depth: int = 3) -> str:
    """The headings in force at `pos`, outermost first: "8. THE PLAN > 8.2 ...".

    A deeper heading CLOSES the ones beneath it, which is what makes this a
    path and not a list of everything seen so far.
    """
    levels: dict[int, str] = {}
    for off, lvl, title in trail:
        if off > pos:
            break
        for deeper in [k for k in levels if k > lvl]:
            levels.pop(deeper)
        levels[lvl] = title
    return " > ".join(levels[k] for k in sorted(levels))[:180]


def _norm(vec: list[float]) -> list[float]:
    n = sum(x * x for x in vec) ** 0.5
    return [x / n for x in vec] if n else vec


def _pack(vec: list[float]) -> bytes:
    return struct.pack(f"<{len(vec)}f", *vec)


def _unpack(blob: bytes) -> tuple[float, ...]:
    return struct.unpack(f"<{len(blob) // 4}f", blob)


# ---------------------------------------------------------------------
# the index
# ---------------------------------------------------------------------


@dataclass
class IndexStats:
    scanned: int = 0
    embedded: int = 0
    skipped_unchanged: int = 0
    skipped_big: int = 0
    chunks: int = 0
    errors: list[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class VectorIndex:
    def __init__(self, db_path: Path, embed_model: str):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.embed_model = embed_model
        self.db = sqlite3.connect(str(self.path))
        self.db.execute("PRAGMA journal_mode=WAL")
        self._schema()
        self._check_schema()
        self._check_model()

    def _schema(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
            CREATE TABLE IF NOT EXISTS docs (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE NOT NULL,
                root TEXT NOT NULL,
                sha TEXT NOT NULL,
                chars INTEGER NOT NULL,
                indexed_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY,
                doc_id INTEGER NOT NULL REFERENCES docs(id) ON DELETE CASCADE,
                ord INTEGER NOT NULL,
                start INTEGER NOT NULL,
                text TEXT NOT NULL,
                vec BLOB NOT NULL,
                label TEXT DEFAULT '',
                stamp TEXT DEFAULT '',
                session TEXT DEFAULT ''
            );
            CREATE INDEX IF NOT EXISTS chunks_doc ON chunks(doc_id);
            """
        )
        # EXACT SEARCH BESIDE MEANING (2026-09-17, his word: "hybrid
        # retrieval"). An embedding is a poor way to find `_INDEX_BUSY`,
        # `tagSend` or `MANJUEL_GIT_REMOTE`: the vector of an identifier is the
        # vector of the words around it, so the one passage that DEFINES a name
        # ranks beside every passage that mentions the subject. BM25 finds the
        # token itself. Neither is better; they fail differently, which is why
        # every serious retrieval stack runs both and fuses the ranks.
        #
        # FTS5 SHIPS WITH PYTHON'S OWN SQLITE -- no dependency (LAW 6, RULE 4),
        # no second process, no second file: the same vectors.db carries it.
        #
        # `content='chunks'` makes it DERIVED, which is the estate's own rule
        # for everything that is not the record: it holds no text of its own and
        # is rebuilt from the chunks table in one statement. Nothing to keep in
        # step by hand, and nothing that can drift.
        #
        # `tokenchars '_'` KEEPS AN IDENTIFIER WHOLE. Without it unicode61
        # splits on the underscore, `_INDEX_BUSY` becomes `index` + `busy`, and
        # the exact half of a hybrid search stops being exact about the one
        # thing it is for.
        try:
            self.db.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5("
                "text, content='chunks', content_rowid='id', "
                "tokenize=\"unicode61 tokenchars '_'\")")
            self.fts = True
        except sqlite3.OperationalError:
            # A python built without FTS5 keeps the whole index working and
            # loses only the exact half. Named on the answer, never silent.
            self.fts = False
        self.db.commit()

    def _check_schema(self) -> None:
        row = self.db.execute("SELECT value FROM meta WHERE key='schema'").fetchone()
        if row is None:
            self.db.execute("INSERT INTO meta(key,value) VALUES('schema',?)", (SCHEMA_VERSION,))
            self.db.commit()
        elif row[0] != SCHEMA_VERSION:
            # The index is derived state, never a record -- it is rebuilt from
            # the ground rather than migrated.
            self.db.executescript(
                "DROP TABLE IF EXISTS chunks_fts; "
                "DROP TABLE IF EXISTS chunks; DROP TABLE IF EXISTS docs; DELETE FROM meta;"
            )
            self.db.commit()
            self._schema()
            self.db.execute("INSERT INTO meta(key,value) VALUES('schema',?)", (SCHEMA_VERSION,))
            self.db.commit()

    def _check_model(self) -> None:
        cur = self.db.execute("SELECT value FROM meta WHERE key='embed_model'")
        row = cur.fetchone()
        if row is None:
            self.db.execute(
                "INSERT INTO meta(key,value) VALUES('embed_model',?)", (self.embed_model,)
            )
            self.db.commit()
        elif row[0] != self.embed_model:
            raise IndexError_(
                f"index at {self.path.name} was built with '{row[0]}' but the "
                f"configured embedder is '{self.embed_model}'. Vectors from "
                f"different models are not comparable. Rebuild with "
                f"index_ground <rebuild> or restore the old tag."
            )

    # ---- the exact half ----------------------------------------------

    def _refresh_fts(self) -> None:
        """Re-derive the whole keyword index from the chunks table.

        ONE STATEMENT, and it is the reason this is external-content rather
        than a table with triggers: `rebuild` reads the chunks as they stand,
        so the keyword half can never hold a passage the vector half does not,
        and there is no insert path to forget. It costs no embedding and no
        model -- on this estate's corpus it is milliseconds, which is why it is
        simply run after every build rather than tracked.
        """
        if not getattr(self, "fts", False):
            return
        try:
            self.db.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
            n = self.db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
            self.db.execute("INSERT OR REPLACE INTO meta(key,value) "
                            "VALUES('fts_built',?)", (str(n),))
            self.db.commit()
        except sqlite3.DatabaseError:
            self.fts = False

    def _fts_ready(self) -> bool:
        """True when the keyword index holds what the chunks hold.

        AN INDEX BUILT BEFORE THIS EXISTED IS UPGRADED WITHOUT RE-EMBEDDING.
        The chunk TEXT is already stored; the keyword half is derived from it,
        so an old vectors.db gains exact search the first time it is searched,
        with no rebuild, no GPU and nothing for the operator to run.

        ASKED OF `meta`, NOT OF THE TABLE, and that distinction cost a red
        stroke to find: an external-content FTS5 table answers `COUNT(*)` from
        the CONTENT table, so an empty keyword index reports the chunk count
        and looks full. The marker records how many chunks the last refresh
        covered; a missing or stale one rebuilds.
        """
        if not getattr(self, "fts", False):
            return False
        try:
            want = self.db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
            row = self.db.execute(
                "SELECT value FROM meta WHERE key='fts_built'").fetchone()
        except sqlite3.DatabaseError:
            self.fts = False
            return False
        if want and (row is None or row[0] != str(want)):
            self._refresh_fts()
        return bool(getattr(self, "fts", False))

    def _fts_hits(self, qtext: str) -> dict:
        """{chunk id: bm25 rank position} for the query's own words.

        THE QUERY IS SANITISED INTO TOKENS, never passed through. FTS5's MATCH
        takes an expression language -- quotes, `NEAR`, `*`, `^`, a bare `-` --
        and an operator's sentence is not one. A raw question mark or an
        unbalanced quote raises, and a search that raises on ordinary English
        is worse than no exact half at all. Words out, OR between them: the
        ranking decides which matter, which is what BM25 is for.
        """
        toks = [t for t in re.findall(r"[A-Za-z0-9_]+", qtext or "") if len(t) > 1]
        if not toks or not self._fts_ready():
            return {}
        expr = " OR ".join('"' + t.replace('"', '') + '"' for t in toks[:24])
        try:
            rows = self.db.execute(
                "SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH ? "
                "ORDER BY bm25(chunks_fts) LIMIT 200", (expr,)).fetchall()
        except sqlite3.DatabaseError:
            return {}
        return {r[0]: i for i, r in enumerate(rows)}

    # ---- building ---------------------------------------------------

    def _iter_files(self, roots: list[Path]):
        # THE LOG HORIZON. logs/ grows by a file per run forever, and an
        # index that keeps every transcript ever written slowly buries the
        # ground's own documents under old chatter -- a two-month-old run
        # about a bug that no longer exists competing with the doctrine.
        # Only TRANSCRIPTS age out: everything else in the ground is a
        # standing document and stays indexed however old it is. The
        # transcripts themselves are never deleted; they simply stop being
        # retrieval candidates, and `sitting` and `when` still read them
        # directly, by number and by date.
        seen = 0
        for root in roots:
            if not root.exists():
                continue
            if root.is_file():
                if (root.suffix.lower() in TEXT_SUFFIXES
                        and not is_secret(root) and not is_protected(root)):
                    seen += 1
                    yield root.parent, root
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
                for fn in sorted(filenames):
                    p = Path(dirpath) / fn
                    if is_secret(p) or is_protected(p):
                        continue
                    if p.suffix.lower() not in TEXT_SUFFIXES:
                        continue
                    if _too_old_to_index(p):
                        continue
                    seen += 1
                    if seen > MAX_FILES:
                        return
                    yield root, p

    def build(self, roots: list[Path], embed_fn, report=lambda s: None,
              declared: bool = True) -> IndexStats:
        st = IndexStats()
        for root, p in self._iter_files(roots):
            st.scanned += 1
            try:
                size = p.stat().st_size
                if size > MAX_FILE_BYTES:
                    st.skipped_big += 1
                    continue
                raw = p.read_bytes()
            except Exception as exc:
                st.errors.append(f"{p.name}: {exc}")
                continue

            sha = hashlib.sha256(raw).hexdigest()
            key = str(p.resolve())

            cur = self.db.execute("SELECT id, sha FROM docs WHERE path=?", (key,))
            row = cur.fetchone()
            if row and row[1] == sha:
                st.skipped_unchanged += 1
                continue

            try:
                text = raw.decode("utf-8", errors="replace")
            except Exception as exc:
                st.errors.append(f"{p.name}: {exc}")
                continue
            if not text.strip():
                continue

            # A RUN TRANSCRIPT IS INDEXED BY ITS DELIVERY (his ruling
            # 2026-09-10). transcript.index_text returns "" for anything that
            # is not a run -- a standup report, a parity run -- and those fall
            # through to whole-file chunking below, because both are already
            # summaries and dropping them would be a silent loss.
            trimmed = ""
            if p.suffix.lower() == ".md":
                try:
                    trimmed = _transcript.index_text(text)
                except Exception:
                    trimmed = ""

            if trimmed:
                pieces = [(st, tx, "delivery", "", "")
                          for st, tx in chunk_text(trimmed)]
            elif p.name == _memory.MEMORY_FILE:
                # One chunk per remembered entry, carrying its stamp and the
                # session that produced it, instead of one growing blob.
                pieces = [(st, tx, lb, sp, ss)
                          for st, tx, lb, sp, ss in _memory.split_entries(text)]
            elif p.suffix.lower() == ".md":
                # THE SECTION TRAVELS WITH THE PASSAGE. Its words are part of
                # what gets embedded -- a passage under "8.2 the versions
                # ahead" should answer a question about the versions ahead even
                # when it never repeats the phrase -- and the same string lands
                # in `label`, which is what the result line already prints.
                trail = heading_trail(text)
                pieces = []
                for off, tx in chunk_text(text):
                    where = heading_path_at(trail, off)
                    body = f"[{p.name} > {where}]\n{tx}" if where else tx
                    pieces.append((off, body, where, "", ""))
            else:
                pieces = [(st, tx, "", "", "") for st, tx in chunk_text(text)]
            if not pieces:
                continue

            vecs = []
            try:
                for piece in pieces:
                    vecs.append(_norm(embed_fn(piece[1])))
            except Exception as exc:
                st.errors.append(f"{p.name}: embed failed ({exc})")
                continue

            if row:
                self.db.execute("DELETE FROM chunks WHERE doc_id=?", (row[0],))
                self.db.execute(
                    "UPDATE docs SET sha=?,chars=?,indexed_at=?,root=? WHERE id=?",
                    (sha, len(text), _now(), str(root), row[0]),
                )
                doc_id = row[0]
            else:
                cur = self.db.execute(
                    "INSERT INTO docs(path,root,sha,chars,indexed_at) VALUES(?,?,?,?,?)",
                    (key, str(root), sha, len(text), _now()),
                )
                doc_id = cur.lastrowid

            self.db.executemany(
                "INSERT INTO chunks(doc_id,ord,start,text,vec,label,stamp,session)"
                " VALUES(?,?,?,?,?,?,?,?)",
                [
                    (doc_id, i, pieces[i][0], pieces[i][1], _pack(vecs[i]),
                     pieces[i][2], pieces[i][3], pieces[i][4])
                    for i in range(len(pieces))
                ],
            )
            self.db.commit()
            st.embedded += 1
            st.chunks += len(pieces)
            report(f"    + {p.name} ({len(pieces)} chunks)")

        # ONLY A DECLARED SCOPE MAKES AN ORPHAN (2026-09-15). This handed
        # prune() the `roots` of every build, and two callers build from a
        # handful of CHANGED FILES rather than from index_roots.txt: the
        # watcher's drain (cli._apply_ground_changes) and embed_text. Against
        # those, every other document was "under a root no longer declared".
        # On the live index (1,290 documents on 2026-09-15) that share is
        # always over the ceiling, so the eviction was refused -- silently,
        # neither caller passes a report -- after resolving every indexed
        # path, on every turn a file had changed. On a small index, where the
        # changed files were three quarters of it or more, the rest was evicted
        # for real. A caller whose roots are not the index's scope says so, and
        # the prune asks only question 1: is the file gone?
        self.prune(report, roots=roots if declared else None)
        # The keyword half is DERIVED from the chunks, so it is re-derived
        # whenever they move -- after the prune, so it never holds a passage
        # belonging to a document that has just been evicted.
        if st.embedded or st.chunks:
            self._refresh_fts()
        return st

    # A refresh may evict this share of the corpus and no more. Above it the
    # prune REFUSES and reports, because a number that large is far more
    # likely to be a typo in index_roots.txt than a deliberate narrowing --
    # and the operator finding out via a thin search result days later is
    # the failure mode this bound exists to prevent.
    ORPHAN_CEILING = 0.25

    def prune(self, report=lambda s: None, roots: list[Path] | None = None) -> int:
        """Drop docs the index should no longer be holding.

        TWO QUESTIONS, and until 2026-09-03 it could only ask the first:

            1. is the file gone?              (the filesystem knows)
            2. is its root still declared?    (index_roots.txt knows)

        The second was the hole. Sitting 78: `worlds/manjuel` was removed
        from index_roots.txt and 91 of 801 documents from that world STAYED
        IN THE CORPUS and kept answering, because every one of their files
        still existed on disk. The door was shut and the room was still
        full. Only a full rebuild cleared it, and nothing said so.

        MATCH ON THE PATH, NOT THE STORED `root` STRING. A root can be
        renamed, narrowed (`worlds/manjuel` -> `worlds/manjuel/codex`) or
        re-cased; the stored label then compares equal for documents that
        are genuinely out of scope, and unequal for ones that are not. The
        path is the fact.

        GATED, and this is the operator's ruling of 2026-09-03 (option c of
        three). Root-awareness makes a REFRESH destructive in a way it has
        never been: a typo in index_roots.txt would silently evict that
        root's documents on the very next run. So an eviction larger than
        ORPHAN_CEILING of the corpus is REFUSED and reported instead --
        the shape of a guard that will not perform a suspiciously large
        action on the say-so of a config file. `rebuild` still clears
        everything; that path DROPs the tables and is explicit.

        `roots=None` keeps the old behaviour exactly -- missing files only.
        A caller that cannot say what is in scope must not be taken to mean
        that nothing is.
        """
        rows = list(self.db.execute("SELECT id, path FROM docs"))
        total = len(rows)

        missing = [(i, p) for i, p in rows if not Path(p).exists()]

        orphans: list[tuple] = []
        if roots:
            live = []
            for r in roots:
                try:
                    live.append(Path(r).resolve())
                except OSError:
                    continue
            known = {i for i, _ in missing}
            for i, p in rows:
                if i in known:
                    continue
                try:
                    rp = Path(p).resolve()
                except OSError:
                    continue
                if not any(rp == root or root in rp.parents for root in live):
                    orphans.append((i, p))

        if orphans and total and (len(orphans) / total) > self.ORPHAN_CEILING:
            report(f"    ! {len(orphans)} of {total} docs are under a root no "
                   f"longer declared -- more than "
                   f"{int(self.ORPHAN_CEILING * 100)}% of the corpus.")
            report("      REFUSED as too large for a refresh. Check "
                   "index_roots.txt; run `index_ground rebuild` if it is right.")
            orphans = []

        for i, pth in missing:
            self.db.execute("DELETE FROM chunks WHERE doc_id=?", (i,))
            self.db.execute("DELETE FROM docs WHERE id=?", (i,))
            report(f"    - {Path(pth).name} (missing)")
        for i, pth in orphans:
            self.db.execute("DELETE FROM chunks WHERE doc_id=?", (i,))
            self.db.execute("DELETE FROM docs WHERE id=?", (i,))
            report(f"    - {Path(pth).name} (root no longer declared)")

        if missing or orphans:
            self.db.commit()
            self._refresh_fts()
        return len(missing) + len(orphans)

    # ---- searching --------------------------------------------------

    def search(self, qvec: list[float], limit: int = 5, per_doc: int = 2,
               scope: str = "all", qtext: str = ""):
        """Rank the index. `qtext` is the query's own WORDS: given, the keyword
        half runs beside the vector half and the two rankings are fused (see
        below). Omitted, this behaves exactly as it always has.

        `scope` picks the corpus (his ruling 2026-09-10):

            sources      WHAT IS -- the doctrine, the law, the code, the
                         seats, the specs. Neither transcripts nor ledgers.
            record       WHAT HAPPENED -- transcripts AND the append-only
                         ledgers (CHANGELOG, HANDOFF, SEAT_LOG, DAYBOOK,
                         TASKS, REFUSALS, memory, BUILDMAP)
            transcripts  logs/ only: what was SAID on a past run
            ledgers      the eight ledgers only
            all          everything, kept for callers that mean it

        WHY THIS EXISTS. Measured 2026-09-10: 812 of 996 indexed documents and
        4,060 of 6,705 ranked passages were old runs, and "what does the
        covenant say" returned eight transcripts and never the covenant. Each
        answer is written back to logs/ and indexed, so the estate was
        answering from its own echo and laundering an error into the record.
        A weight was refused in favour of a split -- a cosine penalty is a
        number nobody can defend and would still return transcripts for a
        question about doctrine, just fewer of them.
        """
        q = _norm(qvec)
        rows = self.db.execute(
            "SELECT c.id, c.doc_id, c.ord, c.start, c.text, c.vec, d.path, "
            "c.label, c.stamp, c.session "
            "FROM chunks c JOIN docs d ON d.id = c.doc_id"
        ).fetchall()

        # SOURCES ARE WHAT IS; THE RECORD IS WHAT HAPPENED. The 2026-09-10
        # ruling split logs/ off for that reason and the ledgers belong on the
        # same side of it -- see is_record for the measurement that showed
        # them outweighing the doctrine seven to one.
        if scope == "sources":
            rows = [r for r in rows
                    if not is_transcript(r[6]) and not is_record(r[6])]
        elif scope == "record":
            rows = [r for r in rows if is_transcript(r[6]) or is_record(r[6])]
        elif scope == "transcripts":
            rows = [r for r in rows if is_transcript(r[6])]
        elif scope == "ledgers":
            rows = [r for r in rows if is_record(r[6])]

        usable = [r for r in rows if len(r[5]) // 4 == len(q)]
        if not usable:
            return []

        if _np is not None:
            mat = _np.frombuffer(b"".join(r[5] for r in usable), dtype="<f4")
            mat = mat.reshape(len(usable), len(q))
            sims = mat @ _np.asarray(q, dtype="<f4")
            cos = [float(sims[i]) for i in range(len(usable))]
        else:
            cos = [sum(a * b for a, b in zip(q, _unpack(r[5]))) for r in usable]

        items = [
            {"cid": r[0], "score": cos[i], "path": r[6], "ord": r[2],
             "start": r[3], "text": r[4], "label": r[7], "stamp": r[8],
             "session": r[9], "found": "meaning"}
            for i, r in enumerate(usable)
        ]
        items.sort(key=lambda d: d["score"], reverse=True)

        # HYBRID: TWO RANKINGS, FUSED BY RANK AND NOT BY SCORE (2026-09-17).
        #
        # A cosine and a BM25 number are not on one scale and never will be --
        # adding them, or weighting one against the other, is a constant nobody
        # can defend, which is the same objection that refused a recency weight
        # here in favour of a corpus split. RECIPROCAL RANK FUSION needs no
        # such constant: each list contributes 1/(k+rank), so a passage both
        # halves rank highly wins, a passage only ONE half can see still
        # surfaces, and k=60 -- the published default -- flattens the top so
        # neither retriever dominates the other's certainties.
        #
        # THE EXACT HALF ONLY ADDS. A query whose words appear nowhere returns
        # no keyword hits and the order is exactly the cosine order it has
        # always been, which is why this cannot make an existing search worse.
        fts = self._fts_hits(qtext) if qtext else {}
        if fts:
            K = 60.0
            by_id = {d["cid"]: d for d in items}
            # WHAT "THE VECTOR HALF FOUND IT" MEANS. Cosine scores every chunk
            # in the corpus, so "it has a score" says nothing -- the honest
            # test is whether it ranked where a caller would ever have seen it.
            reach = {d["cid"] for d in items[:max(20, limit * 4)]}
            fused = {d["cid"]: 1.0 / (K + i) for i, d in enumerate(items)}
            for cid, i in fts.items():
                if cid not in by_id:
                    continue            # out of this scope: not a candidate
                fused[cid] = fused.get(cid, 0.0) + 1.0 / (K + i)
                by_id[cid]["found"] = "both" if cid in reach else "exact"
            items.sort(key=lambda d: fused.get(d["cid"], 0.0), reverse=True)

        out, per, seen = [], {}, set()

        def take(d) -> bool:
            if d["cid"] in seen or per.get(d["path"], 0) >= per_doc:
                return False
            seen.add(d["cid"])
            per[d["path"]] = per.get(d["path"], 0) + 1
            out.append(d)
            return True

        for d in items:
            if len(out) >= limit:
                break
            take(d)

        # AND THE EXACT HALF KEEPS A SEAT AT THE TABLE.
        #
        # MEASURED 2026-09-17, on a corpus built to look like this one. A query
        # that names an identifier AND two ordinary words -- which is how a
        # person actually asks -- gives the ordinary words a vote in BOTH
        # rankings and the identifier a vote in one. Fusion then puts a passage
        # both halves quite like above the single passage that carries the
        # name, and the one line the operator asked for is not in the answer at
        # all. The keyword half had it at rank 1; the fusion lost it.
        #
        # So the ORDER stays the fusion's, and the PRESENCE of the best keyword
        # hits is guaranteed: up to two of them displace the weakest fused
        # entries. A slot is a count, not a weight -- there is no constant here
        # for anyone to argue about, and nothing is reordered to flatter it.
        if fts and len(out) >= limit:
            best = [c for c, _ in sorted(fts.items(), key=lambda kv: kv[1])][:2]
            for cid in [c for c in best if c in by_id and c not in seen]:
                dropped = out.pop()
                seen.discard(dropped["cid"])
                per[dropped["path"]] = max(0, per.get(dropped["path"], 1) - 1)
                take(by_id[cid])

        return [{k: v for k, v in d.items() if k != "cid"} for d in out]

    def stats(self) -> dict:
        d = self.db.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
        c = self.db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        roots = [r[0] for r in self.db.execute("SELECT DISTINCT root FROM docs")]
        return {"docs": d, "chunks": c, "roots": roots, "model": self.embed_model}

    def close(self) -> None:
        self.db.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_roots(config: Path, default: list[Path], base: Path | None = None) -> list[Path]:
    """Roots come from a plain text file, one path per line. Keeps the ground
    list editable without touching code, same as agents/ and skills/.

    Relative entries resolve against `base` (manjuel's own ground), NOT the
    process working directory -- otherwise the same config would index
    different files depending on where the REPL was launched from.
    """
    if not config.exists():
        return list(default)
    base = base or config.parent
    roots = []
    for line in config.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = Path(os.path.expandvars(os.path.expanduser(line)))
        roots.append(p if p.is_absolute() else (base / p))
    return roots or list(default)
