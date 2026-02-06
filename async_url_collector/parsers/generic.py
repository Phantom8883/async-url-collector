"""
Универсальный парсер для любого сайта.
"""

from typing import Dict, List
from .base import BaseParser


class GenericParser(BaseParser):
    """
    Универсальный парсер, который работает с любым сайтом.
    Извлекает все изображения и базовые метаданные.
    """
    
    async def parse_page(self, url: str) -> Dict:
        """
        Парсит страницу и извлекает изображения и метаданные.
        
        Args:
            url: URL страницы для парсинга
        
        Returns:
            Словарь:
            {
                'url': str,
                'images': [список URL изображений],
                'metadata': {
                    'title': str,
                    'author': str,
                    'date': str,
                    ...
                }
            }
        
        TODO:
            1. Получить HTML через self.fetch_html(url)
            2. Извлечь изображения через self.extract_images(html, url)
            3. Извлечь метаданные через self.extract_metadata(html, url)
            4. Вернуть словарь с результатами
        """
        # TODO: Реализовать метод
        pass
    
    async def parse_multiple(self, urls: List[str]) -> List[Dict]:
        """
        Парсит несколько URL параллельно.
        
        Args:
            urls: Список URL для парсинга
        
        Returns:
            Список результатов от parse_page()
        
        TODO:
            1. Создать задачи для каждого URL через parse_page()
            2. Использовать asyncio.gather() для параллельного выполнения
            3. Вернуть список результатов
        """
        # TODO: Реализовать метод
        pass

