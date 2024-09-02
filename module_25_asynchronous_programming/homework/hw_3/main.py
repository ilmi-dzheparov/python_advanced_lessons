import time
from urllib.parse import urlparse, urlunparse

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


def parsing_of_page(url: str, count: int = COUNT, visited_urls=[]):

    url = normalize_url(url)
    if count <= 0 or url in visited_urls:
        print(url)
        return


    response = requests.get(url, timeout=(5, 5))
    # print(response)
    html = response.text()
    print(html)
    bs = BeautifulSoup(html,"lxml")
    print(bs.find_all('a'))
    for link in bs.find_all('a'):
        link_address = link.get("href")

        if not link_address:
            continue
        if not urlparse(link_address).scheme in ['http', 'https']:
            continue

        if link_address not in visited_urls:
            with open("links.txt", "a") as f:
                f.write(link_address + "\n")
            visited_urls.append(url)
            # print(visited_urls)
            parsing_of_page(link_address, count-1, visited_urls)


if __name__ == "__main__":
    start_time = time.time()
    parsing_of_page(URL, count=1)
    print(time.time() - start_time)