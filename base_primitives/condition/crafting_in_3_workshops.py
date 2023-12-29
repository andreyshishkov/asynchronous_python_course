import asyncio


stone_resources_dict = {
    'Каменная плитка': 10,
    'Каменная ваза': 40,
    'Каменный столб': 50,
}

metal_resources_dict = {
    'Металлическая цепь': 6,
    'Металлическая рамка': 24,
    'Металлическая ручка': 54,
}

cloth_resources_dict = {
    'Тканевая занавеска': 8,
    'Тканевый чехол': 24,
    'Тканевое покрывало': 48,
}

condition = asyncio.Condition()
crafting_done = asyncio.Event()
stone_storage, metal_storage, cloth_storage = 0, 0, 0


async def gather_stone():
    global stone_storage
    while stone_storage < 60:
        await asyncio.sleep(0.2)
        stone_storage += 10
        print(f'Добыто 10 ед. камня. На складе {stone_storage} ед.')
        async with condition:
            condition.notify_all()


async def gather_metal():
    global metal_storage
    while metal_storage < 60:
        await asyncio.sleep(0.2)
        metal_storage += 6
        print(f'Добыто 6 ед. металла. На складе {metal_storage} ед.')
        async with condition:
            condition.notify_all()


async def gather_cloth():
    global cloth_storage
    while cloth_storage < 60:
        await asyncio.sleep(0.2)
        cloth_storage += 8
        print(f'Добыто 8 ед. ткани. На складе {cloth_storage} ед.')
        async with condition:
            condition.notify_all()


async def craft_stone_items():
    global stone_storage
    for stone_item, required_stone_count in stone_resources_dict.items():
        async with condition:
            while stone_storage < required_stone_count:
                await condition.wait()
            stone_storage -= required_stone_count
            print(f'Изготовлен {stone_item} из камня.')
    crafting_done.set()


async def craft_metal_items():
    global metal_storage
    for metal_item, required_metal_count in metal_resources_dict.items():
        async with condition:
            while metal_storage < required_metal_count:
                await condition.wait()
            metal_storage -= required_metal_count
            print(f'Изготовлен {metal_item} из металла.')
    crafting_done.set()


async def craft_cloth_items():
    global cloth_storage
    for cloth_item, required_cloth_count in cloth_resources_dict.items():
        async with condition:
            while cloth_storage < required_cloth_count:
                await condition.wait()
            cloth_storage -= required_cloth_count
            print(f'Изготовлен {cloth_item} из ткани.')
    crafting_done.set()


async def main():
    gather_stone_task = asyncio.create_task(gather_stone())
    gather_metal_task = asyncio.create_task(gather_metal())
    _ = asyncio.create_task(gather_cloth())

    _ = asyncio.create_task(craft_stone_items())
    _ = asyncio.create_task(craft_metal_items())
    _ = asyncio.create_task(craft_cloth_items())

    await crafting_done.wait()


if __name__ == '__main__':
    asyncio.run(main())