"""
Извлечение EXIF данных из изображений (опционально).

Для этого понадобится библиотека Pillow:
pip install Pillow
"""

from pathlib import Path
from typing import Dict, Optional

# TODO: Раскомментировать после установки Pillow
# from PIL import Image
# from PIL.ExifTags import TAGS


def extract_exif(image_path: Path) -> Optional[Dict]:
    """
    Извлекает EXIF данные из изображения.
    
    Args:
        image_path: Путь к изображению
    
    Returns:
        Словарь с EXIF данными или None
    
    TODO (опционально):
        1. Открыть изображение через PIL.Image.open()
        2. Получить EXIF данные через .getexif()
        3. Преобразовать теги в читаемые имена через PIL.ExifTags.TAGS
        4. Вернуть словарь
    """
    # TODO: Реализовать функцию (опционально)
    pass

