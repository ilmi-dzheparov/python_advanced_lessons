from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/uptime', methods=['GET'])
# def get_uptime():
#     try:
#         # Выполнение команды uptime
#         result = subprocess.check_output(['uptime'])
#         print(result)
#         # Декодирование байтового вывода в строку
#         uptime_string = result.decode('utf-8').strip()
#         print(uptime_string)
#         # Разбиение строки по запятой и взятие первого элемента
#         uptime = uptime_string.split(',')[0]
#
#         return f"Current uptime is {uptime}"
#     except Exception as e:
#         return f"Error getting uptime: {str(e)}", 500

def uptime1():
    raw = subprocess.check_output(['uptime', '-p']).decode("utf8")#.replace(',', '')
    print(raw[3:])
    # days = int(raw.split()[2])
    # if 'min' in raw:
    #     hours = 0
    #     minutes = int(raw[4])
    # else:
    #     hours, minutes = map(int,raw.split()[4].split(':'))
    # totalsecs = ((days * 24 + hours) * 60 + minutes) * 60
    return "None" #totalsecs


if __name__ == '__main__':
    app.run(debug=True)