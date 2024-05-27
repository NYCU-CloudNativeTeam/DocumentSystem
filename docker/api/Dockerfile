FROM python:3.10.14
ARG ENVIRONMENT

WORKDIR /app

COPY requirements/$ENVIRONMENT.txt requirements.txt

COPY system .

COPY system/controller/.env.sample controller/.env

RUN pip install --no-cache-dir -r requirements.txt

CMD sleep 10; python -m controller.app
