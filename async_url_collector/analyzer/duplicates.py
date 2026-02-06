"""
Поиск дубликатов файлов по хешу SHA256.
"""

from typing import Dict, List
from pathlib import Path
from collections import defaultdict

# TODO: Импортировать функцию чтения манифеста
# from ..downloader.manifest import read_manifest


def find_duplicates(manifest_path: Path) -> Dict[str, List[Dict]]:
    """
    Находит дубликаты файлов по SHA256 хешу.
    
    Args:
        manifest_path: Путь к файлу manifest.jsonl
    
    Returns:
        Словарь, где ключ - SHA256 хеш, значение - список файлов с этим хешем
        Пример: {'abc123...': [{'url': '...', 'path': '...'}, ...]}
    
    TODO:
        1. Прочитать манифест через read_manifest()
        2. Отфильтровать только успешно скачанные файлы (ok: True)
        3. Сгруппировать по sha256 хешу
        4. Вернуть только группы с >1 файлом (дубликаты)
    """
    # TODO: Реализовать функцию
    pass


def get_duplicate_stats(manifest_path: Path) -> Dict:
    """
    Получает статистику по дубликатам.
    
    Args:
        manifest_path: Путь к файлу manifest.jsonl
    
    Returns:
        Словарь со статистикой:
        {
            'total_files': int,
            'unique_files': int,
            'duplicate_groups': int,
            'duplicate_files': int,
            'saved_space': int  # в байтах (если удалить дубликаты)
        }
    
    TODO:
        1. Использовать find_duplicates()
        2. Подсчитать статистику
        3. Вычислить сэкономленное место
    """
    # TODO: Реализовать функцию
    pass

