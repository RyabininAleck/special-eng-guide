#!/usr/bin/env python3
"""Генератор RU→EN карточек: phrasal verbs из txt."""

import csv
from pathlib import Path

from anki_card_html import build_back, build_front
from auto_sentence_builder import phrasal_related, phrasal_sentences
from word_list_parser import parse_en_ru_lines, primary_ru

SRC = Path(__file__).parent / "Самые нужные.txt"
OUT = Path(__file__).parent / "phrasal_verbs.csv"


def build_cards() -> list[tuple]:
    cards = []
    for en, ru in parse_en_ru_lines(SRC):
        desc = primary_ru(ru)
        ru_sents, en_sents = phrasal_sentences(en, ru)
        verb, noun, adj, opp = phrasal_related(en)
        cards.append((en, desc, ru_sents, en_sents, verb, noun, adj, opp))
    return cards


def main():
    cards = build_cards()
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Front", "Back"])
        for word, desc, ru, en, verb, noun, adj, opp in cards:
            w.writerow([build_front(desc, ru), build_back(word, en, verb, noun, adj, opp)])
    print(f"✓ {len(cards)} карточек → {OUT}")


if __name__ == "__main__":
    main()
