# LOFT Process Safety Study Aids

Study material for the **LOFT** (Leadership for Operations Framework for Training)
Process Safety competency assessment, for candidates in Second- and Third-Line
Supervisor positions and the assessment teams who verify them.

This repository is not an application. It holds one interactive HTML study aid, a
review sheet for the answers that only the asset can confirm, and the controlled
source documents both are derived from.

## The study aid

**`LOFT-Process-Safety.html`** — open it in any browser. No install, no server, works
offline. One file, three modes, switched from the bar at the top:

| Mode | What it does | For |
|---|---|---|
| **Guide** | Every question with its model answer, by section, with the glossary and source links | Reading through; running an assessment |
| **Test** | Answers hidden, revealed one at a time, with search across questions and answers | Self-testing before the interview |
| **Cards** | One question at a time — flip to the answer, mark *Got it* or *Needs review*, shuffle, filter by category | Practising recall |

All three modes read the **same** questions and answers. Correcting an answer fixes it
everywhere at once — there is no second copy to drift out of step.

Search works in Guide and Test modes, so a question can be found mid-interview without
scrolling. On a phone or tablet the contents list collapses into a **Contents** drawer.

It covers 100 questions across the ten Process Safety categories: Risk Management,
Training, Operating Procedures, Critical Equipment, Alarm Management, Work Management,
Management of Change, Incident Investigation, Environmental, and Emergency Response.

Keyboard shortcuts in Cards mode: **Space** flips, **←/→** move, **G** marks got it,
**R** marks needs review, **S** shuffles.

> **This file replaces `Loft.html` and `LOFT Training Flip Card.v1.html`,** which were
> removed. They held overlapping copies of the same material, and every content
> correction had to be made in two or three places — five of seven content fixes in
> August 2026 touched more than one file. Both remain in git history if needed.

## Practice questions

`LOFT-Practice-Questions.html` is a multiple-choice drilling tool &mdash; 133 questions
across all eleven topics, every answer traced to the study aid.

> **The assessment is a face-to-face interview.** You will be asked to *demonstrate* and
> *describe*, out loud, to an assessment team. Multiple choice cannot test that, and
> passing this does not mean you are ready. What it is good for is the factual half:
> approval levels, thresholds, timeframes, who signs what. Get those solid here, then
> practise saying the full answers aloud from the study guide.

- **Practice mode** marks each answer as you go, with the reason and the study guide
  question it came from. **Test mode** holds the score until the end.
- Pick a topic or take the lot; 10, 20, 40 or all 133. Questions and options are shuffled.
- The result breaks the score down by topic and lists everything missed, with the
  explanation, so it doubles as a revision list. Best score per topic is kept in the
  browser so weak areas stay visible.
- Keys **1&ndash;4** answer, **Enter** moves on. An unfinished attempt can be resumed.
- Questions marked **asset** come from Hebron/Hibernia local material that no source
  document can confirm &mdash; the same 38 answers under review. Treat them as current
  practice rather than verified fact.

Distractors were deliberately written to match the correct answer in length and
specificity. An earlier draft had the correct option longest in 79% of questions, which
would have let someone score well by picking the longest answer without knowing anything.

## Two kinds of notes

The file carries **two separate note systems**, and they never mix.

| | Who | Where | Saved as |
|---|---|---|---|
| **My study notes** | the candidate, while studying | under every question, always visible | `LOFT-my-study-notes.json` |
| **Assessor notes** | the assessment team, during the interview | under every question, behind the assessor gate | `LOFT-<candidate>-<date>.json` |

They use different storage, different file formats, and each loader refuses the
other's file. A candidate studying on a shared machine cannot write into an
assessment record, and an assessment record never picks up study material.

**Study notes.** Type in the *My study notes* box under any question — what tripped you
up, how you remember it, where to read more. It saves as you type. **My notes** in the
top bar collects everything you have written, grouped by section, and prints. The button
shows a running count.

## Assessor access

The assessment record — notes, outcomes, modules, the session bar and the summary — is
hidden until you unlock it with **Assessor access** in the top bar. The default password
is `admin`. **Password** (visible once unlocked) changes it for that machine.

> **This is a gate, not security.** The whole file is delivered to the browser, so anyone
> who opens View Source can find the check and bypass it. It exists so a candidate does
> not wander into the assessment record by accident, and so the two roles stay visibly
> apart on a shared machine. Do not put anything behind it that would matter if it were
> read. If an assessment record needs real protection, protect the saved `.json` file.

**You can tell at a glance which mode you are in.** In assessor mode the top bar turns
green and a banner sits under it — *"Assessor mode — the assessment record is visible and
is being saved"* — with a **Lock** button on the right. The banner stays for as long as
the mode does. When the record first appears the session bar is scrolled to and flashed,
so the change is visible even from the middle of a long page.

Unlocking lasts for the browser tab, not the machine — closing the browser re-locks,
which is the safer default on a shared computer. Click **Assessor mode on** to lock again
straight away.

Printing follows the mode: **locked** prints the study notes, **unlocked** prints the
assessment record without them.

A forgotten password is reset by clearing the site data for the file, which restores
`admin`. To change the default for everyone rather than one machine, edit `DEFAULT_HASH`
in the `loft-admin-js` script block.

## Recording an assessment

The study guide carries a notes panel under every question, for the assessor or the
assessment team to use during a verification interview.

- **Notes** — a free-text box per question for evidence, examples given, and follow-ups.
- **Outcome** — mark each question *Demonstrated*, *Needs development*, or
  *Gap — action required*. A running count sits in the header bar. These are the
  evidence behind the module decision, not the decision itself.
- **Modules** — section 1.5 verifies competency per module, so each module is marked
  *Competency demonstrated* or *Gap closure required*, with a re-assessed tick for gaps
  that have since been closed. Overall competency only reads as demonstrated when every
  module does, and the panel states the Risk Approval Authority position either way.
- **Session details** — candidate, position, date assumed position, assessment date, and
  the team by role: Assessment Lead, Assessment Facilitator, Technical Assessor(s). The
  file counts the team and flags if it falls outside the three-to-five that section 1.6
  requires, and computes the 90-day verification target from the date the position was
  assumed (section 1.3).

**Saving.** Everything is saved in the browser as you type, so closing the tab or
reloading will not lose it. That copy lives only in that browser on that machine, so it is
working state, not a record.

To keep or share an assessment, use **Save file** — it downloads a `.json` file named for
the candidate and date. **Load file** restores it, on any machine. That file is the record
to pass to the assessment team; hand it over rather than relying on the browser copy.

**Summary** builds the assessment record and the **gap closure plan**: counts of
demonstrated / needs development / gap, then every question marked *Gap* or *Needs
development* with its notes, followed by anything noted without an outcome. The Assessor
Guide requires a gap closure plan for each of those before Full Risk Approval Authority is
granted. Print it, or **Download summary** for a standalone HTML file to send on.

**Print / PDF** produces a clean record of the full guide: sidebars and buttons drop away,
and the candidate, assessment team and date print at the top with each question, its notes
and its outcome.

**Clear all** wipes the page. Save to a file first if the notes matter.

> If two people assess on the same computer and browser, they share the same working copy.
> Save to a file and clear between candidates.

## Source documents

The study aids are derived from these. **Where an aid and a source disagree, the
source governs.**

| Document | Role |
|---|---|
| `UPBP-400-EN-01-RP-GBL-Process Safety Global Module Assessor_s Guide Rev 3.0.docx` | Authoritative questions and model answers for the Global Module |
| `UPBP-400-EN-02-LG-GBL-LOFT TASKBOOK Rev 3.4.docx` | LOFT Task Book |
| `UPBP-410-EN-02-LG-GBL-LOFT TASK Rev 3.2 Asset Specific Process Safety Modules _5_.docx` | Asset Specific module template (questions; answers are developed by the Business Unit) |
| `Training CriticalE and Expectations .pdf` | Critical Expectations `[CriticalE]` and Expectations `[E]` that govern the program |
| `Leadership for Operations _ Framework for Training _LOFT_.pdf` | LOFT framework overview |

Every question has been diffed against its source document word by word, not just its
answer checked &mdash; see `REVIEW.md` section 16. Four wording defects were found and
fixed, including one question whose text was missing entirely.

Two wording issues in Assessor Guide Rev 3.0 are written up in
`SOURCE-DOCUMENT-QUERIES.md`, ready to send to the document owner: it says ten Process
Safety categories and then lists eleven, and it has both the SLS and the TLS informing
the Site Manager directly. The study aid follows the guide as written in both cases —
a candidate is assessed against what the assessor is reading.

## Two things to know before studying

**The assessment window is 90 days.** `[E] Section 12` requires personnel assigned
to a LOFT Process Safety position to complete the assessment within 90 days of
assuming the position. Risk Approval Authority is delegated until competency is
demonstrated.

**Role titles follow Assessor Guide Rev 3.0 throughout**, confirmed correct by the
asset (August 2026):

| Abbreviation | Title used | Older material may say |
|---|---|---|
| AM | **Operations Manager** | Asset Manager |
| PM | **Site Manager** | Production Manager |
| TLS | Third Line Supervisor (Operations Manager) | — |

This applies to every answer, global and asset-specific alike, so the file never mixes
the two conventions. The glossary states the mapping for anyone arriving from older
material.

## Scope notes

- **Competency Assurance Standard (CAS)** applies only where a work area has not yet
  completed CVPE. **Hebron/Hibernia has completed CVPE** (confirmed by the asset,
  August 2026), so the **Training and Competency UBP answers apply**. The study aid
  leads with the CVPE answer. Where the Assessor Guide also carries a superseded
  CAS-route answer it is shown and labelled, so a candidate can tell them apart:

  | | CVPE route (applies here) | CAS route (superseded) |
  |---|---|---|
  | Procedure revalidation | successfully used in the field; **not to exceed 36 months** | IC 3 years / Normal 5 years / Work Aid BU-defined |
  | Deviation approval | stop work; documented approval from the **SLS** | IC = Site Manager / Normal = SLS / Work Aid = FLS |
  | New or revalidated procedure | technically verified, site validated, endorsed **FLS**, approved **SLS** | SME + user validate, FLS/SLS/TLS endorse, Site Manager approves |

  Three questions exist only on the CAS route — the Integrity Critical Procedure
  definition, the global IC examples list, and the night-time IC error scenario. They
  are retained for reference and marked as not assessed under the current UBP.
- **No marine scenario.** UPBP-410 Q3 asks about *"wellbore integrity **or marine** related
  incident scenarios"*. **Hebron and Hibernia have no marine related incident scenario** in
  the higher consequence set (confirmed by the asset, August 2026). The study aid carries
  the source's full wording and answers both halves &mdash; the two wellbore scenarios, and
  that there is no marine one. The words had been dropped from the question, which quietly
  narrowed an assessed question and would have left a candidate with nothing to say to the
  marine half.
- **Flag / Class** questions in the Assessor Guide apply only to Business Units with
  floating vessels (FPSO, FSO). **Hebron and Hibernia are not floating vessels**
  (confirmed by the asset, August 2026), so these four questions are out of scope and
  are deliberately not covered here. This is the only part of the Assessor Guide
  omitted — every other Global Module question is covered.
- Links into `ishareteam*.na.xom.com`, `teamwork1.exxonmobil.com` and
  `us1.aconex.com` resolve only on the corporate network.

## Reviewing the asset specific answers

`ASSET-SPECIFIC-REVIEW-SHEET.html` is a standalone sheet for one job: getting the 38
asset-local answers checked by somebody who knows the asset.

**Why it exists.** Every other answer in the study aid can be checked against a source
document in this repository. These cannot. UPBP-410 Rev 3.2 is a *question template* —
it sets the questions and leaves the answers to the Business Unit. The answers in the
study aid were carried forward from the existing Hebron/Hibernia material, and nothing
here can confirm whether they are still current.

It holds the 34 Asset Specific Task Book questions in source order, tagged with their
UPBP-410 numbers, plus four items of asset-local content that are not Task Book
questions: three critical-safeguard lists and one global question (breaking containment,
single-valve isolation) that carries a Hebron/Hibernia answer alongside the global one.
Each shows the answer exactly as it currently stands in the study aid, with a verdict —
correct / needs change / not applicable / refer — and a box for the correction.

Open it in a browser. Work saves in that browser as you type; **Save to file** writes a
JSON record that can be reloaded or handed on, and it also carries a plain-text summary
inside it for anyone who just wants to read the verdicts. **Print** gives a paper copy
with writing space.

The sheet records a review. It does not change the study aid — applying the corrections
is a separate edit.

## Contributing

Content changes must be traceable to a source document revision. See
[CONTRIBUTING.md](CONTRIBUTING.md).
