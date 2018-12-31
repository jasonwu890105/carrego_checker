from flask_mail import Message
from app import mail
from flask import render_template
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from app.models import Cars


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)



