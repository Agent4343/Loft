# Contributing

This repository holds process safety training material. A wrong answer here is a
safety-training defect, not a failing test — so the bar for content changes is
traceability to a controlled source document, not code style.

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

Global-module answers use Assessor Guide Rev 3.0 titles: **AM = Operations
Manager**, **PM = Site Manager**. Asset-specific answers keep local titles. Do not
normalise one into the other — the difference is real and each study aid documents
the mapping.

## Changing the HTML

- All three files are standalone: no build, no dependencies, no server. Keep them
  that way — they are opened from disk, sometimes offshore.
- Open the file in a browser and confirm it renders and behaves before committing.
  Check the browser console is clean.
- `LOFT Training Flip Card.v1.html` stores progress in `localStorage` keyed on a
  hash of the question text. **Changing question wording resets a user's progress
  for that card.** That is acceptable for a correction; avoid it for cosmetic edits.
- The study guide's markup was repaired in August 2026 — it previously had a
  premature `</body></html>` partway down, with the TOC and all 19 sections
  sitting after it. Tags are balanced now; keep them that way. If you ever
  regenerate the file wholesale, verify afterwards that the rendered
  `textContent` is unchanged, not just that the HTML parses.

## Reporting a problem

Open an issue with the file, the section, what it currently says, and what the
source document says. If you are not sure which is right, say so — a flagged
discrepancy is more useful than a silent guess.
