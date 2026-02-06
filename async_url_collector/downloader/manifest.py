"""
Модуль для сохранения метаданных о скачанных файлах в формате JSONL.

JSONL (JSON Lines) - формат, где каждая строка это отдельный JSON объект.
Удобен для логов и больших объёмов данных.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# TODO: Импортировать настройки из config
# from ..config import MANIFEST_CONFIG, DOWNLOADS_DIR


def save_to_manifest(
    results: List[Dict],
    manifest_path: Optional[Path] = None,
) -> Path:
    """
    Сохраняет метаданные о скачанных файлах в JSONL файл.
    
    Args:
        results: Список результатов от download_many() или download_one()
        manifest_path: Путь к файлу манифеста (по умолчанию downloads/manifest.jsonl)
    
    Returns:
        Path: Путь к сохранённому файлу манифеста
    
    TODO:
        1. Определить путь к манифесту (использовать config или переданный путь)
        2. Создать директорию, если её нет (mkdir(parents=True, exist_ok=True))
        3. Открыть файл в режиме 'a' (append) для добавления новых записей
        4. Для каждого результата:
           - Сформировать запись с полями: url, filename, path, size, sha256, content_type, status, timestamp, ok
           - Если есть ошибка, добавить поле error
           - Записать JSON строку через json.dumps() + '\n'
        5. Вернуть путь к файлу
    """
    # TODO: Реализовать функцию
    pass


def read_manifest(manifest_path: Optional[Path] = None) -> List[Dict]:
    """
    Читает манифест и возвращает список всех записей.
    
    Args:
        manifest_path: Путь к файлу манифеста
    
    Returns:
        List[Dict]: Список всех записей из манифеста
    
    TODO:
        1. Определить путь к манифесту
        2. Проверить, существует ли файл (если нет - вернуть [])
        3. Открыть файл в режиме 'r'
        4. Для каждой строки:
           - Убрать пробелы (strip())
           - Пропустить пустые строки
           - Попытаться распарсить через json.loads()
           - При ошибке парсинга - пропустить строку (try/except)
           - Добавить в список
        5. Вернуть список записей
    """
    # TODO: Реализовать функцию
    pass


def get_downloaded_urls(manifest_path: Optional[Path] = None) -> set:
    """
    Возвращает множество URL, которые уже были скачаны.
    
    Полезно для пропуска уже скачанных файлов.
    
    Args:
        manifest_path: Путь к файлу манифеста
    
    Returns:
        set: Множество URL, которые уже скачаны (только успешные, ok=True)
    
    TODO:
        1. Прочитать манифест через read_manifest()
        2. Отфильтровать только успешно скачанные (ok: True)
        3. Извлечь URL из каждой записи
        4. Вернуть set() URL
    """
    # TODO: Реализовать функцию
    pass


def filter_new_urls(urls: List[str], manifest_path: Optional[Path] = None) -> List[str]:
    """
    Фильтрует список URL, оставляя только те, которые ещё не скачаны.
    
    Args:
        urls: Список URL для проверки
        manifest_path: Путь к файлу манифеста
    
    Returns:
        List[str]: Список URL, которые ещё не скачаны
    
    TODO:
        1. Получить множество скачанных URL через get_downloaded_urls()
        2. Отфильтровать список urls, оставив только те, которых нет в скачанных
        3. Вернуть отфильтрованный список
    """
    # TODO: Реализовать функцию
    pass

