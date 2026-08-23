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
  the source titles first — 19 occurrences in the flip card, 15 in the study guide, and all
  of `Loft.html` as rebuilt.
- **Asset-specific answers were initially left in local titles**, because no source document
  in this repository governs them: `UPBP-410` is a question template with the answers left
  for the Business Unit to supply.

**Superseded &mdash; the split was removed (August 2026).** Leaving the two conventions
side by side meant a reader met "Operations Manager" in one answer and "Asset Manager" in
the next, with the mapping explained only in the collapsed glossary. The asset then
confirmed that **Operations Manager and Site Manager are the correct titles**, which
removed the reason for the split. A further 13 occurrences in asset-specific answers were
converted (10 "Asset Manager", 3 "Production Manager"), covering the KPI scenario owner,
the Problem Well Reporting email approvals, the PPC sign-off, the platform incident
notification chain, the IMT/ER roles, and the assessment-team composition.

The file now uses Assessor Guide titles throughout &mdash; 19 "Operations Manager", 18
"Site Manager", zero of either old term. The glossary records that older material calls the
same two roles Asset Manager and Production Manager, so anyone arriving from the previous
documents can reconcile them.

One item was raised for a second opinion: in the source, the SLS is told to "immediately
inform **Site Manager**" of a failed critical safeguard, while the TLS is told to inform
the **Site Manager** too. The HTML previously had the SLS informing the Asset Manager
(i.e. the TLS) and the TLS informing the Production Manager (i.e. the Site Manager) — a
cleaner one-level-up escalation.

**Decision: follow the Assessor Guide.** The owner directed that the source governs, so
both roles inform the Site Manager, exactly as Rev 3.0 states (lines 87 and 96). Verified
in all three aids. If the intent really was single-step escalation, that is a change to
make in the *source document*, not in the study aids — a candidate should answer what the
assessor is reading from.

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
  any HTML file. The source scopes these to "BUs with floating vessels e.g., FPSO, FSO".

  **Closed.** The asset confirmed (August 2026) that Hebron and Hibernia are not floating
  vessels, so the exclusion is correct. It is now written down in `README.md` rather than
  inferred from an absence.

### 5.5 Minor wording

- Flip card renders ALARP as "As Low As Reasonably Practicable"; the source (and `Loft.html`)
  say "As Low As **is** Reasonably Practicable". The glossary in the study guide uses the
  source form. Worth making the three consistent.
- Source Rev 3.0 says the guide covers "**ten** Process Safety categories" but then lists
  eleven (Risk Management … Emergency Response, with the last numbered "10"). This is a defect
  in the source document, inherited by the study guide's §1.1. Flag it upstream.

**Applied** for the ALARP wording (the flip card now matches the source's "As Low As **is**
Reasonably Practicable").

**Decision on the ten-versus-eleven miscount: follow the Assessor Guide.** The study guide
carries the source's own wording, "ten Process Safety categories", verified against Rev 3.0.
Correcting the study aids to disagree with the controlling document would be worse than
inheriting its error, and the owner confirmed the source governs. This stays as a defect to
raise with the Assessor Guide's owner rather than an edit to the study aids.

**Corporate Risk Matrix citation &mdash; resolved by following the source.** The study
guide cited the Corporate Risk Matrix as **TMEE211**; Assessor Guide Rev 3.0 cites the
**Corporate SSH&E Risk Matrix (as defined in TMEE330 Risk Matrix Application Guide)**.

Characterising this as "one of the two is out of date" was probably wrong. The titles
differ, which suggests these may be two different current documents &mdash; TMEE211 the
*matrix* itself, TMEE330 the *application guide* that explains how to apply it. Nothing in
this repository settles it: neither PDF nor either taskbook mentions TMEE at all, the
Assessor Guide carries no effective date, and the `.docx` metadata is unusable (all four
files show 2026-08-19, the date they were re-saved, not authored). Document numbers are
library identifiers, not version numbers, so 330 cannot be assumed newer than 211.

**Applied**, at the owner's direction: all three aids now use the Assessor Guide's
citation, on the reasoning that the assessor works from that document. The flip card
previously named the matrix with no document number at all and now carries the same
citation, so all three agree.

Still worth a lookup in the controlled document library: if TMEE211 and TMEE330 are
distinct current documents, citing both would be more accurate than citing either alone.

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

## 9. Open items

Everything in this review has been actioned or decided. What follows is not outstanding
work in this repository.

**Standing decision: where a study aid and the Assessor Guide disagree, the Assessor Guide
governs.** The owner confirmed this. A candidate is assessed against what the assessor is
reading, so a study aid that "corrects" the controlling document would set them up to give
an answer the assessor marks wrong. Where the source itself looks defective, the fix belongs
in the source.

Applied to the two items previously carried here:

- **SLS / TLS escalation (§5.2)** — the source has both roles informing the Site Manager.
  Followed as written; verified in all three aids.
- **"ten categories" miscount (§5.5)** — Rev 3.0 says "ten" then lists eleven. The study
  guide carries the source's wording unchanged.

**One suggestion, not a defect:** confirm in the controlled document library whether
**TMEE211** is superseded by **TMEE330** or is a separate current document (§5.5). All three
aids now use the Assessor Guide's TMEE330 citation either way; if both are current, citing
both would be more accurate.

**Two source-document defects worth raising with the Assessor Guide's owner**, neither of
which is repo work:

1. The ten-versus-eleven category miscount.
2. The SLS/TLS escalation wording, if single-step escalation was the intent.

---

## 10. Source-question reconciliation (added after the review)

Every question in the source documents was checked against all three study aids —
101 source questions (67 in Global Module Assessor Guide Rev 3.0, 34 in Asset Specific
Task Book UPBP-410 Rev 3.2). Coverage was verified by keyword probe against rendered
text; fuzzy title matching alone proved unreliable and produced false gaps.

**Five Global Module questions were missing from the flip card and the study guide.**
All five existed only in `Loft.html`, because they were authored from source during its
rebuild. They have now been added to both:

| Question | Was in | Now |
|---|---|---|
| Purpose of a temporary defeat, and what drives the approval level | `Loft.html` only | all three |
| How often LTIs are reviewed; what triggers engaging the Operations Manager | `Loft.html` only | all three |
| Emergency management expectations of O&M / FLS / SLS / TLS / Site Manager | `Loft.html` only | all three |
| Tactical Response Plan — definition, objectives, phases | `Loft.html` only | all three |
| Objectives of each TRP phase | `Loft.html` only | all three |

The temporary defeat question mattered most: the source carries an explicit teaching
note that *"TD approval escalation is **not solely time based**, but escalation should
occur immediately dependent on the complexity of the defeat."* A candidate studying
only the flip card or study guide learned the 7/30/60-day ladder and never met the point
that complexity alone can force immediate escalation.

**Two factual divergences found and corrected**, both in the DWCM answer:

| | Was | Source Rev 3.0 |
|---|---|---|
| DWCM review of Long Term Isolations (both files) | "weekly" | **monthly** |
| LTI escalation to Operations Manager | *question absent* | minimum **6-month interval** |

**Flag / Class remains the only deliberate omission, now confirmed.** Four questions the
source scopes to "BUs with floating vessels e.g. FPSO, FSO". The asset confirmed in
August 2026 that Hebron and Hibernia are **not floating vessels**, so these questions do
not apply and are correctly absent. This is no longer an open assumption — recorded in
`README.md`.

**CAS vs CVPE route — resolved.** The Assessor Guide carries two variants of several
Operating Procedures and Training questions, gated by the line *"The following section
only applicable if Your Work Area has not completed CVPE and is still using the CAS
standard ... or Skip to Chapter 3."* The asset confirmed (August 2026) that
**Hebron/Hibernia has completed CVPE**, so the Training and Competency UBP answers apply
and the CAS section should be skipped.

The flip card and study guide carried **only** the CAS variant, so three answers were
outright wrong for this asset, and three questions were being studied from a section the
source says to skip. Corrected across all three aids:

| Question | Was (CAS) | Now (CVPE) |
|---|---|---|
| Procedure revalidation | IC 3 years / Normal 5 years / Work Aid BU-defined | successfully used in the field; **not to exceed 36 months** |
| Deviation approval | IC = Site Manager / Normal = SLS / Work Aid = FLS | stop work; documented approval from the **SLS** [or BU defined position] |
| New or revalidated procedure | SME + user validate, FLS/SLS/TLS endorse, Site Manager approves | technically verified, site validated, endorsed **FLS**, approved **SLS** |
| Training objective | objective of the Competency Assurance Standard (CAS Manual) | objective of the **Training and Competency UBP** |
| Competency roles | CAS list, including a Site Manager row | UBP list for O&M / FLS / SLS / TLS (no Site Manager row) |
| Tools and triggers | tools and triggers only | adds the **DIF (Difficulty, Importance, Frequency)** calculation |

Three questions exist **only** on the CAS route — the Integrity Critical Procedure
definition, the global IC examples list, and the night-time IC error scenario. Rather
than delete them (IC procedures remain a live concept in the asset-specific material),
they are retained and marked as not assessed under the current UBP.

Superseded answers are shown alongside the applicable one and colour-coded in all three
files, so a candidate who has seen the older material can tell which is which rather than
simply finding it missing.

Counts after this pass: `Loft.html` 69 questions, flip card **93** cards (was 88),
study guide **101** questions (was 96).

### 10.1 Why the three files have different question counts

They are not meant to be equal, and forcing them to be would make the aids worse.

| | Total | Global module | Asset specific |
|---|---|---|---|
| `Loft.html` | 69 | 54 | 15 |
| Flip card | 93 | 69 | 24 |
| Study guide | 101 | 61 | 40 |

Two things drive the spread:

- **Asset-specific depth.** The Asset Specific Task Book (UPBP-410) holds 34 questions the
  Business Unit answers locally. The study guide covers those in depth, the flip card
  partially, `Loft.html` least. This is the largest factor.
- **Granularity.** The flip card deliberately splits multi-part questions so each card drills
  one thing &mdash; the source's single "Describe your role in the RAM process" becomes a
  separate SLS card and TLS card. `Loft.html` goes the other way, merging §1.1&ndash;1.6 into
  one reading block.

**What should match is topic coverage, not item count.** Verified with 57 curated topic
probes (multiple alternate phrasings each, so paraphrase does not cause false misses):
**57 of 57 topics present in all three**.

A first attempt at this used auto-generated 5-gram fingerprints taken from the source answer
text. That method was discarded &mdash; it demands near-exact wording and flagged topics as
missing that were verifiably present, because the aids legitimately paraphrase. The probe
list used is kept in `tools-coverage-check.py` so the check is repeatable.

**One real gap was found and fixed.** The breaking-containment single-valve-isolation
scenario was answered from two different authorities: `Loft.html` gave the Global Module
answer (flange class &ge;300 &rarr; Operations AA witnesses zero energy; &lt;300 &rarr;
Operations AO, and it cannot be delegated to the Permit Holder), while the flip card and
study guide gave only the Hebron/Hibernia process (Appendix A WMS Addendum, risk screening,
third-party engineer's stamp, Permit Vision, OIM signature, AA at first break). Both are
correct but answer different things, and the flange-class rule is a Global Module answer an
assessor can ask. All three now carry both, each labelled with its authority.

- **§4.10 filename** and **§6.4 duplicate Task Book** — both owner's calls, left alone.


---

## 11. Consolidation to a single file (2026-08-20)

The three study aids were merged into one: **`LOFT-Process-Safety.html`**.
`Loft.html` and `LOFT Training Flip Card.v1.html` were removed; both remain in git
history.

**Why.** They held overlapping copies of the same material, so every content
correction had to be made two or three times. Measured over this review's commits,
**5 of 7 content commits touched more than one HTML file**:

| Fix | Files touched |
|---|---|
| Role titles, 90-day window, initial defects | 3 |
| CVPE route alignment | 3 |
| Five missing questions + DWCM cadence | 2 |
| Global flange-class answer | 2 |
| TMEE330 citation | 2 |

That duplication is what produced the drift this review had to clean up in the first
place &mdash; the flip card and study guide disagreeing on role titles, on the CAS/CVPE
route, and on whether LTIs are reviewed weekly or monthly.

**What replaced them.** One file with three modes over a single set of questions:

- **Guide** &mdash; questions with model answers by section, glossary, source links.
- **Test** &mdash; answers hidden, revealed per question, with search.
- **Cards** &mdash; one question at a time, flip, *Got it* / *Needs review*, shuffle,
  category filter, keyboard shortcuts.

Nothing is duplicated: all three modes read the same DOM, so a correction lands
everywhere at once. Assessor notes and outcomes work across modes &mdash; a note typed on
a card is the same note shown in Guide mode.

**Two defects found and fixed while building it**, both caused by the document's
nested `<section>` structure:

- `closest('section')` attributed **79 of 100 questions to the wrong category**,
  because 11 sections are nested rather than siblings. Replaced with a document-order
  walk that tracks the most recently opened section. Categories now split
  17/6/11/7/7/20/8/7/7/9/1, summing to 100.
- Category chips were ordered by first question rather than section position, so 2.1
  preceded 2.0.

**Verification.** 100 questions, 106 answers, 100 note panels, 44 glossary terms, 19 TOC
entries with no dead links, no console errors, no horizontal overflow; all three modes
render; assessor save-to-file and reload round-trip confirmed; and
`tools-coverage-check.py` reports **57 of 57 Assessor Guide topics present**.

> The question count read 101 until section 13, because one of the divs was an empty
> shell holding another question's answer. Removing it did not remove a question.

The coverage tool was rewritten to be self-contained &mdash; it reads the HTML directly
and exits non-zero if a topic goes missing, so it can be run after any edit.


---

## 12. Repairing the nested question divs (completed)

**Done. 42 sites repaired, none reverted, rendered text byte-identical before and after.**

### The defect

48 of the 101 `.question` divs contained content that belonged outside them. They were
left unclosed in the source, so the browser's error recovery nested whatever followed
inside them. The worst held **53,757 characters, of which 49 were the actual question**;
one question div had swallowed half the document.

### Why it was worth fixing even though nothing was visibly broken

Every user-visible symptom had already been fixed in commit `765165f` &mdash; text
extraction ignored nested content, note panels were anchored per question rather than per
wrapper, and the search filter re-showed any ancestor of a match. What remained was markup
that nobody could hand-edit safely: opening the file in an editor, the boundary between
one question and the next was not where it appeared to be on screen.

### Why the first four attempts failed

Four bulk-flattening rules were tried. Each preserved the total text exactly (105,714
characters every time &mdash; nothing was ever lost) and each **reordered** some of it,
which is not acceptable in safety-training content.

| Attempt | Rule | Outcome |
|---|---|---|
| 1 | Move the first nested block and everything after it | Order preserved, but **6 questions emptied** |
| 2 | Move only children that are or contain a nested block | Text kept, but a section heading moved earlier |
| 3 | Move the nested blocks themselves, not their wrappers | Same heading reorder |
| 4 | Split at the first nested block in document order | New reorder elsewhere &mdash; a question label vanished from its position |

The reason each attempt found a new failure is that the source contains **at least four
distinct malformation patterns**, for example:

```html
<!-- question text inside an unclosed <strong>, so the answer nests inside it too -->
<div class="question"><strong>Describe the principles of the MOC process.<p></p>
  <div class="answer"> ... </div>

<!-- answer unclosed, so the next section heading is swallowed into the question -->
<div class="question">Together with the Person In Charge, attend the DWCM...<p></p>
  <div class="answer">The objective of the meeting is...   <!-- 2.7 heading ends up here -->
```

A rule that fixes one pattern reorders another, so no single rule was ever going to work.

### What did work: one question at a time, verified individually

Instead of one rule applied 48 times, each site was repaired on its own and the whole
document re-rendered and compared after every single change. The loop was:

1. Find the next `.question` div that still contains an `<div class="answer">`.
2. Close the question immediately before that answer, carrying any tags left open inside
   the question (`<strong>`, `<p>`, and so on) across the boundary so the following
   content keeps its formatting, and promote the rest back out to the question's parent.
3. Re-render the file in headless Chromium and extract the visible text.
4. Compare that text, character for character, against a baseline taken before any repair
   began, along with the counts of questions, answers, sections and TOC links.
5. **Identical &rarr; keep the change. Anything different &rarr; restore the previous
   file and move on.** No judgement call, no partial acceptance.

Each individual edit is small enough to read and check, and step 5 makes a bad edit cost
one skipped site rather than a corrupted document. That is the whole reason this worked
where the bulk rules did not: the four earlier attempts could only be evaluated after all
48 changes were already in, by which point a single reorder meant discarding everything.

### Result

- **42 of the sites repaired, 0 reverted.** The remaining 6 were already well-formed once
  their neighbours were fixed &mdash; no question div now contains an answer.
- Rendered text **identical**: 105,714 characters before, 105,714 after, byte for byte.
- Counts unchanged: 101 questions, 106 answers, 19 sections, 19 TOC links.
- Longest question div now **710 characters** including its own markup, down from 53,757.
  None exceeds 800.
- All tags balanced: `div` 426/426, `p` 187/187, `ul` 93/93, `li` 575/575, `section`
  19/19, `strong` 205/205, `main` 1/1.
- Full regression re-run afterwards: no console errors, 100 of 100 note panels correctly
  placed, search still returns one match for each probe, no horizontal overflow at any
  width, and `tools-coverage-check.py` reports **57 of 57 topics present**.

The markup can now be hand-edited: a question div starts and ends where the question
starts and ends.

---

## 13. Second audit pass (after the markup repair)

With the markup well-formed, a fresh audit could see structure the recovered tree had
been hiding. Four defects, all fixed; each change verified by re-rendering and comparing
the extracted text character for character against a baseline, as in section 12.
**Rendered text unchanged throughout.**

### One question had lost its answer

`Apply PEAR to the information in this briefing…` in Emergency Response had **no
answer**, and the next `.question` div was **empty** and held that answer:

```html
<div class="qa">
  <div class="question">Apply PEAR to the information in this briefing…</div>
</div>                          <!-- question ends here, with nothing -->
<div class="qa"><strong>
  <div class="question"></div>  <!-- empty shell -->
  <div class="answer">People … Environment … Asset … Reputation</div>
```

On screen it looked fine, because the answer rendered directly underneath. It was not
fine anywhere that walks the structure: the question carried no answer to reveal in Test
mode, no card back in Cards mode, and the empty div counted as a 101st question.

Merged into one block. The count is now **100 questions, 100 with answers, no empty
divs** — the file had 100 real questions all along.

### Two elements shared one `id`

`summaryTools` was emitted by both the summary panel and the module panel, so
`getElementById` could only ever reach the first. It was a CSS hook with no script
lookups, so it became a class, `.summary-tools`, in both emitters and both rules.

### A link had swallowed its own `target` attribute

One Aconex link was written with an unterminated `href`:

```html
href="…%3D0#/file target=" _blank"="" rel="noopener noreferrerr"
```

The browser recovered by ending the URL after `#/file target=` and inventing an
attribute called `_blank"`. The link pointed at a URL that cannot resolve. Repaired to
`href="…#/file" target="_blank" rel="noopener noreferrer"`, which also cleared the
`noreferrerr` typo in that link and one other.

### Everything else came back clean

No dead internal anchors, no unlabelled inputs, no missing `alt`, no heading-level
jumps, no console errors, and no typographic defects in the content — the only
doubled-word hit was two adjacent list items, and the `--` sequences are the source's
own style.

**One duplicate is deliberately left alone.** The preventative critical-safeguard list
appears twice under Risk Management, and the second copy also repeats part of the
mitigative list. It is asset-local content, so it is item 37 on
`ASSET-SPECIFIC-REVIEW-SHEET.html` for the asset to rule on, rather than something to
delete here.

### TMEE211 vs TMEE330 &mdash; narrowed

Previously carried as "confirm which is current". It can now be narrowed without the
controlled library: **TMEE211 appears in no source document in this repository.** It
existed only in the original uploaded HTML, and git history confirms it was never
introduced by a source. The Assessor Guide Rev 3.0 cites TMEE330 and nothing else, so
the study aid follows it.

What remains is not a conflict between two sources but a single question for the
library: whether the original author's TMEE211 citation was simply wrong, or referred to
a document since superseded. Either way the study aid is already correct.

### Source-document queries written up

The two Assessor Guide defects are now drafted as `SOURCE-DOCUMENT-QUERIES.md`, ready to
send to the document owner, with exact quotations and suggested wording. Working on it
turned up a likely explanation for the first: the eleventh category is **Competency
Assurance Standard**, which the guide elsewhere retires once a work area completes CVPE
— so "ten" is plausibly the count after CAS goes, written into an edition that still
carries it.

---

## 14. Study notes, and putting the assessment record behind a gate

Two changes, asked for together because they are the same idea: the file serves two
different people, and until now it only had furniture for one of them.

### The candidate had nowhere to write

Every question carried an **Assessor notes** box and nothing else. A candidate studying
had no place to record what tripped them up, so the only note-taking surface in the file
was the one meant for the assessment record — which is exactly the wrong place for it.

Every question now carries a **My study notes** box as well, above the assessor panel and
visually distinct (purple rather than blue). It saves as you type. **My notes** in the top
bar collects everything written, grouped by section, and prints.

**The two are kept completely apart**, which matters more than it sounds:

| | Study notes | Assessor notes |
|---|---|---|
| Storage key | `loft-study-notes-v1` | `loft-assessor-notes-v1` |
| File format | `loft-study-notes` | `loft-assessor-notes` |
| Panel | `.study-panel` | `[data-note-panel]` |
| Visible when locked | yes | no |

Each loader rejects the other's file by name, and loading an assessment record into the
study loader says so in those words rather than failing obscurely. Verified by writing
both kinds of note in one browser, exporting both, and checking each file for the other's
text and for the candidate's name: no leakage in either direction.

### The assessment record is now behind a password

The session bar, the per-question assessor panels, the module sheet and the summary are
hidden until unlocked with **Assessor access**. Default password `admin`; **Password**
changes it for that machine.

**It is a gate, not security, and the code and the README both say so in those words.**
The whole file is delivered to the browser — anyone who opens View Source can find the
check and bypass it. What it actually buys is that a candidate revising on a shared
machine does not wander into the assessment record, and that the two roles stay visibly
apart. Anything needing real protection belongs in the saved `.json`, not behind this.

Two deliberate choices:

- **Unlock lives in `sessionStorage`, not `localStorage`**, so closing the browser
  re-locks. On a shared offshore computer, a gate that stays open forever is not a gate.
- **Printing follows the mode.** Locked prints the candidate's study notes; unlocked
  prints the assessment record *without* them, because study material has no place in a
  competency record.

### Three defects found while building it

- **Search matched the new panels.** Both `ownText` helpers strip injected UI so it never
  reaches the index; `.study-panel` had to be added to both, and to `applyFilter`, or
  typing a word from your own note returned that question.
- **The notes view rendered under the mode bar and behind the glossary button.** Both are
  `position: fixed`. `#summaryLayer` already solved this with `inset: 44px 0 0 0` and
  `z-index: 1150`; `#studyLayer` now matches it. Written up in `CONTRIBUTING.md` so the
  next full-screen layer starts from the right numbers.
- **Four regression scripts broke**, all of them reaching for `#sess_candidate`, which is
  now gated. That was the change working. They unlock first now.

### Verification

Rendered content **byte-identical** at 106,350 characters — the change is CSS and two
script blocks, no content touched. 100 questions, 106 answers, 100 assessor panels and
100 study panels correctly placed, no console errors, no overflow from 360px to 1280px,
search still precise, all three modes and the full assessor flow (session, modules,
summary, save, reload, handover to a fresh browser) working, and 57 of 57 topics present.

### 14.1 Follow-up: you could not tell which mode you were in

The first version signalled assessor mode with a button label alone. From the middle of a
long page that is invisible, and the honest report was *"nothing changes"*. Three real
defects sat behind it.

**The state was not visible.** Now the mode bar turns green, a banner sits under it for as
long as the mode lasts — *"Assessor mode — the assessment record is visible and is being
saved"*, with a **Lock** button — and on first unlock the session bar is scrolled to and
flashed. The banner is a `role="status"` region, so it is announced rather than only seen.

**On a phone the button was off the screen entirely.** `#modeBar` scrolled sideways, so at
390px wide **Assessor access** sat at x=679 and **My notes** at x=373 — both past the right
edge, with nothing to suggest they existed. The bar now wraps onto a second row on narrow
screens instead of scrolling, `#modeHint` is dropped there, and the content offset moves
with it. All three buttons measured on screen at 390px, no horizontal scroll.

**The session bar hid its own first row.** `#assessSession` is `position: sticky` at
`top: 44px`, which was correct under the mode bar alone and wrong once the banner took the
next 34px — the Candidate and Position fields stuck *behind* it. The fix that matters is
not the number: every piece of fixed or sticky chrome (`#toc`, `#glossarySidebar`,
`#glossaryToggle`, `#assessSession`) now shifts in **one** `body.assessor-on` block, so a
future banner change cannot leave one of them behind. A first attempt set the offset on
the base rule and lost to a later rule of equal specificity, which is why it is stated
once, in the block that already owns the chrome offsets.

Verified: rendered content still byte-identical at 106,350 characters, coverage 57 of 57,
no console errors, no overflow from 360px to 1280px, and the gate, separation, banner,
password-change and full assessor flow all pass.

---

## 15. UPBP-410 Q3 had lost two words, and half its answer

Found while tracing which source question review-sheet item 37 belongs to. It belongs to
**Q3**, and Q3 itself was wrong.

**The question had been narrowed.** UPBP-410 Rev 3.2 asks:

> Are there any major wellbore integrity **or marine** related incident scenarios for your
> asset? Explain the details of those scenarios and both the preventative and mitigative
> safeguards in place related to those scenarios

The study aid had *"wellbore integrity related incident scenarios"* &mdash; `or marine`
deleted. Two words, and not cosmetic: it silently dropped half of an assessed question. A
candidate preparing from the study aid would meet a question in the interview that the
study aid never asked them.

**The answer covered only the wellbore half.** Two wellbore scenarios (3a Production LOPC,
3b Wellwork LOPC) with their safeguards, and nothing about marine.

**The asset confirmed (August 2026) that Hebron and Hibernia have no marine related
incident scenario** in the higher consequence set. That makes *"none"* the correct answer
&mdash; but it still has to be **said**. "Are there any A or B?" answered with only A reads
as though B was missed. The answer now states both halves and says so explicitly.

Source wording restored, marine answer added, recorded in `README.md` alongside the
floating-vessel and CVPE determinations. Verified by diffing the rendered text: exactly two
insertions, `or marine` and the new answer block, nothing removed or reordered; answers
106 &rarr; 107.

### Review sheet item 37, resolved

Item 37 is the asset-wide **Q1** safeguard list pasted under **Q3**. Three things settle it:
the first block is byte-for-byte identical to item 35 (1,600 characters); the second is item
36 differing by a single character, a missing bracket after `HAEQ`; and Q3 already carries
its own scenario-specific 3a and 3b safeguards above it. The sheet now says so and
recommends deletion, but the call stays with the asset.

### On the sheet being rebuilt mid-review

The sheet was regenerated so item 3 shows the corrected Q3. Item numbering is derived from
source order and did not move, and saved work is keyed by item number &mdash; verified by
seeding a part-finished review, rebuilding, and confirming every verdict, note and the
reviewer's name came back intact.

---

## 16. Source-fidelity sweep of every question

Section 15 found a question that had lost two words. That raised an obvious worry: if one
question's *wording* had drifted, others might have too, and every earlier check had asked
whether an **answer** was right, never whether the **question** still matched the source.
So every question was diffed against the controlling document, word by word.

### Asset Specific module (34 questions, UPBP-410 Rev 3.2)

**Two real defects, both fixed.**

| | Source | Study aid had |
|---|---|---|
| Q1 | *"**Demonstrate** an understanding of all Higher Consequence Potential Scenarios..."* | *"**Describe** an understanding..."* |
| Q34 | *"Explain the basic process flows of the facilities within your asset **as per the attached drawing**"* | `Question:` &mdash; a bare label |

Q34 was the worse of the two. The question text was not in the question at all: the div
held the word `Question:` and the real wording sat inside the answer. In Cards mode the
card front read "Question:" and the question itself was on the back. The source wording is
now in the question, and the two asset Process Diagram links sit directly above it.

**Four apparent mismatches were not defects.** Q7 and Q16 looked truncated because the
*extract* used for comparison had been cut at a sentence boundary, not the study aid. Q24
and Q33 looked short because the next section heading (`ENVIRONMENT`, `OVERALL`) ran on
into the question text and the heading filter did not catch a bare uppercase word. Q14 and
Q17 carry their trailing instructions in the answer rather than the question, which is a
reasonable placement.

**All 34 now match the source word for word.**

### Global module (62 questions, Assessor Guide Rev 3.0)

Splitting the Assessor Guide on `Question:` gives question-and-answer blobs, not questions,
so the first attempt produced 16 "differences" that were mostly the parser's fault. The
check that worked asks a narrower question with a reliable answer: **does each question in
the study aid appear verbatim in the source?**

**Two real defects, both fixed.**

| Source | Study aid had |
|---|---|
| *"**Demonstrate** an understanding of approval process for Long Term Temporary Defeat..."* | *"**Describe** an understanding..."* |
| *"...what are the **expectations** of individuals executing the procedure?"* | *"...the **expectation** of..."* |

The `Demonstrate` &rarr; `Describe` substitution appearing in both modules is worth noting:
it reads as a habit of whoever transcribed the questions rather than two coincidences.
Demonstrating and describing are not the same instruction in a competency assessment.

**One thing found but deliberately not changed.** The Work Management worked example
&mdash; *"Repair, Inspect and Test Crude Oil Transfer Pump Tag PBE-12345"* and the six
questions hanging off it &mdash; appears in **no source document**. Neither `PBE-12345` nor
`Crude Oil Transfer` occurs anywhere in the Assessor Guide, either Task Book, or UPBP-410.
Every concept it drills (permit type, Life Saving Actions, Isolation Control Certificate,
Zero Energy Demonstration) *is* in the Assessor Guide, so this looks like a locally written
practice scenario built around real requirements. That is legitimate and useful, but it is
**not** a question an assessor will ask from the guide, and it is not currently labelled as
local. Worth a decision by the owner; not a defect to fix unilaterally.

Punctuation-only differences were left alone &mdash; `LTI's` &rarr; `LTIs`, a full stop
changed to a question mark on a question. The aid is cleaner and no meaning moves.

### Verification

Each fix applied and checked on its own by re-rendering and diffing the extracted text: the
Q1/Q36 edits show as `scrib` &rarr; `monstrat`, the expectations edit as a single inserted
`s`, and the Q34 edit as `Question:` &rarr; the source wording. Nothing else moved. 100
questions, 107 answers, coverage 57 of 57, no console errors, and all 38 review-sheet items
still matching the study aid.

---

## 17. Practice questions

`LOFT-Practice-Questions.html` &mdash; 133 multiple-choice questions across all eleven
topics, every correct answer traced to a specific answer in the study aid, every item
carrying the study guide question it came from.

### The honest caveat, stated on the page itself

The LOFT assessment is a **face-to-face interview**: the candidate demonstrates and
describes, aloud, to an assessment team. Multiple choice tests recognition, not recall,
and cannot test the thing being assessed. The page says so in its opening panel rather
than burying it, and says what the tool *is* good for &mdash; the factual half, where
marks are actually lost: approval ladders, thresholds, timeframes, who signs what.

### The defect that nearly shipped

The first complete draft was gameable. **The correct option was the longest in 79% of
questions** &mdash; someone who knew nothing could score well by always picking the
longest answer, which would have taught them nothing while telling them they were ready.

Fixed by rewriting the distractors on 93 of the 133 items so they match the correct
answer in length and in specificity. Result:

| | Before | After |
|---|---|---|
| Correct option is longest | 79% | 45% |
| Median length ratio to distractors | &mdash; | **1.05** |
| Items where correct is >1.35&times; the mean distractor | 93 | 5 |

45% still reads high, but at a median ratio of 1.05 most of those are longest by a few
characters, which is not a usable tell. Verified empirically as well: clicking the same
slot every time scored 10% on a 20-question run, against 25% chance.

Distractors are drawn from real adjacent material wherever possible, which makes them
teach something when chosen. The superseded CAS answers are the distractors for the CVPE
questions; the Site Manager and PIC are the distractors on the Operations Manager rung of
the temporary defeat ladder; TMEE211 is the distractor for TMEE330.

### What it does

Practice mode marks each answer immediately with the reason and the source question; test
mode holds the score to the end. Topic filter, 10/20/40/all lengths, Fisher-Yates shuffle
on both questions and options, keyboard 1&ndash;4 and Enter, resumable part-finished
attempts, per-topic best scores kept in the browser, and a result page that breaks the
score down by topic and lists every miss with its explanation as a revision list.

The 41 items drawn from asset-local answers are labelled **asset** on the question and in
the feedback, so a candidate knows which facts are the unverified ones.

### Verification

Answering every question correctly scores **100%**; answering every one wrong scores
**0%** &mdash; the check that matters, since options are shuffled and a scoring bug would
otherwise be invisible. Practice mode reveals feedback and test mode does not; the topic
filter returns only that topic; resume restores the exact position; best scores persist
and clear. No console errors, no horizontal overflow from 360px to 1280px.

Two defects found and fixed during testing: the topic `<select>` was wider than a 360px
screen and pushed the page sideways, and the generic `button:disabled` rule dimmed
answered options to 50% opacity &mdash; making the revealed correct answer the least
readable thing on the page.

### 17.1 Content verification of the question bank

Testing the mechanics is not the same as testing the answers. The mechanics were covered;
the answers had only been checked by the author who wrote them. That gap was closed with
four content checks against the study aid.

**Every citation resolves.** All 133 items name a study aid question, and each was matched
back to a real question in the file. Seven flagged low only because the citation is an
abbreviation of a longer question; one is a scope note rather than a question, by design.

**Correct answers use the source's own vocabulary.** 131 of 133 correct answers draw
&ge;70% of their content words from the cited answer. The two exceptions are both correct:
one is a deliberate *"which is NOT"* item whose answer is meant to be absent from the
source, and the other differs only in phrasing (*"greater than 60 per hour"* against the
source's *">60"*).

**Every number was checked in context, not just for presence.** 27 numeric claims appear
in correct answers; all 27 exist in the study aid, and each critical threshold was then
read in its surrounding sentence to confirm it means what the question says it means:

| Claim | Verified against |
|---|---|
| 36 months | procedure revalidation, CVPE route |
| >60 per hour | Best Practice alarm overload |
| Tier 3 with IRAT 400+ | significant process safety events |
| 30.0 / 44.0 / 15.0 mg/L | produced water 30-day, 24-hour, open drains |
| 46503 | CCR number for a spill or release |
| 14 / 16 minutes | Hebron / Hibernia muster targets |
| 7 days, no extension | maximum work permit validity |
| 6-month interval | LTI reporting to the Operations Manager |
| every 5 years | Cat 2 residual risk review |

One of these initially passed for the wrong reason: the bare probe `400` matched a
document number, `CAHE-EC-OOREF-01-006-4007-000`, rather than the IRAT threshold. Re-run
against `IRAT 400` it verifies properly. A presence check that does not read the context
can confirm a number that is not the number you meant.

The temporary defeat ladder (PIC / Operations Manager / Site Manager at 7, 30 and 60 days),
the flange class 300 split, the *cannot be delegated to the Permit Holder* rule, the
AM&nbsp;=&nbsp;Operations&nbsp;Manager and PM&nbsp;=&nbsp;Site&nbsp;Manager glosses, the
SIMOPS deviation levels and the four COP conditions were each confirmed the same way.

**No question has two defensible answers.** 51 distractors share as much vocabulary with
the source as the correct answer does &mdash; which is the intended design, since good
distractors are built from real adjacent facts. The highest-risk of these were read
individually: ICC generation versus verification (AO generates, AA verifies), flange class
above and below 300, SIMOPS deviation levels 1 to 3, and IRAT score versus Hurt Severity
Level. In every case the question names the condition that disambiguates it.

**One readability defect found and fixed.** In the FIMS criticality item the correct answer
and its first distractor were 97% identical, differing only by *SHE* against *Business*
buried mid-sentence &mdash; the right distinction to test, but easy to misread on a phone.
Reworded so the distinguishing term appears early and the two are 84% similar. Numeric
options that differ only in the number were left alone: for a threshold question that is
the whole point.

---

## 18. Practice folded into the study aid

Shipping the practice questions as their own file contradicted the decision in section 11,
and the owner spotted it. The consolidation there existed because every content fix had to
be made in two or three places and the files drifted. A fourth file recreated exactly that.

**The concrete exposure.** The question bank restates facts from **87 different study aid
answers**. Once the review of the 38 asset answers lands and a threshold or an approval
level changes, the study aid would be corrected and the practice questions would go on
teaching the old value with nothing to flag it.

Practice is now the **fourth mode** &mdash; Guide, Test, Cards, Practice &mdash; using the
same overlay pattern as Cards: a fixed layer below the mode bar, shown by a body class.
`LOFT-Practice-Questions.html` was removed; it remains in git history.

The duplication has not disappeared, only become findable. `CONTRIBUTING.md` now says so
plainly: when an answer changes, grep `loft-practice-bank` for the old value and fix it in
the same commit. One file makes that possible, not automatic.

### Details worth keeping

- The layer clears the assessor banner as well as the mode bar
  (`body.assessor-on #practiceLayer { inset: 78px 0 0 0 }`, 118px on mobile), so it takes
  the same offsets as every other piece of fixed chrome.
- Switching to Guide mid-run and back keeps your place. `setMode` calls
  `window.__loftPractice()`, which rebuilds the setup screen only when no attempt is
  running.
- The bank went in before the **last** `</body>`, not the first: the summary script holds
  the literal string `'</body></html>'` inside the standalone report it generates.

### One defect found in testing

The resume button offered *"Resume (0 of 133 done)"* &mdash; the guard tested
`pos < length` but not `pos > 0`, so a run where nothing had been answered counted as
resumable. Now requires at least one answer.

### Verification

Guide content **byte-identical** at 106,941 characters &mdash; this is CSS and two script
blocks, no content touched. Answering everything correctly scores 100% and everything wrong
scores 0%. All four modes switch cleanly with the right layer visible in each. No console
errors, no overflow from 360px to 1280px on either the setup screen or a question. Study
notes, the assessor gate and banner, the module and summary sheets, save and reload, the
dry run and search all still pass, and coverage is 57 of 57.

File size 244 KB &rarr; 356 KB. It still opens instantly from disk and still works offline.

---

## 19. A hole in the assessor gate, and a design pass

### The gate did not cover Cards mode

Found while screenshotting the interface, not by a test. In Cards mode, with the gate
**locked**, every card carried a box labelled *"Assessor notes for this question"* &mdash;
and typing in it wrote straight into the assessment record. Verified: type one word while
locked, and `__loftAssessmentData()` reports one assessor note recorded.

A candidate revising on cards could write into the assessment record without ever seeing
the password. That is exactly what the gate exists to prevent, and it had been true since
the gate was added.

The box now follows the gate rather than ignoring it:

| | Locked | Unlocked |
|---|---|---|
| Label | My study notes | Assessor notes for this question |
| Writes to | `loft-study-notes-v1` | `loft-assessor-notes-v1` |

Rather than hiding the box, the candidate gets their own note box on the card &mdash; and a
note typed there appears in the Guide's study panel for the same question. Verified in both
directions: locked writes 0 assessor notes and 1 study note; unlocked writes to the record
and leaves study notes untouched. This needed a study-note API
(`__loftGetStudyNote` / `__loftSetStudyNote`) mirroring the assessor one.

### Design pass

The interface had grown by accretion &mdash; three fonts, several unrelated blues, headings
underlined with a full-width double rule, and content boxes with hard grey borders. One set
of tokens now drives type, colour, spacing, radius and shadow, applied as overrides beneath
the original rules so the history stays readable in a diff.

**One genuine defect fixed, not just cosmetics.** `#glossaryToggle` was
`position: fixed; left: 335px` &mdash; a floating slab sitting **on top of the first line of
body text** at every scroll position. It is now a normal button in the mode bar with the
other controls.

**One real usability gain.** The contents rail listed 19 entries with nothing marking the
current one, so on a long scroll you lost your place. The current section now highlights as
you scroll, and the three chapter openers (1.0, 2.0, 3.0) read as group headings.

The rest is craft: a single system font stack, 15.5px/1.62 body text, headings with a short
accent rule instead of a full-width double border, section cards with a hairline and a soft
shadow, quieter note panels so the content leads, and readable link colour in place of gold
on white. The page header was a 1.8rem centred navy slab taking a third of the first screen;
the mode bar already carries the branding, so it is now a title rather than a billboard.

A CSS-generated subtitle was drafted and then removed: `content:` text is not selectable and
not searchable, which is the wrong mechanism for information anyone might need to read.

### Verification

Rendered content differs from before the pass by exactly one string: `" Show Glossary"`,
which moved out of the document flow and into the mode bar. Nothing else changed &mdash; 100
questions, 107 answers, 19 sections, coverage 57 of 57.

All four modes, the gate and banner, study notes, card notes in both states, the module and
summary sheets, save and reload, the dry run, search and the review sheet all pass. No
console errors. No horizontal overflow at 360, 390, 414, 768, 820 or 1280 px, checked in
every mode.

---

## 20. Email to the candidate

Asked for as something the manual requires. **It does not.** All six source documents were
searched &mdash; the four Word documents and both PDFs, the latter extracted for the first
time to check. The only occurrences of "email" anywhere are an administrative reminder that
a Superintendent should be on the right distribution lists. There is no required email, and
no template to reproduce.

What the Assessor Guide **does** require is a set of things that have to be communicated,
and email is the usual way they are:

| Section | Obligation |
|---|---|
| 1.3 | Review the Assessor Guide and expectations with the candidate; assess the gap from previous experience; identify a verification target **within 90 days of assuming position**; ensure Risk Approval Authority is delegated until competency is verified |
| 1.4 | Candidate completes the modules, keeps the supervisor posted, marks completion on Career Connect, and **liaises when ready** for the interview |
| 1.5 | Open-ended questions; the candidate elaborates and speaks fluidly rather than reciting; gaps get a **gap closure plan**, are re-assessed per module, and RAA stays delegated until then |
| 1.6 | Assessment team of **three to five**, and the Assessment Lead is set by the candidate's level |

So the builder was written, with every statement in the draft traceable to those sections.
The caveat is on the page itself, not buried in a readme.

### The dropdowns do work, not decoration

Section 1.6 makes the position a rule rather than a blank to fill:

| Assessing a | Assessment Lead should be |
|---|---|
| Second-Line Supervisor | a BU-experienced third-line Supervisor (Operations Manager or equivalent) |
| Third-Line Supervisor | a BU-experienced fourth-line Supervisor with Operations experience (Site Manager or equivalent) |

Choose the position and the page states which applies. It also computes the 90-day target
from the date the position was assumed, and flags a team below three or above five. Asset is
Hebron or Hibernia and flows into the subject line and the body.

Two templates: *starting out* (expectations, timing, RAA, what to do next) and *booking the
interview* (details, how it runs, what happens if there are gaps, what to bring). Candidate,
dates and team prefill from the assessment record. It sits behind the assessor gate, since
it is the supervisor or the assessment team who sends it.

### Two defects found in testing

**Rebuilding the form on every change lost what was being typed.** The `change` handler
called `render()`, which replaced the input elements mid-edit &mdash; so Technical Assessors
and Location silently vanished from the draft and the team count read 2 when four people were
named. It would also have stolen focus on every dropdown change. Now one handler updates the
derived output in place and never rebuilds the inputs.

**"Hi [candidate,"** &mdash; the greeting took the first word of the fallback placeholder
`[candidate name]`. Now `[first name]` when no name is entered.

Copy uses `navigator.clipboard`, falls back to `execCommand`, and falls back again to
selecting the text with a "Press Ctrl+C" prompt, because `navigator.clipboard` is not
available on every `file://` origin.

### Verification

Rendered guide content unchanged. The button is hidden while the gate is locked; the §1.6
lead rule flips correctly with position; asset reaches both subject and body; team warnings
fire below three and above five; copy works and reports it; Escape closes; entries survive a
reload; no overflow at 360, 414 or 768 px. Coverage 57 of 57, and every other regression
still passes.

---

## 21. Asset-specific content update, August 2026

The asset returned its review. Seven changes to Hebron/Hibernia content, sourced to
**WMS Manual Rev 4.0.4 (July 2026)** and **Canada East Appendix A**, with an explicit
instruction that Global Module questions and model answers stay untouched.

| # | Change | Where |
|---|---|---|
| 1, 2 | LTI review at the DWCM: weekly &rarr; **monthly**, plus the **quarterly field assessment** that physically verifies every isolation point | UPBP-410 Q19 (asset DWCM answer) |
| 3, 4 | Single valve isolation rewritten: approved **Appendix A** list, or **Risk Screening** with **Professional Engineer review and stamp** where not listed; reliable seal confirmed by leak test or approved flange-breaking method; **zero energy before breaking containment**, stop and reassess if it cannot be demonstrated. The third-party-engineer-stamp-and-add-to-SharePoint wording is gone | asset half of the breaking-containment scenario |
| 5 | Wet-ink signatures removed. A permit is **not Live until signed by the Area Operator and Permit Holder**, valid up to seven days, signatures required **each shift** after verifications, briefings and zero-energy demonstration | asset permit-steps answer |
| 6 | **AAF = Area Authority Functional** added to the glossary | glossary, now 45 terms |
| 7 | DWCM attendance: **PIC, AA and AAF, with others attending as necessary** | asset DWCM answer |

### Global content confirmed untouched

Instruction 8 listed six areas to leave alone. Each was checked by probe after the edits and
is byte-identical: the temporary defeat ladder including the *not solely time based*
escalation note, the global SVI flange-class split and the cannot-delegate rule, global ZED,
the SIMOPS deviation levels, the seven-day permit validity, and the JSA answer. The global
LTI answer and the global DWCM answer were also left as they are.

Verified by diffing the rendered text before and after: **every change is one of the seven,
and nothing else moved.**

### Two things the change list did not settle

**AAF expands two different ways.** The study aid said *Approving* Authority Functional; the
change list says *Area* Authority Functional, citing the current WMS. The asset-specific
instance was changed to match the WMS and the glossary entry uses it. Worth confirming, since
the same abbreviation now has one expansion here and possibly another in older material.

**DWCM attendance now differs between global and asset.** Change 7 gives the WMS wording, and
instruction 8 says only asset content changes &mdash; so the asset answer now reads *"PIC, AA
and AAF, with others attending as necessary"* while the Global Module answer still reads
*"PIC, AA, and functional supervisors (AAF)"*. Both were left as instructed. If the Global
Module should follow, that is an Assessor Guide change rather than a repository one, and
belongs in `SOURCE-DOCUMENT-QUERIES.md`.

### Downstream

Per `CONTRIBUTING.md`, the practice bank was grepped for every changed value. No question
restated the old SVI wording, wet ink, or the old AAF expansion. One explanation cited the
Assessor Guide for the monthly LTI review; it now cites WMS Manual Rev 4.0.4 and mentions the
quarterly field assessment. The review sheet was rebuilt: all 38 items still match the study
aid, item numbering is unchanged, and a part-finished review was confirmed to survive.

Coverage 57 of 57. Every regression passes: four modes, the gate and banner, study and card
notes, the email builder, modules, summary, save and reload, the dry run and search.

### 21.1 Practice questions for the updated asset content

Eleven questions added to cover the August 2026 changes, taking the bank from 133 to 144.
None of the new material had been drillable before.

| Covers | Questions |
|---|---|
| Single valve isolation | On the approved Appendix A list vs not; Risk Screening first and what it determines; Professional Engineer review and stamp; integrity confirmed by leak test or approved flange-breaking method; **work stops if zero energy cannot be demonstrated**; OIM signature via Permit Vision |
| Permit signatures | A permit is **not Live** until signed by the Area Operator and Permit Holder; signatures required **each shift** despite seven-day validity |
| AAF | What it stands for; what it does in the permit sequence |
| Long Term Isolations | What the **quarterly field assessment** is for, as distinct from the monthly review |

**The superseded values became the distractors.** *Third-party engineer's stamp* and
*Approving Authority Functional* now appear only as wrong answers, so anyone who learned the
old wording is caught and corrected rather than left with it. Two of the items exist purely
to separate things that are easily merged: Risk Screening before Risk Assessment, not the
reverse; and the monthly review confirming status against the quarterly assessment
physically verifying integrity.

Written with matched-length distractors from the start, rather than repeating the mistake in
section 17: median length ratio **0.96**, maximum 1.09, and the correct option is longest in
2 of 11 &mdash; below the 25% that random chance would give.

### Verification

Every one of the eleven correct answers was checked against the study aid text; all eleven
are supported. The whole bank was then re-validated &mdash; 144 items, no duplicates, no
malformed options, every item carrying its section, source and asset flag. Eleven items were
missing the `a` key the others carry; harmless at runtime, since the engine tracks the
original option index rather than reading it, but fixed for consistency.

**All 144 were then answered correctly in one run and the page scored 100%**, with every
question located by its text and no review cards produced. Coverage 57 of 57, and every
other regression passes.

---

## 22. The WMS documents arrived, and one change was wrong

`WMS Manual Rev 4.0.4 (July 2026)` and `Canada East Appendix A Rev D14` were added to the
repository, so the seven changes in section 21 could be checked against their sources rather
than taken on trust. **Five were confirmed verbatim. One was confirmed and explained a
divergence. One was wrong.**

### Confirmed

| Change | Source |
|---|---|
| AAF = Area Authority Functional | WMS §4.4.1.3 &mdash; *"AREA AUTHORITY FUNCTIONAL (AAF)"*. "Approving" occurs **zero** times |
| LTI reviewed monthly | WMS DWCM agenda &mdash; *"Review Long Term Isolation (Monthly)"* |
| Quarterly field assessment | WMS &mdash; *"quarterly field assessment to physically check the integrity of all isolation points"* |
| Permit not Live until AO and PH sign | WMS §5.1.6.3, **[CriticalE]**. "Wet ink" occurs **zero** times |
| Signatures each shift | WMS **[CriticalE]** &mdash; *"issued for up to seven days, but the permit must be progressed with the appropriate signatures each shift"* |

### The divergence in section 21 is explained, not a defect

The WMS carries **both** DWCM attendance wordings, in two places. The agenda says
*"Attendees: PIC, AA, AAF (EM and Contract), others as necessary"*; §5.1.4.2 says
*"the PIC, AA, and functional supervisors"*. The Global Module answer matches §5.1.4.2, so it
was never stale, and leaving it alone was correct.

### The single valve isolation wording was wrong

The applied text made the **Risk Screening trigger** *"the SVI is not covered by the approved
Appendix A list"*. The documents put it somewhere else entirely, and *"Risk Screening"* does
not appear in Appendix A at all. Three things were wrong: the trigger, the purpose, and what
the Professional Engineer approval covers.

What the documents actually say, now carried in the study aid:

- **Appendix A §14.4** holds the **Professional Engineer approved list** of single valve
  isolations, developed to meet **section 144(3)** of the Canada&ndash;NL Offshore Area OHS
  Regulations. The approval covers the **methods, standards, practices and the list itself**
  &mdash; not a step raised per job.
- Each listed isolation carries its own limits: fluid, pressure range, temperature range,
  size range, acceptable valve type and **zero energy proving method**. Being on the list is
  not blanket permission. **Single seated butterfly valves do not qualify** (NOTE 6).
- **WMS §7.4.1.9 [CriticalE]** &mdash; any SVI valve must provide a reliable seal and
  **integrity must be confirmed before commencing work**.
- **[CriticalE]** SVI is **not permitted** where the valve is **Unable To Isolate**, or zero
  energy cannot be demonstrated close to the isolation free of obstruction. Then a **Risk
  Assessment** is required and an acceptable means of isolation identified, documented and
  approved before breaking containment.
- **[CriticalE]** Hazards not sufficiently controlled and zero energy not achieved &rarr;
  **stop, make safe, Risk Screening**.
- **WMS §7.4.1.10 [CriticalE]** &mdash; where a compliant isolation cannot be achieved at all,
  consult a **Risk Screener** to establish the type of Risk Assessment, and **a deviation is
  required in addition**.

The original instinct was right and only the trigger was mislabelled: a Risk Screening does
lead to a Risk Assessment &mdash; on the **non-compliant isolation** route, not the
not-on-the-list route.

### Practice questions

Five SVI questions were rewritten against the documents and three added, taking the bank from
144 to **147**. The wrong trigger and the per-job Professional Engineer step are gone from
the bank entirely. New coverage: what the P.&nbsp;Eng approval actually covers, that the
Appendix A row is the requirement, when SVI is not permitted, the non-compliant route with its
deviation, the excluded valve type, and why Appendix A exists.

One had a length tell &mdash; *"Single seated butterfly"* against *"Ball"* and *"Plug"*, a
ratio of 3.0. Reworded so all four options are comparable; the bank is back to a median of
1.05 and a maximum of 1.44.

### Verification

Thirteen claims checked directly against the two PDFs; **all thirteen supported, none
unsupported**. The old wording confirmed absent from the bank. 147 items, no duplicates or
malformed options. **All 147 answered correctly in one run scored 100%.** Review sheet
rebuilt, 38 of 38 matching, a part-finished review confirmed to survive. Coverage 57 of 57,
and every other regression passes.

---

## 23. Home, and two bugs it exposed

The file opened straight into the Guide, part-way down the front matter, with no orientation
&mdash; and the requirements that govern the whole process sat in sections 1.3 to 1.6, which
readers scroll through on the way to the questions.

**Home** is now the first mode and the landing page. It does two things: points people at the
right tool for what they are doing, and puts the requirements somewhere they cannot be
scrolled past &mdash; the 90-day target, Risk Approval Authority delegated until competency is
demonstrated, the three-to-five team with the Lead set by the candidate's level, the interview
being open-ended rather than question-and-answer, and what happens when there is a gap. Every
line cites its section. Nothing was moved out of the Guide; the full text is still there.

It also shows work in progress &mdash; study notes written, practice average by topic,
questions recorded against an assessment &mdash; so someone returning can see where they were.

### The modal was unreachable from three of five modes

Found because a Home test could not click the password dialog. `#adminVeil` was at
**z-index 300** while every full-screen mode layer sits at 1100 or above, so the dialog
rendered *underneath* them: visible, and unclickable.

| Mode | Before | After |
|---|---|---|
| Guide | clickable | clickable |
| Cards | **blocked by `#cardBody`** | clickable |
| Practice | **blocked by `.pr-setup`** | clickable |
| Home | **blocked by `.hm-card`** | clickable |

This was **not introduced by Home** &mdash; it had been true for Cards and Practice since the
gate was added. Anyone trying to unlock assessor access while on Cards or Practice simply
could not. Raised to 2000, above the mode bar, as a modal should be.

### Practice mode was never remembered

`setMode` saved the mode, but the whitelist that reads it back was
`['guide', 'test', 'cards']` &mdash; `practice` had never been added. The value was written to
`localStorage` and then silently discarded on reload, dropping the reader back into Guide.
Now every mode is listed, and an unrecognised or absent value lands on Home.

### Verification

Guide content **byte-identical** at 109,009 characters &mdash; Home is additive. Five modes,
no console errors, no horizontal overflow in **any** mode at 360, 414, 768 or 1280 px. The
password dialog is clickable in all five. Practice, Cards and Home all survive a reload.
Coverage 57 of 57.

Three regression scripts failed at first because they assumed the page opens in Guide. That
was the change working, not a defect &mdash; they now set the mode explicitly before running,
along with the rest of the suite, so a future change to the landing mode does not silently
break them.

## 24. Work Management, checked line by line against the Assessor Guide

The prompt was that the work management questions should now be correct. They were not.
Checking all twenty of them against **Assessor Guide Rev 3.0** &mdash; the document an
assessor actually grades against &mdash; and then against **WMS Manual Rev 4.0.4** turned up
three questions that were never transcribed at all, one answer that was simply wrong, and
several that had lost half their content somewhere along the way.

Earlier sweeps checked that every question present was faithful to its source. None of them
checked the other direction: that every question in the source was present. That is how
three questions went missing without anything failing.

### Three questions that were never in the file

| Question | Section | Source |
|---|---|---|
| Types of activities on the non-permitted work list, and who approves them | 2.6 Work Management | Assessor Guide Rev 3.0; WMS §6.1.6 |
| Who endorses the ICC when the isolation standard cannot be met and SVI is required | 2.6 Work Management | Assessor Guide Rev 3.0; WMS §7.4.1.4 |
| When does an MOC require a PSSR | 2.7 Management of Change | Assessor Guide Rev 3.0 |

The non-permitted work answer is a `[CriticalE]`: **non-permitted work activities must be
assessed and mitigating controls documented and approved by the OIMS 6-4 Owner**. The ICC
answer is that the **PIC countersigns the isolation certificate before the permit is
endorsed**, having consulted the Minimum Isolation Standard Table for Condition A or B.

Both were candidate-facing questions with a defined answer, and neither was anywhere in the
file. A candidate studying only this material would have walked into the interview unable to
answer them.

### Life Saving Rules and Actions had the wrong answer

The file said Life Saving Actions "are key actions to prevent serious injuries during
higher-risk activities" and "describe the most important aspects of our Work Management
System". That is a paraphrase of something else. Both sources say the same thing, word for
word:

> Life Saving Rules and Actions (LSRA) define the most critical and life-saving actions
> controlled by a worker. These worker actions become key safeguards in eliminating higher
> potential consequences (i.e., life altering injuries and significant process safety
> events).

&mdash; Assessor Guide Rev 3.0, and WMS Manual Rev 4.0.4 §5.1.2.1

The question title was wrong too: "Life Saving Actions", not "Life Saving Rules and Actions".

### The four roles had drifted

| Role | What the file said | What Rev 3.0 says |
|---|---|---|
| PIC | 24-hour endorsement of Temporary Defeats | **24 hr. to 7-day** endorsement; also **endorses single valve isolation plans** and holds **oversight of and compliance with the WMS** |
| AA | Coordinates work at the facility | ...and **reviews and authorizes permits, TDs and isolation plans**, and ensures competent individuals and appropriate tools |
| AO | Performs the review, **approval** and issue of the permit | Performs the **field review and issuance** of the permit |
| PH | Leads pre-job safety toolbox meeting | Conducts the **Pre-Task Briefing**; ensures START work readiness, reinforces STOP Work Expectations, promotes LMRA; **leads AARs when planned or warranted** |

The AO one matters most. Saying the AO *approves* the permit puts an AA responsibility on the
AO, and the split between endorse (PIC), authorize (AA) and issue (AO) is exactly the kind of
thing an assessor probes. A note now flags it in the answer.

The AA and PH entries had each lost their entire second half. "Toolbox meeting" is WMS 3.x
language; WMS 4.0 calls it the Pre-Task Briefing.

### Content missing from three more answers

- **SIMOPS restrictions.** The file said restrictions are determined using the SIMOPS Matrix
  and stopped there. Both sources say the Matrix **must be used in conjunction with the
  SIMOPS Restriction Tables**, which carry the hazard and mitigation guidance
  (WMS §9.4.5.1). The Level 1 / 2 / 3 approvals were already correct and are untouched.
- **DWCM agenda.** Two of the six Rev 3.0 bullets were absent: establishing the status of
  ongoing activities and reviewing new permits and non-permitted work, and assessing SIMOPS
  and endorsing permits with no conflicts.
- **Control valve with no ZEV bleeder.** The file answered "seek a deviation from the manual,
  and as this deviates from a Must requirement the Site Manager approves it". Rev 3.0 says
  something different: **a Risk Assessment is required and an acceptable means of isolation
  must be identified, documented and approved before breaking containment.** The question
  stem had also dropped "and isolating under a single valve isolation", which changes the
  scenario. Both corrected, with a note calling out the change from earlier revisions.

### Where the Assessor Guide is behind the manual

Two answers are correct against Rev 3.0 and incomplete against WMS Rev 4.0.4. Rev 3.0 is what
you are assessed against, so the answers stand; both now carry a note giving the manual's
position, because a candidate who cites only the guide may be asked about the gap.

- **Activities the PTWS addresses.** Rev 3.0 lists five. WMS §6.1.1 lists **seven**, adding
  Atmospheric Testing and Simultaneous Operations.
- **Permit validity.** "7 days with no ability to extend past that time" is right as the outer
  bound &mdash; a new permit is required after seven days. WMS §6.1.4.5 adds that inside that
  window a permit is valid for the duration of the work or until end of shift, whichever comes
  first, to a **maximum of 16 hours with an approved extension**, and must be re-signed each
  shift (Authorized by the AA, Issued by the AO, Accepted by the PH).

### What was checked and found correct

LTI review frequency (monthly register review, quarterly field assessment, OMT reporting to
the Operations Manager on a minimum 6-month interval &mdash; WMS §7.5.1.21&ndash;22); DWCM
attendees (PIC, AA, AAF, others as necessary &mdash; WMS Table 2 and §6.1.4.4); SIMOPS
deviation levels (Level 1 PIC, Level 2 Operations Manager, Level 3 Site Manager &mdash; WMS
§9.4.4.2 and §9.4.6.3); temporary defeat purpose and Area Authority approval; the WMS objectives and OIMS
System 6-4 wording; the global SVI scenario; the ICC and ZED steps; the shift handover
elements; and the asset-specific DWCM answer.

The frozen global answers &mdash; temporary defeat, SVI, ZED, SIMOPS approval levels, permit
validity, JSA &mdash; were verified rather than edited. All were correct. The two exceptions
are noted above: permit validity gained an explanatory note beneath the unchanged answer, and
the control-valve scenario was corrected because it did not match Rev 3.0 at all.

### Practice bank

Eleven items added and four corrected, 147 to **158**. Item 60 had been built on the wrong
LSRA text; item 61 carried the wrong TD endorsement period in its stem; item 70 stopped at
the Matrix; item 59's explanation now names the WMS 4.0.4 additions.

While adding them, a pre-existing weakness surfaced: **always picking the longest option
scored 41.7%** against 25% for guessing. Shuffling defeats position-based gaming but not
length-based gaming, and the earlier check measured only the former. Rebalancing the
distractors on 14 Work Management and MOC items brings those two sections to **27.4%**, and
the whole bank from 41.7% to **34.0%**. The remaining signal is in the eight sections not
touched here.

### Verification

103 questions, 110 answers, 103 note panels, 19 TOC items with no dead links, 45 glossary
terms, five modes, no console errors. All 158 practice items answered correctly score 100%
with nothing unlocatable. Coverage 57 of 57. The word-level diff against the previous text
was read in full: every change is one of the ones described above, and nothing else was lost.

One defect was introduced and caught: the new source-citation badge carried
`white-space: nowrap`, and a citation like "Assessor Guide Rev 3.0; WMS Manual Rev 4.0.4
§9.4.5.1" pushed the page wider than the viewport at 360 and 414 px in four of the five
modes. The committed version had no overflow at any width, which is how it was spotted.
Changed to wrap; clean at 360, 414, 768 and 1280 px in all five modes.

## 25. "Why does Appendix A exist" &mdash; wrong scope

Reported from Practice mode: the item asked *"Why does Appendix A exist in the form it
does?"* and marked **"To meet section 144(3) of the Canada-NL Offshore Area Occupational
Health and Safety Regulations"** correct.

Section 144(3) does not explain Appendix A. It explains **section 14** of it.

Canada East Appendix A Rev D14 is the site supplement to the WMS Manual and runs to fourteen
sections &mdash; permit to work overview, PSMS key components, PTW and isolation lifecycles,
local regulatory requirements, items requiring a permit, fire water isolation performance
standards, safe work practices, LSRA, the work management flowchart, the approved
non-permitted work list, personal isolation tasks, and the LTI multi-discipline review
process. Only **§14, the WMS Addendum on Single Valve Isolations**, exists to address the
additional isolation requirements of the Canada-NL OHS Regulations, and §14.1 says so in
those words.

So the answer was true of one section out of fourteen and was being taught as the reason for
the whole document. A candidate who repeated it in an interview would be corrected.

### What §144(3) actually gives them

Worth understanding rather than memorising, because it is the reason the addendum exists at
all. The regulation permits an energy-isolating device on a pipe carrying hazardous energy to
be any one of:

- a blank or blind together with valves or blocking seals locked out closed, or
- a double block and bleed &mdash; two valves or seals locked out closed either side of a
  mechanism locked open to bleed between them, or
- **one that has been approved by a professional engineer**

That third route is the one Hebron and Hibernia took. §14.4: the addendum was developed *"to
obtain Professional Engineer approval of the Hebron and Hibernia WMS isolation methods,
standards, and practices including a P. Engineer approved list of Isolations using Single
Valve Isolation."* The P.Eng approval is what makes single valve isolation lawful here &mdash;
it is not a per-job step.

### Changes

- Item 100 rewritten: the stem now asks why the **Single Valve Isolation addendum (Appendix A
  section 14)** exists, and the answer gives §14.1's actual wording. The explanation states
  the scope point explicitly, since that is the trap.
- Item 87's stem said "the Professional Engineer approval behind Appendix A"; now "behind the
  Single Valve Isolation addendum". Its answer was already right.
- One item added on the §144(3) routes, so the P.Eng route is taught as a mechanism rather
  than a fact to recall.
- The same loose phrasing in the guide answer and in the review sheet &mdash; "Appendix A of
  the WMS Manual holds the P.Eng approved list, developed to meet section 144(3)" &mdash; now
  names §14 and sets out the three routes. It was defensible as written, since "developed to
  meet 144(3)" attached to the list rather than to Appendix A, but it was the source of the
  bad question and reads better fixed.

Items 88, 90 and 99 refer to "the approved Appendix A list" and were left alone &mdash; that
is ordinary shorthand for a list that is genuinely in Appendix A, and none of them makes a
claim about why the document exists.

### Verification

103 questions, 110 answers, five modes, no console errors, no overflow at 360, 414, 768 or
1280 px. Bank 158 to **159**, all answered correctly for 100% with nothing unlocatable.
Work Management and MOC now sit at **25.5%** for the longest-option strategy against 25% for
guessing; the whole bank is at 33.1%.

## 26. Following the taskbooks

Decision from the owner: **UPBP-400 Rev 3.4 and UPBP-410 Rev 3.2 are the authority for what
questions exist and how they are worded.** A question not in either comes out.

The working principle that falls out of that, and which the file now follows:

> **Question text follows the taskbook** &mdash; that is the document the candidate works
> through. **Answers follow the Assessor Guide Rev 3.0** &mdash; that is what the assessor
> grades against.

### Method

Both taskbooks were extracted to full question text and compared word by word against every
`.question` in the file, in both directions. Two earlier checks had been too weak to catch
any of this: a 65-character prefix probe (which only proves the opening matches) and a
`difflib.get_close_matches` pass that silently mis-scored &mdash; on strings over 200
characters it treats common letters as junk, which reported UPBP-410 Q11 as missing when it
was present and identical. Re-run with `autojunk=False` and word-level opcodes.

### Truncated questions restored

Six questions had lost text. The most consequential:

- **UPBP-400 Q47**, the IMT scenario, was missing its whole **Background info** paragraph
  &mdash; neighbours complaining of noise and flares, local media attention, and the
  community's dependence on the gas in winter. The very next question asks the candidate to
  apply PEAR and name Reputation issues. The material they needed was the paragraph that had
  been dropped.
- **Q61 / 410-Q14** &mdash; "Review the asset COPs if they exist and verify how risk is
  mitigated for each" had been moved into the answer, leaving "What is meant by the term
  Critical Operating Parameter?" answered by an instruction rather than a definition. The
  stem is restored and the answer now defines a COP.
- **Q64 / 410-Q17** &mdash; the four alarm metrics belong in the stem.
- **Q29** &mdash; the taskbook names PIC, AA, AO and PH in the stem.
- **Q13** &mdash; "on the day".
- **Q39** &mdash; "some of the".

Wording aligned to the taskbook in five more: HC spelled out as High Consequence; the alarm
scenario's "per hr" and "instead of their normal range"; "2 key elements"; "3 low
consequence"; and the three procedures questions, where Rev 3.4 has dropped the "Integrity
Critical" qualifier that the older CAS-route material used. Hebron/Hibernia has completed
CVPE, so the plain wording is the applicable one; the superseded CAS answers stay labelled
inside the answers.

### Removed: the PBE-12345 scenario, seven questions

`Repair, Inspect and Test Crude Oil Transfer Pump Tag PBE-12345` and its six follow-ups
&mdash; permit type, Life Saving Actions, permit steps and roles, work pack documents, the
ICC sequence, and Isolation Verification / ZED. None of the seven is in UPBP-400, UPBP-410 or
the Assessor Guide. It was written locally and carried no marking to say so.

Eleven practice items that drew on it went too. Bank 159 to 148.

**What this cost, stated plainly.** That block was the only place the file taught the
Isolation Control Certificate lifecycle, the zero energy demonstration procedure, permit state
transitions, and the contents of a permit pack. `Isolation Control Certificate` now appears in
the guide only as a glossary entry. The 57-topic coverage check still passes, which says more
about the weakness of those probes than about the material. This is a real gap, and it is a
gap because the taskbooks do not ask those questions &mdash; not because the content was
wrong. If it should come back it should come back badged as supplementary, which was the
alternative offered and declined.

### Removed: a duplicated safeguard block

The third "Examples of preventative critical safeguards" block sat under 410 Q3 (wellbore and
marine scenarios) and was a stray paste of the Q1 answer &mdash; its preventative list
byte-identical to the earlier one, its mitigative list differing by a single missing bracket
after `HAEQ`. Q3 was already fully answered above it. This is review sheet item 37.

### Added: the four Flag/Class questions

UPBP-400 Rev 3.4 contains them and the file did not. They are written for **floating** assets;
Hebron and Hibernia are fixed gravity base structures. Rather than continue to omit them, all
four are in with their Assessor Guide answers and a standing note that they do not apply here
and why. Following the taskbook means carrying its questions even where the answer is "not
applicable to this asset, and here is the reason".

### Result

| | Identical to taskbook |
|---|---|
| UPBP-410 Rev 3.2 | **34 / 34** |
| UPBP-400 Rev 3.4 | **77 / 81** |

The four that differ are deliberate: Q9 and Q13 differ only by a trailing list label the
taskbook uses to introduce its answer rows; Q34 and Q45 carry the Assessor Guide's fuller
phrasing, which the model answers depend on ("and isolating under a single valve isolation",
and the note that candidates answer one of the two environmental scenarios).

99 questions, 105 answers, 99 note panels, no dead TOC links, five modes, no console errors,
no overflow at 360, 414, 768 or 1280 px. 148 practice items, all correct and locatable.

## 27. ICC and ZED restored as supplementary

Section 26 removed the PBE-12345 block and recorded what that cost: the file lost the only
place it taught the Isolation Control Certificate lifecycle and the zero energy demonstration
procedure. `Isolation Control Certificate` survived in the guide only as a glossary entry.
Owner decision: bring it back, badged supplementary.

### Rewritten from the manual, not restored from the local text

The removed material was locally authored and had two things wrong, so it was rebuilt from
WMS Manual Rev 4.0.4 rather than pasted back:

| Local text said | WMS Rev 4.0.4 says |
|---|---|
| "An Operations Functional lock is placed on the ICP and key is secured and maintained by Supervisor" | The AO's Operations Functional lock secures the isolation keys **inside** the box. Each PH puts their own lock on the box and **retains that key in their own custody** while working, handing it to their relief or returning it to their supervisor on leaving. &sect;7.5.1.15 Table 17 |
| "Workers can apply their isolation Functional Lock to ICP after zero energy demonstration has been performed" | Locks go on to take control of the isolations; verification is step 12 and the AO's demonstration of zero energy to the PH is step 13, after which the PH accepts the permit. &sect;7.5.1.5 Table 16 |

Every statement in the restored blocks carries its section reference. The pump walkthrough is
kept as a worked example, since it is the part that made the original useful, but it is now
labelled as an example rather than presented as the answer to a question about a specific tag
number that no source document contains.

### How it is marked

Two blocks in 2.6 Work Management, each with a purple rule down the left, a
**Supplementary** badge on the question, and a closing note saying neither taskbook asks it,
why it is here, and that it is sourced from WMS Rev 4.0.4. Nine practice items carry a
matching `supplementary` badge, explained in the Practice legend alongside the existing
`asset` badge.

The badge is the whole point. An unmarked local question is what produced the wrong
Appendix A answer in section 25 &mdash; content with no visible provenance gets treated as
source material by whoever reads it next, including me.

### Result

Guide questions 99 to **101** &mdash; 99 from the taskbooks, 2 supplementary. Practice 148 to
**157**. Taskbook alignment is untouched: **UPBP-410 34/34**, **UPBP-400 77/81**, because the
comparison strips the badge before matching and the supplementary blocks are not claimed as
taskbook questions.

One defect caught in review: the badge sat directly against the question text with no
separating whitespace, so `innerText` read `SUPPLEMENTARYDescribe the steps...`. Visually fine
because of the badge margin, but it would have broken search matching and read wrong on a
flip card. Space added.

101 questions, 107 answers, 101 note panels, no dead TOC links, five modes, no console errors,
no overflow at 360, 414, 768 or 1280 px, 157 practice items all correct and locatable,
coverage 57/57.

## 28. Front matter collapsed

Sections 1.0 to 1.6 of the Assessor Guide &mdash; the introduction, purpose, the supervisor's
and candidate's roles, the verification process and the assessment team &mdash; opened the
Guide with roughly a screen and a half of prose before the first question. Since Home was
added, the requirements out of &sect;1.3&ndash;1.6 are already summarised there with their
section citations, so this was the same material read twice.

Collapsed, not deleted. The seven sections now sit inside one `<details>` headed **About this
assessment**, closed on load, with a sub-line naming the source and pointing at Home. Guide
now opens on 2.0 Process Safety Knowledge Requirements.

The seven table of contents entries collapse to one, taking the TOC from 19 items to 13 and
putting the ten process safety categories on screen without scrolling.

`activate()` now opens a collapsed `<details>` ancestor before scrolling to a target, so the
TOC entry works and any future deep link into that material still lands somewhere visible
rather than scrolling to a closed box.

Nothing was lost: the guide text is 20 characters longer, not shorter (the summary line), all
101 questions and 107 answers are untouched, and &sect;1.6's content is still in the document.
Search is unaffected because the search index is built from `.question` elements and this
material is prose &mdash; it was never indexed.

### A test that lied

The first check reported the collapse had failed &mdash; `assessment-team` still measured 913
pixels tall with the disclosure closed. It had not failed. Chrome renders closed `<details>`
content with `content-visibility: hidden`, and `getBoundingClientRect()` reports a size from
the skipped subtree regardless. The disclosure itself measured 101 pixels (the summary alone)
and `checkVisibility()` returned `false`. Use `checkVisibility()`, or measure the container,
not a descendant.

Verified: 101 questions, 107 answers, 101 note panels, 13 TOC items with no dead links, five
modes, no console errors, no overflow at 360, 414, 768 or 1280 px, 157 practice items all
correct, coverage 57/57, and mode persistence still working.
