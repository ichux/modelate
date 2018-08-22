# -*- coding: utf-8 -*-
"""
    blueprint.modelate.config
    ----------------------
    A module providing all the configuration of the blueprint.
"""

import datetime
import os

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')


# noinspection PyUnresolvedReferences
class Config(object):
    # http://flask.pocoo.org/docs/config/#development-production
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)  # , seconds=60 * 30 = 30 minutes
    SECRET_KEY = os.getenv('SECRET_KEY')
    SITE_NAME = os.getenv('SITE_NAME')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAINTENANCE_MODE = False
    ACTIVATE_READ_ONLY = False

    # whoosh
    ELOG_NAME = 'ELIX'
    MAX_WHOOSH_SEARCH_RESULTS = 200
    SHOW_ERROR_LOG = False

    # FOR DB MODELS
    CASCADE = "all, delete-orphan"
    LAZY = 'joined'

    ALLOWED_BOOK_EXTENSIONS = {'pdf', 'zip'}
    ALLOWED_USERS_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    FILE_SIZE = 70 * 1024 * 1024
    UPLOAD_BYTE_SIZE = 2 ** 20

    # WTF_CSRF_SECRET_KEY = ''  # Used to securely sign the csrf_token if provided
    # WTF_CSRF_TIME_LIMIT = 600  # Number of seconds that the csrf_token is valid if provided

    # gmail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')

    # GMAIL_SETTINGS = {
    #     'mail_username': os.getenv('MAIL_USERNAME'),
    #     'mail_password': os.getenv('EMAIL_FROM'),
    #     'mail_server': 'smtp.gmail.com',
    #     'mail_use_tls': False,
    #     'mail_use_ssl': True,
    #     'mail_port': 465
    # }

    # work mail settings
    SMTP_EMAIL_SETTINGS = {
        'email_from': os.getenv('EMAIL_FROM'),
        'email_smtp': os.getenv('EMAIL_SMTP'),
        'email_username': os.getenv('EMAIL_USERNAME'),
        'email_password': os.getenv('EMAIL_PASSWORD')
    }

    # flask session settings
    SESSION_TYPE = 'sqlalchemy'
    SESSION_USE_SIGNER = True

    # recaptcha
    RECAPTCHA_ENABLED = False
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
    RECAPTCHA_THEME = "light"  # "dark"
    RECAPTCHA_TYPE = "audio"  # "image"
    RECAPTCHA_SIZE = "compact"  # "normal"
    RECAPTCHA_RTABINDEX = 10

    # celery configurations
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_DB_NO, REDIS_HOST, REDIS_PORT = 0, "192.168.56.20", 6379
    CACHE_REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    TTL_REDIS_BACKEND = 60

    # celery configurations
    CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    SESSION_WITH_REDIS = {"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB_NO, "password": REDIS_PASSWORD}
    CELERYBEAT_SCHEDULE = {
        'every-10s': {
            # 'task': 'tasks.hello',
            # 'schedule': datetime.timedelta(seconds=10)
        },
        'every-15s': {
            # 'task': 'tasks.add_async_digits',
            # 'schedule': datetime.timedelta(seconds=15),
            # 'args': (12, 3)
        },
        'every-60s': {
            # 'task': 'tasks.playful_add',
            # 'schedule': crontab(minute='*/1'),  # crontab(hour=9, minute=10)
            # 'args': (12, 3)
        },
        'optimize_indexes': {
            # 'task': 'tasks.optimize_indexes',
            # 'schedule': crontab(day_of_week='mon-fri', hour=13, minute=21),
            # 'options': {
            #     # ensure we don't accumulate a huge backlog of these if the workers are down
            #     'expires': 60
            # }
        }
    }
    CELERY_TIMEZONE = 'UTC'
    # CELERY_TASK_RESULT_EXPIRES = 3600
    # CELERY_DISABLE_RATE_LIMITS = True
    # CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
    # CELERYD_CONCURRENCY = 16
    # CELERYD_TASK_TIME_LIMIT = 3630

    # cache settings
    CACHE_CONFIG = {'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'model_cache', 'CACHE_REDIS_URL': CACHE_REDIS_URL,
                    'CACHE_DEFAULT_TIMEOUT': 3600,  # 'CACHE_THRESHOLD': 922337203685477580
                    }


class DevelopmentConfig(Config):
    """Use "if app.debug" anywhere in your code, that code will run in development code."""
    TESTING = False
    DEBUG = True

    # MySQL configurations
    # INTERNAL = f'{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://' + INTERNAL + '?charset=utf8'
    # SQLALCHEMY_BINDS = {'readonly': f'mysql+pymysql://' + INTERNAL + '?charset=utf8'}
    # SQLALCHEMY_POOL_RECYCLE = 299
    # SQLALCHEMY_POOL_TIMEOUT = 20

    # Postgres configurations
    POSTGRES_INTERNAL = f'{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_DATABASE_URI = f"postgresql://" + POSTGRES_INTERNAL
    SQLALCHEMY_BINDS = {'readonly': f"postgresql://" + POSTGRES_INTERNAL}

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = True

    # celery configurations
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_DB_NO, REDIS_HOST, REDIS_PORT = 0, "192.168.56.20", 6379

    CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    SESSION_WITH_REDIS = {"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB_NO, "password": REDIS_PASSWORD}

    # used in whoosh file
    CONSOLE_ERROR_LOG = True

    RECAPTCHA_ENABLED = False


class LiveConfig(Config):
    DEBUG = False
    TESTING = False

    # MySQL configurations
    # INTERNAL = f'{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://' + INTERNAL + '?charset=utf8'
    # SQLALCHEMY_BINDS = {'readonly': f'mysql+pymysql://' + INTERNAL + '?charset=utf8'}
    # SQLALCHEMY_POOL_RECYCLE = 299
    # SQLALCHEMY_POOL_TIMEOUT = 20

    # Postgres configurations
    POSTGRES_INTERNAL = f'{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_DATABASE_URI = f"postgresql://" + POSTGRES_INTERNAL
    SQLALCHEMY_BINDS = {'readonly': f"postgresql://" + POSTGRES_INTERNAL}

    # celery configurations
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_DB_NO, REDIS_HOST, REDIS_PORT = 0, "192.168.56.20", 6379

    CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    SESSION_WITH_REDIS = {"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB_NO, "password": REDIS_PASSWORD}

    RECAPTCHA_ENABLED = True


class TestConfig(Config):
    DEBUG = False
    TESTING = True

    POSTGRES_INTERNAL = f'{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_DATABASE_URI = f"postgresql://" + POSTGRES_INTERNAL
    SQLALCHEMY_BINDS = {'readonly': f"postgresql://" + POSTGRES_INTERNAL}

    # celery configurations
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_DB_NO, REDIS_HOST, REDIS_PORT = 0, "192.168.56.20", 6379

    CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NO}'
    SESSION_WITH_REDIS = {"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB_NO, "password": REDIS_PASSWORD}

    RECAPTCHA_ENABLED = False
