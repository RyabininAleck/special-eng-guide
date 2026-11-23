"""Общие HTML-шаблоны для RU→EN карточек Anki."""

import re


def highlight_word(sentence: str, word: str) -> str:
    pattern = re.escape(word)
    m = re.search(pattern, sentence, re.IGNORECASE)
    if m:
        return sentence[: m.start()] + m.group().upper() + sentence[m.end() :]
    return sentence


def build_front(description: str, sentences_ru: list[str]) -> str:
    items = "".join(
        f'<div style="margin-bottom: 10px; color: #e8e8e8; font-size: 17px;">{i + 1}. {s}</div>'
        for i, s in enumerate(sentences_ru)
    )
    return f'''<div style="font-size: 17px; line-height: 1.6;">
{items}
<div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #444; color: #888; font-size: 14px;">
глагол · сущ · прилагательное · противоположение
</div>
<div style="margin-top: 10px; color: #a0a0a0; font-style: italic; font-size: 15px;">{description}</div>
</div>'''


def build_back(word: str, sentences_en: list[str], verb, noun, adj, opposite) -> str:
    items = "".join(
        f'<div style="margin-bottom: 10px; color: #d0d0d0; font-size: 17px;">{i + 1}. {highlight_word(s, word)}</div>'
        for i, s in enumerate(sentences_en)
    )
    related = f'''<div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #444; font-size: 15px; color: #a0a0a0;">
<div style="font-weight: bold; color: #e8e8e8; margin-bottom: 8px;">{word.upper()}</div>
<div>глагол: <span style="color: #d0d0d0;">{verb}</span></div>
<div>сущ: <span style="color: #d0d0d0;">{noun}</span></div>
<div>прилагательное: <span style="color: #d0d0d0;">{adj}</span></div>
<div>противоположение: <span style="color: #d0d0d0;">{opposite}</span></div>
</div>'''
    return f'<div style="line-height: 1.6;">{items}{related}</div>'
