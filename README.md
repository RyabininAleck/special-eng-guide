# special-eng-guide

Интерактивные HTML-уроки английского. Для учителя: открыть [index.html](index.html) (или GitHub Pages с корня репозитория).

## Структура

| Путь | Назначение |
|------|------------|
| `index.html` | Каталог уроков — домашняя страница Pages |
| `anki.html` | Скачать CSV-колоды для Anki |
| `anki/` | Исходные CSV (и генераторы) |
| `teacher.html` | Как собирать новый урок |
| `html/` | Готовые уроки (один HTML = один урок) |
| `lessons/` | Markdown-конспекты / handout |
| `specs/` | Спецификация и шаблоны упражнений |

## GitHub Pages

Settings → Pages → Deploy from a branch → branch `main`, folder `/` (root).  
После деплоя: `https://<user>.github.io/<repo>/` → `index.html`.  
`.nojekyll` уже лежит в корне — Jekyll не трогает пути.

## Новый урок

1. Скопировать эталон из `html/` (обычно `health.html`).
2. Читать `specs/HTML_LESSON_SPEC.md` и `specs/HTML_LESSON_TEMPLATES.md`.
3. Положить файл в `html/`, добавить ссылку в `index.html`.
