import asyncio
import aiofiles
import glob
import json
from aiocsv import AsyncReader
from typing import List, Dict


HEADERS = [
    'ФИО',
    'Возраст',
    'Пол',
    'Город проживания',
    'ВУЗ',
    'Факультет',
    'Балл ЕГЭ',
    'Телефон для связи',
]


def get_filenames() -> List[str]:
    return glob.glob('data/region_student/region_student/Задача Студенты/*/*.csv')


def load_to_json(pupils: List[Dict[str, str]], path_to_save: str = 'data/result.json') -> None:
    with open(path_to_save, 'w', encoding='utf-8') as file:
        json.dump(pupils, file, ensure_ascii=False, indent=4)
    print('File is created')


async def add_excellent_pupils_from_file(
        filename: str,
        excellent_pupils: List[Dict[str, str]],
        semaphore: asyncio.Semaphore
) -> None:
    async with semaphore:
        async with aiofiles.open(filename, mode='r', newline='', encoding='utf-8-sig') as file:
            await file.readline()

            async for row in AsyncReader(file):
                ege_points = row[6]
                if ege_points == '100':
                    pupil_data = dict(zip(HEADERS, row))
                    excellent_pupils.append(pupil_data)


async def main():
    filenames = get_filenames()
    print(f'Number of files: {len(filenames)}')
    excellent_pupils = []
    semaphore = asyncio.Semaphore(500)

    tasks = []
    for filename in filenames:
        task = asyncio.create_task(add_excellent_pupils_from_file(filename, excellent_pupils, semaphore))
        tasks.append(task)

    await asyncio.gather(*tasks)

    excellent_pupils.sort(key=lambda x: x['Телефон для связи'])
    load_to_json(excellent_pupils)


if __name__ == '__main__':
    asyncio.run(main())