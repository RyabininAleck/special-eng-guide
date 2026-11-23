# Шаблон HTML-урока — практика

Источник правды по стилю и запретам: `HTML_LESSON_SPEC.md`.

**Эталоны для копирования:**

| Задача | Файл |
|--------|------|
| Одна грамматическая глава, один большой банк RU→EN | `html/perfect-have-had.html` |
| Лексика по блокам md: карточки + Gap + Match под каждый раздел | `html/health.html` |
| Много групп однотипной лексики (синонимы, словообразование) | `html/synonyms.html` (20× карточки + Gap + Match) |

Новый урок с несколькими типами заданий: **скопировать `html/health.html`**, выкинуть лишние секции, заменить массивы данных, оставить `<script>` целиком (или вырезать неиспользуемые ключи в `DRILL_SECTIONS` / `MATCH_SETS`).

---

## Каркас секции (теория → практика сверху вниз)

```html
<section id="feel">
  <div class="card prose">
    <p class="section-tag">health.md · Feelings</p>
    <h2>III. Feelings (general state)</h2>
  <p class="ru">…объяснение по-русски…</p>
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

Инициализация внизу скрипта:

```javascript
const KEY_BASE = "my-lesson-v1"; // уникально на урок
document.querySelectorAll(".drill-root").forEach(initDrill);
document.querySelectorAll(".match-root").forEach(initMatch);
```

`data-drill` / `data-match` **должны совпадать** с ключами в `DRILL_SECTIONS` и `MATCH_SETS`.

---

## CSS: обязательные дополнения к базе из SPEC

Плотные строки, без рамки на каждое задание; кнопка **Check** с классом `btn`.

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
.sticky-prog { position: sticky; top: 48px; … } /* см. html/health.html */
```

Match — см. блок `.match-line`, `.match-card`, `.match-drop` в `html/health.html` (drag-and-drop, одна кнопка **Check all**).

**Не использовать:** двухколоночную «теория | sticky-практика», `task-grid` в 2–3 колонки.

---

## Типы письменных заданий (`initDrill`)

Одна строка банка = `[ prompt, expected ]` или `[ prompt, ["alt1", "alt2"] ]`.

Префикс в `prompt` задаёт бейдж через `taskTypeLabel()`; в UI показывается только тело после первого `: ` (см. `promptBody()`), кроме `Dictation …` и `Dialogue C …`.

| Тип | Префикс prompt (EN) | Бейдж | expected |
|-----|---------------------|-------|----------|
| **Gap** | `Gap: My nose is ______.` | Gap | одно слово или `["stuffy", "blocked"]` |
| **RU→EN** | `RU: У меня болит голова.` или `PP RU: …` | RU→EN | полное предложение EN |
| **Dictation** | `Dictation A1` (без двоеточия с текстом) | Dictation | строка целиком |
| **Dialogue line** | `Dialogue C: How do you feel?` | Dialogue | реплика EN |
| **Fix** | `Ex.4 fix: She was bite by …` | Fix | исправленное предложение |
| **Unscramble** | `Ex.11 unscramble: word / word / .` | Unscramble | одно предложение |
| **PP gap** | `PP gap: I have ______ a fever since …` | Gap | форма (V3) |
| **PP write** | `PP EN: Negative: I / not / …` | Write | собранная строка |
| **Mixed ex gaps** | `Ex.1 gap: …` | Gap | как Gap |

Пример секции в данных:

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

Короткие ответы (одно слово) в `rowToItem` не разворачиваются через `expand()`; длинные фразы — допускают варианты `I'm` / `I am` и т.п. (см. `html/health.html`).

Разметка одного задания (генерируется в `mountTasks`):

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

Пары: `[ phraseEn, explanationEn ]`. Фраза слева (фикс), определения справа — DnD между строками.

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

При **Check all**: строка зелёная, если `data-expl` карточки === эталонное объяснение для этой фразы. Прогресс: `localStorage` ключ `KEY_BASE + "-match-" + matchKey`.

Добавить новый Match: ключ в `MATCH_SETS` + блок в HTML с тем же `data-match`.

---

## Лексика на карточках (`mountVocab`)

Тройка: `[ phraseEn, definitionEn, glossRu ]`

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

Карточки **shuffle** при каждой загрузке.

---

## Расширить тип задания

1. Договориться о **префиксе** prompt (английский, короткий).
2. Добавить ветку в `taskTypeLabel(prompt)` → `{ cls, text }` для бейджа.
3. При необходимости — правило в `promptBody()` (когда не резать текст после `:`).
4. Заполнить `DRILL_SECTIONS.имя_секции`.

Класс `task-type.fix` / `.dictation` уже стилизованы; для нового типа можно добавить модификатор в CSS.

---

## Порядок работы над новым уроком

1. Прочитать md/handout — выписать секции как в `lessons/health.md`.
2. Скопировать `html/health.html` → `html/my-topic.html`.
3. Заменить `KEY_BASE`, `<title>`, nav, теорию, `VOCAB_BLOCKS`, `DRILL_SECTIONS`, `MATCH_SETS`.
4. Удалить лишние `<section>` и пустые ключи в объектах.
5. Проверить: EN в UI, RU в теории, Check с `class="btn"`, поток сверху вниз.
6. Открыть файл в браузере, пройти один блок Gap + Match.
7. Добавить карточку на `index.html`.

Полная реализация `normalize`, `bestDiff`, `initDrill`, `initMatch` — **не дублировать здесь**; держать одну копию в эталонном HTML и синхронизировать при доработках только эталон + этот документ.