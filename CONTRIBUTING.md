# Contributing

This repository holds process safety training material. A wrong answer here is a
safety-training defect, not a failing test — so the bar for content changes is
traceability to a controlled source document, not code style.

## The Assessor Guide governs

Where a study aid and the Assessor Guide disagree, **the Assessor Guide wins** — even when
the source looks wrong. A candidate is assessed against what the assessor is reading, so a
study aid that "corrects" the controlling document sets them up to give an answer the
assessor marks wrong.

If you believe the source is defective, raise it with the Assessor Guide's owner and leave
the study aid matching the source until the source changes. Two known examples are recorded
in `REVIEW.md` §9: the guide says it covers "ten Process Safety categories" then lists
eleven, and it has both the SLS and the TLS informing the Site Manager of a failed critical
safeguard. Both are carried as written.

## Before changing any answer

1. **Identify the governing source.** For Global Module content that is
   `UPBP-400-EN-01-RP-GBL Process Safety Global Module Assessor Guide Rev 3.0`. For
   asset-specific content it is the Business Unit's own material.
2. **Quote it.** Put the source document, revision, and section in the commit
   message. "Matches Assessor Guide Rev 3.0, Risk Management" is enough; "fixed
   wording" is not.
3. **Do not paraphrase approval authorities, thresholds, or timeframes.** Who
   approves what, how many days, and which category — copy these exactly. These are
   the answers a candidate is assessed on.
4. **Keep global and asset-specific content distinct.** If a change applies only to
   Hebron/Hibernia, mark it *Asset specific* rather than editing a global answer.

## Role titles

Use Assessor Guide Rev 3.0 titles everywhere: **AM = Operations Manager**, **PM =
Site Manager**. The asset confirmed these are correct (August 2026), so they apply to
asset-specific answers too.

Do not reintroduce "Asset Manager" or "Production Manager". Older material uses those
names for the same two roles; the glossary notes this so a reader coming from the old
documents is not confused.

## Changing the HTML

- There is **one** study aid file, `LOFT-Process-Safety.html`. Guide, Test, Cards and
  Practice are four views of the same material — do not fork it into separate files
  again. The reason it was consolidated is that every content fix previously had to
  be repeated in two or three places, and they drifted. This happened a second time:
  the practice questions shipped as their own file, restating facts from 87 study aid
  answers, and were folded back in for the same reason.
- **The practice bank restates facts that live in the answers above it.** When you
  correct an answer, grep `loft-practice-bank` for anything that repeats the old value
  — a threshold, an approval level, a timeframe — and fix it in the same commit. That
  duplication is the price of having a question bank at all; being in one file only
  makes it findable, not automatic.
- **The `.question` divs are now well-formed — keep them that way.** 48 of them used to
  swallow the content that followed, because they were left unclosed in the source and the
  browser nested whatever came next inside them. They were repaired one at a time (see
  `REVIEW.md` section 12); a question div now starts and ends where the question does. If
  you add a question, close every tag you open inside it.
- **Never fix that kind of markup with a single bulk rule.** Four were tried and every one
  silently reordered text elsewhere in the document, because the source had several
  different malformation patterns. What worked was repairing one site, re-rendering the
  whole file, comparing the extracted text character for character against a baseline, and
  reverting that one change if anything differed. Use the same loop for any structural
  edit: one change, verify, keep or revert.
- **Two note systems, deliberately separate.** Study notes (`loft-study-notes-v1`,
  `.study-panel`) belong to the candidate; assessor notes (`loft-assessor-notes-v1`,
  `[data-note-panel]`) are the assessment record. Different keys, different file
  formats, and each loader rejects the other's file. Do not merge them or route one
  through the other's storage — the separation is the point.
- **The assessor password is a gate, not security**, and the code says so. It keeps a
  candidate out of the record by accident; it does not withstand View Source. Do not
  describe it as protection, and do not put anything behind it that would matter if it
  were read.
- **New panels must be excluded from `ownText`.** Both `ownText` helpers strip
  `.question, .answer, .note-panel, .study-panel, .reveal-btn` so injected UI never
  reaches the search index or a saved record. Any new panel class has to be added to
  both, and to `applyFilter`, or search starts matching your own furniture.
- **Full-screen layers need `inset: 44px 0 0 0` and `z-index: 1150`.** The mode bar and
  the glossary toggle are both `position: fixed`; a layer that ignores this renders
  underneath them. `#summaryLayer` and `#studyLayer` both do it this way.
- **Careful inserting new `<script>` blocks.** The summary script contains the literal
  string `'</body></html>'` inside the standalone report it generates, so a naive
  "insert before `</body>`" lands inside that string literal and breaks two scripts.
  Insert before the **last** `</body>`.
- It is standalone: no build, no dependencies, no server. Keep it that way — it is
  opened from disk, sometimes offshore.
- After any content edit run `python3 tools-coverage-check.py`. It verifies that all
  57 Assessor Guide topics are still present and exits non-zero if one goes missing.
- Open the file in a browser and confirm it renders and behaves before committing.
  Check the browser console is clean.
- Card progress and assessor notes are stored keyed on a hash of the question text.
  **Changing question wording resets progress and unlinks any note for that
  question.** That is acceptable for a correction; avoid it for cosmetic edits.
- The markup was repaired in August 2026 — it previously had a
  premature `</body></html>` partway down, with the TOC and all 19 sections
  sitting after it. Tags are balanced now; keep them that way. If you ever
  regenerate the file wholesale, verify afterwards that the rendered
  `textContent` is unchanged, not just that the HTML parses.

## Reporting a problem

Open an issue with the file, the section, what it currently says, and what the
source document says. If you are not sure which is right, say so — a flagged
discrepancy is more useful than a silent guess.
