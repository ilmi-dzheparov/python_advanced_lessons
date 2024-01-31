FROM python:3.11-slim

RUN mkdir "/app"

COPY requirements.txt /app/

RUN ["python", "-m", "pip", "install", "-r", "/app/requirements.txt"]

COPY . /app/

WORKDIR /app

ENTRYPOINT ["python", "app.py"]
