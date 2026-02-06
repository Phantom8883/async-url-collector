"""
Анализ метаданных из манифеста.
"""

from typing import Dict, List
from pathlib import Path
from collections import Counter
import statistics

# TODO: Импортировать функцию чтения манифеста
# from ..downloader.manifest import read_manifest


def analyze_file_sizes(manifest_path: Path) -> Dict:
    """
    Анализирует размеры файлов.
    
    Args:
        manifest_path: Путь к файлу manifest.jsonl
    
    Returns:
        Словарь со статистикой:
        {
            'min': int,
            'max': int,
            'mean': float,
            'median': float,
            'total': int
        }
    
    TODO:
        1. Прочитать манифест
        2. Извлечь размеры файлов (size)
        3. Вычислить статистику через statistics модуль
    """
    # TODO: Реализовать функцию
    pass


def analyze_content_types(manifest_path: Path) -> Dict[str, int]:
    """
    Анализирует типы контента.
    
    Args:
        manifest_path: Путь к файлу manifest.jsonl
    
    Returns:
        Словарь: {content_type: количество}
        Пример: {'image/jpeg': 50, 'image/png': 30}
    
    TODO:
        1. Прочитать манифест
        2. Использовать Counter для подсчёта content_type
        3. Вернуть словарь
    """
    # TODO: Реализовать функцию
    pass


def analyze_timeline(manifest_path: Path) -> Dict[str, int]:
    """
    Анализирует временную линию скачиваний.
    
    Args:
        manifest_path: Путь к файлу manifest.jsonl
    
    Returns:
        Словарь: {дата: количество файлов}
        Пример: {'2024-01-15': 10, '2024-01-16': 5}
    
    TODO:
        1. Прочитать манифест
        2. Извлечь timestamp из каждой записи
        3. Преобразовать в дату (использовать datetime)
        4. Сгруппировать по дате
        5. Подсчитать количество
    """
    # TODO: Реализовать функцию
    pass


def get_platform_stats(manifest_path: Path) -> Dict[str, int]:
    """
    Статистика по платформам (доменам).
    
    Args:
        manifest_path: Путь к файлу manifest.jsonl
    
    Returns:
        Словарь: {домен: количество файлов}
        Пример: {'pinterest.com': 50, 'twitter.com': 30}
    
    TODO:
        1. Прочитать манифест
        2. Извлечь URL из каждой записи
        3. Парсить домен через urllib.parse.urlparse()
        4. Использовать Counter для подсчёта
    """
    # TODO: Реализовать функцию
    pass

