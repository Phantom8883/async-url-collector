from .io_utils import read_urls
from .downloader import download_one
import asyncio
from pathlib import Path



async def main():
    project_dir = Path(__file__).resolve().parents[1]
    urls_path = project_dir / 'urls.txt' 
    out_dir = project_dir / 'downloads'
    urls = read_urls(urls_path)
    if not urls:
        print(f"Ошибка urls.txt пуст")
    for url in urls:
        result = await download_one(url, out_dir)
        print(f'{url} -> {result["ok"]}, size: {result["size"]} bytes')



if __name__ == '__main__':
    asyncio.run(main())
