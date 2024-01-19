import logging

# Шаг 1: Создаем логгеры
logging.basicConfig(level=logging.DEBUG)
root_logger = logging.getLogger('root')
sub_1_logger = logging.getLogger('root.sub_1')
sub_2_logger = logging.getLogger('root.sub_2')
sub_sub_1_logger = logging.getLogger('root.sub_2.sub_sub_1')

# Шаг 2: Добавляем обработчик для логгеров sub_1 и sub_sub_1
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)s')
handler.setFormatter(formatter)
sub_1_logger.addHandler(handler)
sub_sub_1_logger.addHandler(handler)

# Шаг 3: Создаем форматтер и добавляем его к обработчику
formatter = logging.Formatter('%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)s')
handler.setFormatter(formatter)

# Шаг 4: Создаем обработчик для root с уровнем DEBUG и добавляем форматтер
root_handler = logging.StreamHandler()
root_handler.setLevel(logging.DEBUG)
root_handler.setFormatter(formatter)
root_logger.addHandler(root_handler)

# Шаг 5: Запрещаем передачу сообщений из sub_2 в root
sub_2_logger.propagate = False

# Пример использования
sub_1_logger.info('This is an INFO message from sub_1')
sub_sub_1_logger.debug('This is a DEBUG message from sub_sub_1')

logging.FileHandler()
