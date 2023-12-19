import subprocess

# ...

@app.route('/uptime')
def get_uptime():
    try:
        # Выполняем команду ps для вывода списка процессов
        result = subprocess.check_output(['ps', 'aux'], text=True)
        uptime_message = f"Process list:\n{result}"
    except subprocess.CalledProcessError as e:
        # Обработка ошибок при выполнении команды
        uptime_message = f"Failed to get process list. Error: {e}"

    return uptime_message