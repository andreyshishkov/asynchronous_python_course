import asyncio
import aiofiles
import glob
from aiocsv import AsyncReader


async def get_num_from_file(filename: str) -> int:
    acc = 0
    async with aiofiles.open(filename, mode='r', newline='', encoding='utf-8') as file:
        async for row in AsyncReader(file):
            n = int(row[0])
            acc += n

    return acc


async def main():
    files = glob.glob('data/5000folder/5000folder/*/*.csv')

    tasks = []
    for file in files:
        task = asyncio.create_task(get_num_from_file(file))
        tasks.append(task)

    nums = await asyncio.gather(*tasks)
    print(sum(nums))


if __name__ == '__main__':
    asyncio.run(main())
