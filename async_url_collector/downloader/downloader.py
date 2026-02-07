import aiohttp
from pathlib import Path
import os
import urllib.parse

async def download_one(url, out_dir):
    '''
    Первая асинхронаая функция для меня, которую я понял по полной.

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
    try:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                status_code = resp.status
                
                if status_code != 200:
                    return {
                        'url': url,
                        "ok": False,
                        "status": status_code,
                        "path": None,
                        "size": 0,
                        "error": f"HTTP статус {status_code}",
                    }
                
                data = await resp.read()
                parsed_url = urllib.parse.urlparse(url)
                file_name = os.path.basename(parsed_url.path)
                
                if not file_name:
                    import hashlib
                    file_name = hashlib.md5(url.encode()).hexdigest() + '.bin'

                out_path = out_dir / file_name
                with open(out_path, 'wb') as f:
                    f.write(data)

                return {
                    'url': url,
                    'ok': True,
                    'status': status_code,
                    'path': str(out_path),
                    'size': len(data),
                    'error': None,
                }
    
    except aiohttp.ClientError as e:
        return {
            'url': url,
            'ok': False,
            'status': 0,
            'path': None,
            'size': 0,
            'error': f'Ошибка сети: {str(e)}',
        }
    
    except (PermissionError, OSError) as e:
        return {
            'url': url,
            'ok': False,
            'status': 0,
            'path': None,
            'size': 0,
            'error': f'Ошибка файловой системы: {str(e)}',
        }
    
    except Exception as e:
        return {
            'url': url,
            'ok': False,
            'status': 0,
            'path': None,
            'size': 0,
            'error': f'Неожиданная ошибка: {str(e)}',
        }

