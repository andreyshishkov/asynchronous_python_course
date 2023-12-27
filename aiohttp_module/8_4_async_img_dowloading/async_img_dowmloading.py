import aiohttp
import asyncio
import aiofiles
import uuid
import os
from bs4 import BeautifulSoup
from typing import List


async def write_file(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, url: str, img_name: str):
    async with semaphore, aiofiles.open(f'images/{img_name}.jpg', mode='wb') as afp:
        async with session.get(url) as response:
            async for x in response.content.iter_chunked(1024):
                await afp.write(x)


async def get_soup(url) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_image_urls(soup: BeautifulSoup) -> List[str]:
    img_tags = soup.find('main').find_all('img')
    base = 'https://asyncio.ru/zadachi/4/'
    img_links = [base + tag['src'] for tag in img_tags]
    return img_links


def get_folder_size(folder_path: str) -> int:
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size


async def main():
    main_url = 'https://asyncio.ru/zadachi/4/index.html'
    soup = await get_soup(main_url)
    img_links = get_image_urls(soup)
    assert len(img_links) == 1000
    semaphore = asyncio.Semaphore(10)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in img_links:
            img_name = str(uuid.uuid4())
            task = asyncio.create_task(write_file(session, semaphore, link, img_name))
            tasks.append(task)
        await asyncio.gather(*tasks)

    print(get_folder_size('images'))


if __name__ == '__main__':
    asyncio.run(main())
