FROM python:3.10.8-slim-buster

RUN apt-get update && apt-get upgrade -y

COPY . .

RUN pip install --upgrade pip
RUN pip install --upgrade poetry
RUN poetry install
