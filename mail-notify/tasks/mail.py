from flask_mail import Message

from base import app, mail_app
from tasks import celery_app


@celery_app.task
def send_mail(recipients, title, content):
    with app.app_context():
        msg = Message(title, recipients=[recipients])
        msg.body = content
        mail_app.send(msg)