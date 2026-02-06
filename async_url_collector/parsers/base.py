
# parsers/base.py

# aiohttp — асинхронная библиотека для HTTP-запросов
# Она позволяет скачивать страницы одновременно (без блокировки программы)
import aiohttp

# urllib.parse.urljoin — для объединения относительных и абсолютных URL
# Например, "/image.jpg" + "https://site.com/page" -> "https://site.com/image.jpg"
from urllib.parse import urljoin

# BeautifulSoup — библиотека для парсинга HTML
# Позволяет удобно извлекать теги, атрибуты и текст
from bs4 import BeautifulSoup



class BaseParser:
    """Базовый парсер для любого сайта"""
    async def fetch_html(self, url):
        """
        Скачивает HTML страницы асинхронно.

        Agrs:
            url (str): сслыка на страницу

        Returns:
            str | None: HTML-код страницы или None при ошибке
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Ошибка при скачивании {url}: статус: {resp.status}")
                    return None
            return await resp.text()


    async def extract_images(self, html, base_url):
        """
        Извлекает URL картинок из HTML и приводит их к абсолютному виду.

        Args:
            html (str): HTML-код страницы
            base_url (str): URL страницы для абсолютных ссылок

        Returns:
            list[str]: список URL картинок
        """
        urls = []
        soup = BeautifulSoup(html, 'html.parser') # - создаём объяект для парсинга
        for img in soup.find_all('img'): # находим все теги <img> 
            src = img.get('src') # берём атрибут src (ссылка на картинку)
            if not src:
                continue
            # urljoin - превращает относительную ссылку в абсолютную
            full_url = urljoin(base_url, src)
            # Фильтр по расширениям картинок
            if any(full_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', 'gif']):
                urls.append(full_url)
        return urls



    async def crawl_page(self, url): # объединяет fetch + extract 
        """
        Объединяет fetch + extract_images
        Получает HTML страницы и сразу возвращаем список картинок

        Args:
            url (str): страница для парсинга

        Returns:
            list[str]: список URL картинок
        """
        html = await self.fetch_html(url)
        if not html:
            return []
        return self.extract_images(html, url)



class PixivParser(BaseParser):
    async def crawl_user_illusts(self, user_url):
        urls = await self.crawl_page(user_url)
        return urls




class TwitterParse(BaseParser):
    pass
class TelegramParser(BaseParser):
    pass
