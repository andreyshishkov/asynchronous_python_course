import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
from typing import List


def get_links_from_page(soup: BeautifulSoup, cur_link: str) -> List[str]:
    cur_link = re.sub(r'\w+.html', '', cur_link)
    links = soup.find_all('a', class_='link')
    links = [cur_link + link['href'] for link in links]
    return links


def get_num_from_page(soup: BeautifulSoup) -> int:
    tag = soup.find('p', {'id': 'number'})
    num = int(tag.text) if tag else 0
    return num


async def process_page(url: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
    num = get_num_from_page(soup)

    links = get_links_from_page(soup, url)
    tasks = []
    for link in links:
        task = asyncio.create_task(process_page(link, semaphore))
        tasks.append(task)
    deep_nums = await asyncio.gather(*tasks)

    return num + sum(deep_nums)


async def main():
    main_page = 'https://asyncio.ru/zadachi/3/index.html'
    semaphore = asyncio.Semaphore(7)

    result = await process_page(main_page, semaphore)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
