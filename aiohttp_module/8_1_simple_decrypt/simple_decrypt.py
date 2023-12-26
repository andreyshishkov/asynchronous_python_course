import asyncio
import aiohttp
from bs4 import BeautifulSoup


code_dict = {
    0: 'F',
    1: 'B',
    2: 'D',
    3: 'J',
    4: 'E',
    5: 'C',
    6: 'H',
    7: 'G',
    8: 'A',
    9: 'I'
}


def decrypt_message(message: str):
    decrypted_message = ''
    for symbol in message:
        if symbol.isdigit():
            decrypted_message += code_dict[int(symbol)]
    return decrypted_message


async def process_page():
    url = 'https://asyncio.ru/zadachi/1/index.html'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'lxml')
    message = soup.find('p').text
    decrypted_message = decrypt_message(message)

    print(decrypted_message)


if __name__ == '__main__':
    asyncio.run(process_page())
