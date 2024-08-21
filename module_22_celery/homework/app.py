from flask import Flask, request, jsonify
from celery import Celery, group
from celery_module import process_image, celery
from config import make_celery
from models import User


app = Flask("__name__")

# celery = make_celery(app.name)
# celery.conf.update(
#         result_expires=3600,
#         timezone='UTC',
#     )


@app.route("/blur", methods=["POST"])
def process_images():
    """Ставит в очередь обработку переданных изображений. Возвращает ID группы задач по обработке изображений."""
    images = request.json.get("images")

    if images and isinstance(images, list):
        for image in images:
            if not image.get("src_filename"):
                return jsonify({"error": "src_filename is required"}), 400
        task_group = group(
            process_image.s(image.get("src_filename"), image.get("dst_filename"))
            for image in images
        )
        result = task_group.apply_async()
        result.save()
        return jsonify({"group_id": result.id}), 202
    else:
        return jsonify({"error": "Missing of invalid images names"}), 400


@app.route("/status/<group_id>", methods=["GET"])
def get_status(group_id: str):
    """Возвращает информацию о задаче: прогресс (количество обработанных задач) и статус (в процессе обработки, обработано)"""
    result = celery.GroupResult.restore(group_id)
    print(result)
    if result:
        count = result.completed_count()
        status = count / len(result)
        if status == 1:
            return jsonify({"Count of completed tasks": count, "status": "processed"})
        else:
            return jsonify(
                {"Count of completed tasks": count, "status": "in processing"}
            )
    else:
        return jsonify({"error": "invalid group_id"})


@app.route("/subscribe", methods=["POST"])
def subscribe():
    """Пользователь указывает почту и подписывается на рассылку. Каждую неделю ему будет приходить письмо о сервисе на почту"""
    order_id = "1"
    filename = "mail.py"
    receiver_email = request.get_json("receiver_email")
    if receiver_email:
        # subscribe_user.apply_async(args=[order_id, receiver_email.get("email"), filename],)
        User.set_user_subscribed(receiver_email.get("email"), order_id, filename)
        return jsonify({"message": "Client is subscribed"}), 200
    else:
        return jsonify({"error": "email is required"}), 400


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    """Пользователь указывает почту и отписывается от рассылки"""
    receiver_email = request.get_json("receiver_email")
    if receiver_email:
        User.set_user_unsubscribed(receiver_email.get("email"))
        return jsonify({"message": "Client is unsubscribed"}), 200
    else:
        return jsonify({"error": "email is required"}), 400


if __name__ == "__main__":
    app.run(debug=True)
