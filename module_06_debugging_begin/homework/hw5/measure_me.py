"""
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
можно отследить, сколько времени выполняется функция.

Программа, которую вы видите, по умолчанию пишет логи в stdout. Внутри неё есть функция measure_me,
в начале и в конце которой пишется "Enter measure_me" и "Leave measure_me".
Сконфигурируйте логгер, запустите программу, соберите логи и посчитайте среднее время выполнения функции measure_me.
"""
import logging
import random
import sys
from typing import List




def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.debug("Enter measure_me")
    results = []
    nums.sort()


    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")

        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.debug("Leave measure_me")
    # print(logger.handlers)
    print(sys.stdout)

    return results

def time_to_sec(time: str) -> float:
    time = time.replace(",", ".")
    time_l = time.split(":")
    time_sec = int(time_l[0]) * 3600 + int(time_l[1]) * 3600 + float(time_l[2])
    return time_sec


if __name__ == "__main__":
    logging.basicConfig(
        level="DEBUG",
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="mesure.log",
        filemode="w",
        # datefmt="%H:%M:%S.%f"
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


    # print(console_handler.)

    for it in range(15):
        data_line = get_data_line(10 ** 1)
        measure_me(data_line)
    with open("mesure.log", "r") as file:
        lines = file.readlines()
        time_begin = time_to_sec(lines[2].split()[1])
        time_end = time_to_sec(lines[len(lines)-1].split()[1])
        print(time_end, time_begin)
        print(f"Время выполнения функции mesure_me: {time_end - time_begin:.3f} сек")