import asyncio
import time
from urllib.parse import urlparse, urlunparse, urljoin

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

URL = 'https://www.yandex.com'
COUNT = 3


def normalize_url(url: str) -> str:
    """
    Приведение URL к стандартному виду: удаление фрагментов и нормализация пути.
    """
    parsed_url = urlparse(url)
    # Убираем фрагменты и query параметры
    normalized_url = parsed_url._replace(fragment='', query='')
    return urlunparse(normalized_url)


async def get_bs(client: aiohttp.ClientSession, url: str):
    try:
        async with client.get(url) as response:
            html = await response.text()
            bs = BeautifulSoup(html, "lxml")
            # print(bs)
            return bs
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def write_to_file(content: str):
    file_path = "links_parsed.txt"
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(content + '\n')


async def parsing_of_page(client: aiohttp.ClientSession, url: str, count: int, visited_urls: set):
    url = normalize_url(url)
    if count <= 0 or url in visited_urls:
        return

    visited_urls.add(url)

    count -= 1

    bs = await get_bs(client, url)

    if bs is None:
        return
    # print(bs.find_all('a'))

    for link in bs.find_all('a'):
        link_address = link.get("href")

        if not link_address:
            continue

        link_address = urljoin(url, link_address)  # Обработка относительных ссылок
        if not urlparse(link_address).scheme in ['http', 'https']:
            continue

        if link_address not in visited_urls:
            # print(link_address)
            await write_to_file(link_address)
            await parsing_of_page(client, link_address, count, visited_urls)


async def main(count: int = COUNT):
    timeout = aiohttp.ClientTimeout(total=10)
    connector = aiohttp.TCPConnector(limit_per_host=10)
    visited_urls = set()

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as client:
        await parsing_of_page(client, URL, count, visited_urls)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main(count=2))
    print(time.time() - start_time)
