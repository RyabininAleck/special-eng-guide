#!/usr/bin/env python3
"""
Генератор Anki карточек для изучения английских фраз и оборотов.
Извлекает продвинутые фразы (B1-C1) из текста.

Использование:
1. Создай файл phrases_data.py с переменной PHRASES
2. Запусти этот скрипт
3. Импортируй anki_phrases.csv в Anki

Форматирование:
- Front: фраза жирным шрифтом, контекст курсивом серым
- Back: перевод обычным текстом
- Все поля используют HTML для красивого отображения
"""

import csv
from typing import List, Tuple


def create_anki_csv(phrases: List[Tuple[str, str, str]], output_file: str):
    """
    Создает CSV файл для импорта в Anki с HTML-форматированием.
    Формат: Front (фраза + контекст в HTML) | Back (перевод в HTML)
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Заголовок
        writer.writerow(['Front', 'Back'])
        
        for phrase, context, translation in phrases:
            # Front: фраза жирным, контекст курсивом (светлые цвета для темной темы)
            front_html = f'''<div style="font-size: 18px; line-height: 1.6;">
<div style="font-weight: bold; color: #e8e8e8; margin-bottom: 12px;">{phrase}</div>
<div style="font-style: italic; color: #a0a0a0; font-size: 16px;">{context}</div>
</div>'''
            
            # Back: перевод светлым цветом
            back_html = f'<div style="font-size: 17px; color: #d0d0d0; line-height: 1.5;">{translation}</div>'
            
            writer.writerow([front_html, back_html])
    
    print(f"✓ Создано {len(phrases)} карточек")
    print(f"✓ Файл сохранен: {output_file}")


def main():
    # Импортируем фразы из отдельного файла
    from phrases_data import PHRASES
    
    print("Создаю Anki карточки из phrases_data.py...")
    
    output_file = "02_Hobbies/English/anki_phrases.csv"
    create_anki_csv(PHRASES, output_file)
    
    print("\n" + "="*60)
    print("Как импортировать в Anki:")
    print("="*60)
    print("1. Открой Anki")
    print("2. File → Import")
    print("3. Выбери файл anki_phrases.csv")
    print("4. Настрой поля:")
    print("   - Field 1 → Front (фраза + контекст)")
    print("   - Field 2 → Back (перевод)")
    print("5. Выбери разделитель: Semicolon")
    print("6. Нажми Import")


if __name__ == "__main__":
    main()
