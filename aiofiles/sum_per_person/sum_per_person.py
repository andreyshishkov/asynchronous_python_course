import aiofiles
import asyncio
import json
from typing import Tuple, Dict, List, DefaultDict
from collections import defaultdict


def sort_dict(user2cost: DefaultDict[str, float]) -> Dict[str, str]:
    data = [(user, cost) for user, cost in user2cost.items()]
    data.sort(key=lambda x: x[1], reverse=True)

    data = [(user, f'{round(cost, 2)}р') for user, cost in data]

    return dict(data)


def get_user_and_message(log: str) -> Tuple[str, str]:
    _, user_and_message = log.split(' - ', 1)
    user, message = user_and_message.split(': ', 1)
    message = message.strip()
    return user, message


def get_sum_from_log(log: str) -> Tuple[str, float]:
    user, message = get_user_and_message(log)
    cost = 0.03 * len(message)
    return user, cost


def add_cost_per_user_from_logs(logs: List[str], user2cost: DefaultDict[str, float]) -> None:

    for log in logs:
        user, cost = get_sum_from_log(log)
        user2cost[user] += cost


async def add_sums_into_dict_from_file(filename: str, user2cost: DefaultDict[str, float]) -> None:
    async with aiofiles.open(filename, mode='r', encoding='utf-8') as file:
        logs = await file.readlines()

    add_cost_per_user_from_logs(logs, user2cost)


async def main():
    filenames = [f'data/chat_log/chat_{i}.txt' for i in range(1, 2001)]
    user2cost = defaultdict(float)

    tasks = []
    for filename in filenames:
        task = asyncio.create_task(add_sums_into_dict_from_file(filename, user2cost))
        tasks.append(task)

    await asyncio.gather(*tasks)

    sorted_dict = sort_dict(user2cost)

    print(json.dumps(sorted_dict, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    asyncio.run(main())
