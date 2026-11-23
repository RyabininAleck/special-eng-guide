"""Парсинг списков English — русский из txt-файлов."""

import re
from pathlib import Path

CYRILLIC = re.compile(r"[а-яА-ЯёЁ]")


def parse_en_ru_lines(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if " — " not in line:
            continue
        en, ru = line.split(" — ", 1)
        en, ru = en.strip(), ru.strip()
        if not en or not ru:
            continue
        if CYRILLIC.search(en):
            continue
        entries.append((en, ru))
    return entries


def primary_ru(ru: str) -> str:
    return ru.split(";")[0].split(",")[0].strip()
