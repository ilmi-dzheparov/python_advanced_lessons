"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
import re
from typing import List


def my_t9(input_numbers: str) -> List[str]:
    digit_letters = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz"
    }
    for sym in input_numbers:
        if sym not in digit_letters.keys():
            raise ValueError("Input should consist of digits 2-9 only")

    with open("words.txt", "r") as file:
        words_list: List[str] = file.readlines()

    def search_words(words, letters, n) -> List[str]:
        string = '.' * (n-1) + f'[{letters}].'
        # print(string)
        pattern = re.compile(f"^{string}", re.IGNORECASE)
        matching_words = [word for word in words if pattern.match(word)]

        return matching_words

    new_words = words_list
    n = 1
    for sym in input_numbers:
        letters = digit_letters[sym]
        new_words = search_words(new_words, letters, n)
        n += 1

    return new_words

if __name__ == '__main__':
    numbers: str = input()
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')
