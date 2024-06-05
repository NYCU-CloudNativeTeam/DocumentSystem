FROM python:3.10.14
ARG ENVIRONMENT

WORKDIR /app

COPY requirements/$ENVIRONMENT.txt requirements.txt

COPY system .

RUN pip install --no-cache-dir -r requirements.txt

CMD sleep 15; python -m controller.app
