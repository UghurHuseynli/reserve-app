from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_task(subject, message, to_email):
    email = EmailMessage(subject, message, to=[to_email])
    if email.send():
        return 'ok'
    else:
        return 'problem'