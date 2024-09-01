import asyncio
from pathlib import Path
import time

import aiohttp
# import aiofiles

# URL = 'https://cataas.com/cat'
URL = 'https://picsum.photos/200'
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        print(response.status)
        result = await response.read()
        await asyncio.to_thread(write_to_disk, result, idx)
        # write_to_disk(result, idx)


def write_to_disk(content: bytes, id: int):
    file_path = "{}/cat_{}.png".format(OUT_PATH, id)
    with open(file_path, 'wb') as f:
        f.write(content)


# async def write_to_disk(content: bytes, id: int):
#     file_path = "{}/{}.png".format(OUT_PATH, id)
#     async with aiofiles.open(file_path, mode='wb') as f:
#         await f.write(content)


async def get_all_cats():

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


def main():
    res = asyncio.run(get_all_cats())
    print(len(res))


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(end_time - start_time)
