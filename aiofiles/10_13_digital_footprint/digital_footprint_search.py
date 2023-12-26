import asyncio
import aiofiles
import aiofiles.os as aos
import json
import csv
from datetime import datetime
from itertools import chain
from typing import Iterator, List, Union

HEADERS = [
        'Время и дата',
        'IP-адрес',
        'User-Agent',
        'Запрошенный URL',
        'HTTP-статус',
        'Реферер',
        'Cookie',
        'Размер страницы и заголовки ответа',
        'Метод запроса',
        'Информация об ошибке',
    ]


async def process_file(path: str, semaphore: asyncio.Semaphore) -> List[List[Union[int, str]]]:
    async with semaphore, aiofiles.open(path, mode='r', encoding='utf-8') as afp:
        logs = await afp.read()
        logs = json.loads(logs)

    data = []
    for log in logs:
        if log['HTTP-статус'] == 200:
            data.append(list(log.values()))

    return data


def transform_date(date_str: str) -> str:
    date = datetime.fromisoformat(date_str)
    return date.strftime('%d.%m.%Y %H:%M:%S')


def prepare_data(data: Iterator[List[Union[str, int]]]):
    data = list(data)
    data.sort(key=lambda x: x[0])

    for row in data:
        row[0] = transform_date(row[0])

    return data


def load_to_json(data: List[List[Union[str, int]]], path_to_save: str = 'data/result.csv'):
    with open(path_to_save, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';', lineterminator='\n')
        writer.writerow(HEADERS)
        writer.writerows(data)


async def process_directory():
    dir_path = 'data/logs/logs'
    files = await aos.listdir(dir_path)

    semaphore = asyncio.Semaphore(1000)

    tasks = []
    for file in files:
        full_path = f'{dir_path}/{file}'
        task = asyncio.create_task(process_file(full_path, semaphore))
        tasks.append(task)

    data = await asyncio.gather(*tasks)
    data = chain.from_iterable(data)
    data = prepare_data(data)
    load_to_json(data)


if __name__ == '__main__':
    asyncio.run(process_directory())
