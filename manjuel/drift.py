"""Drift: does a stage's output still say what the source said?

This is §11's tier-1 check. It is not a model judging a model -- it is a
measurement. Embed the source material, embed what a stage produced, take the
cosine. A low score means the stage wandered from, dropped, or invented
material relative to what it was given.

Why it matters here specifically: the Morning Reviewer is a 0.5b model running
FIRST, compressing a noisy feed to two sentences. Everything downstream
inherits whatever it discarded or made up, and no later seat can recover it.
A cosine score cannot hallucinate, and it costs one embedding per stage.

It is ADVISORY. A low score is recorded and reported, never used to rewrite or
silently discard a stage -- the same principle that keeps Manjuel and Jesster
from rewriting the work they rule on. What it can do is raise a flag, so a
`When:` step could react to it.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import mathkit

# Below this cosine, a stage is reported as having drifted. Chosen to be
# quiet in normal use: unrelated text on nomic-embed-text sits near 0.2-0.4,
# a faithful summary of its source typically 0.7+.
# A SHORT SOURCE carries less signal than a full feed -- a one-line tool
# result, a feed of a sentence -- so a source under SHORT_SOURCE_CHARS is
# judged against the lower bar (see `score`). This comment promised that bar
# to "a bare objective" until 2026-09-29; a bare objective has never primed
# the checker at all (sitting 27's ruling: a request is not a source).
DRIFT_WARN = 0.55
DRIFT_WARN_SHORT = 0.35
SHORT_SOURCE_CHARS = 200

# Two floors, not one. An OUTPUT needs real length before a cosine means
# anything. A SOURCE does not: "review the git init" is only 19 characters and
# is still exactly the thing the answer should be about. Sessions 3 and 4 both
# skipped the check entirely because one floor was applied to both, so the
# 274MB embedder never ran at all.
MIN_OUTPUT_CHARS = 80
MIN_SOURCE_CHARS = 12


@dataclass
class DriftScore:
    score: float
    ok: bool
    reason: str = ""

    def stamp(self) -> str:
        if self.reason:
            return f"drift: not scored ({self.reason})"
        verdict = "ok" if self.ok else "DRIFTED"
        return f"drift: {self.score:.3f} {verdict}"


class DriftChecker:
    """Embeds the source once per run, then scores each stage against it."""

    def __init__(self, runtime, model: str, threshold: float = DRIFT_WARN):
        self.runtime = runtime
        self.model = model
        self.threshold = threshold
        self._source: list[float] | None = None
        self._failed = False
        self._noted = False   # a skip is reported once, not once per stage
        self._short_source = False
        self._too_short = False   # the last source offered was under the floor

    def prime(self, source_text: str) -> bool:
        """Embed the source material. False if it cannot be scored at all.

        RE-PRIMABLE, and that is what the citation check needs: a run's source
        changes when a tool returns, and the stages after it are speaking
        about the RESULT, not about the feed.

        A SHORT SOURCE IS NOT A DEAD EMBEDDER. Until 2026-09-10 this set
        `_failed = True` for a source under MIN_SOURCE_CHARS, and `_failed` is
        permanent -- so one short string poisoned the object and no later,
        longer source could ever prime it. The embedder failing IS permanent;
        a string being too short is a fact about that string.
        """
        if self._failed:
            return False
        text = (source_text or "").strip()
        if len(text) < MIN_SOURCE_CHARS:
            self._too_short = True
            return False
        self._short_source = len(text) < SHORT_SOURCE_CHARS
        try:
            self._source = self.runtime.embed(self.model, text)
            self._too_short = False
            return True
        except Exception:
            # An embedder that is missing or down must not take the run with
            # it -- the check is a courtesy, not a dependency.
            self._failed = True
            return False

    def why_unscored(self) -> str:
        """Why score() answered None, saying WHICH of three states it is.

        ONE NOTE STOOD FOR ALL THREE until 2026-09-29, and it called the
        source "not usable". It read as WE LOOKED AND FOUND NOTHING WORTH
        SCORING, 463 times in 502 transcripts, and the truth was that the
        check had never been armed -- no feed was pasted and no tool ran, by
        design. The operator reasoned aloud about automating the toll on a
        measurement that had not once run (TASKS, the drift finding).

          NOT ARMED    nothing was ever offered as a source: no pasted feed,
                       no tool result. Nothing was tried; nothing was unusable.
          TOO SHORT    a source was offered and is under MIN_SOURCE_CHARS.
          NOT SCORED   a source was offered and the embedder could not be
                       reached. The check is a courtesy; the run went on.
        """
        if self._failed:
            return ("not scored this run (the embedder could not be reached; "
                    "the run went on without the check)")
        if self._source is None and self._too_short:
            return (f"not armed this run (the source offered was under "
                    f"{MIN_SOURCE_CHARS} characters, too short to measure against)")
        return ("not armed this run (no pasted source and no tool result to "
                "measure against; an objective alone is a request, not a source)")

    def note_once(self, reason: str) -> str | None:
        """Return `reason` the first time only, so a skipped check is stated
        without repeating itself at every stage."""
        if self._noted:
            return None
        self._noted = True
        return reason

    def score(self, output: str) -> DriftScore | None:
        if self._failed or self._source is None:
            return None
        text = (output or "").strip()
        if len(text) < MIN_OUTPUT_CHARS:
            return DriftScore(0.0, True, reason="output too short to score")
        try:
            vec = self.runtime.embed(self.model, text)
        except Exception as exc:
            return DriftScore(0.0, True, reason=f"embedder unavailable: {exc}")

        sim = mathkit.cosine(self._source, vec)
        # Against a SHORT source the expected similarity is genuinely lower;
        # holding it to the full-feed bar would cry drift on every short run.
        bar = DRIFT_WARN_SHORT if self._short_source else self.threshold
        return DriftScore(sim, sim >= bar)
