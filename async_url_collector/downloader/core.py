"""
Основная логика асинхронного скачивания файлов.

Включает:
- Параллельные загрузки с ограничением (Semaphore)
- Повторные попытки при ошибках
- Таймауты
- Вычисление SHA256 хеша
"""

import asyncio
import aiohttp
import aiofiles
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import urllib.parse
from datetime import datetime
import os
from ..config import DOWNLOADER_CONFIG, DOWNLOADS_DIR
# DOWNLOADER_CONFIG = {
#     "concurrency": 8,      # Количество одновременных загрузок
#     "timeout": 30,         # Таймаут запроса в секундах
#     "retries": 3,          # Количество повторных попыток при ошибке
#     "retry_delay": 1,      # Задержка между попытками в секундах
# }




async def download_many(
    urls: List[str],
    out_dir: Optional[Path] = None,
    concurrency: int = None,
    timeout: int = None,
    retries: int = None,
) -> List[Dict]:

    """
    Асинхронно скачивает множество файлов.
    
    Args:
        urls: Список URL для скачивания
        out_dir: Папка для сохранения (по умолчанию из config)
        concurrency: Количество одновременных загрузок
        timeout: Таймаут запроса в секундах
        retries: Количество повторных попыток
    
    Returns:
        List[Dict]: Список результатов для каждого URL
    
    TODO:
        1. Определить out_dir (использовать config или переданный)
        2. Определить concurrency (использовать config или переданный)
        3. Создать Semaphore: asyncio.Semaphore(concurrency)
        4. Создать одну сессию: async with aiohttp.ClientSession() as session:
            5. Создать список задач: [download_one(...) for url in urls]
            6. Запустить через asyncio.gather(*tasks, return_exceptions=True)
        7. Обработать исключения из gather (преобразовать в словари с ошибками)
        8. Вернуть список результатов
    """

    out_dir = out_dir or DOWNLOADS_DIR # Дирректория для вывода данных
    concurrency = concurrency or DOWNLOADER_CONFIG["concurrency"] # количество одновременных загрузок.
    timeout = timeout or DOWNLOADER_CONFIG["timeout"] # таймаут берём из конфига
    retries = retries or DOWNLOADER_CONFIG["retries"] # попытки берём из конфига

    semaphore = asyncio.Semaphore(concurrency) # создаём объект

    async with aiohttp.ClientSession() as session: # создаём сессию и закидываем ниже как значения для download_one потому что создание сессии много требует рессурсов
        tasks = [
            download_one(url, out_dir, session, semaphore, timeout, retries)
            for url in urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        fixed = []
        for result in results:
            if isinstance(result, Exception):
                fixed.append({
                    "url": None,
                    "ok": False,
                    "status": 0,
                    "path": None,
                    "filename": "",
                    "size": 0,
                    "sha256": None,
                    "content_type": None,
                    "error": str(result),
                    "timestamp": datetime.utcnow().isoformat()
                })
            else:
                fixed.append(result)
        return fixed







async def download_one(
    url: str,
    out_dir: Path,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    timeout: int = None,
    retries: int = None,
) -> Dict:
    """
    Асинхронная функция для скачивания одного файла по URL.
    
    Args:
        url: URL файла для скачивания
        out_dir: Путь к папке, куда сохранить файл
        session: aiohttp сессия (переиспользуется для всех запросов)
        semaphore: Semaphore для ограничения параллелизма
        timeout: Таймаут запроса в секундах
        retries: Количество повторных попыток при ошибке
    
    Returns:
        dict: {
            "url": str - исходный URL
            "ok": bool - успешно ли скачалось
            "status": int - HTTP статус код
            "path": str | None - путь к сохранённому файлу
            "filename": str - имя файла
            "size": int - размер файла в байтах
            "sha256": str | None - хеш файла
            "content_type": str | None - MIME тип файла
            "error": str | None - текст ошибки, если была
            "timestamp": str - время скачивания
        }
    
    TODO:
        1. Использовать semaphore: async with semaphore:
        2. Реализовать цикл ретраев (for attempt in range(retries + 1))
        3. Внутри цикла:
           - Создать timeout объект: aiohttp.ClientTimeout(total=timeout)
           - Сделать GET запрос через session.get(url, timeout=timeout_obj)
           - Проверить статус (если не 200 - вернуть ошибку)
           - Прочитать данные: await resp.read()
           - Получить content_type из заголовков
           - Вычислить SHA256: hashlib.sha256(data).hexdigest()
           - Сгенерировать имя файла из URL (или хеш, если имени нет)
           - Сохранить через aiofiles: async with aiofiles.open(path, 'wb') as f: await f.write(data)
           - Вернуть успешный результат
        4. При ошибках (TimeoutError, ClientError):
           - Если attempt < retries - подождать и повторить (await asyncio.sleep(delay))
           - Если все попытки исчерпаны - вернуть ошибку
        5. Обработать исключения файловой системы (PermissionError, OSError)
    """

    retry_delay = DOWNLOADER_CONFIG.get("retry_delay", 1) # правило хорошего тона в Python — не доверять внешним структурам данных на 100%.

    async with semaphore:
        for attempt in range(retries + 1): #?
            try:
                timeout_obj = aiohttp.ClientTimeout(total=timeout)
                async with session.get(url, timeout=timeout_obj) as resp:
                    status_code = resp.status
                        
                    if status_code != 200:
                        return {
                            "url": url,
                            "ok": False,
                            "status": status_code,
                            "path": None,
                            "filename": "",
                            "size": 0,
                            "sha256": None,
                            "content_type": None,
                            "error": f"HTTP статус {status_code}",
                            "timestamp": datetime.utcnow().isoformat(), #?
                        }

                    content_type = resp.headers.get("Content-Type") #?
                    parsed_url = urllib.parse.urlparse(url) #?
                    file_name = os.path.basename(parsed_url.path) #?

                    if not file_name:

                        # url.encode() - Превращает строку в байты. -> bytes

                        # hashlib.md5(...) - Создаёт хеш-объект
                        # Это как: "коробка, в которую можно класть данные и считать отпечаток"

                        # .hexdigest() - Берёт внутренний хеш и превращает его в строку из символов -> str

                        #    + '.bin' -  Просто добавляем расширение.

                        file_name = hashlib.md5(url.encode()).hexdigest() + '.bin' 
                    
                    out_path = out_dir / file_name


                    hasher = hashlib.sha256() # hasher - объект счётчик.
                    size = 0

                    async with aiofiles.open(out_path, 'wb') as f:
                        # chunk - это bytes НЕ список, НЕ строка, НЕ массив
                        async for chunk in resp.content.iter_chunked(8192): # 8192 - максмиальный размер одного чанка
                            hasher.update(chunk)
                            size += len(chunk) # len(chunk) - возвращает колличество байтов
                            await f.write(chunk)

                        sha256 = hasher.hexdigest() # переводим в строку из символов -> str для api и отсчётов

                    return {
                        "url": url,
                        "ok": True,
                        "status": status_code,
                        "path": str(out_path),
                        "filename": file_name,
                        "size": size,      
                        "sha256": sha256,
                        "content_type": content_type,
                        "error": None,
                        "timestamp": datetime.utcnow().isoformat(), 
                    }

            except (asyncio.TimeoutError, aiohttp.ClientError) as e: 
                if attempt < retries:
                    await asyncio.sleep(retry_delay) 
                    continue
                return {
                    "url": url,
                    "ok": False,
                    "status": 0,
                    "path": None,
                    "filename": "",
                    "size": 0,
                    "sha256": None,
                    "content_type": None,
                    "error": f"Ошибка сети: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat(), 
                }
            except (PermissionError, OSError) as e: 
                return {
                    "url": url,
                    "ok": False,
                    "status": 0,
                    "path": None,
                    "filename": "",
                    "size": 0,
                    "sha256": None,
                    "content_type": None,
                    "error": f"Ошибка файловой системы: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat(), 
                }
            except Exception as e:
                return {
                    "url": url,
                    "ok": False,
                    "status": 0,
                    "path": None,
                    "filename": "",
                    "size": 0,
                    "sha256": None,
                    "content_type": None,
                    "error": f"Неожиданная ошибка: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat(), 
                }


















