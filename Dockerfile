# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /foodbot
ENV FLASK_APP=main.py
RUN python -m venv venv
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "flask", "run"]
