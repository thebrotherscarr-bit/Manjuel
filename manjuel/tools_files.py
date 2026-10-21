"""The ground's search and patch doors: ground_grep, find_files, apply_patch.

WHY THESE THREE (2026-10-21, the harness study). Every coding harness the
study read -- opencode, Cline, Codex, Hermes -- gives its model the same
three hands before anything else: a regex search over the tree, a glob over
the tree, and a patch that can touch several files at once. Steward had
ground_read and ground_list, which answer "what is in THIS file" and "what is
in THIS folder", and nothing that answers "WHERE is it". A model that cannot
ask where a name is used reads files one by one until its budget is gone.

THE WALLS ARE THE ONES ALREADY STANDING. Nothing here draws a new jail:

  - the two readers walk the ground and never name or open what ground_read
    refuses -- a secret or a protected file by `is_secret`/`is_protected`,
    worlds/ and any vault/ (ESTATE LAW 2), every .git/ -- and they skip what
    is not the work: node_modules, index/, logs/_prompts, __pycache__, a
    virtualenv, a binary (a NUL in its first 4 KB), a file over 2 MB;
  - the writer goes through every wall ground_write and ground_edit go
    through, by calling the same functions: `_inside_ground`,
    `never_written`, `line_of_work`, the .py structural gate, the
    terminator kept and MIXED refused (skills.py, THE TREE DOORS).

THE PATCH IS WHOLE OR NOTHING (Hermes' V4A, Cline's rule). Every hunk of
every file is found against the files as they stand BEFORE any file is
touched; one miss refuses the whole patch, naming each hunk that failed and
why. A half-applied patch leaves a tree nobody wrote, which is worse than a
refusal: the refusal says what to fix, the half-tree hides it.

Registered on import; skills.py imports this module at its end, so the
handlers are in place whenever the library is.
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

from .skills import (skill, unjail, _inside_ground, never_written, line_of_work,
                     repo_of, terminator_for, checked_python, _one_terminator)
from .vectors import is_protected, is_secret

try:
    # The forgiving matcher's own pieces (skills.py, THE PLAIN FORMS): one map
    # of curly quotes, long dashes and odd spaces to their plain twins, and the
    # "nearest lines" help on a miss. Reused so a model that learns what
    # ground_edit forgives finds the same forgiveness here.
    from .skills import _PLAIN, _nearest_lines
except ImportError:                          # pragma: no cover - older skills.py
    _PLAIN = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                            "–": "-", "—": "-", " ": " "})

    def _nearest_lines(lines, wanted):
        return ""


# =====================================================================
# THE WALK: what the two readers may see
# =====================================================================

# Skipped at ANY depth: the history, the vendored, the derived, the client.
_SKIP_ANYWHERE = {".git", "node_modules", "__pycache__", ".venv", "venv",
                  ".mypy_cache", ".pytest_cache", "vault"}
# Skipped at the ground's top only: another world's (ESTATE LAW 2), and the
# index, which is derived from the ground and would answer every search twice.
_SKIP_TOP = {"worlds", "index"}
# Skipped by their path from the ground: full prompts repeat the objective
# and the feed once per stage, so a search would drown in near-duplicates.
_SKIP_PATHS = {("logs", "_prompts")}

GREP_MAX_BYTES = 2 * 1024 * 1024
GREP_SHOW = 200
GREP_LINE_CHARS = 200
FIND_SHOW = 300
_GLOB_CHARS = set("*?[{")


def _skip_dir(rel_parts: tuple, name: str) -> bool:
    """Whether the walk goes into this folder. Judged by name, never by
    content: a folder that is not the work is not opened at all."""
    low = name.lower()
    if low in _SKIP_ANYWHERE or is_secret(name):
        return True
    if not rel_parts and low in _SKIP_TOP:
        return True
    return tuple(p.lower() for p in rel_parts) + (low,) in _SKIP_PATHS


def _walk(ground: Path, start: Path):
    """Every file under `start` the readers may see, as (path, rel posix).

    A secret or a protected file is dropped HERE, before any caller sees its
    name, so no reader built on this can name one. `is_protected` is asked
    with its peek: the [[CLIENT]] token lives in a file's first bytes, and a
    file that carries it is never named either."""
    ground = ground.resolve()
    for root, dirs, files in os.walk(start):
        here = Path(root)
        try:
            rel_parts = here.resolve().relative_to(ground).parts
        except ValueError:
            dirs[:] = []
            continue
        dirs[:] = sorted(d for d in dirs if not _skip_dir(rel_parts, d))
        for f in sorted(files):
            p = here / f
            if is_secret(f) or os.path.islink(p):
                continue
            if is_protected(p):
                continue
            yield p, "/".join(rel_parts + (f,))


def _glob_re(pattern: str):
    """A glob as a compiled regex over ground-relative posix paths.

    `**/` is any number of folders (none included), `**` anything, `*` and
    `?` stay inside one folder, `[...]` is a class and `{a,b}` a choice.
    Case-insensitive on Windows, where the disk is."""
    out, i = [], 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[" and pattern.find("]", i + 1) > i + 1:
            j = pattern.find("]", i + 1)
            cls = pattern[i + 1:j]
            if cls.startswith("!"):
                cls = "^" + cls[1:]
            out.append("[" + cls.replace("\\", "\\\\") + "]")
            i = j + 1
        elif c == "{" and pattern.find("}", i) > i:
            j = pattern.find("}", i)
            out.append("(?:" + "|".join(re.escape(a) for a in pattern[i + 1:j].split(",")) + ")")
            i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(out) + "$", re.IGNORECASE if os.name == "nt" else 0)


def _scope(env, raw: str, verb: str, bare_is_anywhere: bool):
    """(start folder, path matcher or None, label, refusal) for a reader's
    <filepath>.

    A folder limits the walk to it. A file is that file alone. A glob is
    matched against every walked path; one with no `/` in it matches at any
    depth, the way .gitignore reads one (`*.py`, `skills.py`). A bare name
    that is neither a folder nor a file is `**/<name>`."""
    ground = Path(env.ground).resolve()
    raw = unjail((raw or "").strip().strip("'\"`").replace("\\", "/")).strip("/")
    if not raw or raw in (".", "**", "**/*"):
        return ground, None, "the ground", ""
    if raw.startswith("/") or ":" in raw:
        return None, None, "", (f"Refused: '{raw}' is an absolute path; give one relative "
                                f"to the ground. Nothing was searched.")
    parts = raw.split("/")
    fixed = []
    for p in parts:
        if _GLOB_CHARS & set(p):
            break
        fixed.append(p)
    low = [p.lower() for p in fixed]
    if (low and low[0] == "worlds") or "vault" in low or ".git" in low:
        return None, None, "", (f"Refused [ESTATE LAW 2]: '{raw}' is under worlds/, a vault/ "
                                f"or a .git/, and {verb} never opens or names what is "
                                f"there. Nothing was searched.")
    globbed = len(fixed) < len(parts)
    if not globbed:
        here = _inside_ground(env, raw)
        if here is None:
            return None, None, "", (f"Refused: '{raw}' is outside the ground. Nothing was "
                                    f"searched.")
        if here.is_dir():
            return here, None, raw, ""
        if here.is_file():
            rel = here.relative_to(ground).as_posix()
            return here.parent, (lambda r, want=rel.lower(): r.lower() == want), raw, ""
        if "/" in raw or not bare_is_anywhere:
            return None, None, "", (f"Error: '{raw}' is not a folder or a file in the ground. "
                                    f"For a pattern send a glob, e.g. `**/*.py` or "
                                    f"`skills/*.md`.")
    if "/" not in raw:
        rx = _glob_re("**/" + raw)
        return ground, rx.match, raw, ""
    start = _inside_ground(env, "/".join(fixed)) if fixed else ground
    if start is None:
        return None, None, "", f"Refused: '{raw}' reaches outside the ground. Nothing was searched."
    if not start.is_dir():
        return None, None, "", (f"Error: '{'/'.join(fixed)}' is not a folder in the ground, so "
                                f"'{raw}' matches nothing.")
    return start, _glob_re(raw).match, raw, ""


# =====================================================================
# ground_grep
# =====================================================================

@skill("ground_grep")
def _ground_grep(env, args: dict) -> str:
    """A regex search over the ground, live from disk. Read-only.

    SMART CASE (ripgrep's rule): a pattern written all in lower case matches
    any case; one carrying a capital means it. The model rarely knows how a
    name is capitalised and nearly always knows when it does.

    A BAD REGEX IS REFUSED WITH THE REGEX'S OWN ERROR, so the next try can
    mend the pattern instead of guessing what went wrong."""
    pattern = args.get("content") or ""
    if not pattern.strip():
        return ("Refused: ground_grep needs the pattern as <content> (a Python regex, "
                "e.g. `def _ground_read` or `never_written\\(`), and optionally the folder "
                "or glob to search as <filepath>.")
    flags = re.IGNORECASE if pattern == pattern.lower() else 0
    try:
        rx = re.compile(pattern, flags)
    except re.error as exc:
        return (f"Refused: {pattern!r} is not a valid regex -- {exc}. Escape a literal "
                f"( [ . * + ? with a backslash. Nothing was searched.")
    start, match, label, why = _scope(env, args.get("filepath") or "", "ground_grep", True)
    if why:
        return why
    ground = Path(env.ground)
    hits: list[str] = []
    total = 0
    files_hit = 0
    searched = 0
    for p, rel in _walk(ground, start):
        if match is not None and not match(rel):
            continue
        try:
            if p.stat().st_size > GREP_MAX_BYTES:
                continue
            raw = p.read_bytes()
        except OSError:
            continue
        if b"\x00" in raw[:4096]:
            continue
        searched += 1
        found_here = False
        for n, line in enumerate(raw.decode("utf-8", "replace").splitlines(), 1):
            if rx.search(line):
                total += 1
                found_here = True
                if len(hits) < GREP_SHOW:
                    text = line.rstrip()
                    if len(text) > GREP_LINE_CHARS:
                        text = text[:GREP_LINE_CHARS] + "..."
                    hits.append(f"{rel}:{n}: {text}")
        files_hit += found_here
    case = "any case" if flags else "case as written"
    if not total:
        return (f"No hits for /{pattern}/ ({case}) in {label}: {searched:,} file(s) "
                f"searched, live from disk.")
    head = (f"{total:,} hit(s) for /{pattern}/ ({case}) in {files_hit:,} file(s) of "
            f"{searched:,} searched in {label}, live from disk (read-only):")
    tail = [f"({total - len(hits):,} more not shown -- narrow the pattern or the "
            f"<filepath>)"] if total > len(hits) else []
    return "\n".join([head] + hits + tail)


# =====================================================================
# find_files
# =====================================================================

@skill("find_files")
def _find_files(env, args: dict) -> str:
    """Files in the ground by glob, newest first. Read-only.

    NEWEST FIRST because the file a model is looking for is most often the
    one just touched -- opencode's glob sorts the same way for that reason."""
    raw = (args.get("filepath") or args.get("content") or "").strip()
    if not raw:
        return ("Refused: find_files needs a glob as <filepath>, e.g. `**/*.py`, "
                "`skills/*.md`, or a bare name like `skills.py` (found at any depth).")
    start, match, label, why = _scope(env, raw, "find_files", True)
    if why:
        return why
    ground = Path(env.ground)
    found = []
    for p, rel in _walk(ground, start):
        if match is not None and not match(rel):
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        found.append((st.st_mtime, rel, st.st_size))
    if not found:
        return f"No files in the ground match '{label}'."
    found.sort(key=lambda x: (-x[0], x[1]))
    lines = [f"{len(found):,} file(s) match '{label}', newest first, live from disk "
             f"(read-only):"]
    for mtime, rel, size in found[:FIND_SHOW]:
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
        lines.append(f"  {rel}  ({size:,} bytes, {when})")
    if len(found) > FIND_SHOW:
        lines.append(f"({len(found) - FIND_SHOW:,} more not shown -- narrow the glob)")
    return "\n".join(lines)


# =====================================================================
# apply_patch
# =====================================================================
#
# THE ENVELOPE is Codex's (OpenAI's apply_patch), because it is the one the
# models were trained to write:
#
#   *** Begin Patch
#   *** Add File: path            every line after it begins with +
#   *** Update File: path
#   *** Move to: path             optional, right after Update
#   @@ optional context line      a hunk: ' ' context, '-' removed, '+' added
#   *** End of File               optional: the hunk sits at the file's end
#   *** Delete File: path
#   *** End Patch
#
# Whatever wraps it -- a ```fence, a shell heredoc (`apply_patch <<'EOF'`) --
# is outside the two marker lines and is never read. A patch with no
# `*** End Patch` is refused: it may have been cut off, and a cut-off patch
# applied is a tree nobody wrote.
#
# A HUNK IS FOUND BY WHOLE LINES, not as a substring. ground_edit's
# `_locate_passage` matches characters, which is right for a passage a model
# quotes; a hunk is lines, and a three-character context line matched
# mid-line would land a change in the wrong place. The three tiers are the
# same: exactly, then with trailing spaces ignored, then with quotes, dashes
# and odd spaces made plain (its _PLAIN map). Each must find ONE place; an
# `@@ line` header may pick one of several, the way Codex uses it.

_BEGIN = "*** Begin Patch"
_END = "*** End Patch"
_ADD = "*** Add File:"
_UPDATE = "*** Update File:"
_DELETE = "*** Delete File:"
_MOVE = "*** Move to:"
_EOF = "*** End of File"
_UNIFIED_HEAD = re.compile(r"^-\d+(?:,\d+)? \+\d+(?:,\d+)? @@\s*(.*)$")


class _Hunk:
    __slots__ = ("n", "header", "old", "new", "eof", "added", "removed", "kinds")

    def __init__(self, n: int, header: str):
        self.n, self.header = n, header
        self.old, self.new, self.kinds = [], [], []
        self.eof = False
        self.added = self.removed = 0


class _Op:
    __slots__ = ("kind", "path", "dest", "lines", "hunks")

    def __init__(self, kind: str, path: str):
        self.kind, self.path = kind, path
        self.dest = ""
        self.lines: list[str] = []
        self.hunks: list[_Hunk] = []


def _parse_patch(text: str) -> tuple[list, list]:
    """(ops, problems). Pure: reads the text, touches no disk."""
    lines = (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    begin = next((i for i, l in enumerate(lines) if l.strip() == _BEGIN), None)
    if begin is None:
        return [], [f"no `{_BEGIN}` line: a patch is `{_BEGIN}`, then the file "
                    f"operations, then `{_END}`"]
    end = next((i for i in range(begin + 1, len(lines)) if lines[i].strip() == _END), None)
    if end is None:
        return [], [f"no `{_END}` line after `{_BEGIN}`: the patch may have been cut "
                    f"off, so none of it is applied"]
    body = lines[begin + 1:end]
    ops: list[_Op] = []
    problems: list[str] = []
    op = None
    for k, line in enumerate(body, begin + 2):
        head = line.strip()
        if head.startswith((_ADD, _UPDATE, _DELETE)):
            kind = ("add" if head.startswith(_ADD) else
                    "update" if head.startswith(_UPDATE) else "delete")
            path = head.split(":", 1)[1].strip()
            if not path:
                problems.append(f"line {k}: `{head}` names no file")
            op = _Op(kind, path)
            ops.append(op)
            continue
        if op is None:
            if head:
                problems.append(f"line {k}: expected `{_ADD}`, `{_UPDATE}` or `{_DELETE}`, "
                                f"got {line[:80]!r}")
            continue
        if op.kind == "delete":
            if head:
                problems.append(f"line {k}: `{_DELETE} {op.path}` takes no lines, got "
                                f"{line[:80]!r}")
            continue
        if op.kind == "add":
            if line.startswith("+"):
                op.lines.append(line[1:])
            elif not line.strip():
                op.lines.append("")
            else:
                problems.append(f"line {k}: in `{_ADD} {op.path}` every line begins with "
                                f"+, got {line[:80]!r}")
            continue
        # update
        if head.startswith(_MOVE) and not op.hunks and not op.dest:
            op.dest = head.split(":", 1)[1].strip()
            continue
        if line.startswith("@@"):
            hdr = line[2:].strip()
            m = _UNIFIED_HEAD.match(hdr)
            if m:
                hdr = m.group(1).strip()
            op.hunks.append(_Hunk(len(op.hunks) + 1, hdr))
            continue
        if head == _EOF:
            if op.hunks:
                op.hunks[-1].eof = True
            continue
        if not op.hunks:
            op.hunks.append(_Hunk(1, ""))
        h = op.hunks[-1]
        if line.startswith(" "):
            h.old.append(line[1:]); h.new.append(line[1:]); h.kinds.append(" ")
        elif line.startswith("-"):
            h.old.append(line[1:]); h.removed += 1; h.kinds.append("-")
        elif line.startswith("+"):
            h.new.append(line[1:]); h.added += 1; h.kinds.append("+")
        elif line == "":
            h.old.append(""); h.new.append(""); h.kinds.append("")
        else:
            problems.append(f"line {k}: in `{_UPDATE} {op.path}` hunk {h.n}, a line begins "
                            f"with ' ', '-' or '+', got {line[:80]!r}")
    for op in ops:
        while op.kind == "add" and op.lines and op.lines[-1] == "":
            op.lines.pop()
        for h in op.hunks:
            # A bare blank line at a hunk's END is the wire's, not the file's.
            while h.kinds and h.kinds[-1] == "":
                h.old.pop(); h.new.pop(); h.kinds.pop()
        if op.kind == "update" and not op.hunks and not op.dest:
            problems.append(f"`{_UPDATE} {op.path}` has no hunk and no `{_MOVE}`: nothing to do")
        for h in op.hunks:
            if not h.added and not h.removed:
                problems.append(f"{op.path} hunk {h.n}: changes nothing (no + or - line)")
    if not ops and not problems:
        problems.append("the patch names no file")
    return ops, problems


def patch_targets(text: str) -> list[str]:
    """Every path a patch names -- each file it adds, updates, moves to or
    deletes -- as written, in order. Pure; for a caller that must know the
    files before the patch runs (a card that names them, a driver that keeps
    their bytes to put back)."""
    ops, _ = _parse_patch(text)
    out: list[str] = []
    for op in ops:
        for p in (op.path, op.dest):
            if p and p not in out:
                out.append(p)
    return out


def _find_block(lines: list, want: list, header: str, eof: bool) -> tuple:
    """(start line index, how it matched, refusal) for one hunk's old lines."""
    n = len(want)
    last = len(lines) - (1 if lines and lines[-1] == "" else 0)
    tiers = (("", lambda s: s),
             ("with trailing spaces ignored", lambda s: s.rstrip()),
             ("with quotes, dashes and spaces made plain", lambda s: s.translate(_PLAIN).rstrip()))
    for how, f in tiers:
        hay = [f(l) for l in lines]
        w = [f(l) for l in want]
        first = w[0]
        found = [i for i in range(len(hay) - n + 1)
                 if hay[i] == first and hay[i:i + n] == w]
        if not found:
            continue
        if len(found) > 1 and eof:
            at_end = [i for i in found if i + n >= last]
            found = at_end or found
        if len(found) > 1 and header:
            key = f(header).strip()
            marks = [i for i, l in enumerate(hay) if l.strip() == key] or \
                    [i for i, l in enumerate(hay) if key and key in l]
            if marks:
                after = [i for i in found if i > marks[0]]
                found = after[:1] if after else found
        if len(found) == 1:
            return found[0], how, ""
        where = ", ".join(str(i + 1) for i in found[:6])
        return None, how, (f"its old lines appear {len(found)} times (at lines {where}"
                           f"{', ...' if len(found) > 6 else ''}); add context lines, or an "
                           f"`@@` line naming the definition it is in, until it is unique")
    return None, "", ("its old lines are not in the file -- quote them exactly, whitespace "
                      "and all." + _nearest_lines(lines, want))


def _apply_hunks(flat: str, op: _Op) -> tuple[str, list, list]:
    """(new text, notes, problems). Every hunk is found against the file AS
    IT STANDS, then they are applied bottom-up so no hunk moves another."""
    lines = flat.split("\n")
    placed, problems, notes = [], [], []
    for h in op.hunks:
        tag = f"{op.path} hunk {h.n}" + (f" (@@ {h.header[:60]})" if h.header else "")
        if not h.old:
            at = len(lines) - (1 if lines and lines[-1] == "" else 0)
            placed.append((at, 0, h))
            continue
        at, how, why = _find_block(lines, h.old, h.header, h.eof)
        if why:
            problems.append(f"{tag}: {why}")
            continue
        if how:
            notes.append(f"hunk {h.n} matched {how}")
        placed.append((at, len(h.old), h))
    placed.sort(key=lambda x: (x[0], x[2].n))
    for (a, an, ha), (b, bn, hb) in zip(placed, placed[1:]):
        if a + an > b:
            problems.append(f"{op.path} hunks {ha.n} and {hb.n} overlap (lines {a + 1}-"
                            f"{a + an} and {b + 1}-{b + bn}); merge them into one hunk")
    if problems:
        return "", notes, problems
    for at, n, h in reversed(placed):
        lines[at:at + n] = h.new
    return "\n".join(lines), notes, []


def _python_gate(name: str, before: str, after: str) -> tuple[str, str]:
    """(refusal, carried) for a .py as it would stand. HELD TO WHAT IT ADDS,
    the way `_apply_passage` holds an edit: a file that already carries what
    the gate refuses takes a patch that adds none of it, and the reply says
    what it carried."""
    import ast as _ast
    from .pipeline import inspect_code as _inspect_code, inspect_added as _inspect_added
    try:
        _ast.parse(after)
    except SyntaxError as exc:
        return (f"{name} would not parse after the patch -- {exc.msg} at line "
                f"{exc.lineno}"), ""
    ok, why = _inspect_code(name, after)
    if ok:
        return "", ""
    added = _inspect_added(name, before, after)
    if added:
        return (f"the patch would leave {name} {added} -- the same check ground_edit, "
                f"write_file and the coder's landing make"), ""
    return "", why


def _recoverable(repo: Path, path: Path) -> str:
    """"" when the file's bytes are in the repository's last commit, so a
    delete can be undone from history; else why not. Asks git read-only
    questions only (ls-files, hash-object without -w, rev-parse)."""
    from . import gitstate as _git
    rel = path.resolve().relative_to(repo.resolve()).as_posix()
    try:
        rc, _ = _git._run(["ls-files", "--error-unmatch", "--", rel], repo)
        if rc != 0:
            return "it is not tracked by git, so a delete could never be undone"
        rc1, now = _git._run(["hash-object", "--", rel], repo)
        rc2, head = _git._run(["rev-parse", "HEAD:" + rel], repo)
    except RuntimeError as exc:
        return f"git could not be asked ({exc})"
    if rc1 != 0 or rc2 != 0 or now != head:
        return ("it carries work that is not in the last commit, and a delete would lose "
                "it; commit it first")
    return ""


def _target(env, raw: str, lines_of_work: dict) -> tuple:
    """(path, rel, refusal) through the tree doors' walls: inside the
    ground, never written, on a line of work (asked once per repository)."""
    rel = unjail((raw or "").strip().strip("'\"`"))
    if not rel:
        return None, rel, "names no file"
    path = _inside_ground(env, rel)
    if path is None:
        return None, rel, "is outside the ground"
    why = never_written(env, path)
    if why:
        return None, rel, why.replace(" Nothing was written.", "")
    repo = repo_of(env, path)
    key = str(repo)
    if key not in lines_of_work:
        lines_of_work[key] = line_of_work(env, path)
    why, _branch = lines_of_work[key]
    if why:
        return None, rel, why.replace(" Nothing was written.", "")
    return path, rel, ""


@skill("apply_patch")
def _apply_patch(env, args: dict) -> str:
    """Apply a multi-file patch to the ground, on a line of work, whole or
    not at all.

    PHASE ONE touches nothing: it parses the envelope, puts every named path
    through the walls, reads every file, finds every hunk and runs the .py
    gate on every file as it would stand. Any problem anywhere and the whole
    patch is refused, every problem named. PHASE TWO writes; if the disk
    fails part way, every file already written is put back as it was."""
    text = args.get("content") or ""
    ops, problems = _parse_patch(text)
    if problems:
        return _refused(problems)
    ground = Path(env.ground).resolve()
    lines_of_work: dict = {}
    plan = []                 # (kind, rel, path, dest_rel, dest, new bytes or None, summary)
    seen: dict = {}
    for op in ops:
        path, rel, why = _target(env, op.path, lines_of_work)
        if why:
            problems.append(f"{rel or op.path}: {why}")
            continue
        dest, dest_rel = None, ""
        if op.dest:
            dest, dest_rel, why = _target(env, op.dest, lines_of_work)
            if why:
                problems.append(f"{dest_rel or op.dest} (the move's destination): {why}")
                continue
            if dest == path:
                dest, dest_rel = None, ""
        for p, r in ((path, rel), (dest, dest_rel)):
            if p is not None:
                if p in seen:
                    problems.append(f"{r}: named twice in one patch ({seen[p]} and {op.kind}); "
                                    f"one operation per file")
                seen.setdefault(p, op.kind)
        if op.kind == "add":
            if path.exists():
                problems.append(f"{rel}: already exists; `{_UPDATE}` changes a file that is there")
                continue
            if not path.parent.is_dir():
                problems.append(f"{rel}: its folder does not exist, and a seat makes no folder "
                                f"-- a new folder is the operator's to place (RULE 8)")
                continue
            body = "\n".join(op.lines) + "\n"
            why = checked_python(path, body)
            if why:
                problems.append(f"{rel}: {why.replace('Refused: ', '', 1)}")
                continue
            eol = terminator_for(path) or b"\n"
            kept = "CRLF" if eol == b"\r\n" else "LF"
            plan.append(("add", rel, path, "", None,
                         body.replace("\n", eol.decode()).encode("utf-8"),
                         f"added {rel}: {len(op.lines)} line(s), {kept}"))
            continue
        if not path.is_file():
            problems.append(f"{rel}: there is no such file in the ground to "
                            f"{'delete' if op.kind == 'delete' else 'update'}")
            continue
        if op.kind == "delete":
            why = _recoverable(repo_of(env, path), path)
            if why:
                problems.append(f"{rel}: not deleted -- {why}")
                continue
            plan.append(("delete", rel, path, "", None, None, f"deleted {rel}"))
            continue
        raw = path.read_bytes()
        eol = _one_terminator(raw)
        if not eol:
            problems.append(f"{rel}: has MIXED line endings, so a patch cannot keep what it "
                            f"has; that is a file to fix before it is patched")
            continue
        if b"\x00" in raw[:4096]:
            problems.append(f"{rel}: is binary, and a patch is for text")
            continue
        try:
            before = raw.decode("utf-8")
        except UnicodeDecodeError:
            problems.append(f"{rel}: is not UTF-8 text, and patching it would re-encode it")
            continue
        flat = before.replace("\r\n", "\n")
        if op.hunks:
            after, notes, bad = _apply_hunks(flat, op)
            if bad:
                problems.extend(bad)
                continue
        else:
            after, notes = flat, []
        out_path = dest or path
        carried = ""
        if out_path.suffix.lower() == ".py":
            why, carried = _python_gate(out_path.name, flat if path.suffix.lower() == ".py" else "", after)
            if why:
                problems.append(f"{dest_rel or rel}: {why}")
                continue
        if dest is not None:
            if dest.exists():
                problems.append(f"{dest_rel}: the move's destination already exists")
                continue
            if not dest.parent.is_dir():
                problems.append(f"{dest_rel}: its folder does not exist, and a seat makes no "
                                f"folder (RULE 8)")
                continue
        plus = sum(h.added for h in op.hunks)
        minus = sum(h.removed for h in op.hunks)
        kept = "CRLF" if eol == b"\r\n" else "LF"
        what = (f"moved {rel} -> {dest_rel}" if dest is not None else f"updated {rel}")
        summary = (f"{what}: {len(op.hunks)} hunk(s), +{plus} -{minus} line(s), {kept} kept"
                   + (f" ({'; '.join(notes)})" if notes else "")
                   + (f"; the file already carried what the gate refuses -- {carried} -- and "
                      f"the patch added none of it" if carried else ""))
        plan.append(("move" if dest is not None else "update", rel, path, dest_rel, dest,
                     after.replace("\n", eol.decode()).encode("utf-8"), summary))
    if problems:
        return _refused(problems)

    # PHASE TWO. Every original is held before the first byte moves.
    saved: list = []
    try:
        for kind, rel, path, dest_rel, dest, data, _ in plan:
            if kind == "add":
                saved.append((path, None))
                path.write_bytes(data)
            elif kind == "update":
                saved.append((path, path.read_bytes()))
                path.write_bytes(data)
            elif kind == "move":
                saved.append((dest, None))
                dest.write_bytes(data)
                saved.append((path, path.read_bytes()))
                path.unlink()
            else:
                saved.append((path, path.read_bytes()))
                path.unlink()
    except OSError as exc:
        put_back = []
        for p, old in reversed(saved):
            try:
                if old is None:
                    if p.exists():
                        p.unlink()
                else:
                    p.write_bytes(old)
            except OSError as exc2:
                put_back.append(f"{p.name} ({exc2})")
        return (f"Refused: the disk failed part way ({exc}). "
                + ("Every file written was put back as it was. Nothing was written."
                   if not put_back else
                   f"These could NOT be put back and need the operator's eye: "
                   f"{', '.join(put_back)}."))
    branches = sorted({b for why, b in lines_of_work.values() if b})
    on = ", ".join(f"`{b}`" for b in branches)
    return (f"Patched {len(plan)} file(s) on line of work {on}:\n"
            + "\n".join(f"  {p[6]}" for p in plan)
            + "\nUnsaved until git_commit lands it on that line; the main line moves only "
              "by the operator's hand.")


def _refused(problems: list) -> str:
    return (f"Refused: the patch was checked whole and NOTHING WAS WRITTEN. "
            f"{len(problems)} problem(s):\n" + "\n".join(f"  - {p}" for p in problems))


# =====================================================================
# The strokes: run on a temp ground of their own, never on this one
# =====================================================================

def _strokes() -> None:
    """Prove the three on a throwaway ground with its own git repository on
    a line of work. Raises AssertionError on the first failure, naming it."""
    import shutil
    import subprocess
    import sys
    import tempfile
    from .skills import SkillExecutionEnv, _HANDLERS

    def check(name: str, ok: bool, detail: str = "") -> None:
        if not ok:
            raise AssertionError(f"{name}\n--- got ---\n{detail}")
        print(f"  ok  {name}")

    g = Path(tempfile.mkdtemp(prefix="tools_files_")).resolve()

    def git(*a):
        return subprocess.run(["git", *a], cwd=str(g), capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=30)

    def put(rel: str, data) -> Path:
        p = g / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return p

    try:
        (g / "agent_workspace").mkdir()
        put("src/alpha.py", "def alpha():\n    return 'needle'\n\n\ndef beta():\n    return 2\n")
        put("src/notes.md", "# Notes\r\nThe Needle is here.\r\nit’s a second line\r\n")
        put("src/many.txt", "".join(f"hit {i}\n" for i in range(250)))
        put("secrets.txt", "needle in a secret\n")
        put("api_key.json", '{"needle": 1}\n')
        put("notes.client.md", "needle for a client\n")
        put("tagged.md", "[[CLIENT]]\nneedle tagged\n")
        put("vault/inside.md", "needle in a vault\n")
        put("worlds/w/a.md", "needle in a world\n")
        put("node_modules/m.js", "needle vendored\n")
        put("blob.dat", b"needle\x00\x01\x02")
        put("big.txt", "needle\n" + "x" * (GREP_MAX_BYTES + 10))
        put("law/LAW.md", "the law\n")
        put("gone.txt", "to be deleted\n")
        git("init", "-b", "steward-test")
        git("config", "user.name", "prove")
        git("config", "user.email", "prove@localhost")
        git("config", "core.autocrlf", "false")
        git("add", "-A")
        c = git("commit", "-m", "the first save")
        check("the temp ground has a real commit", c.returncode == 0, c.stderr + c.stdout)
        os.utime(g / "src/alpha.py", (1_000_000_000, 1_000_000_000))
        os.utime(g / "src/many.txt", (1_500_000_000, 1_500_000_000))
        os.utime(g / "src/notes.md", (2_000_000_000, 2_000_000_000))
        env = SkillExecutionEnv(workspace=g / "agent_workspace", registry=None, runtime=None,
                                ground=g, session="S-strokes")
        grep, find, patch = (_HANDLERS["ground_grep"], _HANDLERS["find_files"],
                             _HANDLERS["apply_patch"])

        # ---- ground_grep -------------------------------------------------
        out = grep(env, {"content": "needle"})
        check("grep: lower case matches any case, two real hits",
              out.startswith("2 hit(s)") and "src/alpha.py:2:" in out
              and "src/notes.md:2: The Needle is here." in out, out)
        for bad in ("secret", "api_key", "client", "tagged", "vault", "worlds",
                    "node_modules", "blob", "big.txt"):
            check(f"grep: never names {bad}", bad not in out.lower().split("live from disk")[1], out)
        out = grep(env, {"content": "Needle"})
        check("grep: a capital means case as written",
              out.startswith("1 hit(s)") and "notes.md" in out and "alpha" not in out, out)
        out = grep(env, {"content": "needle", "filepath": "**/*.py"})
        check("grep: a glob limits it", out.startswith("1 hit(s)") and "src/alpha.py:2" in out, out)
        out = grep(env, {"content": "needle", "filepath": "src"})
        check("grep: a folder limits it", out.startswith("2 hit(s)"), out)
        out = grep(env, {"content": "hit \\d+"})
        check("grep: 200 shown and the rest counted",
              out.startswith("250 hit(s)") and "(50 more not shown" in out
              and len(out.splitlines()) == 1 + 200 + 1, out[:300])
        out = grep(env, {"content": "(unclosed"})
        check("grep: a bad regex is refused with its own error",
              out.startswith("Refused:") and "missing )" in out, out)
        out = grep(env, {"content": "needle", "filepath": "worlds"})
        check("grep: worlds/ is refused by name", out.startswith("Refused [ESTATE LAW 2]"), out)
        out = grep(env, {"content": "needle", "filepath": "../"})
        check("grep: outside the ground is refused", out.startswith("Refused"), out)

        # ---- find_files --------------------------------------------------
        out = find(env, {"filepath": "src/*"})
        rows = [l.strip().split("  ")[0] for l in out.splitlines()[1:]]
        check("find: newest first, with sizes",
              rows == ["src/notes.md", "src/many.txt", "src/alpha.py"] and "bytes" in out, out)
        out = find(env, {"filepath": "*.py"})
        check("find: a glob with no slash matches at any depth",
              out.startswith("1 file(s)") and "src/alpha.py" in out, out)
        out = find(env, {"filepath": "alpha.py"})
        check("find: a bare name is **/<name>", "src/alpha.py" in out, out)
        out = find(env, {"filepath": "secrets.txt"})
        check("find: a secret is never named", out.startswith("No files"), out)
        out = find(env, {"filepath": "**/*.md"})
        check("find: client, tagged, vault and worlds files are never named",
              "client" not in out and "tagged" not in out and "vault" not in out
              and "worlds" not in out and "src/notes.md" in out, out)

        # ---- apply_patch: whole or nothing --------------------------------
        a0, n0 = (g / "src/alpha.py").read_bytes(), (g / "src/notes.md").read_bytes()
        bad = ("*** Begin Patch\n"
               "*** Update File: src/alpha.py\n"
               "@@ def alpha():\n"
               "-    return 'needle'\n"
               "+    return 'thread'\n"
               "*** Update File: src/notes.md\n"
               "@@\n"
               "-This line is not there\n"
               "+anything\n"
               "*** Add File: src/never.py\n"
               "+X = 1\n"
               "*** End Patch\n")
        out = patch(env, {"content": bad})
        check("patch: one bad hunk refuses the whole patch, naming it",
              out.startswith("Refused: the patch was checked whole and NOTHING WAS WRITTEN")
              and "src/notes.md hunk 1" in out, out)
        check("patch: and writes NOTHING",
              (g / "src/alpha.py").read_bytes() == a0 and (g / "src/notes.md").read_bytes() == n0
              and not (g / "src/never.py").exists(), out)

        good = ("Here it is:\n```\napply_patch <<'EOF'\n*** Begin Patch\n"
                "*** Update File: src/alpha.py\n"
                "@@ def alpha():\n"
                "-    return 'needle'\n"
                "+    return 'thread'\n"
                "@@ def beta():\n"
                "-    return 2\n"
                "+    return 3\n"
                "*** Update File: src/notes.md\n"
                "@@\n"
                " The Needle is here.\n"
                "-it's a second line\n"
                "+a second line, patched\n"
                "*** Add File: src/gamma.py\n"
                "+def gamma():\n"
                "+    return 'new'\n"
                "*** End Patch\nEOF\n```\n")
        check("patch_targets names every file before it runs",
              patch_targets(good) == ["src/alpha.py", "src/notes.md", "src/gamma.py"],
              str(patch_targets(good)))
        out = patch(env, {"content": good})
        check("patch: two updates and an add, through a fence and a heredoc",
              out.startswith("Patched 3 file(s) on line of work `steward-test`")
              and "updated src/alpha.py: 2 hunk(s), +2 -2" in out
              and "updated src/notes.md" in out and "added src/gamma.py" in out, out)
        alpha = (g / "src/alpha.py").read_bytes()
        notes = (g / "src/notes.md").read_bytes()
        check("patch: LF kept in the .py",
              b"\r" not in alpha and b"return 'thread'\n" in alpha and b"return 3\n" in alpha,
              repr(alpha))
        check("patch: CRLF kept in the .md, and a curly quote matched plain",
              notes == b"# Notes\r\nThe Needle is here.\r\na second line, patched\r\n"
              and "made plain" in out, repr(notes))
        check("patch: a new .py takes its neighbours' LF",
              (g / "src/gamma.py").read_bytes() == b"def gamma():\n    return 'new'\n",
              repr((g / "src/gamma.py").read_bytes()))

        # ---- the walls ---------------------------------------------------
        def one(body: str) -> str:
            return patch(env, {"content": "*** Begin Patch\n" + body + "*** End Patch\n"})

        out = one("*** Update File: src/alpha.py\n@@\n-    return 3\n+    return eval('3')\n")
        check("patch: the .py gate refuses eval, nothing written",
              out.startswith("Refused") and "eval" in out
              and (g / "src/alpha.py").read_bytes() == alpha, out)
        out = one("*** Add File: law/NEW.md\n+no\n")
        check("patch: law/ is never written", out.startswith("Refused") and "law/" in out, out)
        out = one("*** Add File: .env\n+KEY=1\n")
        check("patch: a secret is never written",
              out.startswith("Refused") and "secret" in out and not (g / ".env").exists(), out)
        out = one("*** Add File: newdir/x.py\n+X = 1\n")
        check("patch: no folder is made", out.startswith("Refused") and "RULE 8" in out, out)
        out = patch(env, {"content": "*** Begin Patch\n*** Add File: src/cut.py\n+X = 1\n"})
        check("patch: no End Patch, nothing applied",
              out.startswith("Refused") and "cut" in out and not (g / "src/cut.py").exists(), out)
        out = one("*** Delete File: src/gamma.py\n")
        check("patch: an untracked file is never deleted",
              out.startswith("Refused") and "not tracked" in out and (g / "src/gamma.py").exists(), out)

        git("add", "-A")
        git("commit", "-m", "the patch")
        out = one("*** Update File: src/gamma.py\n*** Move to: src/delta.py\n@@\n"
                  "-    return 'new'\n+    return 'moved'\n"
                  "*** Delete File: gone.txt\n")
        check("patch: a move with a hunk and a delete",
              out.startswith("Patched 2 file(s)") and "moved src/gamma.py -> src/delta.py" in out
              and not (g / "src/gamma.py").exists() and not (g / "gone.txt").exists()
              and (g / "src/delta.py").read_bytes() == b"def gamma():\n    return 'moved'\n", out)

        (g / "src/notes.md").write_bytes(b"# Notes\r\nmixed\n")
        out = one("*** Update File: src/notes.md\n@@\n-mixed\n+fine\n")
        check("patch: a MIXED file is refused", out.startswith("Refused") and "MIXED" in out, out)

        git("checkout", "-q", "-b", "main")
        out = one("*** Update File: src/delta.py\n@@\n-    return 'moved'\n+    return 'main'\n")
        check("patch: the main line is refused",
              out.startswith("Refused") and "main line is the operator's" in out
              and b"'moved'" in (g / "src/delta.py").read_bytes(), out)
    finally:
        def _writable(func, p, _exc):
            os.chmod(p, 0o700)
            func(p)
        if sys.version_info >= (3, 12):
            shutil.rmtree(g, onexc=_writable)
        else:
            shutil.rmtree(g, onerror=_writable)
