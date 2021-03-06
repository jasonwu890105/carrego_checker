from app import app, mail
from app.models import Cars
from flask_mail import Message
#import redis
#from rq import Worker, Queue, Connection
#from celery import Celery
#import app.celeryconfig
import celery



'''
celery = Celery('tasks')
celery.config_from_object('celeryconfig')
celery.conf.enable_utc = False
'''


def send_email(subject, sender, recipients, text_body):

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)


def check_rego():
    with app.app_context():
        daysleftlist = Cars.query.all()
        for dayleft in daysleftlist:
            if dayleft.rego_daysleft == 10:
                send_email('%s is expiring in %d days' % (dayleft.regonum, dayleft.rego_daysleft),
                        'Marylin.Suiza@tpgtelecom.com.au', [dayleft.email], 'We have detected your car with Rego Plate %s will be expiring at %s' % (dayleft.regonum, dayleft.expirydate))

@celery.task
def email_notification():
    check_rego()

'''
listen = ['default']
REDIS_URL = 'redis://localhost:6379/0'
conn = redis.from_url(REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
'''
