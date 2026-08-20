# LOFT Process Safety Study Aids

Study material for the **LOFT** (Leadership for Operations Framework for Training)
Process Safety competency assessment, for candidates in Second- and Third-Line
Supervisor positions and the assessment teams who verify them.

This repository is not an application. It holds three interactive HTML study aids
and the controlled source documents they are derived from.

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
  August 2026), so the **Training and Competency UBP answers apply**. All three aids
  now lead with the CVPE answer. Where the Assessor Guide also carries a superseded
  CAS-route answer it is shown and labelled, so a candidate can tell them apart:

  | | CVPE route (applies here) | CAS route (superseded) |
  |---|---|---|
  | Procedure revalidation | successfully used in the field; **not to exceed 36 months** | IC 3 years / Normal 5 years / Work Aid BU-defined |
  | Deviation approval | stop work; documented approval from the **SLS** | IC = Site Manager / Normal = SLS / Work Aid = FLS |
  | New or revalidated procedure | technically verified, site validated, endorsed **FLS**, approved **SLS** | SME + user validate, FLS/SLS/TLS endorse, Site Manager approves |

  Three questions exist only on the CAS route — the Integrity Critical Procedure
  definition, the global IC examples list, and the night-time IC error scenario. They
  are retained for reference and marked as not assessed under the current UBP.
- **Flag / Class** questions in the Assessor Guide apply only to Business Units with
  floating vessels (FPSO, FSO). **Hebron and Hibernia are not floating vessels**
  (confirmed by the asset, August 2026), so these four questions are out of scope and
  are deliberately not covered here. This is the only part of the Assessor Guide
  omitted — every other Global Module question appears in all three study aids.
- Links into `ishareteam*.na.xom.com`, `teamwork1.exxonmobil.com` and
  `us1.aconex.com` resolve only on the corporate network.

## Contributing

Content changes must be traceable to a source document revision. See
[CONTRIBUTING.md](CONTRIBUTING.md).
