import asyncio

# Определение функции worker, которая принимает на вход список чисел и событие
async def worker(numbers, event):

    # Цикл по числам в списке
    for number in numbers:

        # Если число равно 15, устанавливаем событие
        if number == 15:
            event.set()

        # Вывод на экран информации о поиске события
        print(f"Поиск события: Обрабатываемое число {number}")

        # Остановка на 0.3 секунды для эмуляции задержки
        await asyncio.sleep(0.3)

# Определение функции manager, которая принимает событие на вход
async def manager(event):

    # Вывод на экран сообщения о ожидании события
    print("Ожидаем событие")

    # Ожидание события
    await event.wait()

    # Вывод на экран сообщения о свершении события
    print("Событие свершилось")

# Определение функции main
async def main():

    # Создание списка чисел от 1 до 30
    numbers = range(1, 30)

    # Создание события
    event = asyncio.Event()

    # Запуск обоих корутин (worker и manager) и ожидание их завершения
    await asyncio.gather(worker(numbers, event), manager(event))


# Запуск функции main с помощью asyncio.run
asyncio.run(main())