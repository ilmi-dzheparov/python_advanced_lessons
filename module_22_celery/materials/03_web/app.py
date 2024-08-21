import random

from flask import Flask, request, jsonify
from flask_caching import Cache
from celery import Celery, group
import time

app = Flask(__name__)

# Конфигурация Celery
celery = Celery(
    app.name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 10  # Кэшируем на 10 секунд
cache = Cache(app)

# @app.before_request
# def setup_cache():
#     # Инициализация кэша
#     get_celery_control_info()


@cache.cached(timeout=10, key_prefix='celery_control_info')
def get_celery_control_info():
    # Получение информации о задачах и очередях
    control = celery.control.inspect()
    active_tasks = control.active()
    scheduled_tasks = control.scheduled()
    reserved_tasks = control.reserved()
    registered_tasks = control.registered()

    return {
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks,
        'reserved_tasks': reserved_tasks,
        'registered_tasks': registered_tasks,
    }


@app.route('/control', methods=['GET'])
def control_info():
    # Возвращаем кэшированные данные
    return jsonify(get_celery_control_info())


# Задача Celery для обработки изображения
@celery.task
def process_image(image_id):
    # В реальной ситуации здесь может быть обработка изображения
    # В данном примере просто делаем задержку для демонстрации
    time.sleep(random.randint(5, 15))
    return f'Image {image_id} processed'


@app.route('/process_images', methods=['POST'])
def process_images():
    images = request.json.get('images')

    if images and isinstance(images, list):
        # Создаем группу задач
        task_group = group(
            process_image.s(image_id)
            for image_id in images
        )

        # Запускаем группу задач и сохраняем ее
        result = task_group.apply_async()
        result.save()

        # Возвращаем пользователю ID группы для отслеживания
        return jsonify({'group_id': result.id}), 202
    else:
        return jsonify({'error': 'Missing or invalid images parameter'}), 400


@app.route('/status/<group_id>', methods=['GET'])
def get_group_status(group_id):
    result = celery.GroupResult.restore(group_id)

    if result:
        # Если группа с таким ID существует,
        # возвращаем долю выполненных задач
        status = result.completed_count() / len(result)
        return jsonify({'status': status}), 200
    else:
        # Иначе возвращаем ошибку
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route('/cancel/<group_id>', methods=['GET'])
def cancel_group(group_id):
    result = celery.GroupResult.restore(group_id)

    if result:
        # Если группа с таким ID существует,
        # возвращаем долю выполненных задач
        result.revoke()
        return jsonify({'message': 'Group is canceled'}), 200
    else:
        # Иначе возвращаем ошибку
        return jsonify({'error': 'Invalid group_id'}), 404


if __name__ == '__main__':
    app.run(debug=True)
