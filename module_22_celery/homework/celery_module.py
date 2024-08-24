from typing import Optional
from models import User
from celery import Celery, group
from celery.schedules import crontab

from image import blur_image
from config import make_celery
import random
import time
from mail import send_email


celery = make_celery("tasks")
# celery.conf.update(
#     result_expires=3600,
#     timezone="UTC",
# )


@celery.task
def process_image(src_filename: str, dst_filename: Optional[str] = None):
    # time.sleep(random.randint(5, 15))
    time.sleep(45)
    blur_image(src_filename, dst_filename)

    return f"Image {src_filename} processed"


@celery.task
def send_email_task():
    users = User.get_subscribed_users()
    if users is not None:
        for user in users:
            order_id = user.order_id
            email = user.email
            filename = user.filename
            send_email(order_id, email, filename)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15, send_email_task.s(), name="send_every_15_sec")
    sender.add_periodic_task(
        # crontab(),
        crontab(hour=12, minute=30, day_of_week=1),
        send_email_task.s(),
        name="send_mail_weekly",
    )


# celery.conf.beat_schedule = {
#     "send_email": {
#         "task": "celery_module.send_email_task",
#         "schedule": 15.0,  # Интервал выполнения задачи в секундах
#         # 'args': ("111", "mail@yandex.ru", "db_1.png")
#     }
# }
