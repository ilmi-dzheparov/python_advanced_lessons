FROM python:3.7.9-slim-stretch

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app
COPY . /app

EXPOSE 8000

RUN python -m pip install -r requirements.txt

# ENTRYPOINT ["gunicorn" , "-w", "4", "-b", "0.0.0.0:8000", "flask_app:app"]
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "flask_app:app"]