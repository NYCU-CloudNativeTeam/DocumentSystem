FROM python:3.10.14
ARG ENVIRONMENT

WORKDIR /app

COPY requirements/$ENVIRONMENT.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./system .

CMD sleep 15; python -m email_notification_system.main