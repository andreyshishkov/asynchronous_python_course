import asyncio
import aiofiles
import aiofiles.os as aos
import aiocsv
import json
from collections import defaultdict
from typing import DefaultDict, Dict


def load_to_json(data_to_save: DefaultDict[str, int], path_to_save: str = 'data/result.json'):
    with open(path_to_save, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)
    print('Result is saved')


async def process_file(path: str, semaphore: asyncio.Semaphore, costs: DefaultDict[str, int]):
    async with semaphore, aiofiles.open(path, mode='r', encoding='windows-1251') as afp:
        reader = aiocsv.AsyncReader(afp, delimiter=';', quotechar='"')
        await reader.__anext__()
        async for row in reader:
            state, cost = row[-1], int(row[-2])
            costs[state] += cost


async def process_directory(
        path: str,
        semaphore: asyncio.Semaphore,
        costs: DefaultDict[str, int]
):
    tasks = []
    entries = await aos.listdir(path)
    for entry in entries:
        full_path = f'{path}/{entry}'
        if await aos.path.isfile(full_path) and entry.endswith('.csv'):
            tasks.append(
                asyncio.create_task(
                    process_file(full_path, semaphore, costs)
                )
            )

        elif await aos.path.isdir(full_path):
            tasks.append(
                asyncio.create_task(process_directory(full_path, semaphore, costs))
            )

    await asyncio.gather(*tasks)


async def main():
    costs = defaultdict(int)
    semaphore = asyncio.Semaphore(1000)
    data_path = 'data/auto/auto/Задача 3'

    await process_directory(data_path, semaphore, costs)
    load_to_json(costs)


if __name__ == '__main__':
    asyncio.run(main())