import aiohttp
from pathlib import Path
import os
import urllib.parse

async def download_one(url, out_dir):
    '''
    Асинхронная функция для скачивания одного файла по URL.
    
    Args:
        url: URL файла для скачивания
        out_dir: Путь к папке, куда сохранить файл
    
    Returns:
        dict: {
            "ok": bool - успешно ли скачалось
            "status": int - HTTP статус код (200, 404, и т.д.)
            "path": str | None - путь к сохранённому файлу
            "size": int - размер файла в байтах
            "error": str | None - текст ошибки, если была
        }
    '''

    # Превращаем строку в объект Path - так удобнее работать с путями
    # Path позволяет делать: path / "file.txt" вместо os.path.join(path, "file.txt")
    out_dir = Path(out_dir)
    
    # Создаём папку, если её нет
    # parents=True - создаст все родительские папки, если их нет
    # exist_ok=True - не будет ругаться, если папка уже существует
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # async with - это асинхронный контекстный менеджер
    # ClientSession() - это "браузер", который может делать много запросов одновременно
    # async with гарантирует, что сессия корректно закроется после блока
    async with aiohttp.ClientSession() as session:
        # session.get(url) - отправляем GET-запрос по URL
        # async with здесь нужен, чтобы корректно закрыть соединение после чтения
        # resp - это объект ответа от сервера
        async with session.get(url) as resp:
            # resp.status - HTTP статус код (200 = OK, 404 = Not Found, 500 = Server Error, и т.д.)
            status_code = resp.status
            
            # Если статус не 200 (OK), значит что-то пошло не так
            if status_code != 200:
                return {
                    "ok": False,
                    "status": status_code,
                    "path": None,
                    "size": 0,
                    "error": "Статус запроса не равен 200",
                }
            else:
                # await resp.read() - читаем ВСЕ байты ответа в память
                # await означает: "ждём, пока байты придут по сети, но пока ждём - 
                # отдаём управление другим задачам (чтобы они могли работать параллельно)"
                # data - это bytes (байты), например: b'\xff\xd8\xff\xe0...' для изображения
                data = await resp.read()

                # Разбираем URL на части, чтобы извлечь имя файла
                # urlparse("https://site.com/path/to/file.jpg") вернёт объект с полями:
                #   scheme="https", netloc="site.com", path="/path/to/file.jpg"
                parsed_url = urllib.parse.urlparse(url)
                path = parsed_url.path  # получаем путь: "/path/to/file.jpg"
                
                # os.path.basename("/path/to/file.jpg") вернёт "file.jpg"
                # берём только последнюю часть пути (имя файла)
                file_name = os.path.basename(path)

                # Собираем полный путь: папка + имя файла
                # Path поддерживает оператор / для склеивания путей
                out_path = out_dir / file_name

                # Открываем файл для записи в бинарном режиме ("wb" = write binary)
                # with гарантирует, что файл закроется после записи
                # f.write(data) - записываем байты в файл
                with open(out_path, 'wb') as f:
                    f.write(data)

                # Возвращаем словарь с результатами успешной загрузки
                return {
                    'ok': True,
                    'status': status_code,
                    'path': str(out_path),  # преобразуем Path обратно в строку
                    'size': len(data),  # размер файла = количество байтов
                }

