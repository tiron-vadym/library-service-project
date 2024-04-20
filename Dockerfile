FROM python:3.11-slim
LABEL maintainer="tironvadim1@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

RUN apt-get update && apt-get install -y zlib1g-dev libjpeg-dev gcc musl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user
