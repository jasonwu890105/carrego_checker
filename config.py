class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:wd123WD123@localhost/carrego'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class EmailConfig(object):
    MAIL_SERVER = 'mail.tpgtelecom.com.au'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1.2
    #MAIL_USE_SSL = True
    MAIL_USERNAME = 't5721793admin@tpgtelecom.com.au'  # enter your email here
    MAIL_DEFAULT_SENDER = 't5721793@tpgtelecom.com.au' # enter your email here
    MAIL_PASSWORD = 'Summer23' # enter your password here

class CeleryConfig(object):
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    imports = ('app.tasks')
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'Australia/Sydney'
