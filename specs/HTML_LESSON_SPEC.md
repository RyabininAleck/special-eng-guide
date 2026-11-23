# Spec: HTML pages for English study

One file = one lesson. HTML + CSS + JS in one document. No CDN, no libraries. Opens with a double-click.

**Templates and drill snippets:** `HTML_LESSON_TEMPLATES.md` (copy `html/health.html` or `html/perfect-have-had.html`; Gap / Match / Dictation / Fix / Unscramble / vocab data formats).

Lesson catalog: `index.html`. How to build a lesson: `teacher.html`.

## Hard bans

- Do not mix topics. Teach **one** thing (one tense, one pattern, one word set). Neighbouring forms: grey contrast, labelled “not this chapter”.
- **No multiple-choice.** No radio, no “pick A/B/C”, no clicking a ready-made phrase as the answer.
- A drill = the student **types** in `<input>` / `<textarea>`.
- Vocab blocks and drills **always shuffle** on load and on Shuffle (Fisher–Yates). Source-array order is never screen order.

## Look (premium course, not a wiki)

```css
:root {
  --bg: #0f172a;
  --card: #1e293b;
  --card-2: #243044;
  --line: rgba(148, 163, 184, 0.18);
  --text: #e2e8f0;
  --muted: #94a3b8;
  --accent: #38bdf8;
  --ok: #34d399;
  --bad: #f87171;
  --warn: #fbbf24;
  --radius: 16px;
  --shadow: 0 18px 50px rgba(0, 0, 0, 0.35);
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  background: radial-gradient(1200px 500px at 10% -10%, rgba(56, 189, 248, 0.12), transparent 60%), var(--bg);
  color: var(--text);
  line-height: 1.6;
}
```

- Sticky nav with section anchors.
- Cards: `border-radius: 16px`, thin `--line` border, `--shadow`.
- Formulas: monospace block on `#0b1220`.
- Narrative theory may be Russian; EN examples large; glosses grey (`.ru`).
- Examples from the student’s life: code, PRs, China, Quy Nhon, study — not children’s English.

## UI language (required)

- **English:** buttons, nav, **section titles** (`III. Symptoms`, `health.md · Pain`), `Type · Gap` / `Type · Match`, badges, counters, checkboxes, Match, feedback.
- **Forbidden** in UI: Russian buttons, or EN/RU duplicated on one control.
- **Russian:** narrative theory, `.ru` glosses, “why” notes when English would block the student. Inputs: the student writes English.

## Density and flow

- The lesson is **sequential**: no sticky “practice beside theory” column.
- Gap / RU→EN list: one row per item (badge + prompt + field + Check); wrap only on a narrow screen; no bordered mini-card per item.

## Genre: textbook chapter, not a cheat sheet

Canonical: `html/perfect-have-had.html` (Present Perfect). New lessons must not be shorter or drier than that chapter.

Narrative article: origin and meaning first, then form. Not a fact list and not TikTok cards.

Theory must include:

- **Where the form came from** — historical or logical genesis (for Perfect: *I have the letter written* → *I have written the letter*). Do not start with a table.
- **What the speaker holds in mind** — why English makes this distinction; what Russian aspect/word does not encode.
- **Why that auxiliary** — *have* is not a random label.
- **One through-line sentence** for the whole chapter (lunch, a PR, a laptop) — to show what the form *means*, not how it conjugates.
- Neighbours (Simple, Continuous, other tenses) — grey only, labelled “not this chapter”, only to hear the border.
- Paragraphs, not bullets. Serious, dense tone. No motivational filler.

Forbidden as a substitute: “3 examples + formula + quiz”. If theory is less than roughly half the screen before practice — add origin and meaning.

## Lesson structure

1. **Kicker + chapter title** — what we teach, one line.
2. **Origin** — how the form formed and why it looks like this.
3. **Meaning** — speaker’s camera, live examples, not a table.
4. **Formula** — follows from the history, not the other way around.
5. **One sentence** — one lexical situation; for vocab: definition + live example on a card.
6. **Border / traps** — what kills this form (for Perfect: a closed date).
7. **Writing** — bank under md sections (Gap, Match, Dictation, …) — see `HTML_LESSON_TEMPLATES.md`.
8. **Cheat sheet** at the bottom; print without nav and drills.

Practice: unfinished items bright; done items faded (opacity ~0.32). Counter `done N / M`. Progress in `localStorage` (`KEY_BASE` + section id). Checkbox `only unfinished`.

## Drills: typing + letter check only

Each item:

```
prompt + badge (Gap / RU→EN / …)
[ input ] [ Check ]  /* class="btn" */
letter row: green = match, red = wrong letter, grey dash = missing
```

Check rules:

- Gold standard is a canonical English string (`expected`). Array `expected[]` is allowed; any variant counts.
- Compare **character by character** after `trim()`. Case **matters** (English). Collapse repeated spaces to one.
- Button **next to** the field, not at the bottom of the page.
- Until **Check** — no highlight, no answer.
- After check: letter ribbon + one “why” line on error. Do not spoil the full gold string until the second failed attempt.
- Enter in the field = **Check**.
- Counter: how many items match every character (all green).

Minimal JS (copy into the lesson):

```javascript
function normalize(s) {
  return s.trim().replace(/\s+/g, " ");
}

function diffChars(expected, got) {
  const e = [...expected];
  const g = [...got];
  const n = Math.max(e.length, g.length);
  const out = [];
  for (let i = 0; i < n; i++) {
    if (i >= e.length) out.push({ ch: g[i], kind: "extra" });
    else if (i >= g.length) out.push({ ch: e[i], kind: "miss" });
    else if (e[i] === g[i]) out.push({ ch: g[i], kind: "ok" });
    else out.push({ ch: g[i], kind: "bad" });
  }
  return out;
}

function bestDiff(expectedList, got) {
  const g = normalize(got);
  let best = null;
  for (const exp of expectedList) {
    const e = normalize(exp);
    const parts = diffChars(e, g);
    const score = parts.filter((p) => p.kind === "ok").length;
    if (!best || score > best.score) best = { exp: e, parts, score, perfect: g === e };
  }
  return best;
}

function renderDiff(el, parts) {
  el.innerHTML = parts.map((p) => {
    const cls = p.kind === "ok" ? "ok" : p.kind === "miss" ? "miss" : "bad";
    const ch = p.ch === " " ? "·" : p.ch;
    return `<span class="ch ${cls}">${ch === "<" ? "&lt;" : ch}</span>`;
  }).join("");
}
```

Ribbon CSS:

```css
.row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.row input {
  flex: 1; min-width: 220px;
  background: #0b1220; color: #e2e8f0; border: 1px solid var(--line);
  border-radius: 12px; padding: 10px 12px; font: inherit;
}
.row button {
  background: #38bdf8; color: #082f49; border: 0; border-radius: 999px;
  padding: 10px 14px; font-weight: 700; cursor: pointer;
}
.ch { display: inline-block; min-width: 0.7em; text-align: center; font-family: ui-monospace, Consolas, monospace; }
.ch.ok { color: #34d399; }
.ch.bad { color: #f87171; text-decoration: underline; }
.ch.miss { color: #64748b; border-bottom: 1px dashed #64748b; }
```

Written drill types (mixable in one lesson):

- **Sense dictation:** RU → write EN.
- **Gap:** sentence with a blank, type the form (`have had`, `has gone`).
- **Transform:** statement → question / negative; student writes the whole line.
- **Words:** RU or EN definition → write the word/collocation.

## Vocab: always shuffle

```javascript
function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
```

- Card lists, drill queues, practice examples — `shuffle` on `DOMContentLoaded` and on Shuffle.
- Do not freeze “word 1 is always first”.
- For grammar, shuffle items too: otherwise the student memorizes the number, not the rule.

## Tone

Professional, dense, **expanded**. No “well done, you’re amazing”. Wrong character — show which one. Do not smear one lesson across all tenses “for completeness”. Do not crush a chapter into bullets: a long coherent text on one form beats a short tour of three.
