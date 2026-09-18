"""The ground watches itself.

Sitting 41: the operator installed watchdog. Before this, an edit to a seat,
a skill, or a document sat invisible until a manual /reload or /index -- the
chain's knowledge of its own ground went stale the moment the operator
touched a file. Now the ground reports its own changes, and the CLI applies
them at TURN BOUNDARIES: never mid-answer, always audibly.

watchdog is OPTIONAL. Absent, everything here degrades to no-ops and the
CLI behaves exactly as before -- a missing convenience is never a refusal.

Two kinds of change matter, and they are handled differently:

  DECLARATIONS  agents/*.md, skills/*.md, pipelines.md, commands.md,
                providers of behavior -> queue a reload.
  MATERIAL      indexable files under a root index_roots.txt declares -> queue
                an incremental re-embed, so semantic_search stops lying about
                fresh edits. A file the index is not told to hold is not
                material, however it is edited.

Secrets are refused by name here too -- a .env touched is a .env IGNORED.
"""

from __future__ import annotations

import importlib.util
import threading
from pathlib import Path

from .vectors import SKIP_DIRS, TEXT_SUFFIXES, is_protected, is_secret

_DECLARATION_DIRS = {"agents", "skills"}
_DECLARATION_FILES = {"pipelines.md", "commands.md", "agents.md"}
_IGNORE_PARTS = {".git", "__pycache__", "index", "_prompts", "bin",
                 ".venv", "node_modules",
                 # THE CHAIN'S OWN WRITES (the REPL read, 2026-09-08). The
                 # ledger and the thread are written at every open, turn,
                 # toll and close; with `sessions` watched, every turn
                 # queued thread.jsonl and the NEXT turn re-embedded the
                 # whole rolling conversation ("reindexed on change:
                 # thread.jsonl", every turn). logs/ was already excused
                 # for the same reason; sessions/ is the same hand.
                 "sessions"}
# Files the chain writes into the ground's root and tests/, for the same
# reason: touched by the record, not by the operator's hand.
_SELF_WRITTEN = {"SEAT_LOG.md", "memory.md", "rack.md",
                 "last_run.json", "last_run.md", "run_history.jsonl",
                 "parity_history.jsonl", "last_audit.md"}


def available() -> bool:
    try:
        return importlib.util.find_spec("watchdog") is not None
    except (ImportError, ValueError):
        return False


class GroundWatch:
    """Collects change events; the CLI drains them between turns.

    The handler logic is plain methods so the suite can drive it without a
    real observer thread; the observer is only wired when watchdog exists.
    """

    def __init__(self, ground: Path, roots=None):
        self.ground = Path(ground).resolve()
        self._lock = threading.Lock()
        self._reload_needed = False
        self._changed: set[Path] = set()
        self._observer = None
        # WHAT THE INDEX IS TOLD TO HOLD (2026-09-15). The doors hand in
        # index_roots.txt as index_ground reads it (skills.index_roots), once,
        # when the sitting opens: the standing's shape -- a list edited
        # mid-sitting is read at the next launch. Until then this queued any
        # text file under the ground the lists above did not excuse, and the
        # next turn embedded it into the live index, declared or not. On
        # 2026-09-15 that index held 12
        # documents under no root, and no version of index_roots.txt in git
        # ever declared one: flows/ (10), state/rack_ledger.jsonl, and
        # law/chain.jsonl -- the ledger index_roots.txt keeps out by listing
        # the laws "Five FILES, not the folder".
        #
        # None keeps the old reach, every indexable file under the ground, for
        # a caller that cannot say what the index holds.
        self._roots: list[Path] | None = None
        if roots is not None:
            self._roots = []
            for r in roots:
                try:
                    self._roots.append(Path(r).resolve())
                except OSError:
                    continue

    # ---- classification (pure; unit-tested directly) -----------------

    def held(self, p: Path) -> bool:
        """Would index_ground take this file? Its roots, walked its way.

        A file root is held when it IS the file. A folder root holds what is
        under it, except below a folder the indexer's own walk skips
        (vectors.SKIP_DIRS, and any dot-folder) -- so a build/ or .cache/ under
        manjuel/ is not material here either."""
        if self._roots is None:
            return True
        for root in self._roots:
            if p == root:
                return True
            if root in p.parents:
                below = p.relative_to(root).parts[:-1]
                if not any(d in SKIP_DIRS or d.startswith(".") for d in below):
                    return True
        return False

    def note(self, path) -> None:
        """One changed path, classified. Called by the observer thread."""
        try:
            p = Path(path).resolve()
        except OSError:
            return
        if self.ground not in p.parents:
            return                        # outside the ground: not ours
        rel = p.relative_to(self.ground)
        if any(part in _IGNORE_PARTS for part in rel.parts):
            return
        if rel.name in _SELF_WRITTEN:
            return                        # the record's own hand
        if is_secret(p.name):
            return                        # a secret: touched is ignored
        declaration = ((rel.parts[0] in _DECLARATION_DIRS and p.suffix == ".md")
                       or rel.name in _DECLARATION_FILES)
        # logs are indexed too, but they change every turn by our own hand --
        # indexing them stays with /index, not the watcher.
        material = (p.suffix.lower() in TEXT_SUFFIXES and rel.parts[0] != "logs"
                    and self.held(p))
        if not (declaration or material):
            # NOTHING HERE WOULD ACT ON IT, SO NOTHING IS OPENED. is_protected
            # reads a file's first 2 KB for the client token, and it was asked
            # of every event under the ground -- the door's and the glass's
            # logs under atlas/ among them, as they write.
            return
        if is_protected(p):
            return                        # client data: touched is ignored
        with self._lock:
            if declaration:
                self._reload_needed = True
            if material:
                self._changed.add(p)

    # ---- draining (called by the CLI at turn boundaries) -------------

    def drain(self) -> tuple[bool, list[Path]]:
        """(reload_needed, changed_files) -- and the slate is wiped."""
        with self._lock:
            reload_needed = self._reload_needed
            changed = sorted(self._changed)
            self._reload_needed = False
            self._changed.clear()
        return reload_needed, changed

    # ---- the real observer (only when watchdog exists) ----------------

    def start(self) -> bool:
        if not available():
            return False
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer

        watch = self

        class H(FileSystemEventHandler):
            def on_modified(self, event):
                if not event.is_directory:
                    watch.note(event.src_path)

            def on_created(self, event):
                if not event.is_directory:
                    watch.note(event.src_path)

            def on_moved(self, event):
                if not event.is_directory:
                    watch.note(event.dest_path)

        self._observer = Observer(timeout=2)
        self._observer.schedule(H(), str(self.ground), recursive=True)
        self._observer.daemon = True
        self._observer.start()
        return True

    def stop(self) -> None:
        if self._observer is not None:
            try:
                self._observer.stop()
            except Exception:
                pass
            self._observer = None
