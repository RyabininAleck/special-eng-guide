# special-eng-guide

Interactive HTML English lessons. For the teacher: open [index.html](index.html) (or GitHub Pages from the repo root).

Lesson **UI is English**. Narrative theory and glosses in some chapters stay **Russian** (the student is a Russian speaker).

## Layout

| Path | What |
|------|------|
| `index.html` | Lesson catalog — Pages home |
| `anki.html` | Download Anki CSVs |
| `anki/` | CSV decks (and generators) |
| `make-lesson.html` | Copy-paste prompt to generate a lesson |
| `teacher.html` | Spec overview (hard rules, workflow) |
| `html/` | Finished lessons (one HTML file = one lesson) |
| `lessons/` | Markdown handouts |
| `specs/` | Spec and exercise templates |

## GitHub Pages

Settings → Pages → Deploy from a branch → `main`, folder `/` (root).  
Live URL: `https://<user>.github.io/<repo>/` → `index.html`.  
`.nojekyll` is in the root so Jekyll does not rewrite paths.

## New lesson

1. Copy a canonical file from `html/` (usually `health.html`).
2. Read `specs/HTML_LESSON_SPEC.md` and `specs/HTML_LESSON_TEMPLATES.md`.
3. Put the file in `html/`, add a card on `index.html`.
