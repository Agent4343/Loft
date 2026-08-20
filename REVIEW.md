# LOFT Repository — HTML & Documentation Review

**Date:** 2026-08-20
**Scope:** The three HTML study aids in this repository, reviewed against the source
documentation (`.docx` / `.pdf`) also committed here, plus the repository's own docs
(`README.md`, `CONTRIBUTING.md`, `.gitignore`).

**Method:** Every finding below was reproduced by loading the files in headless Chromium
(same engine as the "Use Google Chrome" instruction in one filename) and by extracting and
diffing the text of the source `.docx`/`.pdf` files against the HTML.

> **Status (2026-08-20): fixes applied.** Every code and content finding below has been
> acted on. Each finding carries its outcome; what remains in §9 is owner decisions and
> source-document defects, not outstanding work in this repository. §5.2 has been **corrected**: the original mapping
> in this review was wrong, and the fix that was applied differs from what it first
> recommended.

---

## 1. Summary

| File | Verdict as found | Headline issue | Now |
|---|---|---|---|
| `Loft.html` | **Broken — do not use** | JavaScript fails to parse; 59 of 68 answers are placeholders | Rebuilt: 69 real answers, no errors |
| `LOFT Training Flip Card.v1.html` | **Good — one data-integrity bug** | Shuffle silently reassigns your progress marks to the wrong questions | Fixed and regression-tested |
| `LOFT_Assessment_Study Use Google Chrome20260212.html` | **Usable — several defects** | One dead TOC link; stated assessment window contradicts the UBP | Fixed, markup repaired |
| Repository docs | **Inaccurate** | `README.md` describes a different project entirely | Rewritten |

Two issues cut across the whole repository and matter more than any single bug:

1. **A factual contradiction with the controlling UBP.** The study guide tells candidates the
   assessment happens **within 60 days** of assuming the position. The `Training CriticalE and
   Expectations` PDF in this repo states `[E] Section 12 ... should complete the LOFT Process
   Safety assessment **within 90 days** of assuming the position.` The Assessor Guide Rev 3.0
   agrees: *"target should be within 90 days of assuming position."* The study aid is wrong.
2. **Systematic role-title substitution.** The source documents say **Site Manager** (13×) and
   **Operations Manager** (7×), and never say "Asset Manager". All three HTML files say
   **Asset Manager** (4/11/14×) and never say "Site Manager". Because these questions are
   *about approval authority*, a candidate who studies the HTML will name the wrong role in
   assessment. See §5.2 for the exact mapping — it is **not** a straight
   "Asset Manager → Site Manager" rename.

---

## 2. `Loft.html` — non-functional

### 2.1 The entire script fails to parse (critical)

The page loads with `Uncaught SyntaxError: Unexpected end of input`. `toggleMode`,
`revealAnswer` and `filterQA` are all `undefined`, so **Test Mode, every "Reveal Answer"
button, and the search box are dead**.

Root cause: the file was minified by stripping newlines while keeping `//` line comments.
The whole `<script>` is one line, so this tail:

```js
window.addEventListener('DOMContentLoaded',()=>{ // default to Study Mode  toggleMode(); // turn on Test  toggleMode(); // back to Study });
```

comments out everything from the first `//` to end-of-file — the arrow function is never
closed. Verified with `node --check` on the extracted script.

*Fix:* restore line breaks after each `//` comment, or convert them to `/* … */`.

**Applied.** `Loft.html` was rebuilt: the script is now multi-line with proper
statement termination, and loads without error.

### 2.2 Stray `<` destroys the one complete answer (critical)

`#a_risk_1` renders as an **empty box**. The source text uses bare `<` characters where
bullets belong:

```html
<pre>Provide a common framework ... <Reduce identified risks to an acceptable level. <Prevent or mitigate ...</pre>
```

Chromium parses `<Reduce` as an unknown start tag, consumes the rest of the paragraph as
attribute names, and swallows the closing `</pre>`. Confirmed in the DOM: an element
`<REDUCE identified risks to an acceptable level. <prevent …>` exists with 0 characters of
text. All of that answer's content is invisible.

*Fix:* escape as `&lt;`, or (better) mark the bullets up as a `<ul>`.

**Applied.** The bullets are now real `<ul>/<li>` markup. No unknown elements remain
in the parsed DOM.

### 2.3 The file is 87% placeholder (critical)

68 answer blocks; **59 contain literal placeholders** — `[Exact text preserved]`,
`[Exact PEAR content preserved]`, `[Exact roles text preserved]`. Only 9 have real content,
and one of those nine is the broken one above. Two authoring comments left in the source
confirm the file was never finished:

```html
<!-- Due to message size, the following sections are summarized with placeholders that
     indicate exact text preserved. In the file, you should paste the exact text just
     like the earlier sections. -->
```

The page nonetheless tells the reader *"All content below preserves your exact wording."*

**Applied.** All 69 questions now carry real answers — 57,145 characters across 404
list items, zero placeholders. Global-module answers come from Assessor Guide Rev 3.0;
asset-specific answers come from the Hebron/Hibernia material and are labelled as such.

### 2.4 ~30,000px of horizontal scroll

`document.documentElement.scrollWidth` is **30009px** against a 1280px viewport. Answers are
in `<pre>` with no `white-space: pre-wrap`, and each answer is a single unbroken line.

*Fix:* `pre { white-space: pre-wrap; overflow-wrap: anywhere; }`

**Applied.** `scrollWidth` is now 1280px at a 1280px viewport and 390px at 390px, with
every answer expanded.

### 2.5 Smaller items

- Title says *"(Test Mode)"* but the page defaults to Study Mode.
- The init handler calls `toggleMode()` twice to reach the default state; setting the state
  directly would be clearer and wouldn't depend on an even number of calls.
- `filterQA()` reads `b.innerText`, which excludes `display:none` content — so in Test Mode
  the search only matches question text, never answers.
- The search `<input>` has no `<label>` or `aria-label`.
- A typo carried over from the source: *"the risk of keeping the **like** in service"* → *line*.

**Applied.** All of the above, including a labelled search input, a search that matches
answer text while hidden in Test Mode, and a title that no longer contradicts the default mode.

**Resolution:** finished rather than deleted, at the owner's direction. `Loft.html` was rebuilt
from the Assessor Guide: 69 questions, 69 answers, no placeholders, semantic list markup, a
working Study/Test mode toggle, and search that matches hidden answer text. It is the only one
of the three that covers both the CAS and CVPE routes where their answers differ.

---

## 3. `LOFT Training Flip Card.v1.html` — good, with one real bug

The strongest artifact here: 88 cards across 10 categories, no console errors, keyboard
shortcuts, filters, per-card status, and a clean responsive layout.

| Category | Cards | Knowledge / Scenario / Asset |
|---|---|---|
| Risk Management | 16 | 11 / 1 / 4 |
| Training | 6 | 5 / 0 / 1 |
| Operating Procedures | 11 | 7 / 2 / 2 |
| Critical Equipment | 7 | 3 / 3 / 1 |
| Alarm Management | 6 | 3 / 1 / 2 |
| Work Management | 15 | 6 / 7 / 2 |
| Management of Change | 7 | 4 / 2 / 1 |
| Incident Investigation | 7 | 2 / 1 / 4 |
| Environmental | 7 | 2 / 3 / 2 |
| Emergency Response | 6 | 0 / 1 / 5 |

### 3.1 Shuffle corrupts your progress (high)

`cardStatus` is keyed by position — `cardKey(cat, idx)` → `"Risk Management__0"` — but
`shuffleCards()` reorders `CARDS[currentCat]` **in place**. After a shuffle, every mark points
at whatever card now occupies that index.

Reproduced: marked *"What is the intent of the RAM Process?"* as Known → `{"Risk Management__0":"done"}`.
After `shuffleCards()`, index 0 is *"ASSET SPECIFIC: How is the close-out of Risk Assessment
action items confirmed?"* — which now shows the green Known dot, while the card actually
studied shows as unseen. The header "Known / Review" counters stay numerically right, so
nothing looks wrong.

*Fix:* key `cardStatus` on a stable card identity (e.g. a hash of `card.q`, or an `id` field
added to each card) rather than array index. Shuffle a separate index array and leave `CARDS`
untouched.

**Applied.** Each card now gets a stable id hashed from its category and question text, and
`cardStatus` is keyed on that. Regression test: mark a card, shuffle, and the mark stays on
the same question (verified — key identical before and after, exactly one card flagged).

### 3.2 Biased shuffle

`[...cards].sort(() => Math.random() - 0.5)` is an inconsistent comparator; the resulting
permutation is not uniform and the behaviour is implementation-defined.

*Fix:* Fisher–Yates.

**Applied.**

### 3.3 Progress is lost on reload

`cardStatus` lives only in memory. For a tool used across multiple study sessions,
persisting to `localStorage` (as the third file already does for its own state) would be a
meaningful improvement.

**Applied.** Progress persists to `localStorage` and survives reload (verified). A reset
control was added next to shuffle, since progress is now durable.

### 3.4 Off-by-one under the "Needs Review" filter

In `markCard()`, marking a card **Got It** while the review filter is active removes it from
`filteredIndices`. `buildQList()` then rebuilds that array, so `currentIdx` already points at
the next card — and the trailing `navigate(1)` advances a second time, skipping a card.

**Applied.** `markCard` now checks whether the card is still in the filtered list and only
advances when it is.

### 3.5 Answer text can't be selected

`.card-wrapper` has `onclick="flipCard()"`, so any click inside the scrollable answer body
flips the card away. Selecting or copying an answer is not possible.

*Fix:* ignore clicks that land inside `.card-answer-body`, or that occur when
`window.getSelection().toString()` is non-empty.

**Applied.** Verified: with 426 characters selected, a click no longer flips the card.

### 3.6 Smaller items

- No `<h1>`; the title is a `<div class="logo-title">`. Poor document outline for assistive tech.
- `.card-wrapper` is a `div[onclick]` with no `role`, `tabindex`, or `aria-*`. The global
  Space shortcut partly compensates, but screen readers get nothing.
- `.main { height: calc(100vh - 130px) }` hard-codes the header height; the header wraps on
  narrow viewports and the layout overflows.
- Fonts load from `fonts.googleapis.com`. If this is used offshore or on an air-gapped
  network it will silently fall back — worth embedding or accepting explicitly.

**Applied** (except the font CDN): the title is now a real `<h1>`; the card has
`role="button"`, `tabindex`, `aria-label` and `aria-pressed`, and responds to Enter; header
height is measured at runtime instead of hard-coded. The Google Fonts link is **left as is** —
it was confirmed to fail cleanly offline during testing and fall back to the declared stacks,
so it degrades rather than breaks.

---

## 4. `LOFT_Assessment_Study Use Google Chrome20260212.html` — usable, several defects

The most complete of the three: 19 sections, a 44-term glossary, and links into the source
material.

### 4.1 One TOC entry is a dead link (high)

The list item targets `data-section="verification"`, but the section is
`id="verification-assessment-process"`. Clicking **1.5 Verification and Assessment Process**
matches nothing, so `getElementById` returns `null` and nothing happens — no scroll, no error.
The other 18 entries all match.

*Fix:* change the attribute to `data-section="verification-assessment-process"`.

**Applied.** All 19 TOC entries now resolve; clicking 1.5 scrolls and highlights.

### 4.2 The `.active` section mechanism does nothing

Both scripts add and remove `.active` on `<section>` elements, but **no CSS rule keys off it**
for sections — the only `.active` rule in the stylesheet is
`.active + .glossary-definition { display: block }`, which is for glossary terms. All 19
sections are visible at all times (verified: 19 of 19 have non-zero height after a TOC click).
Either the show-one-section-at-a-time design was dropped and the code is dead, or the CSS was
lost. Reusing `.active` for two unrelated purposes is also asking for a future collision.

**Applied.** Sections stay visible — that reads better for a study guide than hiding 18 of
19 — and the TOC now scrolls to the target and highlights it via a dedicated
`.section-current` rule, so the glossary's `.active` is no longer overloaded.

### 4.3 The overlay is invisible and unreachable (dead code)

`document.createElement('div')` with `id="overlay"` is appended to `<body>`, and `.active` is
toggled on it — but **there is no `#overlay` rule in the stylesheet**. Measured:
`{x:0, y:35104, width:1280, height:0}` — zero height, parked at the bottom of a 35,000px
document. Its click handler can never fire.

This matters because of what the toggle does: open the glossary, and the script sets
`toc.style.pointerEvents = 'none'`. With no working overlay to click, **the table of contents
becomes completely unusable while the glossary is open**, and the only way out is the
"Hide Glossary" button.

**Applied.** `#overlay` now has real CSS (verified 1280×900 and visible when open), clicking
it closes the glossary, and Escape does too.

### 4.4 Inconsistent margins between the two collapse paths

The button's collapse path sets `mainContent.style.marginLeft = '300px'`; the (unreachable)
overlay path sets `'180px'`. They should agree. Both also override the stylesheet's
`main.collapsed { margin-left: 200px }` with inline styles, making that rule dead. Layout
geometry is currently split across CSS and three places in JS.

**Applied.** All inline `marginLeft` writes are gone (0 remaining); geometry is driven by
`--toc-w` / `--glossary-w` custom properties, and one `setGlossary(open)` function owns the
state for every path.

### 4.5 The toggle button covers the table of contents

`#glossaryToggle.collapsed { left: 10px }` places the button at x 10–161, inside the TOC's
0–213px column — and the script forces the collapsed state on load, so this is the **default**
appearance. Confirmed in a screenshot: "Show Glossary" sits on top of the "Contents" heading.

**Applied.** The button sits at `calc(var(--toc-w) + 10px)`; measured left edge 210px against
a TOC right edge of 200px.

### 4.6 The `<h1>` is clipped by the sidebar

`<header>` is full-width and unindented while `#toc` is `position: fixed` over it, so the
page title renders as "**…OFT Assessment Study Guide**" at 1280px.

**Applied.** The header is offset by the sidebar width; the `<h1>` now starts at 224px, clear
of the TOC.

### 4.7 Malformed markup

Tag counts across the file:

| Tag | Open | Close | Delta |
|---|---|---|---|
| `<div>` | 376 | 320 | **56 unclosed** |
| `<p>` | 82 | 131 | **49 stray closers** |
| `<ul>` | 79 | 103 | **24 stray closers** |
| `<li>` | 524 | 538 | **14 stray closers** |
| `<strong>` | 80 | 85 | **5 stray closers** |

Also `<h2><strong>2.0 Process Safety Knowledge Requirements</h2>` — the `<strong>` is never
closed. Browsers recover from all of this, but it makes the file fragile to edit and unsafe to
process with any non-browser tool. There are also 96 `.question` elements against 101
`.answer` elements.

**Applied**, on a second attempt, after finding the actual cause.

The first attempt duplicated the entire body (38 sections instead of 19, text doubled to
191,889 characters) and was reverted. The cause was not the approach but the boundaries:
the file contains a **premature `</body></html>` at byte 15957**, and the slice
`<body> … </body>` therefore captured only the first 10KB — the header, glossary and first
script. The real content, the entire TOC and all 19 sections, sits *after* the document's
closing tags. Writing the full serialized body into that 10KB slot left the original content
in place below it, hence the duplication.

Structurally the file was:

```
<html><head>…</head>
<body> header, glossary sidebar, script </body></html>   <-- document "ends" here
<nav id="toc">…</nav>                                    <-- but content continues
<main id="mainContent"> 19 sections …                    <-- never closed
```

Measured against the real end of file rather than that stray tag, the damage was larger than
the original tag counts suggested: **81 elements left open at EOF** (77 `<div>`, 2
`<section>`, `<main>`, `<p>`), **76 closed only implicitly**, and **184 stray closing tags**
(64 `</p>`, 55 `</ul>`, 22 `</div>`, 21 `</li>`, 19 `</strong>`, 3 `</a>`).

The fix replaces everything from `<body>` to EOF with the parser's own serialization of the
tree, then closes the document properly. Result: every tag balanced — `div` 377/377, `p`
145/145, `ul` 79/79, `li` 524/524, `section` 19/19, `strong` 160/160, `main` 1/1, one `<body>`
and one `<html>`.

Verified equivalent, not merely valid: the rendered `textContent` is **byte-for-byte
identical** at 98,943 characters, with section count, question count, answer count, glossary
terms, links, TOC items, section ids and link targets all unchanged, and the glossary, TOC
and layout behaviour re-tested after the rewrite.

### 4.8 Debug logging left in

Five `console.log` calls in the TOC handler (`'TOC item clicked:'`, `'Target section ID:'`,
`'Added active class to:'`, …).

**Applied.** Zero `console.log` calls remain.

### 4.9 Dead localStorage code

The bottom of the file iterates `document.querySelectorAll('textarea')` to save and restore
notes. **There are zero `<textarea>` elements in the document.** Either the note-taking
feature was removed and its persistence code was left behind, or the textareas were never
added — worth deciding which, because a note field per section would be genuinely useful here.

**Applied.** The dead code is removed. A per-section note field is a reasonable future
addition but was out of scope here.

### 4.10 Filename

`LOFT_Assessment_Study Use Google Chrome20260212.html` embeds an instruction and a date in the
filename, and contains spaces. Nothing in the file requires Chrome specifically; it renders
the same in any modern engine. Suggest `loft-assessment-study-guide.html` with the version
already stated on the page ("Version 1.3: July 2025").

**Not applied.** Renaming the file breaks any existing bookmark or shortcut, and that is the
owner's call rather than a defect to fix unilaterally.

---

## 5. Content accuracy vs. the source documents

These are the findings most likely to affect an actual assessment outcome. Every "Source"
quote below is from a file committed in this repository.

### 5.1 Assessment window: 60 vs 90 days (highest priority)

| | Text |
|---|---|
| **`Training CriticalE and Expectations .pdf`** | "[E] Section 12 Personnel assigned to a LOFT Process Safety position should complete the LOFT Process Safety assessment **within 90 days** of assuming the position." |
| **Assessor Guide Rev 3.0** | "…identify a target timing for the verification – target should be **within 90 days** of assuming position" |
| **Study guide HTML §1.1** | "It is expected that this is conducted **within 60 days** of assuming the position." |
| **Study guide HTML §1.3** | "…target should be **within 60 days** of assuming position." |

The HTML contradicts a `[E]` Expectation in the UBP, in two places. This should be corrected
or, if a Business Unit has deliberately set a tighter local target, stated as such.

**Applied.** Both occurrences now read 90 days. Note that the file contains a third and a
fourth "60 days" — the Long Term Temporary Defeat thresholds — which are **correct** per the
source and were deliberately left untouched. A blanket find-and-replace here would have
introduced two new errors.

### 5.2 Role titles substituted throughout

> **Correction.** The first version of this review recommended renaming
> "Asset Manager" → "Site Manager". **That was wrong**, and it was based on reading the
> Risk Management section alone. The Assessor Guide glosses the abbreviations directly
> in two other places, which settles the mapping:
>
> - Long Term Temporary Defeat: `AM (Operations Manager)` … `PM (Site Manager)`
> - SIMOPS deviations: "Level 2 by the **Operations Manager** and Level 3 by the **Site Manager**"
> - Risk Management: "Role of the TLS (**Operations Manager**)"
>
> So the escalation ladder is PIC → AA → **Operations Manager (AM / TLS)** → **Site Manager (PM)**.
> The HTML files use a consistent local convention — AM = "Asset Manager", PM = "Production
> Manager" — for the *same two roles*. The correct mapping is therefore:

| HTML files said | Assessor Guide Rev 3.0 says |
|---|---|
| Asset Manager | **Operations Manager** |
| Production Manager | **Site Manager** |
| Operations Superintendent (SIMOPS Level 2) | **Operations Manager** |

Raw counts before the fix:

| Term | Assessor Guide Rev 3.0 | Taskbook Rev 3.4 | `Loft.html` | Flip card | Study guide |
|---|---|---|---|---|---|
| Site Manager | 13 | 11 | 0 | 0 | 0 |
| Operations Manager | 7 | 5 | 0 | 0 | 0 |
| Asset Manager | 0 | 1 | 4 | 11 | 14 |
| Production Manager | 0 | 1 | 1 | 11 | 10 |

**Applied.** Corrected per-occurrence, not by global find-and-replace, because the same
words are correct in asset-specific answers and wrong in global-module answers:

- **Global-module answers** (where the Assessor Guide is authoritative) were corrected to
  the source titles — 19 occurrences in the flip card, 15 in the study guide, and all of
  `Loft.html` as rebuilt.
- **Asset-specific answers** keep their local titles, because no source document in this
  repository governs them: the Asset Specific module (`UPBP-410`) is a question template
  with the answers left for the Business Unit to supply. These are the KPI scenario owner,
  the Problem Well Reporting email approvals, the PPC sign-off, the platform incident
  notification chain, the IMT/ER roles, and the assessment-team composition.
- Each file now states the AM/PM mapping on the page, so a candidate reading either
  convention knows what the other means.

One item worth a second opinion: in the source, the SLS is told to "immediately inform
**Site Manager**" of a failed critical safeguard, while the TLS is told to inform the
**Site Manager** too. The HTML had the SLS informing the Asset Manager (i.e. the TLS) and
the TLS informing the Production Manager (i.e. the Site Manager) — a cleaner one-level-up
escalation. The source wording has been followed, but if the intent really is
single-step escalation, the *source* is what needs amending.

### 5.3 Risk Management role lists diverge from the source

Comparing the Assessor Guide Rev 3.0 SLS/TLS lists against `Loft.html` and the flip card:

| Source (Rev 3.0) | HTML files |
|---|---|
| SLS: "**Charter risk assessments**" | *omitted from SLS* |
| SLS: "**Provide initial risk approval for Cat 3 risks**" | *omitted* |
| SLS: "Immediately inform **Site Manager**…" | "…inform **Asset Manager**" |
| TLS: "Charter risk assessments **waivers**" | "Charter risk assessments" (different scope) |
| TLS: "Provide initial risk approval for **Cat 2 and 1E** risks" | "initial approval for continued operations for **Cat 2 and 3** risks" |
| TLS: "Immediately inform **Site Manager**…" | "…inform **Production Manager**" |

`Cat 1E` appears in the source and in **none** of the HTML files or the glossary. The
glossary defines "Cat 1, Cat 2, Cat 3, Cat 4" but not `1E`.

### 5.4 Two source topics have no HTML coverage

- **Competency Assurance Standard.** The Assessor Guide has this as a full category
  (section 2, with its own Training and Operating Procedures question sets, used where a work
  area has not yet completed CVPE). None of the three HTML files has a CAS category — the flip
  card's 10 categories skip straight from Risk Management to Training.
- **Flag / Class (floating vessels).** Four questions in the source — Flag State and
  Classification Society roles, Annual Alignment Workshops, external exposures, and the
  decision to maintain Class. Zero occurrences of "Flag State" or "Classification Societ" in
  any HTML file. The source scopes these to "BUs with floating vessels e.g., FPSO, FSO", so
  excluding them for Hebron/Hibernia may well be correct — but that scoping decision should be
  written down rather than inferred from an absence.

### 5.5 Minor wording

- Flip card renders ALARP as "As Low As Reasonably Practicable"; the source (and `Loft.html`)
  say "As Low As **is** Reasonably Practicable". The glossary in the study guide uses the
  source form. Worth making the three consistent.
- Source Rev 3.0 says the guide covers "**ten** Process Safety categories" but then lists
  eleven (Risk Management … Emergency Response, with the last numbered "10"). This is a defect
  in the source document, inherited by the study guide's §1.1. Flag it upstream.

**Applied** for the ALARP wording (the flip card now matches the source's "As Low As **is**
Reasonably Practicable"). The ten-versus-eleven miscount is a defect in the **source
document** and has been left alone — correcting the study aids to disagree with the
controlling document would be worse than inheriting its error. It should be raised with the
Assessor Guide's owner.

**New finding, not fixed:** the study guide cites the Corporate Risk Matrix as
**TMEE211**, while Assessor Guide Rev 3.0 cites **TMEE330 Risk Matrix Application Guide**.
One of the two is out of date. This is a document reference rather than a role title, and
which revision is current cannot be determined from the material in this repository, so it
has been left as-is and is flagged here for the owner.

---

## 6. Repository documentation

### 6.1 `README.md` describes a different project

> "Loft — A modern application platform."

This repository contains no application. It is a collection of LOFT process-safety training
material. The **Project Structure** block lists only `README.md`, `CONTRIBUTING.md` and
`.gitignore`, omitting all three HTML files and all six source documents — i.e. everything the
repository is actually for. There is also no `LICENSE` file despite the README asserting MIT.

The README should say what this is (study aids for the LOFT Process Safety competency
assessment), which file to open for what, which source document each aid derives from, and
which revision each was built against.

**Applied.** `README.md` was rewritten: what the repository is, a table of the three study
aids and what each is best for, a table of the five source documents with the note that the
source governs on any disagreement, the 90-day window, the AM/PM role mapping, and the CAS
and Flag/Class scope decisions. The unsupported MIT claim was removed rather than adding a
`LICENSE` — this is controlled corporate material, not MIT-licensed work.

### 6.2 `CONTRIBUTING.md` doesn't fit the content

It asks contributors to "Add tests for new functionality" and "Follow existing code style".
For this repository the meaningful guidance is different: which source document is
authoritative, that content changes must be traceable to a specific `UPBP-…` revision, and who
signs off on a technical-content change. A wrong answer here is a safety-training defect, not a
failing test.

**Applied.** `CONTRIBUTING.md` was rewritten around source traceability: name the governing
document and revision in the commit message, never paraphrase approval authorities or
thresholds, keep global and asset-specific content distinct, and the warning about the bulk
re-serialization trap in §4.7.

### 6.3 `.gitignore` is a generic template

It covers `node_modules/`, `dist/`, `coverage/`, `.nyc_output/` — none of which apply. Harmless,
but it reinforces the impression that the repository scaffolding was generated for a software
project and never adapted.

**Not applied.** Harmless as noted, and trimming it has no benefit that justifies the churn.

### 6.4 Duplicate source document

`UPBP-400-EN-02-LG-GBL-LOFT TASKBOOK Rev 3.4.docx` and
`UPBP-410-EN-02-LG-GBL-LOFT TASKBOOK Rev 3.4 _1_.docx` have **byte-identical extracted text**
(86,837 characters each; the binaries differ only in packaging). One is a copy filed under the
wrong document number, and the `_1_` suffix suggests a duplicated download. Keep one.

**Not applied.** Deleting a controlled document — even a duplicate — is the document owner's
call, not a reviewer's. `README.md` lists the `UPBP-400` copy as the Task Book of record.

---

## 7. Handling of controlled material

**Repository visibility: private** (confirmed by the owner, 2026-08-20). This closes the main
exposure question — the notes below are for ongoing handling, not an open issue.

This repository contains material that is marked and structured as ExxonMobil-internal:

- Six controlled documents with UPBP document numbers and revision levels.
- 20 links into corporate intranet hosts — `ishareteam1/2/6/8.na.xom.com`,
  `teamwork1.exxonmobil.com`, `us1.aconex.com` — four of which have `/Proprietary/` in the path.
- Named asset references (Hebron, Hibernia) alongside process-safety scenarios and approval
  thresholds.

Two things still worth keeping in view:

- **Visibility is a setting, not a property.** Flipping this repository to public later would
  expose the full history, not just the current tree. Anyone with that ability should know
  what is in here. The same applies to forks and to adding outside collaborators.
- **The intranet links will not resolve off the corporate network.** Roughly a fifth of the
  study guide's supporting references are unreachable to a candidate studying from home or
  offshore. Where a link carries information the candidate actually needs, consider
  summarising it inline rather than relying on the link alone.

---

## 8. What was done

1. **Repository visibility** — confirmed private by the owner (§7).
2. **60 → 90 day contradiction** — fixed in both places, TD thresholds preserved (§5.1).
3. **Role titles** — corrected to source terms per-occurrence across all three files, with the
   mapping documented on each page; asset-specific answers left in local terms (§5.2).
4. **Flip card shuffle** — fixed and regression-tested; progress now persists (§3.1–3.5).
5. **Study guide navigation and layout** — dead TOC link, overlay, geometry, header clipping,
   debug logging and dead code all fixed (§4.1–4.9).
6. **Study guide markup** — premature `</body></html>` found and the document structure
   repaired; all tags now balanced, rendered text byte-for-byte identical (§4.7).
7. **`Loft.html`** — rebuilt with all 69 answers authored from source (§2).
8. **`README.md` / `CONTRIBUTING.md`** — rewritten for what the repository actually is (§6).

## 9. Still open for the owner

- **§5.2 SLS escalation.** The source has both SLS and TLS informing the Site Manager. The
  study aids now follow the source, but if single-step escalation was intended, the source
  needs amending.
- **§5.5 TMEE211 vs TMEE330.** Conflicting Corporate Risk Matrix references between the study
  guide and Assessor Guide Rev 3.0. Cannot be resolved from material in this repository.
- **§5.5 "ten categories" miscount** in Assessor Guide Rev 3.0 — a source document defect.
- **§5.4 CAS and Flag/Class coverage** — now documented as scope decisions in `README.md`;
  worth confirming those decisions are correct.
- **§4.10 filename** and **§6.4 duplicate Task Book** — both owner's calls, left alone.
