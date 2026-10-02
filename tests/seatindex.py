"""SEAT_LOG_INDEX.md -- every toll in SEAT_LOG.md, in the order it was paid, read off the log.

    python tests/seatindex.py            rewrites SEAT_LOG_INDEX.md
    python tests/seatindex.py --check    exit 1 if the index is stale

WHY (2026-10-01, his ruling of 2026-09-30, WHAT'S LEFT B13). SEAT_LOG.md is append-only (ESTATE LAW 8)
and is written by more than one hand, so its sitting numbers carry gaps and duplicates and its order
is the order of writing. He asked for it "sorted and numbered"; the log itself cannot be sorted
without rewriting it, which the law forbids. This is the index beside it, regenerated from the log so
it cannot drift, the way BUILDMAP.md is read off the code. The log is never touched.

THE GENERATOR LIVES IN manjuel/seatlog.py SINCE 2026-10-02 and runs at every toll (`seatlog.pay`), so
a sitting that pays a toll never leaves the index stale. This script is the hand's way to run it and
the check the suites hold, for a log written any other way. The names below are the stroke's.

SEAT_LOG.md is the record and is untracked (his ruling 2026-09-08); so is this index. Where the log is
absent -- a fresh checkout -- `--check` says so and passes: there is nothing to be stale.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from manjuel import seatlog  # noqa: E402

LOG = ROOT / seatlog.SEAT_LOG
OUT = ROOT / seatlog.SEAT_LOG_INDEX

tolls = seatlog.toll_rows
ordered = seatlog.ordered_tolls
arithmetic = seatlog.numbering
render = seatlog.index_text


def main() -> int:
    if not LOG.exists():
        print("no SEAT_LOG.md here (the record is untracked); nothing to index, nothing stale.")
        return 0
    text = LOG.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n")
    if "--check" in sys.argv:
        if not seatlog.index_is_current(ROOT):
            print("SEAT_LOG_INDEX.md is STALE (or absent): regenerate with `python tests/seatindex.py`")
            return 1
        print(f"SEAT_LOG_INDEX.md matches the log: {len(tolls(text))} tolls.")
        return 0
    seatlog.write_index(ROOT)
    rows = tolls(text)
    gaps, dups = arithmetic(rows)
    print(f"wrote SEAT_LOG_INDEX.md: {len(rows)} tolls, {len(gaps)} never tolled, {len(dups)} tolled more than once")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
