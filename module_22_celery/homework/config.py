"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""
from celery import Celery


# https://yandex.ru/support/mail/mail-clients/others.html

SMTP_USER = "mail@yandex.ru"
SMTP_HOST = "smtp.yandex.com"
SMTP_PASSWORD = "qwerty"
SMTP_PORT = 587


def make_celery(app_name: str) -> Celery:
    # Создание экземпляра Celery
    celery = Celery(
        app_name,  # Имя приложения Celery
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )

    return celery