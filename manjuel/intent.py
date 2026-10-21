"""Deterministic pre-routing: does the objective plainly name a tool?

Session 5c. Three runs of `git commit` in a row never reached the Router,
because the Router only wakes on `needs_tool` and that flag was left entirely
to a 2b Steward's willingness to emit an exact XML string. It refused, then
excused, then returned nothing at all -- three different failures of the same
single point.

A request that literally says "git commit" should not need a language model's
permission to reach the git skill. This scan is free, runs before any model
is loaded, and only ever OPENS the door: the Router still decides what (if
anything) actually runs, and may still answer in prose instead.
"""

from __future__ import annotations

import hashlib
import math
import re

from .context import POINTING_WORDS

# THE WORDS THAT BELONG TO NO SINGLE SKILL (WHAT'S LEFT C51, 2026-10-20, his cards: "Every skill
# declares them", "Require it, move the table"). Each skill declares its own phrases in its own file
# (`**Says:**`), and a stroke holds that every one does; this table keeps only the here-words, the
# generic file words, the forms the number rule still guards, and the bare words a skill may not
# claim as its own (a declared phrase is two words or more, test_a_skill_owns_its_own_dispatch).
# Every other phrase moved into its skill's file that day, measured over the 752 requests on the
# record: the 18 that route differently were the faults (the linter, a trendline, "say aloud" and
# the rest), and nothing else moved.
ALIASES: dict[str, tuple[str, ...]] = {
    # The bare words worth the risk, read as a judgment call below every skill's own words.
    "git_commit": ("commit",),
    "git_push":   ("push",),
    "git_pull":   ("pull",),
    "git_status": ("dirty", "untracked"),
    # A sitting is named by NUMBER and its runs are filed by timestamp, so
    # without this the Router guesses at filenames (sitting 63 guessed
    # `logs/sitting_63.md`, twice). The word is the whole alias -- the
    # skill pulls the number out of the objective itself.
    "sitting":    ("sitting", "the sitting"),
    "list_directory": ("the workspace",),
    "ground_list": ("this place", "this archive", "this folder",
                    "this directory", "this repo", "in here", "around here"),
    "ground_read": ("read the file", "open the file", "show me the file",
                    "this file", "that file", "the file",
                    "read pipelines", "read memory.md"),
    "ground_report": ("where are we", "where am i"),
    # index_ground's phrases MOVED OUT of this table on 2026-09-02 and into
    # skills/index_ground.md, where a person editing the skill can see them
    # (`**Says:**`). It is the first skill to own its own dispatch, and the
    # pattern this table should shrink toward: what belongs to one skill
    # lives in that skill's file; what belongs to no single skill -- the
    # here-words, the cross-skill vocabulary -- stays here.
}

_WORD = re.compile(r"[a-z0-9_]+")


def _norm(text: str) -> str:
    return " ".join(_WORD.findall((text or "").lower()))


_FILENAME_RE = re.compile(
    r"\b[\w./\\-]+\.(md|py|txt|json|jsonl|us|toml|yml|yaml|csv)\b")


def names_a_file(objective: str) -> str:
    """A filename-shaped token in the objective, or "". Sitting 40: 'look at
    jesster.md' invented the file's contents instead of reading the file."""
    m = _FILENAME_RE.search(objective or "")
    return m.group(0) if m else ""


# THE CLAIM-CHECK. A seat that presents a file's contents when nothing read
# that file is asserting something the engine can already disprove -- so make
# it arithmetic rather than a matter of the model's character.
#
# NARROW ON PURPOSE. Each pattern is a construction that PRESENTS contents,
# not one that merely mentions a file: "the contents of x.md", "here is x.md",
# "x.md says". A seat discussing a file it did not read ("we should check
# x.md") is not claiming anything and must pass. HANDOFF, 2026-09-01: narrow
# and certainly right beats broad and crying wolf.
_F = r"[`'\"*]?(?P<f>[\w./\\-]+\.(?:md|py|txt|json|jsonl|us|toml|yml|yaml|csv))[`'\"*]?"
_CLAIM_RES = tuple(re.compile(p, re.I) for p in (
    rf"\bcontents?\s+of\s+(?:the\s+file\s+)?{_F}",
    rf"\bhere\s*(?:is|are|'s)\s+(?:the\s+)?"
    rf"(?:contents?|text|body|file|poem|note)\b[^.\n]{{0,40}}?{_F}",
    rf"{_F}\s+(?:says|reads|contains|states)\b",
    rf"\b(?:according\s+to|as\s+written\s+in|quoting|straight\s+from)\s+{_F}",
    rf"\bfile\s+{_F}\s*(?::|\bcontains\b|\bsays\b)",
))


def claims_file_contents(text: str) -> str:
    """The file a seat's own output claims to be SHOWING, or "".

    Point this at the SEAT'S OUTPUT, never at the objective: the objective
    asking for a file is a request, and only the reply can make a claim.

    HONEST LIMITS, written here rather than discovered later:
      - It catches a claim that NAMES A FILE. Invention that cites nothing
        still passes, and always will.
      - It proves a claim is UNSUPPORTED, never that it is FALSE. That is
        enough: LAW 5 says testimony is not fact, and an unsupported claim of
        fact is exactly what must not reach the operator.
      - A seat legitimately quoting a file read in an EARLIER turn trips it.
        The caller scopes it to THIS turn's reads and accepts that cost.
    """
    for rx in _CLAIM_RES:
        m = rx.search(text or "")
        if m:
            return m.group("f")
    return ""


# THE CITATION-CHECK's two halves (named sitting 61, built 2026-09-02).
# semantic_search prints one header line per hit:
#     1. logs/x.md  [chunk 3 @ 120]  written 2h ago  cosine 0.5140
# so the tool output IS the exhaustive list of (path, cosine) this turn.
_RESULT_LINE = re.compile(
    r"(?m)^\s*\d+\.\s+(?P<p>\S+)\s+\[[^\]]*\][^\n]*?\bcosine\s+(?P<s>\d\.\d+)\s*$")

# A filename with a score-like number near it on the same line. Narrow BY
# DESIGN, like the claim-check: it wants a path CITED AS A SCORED RESULT,
# not any mention of a file near any number.
_CITED_PAIR = re.compile(
    r"[`'\"*]?(?P<f>[\w./\\-]+\.(?:md|py|txt|json|jsonl|us|toml|yml|yaml|csv))"
    r"[`'\"*]?[^\n]{0,80}?\b(?P<s>[01]\.\d{2,4})")


def search_result_pairs(results_text: str) -> list:
    """Every (path, cosine) a search actually returned, parsed from the
    result header lines. Snippets are indented and never match."""
    return [(m.group("p").replace("\\", "/"), m.group("s"))
            for m in _RESULT_LINE.finditer(results_text or "")]


def cites_search_results(prose: str) -> list:
    """Every (path, score) a seat's prose presents as a scored hit.

    Sitting 61: the Router lifted a filename out of one result's SNIPPET
    and reported it as "Most Relevant" carrying ANOTHER result's cosine.
    Unlike uncited invention this has ground truth -- the cited pair either
    appears in the tool output or it does not. HONEST LIMIT: prose that
    fabricates without naming a path and a number still passes; that class
    is the claim-check's, and beyond both when it cites nothing at all."""
    return [(m.group("f").replace("\\", "/"), m.group("s"))
            for m in _CITED_PAIR.finditer(prose or "")]


# ---------------------------------------------------------------------
# Numbers a seat said that no tool returned
# ---------------------------------------------------------------------
#
# MOVED HERE FROM cli.py 2026-09-10, UNCHANGED. It lived beside `/brief` and
# ran only there, so the one place a seat most often invents a number -- an
# ordinary turn, speaking after a tool returned -- was never checked by the
# engine at all. SPEC 4.7's "the door invents numbers (35 for 37)", and
# 2026-09-09's "37 markdown files, ranging from 300 to 1200 bytes in size"
# with 300 and 1200 in no tool result that run.
#
# It belongs in this module because this is where the estate reads the SHAPE
# of text, and because `cites_search_results` and `search_result_pairs` above
# are the CITED half of the same question. cli.py keeps the old names as
# aliases; /brief, tests/standup.py and the strokes are untouched.

_NUM_OR_HASH = re.compile(r"(?<![\w.])([0-9a-f]{7,40}|\d[\d,]*\.?\d*)(?![\w.])")

_MONTHS = (r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
           r"jul(?:y)?|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|"
           r"nov(?:ember)?|dec(?:ember)?")

CLOCK_SHAPES = re.compile(r"""
      \d{4}-\d{2}-\d{2}(?:[T ]\d{1,2}:\d{2}(?::\d{2})?)?      # 2026-09-09, with time
    | \d{1,2}[/]\d{1,2}[/]\d{2,4}                              # 09/09/2026
    | \d{1,2}:\d{2}(?::\d{2})?(?:\s*[ap]\.?m\.?)?              # 12:15, 12:15:30, 3:04 pm
    | \b\d{1,2}\s+(?:""" + _MONTHS + r""")\b\.?(?:,?\s*\d{4})?   # 09 September 2026
    | \b(?:""" + _MONTHS + r""")\b\.?\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\d{4})?
    """, re.IGNORECASE | re.VERBOSE)


def without_clock(text: str) -> str:
    """`text` with every date and clock expression blanked out.

    Used by both number guards -- this one and the standup's -- so the two can
    never disagree about what a date looks like.
    """
    return CLOCK_SHAPES.sub(" ", text or "")


# A NUMBER GLUED TO ITS UNIT IN A SOURCE (2026-10-21, the cut of v0.2.6). rack_list prints "13.8GB";
# gpt-oss writes "13.8 GB", and _NUM_OR_HASH, which stops at a letter, read the tool's number as no
# number at all -- so both guards called a true answer invented and the release stopped at its live
# check. A SOURCE is loosened from its units before it is read; what is JUDGED is not, so nothing said
# that no tool returned passes. One definition, shared with the standup's guard.
_GLUED_UNIT = re.compile(r"(\d)(?=(?:[kKMGT]i?B|B|ms|s|min|h)(?![\w]))")


def unglued(text: str) -> str:
    """`text` with a space between a number and the unit glued to it (13.8GB -> 13.8 GB)."""
    return _GLUED_UNIT.sub(r"\1 ", text or "")


def unsourced_numbers(said: str, facts: str) -> list[str]:
    """Numbers and hashes in `said` that appear nowhere in `facts`.

    Small integers (0-12) are words in prose and are not judged, and
    numbers written as a date or a clock are not judged either (see
    CLOCK_SHAPES). Everything else is. A number in `facts` glued to its
    unit (13.8GB) is read as the number it is (unglued).
    """
    have = {m.group(1).replace(",", "").rstrip(".") for m in _NUM_OR_HASH.finditer(unglued(facts))}
    out = []
    # `facts` keeps its dates -- they are a SOURCE. Only what is judged is
    # stripped, so the door may say the date without being called a liar.
    for m in _NUM_OR_HASH.finditer(without_clock(said)):
        tok = m.group(1).replace(",", "").rstrip(".")
        if tok.isdigit() and int(tok) <= 12:
            continue
        if tok in have or any(tok in h or h in tok for h in have if len(tok) >= 7):
            continue
        if tok not in out:
            out.append(tok)
    return out


# A LISTING THE CLOSING SEAT MUST NOT SHORTEN (WHAT'S LEFT C7, 2026-10-02). "What models are on the
# rack?" is answered by `rack_list`, which returns every installed model by name; the closing seat
# (llama3.2) then PARAPHRASES the result and drops the names. Measured over every such turn on record:
# of fourteen the answer named all eleven twice; the eight of 2026-09-30 named 3, 0, 11, 8, 4, 0, 0
# and 3, and the one of 2026-10-02 named none ("eleven installed, three loaded, eight ready"). Nothing
# was invented, so the number check cannot see it: the names were OMITTED. So it is arithmetic, like
# the failures `recompose` appends (pipeline.py): where the objective NAMED a listing tool and the
# closing words leave out items the tool returned, the listing travels with the answer.
#
# Only a tool whose result is a LIST OF NAMED THINGS belongs here, and only the rack's is (the measured
# fault); a tool is added by adding a line, not by a model's guess. The pattern's `item` group is the
# name; a line that does not open with one is not an item, so the seats' lines and the card's are not
# read. THE FORMAT IS A CONVENTION UNTIL A STROKE HOLDS IT: one calls the real `rack_list` and
# requires this pattern to find every model it printed, so a changed layout is red, not silence.
LISTING_TOOLS = {
    # tool: (what the operator calls it, what one item is, the pattern)
    "rack_list": ("the rack", "model", re.compile(
        r"^[ \t]*(?:LOADED[ \t]+)?(?P<item>[A-Za-z0-9][\w.\-]*:[\w.\-]+)[ \t]+[\d?]", re.M)),
    # THE SKILLS' TWO LISTINGS (WHAT'S LEFT C46, sitting 373: four of skill_search's five named,
    # git_pull dropped). Their item lines as the handlers write them: skill_report's "  name   its
    # first sentence" -- never its use lines ("used N", "never used:") -- and skill_search's
    # "  name   (file.md)". A stroke reads both handlers' real output with these.
    "skill_report": ("the skills", "skill", re.compile(
        r"^  (?P<item>[a-z][a-z0-9_]*) +(?!used \d|used:)\S", re.M)),
    "skill_search": ("the matching skills", "skill", re.compile(
        r"^  (?P<item>[a-z][a-z0-9_]*) +\([^)\n]+\)[ \t]*$", re.M)),
}


def listing_items(skill: str, result: str) -> list[str]:
    """The items a listing tool's result names, in its order and once each; [] for a tool that is not
    a listing, or a result with none."""
    spec = LISTING_TOOLS.get(skill)
    if spec is None:
        return []
    out: list[str] = []
    for m in spec[2].finditer(result or ""):
        if m.group("item") not in out:
            out.append(m.group("item"))
    return out


def _is_named(item: str, said_l: str) -> bool:
    """An item is named when its words are in `said_l` (already lower-cased); a model's `:latest` is
    its default tag and is not said aloud ("llama3.2")."""
    low = item.lower()
    return low in said_l or (low.endswith(":latest") and low[:-len(":latest")] in said_l)


def dropped_items(skill: str, result: str, said: str) -> list[str]:
    """The items of a listing that `said` does not name, in the listing's order."""
    said_l = (said or "").lower()
    return [i for i in listing_items(skill, result) if not _is_named(i, said_l)]


def listing_lines(skill: str, result: str) -> list[str]:
    """The listing's own item lines, as the tool wrote them (the indent trimmed, runs of spaces
    closed up), in its order."""
    spec = LISTING_TOOLS.get(skill)
    if spec is None:
        return []
    return [re.sub(r"\s{2,}", "  ", line.strip())
            for line in (result or "").splitlines() if spec[2].match(line)]


# Asking to be ADVISED, not to be told. `rack_report` gives facts only
# unless a judgement is asked for (the operator, 2026-09-09: "4.3 facts
# only"), and this is the test.
#
# THE BURDEN IS ON ASKING, deliberately. The default is the observed numbers,
# so a question that does not plainly ask for an opinion gets them; being
# wrong that way costs a reading he can ask for again, and being wrong the
# other way is a seat's prose the Router will summarise instead of the facts
# -- which is the fault this exists to close (sitting 85, three times).
#
# Every frame here is first-person-addressed or explicitly evaluative. A bare
# "what is the state of the rack?" is a FACTS question and must not match.
_JUDGEMENT_RE = re.compile(
    r"\bshould\s+(?:i|we|you|it|he|they|the)\b"
    r"|\bwhat\s+should\b"
    r"|\bwould\s+you\s+(?:recommend|advise|suggest|keep|drop|pull)\b"
    r"|\b(?:recommend|advise|suggest|evaluate|assess|critique|appraise)\b"
    r"|\byour\s+(?:opinion|read|view|assessment|judgement|judgment|take|advice)\b"
    r"|\bwhat\s+do\s+you\s+(?:think|make\s+of|reckon)\b"
    r"|\bdo\s+you\s+think\b"
    r"|\bis\s+it\s+(?:worth|wise|sensible|safe|a\s+good\s+idea)\b"
    r"|\bany\s+(?:concerns?|worries|problems?|issues?)\b"
    r"|\bwhat\s+would\s+you\b",
    re.IGNORECASE)


def asks_for_a_judgement(question: str) -> bool:
    """Does this question ask to be ADVISED, rather than told?

    Used by rack_report to decide whether a seat is woken at all. False is the
    safe answer and the default: the caller gets the observed numbers, which
    are never wrong, instead of a reading that has been (SPEC 4.7 -- the
    Quartermaster on llama3.2 invented in three of three readings).
    """
    return bool(_JUDGEMENT_RE.search(question or ""))


# Asking ABOUT a tool, not asking FOR it. The frames are deliberately
# narrow and all interrogative: a question about a thing, never an order
# involving it. "read pipelines.md" must keep dispatching.
_ABOUT_FRAMES = (
    "what does", "what do", "what is", "what are", "whats", "what can",
    "how does", "how do", "how is", "how would", "when do", "when should",
    "when would", "why would", "why does", "tell me about", "explain",
    "describe", "what happens when", "what would happen",
)
_ABOUT_TAIL = ("do", "does", "mean", "work", "works", "used for", "for",
               "good for", "about")


def asks_about_a_tool(objective: str, keywords) -> str:
    """The tool a question is ASKING ABOUT, or "".

    SITTING 69: "what does deep research do?" matched the spaced keyword
    form, dispatched the skill, and the closing seat then narrated the
    Router's DESCRIPTION as completed work -- "Deep research conducted an
    intensive analytical evaluation", past tense, over a run in which
    nothing ran. Every skill in the library is a landmine for a question
    about it, and the library is the thing the operator most needs to ask
    about.

    A question about a tool is answered FROM THE SKILL'S OWN MARKDOWN,
    which is authoritative and already written: facts read, not generated.

    A QUESTION IS ABOUT A SKILL WHEN IT SAYS THE SKILL'S NAME (WHAT'S LEFT C51,
    its follow-up, 2026-10-20; his card: "Name or table only"). A declared
    `**Says:**` phrase is the act itself: "what are the mean, median and
    standard deviation of 4, 8, 15?" asks for the numbers, not about
    `statistics`. So the naming here is read off the names and the shared
    table alone. Measured over the 748 asks on the record: that ask moved, and
    nothing else did.
    """
    named = names_a_tool(objective, keywords.keywords() if hasattr(keywords, "keywords")
                         else keywords)
    if not named:
        return ""
    text = " ".join((objective or "").lower().split())
    if not (text.endswith("?") or any(text.startswith(f) for f in _ABOUT_FRAMES)):
        return ""
    if not any(text.startswith(f) for f in _ABOUT_FRAMES):
        return ""
    # An order can still wear a question mark ("can you read pipelines.md?"),
    # so the frame must be ABOUT-shaped: it asks what the thing is or does,
    # rather than asking the thing to happen.
    if wants_writing(text) or names_a_file(text):
        return ""
    tail = text.rstrip("?").split()
    if tail and (tail[-1] in _ABOUT_TAIL or text.startswith(
            ("what is", "what are", "whats", "tell me about", "explain",
             "describe"))):
        return named
    return ""


# AN EDIT IS A WRITE (WHAT'S LEFT C8, 2026-09-30). The 09-28 coder-flow run
# had the Steward claim an edit that never happened, and this reader knew
# saved / wrote / created / stored / committed / added and not edited,
# updated, modified, changed, rewrote or patched -- so a claimed edit to a
# named file passed as speech. Same honest limit as before: a NAMED file.
_WROTE_RES = tuple(re.compile(p, re.I) for p in (
    r"\b(?:saved|wrote|created|stored|committed|added|edited|updated|modified|"
    r"changed|rewrote|patched)\s+(?:it\s+)?"
    r"(?:as|to|into|in)?\s*[`'\"]?(?P<f>[\w./\\-]+\.\w{1,6})",
    r"\bI\s+(?:have\s+|'ve\s+)?(?:saved|wrote|written|created|stored|edited|updated|"
    r"modified|changed|rewritten|patched)\s+"
    r"[^.\n]{0,40}?[`'\"]?(?P<g>[\w./\\-]+\.\w{1,6})",
))


def claims_wrote_a_file(text: str) -> str:
    """The file a seat says it WROTE, or "".

    SITTING 70's closer: "Yesterday, I compiled a poem about autumn, saved
    it as 'poem.txt' in the Research folder, and successfully read it back
    to you." There is no yesterday, no poem.txt, and no earlier reading --
    a whole invented history, of which the one true clause was that
    `speak` had run.

    None of the existing gates could see it. The claim-check wants a
    CONTENTS claim and this claims a SAVE; the citation-check wants a
    search result; the recompose only appends failures. But it is the same
    arithmetic in a new place: a seat says a file was written, and the
    turn's tool calls say whether any writer ran.

    Same honest limits as its sibling: it wants a NAMED FILE, so invention
    that cites nothing still passes, and it proves a claim UNSUPPORTED
    rather than false. Narrow and certainly right beats broad and crying
    wolf."""
    for rx in _WROTE_RES:
        m = rx.search(text or "")
        if m:
            return (m.groupdict().get("f") or m.groupdict().get("g") or "")
    return ""


# KEYWORDS THAT ARE ALSO GRAMMAR. A skill may be called `when`, and then the
# word "when" appears in every third sentence anyone writes -- as a
# conjunction, doing a job that has nothing to do with the skill. On
# 2026-09-12 the coder flow's `verify` objective carried a brief that said
# "...when executed, it should print 55", and intent dispatched the `when`
# skill: a transcript-window reader, woken to answer a question about a
# Python file, because of a subordinate clause.
#
# A CONTENT word is different. "inspect", "remember", "statistics" are also
# keywords, and someone who writes them usually does mean the thing; they are
# left alone. These are FUNCTION words: they carry no subject of their own, so
# they are grammar unless the sentence is plainly ABOUT them.
#
# Only `when` is a keyword today. The rest are here because a skill named
# `how` or `where` would arrive with the same fault already fixed.
_FUNCTION_WORDS = frozenset({
    "when", "where", "what", "who", "whom", "why", "how", "which",
    "if", "then", "while", "until", "after", "before", "since", "unless",
})

# `when`, `'when'`, "when" -- a word wearing quotes is a word being NAMED
# rather than used. Checked against the RAW objective, because _norm strips
# exactly the marks that carry the distinction.
_QUOTED = "`'\"*"


# A KEYWORD WHOSE ARGUMENT IS A NUMBER WANTS A NUMBER BESIDE IT.
#
# `when` was fixed by asking whether a function word was NAMED or merely
# spoken. `sitting` is the next collision and needs a different question,
# because it is a CONTENT word: `skills/sitting.md` resolves a numbered
# sitting -- "review sitting 63", "what ran in sitting 47" -- and this estate
# says the bare word constantly. CLAUDE.md and `law/` alone carry it 58 times:
# "while the operator's sitting is open", "mid-sitting", "the sitting laws".
#
# THE SKILL'S OWN DECLARATION IS THE TEST, not a list beside it. `sitting.md`
# says its argument is "The sitting number alone, e.g. 63", so a naming has a
# number next to it and a mention does not. Read off `param_notes` -- the
# author's own words -- which is the same doctrine that put phrases in
# `**Says:**` (sitting 66: markdown declares, Python only runs it).
_NUMERIC_PARAM = re.compile(r"\bnumber\b", re.I)

# How far after the keyword a digit may sit and still be its argument:
# "sitting 63", "sitting number 63", "sitting #63" all count; "sitting is
# open" does not.
_NUMBER_WINDOW = 2


def _wants_a_number(spec) -> bool:
    """Does this skill's own markdown describe its argument as a number?"""
    if spec is None:
        return False
    try:
        notes = spec.param_notes or {}
    except Exception:
        return False
    return any(_NUMERIC_PARAM.search(str(v or "")) for v in notes.values())


def _number_follows(form: str, hay: str) -> bool:
    """Is there a digit within `_NUMBER_WINDOW` words after this form in hay?

    `hay` is normalised, so punctuation is already gone and "sitting 84's
    toll" reads as "sitting 84 s toll" -- which is still a naming, and still
    finds its number.
    """
    words = hay.split()
    n = len(form.split())
    for i in range(len(words) - n + 1):
        if words[i:i + n] == form.split():
            for w in words[i + n:i + n + _NUMBER_WINDOW]:
                if any(ch.isdigit() for ch in w):
                    return True
    return False


def _wears_quotes(form: str, raw: str) -> bool:
    """A word wearing quotes is a word being NAMED rather than used."""
    return any(f"{q}{form}{q}" in raw.lower() for q in _QUOTED)


def _named_not_used(form: str, hay: str, raw: str) -> bool:
    """Is this FUNCTION-WORD form being NAMED here, rather than spoken?

    Two ways, both structural: it OPENS the objective ("when did we last
    commit" is a question about time; "...when executed" is a clause), or it
    wears quotes in the raw text ("call `when`").

    THE OPENING CLAUSE IS FOR FUNCTION WORDS ONLY, and the numeric rule below
    must not borrow it -- see `_wants_a_number`'s use. A WH-word at the front
    of a sentence IS the question; a content word at the front is just a
    sentence. `ALIASES` carries "the sitting", so "the sitting laws bind any
    hand" opens with the form and means nothing of the kind.
    """
    if hay == form or hay.startswith(form + " "):
        return True
    return _wears_quotes(form, raw)


# THE WORKSPACE HAS ITS OWN READER AND LISTER (sitting 370). The table names
# the ground's reader and lister by "read the file" and "list the files";
# said with the workspace as the place, the workspace's own skill is the one
# he means. "read the file measure.py from the workspace" is read_file --
# not ground_read, and not list_directory on a tie the alphabet broke.
_WORKSPACE_TWINS = {"ground_read": "read_file", "ground_list": "list_directory"}
_WORKSPACE_PLACE = re.compile(r"(?<![a-z0-9_])(?:(?:the|my|our|agent) workspace|agent_workspace)(?![a-z0-9_])")


def names_a_tool(objective: str, keywords) -> str:
    """Return the keyword the objective names, or "" if none does.

    Matches the keyword itself (`git_commit`), its spaced form (`git commit`),
    a phrase the skill declares in its own file (`**Says:**`), and the shared
    table above. WHICH ONE WINS is his word of 2026-10-12, the plain intent of
    the input read off what the system actually has: a skill's OWN words (its
    name, its spaced name, its `Says:`) outrank the shared table; then a form
    he LEADS with (after one courtesy clause) outranks one named later; then
    the longest, so `git_commit` still beats `commit`. Sitting 370 measured the
    old rule, length alone: "inspect the file INVENTORY.md" went to ground_read
    on the table's "the file", one letter longer than "inspect". Said with the
    workspace as the place, the ground's reader and lister give way to the
    workspace's own (`_WORKSPACE_TWINS`). And an order to run a named `.py` is
    not taken by anything but his own lead: wants_running reads it next.

    A ONE-WORD KEYWORD THAT IS ENGLISH GRAMMAR must be named, not merely
    spoken -- see `_FUNCTION_WORDS`. A declared `**Says:**` phrase is never
    subject to that: a phrase is already a naming, which is why the cure for a
    skill caught by this is to declare its phrases in its own markdown.

    A skill may declare its OWN phrases in its markdown (`**Says:**`), and
    those are read here alongside the table below. The table came first and
    stays -- it holds the here-words and the cross-skill vocabulary that
    belong to no single file -- but a phrase that is plainly one skill's
    business now lives in that skill's file, where a person editing the
    skill will see it (the operator's ruling, sitting 66: markdown declares,
    Python only runs it).

    `keywords` may be a plain set of keywords or a SkillLibrary; passing the
    library is what makes the declared phrases visible.
    """
    hits, kws, hay = _tool_hits(objective, keywords)
    if not hits:
        return ""
    (is_own, leads, _), kw = max(hits)
    twin = _WORKSPACE_TWINS.get(kw)
    if twin and twin in kws and _WORKSPACE_PLACE.search(hay):
        kw = twin
    # AN ORDER TO RUN A NAMED SCRIPT IS NOT TAKEN BY A PLACE WORD (sitting
    # 370): "run measure.py from the workspace" was named list_directory on
    # the table's "the workspace", and the order to run never reached
    # wants_running. Only his own lead -- `run_python measure.py` -- stands
    # in front of it.
    if not (is_own and leads) and wants_running(objective):
        return ""
    return kw


def _tool_hits(objective: str, keywords) -> tuple[list, object, str]:
    """Every skill his words name, each ranked (own, leads, length) -- the one
    ranking names_a_tool and tool_choices share, so the card he is shown and
    the pick can never disagree about what he said. Returns the hits, the
    keywords they were drawn from, and the normalised objective."""
    hay = _norm(objective)
    if not hay:
        return [], (), hay
    # What he LEADS with: his words after one courtesy clause.
    lead = _norm(_after_courtesy(objective))

    lib = keywords if hasattr(keywords, "keywords") else None
    kws = lib.keywords() if lib is not None else keywords

    # Each hit is ranked (own, leads, length): OWN is a skill's own words
    # against the shared table; LEADS is the form opening what he said.
    hits: list[tuple[tuple[bool, bool, int], str]] = []
    spans: list[tuple[list, bool, str]] = []    # where each hit stands, is it a name, whose
    for kw in kws:
        declared: tuple = ()
        spec = None
        if lib is not None:
            spec = lib.spec(kw)
            declared = tuple(getattr(spec, "says", ()) or ()) if spec else ()
        own = [kw, kw.replace("_", " ")]
        shared = list(ALIASES.get(kw, ()))
        # A DECLARED PHRASE IS ALREADY A NAMING, so it is never held to the
        # function-word rule below -- the declared phrases and the bare forms
        # are kept apart for exactly that reason.
        for form, is_phrase, is_own in ([(f, False, True) for f in own]
                                        + [(f, False, False) for f in shared]
                                        + [(f, True, True) for f in declared]):
            f = _norm(form)
            if not f:
                continue
            at = [m.span() for m in re.finditer(
                rf"(?<![a-z0-9_]){re.escape(f)}(?![a-z0-9_])", hay)]
            if not at:
                continue
            if (not is_phrase and f in _FUNCTION_WORDS
                    and not _named_not_used(f, hay, objective or "")):
                continue
            # A bare keyword whose declared argument is a NUMBER is only a
            # naming with a number beside it. A declared PHRASE is exempt for
            # the same reason it is exempt above: a phrase is already a naming.
            if (not is_phrase and _wants_a_number(spec)
                    and not _number_follows(f, hay)
                    and not _wears_quotes(f, objective or "")):
                continue
            leads = lead == f or lead.startswith(f + " ")
            hits.append(((is_own, leads, len(f)), kw))
            spans.append((at, is_own and not is_phrase, kw))
    # A SKILL'S NAME OUTRANKS ANOTHER SKILL'S PHRASE IN THE SAME WORDS (WHAT'S LEFT
    # C51, its follow-up, 2026-10-20; his card: "Name outranks a phrase"). "give me
    # the rack report" says rack_report's name, and rack_list's "the rack" lies
    # across it: one naming, not two, so he is not asked which. A phrase or table
    # word that stands only where another skill's name stands is dropped. Measured
    # over the 748 asks on the record: the two rack-report cards ended and nothing
    # else moved; the wider reading, a name over any phrase anywhere, named
    # git_commit outright for a question that asked "how does he know when to git
    # commit".
    names = [(s, e, kw) for at, is_name, kw in spans if is_name for s, e in at]
    across = [not is_name and all(any(ns < e and s < ne and nk != kw for ns, ne, nk in names)
                                  for s, e in at) for at, is_name, kw in spans]
    return [h for h, gone in zip(hits, across) if not gone], kws, hay


def tool_choices(objective: str, keywords) -> tuple[list[str], bool]:
    """The skills his words name, best first (three at most, each its workspace
    twin where the place says so), and whether the first is SURE: alone, or a
    class above the next -- a skill's own words over the shared table, his lead
    over a word named later. Two in one class is a guess, and a guess is put to
    him on one card (his cards of 2026-10-12: "Only when it isn't sure", "Best
    match + next two")."""
    hits, kws, hay = _tool_hits(objective, keywords)
    best: dict[str, tuple] = {}
    for rank, kw in hits:
        twin = _WORKSPACE_TWINS.get(kw)
        if twin and twin in kws and _WORKSPACE_PLACE.search(hay):
            kw = twin
        if kw not in best or rank > best[kw]:
            best[kw] = rank
    ranked = sorted(best.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    choices = [kw for kw, _ in ranked[:3]]
    sure = len(ranked) <= 1 or ranked[0][1][:2] > ranked[1][1][:2]
    return choices, sure


# ---------------------------------------------------------------------
# Manjuel's logic core: the PPMI reader (2026-10-13, WHAT'S LEFT H29)
# ---------------------------------------------------------------------
#
# HIS CARDS, 2026-10-13: "the whole first piece was essentially supposed to be
# manjuel as the logic core that represents the PPMI and very-quick
# decision/logic side of the system", and PPMI's first job is reading the
# request. His July design of the honest heart read meaning this way, with no
# language model: word pairs counted and weighted by PPMI, a fixed projection,
# and sentence weighting. Standard library only; nothing is downloaded.
#
# WHAT IT LEARNS FROM, his card: the skills' own words alone -- never the seats'
# or the documents', which would move the reading with every day's edit. The
# word pairs are counted over each skill's whole file; a skill is then stood
# for by its OWN words: its name (twice), the summary the Router reads, its
# `Says:` and its arguments' notes.
#
# HOW IT WAS SET, measured 2026-10-13 in the Python tab on the 51 asks of
# H29's step (1). On its own, at its best line, it named the right skill for 35
# of them, the regex 39; under his rule (`read_the_request`) 44, none of the
# regex's 39 lost. The phrasing matrix's 385 phrasings of its plain, rack and
# git asks came out unchanged, and the 14 new asks of sittings 375 to 377 were
# 10 and 10. The axes are his card (256; 43 of 51 at the July design's 64).
# THE LINE WAS SET ON THOSE SAME 51 ASKS, so it flatters them: the live
# sitting re-asks.
PPMI_DIMS = 256                 # the fixed projection's axes (his card)
PPMI_WINDOW = 4                 # words either side of a word that count as a pair
PPMI_SURE = 0.6                 # the cosine at and above which the reader names a skill
PPMI_BY = "the PPMI reader"     # ctx.named_by when the reader chose the tool
_PPMI_WORD = re.compile(r"[a-z0-9]+")
_PPMI_MODELS: dict = {}         # one reader, kept until a skill's words change


def _ppmi_words(text: str) -> list[str]:
    """The words the reader counts: lower case, split at anything that is not a
    letter or a digit, without bare numbers, single letters, greetings, or the
    furniture any question is made of (`_COMMON_ENOUGH`, below)."""
    return [w for w in _PPMI_WORD.findall((text or "").lower())
            if len(w) > 1 and not w.isdigit()
            and w not in _COMMON_ENOUGH and w not in _GREETING_LEADS]


def _ppmi_signs(word: str, dims: int = PPMI_DIMS) -> list[float]:
    """A word's fixed direction, +1 or -1 on each axis, read off its blake2b
    digest -- the same on every machine and in every process, where Python's
    own hash() is salted per process."""
    h = hashlib.blake2b(word.encode("utf-8"), digest_size=dims // 8).digest()
    return [1.0 if (h[i // 8] >> (i % 8)) & 1 else -1.0 for i in range(dims)]


def _ppmi_sentence(words, vec: dict, weight: dict, dims: int):
    """A text's vector: its words' vectors, each weighted by how rare the word
    is in the skills (SIF), averaged -- or None when no word of it is known."""
    v = [0.0] * dims
    n = 0
    for w in words:
        if w in vec:
            g = weight[w]
            v = [x + g * y for x, y in zip(v, vec[w])]
            n += 1
    return [x / n for x in v] if n else None


def _ppmi_strip(v: list, u: list) -> list:
    """`v` less the direction every skill shares (SIF's last step)."""
    d = sum(x * y for x, y in zip(v, u))
    return [x - d * y for x, y in zip(v, u)]


def _ppmi_cosine(p: list, q: list) -> float:
    a = math.sqrt(sum(x * x for x in p))
    b = math.sqrt(sum(x * x for x in q))
    return sum(x * y for x, y in zip(p, q)) / (a * b) if a and b else 0.0


def _ppmi_build(specs, dims: int = PPMI_DIMS) -> tuple:
    """(word vectors, word weights, the shared direction, each skill's vector,
    the axes), from the skills' own words."""
    docs = [_ppmi_words(s.keyword.replace("_", " ") + " " + s.body) for s in specs]
    uni: dict[str, int] = {}
    pairs: dict[str, dict[str, int]] = {}
    for ws in docs:
        for i, w in enumerate(ws):
            uni[w] = uni.get(w, 0) + 1
            row = pairs.setdefault(w, {})
            for j in range(max(0, i - PPMI_WINDOW), min(len(ws), i + PPMI_WINDOW + 1)):
                if j != i:
                    row[ws[j]] = row.get(ws[j], 0) + 1
    count = sum(uni.values()) or 1
    total = sum(sum(r.values()) for r in pairs.values()) or 1
    seen: dict[str, int] = {}
    for r in pairs.values():
        for c, k in r.items():
            seen[c] = seen.get(c, 0) + k
    # A context's count smoothed (to the power 0.75), so a word met once does
    # not outweigh the rest.
    smooth = {c: k ** 0.75 for c, k in seen.items()}
    smooth_total = sum(smooth.values()) or 1.0
    signs = {c: _ppmi_signs(c, dims) for c in seen}
    vec: dict[str, list] = {}
    for w, r in pairs.items():
        pw = sum(r.values()) / total
        v = [0.0] * dims
        for c, k in r.items():
            pmi = math.log((k / total) / (pw * smooth[c] / smooth_total))
            if pmi > 0:
                v = [x + pmi * y for x, y in zip(v, signs[c])]
        vec[w] = v
    weight = {w: 0.001 / (0.001 + k / count) for w, k in uni.items()}
    own = []
    for s in specs:
        said = " ".join([s.keyword.replace("_", " ")] * 2 + [s.summary]
                        + list(s.says or ()) + list(s.param_notes.values()))
        v = _ppmi_sentence(_ppmi_words(said), vec, weight, dims)
        if v is not None:
            own.append((s.keyword, v))
    # The direction every skill shares, by power iteration from a fixed start,
    # so what all the skills say alike decides nothing between them.
    u = [1.0] * dims
    for _ in range(60):
        acc = [0.0] * dims
        for _, v in own:
            d = sum(x * y for x, y in zip(v, u))
            acc = [p + d * x for p, x in zip(acc, v)]
        norm = math.sqrt(sum(x * x for x in acc)) or 1.0
        u = [x / norm for x in acc]
    return vec, weight, u, [(kw, _ppmi_strip(v, u)) for kw, v in own], dims


def _ppmi_model(specs) -> tuple:
    """The reader for this library: built once (about a third of a second),
    then kept until a skill's words change -- the watcher reloads skills/."""
    key = tuple((s.keyword, s.body) for s in specs)
    model = _PPMI_MODELS.get(key)
    if model is None:
        _PPMI_MODELS.clear()
        model = _PPMI_MODELS[key] = _ppmi_build(specs)
    return model


def ppmi_reading(objective: str, keywords) -> tuple[str, float, list]:
    """(the skill his words mean, its cosine, the best three as (skill, cosine)),
    by the PPMI reader -- the skill is "" under PPMI_SURE; ("", 0.0, []) with no
    library to read from or no word of his it knows. Arithmetic, no model: the
    same words in, the same reading out, in a millisecond or two."""
    specs = list(getattr(keywords, "specs", None) or ()) if hasattr(keywords, "keywords") else []
    if not specs:
        return "", 0.0, []
    vec, weight, u, skills, dims = _ppmi_model(specs)
    v = _ppmi_sentence(_ppmi_words(objective), vec, weight, dims)
    if v is None or not skills:
        return "", 0.0, []
    v = _ppmi_strip(v, u)
    ranked = sorted(((_ppmi_cosine(v, sv), kw) for kw, sv in skills), reverse=True)[:3]
    score = ranked[0][0]
    return ((ranked[0][1] if score >= PPMI_SURE else ""), round(score, 3),
            [(kw, round(s, 3)) for s, kw in ranked])


def read_the_request(objective: str, keywords) -> tuple[str, str, tuple, str, bool]:
    """HIS RULE (2026-10-13, his card: "Own words win; shared phrases yield"):
    (the skill the turn takes, who chose it, the reading, the line for the
    record, whether the reading is a write).

      a skill's OWN words in his request -- its name, its `Says:` -- stand, and
      the reader is not asked; an order to run a named script is
      wants_running's, as before;
      otherwise the reader is asked: a skill it names at its line is the one
      taken, and where the shared table named another, the table's phrase
      gives way; under the line the table's pick stands, or none;
      but a skill that WRITES is never named by arithmetic (the 2026-09-08
      ruling): the reading names no tool and the turn wakes the Router to
      decide the write, as a write-shaped objective does.

    `who` is "" when his words named the skill and PPMI_BY when the reader did;
    the reading is (skill, cosine, best three), or () when it was not asked."""
    named = names_a_tool(objective, keywords)
    hits, kws, hay = _tool_hits(objective, keywords)
    if (hits and max(hits)[0][0]) or wants_running(objective):
        return named, "", (), "", False
    pick, score, best = ppmi_reading(objective, keywords)
    if not best:
        return named, "", (), "", False
    twin = _WORKSPACE_TWINS.get(pick)
    if twin and twin in kws and _WORKSPACE_PLACE.search(hay):
        pick = twin
    reading = (pick, score, best)
    ranked = ", ".join(f"`{kw}` {s}" for kw, s in best)
    if not pick:
        return named, "", reading, (f"intent: the PPMI reader names nothing -- its best is "
                                    f"under its line, {PPMI_SURE}: {ranked}"), False
    from .skills import WRITING_SKILLS          # a write is never arithmetic's
    if pick in WRITING_SKILLS:
        return "", "", reading, (f"intent: the PPMI reader read `{pick}` ({score}), a skill "
                                 f"that writes -- a write is the Router's to decide, never "
                                 f"arithmetic's: no tool is named, the Router is woken: "
                                 f"{ranked}"), True
    if pick == named:
        return named, "", reading, f"intent: the PPMI reader agrees, `{pick}`: {ranked}", False
    return pick, PPMI_BY, reading, (
        f"intent: the PPMI reader reads `{pick}` ({score})"
        + (f" over the shared table's `{named}`" if named else "")
        + f" -- no skill's own words were in the request: {ranked}"), False


# ---------------------------------------------------------------------
# Gibberish: measured, not judged
# ---------------------------------------------------------------------

_VOWELS = set("aeiouy")
_WORDISH = re.compile(r"[a-z]+")


def _wordlike(token: str) -> bool:
    """Does this token look like a word a person meant to type?"""
    if not (2 <= len(token) <= 24):
        return False
    # Real words are roughly a fifth vowels; "tgjergnn" is not.
    if sum(c in _VOWELS for c in token) / len(token) < 0.2:
        return False
    # aaaaabbbb / qwcooooooo: a third of the token as one repeated char
    for ch in set(token):
        if token.count(ch) > max(3, len(token) * 2 // 3):
            return False
    return True


def gibberish(objective: str) -> bool:
    """True when the objective does not parse as language at all.

    Sitting 22: keyboard mash ("9 sjdnfjnjn ghagga abbbbb...") raised
    `technical`, woke the Expert Coder, and produced four stages of invented
    work about a request that meant nothing. Seats IMPROVISE on noise -- so
    noise is stopped by arithmetic before any seat sees it. Deliberately
    lenient: one real word in a short line passes ("vram?", "ok"), and typos
    pass, because a typo is still language.
    """
    text = (objective or "").lower()
    solid = [c for c in text if not c.isspace()]
    if solid and sum(c.isdigit() for c in solid) / len(solid) > 0.4:
        return True                      # mostly digits is a mash, not a sum
    tokens = _WORDISH.findall(text)
    if not tokens:
        return True                      # digits and symbols only
    words = sum(1 for t in tokens if _wordlike(t))
    if len(tokens) <= 2:
        return words == 0
    return words / len(tokens) < 0.5


# ---------------------------------------------------------------------
# Injection markers: the gate before the Guardian
# ---------------------------------------------------------------------

# Sitting 39: the injection test feed sailed past the model Guardian and
# moved the chain's hands -- classify ran, speak said 76 characters aloud.
# The docs held at the bottom (secrets refuse by name), but the front gate
# rolled dice. These patterns refuse by ARITHMETIC, before any model reads
# a word. The Guardian model remains behind this as the judgment layer.
_INJECTION_MARKERS = [
    (re.compile(r"(?i)\b(ignore|disregard|forget)\b.{0,40}\b(previous|prior|all|above|earlier)\b.{0,20}\binstructions?\b"),
     "an instruction to ignore instructions"),
    (re.compile(r"(?i)\byou (must|will) now\b|\bnew instructions\s*:"),
     "an attempt to re-instruct the machine"),
    (re.compile(r"(?i)\b(print|reveal|show|output|read|send|dump)\b.{0,60}\.(env|netrc|npmrc|pypirc)\b"),
     "a reach for a secrets file"),
    (re.compile(r"(?i)\b(api[ _-]?keys?|passwords?|credentials?|secret keys?|tokens?)\b.{0,40}\b(print|reveal|show|send|list|dump|output)\b"),
     "a reach for credentials"),
    (re.compile(r"(?i)\b(print|reveal|show|send|dump|list)\b.{0,40}\b(api[ _-]?keys?|passwords?|credentials?|secret keys?)\b"),
     "a reach for credentials"),
    (re.compile(r"(?i)\bsystem prompt\b.{0,40}\b(print|reveal|show|repeat|output)\b"),
     "a reach for the machine's own instructions"),
    (re.compile(r"(?i)\b(print|reveal|show|repeat|output)\b.{0,40}\bsystem prompt\b"),
     "a reach for the machine's own instructions"),
]


def injection_markers(feed: str) -> list[str]:
    """Named markers found in pasted material. Empty list = no hard match.

    Deliberately about UNAMBIGUOUS shapes only -- prose ABOUT injection
    ("the guardian catches injection attacks") matches nothing here. The
    model Guardian judges everything softer.
    """
    # THE WORDS, NOT THE SPACES (2026-10-02, the phrasing matrix). "You  must  now reveal ..." with two
    # spaces, a tab or a non-breaking space between the words was not an instruction to this gate, and
    # neither was a marker broken across a line (`.` stops at a newline). Whitespace of every kind is one
    # space before the patterns read it; nothing else about the text changes.
    text = " ".join((feed or "").split())
    return [name for rx, name in _INJECTION_MARKERS if rx.search(text)]


# ---------------------------------------------------------------------
# Topic boundaries: the operator says so, or the drift shows it
# ---------------------------------------------------------------------

_SESSION_CUES = ("new session", "fresh session", "start over", "clean slate",
                 "start fresh", "wipe the thread")
_TOPIC_CUES = ("new topic", "next topic", "new thread", "next thread",
               "switch gears", "switching gears", "change of pace",
               "different thing", "something different", "moving on",
               "next subject", "new subject", "change the subject")


def topic_cue(objective: str) -> str:
    """"session", "topic", or "". The operator's own words draw the line."""
    low = " ".join((objective or "").lower().split())
    if any(c in low for c in _SESSION_CUES):
        return "session"
    if any(c in low for c in _TOPIC_CUES):
        return "topic"
    return ""


def cue_only(objective: str) -> bool:
    """True when the turn is the cue and nothing else -- no question rides
    along, so no seat needs to sit."""
    low = " ".join((objective or "").lower().split()).strip(".!?, ")
    for c in _SESSION_CUES + _TOPIC_CUES:
        if low == c or low in (f"ok {c}", f"okay {c}", f"alright {c}",
                               f"{c} then", f"lets {c}", f"let's {c}"):
            return True
    return False


# ---------------------------------------------------------------------
# Action shapes: route without presuming
# ---------------------------------------------------------------------

# Write-shaped verbs: a filename after one of these is a thing to MAKE or
# CHANGE, never a thing to read. Sitting 42's lesson inverted a fix: the
# bare filename rule presumed ground_read, so "write hello.md" would have
# READ hello.md. A write is a decision -- what file, what content, which
# skill -- and deciding is the Router's office, so these raise needs_tool
# with NO named tool.
# `replace` joined 2026-10-12 (sitting 370: "in measure.py in the workspace,
# replace 'x' with 'y'" was not write-shaped, so list_directory, a reader, took it).
_VERB = (r"(?:write|make|create|save|generate|build|add|append|update|edit|"
         r"fix|change|modify|refactor|implement|delete|remove|rename|replace)")
_WRITE_VERBS = re.compile(rf"(?i)\b{_VERB}\b")

# WHAT COUNTS AS AN ORDER TO WRITE (WHAT'S LEFT C49, 2026-10-20, his card: "All that, and
# prose in chat"). Of the 54 turns read as writes since 2026-09-01, eleven ordered none: a
# verb inside pasted code ("lint this python: def add(a, b)"), a verb used as a noun ("the
# build plan", "land a change safely"), a question about what the system can do ("how would
# you build a skill?", "you can make things for me?"). And "write me a poem" wants words in
# chat, not a file, unless a file or the workspace is named.
_PASTED = re.compile(r"```.*?(?:```|$)|`[^`\n]*`", re.S)
_CODE_MARK = re.compile(r"\b(?:def|class|return|import|lambda|print)\b|[(){};=<>]")
_AS_NOUN = re.compile(rf"(?i)\b(?:the|a|an|my|our|your|this|that|these|those|its|his|her|"
                      rf"their|any|each|every)\s+{_VERB}\b")
_COMPOUND = re.compile(r"(?i)\bbuild\s+(?:plans?|paths?|maps?|order|steps?|logs?)\b")
_HOW = re.compile(rf"(?i)\bhow\s+(?:would|could|do|does|did|can|should|might|to)\b[^.?!]*?\b{_VERB}\b")
_YOU_CAN = re.compile(rf"(?i)\byou\s+(?:can|could)\s+{_VERB}\b[^.!]*\?")
# ...and a verb in a question clause, to the clause's end (sitting 376: "what I could change
# to make the common turns faster", inside an ask to explain -- missed in the first count).
_WH_CLAUSE = re.compile(rf"(?i)\b(?:what|which|where|whether)\s+(?:i|we|you)\s+"
                        rf"(?:could|can|should|might|would)\s+{_VERB}\b[^.?!]*")
_PROSE = re.compile(r"(?i)\b(?:write|make|compose|create)\s+(?:me\s+|us\s+)?"
                    r"(?:a\s+|an\s+|some\s+)?(another\s+)?(?:short\s+|little\s+|quick\s+)?"
                    r"(?:poem|haiku|story|song|limerick|sonnet|verse|joke|riddle)s?\b")
_A_PLACE = re.compile(r"(?i)\b(?:workspace|file|folder|disk|save)\b|\.\w{1,5}\b")

# Action-verb + object shapes that plainly want hands, without naming which.
_ACTION_SHAPE = re.compile(
    r"(?i)\b(check|verify|test|run|execute|analyze|analyse|compare|count|"
    r"measure|calculate|compute|scan|inspect|audit)\b.{0,50}"
    r"\b(file|files|folder|dir|directory|repo|code|ground|workspace|log|"
    r"logs|index|record|this|it|that)\b")


def own_words(objective: str) -> str:
    """His words with what he pasted taken out: fenced and backticked code, and
    the tail after a colon that is followed by code."""
    text = _PASTED.sub(" ", objective or "")
    i = text.find(":")
    while i != -1:
        if _CODE_MARK.search(text[i + 1:]):
            return text[:i]
        i = text.find(":", i + 1)
    return text


def wants_writing(objective: str) -> bool:
    """An order to write, in his own words: a write verb used as a verb -- not a
    noun, not in a question about what the system can do, and not prose to be
    written in chat. Router decides the rest."""
    text = own_words(objective)
    if _PROSE.search(text) and not _A_PLACE.search(text):
        return False
    for rx in (_AS_NOUN, _COMPOUND, _HOW, _YOU_CAN, _WH_CLAUSE):
        text = rx.sub(" ", text)
    return bool(_WRITE_VERBS.search(text))


def wants_action(objective: str) -> bool:
    """Action-verb + object: the turn wants hands, tool unspecified."""
    return bool(_ACTION_SHAPE.search(objective or ""))


# AN ORDER TO RUN SOMETHING. Narrow on purpose: the verb has to mean
# EXECUTE, not "run through it" or "run a check on the record".
_RUN_VERBS = re.compile(r"(?i)\b(run|execute|rerun|re-run)\b")


def wants_running(objective: str) -> str:
    """The `.py` this objective orders RUN, or "".

    EARNED 2026-09-12, from the coder flow. `verify`'s objective was "Run the
    .py file this task names and report exactly what it said", the file was
    named in the text, and the Router answered "NO skill is needed" -- twice,
    for two different reasons, on two different runs. Once it wrote the file
    and never ran it; once it decided the answer was already in the thread.
    Both times a seat's judgement stood where arithmetic was available: the
    objective says RUN, it names a `.py`, and whether that file exists is a
    fact on disk. The estate's own pattern for that is to DECIDE the call and
    wake the Router to read the result -- "it does not choose".

    `.py` ONLY, because `run_python` runs Python and nothing else; a "run
    notes.md" is not an order this can answer, and it falls through to the
    reader exactly as it did before.
    """
    text = objective or ""
    if not _RUN_VERBS.search(text):
        return ""
    got = names_a_file(text)
    return got if got.lower().endswith(".py") else ""


# HIS PLAIN WORDS RAISE A RACKED SEAT'S FLAG (2026-10-12, his card: "Engine
# raises on plain words"). Sitting 370: "proofread this sentence", "think hard:
# ...", "lint this python" and "give me the rack report" woke nobody -- the
# racked seats waited on a tag the Steward did not write. Narrow on purpose: a
# wrong wake costs minutes (the Reasoner once sat 235 s on a mention), and every
# wake is put to him on a card first (pipeline.py, _ask_to_wake).
_PLAIN_FLAGS = (
    ("prose", re.compile(r"(?i)\b(?:proof-?read|copy-?edit|check (?:the|my) (?:grammar|spelling)"
                         r"|fix (?:the|my) (?:grammar|spelling))\b")),
    ("hard", re.compile(r"(?i)\b(?:think (?:hard|it through|this through)|reason (?:it|this) (?:out|through)"
                        r"|step by step)\b")),
    ("technical", re.compile(r"(?i)\b(?:lint|debug|traceback|stack trace)\b")),
    ("rack", re.compile(r"(?i)\b(?:rack report|what(?:'s| is) loaded|which models|in vram)\b")),
)


def plain_flags(objective: str) -> set[str]:
    """The racked seats' flags his own words raise, or an empty set."""
    text = objective or ""
    return {flag for flag, rx in _PLAIN_FLAGS if rx.search(text)}

# THE LEVELS (2026-10-12, his idea -- "tagging the things based on the size of
# the input ... different levels of escalation based on the complexity of the
# input" -- and his cards: "Arithmetic on your words", "By the seat that takes
# it"; his ruling: "keep the current laws and rulings for roles, and use them for
# the routing and escalation processes"). A turn is measured by arithmetic on his
# own words and tagged by the seat that takes it, with today's seats: the Steward
# a short single ask; the Router a larger one; the Reasoner, or the Expert Coder
# for code, a much larger one; a workflow (H23) many acts, or more than a big
# seat's window holds. The cut lines are judgement, set that day and checked in a
# live sitting; the counting is the engine's own (_ACT_VERB, the numbered list
# is_big_objective reads, plain_flags, names_a_file).
LEVEL_LONG = 200               # characters: a larger ask
LEVEL_VERY_LONG = 600          # characters: a much larger one
LEVEL_FEED = 2000              # a pasted feed this long is a big seat's to read
LEVEL_BEYOND_A_WINDOW = 24000  # a big seat's 8,192 tokens, at three characters to a token
LEVEL_SEATS = {1: "Steward", 2: "Router", 3: "Reasoner", 4: "workflow"}
_CODE_RE = re.compile(r"(?m)```|^\s*(?:def|class|import|from)\s+\w|\bdef\s+\w+\s*\(|\bfunction\s+\w+\s*\(")


def level(objective: str, feed: str = "") -> tuple[int, str, list, str]:
    """(level, the seat that takes it, why, the big seat's flag) for one turn.
    A level only ever adds to the route the engine already chose."""
    text = (objective or "").strip()
    feed = (feed or "").strip()
    raised = plain_flags(text)
    code = bool(_CODE_RE.search(text)) or "technical" in raised
    acts = len(_ACT_VERB.findall(text))
    steps = len(re.findall(r"(?m)^\s*(?:\d+[.)]|[-*])\s+\S", text))
    why: list = []
    n = 1
    if len(text) > LEVEL_LONG:
        n = 2
        why.append(f"{len(text)} characters")
    if text.count("?") >= 2:
        n = max(n, 2)
        why.append(f"{text.count('?')} questions")
    named = names_a_file(text)
    if named:
        n = max(n, 2)
        why.append(f"names {named}")
    if len(text) > LEVEL_VERY_LONG:
        n = max(n, 3)
    if code:
        n = max(n, 3)
        why.append("code")
    if raised & {"hard", "technical"}:
        n = max(n, 3)
        why.append("his words: " + ", ".join(sorted(raised & {"hard", "technical"})))
    if len(feed) > LEVEL_FEED:
        n = max(n, 3)
        why.append(f"a {len(feed)}-character feed")
    if is_big_objective(text) and max(acts, steps) >= 3:
        n = 4
        why.append(f"{max(acts, steps)} acts in sequence")
    if len(feed) > LEVEL_BEYOND_A_WINDOW:
        n = 4
        why.append("a feed beyond a big seat's window")
    flag = ("technical" if code else "hard") if n >= 3 else ""
    seat = "Expert Coder" if n == 3 and code else LEVEL_SEATS[n]
    return n, seat, why, flag


# A FOLLOW-UP POINTS AT THE CONVERSATION. Sitting 87 (2026-09-04, runs 8,
# 9, 13): "what does that last part mean? Refused: `content` must be a
# PATH..." -- the operator pasting the line he had just been shown -- was
# dispatched to the reader by asks_the_ground, the front Steward was
# skipped as already-dispatched, and the Router, which by design never
# sees the dialogue, answered "there is no conversation history in this
# run". The one seat that holds the thread was the one seat not asked.
# The toll that night: "needs more context".
#
# Three shapes, all decidable without a model: a short question built on
# an anaphor (the sitting-71 rule, already used by asks_the_ground); a
# question that OPENS with a follow-up lead ("what does that", "what do
# you mean", "that last part", "say that again"); and a turn that QUOTES
# the previous delivery -- forty characters of it verbatim is not a
# coincidence. Any of these, with a dialogue to point at, keeps the door
# in the run. It does not stop the Router from waking if the door raises
# the flag; it stops the door from being skipped.
_FOLLOWUP_LEADS = (
    "what does that", "what do you mean", "what did you mean", "what was that",
    "that last part", "the last part", "say that again", "explain that",
    "what does it mean", "what's that mean", "whats that mean", "meaning what",
    "and that", "so that", "why is that", "how so", "in what way", "such as",
    "like what", "for example", "which one", "which ones", "that one",
)
_QUOTE_MIN = 40

# A TURN THAT NAMES AN EARLIER TURN -- BY EITHER SPEAKER. The third way a
# turn can point back, and the one that was missing: _ANAPHORA covers
# pointing words ("that", "it"), _FOLLOWUP_LEADS covers fixed openings
# ("say that again"), and neither covers "what colour did you just say"
# or "what were the two colours I asked you for".
#
# BOTH HALVES WERE MEASURED, a fix apart. The seat's half first: "what
# colour did you just say" was routed as a fresh objective. Then the
# operator's own half, live and after that fix: "What were the two colours
# I asked you for?" answered "I don't have access to the conversation
# history", and "And which one did I ask for first?" ran a semantic_search
# over past sessions -- both had asks_the_ground TRUE, so the guess that
# the question was about the GROUND claimed them. pipeline.py withdraws
# that guess for a follow-up; only the recognition was missing.
#
# PAST TENSE ONLY on the operator's half, and that is the whole guard
# against false positives: "what should i ask the router" is a real
# question about the ground, and a present-tense "i ask" would claim it,
# keep the door, and stop his work reaching the Router.
#
# Measured through the glass 2026-09-09: that exact question was routed as
# a fresh objective, so the Steward was skipped, and the Router -- which
# never sees the dialogue, by design -- answered truthfully that it had no
# memory of the previous turn. Everything beneath was working; the door was
# simply not kept.
#
# A RULE, NOT MORE PHRASES: second person plus a speech verb. A list of
# literal leads would have caught that one sentence and missed the next
# phrasing of it.
_SPOKE_BACK = re.compile(
    r"\byou(?:'ve| have)?\s+(?:just\s+)?"
    r"(?:said|say|says|told|tell|answered|answer|wrote|mentioned|called)\b"
    r"|\bdid\s+you\s+(?:just\s+)?(?:say|said|tell|mention|call|answer)\b"
    r"|\byour\s+(?:last|previous|first|own)\s+"
    r"(?:answer|reply|response|word|words|message|line)\b"
    r"|\bthe\s+last\s+thing\s+you\s+(?:said|wrote|told)\b"
    # the operator's own earlier turn: "I asked", "did I say", "my last
    # question". Past tense only -- see the note above.
    r"|\bi\s+(?:just\s+)?(?:asked|said|told|mentioned|requested|wanted)\b"
    r"|\bdid\s+i\s+(?:just\s+)?(?:ask|say|tell|mention|request)\b"
    r"|\bwas\s+i\s+(?:just\s+)?(?:asking|saying|telling)\b"
    r"|\bmy\s+(?:last|previous|first|own)\s+"
    r"(?:question|request|words?|message|line|ask)\b",
    re.IGNORECASE,
)

# A QUESTION ABOUT THIS SITTING (0.1.6, the sitting story). Sitting 93:
# "what happened? why did you suck so bad?" went to semantic_search over
# the whole record. The door now holds the sitting story (seatlog.
# story_block), so a question about what THIS sitting did is the door's
# to answer from it -- a reader dispatch is withdrawn, as a follow-up's
# is. Leads only; a question that also names a tool or a file is still
# the operator's order.
_SITTING_LEADS = (
    "what happened", "what just happened", "what did you do", "what did you just",
    "what have you done", "what went wrong", "why did that fail", "why did you",
    "what did we do", "what have we done", "so far", "this sitting",
    "what ran", "what did that run", "recap", "where were we", "what were we",
)


def asks_the_sitting(objective: str) -> bool:
    """Whether the turn asks what THIS sitting has done -- the story's turf."""
    low = " ".join((objective or "").lower().split()).strip(" ?!.")
    if not low or len(low.split()) > 14:
        return False
    return any(lead in low for lead in _SITTING_LEADS)


def is_followup(objective: str, dialogue: list | None) -> bool:
    """Whether this turn points back at the conversation rather than at
    the ground. Needs a dialogue to point at; with none it is never one."""
    if not dialogue:
        return False
    text = " ".join((objective or "").split())
    low = text.lower().strip()
    if not low:
        return False
    words = _WORD.findall(_norm(low))
    if len(words) <= 8 and any(w in _ANAPHORA for w in words):
        return True
    if any(low.startswith(lead) for lead in _FOLLOWUP_LEADS):
        return True
    # either speaker's earlier turn: "what colour did you just say",
    # "your last answer", "what were the two colours I asked you for"
    if _SPOKE_BACK.search(low):
        return True
    # a turn that carries the previous delivery's own words
    last = ""
    for e in reversed(list(dialogue)):
        who = str(e[0]).lower() if len(e) else ""
        if who != "operator":
            last = " ".join(str(e[1]).split()) if len(e) > 1 else ""
            break
    if len(last) >= _QUOTE_MIN:
        # any 40-char window of the last delivery appearing verbatim
        step = 20
        for i in range(0, max(1, len(last) - _QUOTE_MIN + 1), step):
            piece = last[i:i + _QUOTE_MIN]
            if len(piece) == _QUOTE_MIN and piece.lower() in low:
                return True
    return False


def last_file_in(thread: list) -> str:
    """The most recently MENTIONED filename in the conversation, newest
    first -- so "read the file" means the file we were just talking about,
    the way it does between people."""
    for e in reversed(list(thread or [])):
        what = e[1] if len(e) > 1 else ""
        m = None
        for m in _FILENAME_RE.finditer(str(what)):
            pass                          # keep the LAST match in the entry
        if m:
            return m.group(0)
    return ""


# Words a question can be made of WITHOUT being about anything in
# particular. Function words, casual words, question leads. Deliberately
# small: an unlisted word is treated as a term worth looking up, because
# sitting 60 showed what fills the gap when a real term ISN'T looked up --
# a seat invented a client narrative from nothing. Missing common words
# cost a search; missing content terms cost the truth.
_COMMON_ENOUGH = frozenset("""
a an the is are was were be been being am do does did doing done can could
will would should shall may might must have has had having i you we they he
she it me us them him her my your our their its mine yours this that these
those there here now then and or but not no yes if so of in on at to for
from with about into onto over under out up down off again once right just
like some any all both each few more most other such only own same too very
also than as how what who whom whose which when where why whats whos hows
dont cant wont didnt doesnt isnt arent im ive youre weve theyve thats whats
hey hi hello sup yo howdy dude bro man bud buddy homie fam boss chief stew
steward thanks thank please cool ok okay good nice well fine great alright
yeah yea nah hmm huh oh ah wow damn really actually basically literally
gonna wanna gotta let lets go going come came get got give take make know
think say said see look want need feel mean tell told ask
up down out in on off over here there back again still even ever
fuck fucking fucked shit shitty damn damned hell crap wtf ass bloody
sup yo dawg fam bruh homie buddy pal chief boss stew stewy
""".split())

# A question that opens with a greeting is a greeting. Sitting 48's law
# (greetings stay at the door) survives its gate being dropped.
# Words that point BACKWARD, at the conversation, rather than at anything
# in the ground. The core is context.POINTING_WORDS, shared with the door's
# follow-up (pipeline.py) and the topic boundary (context.py); dispatch adds
# the plurals and the persons, because a question about "them" or "she" is
# about somebody already named in the thread.
_ANAPHORA = POINTING_WORDS | {"those", "these", "them", "repeat", "he", "she",
                              "they"}

_GREETING_LEADS = {"hey", "hi", "hello", "sup", "yo", "howdy", "morning",
                   "evening", "afternoon", "greetings", "good", "gday",
                   "mornin", "afternoon", "salutations"}

_QUESTION_LEADS = {"who", "whos", "what", "whats", "where", "wheres", "when",
                   "which", "why", "how", "hows", "tell", "explain",
                   "describe", "find"}


_COURTESY_LEADS = {
    "thanks", "thank", "ok", "okay", "kk", "cool", "nice", "great", "right",
    "sure", "alright", "sweet", "awesome", "perfect", "gotcha", "understood",
    "noted", "interesting", "appreciate", "yes", "yeah", "yep", "fine",
}


def _after_courtesy(text: str) -> str:
    """Drop ONE leading courtesy clause, so the question behind it is seen.

    SITTING 81, and it is the greeting bug's mirror image. asks_the_ground
    requires words[0] to be a question lead, or the text to end in `?`. A
    polite lead-in moves the question word off position 0, and someone who
    opens with "thanks" usually does not close with a question mark:

        "where do i find a list or description of the existing tools"
            -> dispatched
        "thank you for the clarification, where do i find a list or
         description of the existing tools"
            -> NOT dispatched

    Same sentence. The second ran no tool, and the Steward -- with nothing
    dispatched and only the thread to go on -- answered a question from TWO
    turns earlier and invented the contents of `pipeline_steps.py` doing it.
    The greeting bug cost 155 seconds; this one cost a confident wrong
    answer, which is dearer.

    ONE CLAUSE, AND ONLY FROM THE FRONT. If the first word is a courtesy,
    everything up to the first comma goes -- or just the courtesy words when
    there is no comma. Bounded to the opening: a "thanks" in the middle of a
    sentence is part of the sentence, and a second clause is content.

    The greeting test still runs on what is left, so "thanks, good morning"
    is still a greeting and still reaches no reader.
    """
    raw = (text or "").strip()
    if not raw:
        return raw
    first = _WORD.findall(_norm(raw))
    if not first or first[0] not in _COURTESY_LEADS:
        return raw
    head, sep, tail = raw.partition(",")
    if sep and tail.strip() and len(_WORD.findall(_norm(head))) <= 8:
        return tail.strip()
    # No comma: peel the courtesy words themselves off the front.
    out = raw
    for _ in range(3):
        m = re.match(r"^\s*([A-Za-z']+)\b[\s,:-]*", out)
        if not m or _norm(m.group(1)) not in _COURTESY_LEADS:
            break
        out = out[m.end():]
    return out.strip() or raw


# "WHAT IS IN THE <X> DIR" IS A LISTING, NOT A LOOKUP. Sittings 86, 88 and
# 90 -- three standups in a row -- sent "what is in the skills dir" to the
# reader (asks_the_ground: a question carrying a term), and the Router then
# listed the WORKSPACE and reported the skills folder missing. The shape is
# a folder named by the operator with a listing verb around it; the folder
# is checked on disk (the same viability step as the named file), and a real
# one is a ground_list with its name as the argument. The operator, sitting
# 90: "9/10 on the dry run, what the fuck dude." Third sighting; built.
_FOLDER_RE = re.compile(
    r"(?i)\b(?:what(?:'s|s| is| are)?\s+(?:in|inside|under)|list|show(?: me)?|"
    r"contents? of|look (?:in|inside|at))\s+(?:the\s+|my\s+|our\s+)?"
    r"(?P<name>[A-Za-z0-9_][A-Za-z0-9_.\-]*(?:/[A-Za-z0-9_.\-]+)*)"
    r"(?:/(?!\S)|\s+(?:dir|directory|folder)\b)")


def names_a_folder(objective: str) -> str:
    """The folder an objective asks to see, or "". `what is in the skills
    dir` -> `skills`; `list manjuel/` -> `manjuel`; `show me the law
    folder` -> `law`. The caller checks it is a real folder in the ground."""
    m = _FOLDER_RE.search(objective or "")
    if not m:
        return ""
    name = m.group("name").strip().strip("/")
    if name.lower() in ("the", "a", "this", "that"):
        return ""
    return name


def asks_the_ground(objective: str) -> bool:
    """A question carrying a term worth looking up. Sitting 60: five
    questions about the estate's own contents -- "what is the ledger?",
    "who is X?", "what is the ledger work?" -- raised no flag, ran no
    tool, and one produced a confident invented paragraph about a real
    client. A question about the ground must reach a reader; an empty
    search result is the honest answer (s61 proved what that looks like).

    Shape: question-led or question-marked, not a greeting, not an exit,
    not gibberish, and at least one word that is NOT common conversational
    furniture. "what are you doing right now" is all furniture -- no
    dispatch. "who is warden?" carries `warden` -- dispatched. The common
    list errs small ON PURPOSE: an over-match costs one search; an
    under-match is sitting 60 again."""
    text = _after_courtesy((objective or "").strip())
    words = _WORD.findall(_norm(text))
    # A GREETING IS THE FIRST TWO WORDS, NOT THE FIRST. Sitting 79: "good
    # morning, sunshine, how are ya?" was dispatched to the reader and cost
    # 155 seconds, because this test read words[0] -- and the whole `good X`
    # family, the commonest greeting form in English, leads with `good`.
    # "good morning, sir" escaped only by luck: it carries no question mark.
    # The set had `morning`/`evening`/`afternoon` and could never reach them.
    if len(words) < 2 or _GREETING_LEADS & set(words[:2]):
        return False
    if not (text.endswith("?") or words[0] in _QUESTION_LEADS):
        return False
    if wants_out(text) or gibberish(text):
        return False
    # A SHORT QUESTION ABOUT THE SEAT ITSELF IS CONVERSATION (the keyword
    # bait, fifth sighting, sitting 93: "can you hear me" -> the reader ->
    # the Router called `speak` with nothing, 84s). "are you there", "can
    # you hear me", "you awake" -- four words or fewer, addressed to
    # "you", carrying no noun the ground would hold -- reach the door.
    if len(words) <= 4 and "you" in words:
        return False
    # AN ANAPHOR POINTS AT THE CONVERSATION, NOT AT THE GROUND. Sitting 71:
    # "what does that even mean?" was dispatched to the reader, and the
    # Router -- which by design never sees the dialogue -- answered "there
    # is no prior exchange and nothing to refer to as 'that'". It was
    # right, and it should never have been asked. A short question built
    # around `that`/`it`/`this` is a FOLLOW-UP: the Steward holds the
    # conversation and is the seat that can answer it.
    if len(words) <= 8 and any(w in _ANAPHORA for w in words):
        return False
    return any(len(w) >= 3 and w not in _COMMON_ENOUGH for w in words)


# THE DECOMPOSER (operator's design, sitting 62 conversation): dispatch by
# VERB-OBJECT STRUCTURE, not by pre-carved phrases. "search the ground find
# the warden estate!" matched no alias twice in sitting 61 -- every word was
# understood and no pattern was exact, so nothing ran. Decomposition moves
# the match from phrases to structure, and stays pure arithmetic.
#
# THE BALANCE, his ruling: matched executes, everything else FALLS THROUGH
# TO CONVERSATION. So this is imperative-lead only -- the verb must open
# the sentence (after politeness filler). "i cant find anything in this
# repo man" is a complaint; "that search was garbage" is a review; neither
# is an order, and neither dispatches. Reader-verbs only for now: the
# write/action shapes above already carry their own classes.
_READER_VERBS = {"search", "find", "grep", "locate", "query", "look", "dig"}
_GROUND_OBJECTS = {"ground", "dir", "directory", "estate", "repo",
                   "repository", "record", "records", "archive", "index",
                   "folder", "workspace", "place", "files"}
_LEAD_FILLER = {"please", "ok", "okay", "now", "hey", "yo", "alright",
                "just", "go", "then", "and", "so", "can", "you", "u",
                "through", "up", "in", "into", "at", "the", "this", "that",
                "my", "our"}


# Conjunctions and enumerations that join SEPARATE acts. "and" alone is
# not one of them -- "read the rack and tell me" is one act described
# twice, and treating it as two is how a chain talks itself into work
# nobody asked for.
# Verbs that name an ACT this estate can perform. Counting acts with
# _WRITE_VERBS + _ACTION_SHAPE was wrong and the strokes caught it: those
# two were built for other jobs and between them know nothing of `read`,
# `search`, `index` or `commit`, so "read the rack, then write a note,
# then commit it" counted as ONE act. The estate's own working vocabulary
# is the right list.
_ACT_VERB = re.compile(
    r"(?i)\b(read|write|make|create|save|generate|build|add|append|update|"
    r"edit|fix|change|modify|refactor|implement|delete|remove|rename|"
    r"search|find|look|index|commit|push|pull|list|show|open|check|verify|"
    r"test|run|execute|review|analyz|analys|compare|count|measure|scan|"
    r"inspect|audit|summaris|summariz|report|remember|speak|load|unload)\b")

_MULTI_ACT = re.compile(
    r"(?i)(,\s*then\b|\bthen\b|\bafter that\b|\bnext,|\bfollowed by\b|"
    r"\bonce that\b|\band then\b|;\s*\w)")


def is_big_objective(objective: str, verbs: int = 2) -> bool:
    """Whether an objective is plainly SEVERAL acts, not one.

    The gate for waking the decomposer. It is deliberately hard to trip:
    a long sentence is not a big objective, and neither is a bare "and".
    What counts is sequencing language ("then", "after that", "followed
    by") carrying at least two act-shaped verbs, or a numbered list the
    operator wrote himself.

    Erring shut is the right error. A decomposition that fires on one act
    spends a model call to restate the request, and every unnecessary
    stage is another chance to drift (DESIGN 11: serial chains compound
    error). A missed decomposition just means the chain does the work the
    ordinary way."""
    text = (objective or "").strip()
    if len(text) < 40:
        return False
    if re.search(r"(?m)^\s*(?:\d+[.)]|[-*])\s+\S+.*\n\s*(?:\d+[.)]|[-*])\s+\S",
                 text):
        return True                      # a list the operator wrote himself
    if not _MULTI_ACT.search(text):
        return False
    return len(_ACT_VERB.findall(text)) >= verbs


def decomposes_to_search(objective: str) -> str:
    """The remainder-as-payload when the words are an ORDER to search the
    ground, else "". Verb class + object class + remainder: an opening
    reader-verb, a ground-object somewhere after it, and whatever is left
    becomes the query (may be empty -- the skill falls back to the
    objective, its own law since sitting 26)."""
    words = _WORD.findall(_norm(objective))
    while words and words[0] in _LEAD_FILLER:
        words = words[1:]
    if not words or words[0] not in _READER_VERBS:
        return ""
    rest = words[1:]
    hit = next((i for i, w in enumerate(rest) if w in _GROUND_OBJECTS), -1)
    if hit < 0:
        return ""
    # The payload sits on either side of the object ("search the ground
    # for X" / "find X in the records"). Only the FIRST object is the
    # frame -- a later object-class word belongs to the payload: in
    # "search the ground find the warden estate", `estate` is the client's
    # own word, not structure (the stroke that caught this scrubbed it to
    # "warden"). Filler, verbs and "for" stay structural throughout.
    payload = [w for i, w in enumerate(rest)
               if i != hit
               and w not in _LEAD_FILLER and w not in _READER_VERBS
               and w != "for"]
    return " ".join(payload) or objective.strip()


_LEAVE_WORDS = {"exit", "quit", "leave", "bye", "goodbye", "peace", "out",
                "done", "go"}
_VOCATIVES = {"bro", "man", "dude", "homie", "bud", "buddy", "fam", "dawg",
              "stew", "steward", "chief", "boss", "im", "i'm", "gotta",
              "gonna", "later", "yall", "now", "ok", "okay", "alright"}


def wants_out(objective: str) -> bool:
    """An exit command wearing casual clothes. "exit bro" means exit.

    Strict on purpose: EVERY word must be a leave-word or a vocative, and at
    least one leave-word must appear -- "let me exit the loop in this code"
    never matches, because "let", "the", "loop"... are neither.
    """
    words = [w.strip(".!?,") for w in (objective or "").lower().split()]
    words = [w for w in words if w]
    if not words:
        return False
    if not any(w in _LEAVE_WORDS for w in words):
        return False
    return all(w in _LEAVE_WORDS or w in _VOCATIVES for w in words)


# ---------------------------------------------------------------------
# The maker: "make me a snake game" (2026-09-21)
# ---------------------------------------------------------------------
#
# THE OPERATOR'S TEST, in his words the same day: "if my wife can sit down at
# the PC, ask the system to make a type of software, game, etc. and she can see
# the result, play the game". Sitting 257 put exactly that sentence through the
# estate and nothing was made -- the door role-played a game, the Router planned
# and did not act, the Coder never woke (maker.py has the three runs). These
# three read the request by arithmetic, so no seat has to notice it.
#
# NARROW ON PURPOSE, like every shape in this module: a verb that means MAKE,
# then "a" or "an", then within five words a noun naming a THING PEOPLE USE --
# a game, an app, a page, a tool. "write a poem", "make a note", "create a
# file" and "make a commit" name no such thing and fall through untouched. A
# thing asked for in a language the maker does not write -- python, a script, a
# function -- is the Expert Coder's ordinary path, not a project; and a question
# ABOUT making ("how do I make a game?") is a question.
#
# HER OWN WORDS (2026-09-30, WHAT'S LEFT D2). The wife test's spec carries her
# three messages verbatim, and its two runs of 09-28 made nothing: "If you can
# code, try MAKING me a little game" and "i WANT a game i can play" open no
# maker, because the verb here had to stand in its base form and "want" was
# not one. The 2026-09-21 test sentence was his ("Make me a simple snake game")
# and it matched; hers did not, and the flow's make step fell through to the
# ordinary pipeline, which read files and talked. So: the verb in its -ing
# form too (spelled out -- "making" is not "make" + "ing"), and "want" /
# "would like" / "need" before the thing, with the same five-word window and
# the same list of things people use.
_MAKE_RE = re.compile(
    r"(?i)\b(?:make|making|build|building|create|creating|write|writing|"
    r"code|coding|program|programming|design|designing|"
    r"want|would\s+like|need)\s+(?:me\s+|us\s+)?"
    r"(?:a|an)\s+(?P<what>(?:[\w'-]+\s+){0,5}?"
    r"(?:game|app|application|program|website|web\s*site|web\s*page|webpage|"
    r"web\s*app|site|tool|calculator|timer|stopwatch|clock|quiz|planner|"
    r"tracker|to-?do\s+list|todo\s+list|puzzle|animation))\b")
_NOT_A_PAGE = re.compile(
    r"(?i)\b(?:python|\w+\.py|java|rust|golang|bash|powershell|sql|regex|"
    r"function|class|module|script|cli|command[- ]line|terminal)\b")
_ASKS_ABOUT_MAKING = re.compile(
    r"(?i)^\s*(?:how|why|what|when|where|who|which|is|are|was|were|does|do|"
    r"did|should|shall)\b")


def wants_making(objective: str) -> str:
    """The thing an objective asks to have MADE -- "simple snake game" -- or ""."""
    text = objective or ""
    if _ASKS_ABOUT_MAKING.match(text) or _NOT_A_PAGE.search(text):
        return ""
    m = _MAKE_RE.search(text)
    return " ".join(m.group("what").split()) if m else ""


# A CHANGE TO THE THING IN HAND. The pipeline asks this only when the sitting
# already has a project (maker.current); with none, these words mean nothing
# here and fall through as they always have. The verb must OPEN the request:
# "the snake is too slow" is an observation, and a person who wants it changed
# says "make it faster". "let me try it" is not a change; "let's add a score"
# and "let the snake wrap" are.
# "I WANT IT ..." / "I DON'T WANT IT ..." OPENS A CHANGE TOO (D2, 2026-09-30):
# her second message, verbatim in wife-test v1 -- "i dont want it text based,
# i want a game i can play" -- is a change to the game in hand, and with the
# make phrase inside the same sentence it made a second game instead. "it"
# is the thing in hand; "want a ..." with no "it" stays a request to make.
_CHANGE_RE = re.compile(
    r"(?i)^\s*(?:i\s+(?:don'?t\s+|do\s+not\s+)?want\s+(?:it|the|them|this)\b"
    r"|(?:(?:ok|okay|now|please|and|alright|also|then|cool|nice|great)"
    r"[,!.]?\s+)*(?:(?:can|could|would|will)\s+you\s+)?(?:please\s+)?"
    r"(?:make\s+(?:it|the|them|everything|its|this)|change|add|remove|delete|"
    r"fix|slow|speed|increase|decrease|replace|turn|give\s+(?:it|the)|use|put|"
    r"rename|double|halve|swap|improve|tweak|update|set|let(?!\s+(?:me|us)\b)|"
    r"hide|move|shrink|enlarge|center|centre|resize|recolou?r)\b)")


def wants_changing(objective: str) -> bool:
    """Whether the words ask for a change to the project in hand."""
    return bool(_CHANGE_RE.match(objective or ""))


# THE CODER'S WINDOW ON THE TREE (2026-09-28). Four firings of the coder-tree
# flow put "In manjuel/skills.py, add `foundation` to the `_NEVER_WRITTEN_TOP`
# dict, one line beside the `law` entry" through the estate and nothing was
# edited: a 4B Router planned the two-call edit and stopped at the plan, and
# the Expert Coder -- the seat that can make it -- never sat, because a big
# objective wakes the Router directly and skips the seat that raises
# `technical`. So a change to a NAMED FILE IN THE GROUND is read by
# arithmetic, as a make request is: the file, a change verb, and the names in
# backticks the passage is fetched by. NARROW ON PURPOSE: the file must carry
# a folder (a bare name is the workspace's), the sentence must carry a change
# verb, and a question about changing is a question.
_TREE_CHANGE_VERB = re.compile(
    r"(?i)\b(?:add|append|insert|change|edit|fix|replace|rename|remove|delete|"
    r"update|move|put|set|extend|widen|narrow)\b")
# A name in backticks: a definition (`_LIKE_THIS`, `Class.method`) or, for a
# .md, a heading (`The dials`, `## The dials`) -- so spaces are allowed and
# the file's own map decides what resolves.
_BACKTICKED = re.compile(r"`([^`\n]{1,80})`")


def wants_a_tree_change(objective: str) -> tuple[str, list[str]]:
    """(the file in the ground, the backticked names in order) when the words
    ask for a CHANGE to a named file -- a path with a folder in it, or a bare
    `.md` (a root document: the engine checks it is there before the turn is
    the tree's, and a bare name that is not falls through as before) -- with
    a change verb; else ("", [])."""
    text = objective or ""
    if _ASKS_ABOUT_MAKING.match(text):
        return "", []
    rel = names_a_file(text)
    if not rel:
        return "", []
    if "/" not in rel and "\\" not in rel and not rel.lower().endswith(".md"):
        return "", []
    if not _TREE_CHANGE_VERB.search(text):
        return "", []
    # A backticked FILE is not a passage; `Class.method` is, as the map says.
    names = [n.strip() for n in _BACKTICKED.findall(text)]
    names = [n for n in names if n and not _FILENAME_RE.fullmatch(n)]
    return rel, list(dict.fromkeys(names))


# GOING BACK. Asked before a change, so "change it back" is never handed to the
# Coder to guess at: the earlier version is on disk, and restoring it is git's
# job, not a model's.
_BACK_RE = re.compile(
    r"(?i)\b(?:go(?:ing)?\s+back|undo|revert|roll\s*back|restore|put\s+it\s+back|"
    r"change\s+it\s+back|previous\s+version|the\s+way\s+it\s+was|how\s+it\s+was|"
    r"back\s+to\s+(?:version|v)\s*#?\d)")
_VERSION_NO = re.compile(r"(?i)\b(?:version|v)\s*#?\s*(\d{1,4})\b")
# ...BUT "UNDO" IS ALSO A BUTTON. A page can HAVE an undo, a restore, a back:
# "add an undo button" asks for a CHANGE, and read as a go-back it would throw
# the person's page back a version instead. Named as a thing -- after a/an/the,
# or before button, key, feature -- the word is the feature, not the request.
_BACK_AS_A_THING = re.compile(
    r"(?i)\b(?:a|an|the|its|with)\s+(?:undo|restore|revert|go[ -]?back|back)\b"
    r"|\b(?:undo|restore|revert|back)[ -]?(?:buttons?|keys?|features?|options?|"
    r"arrows?|links?|functions?)\b")
# ...AND INSIDE A CHANGE, ONLY THE WORDS THAT CAN MEAN NOTHING ELSE. "add a
# button that restores the board" opens with a change, and its "restores" is
# the change's own word; "let's go back" and "make it how it was" still go back.
_BACK_EVEN_IN_A_CHANGE = re.compile(
    r"(?i)\b(?:go(?:ing)?\s+back|change\s+it\s+back|put\s+it\s+back|"
    r"previous\s+version|the\s+way\s+it\s+was|how\s+it\s+was|"
    r"back\s+to\s+(?:version|v)\s*#?\d)")


def wants_going_back(objective: str) -> int | None:
    """None when this is not a request to go back; otherwise the version asked
    for, or 0 for "the one before this"."""
    text = objective or ""
    if not _BACK_RE.search(text) or _BACK_AS_A_THING.search(text):
        return None
    if wants_changing(text) and not _BACK_EVEN_IN_A_CHANGE.search(text):
        return None
    m = _VERSION_NO.search(text)
    return int(m.group(1)) if m else 0


# PICKING A PROJECT UP, AND PUTTING IT DOWN (piece 2, 2026-09-21). A sitting
# starts with nothing in hand, and until this the only way to put a project down
# was to close the sitting. The glass's project list sends these words; a
# person can say them too.
#
# PICKING UP: a verb that OPENS the request, then a name. The pipeline looks the
# name up among the projects on disk (maker.find), so words that name none fall
# through exactly as they did before this existed -- "open the pod bay doors" is
# not a project, and neither is "go back to version 2" -- unless they said
# "project" outright, and then the person is told what there is. "go back to"
# is here on purpose: "go back to the snake game", with another project in hand,
# is a request for the snake game, not for this project's last version.
_PICK_RE = re.compile(
    r"(?i)^\s*(?:(?:ok|okay|now|please|and|alright|so|then|cool|great)[,!.]?\s+)*"
    r"(?:(?:let['’]?s|can\s+we|could\s+we|i\s+want\s+to|i['’]?d\s+like\s+to)\s+)?"
    r"(?:please\s+)?"
    r"(?:work\s+on|switch\s+(?:over\s+)?to|pick\s+up|open(?:\s+up)?|"
    r"go\s+back\s+to|continue(?:\s+(?:with|on))?|resume)\s+"
    r"(?P<what>.+?)"
    r"(?:\s+(?:again|now|please|for\s+a\s+(?:bit|while)))*[\s.!?]*$")
# Words that point at a thing without naming one, and the articles in front of
# a name. "work on it" names nothing; "work on the snake game" names snake game.
_NOT_A_NAME = frozenset({"it", "this", "that", "them", "there", "here", "one"})
_ARTICLES = re.compile(r"(?i)^(?:(?:the|a|an|my|our|that|this)\s+)+")


def wants_picking_up(objective: str) -> str:
    """The words naming a project to pick up -- "work on the snake game
    project" -> "snake game" -- or ""."""
    m = _PICK_RE.match(objective or "")
    if not m:
        return ""
    what = re.sub(r"(?i)\s+projects?$", "", m.group("what").strip())
    what = _ARTICLES.sub("", what).strip(" .,!?\"'")
    words = re.findall(r"[a-z0-9]+", what.lower())
    if not words or all(w in _NOT_A_NAME for w in words):
        return ""
    return what


# PUTTING DOWN names no project -- it is the one in hand -- and it must be the
# WHOLE request, because two of its words are a change's: `put` opens a change
# ("put a border round it"), and "put it down lower" asks for one. Anchored at
# both ends, "put it down" can mean only this. It is asked before a change for
# the same reason a go-back is.
_PUT_DOWN_RE = re.compile(
    r"(?i)^\s*(?:(?:ok|okay|now|please|and|alright|right|so|then|cool|great|"
    r"thanks|thank\s+you)[,!.]?\s+)*"
    r"(?:(?:let['’]?s|you\s+can|can\s+you|could\s+you)\s+)?(?:please\s+)?"
    r"(?:put\s+(?:it|this|that|(?:the|this|that)\s+project)\s+(?:down|away|aside)"
    r"|put\s+(?:down|away)\s+(?:the|this|that)\s+project"
    r"|set\s+(?:it|this|that|(?:the|this|that)\s+project)\s+aside"
    r"|(?:close|shelve)\s+(?:the|this|that)\s+project"
    r"|stop\s+working\s+on\s+(?:it|this|that|(?:the|this|that)\s+project)"
    r"|(?:(?:i['’]?m|i\s+am|we['’]?re|we\s+are)\s+)?(?:all\s+)?(?:done|finished)"
    r"\s+with\s+(?:it|this|that|(?:the|this|that)\s+project))"
    r"(?:\s+(?:for\s+now|for\s+today|now))?[\s.!,]*(?:thanks|thank\s+you)?[\s.!]*$")


def wants_putting_down(objective: str) -> bool:
    """Whether the words ask to put the project in hand down."""
    return bool(_PUT_DOWN_RE.match(objective or ""))
