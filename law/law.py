#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE LAW COURT TOOL - the chained ledger of the amendable constitution.

    python law.py direct  <law.md> --note "..."     sovereign law (operator)
    python law.py seal    <law.md> --note "..."     seal an appendable law as far
                                                    as it is written (operator)
    python law.py counsel <writer> <law.md> --note  counsel (steward|neiro|jesster)
    python law.py rule    <law.md> [--cites HASH] --note   the court rules
    python law.py refuse  <law.md> [--cites HASH] --why  record a refusal
    python law.py verify                             walk the whole chain
    python law.py status                             head, count, library
    python law.py --describe                         what it is
    python law.py --prove                            hermetic proof, exit 0

Governance (LAW_001 section 2): counsel flows from steward, neiro, jesster;
manjuel weighs counsel and writes rulings; the operator is sovereign.
Neiro is the judge of broken law - the warden; his findings ride as counsel.

The chain is appended ONLY through this tool, ONLY by links, on the Jesster
line's proven pen (links.py, loaded READ-ONLY from the pen folder - never
edited). Every link points at a standard .md law file in law/ and
carries its sha256 fingerprint. Laws are files; the ledger binds them;
nothing else may touch either. Standard library only. Nothing leaves this
machine.

AN APPENDABLE LAW (2026-09-21, the operator's word: "an appendable ledger
that the hand can continue to iterate on as directed, that we can chain or
seal when we would like"). `seal` binds a file's FIRST N BYTES, not the
whole file: the anchor carries `bytes:N`. The file may grow below byte N;
a changed byte above it, or a cut into it, is a MISMATCH like any other.
law/LAW_LEDGER.md is sealed this way. `direct` on it would bind the whole
file, and the first entry appended after would break the chain.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile

HOME = os.path.dirname(os.path.abspath(__file__))
COVENANT = "65118a147dd49ed9"
# Flat since 2026-09-04 (operator's ruling; SITTING LAW 4). The library and
# the chain both live in law/ itself. The two links sealed before that day
# carry the old "Archive/law/" pointer in their hashed text, so the anchor
# regex accepts both forms and only the bare form is ever written again.
LIBRARY = HOME
CHAIN_DIR = HOME
PEN_PATH = os.path.join(HOME, "pen", "links.py")
COUNSEL = ("steward", "neiro", "jesster")

# A law name is a BARE basename ending in .md. No separators, no drives,
# no whitespace - a link binds one file inside the library, nothing else.
LAW_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+\.md$")
# The canonical pointer line every link's doc MUST open with. The optional
# ` bytes:N` (group 5) is a seal over the first N bytes; without it the link
# binds the whole file, which is every link laid before 2026-09-21.
ANCHOR_RE = re.compile(
    r"^(COUNSEL|RULING|DIRECT|REFUSED) by ([A-Za-z0-9_-]+) -> "
    r"(?:Archive/law/|law/)([A-Za-z0-9._-]+\.md) sha256:([0-9a-f]{64})"
    r"(?: bytes:([1-9][0-9]*))?$")
# The pointer token a link doc must carry exactly once (either form).
POINTER_RE = re.compile(r"-> (?:Archive/law/|law/)")

DESCRIBE = ("THE LAW COURT TOOL - the amendable constitution as a link "
            "chain: counsel (steward/neiro/jesster) -> rulings (manjuel) -> "
            "direct law (operator). Links only, pointing at fingerprinted "
            ".md laws in law/, on the proven Jesster pen. An appendable law "
            "is sealed as far as it is written (seal), and grows below it.")


def _pen():
    """The proven pen, loaded read-only. Never edited, never imitated."""
    spec = importlib.util.spec_from_file_location("law_pen_links", PEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fingerprint(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _prefix_fingerprint(path, nbytes):
    """The fingerprint of a file's first `nbytes`, or None when the file is
    shorter than that -- a seal over bytes that are gone cannot hold."""
    h = hashlib.sha256()
    left = nbytes
    with open(path, "rb") as f:
        while left:
            chunk = f.read(min(65536, left))
            if not chunk:
                return None
            h.update(chunk)
            left -= len(chunk)
    return h.hexdigest()


def link_matches(path, token, nbytes=None):
    """Does the file still hold what its link bound? No bytes: -- every
    byte of it. bytes:N -- its first N bytes; it may have grown below them.
    Read by cmd_verify and by the engine's law gate, so the two walks
    cannot disagree about what a seal means."""
    if nbytes is None:
        return _fingerprint(path) == token
    return _prefix_fingerprint(path, int(nbytes)) == token


def _law_path(name):
    if not LAW_NAME_RE.match(name or ""):
        raise SystemExit("refused: a law name is a bare basename ending in "
                         ".md (got %r)" % (name,))
    p = os.path.join(LIBRARY, name)
    if not os.path.isfile(p):
        raise SystemExit("no such law file: law/%s" % name)
    return p


def _append(kind, writer, law_name, note, cites, prefix=False):
    mod = _pen()
    os.makedirs(CHAIN_DIR, exist_ok=True)
    chain = mod.Chain(os.path.join(CHAIN_DIR, mod.CHAIN_NAME))
    p = _law_path(law_name)
    extent = ""
    if prefix:
        # The length now, and the fingerprint of exactly that many bytes:
        # a write racing the seal lands below it, never inside it.
        size = os.path.getsize(p)
        if not size:
            raise SystemExit("law/%s is empty; there is nothing to seal"
                             % law_name)
        fp = _prefix_fingerprint(p, size)
        if fp is None:
            raise SystemExit("law/%s shrank while it was being sealed"
                             % law_name)
        extent = " bytes:%d" % size
    else:
        fp = _fingerprint(p)
    text = ("%s by %s -> law/%s sha256:%s%s\n%s"
            % (kind, writer, law_name, fp, extent, note))
    entry = chain.deposit(text, mod.OPEN, "%s:%s" % (kind, writer), writer,
                          cites=cites)
    return entry


def _load_chain():
    """(entries, malformed_line_count). One corrupt line never crashes the
    walk; it becomes a named problem instead."""
    path = os.path.join(CHAIN_DIR, _pen().CHAIN_NAME)
    entries = []
    bad = 0
    if not os.path.isfile(path):
        return entries, bad
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except ValueError:
                bad += 1
    return entries, bad


def _head_hash():
    entries, _ = _load_chain()
    return entries[-1]["hash"] if entries else None


def _cite_hash(argv):
    """A citation is a hash: 64 hex (a link), 40 (a git commit), or 16
    (the covenant). The pen refuses anything else; so do we, earlier."""
    v = _flag(argv, "--cites")
    if v is None:
        return []
    if len(v) not in (64, 40, 16) or any(
            c not in "0123456789abcdefABCDEF" for c in v):
        raise SystemExit("--cites takes a hash: 64 hex link, 40 git, "
                         "16 covenant")
    return [v]


def cmd_counsel(argv):
    writer, name = argv[0], argv[1]
    if writer not in COUNSEL:
        raise SystemExit("counsel belongs to steward, neiro, jesster")
    note = _flag(argv, "--note") or ""
    e = _append("COUNSEL", writer, name, note, [])
    _print(e, "counsel laid")


def cmd_rule(argv):
    name = argv[0]
    cites = _cite_hash(argv) or (
        [_head_hash()] if _head_hash() else [COVENANT])
    note = _flag(argv, "--note") or ""
    e = _append("RULING", "manjuel", name, note, cites)
    _print(e, "the court has ruled")


def cmd_direct(argv):
    name = argv[0]
    note = _flag(argv, "--note") or ""
    e = _append("DIRECT", "operator", name, note, [COVENANT])
    _print(e, "sovereign law laid")


def cmd_seal(argv):
    """Seal an APPENDABLE law as far as it is written: a DIRECT link by the
    operator whose anchor carries bytes:N. Below byte N the file may grow;
    above it nothing may change. Sealing again later lays a new link over
    the longer prefix, and every earlier seal still holds its part."""
    name = argv[0]
    note = _flag(argv, "--note") or ""
    e = _append("DIRECT", "operator", name, note, [COVENANT], prefix=True)
    m = ANCHOR_RE.match(e["payload"]["doc"].splitlines()[0])
    _print(e, "law/%s sealed to byte %s" % (name, m.group(5)))


def cmd_refuse(argv):
    name = argv[0]
    cites = _cite_hash(argv) or (
        [_head_hash()] if _head_hash() else [COVENANT])
    why = _flag(argv, "--why") or ""
    e = _append("REFUSED", "manjuel", name, why, cites)
    _print(e, "refusal recorded; it has no force")


def _print(e, what):
    print("%s: link #%d  head %s"
          % (what, e["payload"]["n"], e["hash"][:16]))


def cmd_verify(argv):
    """Three walks: malformed lines, the pen's own integrity walk (prev
    continuity + hash recomputation, wraps included), then the law walk
    (genesis cites the covenant; every link opens with the canonical anchor
    and its fingerprint matches the file on disk -- the whole file, or its
    first N bytes when the anchor carries bytes:N). Note text cannot forge
    an audit: only the ANCHOR LINE names the law, and extra citation tokens
    anywhere in the doc are refused outright."""
    mod = _pen()
    entries, bad = _load_chain()
    links = [e for e in entries if e.get("kind") == "link"]
    if not links:
        raise SystemExit("the chain is empty; nothing to verify")
    problems = []
    if bad:
        problems.append("%d malformed chain line(s)" % bad)
    chain = mod.Chain(os.path.join(CHAIN_DIR, mod.CHAIN_NAME))
    ok, _n, detail = chain.verify()
    if not ok:
        problems.append("pen walk: %s" % detail)
    first = links[0]
    if COVENANT not in [c.lower() for c in first["payload"].get("cites", [])]:
        problems.append("genesis does not cite the covenant")
    for e in links:
        doc = e["payload"].get("doc", "")
        n = e["payload"]["n"]
        ptrs = len(POINTER_RE.findall(doc))
        if ptrs != 1 or doc.count("sha256:") != 1:
            problems.append("link #%d carries %d/%d citation tokens "
                            "(exactly one of each required)"
                            % (n, ptrs, doc.count("sha256:")))
            continue
        first_line = doc.splitlines()[0].strip() if doc else ""
        m = ANCHOR_RE.match(first_line)
        if not m:
            problems.append("link #%d does not open with the canonical "
                            "anchor line" % n)
            continue
        name, token, extent = m.group(3), m.group(4), m.group(5)
        p = os.path.join(LIBRARY, name)
        if not os.path.isfile(p):
            problems.append("link #%d points at a missing law: %s"
                            % (n, name))
        elif not link_matches(p, token, extent):
            problems.append("link #%d fingerprint MISMATCH: %s"
                            % (n, name))
    if problems:
        print("THE CHAIN REFUSES:")
        for p in problems:
            print("  - %s" % p)
        return 1
    print("the law chain proves whole: %d links, head %s"
          % (len(links), entries[-1]["hash"][:16]))
    return 0


def seals():
    """{law name: the furthest byte any link seals it to}, for the laws
    sealed by prefix. A law bound whole is not listed; it has no extent."""
    out = {}
    for e in _load_chain()[0]:
        if e.get("kind") != "link":
            continue
        doc = e["payload"].get("doc", "")
        m = ANCHOR_RE.match(doc.splitlines()[0].strip() if doc else "")
        if m and m.group(5):
            out[m.group(3)] = max(out.get(m.group(3), 0), int(m.group(5)))
    return out


def cmd_status(argv):
    entries, bad = _load_chain()
    links = [e for e in entries if e.get("kind") == "link"]
    print("law chain: %d links%s" % (len(links),
                                     " (%d malformed lines!)" % bad if bad
                                     else ""))
    if entries:
        print("head: %s" % entries[-1]["hash"])
    if os.path.isdir(LIBRARY):
        extent = seals()
        for n in sorted(os.listdir(LIBRARY)):
            if n.endswith(".md"):
                p = os.path.join(LIBRARY, n)
                line = "  %-28s %s" % (n, _fingerprint(p)[:16])
                if n in extent:
                    line += "  sealed to byte %d of %d" % (
                        extent[n], os.path.getsize(p))
                print(line)


def _arg_unused():  # kept off the hot path; CLI reads flags directly
    pass


def _flag(argv, name):
    if name in argv:
        i = argv.index(name)
        if i + 1 >= len(argv):
            raise SystemExit("flag %s needs a value" % name)
        return argv[i + 1]
    return None


def prove():
    """Hermetic: temp library, temp chain, the real pen read-only.
    Seventeen strokes: the reviewer's three attacks, and the appendable
    law's seal (2026-09-21)."""
    tmp = tempfile.mkdtemp(prefix="law_prove_")
    lib = os.path.join(tmp, "law")
    os.makedirs(lib)
    global LIBRARY, CHAIN_DIR
    keep = (LIBRARY, CHAIN_DIR)
    LIBRARY, CHAIN_DIR = lib, lib
    try:
        strokes = []

        def ok(name, cond):
            strokes.append((name, bool(cond)))

        la = os.path.join(lib, "LAW_T_A.md")
        lb = os.path.join(lib, "LAW_T_B.md")
        decoy = os.path.join(lib, "LAW_T_DECOY.md")
        with open(la, "w", encoding="utf-8") as f:
            f.write("# LAW T-A\ntrial law a\n")
        with open(lb, "w", encoding="utf-8") as f:
            f.write("# LAW T-B\ntrial law b\n")
        with open(decoy, "w", encoding="utf-8") as f:
            f.write("# LAW T-DECOY\nthe decoy is honest but irrelevant\n")

        cmd_direct(["LAW_T_A.md", "--note", "genesis of the trial"])
        genesis = _load_chain()[0][0]["hash"]
        cmd_counsel(["neiro", "LAW_T_B.md", "--note", "warden finds drift"])
        counsel_hash = _load_chain()[0][1]["hash"]
        cmd_rule(["LAW_T_B.md", "--cites", counsel_hash,
                  "--note", "so it is written"])
        entries, _ = _load_chain()
        ok("three links laid", len(entries) == 3)
        ok("actors kept apart",
           entries[0]["actor"] == "operator"
           and entries[1]["actor"] == "neiro"
           and entries[2]["actor"] == "manjuel")
        ok("genesis prev is GENESIS", entries[0]["prev"] == "0" * 64)
        ok("ruling cites counsel by hash",
           entries[2]["payload"].get("cites") == [counsel_hash])
        ok("verify green", cmd_verify([]) == 0)

        # ATTACK 1 - note-text spoof: a hand-forged link whose NOTE carries
        # a perfect decoy pointer must be refused (anchor line missing).
        mod = _pen()
        d_fp = _fingerprint(decoy)
        forged_doc = ("cf. -> law/LAW_T_DECOY.md sha256:%s\n"
                      "an innocent-looking note" % d_fp)
        payload = {"n": 4, "says": "RULING:manjuel", "mode": "open",
                   "doc": forged_doc, "cites": [entries[-1]["hash"]]}
        body = {"ts": "2026-08-24T00:00:00+0000", "kind": "link",
                "payload": payload, "prev": entries[-1]["hash"],
                "actor": "manjuel"}
        forged = dict(body)
        forged["hash"] = mod._entry_hash(entries[-1]["hash"], body)
        with open(os.path.join(CHAIN_DIR, mod.CHAIN_NAME), "a",
                  encoding="utf-8") as f:
            f.write(json.dumps(forged, ensure_ascii=False) + "\n")
        ok("forged decoy-pointer link refused", cmd_verify([]) == 1)

        # restore: drop the forged line before the next strokes
        path = os.path.join(CHAIN_DIR, mod.CHAIN_NAME)
        lines = open(path, encoding="utf-8").read().splitlines()[:-1]
        open(path, "w", encoding="utf-8").write(
            "".join(l + "\n" for l in lines))

        # ATTACK 2 - containment: a law name outside the library is refused
        escaped = False
        try:
            _law_path("..\\evil.md")
        except SystemExit:
            escaped = True
        ok("outside-library names refused at deposit", escaped)

        # ATTACK 3 - tamper: flip a byte in a bound law; the walk refuses
        with open(la, "a", encoding="utf-8") as f:
            f.write("one lying byte\n")
        ok("tampered law refuses", cmd_verify([]) == 1)
        with open(la, "w", encoding="utf-8") as f:
            f.write("# LAW T-A\ntrial law a\n")
        ok("restored law walks again", cmd_verify([]) == 0)

        # THE APPENDABLE LAW - a seal holds the first N bytes; the file
        # grows below them, and nothing above them may change.
        lg = os.path.join(lib, "LAW_T_LEDGER.md")
        with open(lg, "wb") as f:
            f.write(b"# LEDGER T\n1. the first entry\n")
        cmd_seal(["LAW_T_LEDGER.md", "--note", "sealed as far as written"])
        ok("a prefix seal verifies", cmd_verify([]) == 0)
        with open(lg, "ab") as f:
            f.write(b"2. a draft below the seal\n")
        ok("an entry appended below the seal still verifies",
           cmd_verify([]) == 0)
        cmd_seal(["LAW_T_LEDGER.md", "--note", "sealed again, further"])
        ok("a second, longer seal verifies", cmd_verify([]) == 0)
        with open(lg, "rb") as f:
            kept = f.read()
        ok("status reads the furthest seal",
           seals().get("LAW_T_LEDGER.md") == len(kept))
        with open(lg, "wb") as f:
            f.write(kept.replace(b"first", b"FIRST"))
        ok("an edit above the seal refuses", cmd_verify([]) == 1)
        with open(lg, "wb") as f:
            f.write(kept[:12])
        ok("a cut into the sealed bytes refuses", cmd_verify([]) == 1)
        with open(lg, "wb") as f:
            f.write(kept)
        ok("the ledger put back walks again", cmd_verify([]) == 0)
        cmd_direct(["LAW_T_LEDGER.md", "--note", "bound whole, wrongly"])
        with open(lg, "ab") as f:
            f.write(b"3. one more draft\n")
        ok("a whole-file link cannot take an append (seal it, not direct)",
           cmd_verify([]) == 1)

        failed = [n for n, c in strokes if not c]
        for n, c in strokes:
            print("  [%s]  %s" % ("PASS" if c else "FAIL", n))
        if failed:
            print("A stroke failed. The court claims nothing.")
            return 1
        print("law prove: %d strokes, exit 0" % len(strokes))
        return 0
    finally:
        LIBRARY, CHAIN_DIR = keep
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def describe():
    print(DESCRIBE)


def main():
    if "--describe" in sys.argv:
        return describe() or 0
    if "--prove" in sys.argv:
        return prove()
    if len(sys.argv) < 2:
        print(DESCRIBE)
        return 2
    cmd = sys.argv[1]
    rest = sys.argv[2:]
    if cmd == "counsel":
        cmd_counsel(rest)
    elif cmd == "rule":
        cmd_rule(rest)
    elif cmd == "direct":
        cmd_direct(rest)
    elif cmd == "seal":
        cmd_seal(rest)
    elif cmd == "refuse":
        cmd_refuse(rest)
    elif cmd == "verify":
        return cmd_verify(rest)
    elif cmd == "status":
        cmd_status(rest)
    else:
        print(DESCRIBE)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
