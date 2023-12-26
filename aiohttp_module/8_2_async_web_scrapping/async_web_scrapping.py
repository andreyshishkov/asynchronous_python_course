import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup


async def get_urls():
    path_to_url_names = 'data/problem_pages.txt'
    async with aiofiles.open(path_to_url_names, mode='r') as afp:
        nums = await afp.readlines()
    urls = [f'https://asyncio.ru/zadachi/2/html/{num}.html' for num in nums]
    return urls


async def process_page(url: str, semaphore: asyncio.Semaphore):
    async with aiohttp.ClientSession() as session:
        async with semaphore, session.get(url) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'lxml')

    num = soup.find('p', id='number').text
    num = int(num)
    return num


async def main():
    urls = await get_urls()
    semaphore = asyncio.Semaphore(75)

    tasks = []
    for url in urls:
        task = asyncio.create_task(process_page(url, semaphore))
        tasks.append(task)

    nums = await asyncio.gather(*tasks)
    print(sum(nums))


if __name__ == '__main__':
    asyncio.run(main())