import asyncio
import aiofiles
from aiocsv import AsyncReader


async def get_num_from_csv(filename: str) -> int:
    async with aiofiles.open(filename, mode='r', newline='', encoding='utf-8') as file:
        acc = 0
        async for row in AsyncReader(file):
            num = int(row[0])
            acc += num
    return acc


async def main():
    filenames = [f'data/5000csv/5000csv/{i}.csv' for i in range(1, 5001)]

    tasks = []
    for file in filenames:
        task = asyncio.create_task(get_num_from_csv(file))
        tasks.append(task)

    nums = await asyncio.gather(*tasks)

    print(sum(nums))


if __name__ == '__main__':
    asyncio.run(main())
