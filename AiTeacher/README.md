# English Teacher AI Agent

Basic starter kit for an AI agent that helps users learn English.

## What Is Inside

- `AGENT.md` - the main prompt/instruction set for agent behavior.
- `STUDENT_PROFILE.md` - the learner context and long-term goals.
- `TEACHER_EXPERIENCE.md` - the teacher persona and background flavor.

## How To Use

1. Open `AGENT.md`.
2. Keep `STUDENT_PROFILE.md` as the source of truth for learner context.
3. Use `TEACHER_EXPERIENCE.md` when you want a richer teacher persona.
4. Adjust the rules for level (A1-C2), goals, and lesson format if needed.
5. Paste the content of `AGENT.md` into the system where your LLM agent runs (Cursor, API, chatbot, etc.).

## Ideas To Extend

- Add lesson files (`lessons/`), a dictionary (`vocabulary/`), and homework (`homework/`).
- Split modes by focus: speaking, grammar, interview prep.
- Add learner progress tracking.
