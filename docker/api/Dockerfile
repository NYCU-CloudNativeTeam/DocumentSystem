FROM python:3.10.14
ARG ENVIRONMENT

WORKDIR /app

COPY requirements/$ENVIRONMENT.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./system .
EXPOSE 5000

CMD sleep 10; python -m controller.app