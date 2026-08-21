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
