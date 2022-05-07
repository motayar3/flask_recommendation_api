# syntax=docker/dockerfile:1

FROM python:3.9-buster
MAINTAINER Anonymous <anon@example.com>


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1



COPY ./requirements.txt /requirements.txt
EXPOSE 5000
WORKDIR /app
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
   /py/bin/pip install -r /requirements.txt  

RUN useradd -ms /bin/bash user

USER user
COPY ./app /app
CMD ["/py/bin/python", "app.py"]