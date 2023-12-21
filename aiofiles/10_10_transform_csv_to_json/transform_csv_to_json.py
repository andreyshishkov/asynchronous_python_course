import asyncio
import aiofiles
import json
import csv
from aiocsv import AsyncReader
from typing import List, Dict


class CustomDialect(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\n'
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect('custom_dialect', CustomDialect)


def load_to_json(data: List[Dict[str, str]], path_to_save: str = 'data/result.json') -> None:
    with open(path_to_save, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print('Json-file is created')


async def transform_csv_to_json(filename: str) -> None:
    data = []

    async with aiofiles.open(filename, 'r', newline='', encoding='utf-8-sig') as file:
        headers = await file.readline()
        headers = headers.strip()
        headers = headers.split(';')
        async for row in AsyncReader(file, dialect='custom_dialect'):
            assert len(row) == len(headers)
            data_from_row = dict(zip(headers, row))
            data.append(data_from_row)

    load_to_json(data)


if __name__ == '__main__':
    asyncio.run(transform_csv_to_json('data/adress_1000000.csv'))
