import logging
import sys
import json
import requests
from logging import handlers


class LevelFileHandler(logging.Handler):
    def __init__(self, file_name_debug_info, file_name_error, mode="a"):
        super().__init__()
        self.file_name_debug_info = file_name_debug_info
        self.file_name_error = file_name_error
        self.mode = mode
    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        log_level = message.split()[0]
        if log_level in ["DEBUG", "INFO"]:
            with open(self.file_name_debug_info, self.mode) as f:
                f.write(message + '\n')
        if log_level == "ERROR":
            with open(self.file_name_error, self.mode) as f:
                f.write(message + '\n')


class JsonHTTPHandler(logging.handlers.HTTPHandler):
    def __init__(self, host, url, method='POST'):
        super().__init__(host, url)
        self.host = host
        self.url = url
        self.method = method

    def emit(self, record):
        log_entry = self.mapLogRecord(record)
        log_json = json.dumps(log_entry)

        # Отправляем лог в JSON-формате
        try:
            response = self.send_log_to_server(log_json)
            response.raise_for_status()
            print("Log is successfully sended to server")
        except Exception as e:
            print(f"Error while sending log to server: {e}")

    def send_log_to_server(self, log_entry):
        if self.method == "POST":
            log_json = json.dumps(log_entry)
            headers = {'Content-Type': 'application/json'}
            response = requests.request(self.method, self.host + self.url, data=log_json, headers=headers)
            return response
        if self.method == "GET":
            response = requests.get(self.host + self.url, params=log_entry)
            return response



# def get_logger(name):
#     ...
#     return logger

