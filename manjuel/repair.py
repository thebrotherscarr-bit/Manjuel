"""Call repair for Steward: a small model's tool call, mended before it is judged.

The driver (serve.py, drive_calls) takes a model's tool call as it comes. A
small model's call often arrives nearly right and is thrown away for a
character: a trailing comma, a missing brace at the end, "count": "3" where
the schema says integer, `ReadFile` for `read_file`, or the whole call written
out as plain text in a template the model was trained on instead of the
native tool_calls field. Proven harnesses (oh-my-pi, OpenClaw, Cline,
opencode) repair these before they judge them; this is that repair, in one
place, the standard library only.

What it will NOT do is guess. A value the model did not send is never made
up; a tool name is fixed only when one name is plainly meant; a call written
as text is promoted only when its name EXACTLY matches a tool on offer
(OpenClaw's rule), so prose that mentions a tool never runs it. What cannot be
mended is refused in words the model can act on -- what was wrong, field by
field, and what it sent -- so the next turn can put it right. And a reply the
length limit cut off is refused whole, never run (cut_by_length): a cut call
can parse cleanly and still be missing the half that mattered.

    repair_json(text)                    -> (value or None, note)
    coerce_args(args, schema)            -> (args, notes)
    nearest_tool(name, names)            -> str
    normalize_call(name, raw_args, schemas, notes=None) -> (name, args or None, problem)
    text_calls(text, names)              -> [(name, args), ...]
    cut_by_length(resp)                  -> bool
"""

from __future__ import annotations

import difflib
import json
import re

# oh-my-pi's MAX_HEAL_DISTANCE: a single-character heal is tried only where the
# parser fails within this many characters of the end, and at most this many
# heals are made. A fault in the middle of a reply is not a typo at the tail;
# it is refused, not rewritten.
MAX_HEAL_DISTANCE = 3

# How deep coerce_args walks into nested objects and arrays.
MAX_DEPTH = 6

# How much of what the model sent is quoted back in a refusal.
RECEIVED_CHARS = 400

_ESCAPABLE = set('"\\/bfnrtu')
_HEX = set("0123456789abcdefABCDEF")
_PY_WORDS = {"True": "true", "False": "false", "None": "null"}
_CLOSER = {"{": "}", "[": "]"}
_OPENER = {"}": "{", "]": "["}


# ---------------------------------------------------------------------------
# repair_json


def _loads(text):
    """(value, None) when text parses as JSON, else (None, the JSONDecodeError)."""
    try:
        return json.loads(text), None
    except ValueError as e:      # JSONDecodeError is a ValueError
        return None, e


def _unfence(text: str) -> str:
    """The inside of the first ``` fence, or text unchanged when there is none. An
    opening fence with no closing one (a reply cut short) is stripped on its own."""
    m = re.search(r"```[A-Za-z0-9_+-]*[ \t]*\r?\n?(.*?)```", text, re.S)
    if m:
        return m.group(1).strip()
    m = re.match(r"\s*```[A-Za-z0-9_+-]*[ \t]*\r?\n?(.*)$", text, re.S)
    if m:
        return m.group(1).strip()
    return text


def _drop_trailing_comma(out: list) -> bool:
    """Remove a comma left before a closer (whitespace after it kept). True if one went."""
    i = len(out) - 1
    while i >= 0 and out[i] in " \t\r\n":
        i -= 1
    if i >= 0 and out[i] == ",":
        del out[i]
        return True
    return False


def _scan(text: str) -> tuple:
    """One string-aware pass over text: (repaired text, [what was done]).

    Inside a string: raw control characters escaped, bad backslashes doubled, a
    single-quoted string rewritten double-quoted. Outside one: Python's True,
    False and None spelled as JSON, trailing commas removed, a closer that does
    not match its opener answered with the closers it skipped, a closer with no
    opener dropped. At the end: an open string closed, then every open bracket
    and brace closed in order."""
    out: list = []
    stack: list = []
    done: dict = {}
    quote = ""                       # '' outside a string, else the quote that opened it
    i, n = 0, len(text)

    def mark(what):
        done[what] = done.get(what, 0) + 1

    while i < n:
        ch = text[i]
        if quote:
            if ch == "\\":
                nxt = text[i + 1] if i + 1 < n else ""
                if quote == "'" and nxt == "'":
                    out.append("'")
                    i += 2
                    continue
                if nxt == "u" and all(c in _HEX for c in text[i + 2:i + 6]) and len(text[i + 2:i + 6]) == 4:
                    out.append(text[i:i + 6])
                    i += 6
                    continue
                if nxt and nxt in _ESCAPABLE and nxt != "u":
                    out.append(ch + nxt)
                    i += 2
                    continue
                out.append("\\\\")
                mark("bad backslash doubled")
                i += 1
                continue
            if ch == quote:
                out.append('"')
                quote = ""
                i += 1
                continue
            if ch == '"':            # a double quote inside a single-quoted string
                out.append('\\"')
                i += 1
                continue
            if ord(ch) < 0x20:
                esc = {"\n": "\\n", "\r": "\\r", "\t": "\\t", "\b": "\\b", "\f": "\\f"}
                out.append(esc.get(ch) or "\\u%04x" % ord(ch))
                mark("control character escaped")
                i += 1
                continue
            out.append(ch)
            i += 1
            continue
        # outside a string
        if ch == '"' or ch == "'":
            if ch == "'":
                mark("single quotes made double")
            quote = ch
            out.append('"')
            i += 1
            continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j]
            if word in _PY_WORDS:
                out.append(_PY_WORDS[word])
                mark("Python literal made JSON")
            else:
                out.append(word)
            i = j
            continue
        if ch in "{[":
            stack.append(ch)
            out.append(ch)
            i += 1
            continue
        if ch in "}]":
            if _drop_trailing_comma(out):
                mark("trailing comma removed")
            want = _OPENER[ch]
            if stack and stack[-1] == want:
                stack.pop()
                out.append(ch)
            elif want in stack:
                while stack[-1] != want:
                    out.append(_CLOSER[stack.pop()])
                    mark("missing closer added")
                stack.pop()
                out.append(ch)
            else:
                mark("stray closer dropped")
            i += 1
            continue
        out.append(ch)
        i += 1

    if quote:
        if out and out[-1] == "\\" and not (len(out) > 1 and out[-2] == "\\"):
            out.append("\\")
        out.append('"')
        mark("open string closed")
    if stack:
        if _drop_trailing_comma(out):
            mark("trailing comma removed")
        while stack:
            out.append(_CLOSER[stack.pop()])
            mark("missing closer added")
    return "".join(out), [f"{k} x{v}" if v > 1 else k for k, v in done.items()]


def _heal(text: str, left: int):
    """(value, edits): a parse of text reached by at most `left` single-character
    edits, each made where the parser failed and within MAX_HEAL_DISTANCE of the
    end; else None."""
    value, err = _loads(text)
    if err is None:
        return value, 0
    if left <= 0:
        return None
    pos = getattr(err, "pos", len(text))
    if len(text) - pos > MAX_HEAL_DISTANCE:
        return None
    tries = [text[:pos] + text[pos + 1:]] if pos < len(text) else []
    if pos > 0:
        tries.append(text[:pos - 1] + text[pos:])
    tries += [text[:pos] + c + text[pos:] for c in '"}],:']
    for t in tries:
        got = _heal(t, left - 1)
        if got is not None:
            return got[0], got[1] + 1
    return None


def repair_json(text) -> tuple:
    """(value, note): text parsed as JSON, repaired first where a small model's
    usual faults stop it. note says what was repaired, '' when nothing was; on
    failure value is None and note says why."""
    if not isinstance(text, str):
        return None, "not text"
    if not text.strip():
        return None, "empty"
    value, err = _loads(text)
    if err is None:
        return value, ""
    notes = []
    work = text.strip()
    inner = _unfence(work)
    if inner != work:
        notes.append("code fence stripped")
        work = inner
        value, err = _loads(work)
        if err is None:
            return value, "; ".join(notes)
    fixed, done = _scan(work)
    notes += done
    value, err = _loads(fixed)
    if err is None:
        return value, "; ".join(notes)
    healed = _heal(fixed, MAX_HEAL_DISTANCE)
    if healed is not None:
        value, edits = healed
        notes.append(f"{edits} character{'s' if edits != 1 else ''} healed near the end")
        return value, "; ".join(notes)
    return None, f"not valid JSON: {err.msg} at char {err.pos}"


# ---------------------------------------------------------------------------
# coerce_args


def _types(schema) -> list:
    t = (schema or {}).get("type") if isinstance(schema, dict) else None
    if isinstance(t, list):
        return [str(x) for x in t]
    return [str(t)] if t else []


def _show(v) -> str:
    try:
        s = json.dumps(v, ensure_ascii=False)
    except (TypeError, ValueError):
        s = repr(v)
    return s if len(s) <= 60 else s[:57] + "..."


def _number(s: str, want_int: bool):
    s = s.strip()
    if re.fullmatch(r"[+-]?\d+", s):
        return int(s)
    if re.fullmatch(r"[+-]?(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?", s):
        f = float(s)
        if want_int:
            return int(f) if f.is_integer() else None
        return int(f) if f.is_integer() and "e" not in s.lower() and "." not in s else f
    return None


def _coerce(value, schema, path: str, notes: list, depth: int):
    if depth > MAX_DEPTH or not isinstance(schema, dict):
        return value
    types = _types(schema)
    if value is None or (isinstance(value, str) and "string" in types):
        return value
    if isinstance(value, str) and ("integer" in types or "number" in types) and not isinstance(value, bool):
        got = _number(value, "number" not in types)
        if got is not None:
            notes.append(f"{path}: {_show(value)} -> {_show(got)}")
            return got
    if "integer" in types and isinstance(value, float) and value.is_integer():
        notes.append(f"{path}: {_show(value)} -> {int(value)}")
        return int(value)
    if "boolean" in types and not isinstance(value, bool):
        key = value.strip().lower() if isinstance(value, str) else value
        table = {"true": True, "yes": True, "1": True, 1: True,
                 "false": False, "no": False, "0": False, 0: False}
        if isinstance(key, (str, int)) and not isinstance(key, float) and key in table:
            notes.append(f"{path}: {_show(value)} -> {_show(table[key])}")
            return table[key]
    if "object" in types and isinstance(value, str):
        got, _ = repair_json(value)
        if isinstance(got, dict):
            notes.append(f"{path}: JSON text -> object")
            value = got
    if "array" in types and not isinstance(value, list):
        got = None
        if isinstance(value, str):
            got, _ = repair_json(value)
        if isinstance(got, list):
            notes.append(f"{path}: JSON text -> list")
            value = got
        elif not ("object" in types and isinstance(value, dict)):
            notes.append(f"{path}: single value wrapped in a list")
            value = [value]
    if isinstance(value, list) and "array" in types:
        items = schema.get("items")
        if isinstance(items, dict):
            value = [_coerce(v, items, f"{path}[{k}]", notes, depth + 1) for k, v in enumerate(value)]
        return value
    if isinstance(value, dict) and ("object" in types or "properties" in schema):
        return _coerce_object(value, schema, path, notes, depth + 1)
    return value


def _coerce_object(args: dict, schema: dict, path: str, notes: list, depth: int) -> dict:
    props = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    closed = schema.get("additionalProperties") is False
    out = {}
    for key, value in args.items():
        where = f"{path}.{key}" if path else str(key)
        if key not in props:
            if closed:
                notes.append(f"{where}: not a field of this tool, dropped")
                continue
            out[key] = value
            continue
        if key not in required and (value is None or value == ""):
            notes.append(f"{where}: empty optional field dropped")
            continue
        out[key] = _coerce(value, props[key], where, notes, depth)
    return out


def coerce_args(args, schema) -> tuple:
    """(args, notes): args brought to what schema (a JSON-schema 'parameters'
    object) declares, where the model sent the right value in the wrong form.
    Nothing is invented: a value that cannot be read as the declared type is left
    exactly as it came, for the check after to name."""
    notes: list = []
    if args is None:
        return {}, notes
    if not isinstance(args, dict) or not isinstance(schema, dict):
        return args, notes
    return _coerce_object(args, schema, "", notes, 1), notes


# ---------------------------------------------------------------------------
# nearest_tool


def _norm(name: str) -> str:
    s = str(name or "").strip()
    if s.startswith("functions."):
        s = s[len("functions."):]
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", s)
    s = re.sub(r"(?<=[A-Z])([A-Z][a-z])", r"_\1", s)
    s = re.sub(r"[-\s.]+", "_", s.lower())
    s = re.sub(r"_+", "_", s).strip("_")
    if s.endswith("_tool") and len(s) > len("_tool"):
        s = s[:-len("_tool")]
    return s


def nearest_tool(name, names) -> str:
    """The tool in names that name plainly means, or '' when none is plain: the
    exact name; then case and separator fixes (CamelCase, '-', a trailing
    '_tool', a 'functions.' prefix); then one close spelling (difflib, 0.8). Two
    names that fit equally well are not chosen between -- '' is returned."""
    names = [str(n) for n in names]
    name = str(name or "").strip()
    if not name:
        return ""
    if name in names:
        return name
    want = _norm(name)
    hits = [n for n in names if _norm(n) == want]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        return ""
    by_norm: dict = {}
    for n in names:
        by_norm.setdefault(_norm(n), []).append(n)
    close = difflib.get_close_matches(want, list(by_norm), n=2, cutoff=0.8)
    if not close:
        return ""
    if len(close) > 1:
        a = difflib.SequenceMatcher(None, want, close[0]).ratio()
        b = difflib.SequenceMatcher(None, want, close[1]).ratio()
        if a == b:
            return ""
    hit = by_norm[close[0]]
    return hit[0] if len(hit) == 1 else ""


# ---------------------------------------------------------------------------
# normalize_call


def _received(raw) -> str:
    if raw is None:
        text = "(nothing)"
    elif isinstance(raw, str):
        text = raw
    else:
        try:
            text = json.dumps(raw, ensure_ascii=False)
        except (TypeError, ValueError):
            text = repr(raw)
    return text if len(text) <= RECEIVED_CHARS else text[:RECEIVED_CHARS - 3] + "..."


def _type_name(t: str) -> str:
    return {"integer": "an integer", "number": "a number", "boolean": "true or false",
            "array": "a list", "object": "an object", "string": "a string",
            "null": "null"}.get(t, t)


def _fits(value, types: list) -> bool:
    if not types:
        return True
    for t in types:
        if t == "string" and isinstance(value, str):
            return True
        if t == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if t == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if t == "boolean" and isinstance(value, bool):
            return True
        if t == "array" and isinstance(value, list):
            return True
        if t == "object" and isinstance(value, dict):
            return True
        if t == "null" and value is None:
            return True
    return False


def _faults(args: dict, schema: dict) -> list:
    props = schema.get("properties") or {}
    faults = []
    for key in schema.get("required") or []:
        if key not in args or args[key] is None:
            faults.append(f"missing required field {key}")
    for key, value in args.items():
        sch = props.get(key)
        if not isinstance(sch, dict) or value is None:
            continue
        types = _types(sch)
        if not _fits(value, types):
            want = " or ".join(_type_name(t) for t in types)
            faults.append(f"{key} must be {want}, got {_show(value)}")
        elif "enum" in sch and isinstance(sch["enum"], list) and value not in sch["enum"]:
            faults.append(f"{key} must be one of {_show(sch['enum'])}, got {_show(value)}")
    return faults


def normalize_call(name, raw_args, schemas: dict, notes: list | None = None) -> tuple:
    """(name, args, problem) for one tool call. schemas maps each tool's name to
    its 'parameters' schema. The name is resolved (nearest_tool), text arguments
    are parsed (repair_json), values are brought to the schema (coerce_args), and
    required fields are checked. problem is '' when the call may run; otherwise
    args is None and problem is the refusal to hand back to the model. When a
    list is passed as notes, every repair made is appended to it."""
    notes = notes if notes is not None else []
    names = list(schemas)
    tool = nearest_tool(name, names)
    if not tool:
        return name, None, (f"Refused: there is no tool named {name}. "
                            f"The tools are: {', '.join(names)}.")
    if tool != name:
        notes.append(f"tool name {name!r} -> {tool!r}")

    def refuse(why):
        return tool, None, (f"Refused: {tool} was not run -- {why}. "
                            f"Received: {_received(raw_args)}. "
                            f"Call it again with corrected arguments.")

    args = raw_args
    if args is None:
        args = {}
    elif isinstance(args, str):
        if not args.strip():
            args = {}
        else:
            parsed, note = repair_json(args)
            if parsed is None:
                return refuse(f"the arguments are not a JSON object ({note})")
            if note:
                notes.append(f"arguments repaired: {note}")
            if isinstance(parsed, str):          # a JSON object sent as one JSON string
                again, note2 = repair_json(parsed)
                if isinstance(again, dict):
                    notes.append("arguments were a JSON string holding the object")
                    parsed = again
            args = parsed
    if not isinstance(args, dict):
        return refuse(f"the arguments must be a JSON object of named fields, not {_show(args)}")
    schema = schemas.get(tool) or {}
    args, cnotes = coerce_args(dict(args), schema)
    notes += cnotes
    faults = _faults(args, schema) if isinstance(schema, dict) else []
    if faults:
        return refuse("; ".join(faults))
    return tool, args, ""


# ---------------------------------------------------------------------------
# text_calls

_HARMONY = re.compile(
    r"to=(?:functions\.)?([A-Za-z0-9_\-.]+)"          # the recipient
    r"[^<]*(?:<\|(?:channel|constrain)\|>[^<]*)*"    # channel / constrain, either order, any missing
    r"<\|message\|>(.*?)(?=<\|call\|>|<\|end\|>|<\|start\|>|<\|return\|>|\Z)",
    re.S)
_HERMES = re.compile(r"<tool_call>\s*(.*?)\s*(?:</tool_call>|\Z)", re.S)
_BRACKET = re.compile(r"\[([A-Za-z0-9_\-.]+)\]\s*(.*?)\s*\[END_TOOL_REQUEST\]", re.S)
_FUNCTION = re.compile(r"<function=([A-Za-z0-9_\-.]+)>(.*?)(?:</function>|\Z)", re.S)
_PARAMETER = re.compile(r"<parameter=([A-Za-z0-9_\-.]+)>(.*?)</parameter>", re.S)


def _args_of(body):
    """A call's arguments: a dict when they parse to one, else the text as sent
    (normalize_call then refuses it in words, rather than the call vanishing)."""
    if isinstance(body, dict):
        return body
    if body is None:
        return {}
    if not isinstance(body, str):
        return body
    if not body.strip():
        return {}
    value, _ = repair_json(body)
    if isinstance(value, str):
        again, _ = repair_json(value)
        value = again if isinstance(again, dict) else value
    return value if isinstance(value, dict) else body


def _named(obj):
    """(name, args) from a {"name"|"tool": ..., "arguments"|"parameters"|"args": ...}
    object, or None when it is not one."""
    if not isinstance(obj, dict):
        return None
    name = obj.get("name", obj.get("tool"))
    if not isinstance(name, str):
        return None
    for key in ("arguments", "parameters", "args"):
        if key in obj:
            return name, _args_of(obj[key])
    return None


def _trim_newline(s: str) -> str:
    if s.startswith("\r\n"):
        s = s[2:]
    elif s.startswith("\n"):
        s = s[1:]
    if s.endswith("\r\n"):
        s = s[:-2]
    elif s.endswith("\n"):
        s = s[:-1]
    return s


def text_calls(text, names) -> list:
    """Every tool call written as plain text in a reply, as (name, args), in the
    order they appear -- each promoted ONLY when its name exactly matches one of
    names. Forms read: gpt-oss harmony, hermes/qwen <tool_call>, [NAME]{json}
    [END_TOOL_REQUEST] (and LM Studio's [TOOL_REQUEST]), qwen3-coder's
    <function=NAME><parameter=KEY>, and one bare {"name", "arguments"} object
    that is the whole reply. args is a dict, or the text as sent when it would
    not parse (normalize_call refuses that in words)."""
    if not isinstance(text, str) or not text.strip():
        return []
    names = set(str(n) for n in names)
    found: list = []

    for m in _HARMONY.finditer(text):
        found.append((m.start(), m.group(1), _args_of(m.group(2).strip())))
    for m in _HERMES.finditer(text):
        value, _ = repair_json(m.group(1))
        got = _named(value)
        if got:
            found.append((m.start(), got[0], got[1]))
    for m in _BRACKET.finditer(text):
        if m.group(1) == "TOOL_REQUEST":
            value, _ = repair_json(m.group(2))
            got = _named(value)
            if got:
                found.append((m.start(), got[0], got[1]))
        else:
            found.append((m.start(), m.group(1), _args_of(m.group(2))))
    for m in _FUNCTION.finditer(text):
        args = {k: _trim_newline(v) for k, v in _PARAMETER.findall(m.group(2))}
        found.append((m.start(), m.group(1), args))

    if not found:
        whole = text.strip()
        if whole.startswith("{") or whole.startswith("```"):
            value, _ = repair_json(whole)
            got = _named(value)
            if got:
                found.append((0, got[0], got[1]))

    found.sort(key=lambda f: f[0])
    return [(name, args) for _, name, args in found if name in names]


# ---------------------------------------------------------------------------
# cut_by_length


def cut_by_length(resp) -> bool:
    """True when an Ollama response stopped at the length limit (done_reason
    "length"). A call in such a reply may be missing its end and must be refused,
    never run -- even when what arrived happens to parse."""
    if resp is None:
        return False
    if isinstance(resp, dict):
        reason = resp.get("done_reason")
    else:
        reason = getattr(resp, "done_reason", None)
    return str(reason or "").strip().lower() == "length"


# ---------------------------------------------------------------------------
# strokes


def _strokes() -> None:
    """The behaviours above, asserted on concrete cases."""
    # repair_json ------------------------------------------------------------
    v, note = repair_json('{"a": 1}')
    assert v == {"a": 1} and note == "", (v, note)
    v, note = repair_json('```json\n{"path": "a.py"}\n```')
    assert v == {"path": "a.py"} and "fence" in note, (v, note)
    v, note = repair_json('{"path": "a.py", "count": 2,')            # trailing comma, no brace
    assert v == {"path": "a.py", "count": 2}, (v, note)
    assert "trailing comma" in note and "closer" in note, note
    v, note = repair_json('{"items": [1, 2, 3,], }')
    assert v == {"items": [1, 2, 3]} and "trailing comma" in note, (v, note)
    v, note = repair_json("{'path': 'it\"s.py', 'force': True, 'x': None}")
    assert v == {"path": 'it"s.py', "force": True, "x": None}, (v, note)
    assert "single quotes" in note and "Python literal" in note, note
    v, note = repair_json('{"text": "line one\nline two\ttab"}')     # raw newline and tab
    assert v == {"text": "line one\nline two\ttab"} and "control" in note, (v, note)
    v, note = repair_json('{"path": "C:\\Users\\kyle\\x.py"}')      # \U, \k and \x are not escapes
    assert v == {"path": "C:\\Users\\kyle\\x.py"}, (v, note)
    assert "backslash" in note, note
    v, note = repair_json('{"a": {"b": [1, 2')                     # nested, cut short
    assert v == {"a": {"b": [1, 2]}}, (v, note)
    v, note = repair_json('{"msg": "half a sentence')             # open string at the end
    assert v == {"msg": "half a sentence"} and "open string" in note, (v, note)
    v, note = repair_json('{"a": [1, 2}')                           # a closer that skips one
    assert v == {"a": [1, 2]}, (v, note)
    v, note = repair_json('{"a": 1}x')                              # junk in the last chars: healed
    assert v == {"a": 1} and "healed" in note, (v, note)
    v, note = repair_json('{"a" 1}')                                # missing colon near the end
    assert v == {"a": 1} and "healed" in note, (v, note)
    v, note = repair_json('{"a" 1, "b": 2, "c": 3, "d": 4}')        # same fault far from the end
    assert v is None and note.startswith("not valid JSON"), (v, note)
    assert repair_json("") == (None, "empty")
    assert repair_json("just words")[0] is None

    # coerce_args ------------------------------------------------------------
    schema = {"type": "object", "additionalProperties": False, "required": ["path"],
              "properties": {"path": {"type": "string"}, "count": {"type": "integer"},
                             "ratio": {"type": "number"}, "force": {"type": "boolean"},
                             "files": {"type": "array", "items": {"type": "string"}},
                             "lines": {"type": "array", "items": {"type": "integer"}},
                             "opts": {"type": "object", "properties": {"depth": {"type": "integer"}}},
                             "note": {"type": "string"}}}
    args, notes = coerce_args({"path": "a.py", "count": "3", "ratio": "0.5", "force": "yes",
                               "files": "b.py", "lines": "[1, \"2\"]", "opts": '{"depth": "4"}',
                               "note": None, "junk": 1}, schema)
    assert args == {"path": "a.py", "count": 3, "ratio": 0.5, "force": True, "files": ["b.py"],
                    "lines": [1, 2], "opts": {"depth": 4}}, args
    assert any("junk" in n for n in notes) and any("note" in n for n in notes), notes
    args, _ = coerce_args({"path": "a", "force": 0, "count": 7.0}, schema)
    assert args == {"path": "a", "force": False, "count": 7}, args
    args, _ = coerce_args({"path": "a", "count": "three", "force": "maybe"}, schema)
    assert args == {"path": "a", "count": "three", "force": "maybe"}, args   # never invented
    args, _ = coerce_args({"path": "a", "count": ""}, schema)
    assert args == {"path": "a"}, args                                       # "" optional dropped
    open_schema = {"type": "object", "properties": {"a": {"type": "integer"}}}
    assert coerce_args({"a": "1", "b": "x"}, open_schema)[0] == {"a": 1, "b": "x"}
    deep = {"type": "object", "properties": {}}
    cur = deep
    for _ in range(10):
        nxt = {"type": "object", "properties": {"n": {"type": "integer"}}}
        cur["properties"]["k"] = nxt
        cur = nxt
    val = {"k": {"k": {"k": {"k": {"k": {"k": {"k": {"k": {"n": "1"}}}}}}}}}
    got, _ = coerce_args(val, deep)
    assert got["k"]["k"]["k"]["k"]["k"]["k"]["k"]["k"]["n"] == "1", got        # past depth 6, untouched
    assert coerce_args({"k": {"n": "1"}}, deep)[0] == {"k": {"n": 1}}            # within depth, coerced

    # nearest_tool -----------------------------------------------------------
    names = ["read_file", "write_file", "edit_file", "run_python", "mcp_call", "done"]
    assert nearest_tool("read_file", names) == "read_file"
    assert nearest_tool("ReadFile", names) == "read_file"
    assert nearest_tool("read-file", names) == "read_file"
    assert nearest_tool("read_file_tool", names) == "read_file"
    assert nearest_tool("functions.run_python", names) == "run_python"
    assert nearest_tool("raed_file", names) == "read_file"               # misspelled
    assert nearest_tool("delete_everything", names) == ""
    assert nearest_tool("x_file", ["a_file", "b_file"]) == ""             # no plain winner

    # normalize_call ---------------------------------------------------------
    schemas = {"read_file": {"type": "object", "required": ["filepath"],
                             "properties": {"filepath": {"type": "string"},
                                            "count": {"type": "integer"}}},
               "done": {"type": "object", "properties": {"summary": {"type": "string"}},
                        "required": []}}
    fix_notes: list = []
    name, args, problem = normalize_call("ReadFile", '{"filepath": "a.py", "count": "3",',
                                         schemas, fix_notes)
    assert (name, args, problem) == ("read_file", {"filepath": "a.py", "count": 3}, ""), (name, args, problem)
    assert any("ReadFile" in n for n in fix_notes) and any("count" in n for n in fix_notes), fix_notes
    name, args, problem = normalize_call("read_file", {"count": "many"}, schemas)
    assert args is None and problem.startswith("Refused: read_file was not run -- "), problem
    assert "missing required field filepath" in problem and "count must be an integer" in problem, problem
    assert 'Received: {"count": "many"}.' in problem, problem
    assert problem.endswith("Call it again with corrected arguments."), problem
    name, args, problem = normalize_call("read_file", "{" + "x" * 900, schemas)
    assert args is None and "Received: {xxx" in problem, problem
    assert len(problem.split("Received: ")[1].split(". Call it again")[0]) == RECEIVED_CHARS, problem
    name, args, problem = normalize_call("rm_rf", {}, schemas)
    assert args is None and problem == "Refused: there is no tool named rm_rf. The tools are: read_file, done.", problem
    assert normalize_call("done", None, schemas) == ("done", {}, "")
    assert normalize_call("done", '"{\\"summary\\": \\"ok\\"}"', schemas) == ("done", {"summary": "ok"}, "")
    assert normalize_call("read_file", "[1, 2]", schemas)[1] is None

    # text_calls -------------------------------------------------------------
    tools = ["read_file", "run_python", "done"]
    gpt_oss = ('<|start|>assistant<|channel|>analysis<|message|>I should read it.<|end|>'
               '<|start|>assistant<|channel|>commentary to=functions.read_file '
               '<|constrain|>json<|message|>{"filepath": "manjuel/serve.py"}<|call|>')
    assert text_calls(gpt_oss, tools) == [("read_file", {"filepath": "manjuel/serve.py"})]
    bare_harmony = 'to=run_python<|message|>{"code": "print(1)"}'      # parts missing, ends at text end
    assert text_calls(bare_harmony, tools) == [("run_python", {"code": "print(1)"})]
    header_first = ('<|start|>assistant to=functions.done<|channel|>commentary json'
                    '<|message|>{"summary": "ok"}<|call|>')
    assert text_calls(header_first, tools) == [("done", {"summary": "ok"})]
    hermes = ('Reading.\n<tool_call>\n{"name": "read_file", "arguments": {"filepath": "a.py"}}\n'
              '</tool_call>\n<tool_call>{"name": "done", "arguments": "{\\"summary\\": \\"x\\"}"}</tool_call>')
    assert text_calls(hermes, tools) == [("read_file", {"filepath": "a.py"}), ("done", {"summary": "x"})]
    bracket = '[read_file]{"filepath": "b.py",}[END_TOOL_REQUEST]'
    assert text_calls(bracket, tools) == [("read_file", {"filepath": "b.py"})]
    lms = '[TOOL_REQUEST]{"name": "done", "arguments": {}}[END_TOOL_REQUEST]'
    assert text_calls(lms, tools) == [("done", {})]
    coder = ('<function=read_file>\n<parameter=filepath>\nc.py\n</parameter>\n'
             '<parameter=count>\n3\n</parameter>\n</function>')
    assert text_calls(coder, tools) == [("read_file", {"filepath": "c.py", "count": "3"})]
    assert text_calls('{"tool": "run_python", "args": {"code": "1+1"}}', tools) == \
        [("run_python", {"code": "1+1"})]
    assert text_calls('```json\n{"name": "done", "parameters": {"summary": "s"}}\n```', tools) == \
        [("done", {"summary": "s"})]
    # an unknown name is never promoted, in any form
    assert text_calls('<tool_call>{"name": "delete_ground", "arguments": {}}</tool_call>', tools) == []
    assert text_calls('to=functions.ReadFile<|message|>{"filepath": "a"}<|call|>', tools) == []
    assert text_calls('{"name": "rm", "arguments": {"path": "/"}}', tools) == []
    # prose that names a tool, or a JSON object that merely has a name, is not a call
    assert text_calls("I will call read_file next with filepath a.py.", tools) == []
    assert text_calls('{"name": "read_file"}', tools) == []
    assert text_calls('Here: {"name": "read_file", "arguments": {}} and more', tools) == []
    # broken arguments come back as text, and normalize_call refuses them in words
    (n0, a0), = text_calls('<tool_call>{"name": "read_file", "arguments": "{bad bad bad bad"}</tool_call>', tools)
    assert n0 == "read_file" and isinstance(a0, str), a0
    assert normalize_call(n0, a0, schemas)[2].startswith("Refused: read_file was not run -- the arguments")

    # cut_by_length ----------------------------------------------------------
    assert cut_by_length({"done_reason": "length", "message": {}}) is True
    assert cut_by_length({"done_reason": "stop"}) is False
    assert cut_by_length(None) is False

    class _Resp:
        done_reason = "length"

    assert cut_by_length(_Resp()) is True
