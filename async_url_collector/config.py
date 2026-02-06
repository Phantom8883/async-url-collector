"""
Конфигурация проекта async_url_collector.

Настройки для парсеров, загрузчиков и других модулей.
"""

from pathlib import Path

# Базовые пути
PROJECT_ROOT = Path(__file__).parent.parent
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
DATA_DIR = PROJECT_ROOT / "async_url_collector" / "data"

# Настройки загрузчика
DOWNLOADER_CONFIG = {
    "concurrency": 8,      # Количество одновременных загрузок
    "timeout": 30,         # Таймаут запроса в секундах
    "retries": 3,          # Количество повторных попыток при ошибке
    "retry_delay": 1,      # Задержка между попытками в секундах
}

# Настройки парсера
PARSER_CONFIG = {
    "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Настройки манифеста
MANIFEST_CONFIG = {
    "filename": "manifest.jsonl",
    "fields": ["url", "filename", "path", "size", "sha256", "content_type", "status", "timestamp"],
}

# Теги для поиска (пример)
SEARCH_TAGS = {
    "default": ["KnT", "z-toon"],
    "pixiv": [],
    "twitter": [],
    "telegram": [],
}

