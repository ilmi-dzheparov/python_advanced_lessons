import asyncio
import time
from urllib.parse import urlparse, urlunparse

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup

URL = 'https://www.yandex.com'
COUNT = 2


def normalize_url(url: str) -> str:
    """
    Приведение URL к стандартному виду: удаление фрагментов и нормализация пути.
    """
    parsed_url = urlparse(url)
    # Убираем фрагменты и query параметры
    normalized_url = parsed_url._replace(fragment='', query='')
    return urlunparse(normalized_url)


async def get_bs(client: aiohttp.ClientSession, url: str):
    async with client.get(url) as response:
        # print(response.status)
        html = await response.text()
        bs = BeautifulSoup(html,"lxml")
        return bs


async def write_to_file(content: str):
    file_path = "links_parsed.txt"
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(content + '\n')


async def parsing_of_page(url: str, count: int = COUNT, visited_urls=[]):
    # if visited_urls is None:
    #     visited_urls = []
    url = normalize_url(url)
    if count <= 0 or url in visited_urls:
        print(url)
        return
    with open("links_parsed.txt", "a") as f:
        f.write(url + "\n")
    count -= 1

    timeout = aiohttp.ClientTimeout(total=10)
    connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as client:
        bs = await get_bs(client, url)

        # print(bs.find_all('a'))
        for link in bs.find_all('a'):
            link_address = link.get("href")

            if not link_address:
                continue
            if not urlparse(link_address).scheme in ['http', 'https']:
                continue

            if link_address not in visited_urls:
                with open("links_parsed.txt", "a") as f:
                    f.write(link_address + "\n")
                # await write_to_file(link_address)
                # print(visited_urls)
                await parsing_of_page(link_address, count, visited_urls)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(parsing_of_page(URL, count=3))
    print(time.time() - start_time)