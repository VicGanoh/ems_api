FROM python:3.9.18-alpine3.19

LABEL maintainer="vicgan.io"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY . /app
COPY ./scripts /scripts

EXPOSE 8000

RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip && \
    apk update && apk add --no-cache build-base postgresql-dev musl-dev linux-headers && \
    /env/bin/pip install -r /requirements.txt --no-cache-dir && \
    adduser --disabled-password --no-create-home app && \
    chmod -R +x /scripts && \
    mkdir -p /app/staticfiles && \
    chown -R app:app /app/staticfiles && \
    chmod -R 755 /app/staticfiles && \
    chown -R app:app /app

ENV PATH="/env/bin:$PATH"

USER app