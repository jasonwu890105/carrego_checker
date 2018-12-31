from flask import Flask
from config import Config, EmailConfig, CeleryConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from sqlalchemy import event
from redis import Redis
from flask_rq2 import RQ
#import rq
from celery import Celery
from celery.schedules import crontab
import celeryconfig
import flask_excel as excel 


app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
app.config.from_object(EmailConfig)
app.config.from_object(CeleryConfig)

### Flask-RQ Configuration
#app.config['RQ_REDIS_URL'] = 'redis://localhost:6379/0'


db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
app.secret_key = "flask rocks!"

mail = Mail(app)
excel.init_excel(app)
#rq = RQ(app)

#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

'''
celery = Celery('tasks')
celery.conf.enable_utc = False
celery.config_from_object(CeleryConfig)
'''

#app.redis = Redis.from_url(app.config['REDIS_URL'])
#app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)


'''
def create_app(config_class=RedisConfig):
    # ...
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    # ...
'''

if __name__ == "__main__":
    app.run(debug=True)




from app import routes, models, forms, tasks, table
#from app.tasks import check_rego


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = make_celery(app)



'''
@celery.task
def email_notification():
    check_rego()
'''

#email_notification.cron('45 23 * * *', 'Sending-Notification-Email')

'''
celery.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'send-emailnotify': {
        'task': 'email_notification',
        'schedule': crontab(hour=1, minute=0),
    },
}
'''

