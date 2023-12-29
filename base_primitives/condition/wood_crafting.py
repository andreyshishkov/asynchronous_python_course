import asyncio

wood_resources_dict = {
    'Деревянный меч': 6,
    'Деревянный щит': 12,
    'Деревянный стул': 24,
}
storage = 0
crafting_done = asyncio.Event()
condition = asyncio.Condition()

results = []


async def gather_wood():
    global storage
    while storage < 35:
        await asyncio.sleep(1)
        storage += 2
        print(f"Добыто 2 ед. дерева. На складе {storage} ед.")
        async with condition:
            condition.notify()


async def craft_item():
    global storage
    for item, required_wood in wood_resources_dict.items():
        async with condition:
            while storage < required_wood:
                await condition.wait()
            storage -= required_wood
            print(f"Изготовлен {item}.")

    crafting_done.set()


async def main():
    _ = asyncio.create_task(gather_wood())
    _ = asyncio.create_task(craft_item())

    await crafting_done.wait()


if __name__ == '__main__':
    asyncio.run(main())