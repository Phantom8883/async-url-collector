
import asyncio
from pathlib import Path
from parsers.base import PixivParser


async def main():
    parser = PixivParser()
    #project_dir = Path(__file__).resolve().parents[1]
    #urls_path = project_dir / 'urls.txt' # 
    #out_dir = project_dir / 'downloads' # получаем url папки для загрузки





    urls = await parser.crawl_user_illusts() # type: ignore







    if not urls:
        print(f"Ошибка urls.txt пуст")
    
    tasks = [download_one(url, out_dir) for url in urls]
    
    results = await asyncio.gather( # gather() -        
        *tasks, # распаковывает список в отдельные аргументы как в декораторах *args
        return_exceptions=True # Продолжает запросы, даже если некоторые буду падать (полезно, если скачиваешь с нескольких источников, особенно нестабильных)
    )

    # Обработка результатов из gather(). Проверка, является ли результат исключением. Вывод информации о каждой загрузке
    for result in results:
        if isinstance(result, Exception):
            print(f'Ошибка: {result}')
        else:
            if result['ok']:
                print(f"Скаченно {result['url']} -> {result['size']} bytes")
            else:
                print(f"Ошибка {result['url']} -> {result['error']}")



if __name__ == '__main__':
    asyncio.run(main())
