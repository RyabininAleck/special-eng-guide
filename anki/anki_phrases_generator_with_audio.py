#!/usr/bin/env python3
"""
Генератор Anki карточек с озвучкой для английских фраз.

Требования:
    pip install gtts

Использование:
1. Создай файл phrases_data.py с переменной PHRASES
2. Запусти этот скрипт
3. Скопируй папку audio/ в Anki media folder (~/.local/share/Anki2/User 1/collection.media/)
4. Импортируй anki_phrases.csv в Anki

Форматирование:
- Front: фраза жирным шрифтом, контекст курсивом серым, кнопка озвучки
- Back: перевод обычным текстом
- Audio: автоматически генерируется для каждой фразы
"""

import csv
import os
import re
from typing import List, Tuple
from pathlib import Path

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠ gTTS не установлен. Озвучка будет отключена.")
    print("  Установи: pip install gtts")


def sanitize_filename(text: str) -> str:
    """Создает безопасное имя файла из текста."""
    # Убираем специальные символы, оставляем только буквы, цифры, пробелы
    text = re.sub(r'[^\w\s-]', '', text)
    # Заменяем пробелы на подчеркивания
    text = text.replace(' ', '_')
    # Ограничиваем длину
    return text[:50].lower()


def generate_audio(phrase: str, output_dir: Path) -> str:
    """
    Генерирует аудио файл для фразы.
    Возвращает имя файла (без пути).
    """
    if not GTTS_AVAILABLE:
        return ""
    
    filename = f"{sanitize_filename(phrase)}.mp3"
    filepath = output_dir / filename
    
    # Если файл уже существует, не генерируем заново
    if filepath.exists():
        return filename
    
    try:
        tts = gTTS(text=phrase, lang='en', slow=False)
        tts.save(str(filepath))
        return filename
    except Exception as e:
        print(f"✗ Ошибка генерации аудио для '{phrase}': {e}")
        return ""


def create_anki_csv_with_audio(phrases: List[Tuple[str, str, str]], output_file: str, audio_dir: Path):
    """
    Создает CSV файл для импорта в Anki с HTML-форматированием и озвучкой.
    Формат: Front (фраза + контекст + аудио) | Back (перевод)
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Заголовок
        writer.writerow(['Front', 'Back'])
        
        for phrase, context, translation in phrases:
            # Генерируем аудио
            audio_filename = generate_audio(phrase, audio_dir) if GTTS_AVAILABLE else ""
            
            # Кнопка воспроизведения (если есть аудио)
            audio_html = ""
            if audio_filename:
                # Anki формат для аудио: [sound:filename.mp3]
                audio_html = f'<div style="margin-top: 8px;">[sound:{audio_filename}]</div>'
            
            # Front: фраза жирным, контекст курсивом, кнопка аудио
            front_html = f'''<div style="font-size: 18px; line-height: 1.6;">
<div style="font-weight: bold; color: #e8e8e8; margin-bottom: 12px;">{phrase}</div>
<div style="font-style: italic; color: #a0a0a0; font-size: 16px;">{context}</div>
{audio_html}
</div>'''
            
            # Back: перевод светлым цветом
            back_html = f'<div style="font-size: 17px; color: #d0d0d0; line-height: 1.5;">{translation}</div>'
            
            writer.writerow([front_html, back_html])
    
    print(f"✓ Создано {len(phrases)} карточек")
    print(f"✓ Файл сохранен: {output_file}")


def main():
    # Импортируем фразы из отдельного файла
    from phrases_data import PHRASES
    
    print("Создаю Anki карточки с озвучкой...")
    
    # Создаем папку для аудио
    audio_dir = Path("02_Hobbies/English/audio")
    audio_dir.mkdir(exist_ok=True)
    
    output_file = "02_Hobbies/English/anki_phrases.csv"
    
    if GTTS_AVAILABLE:
        print(f"Генерирую аудио файлы в {audio_dir}/...")
        create_anki_csv_with_audio(PHRASES, output_file, audio_dir)
        print(f"✓ Аудио файлы сохранены в {audio_dir}/")
    else:
        print("⚠ Генерация без озвучки (gTTS не установлен)")
        create_anki_csv_with_audio(PHRASES, output_file, audio_dir)
    
    print("\n" + "="*60)
    print("Как импортировать в Anki:")
    print("="*60)
    print("1. Скопируй папку audio/ в Anki media folder:")
    print("   Linux: ~/.local/share/Anki2/User 1/collection.media/")
    print("   Windows: %APPDATA%/Anki2/User 1/collection.media/")
    print("   Mac: ~/Library/Application Support/Anki2/User 1/collection.media/")
    print("2. Открой Anki")
    print("3. File → Import")
    print("4. Выбери файл anki_phrases.csv")
    print("5. Настрой поля:")
    print("   - Field 1 → Front (фраза + контекст + аудио)")
    print("   - Field 2 → Back (перевод)")
    print("6. Выбери разделитель: Semicolon")
    print("7. Нажми Import")
    print("\n✓ Аудио будет автоматически воспроизводиться при показе карточки")


if __name__ == "__main__":
    main()
