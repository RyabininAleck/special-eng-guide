# HTML lesson template — practice

Source of truth for style and bans: `HTML_LESSON_SPEC.md`.

**Files to copy:**

| Job | File |
|--------|------|
| One grammar chapter, large RU→EN bank | `html/perfect-have-had.html` |
| Vocab by md blocks: cards + Gap + Match per section | `html/health.html` |
| Many same-shape vocab groups (synonyms, word-building) | `html/synonyms.html` (20× cards + Gap + Match) |

New lesson with several drill types: **copy `html/health.html`**, drop unused sections, replace data arrays, keep the `<script>` (or delete unused keys in `DRILL_SECTIONS` / `MATCH_SETS`).

---

## Section skeleton (theory → practice, top to bottom)

```html
<section id="feel">
  <div class="card prose">
    <p class="section-tag">health.md · Feelings</p>
    <h2>III. Feelings (general state)</h2>
  <p class="ru">…Russian explanation…</p>
    <div id="feel-cards" class="vocab-grid"></div>

    <div class="lesson-practice drill-duo">
      <div class="drill-section">
        <span class="section-tag">Type · Gap</span>
        <div class="drill-root" data-drill="feel"></div>
      </div>
      <div class="drill-section">
        <span class="section-tag">Type · Match</span>
        <div class="match-root" data-match="feel"></div>
      </div>
    </div>
  </div>
</section>
```

Init at the bottom of the script:

```javascript
const KEY_BASE = "my-lesson-v1"; // unique per lesson
document.querySelectorAll(".drill-root").forEach(initDrill);
document.querySelectorAll(".match-root").forEach(initMatch);
```

`data-drill` / `data-match` **must match** keys in `DRILL_SECTIONS` and `MATCH_SETS`.

---

## CSS: required extras on top of the SPEC base

Dense rows, no border per item; **Check** button with class `btn`.

```css
.task {
  margin: 0;
  padding: 10px 0;
  border: none;
  background: transparent;
  border-bottom: 1px solid var(--line);
}
.task.done { opacity: 0.32; filter: saturate(0.35); }

.task-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 10px;
}
.task-type {
  display: inline-block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(56, 189, 248, 0.15);
  color: #7dd3fc;
}
.task-type.dictation { background: rgba(52, 211, 153, 0.15); color: #6ee7b7; }
.task-type.fix { background: rgba(248, 113, 113, 0.15); color: #fca5a5; }

.task-body { flex: 1 1 200px; min-width: 0; font-size: 0.94rem; }
.row input,
.task-line input {
  background: #0b1220;
  color: var(--text);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 12px;
  font: inherit;
}
.task-line input {
  flex: 1 1 160px;
  min-width: min(140px, 100%);
  max-width: 380px;
}
.row button, .btn, .task-line button.btn {
  background: var(--accent);
  color: #082f49;
  border: 0;
  border-radius: 999px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.task-grid { display: flex; flex-direction: column; gap: 0; }
.sticky-prog { position: sticky; top: 48px; … } /* see html/health.html */
```

Match — see `.match-line`, `.match-card`, `.match-drop` in `html/health.html` (drag-and-drop, one **Check all** button).

**Do not use:** two-column “theory | sticky practice”, or a 2–3 column `task-grid`.

---

## Written drill types (`initDrill`)

One bank row = `[ prompt, expected ]` or `[ prompt, ["alt1", "alt2"] ]`.

The prefix in `prompt` sets the badge via `taskTypeLabel()`; the UI shows only the body after the first `: ` (see `promptBody()`), except `Dictation …` and `Dialogue C …`.

| Type | Prompt prefix (EN) | Badge | expected |
|-----|---------------------|-------|----------|
| **Gap** | `Gap: My nose is ______.` | Gap | one word or `["stuffy", "blocked"]` |
| **RU→EN** | `RU: У меня болит голова.` or `PP RU: …` | RU→EN | full EN sentence |
| **Dictation** | `Dictation A1` (no colon + text) | Dictation | whole line |
| **Dialogue line** | `Dialogue C: How do you feel?` | Dialogue | EN line |
| **Fix** | `Ex.4 fix: She was bite by …` | Fix | corrected sentence |
| **Unscramble** | `Ex.11 unscramble: word / word / .` | Unscramble | one sentence |
| **PP gap** | `PP gap: I have ______ a fever since …` | Gap | form (V3) |
| **PP write** | `PP EN: Negative: I / not / …` | Write | assembled line |
| **Mixed ex gaps** | `Ex.1 gap: …` | Gap | same as Gap |

Sample data section:

```javascript
const DRILL_SECTIONS = {
  feel: [
    ["Gap: I feel ______.", ["fine", "great"]],
    ["Gap: I am not well. I feel ______.", ["sick", "ill"]],
  ],
  dictation: [
    ["Dictation A1", "My nose is stuffy."],
    ["Dialogue C: closing", "Get well soon!"]
  ],
  pp: [
    ["PP gap: I have ______ a fever since Monday.", "had"],
    ["PP RU: Я ещё не ходил к врачу.", "I haven't seen a doctor yet."]
  ],
  mixed: [
    ["Ex.4 fix: She was bite by a mosquito.", "She was bitten by a mosquito."],
    ["Ex.11 unscramble: feel / I / dizzy / .", "I feel dizzy."]
  ]
};
```

Short one-word answers in `rowToItem` are not expanded via `expand()`; long phrases allow `I'm` / `I am` etc. (see `html/health.html`).

Markup of one item (generated in `mountTasks`):

```html
<div class="task todo">
  <div class="task-line">
    <span class="task-type">Gap</span>
    <span class="task-num">1.</span>
    <span class="task-body">I feel ______.</span>
    <input type="text" spellcheck="false" autocomplete="off">
    <button type="button" class="btn">Check</button>
  </div>
  <div class="letters"></div>
  <p class="fb"></p>
</div>
```

Feedback (EN): `Match.` · `No match yet. Answer hidden.` · `Answer: …`

Toolbar (EN): `done 0 / N` · `only unfinished` · `Shuffle` · `Reset`

---

## Match (`initMatch`)

Pairs: `[ phraseEn, explanationEn ]`. Phrase on the left (fixed); definitions on the right — drag between rows.

```javascript
const MATCH_SETS = {
  feel: [
    ["I feel dizzy.", "My head feels like it is spinning. I may fall."],
    ["I'm recovering.", "I am getting better. My health is coming back."]
  ]
};
```

```html
<div class="match-root" data-match="feel"></div>
```

On **Check all**: the row is green if the card’s `data-expl` === the gold explanation for that phrase. Progress: `localStorage` key `KEY_BASE + "-match-" + matchKey`.

Add a new Match: key in `MATCH_SETS` + HTML block with the same `data-match`.

---

## Vocab cards (`mountVocab`)

Triple: `[ phraseEn, definitionEn, glossRu ]`

```javascript
const VOCAB_BLOCKS = {
  feel: [
    ["I feel fine / great.", "My body and mood are good. I am okay.", "Тело и порядке."],
  ]
};
```

```html
<div id="feel-cards" class="vocab-grid"></div>
```

```javascript
mountVocab("feel-cards", VOCAB_BLOCKS.feel);
```

Cards **shuffle** on every load.

---

## Add a drill type

1. Agree a **prompt prefix** (English, short).
2. Add a branch in `taskTypeLabel(prompt)` → `{ cls, text }` for the badge.
3. If needed — a rule in `promptBody()` (when not to split after `:`).
4. Fill `DRILL_SECTIONS.section_name`.

Classes `task-type.fix` / `.dictation` are already styled; a new type can add a CSS modifier.

---

## Workflow for a new lesson

1. Read the md/handout — list sections as in `lessons/health.md`.
2. Copy `html/health.html` → `html/my-topic.html`.
3. Replace `KEY_BASE`, `<title>`, nav, theory, `VOCAB_BLOCKS`, `DRILL_SECTIONS`, `MATCH_SETS`.
4. Delete leftover `<section>`s and empty object keys.
5. Check: EN in UI, RU in theory if needed, Check with `class="btn"`, flow top to bottom.
6. Open the file in a browser, run one Gap + Match block.
7. Add a card on `index.html`.

Full `normalize`, `bestDiff`, `initDrill`, `initMatch` — **do not duplicate here**; keep one copy in the canonical HTML and sync this doc only when the canonical file changes.