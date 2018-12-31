from celery.schedules import crontab 


'''
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 a.m.
    'send-emailnotify': {
        'task': 'tasks.email_notification',
        'schedule': crontab(hour=12, minute=17),
        'args' : ()
    },
}
'''


CELERY_IMPORTS = ('app.tasks')
#CELERY_TASK_RESULT_EXPIRES = 30
#CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
  
    'send-emailnotify': {
        'task': 'app.tasks.email_notification',
        'schedule': crontab(hour=15, minute=30),
    },
}