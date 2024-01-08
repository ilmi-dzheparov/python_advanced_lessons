"""
1. Сконфигурируйте логгер программы из темы 4 так, чтобы он:

* писал логи в файл stderr.txt;
* не писал дату, но писал время в формате HH:MM:SS,
  где HH — часы, MM — минуты, SS — секунды с ведущими нулями.
  Например, 16:00:09;
* выводил логи уровня INFO и выше.

2. К нам пришли сотрудники отдела безопасности и сказали, что, согласно новым стандартам безопасности,
хорошим паролем считается такой пароль, который не содержит в себе слов английского языка,
так что нужно доработать программу из предыдущей задачи.

Напишите функцию is_strong_password, которая принимает на вход пароль в виде строки,
а возвращает булево значение, которое показывает, является ли пароль хорошим по новым стандартам безопасности.

Хорошим паролем считается пароль, в котором есть как минимум восемь символов, большие и маленькие буквы,
а также как минимум одна цифра и один символ из списка !@#$%^&*()-+=_

Сделайте так, чтобы при вводе пароля проверялось, является ли пароль хорошим. И если нет — предупредите пользователя
(с помощью warning, конечно), что введённый пароль слабый. В идеале ещё и объясните почему.

"""

import getpass
import hashlib
import logging
import re

logger = logging.getLogger("password_checker")

global words_list
with open("words.txt", "r") as file:
    words_list = [line.strip().lower() for line in file if len(line.strip()) > 4]

def is_strong_password(password: str) -> bool:
    list_of_symbols = "!@#$%^&*()-+=_"
    count_sym = 0
    count_num = 0
    if len(password) >= 8:
        for i in password:
            if i.isdigit():
                count_num += 1
            if i in list_of_symbols:
                count_sym +=1
            if count_num >= 1 and count_sym >= 1:
                words_in_password = re.findall(r'\b[a-zA-Z]{5,}\'s\b|\b[a-zA-Z]{5,}\b', password.lower())
                print(words_in_password)
                for word in words_in_password:
                    if word in words_list:
                        return False
                return True
    return False


def input_and_check_password() -> bool:
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False
    elif not is_strong_password(password):
        logger.warning("Вы ввели слишком слабый пароль")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="stderr.txt",
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
    )
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
