"""
Модуль для сохранения метаданных о скачанных файлах в формате JSONL.

JSONL (JSON Lines) - формат, где каждая строка это отдельный JSON объект.
Удобен для логов и больших объёмов данных.
"""

import asyncio
import aiofiles
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from ..config import MANIFEST_CONFIG, DOWNLOADS_DIR




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

# DOWNLOADS_DIR = PROJECT_ROOT / "downloads"

## Настройки манифеста
#MANIFEST_CONFIG = {
#    "filename": "manifest.jsonl",
#    "fields": ["url", "filename", "path", "size", "sha256", "content_type", "status", "timestamp"],
#}

    # 1. Определяем путь к манифесту
    if manifest_path is None:
        path_manifest = DOWNLOADS_DIR / MANIFEST_CONFIG['filename']
    else:
        path_manifest = manifest_path

    # 2. Гарантируем, что директория существует
    path_manifest.parent.mkdir(parents=True, exist_ok=True)

    # 3. Открываем файл в режиме append
    with open(path_manifest, 'a', encoding='utf-8') as f:

        # 4. Проходим по результатам загрузки
        for result in results:

            # 4. Формируем запись манифеста по контракту
            record = {}

            # 5. Копируем только разрешённые поля
            for field in MANIFEST_CONFIG['fields']:
                record[field] = result.get(field)

            # 6. Явно добавляем флаг ok
            record['ok'] = result.get('ok', False)

            # 7. Если была ошибка — сохраняем её
            if not record['ok'] and result.get['error']:
                record['error']

            # 8. Сериализуем и пишем одну строку
            json_line = json.dumps(result, ensure_ascii=False) # encure_ascii - Unicode-последовательности
            f.write(json_line + '\n')

    # 9. Возвращаем путь к манифесту
    return path_manifest












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



    if manifest_path:
        path_manifest = manifest_path
    else:
        path_manifest = DOWNLOADS_DIR / MANIFEST_CONFIG['filename']
    result_list = []
    if not path_manifest.exists():
        return []
    with open(path_manifest, 'r', encoding='utf-8') as f:

        for line in f:

            if not line.strip():
                continue

            try:
                j = json.loads(line)
            except json.JSONDecodeError:
                continue
            result_list.append(j)

    return result_list







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

