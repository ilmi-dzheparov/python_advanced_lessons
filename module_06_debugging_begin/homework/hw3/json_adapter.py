"""
Удобно сохранять логи в определённом формате, чтобы затем их можно было фильтровать и анализировать. 
Сконфигурируйте логгер так, чтобы он писал логи в файл skillbox_json_messages.log в следующем формате:

{"time": "<время>", "level": "<уровень лога>", "message": "<сообщение>"}

Но есть проблема: если в message передать двойную кавычку, то лог перестанет быть валидной JSON-строкой:

{"time": "21:54:15", "level": "INFO", "message": "“"}

Чтобы этого избежать, потребуется LoggerAdapter. Это класс из модуля logging,
который позволяет модифицировать логи перед тем, как они выводятся.
У него есть единственный метод — process, который изменяет сообщение или именованные аргументы, переданные на вход.

class JsonAdapter(logging.LoggerAdapter):
  def process(self, msg, kwargs):
    # меняем msg
    return msg, kwargs

Использовать можно так:

logger = JsonAdapter(logging.getLogger(__name__))
logger.info('Сообщение')

Вам нужно дописать метод process так, чтобы в логах была всегда JSON-валидная строка.
"""
import json
import logging
import re
from datetime import datetime


class JsonAdapter(logging.LoggerAdapter):


    def process(self, msg, kwargs):
        print(kwargs)
        time = datetime.now().time().strftime("%H:%M:%S")
        level= kwargs.pop('lev', self.extra['lev'])
        print(level)
        if len(re.findall(r'\"', msg)) % 2 == 1:
            msg += '"'
        msg = {"time": str(time), "level": level, "message": msg}
        msg = json.dumps(msg, ensure_ascii=False)

        return msg, kwargs




if __name__ == '__main__':
    logger = JsonAdapter(logging.getLogger(__name__), {"lev": "UNKNOWN"})
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(filename='skillbox_json_messages.log',
                        level=logging.DEBUG,
                        format='%(message)s')
    logger.info("Cообщение", lev="INFO")
    logger.error('"Кавычка)"', lev="ERROR")
    logger.debug("Еще одно сообщение", lev="DEBUG")

