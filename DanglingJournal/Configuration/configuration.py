#  Project dangling-journal is developed by "Fahad Ahammed" on 11/12/19, 5:36 PM.
#
#  Last modified at 11/12/19, 5:36 PM.
#
#  Github: fahadahammed
#  Email: obak.krondon@gmail.com
#
#  Copyright (c) 2019. All rights reserved.

import os

if not os.path.exists("Logs"):
    os.mkdir("Logs")

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s at %(threadName)s in %(module)s : %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': 'Logs/logs.log',
            'formatter': 'default'
        }
    },
    'root': {
        'handlers': ['wsgi', 'logfile']
    }
}


class BaseConfig(object):
    APPLICATION_NAME = "DanglingJournal"
    DanglingJournal_VERSION = "1.0.1"

    DEBUG = True
    TESTING = True
    PROTECTED_PATH = "ProtectedPath"
    TEMPLATES_AUTO_RELOAD = True
    THREADED = True
    ACCOUNT_ENDPOINT = "http://127.0.0.1:36302"
    HOST = "0.0.0.0"
    PORT = 11220

    DANGLINGJOURNAL_DB_PORT = 27017
    DANGLINGJOURNAL_DB_HOST = "127.0.0.1"
    DANGLINGJOURNAL_DB_USER = "DanglingJournal"
    DANGLINGJOURNAL_DB_PASSWORD = "DanglingJournal"
    DANGLINGJOURNAL_DB_NAME = "DanglingJournal"


class DevelopmentConfig(BaseConfig):
    ENV = 'dev'
    SECRET_KEY = "m6LbqS5RnPbtOhzBzfsUzfwQsPpOqD59Va6nrZrb"

    CACHE_TYPE = 'simple'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = '11'
    CACHE_KEY_PREFIX = '@DanglingJournal'
    CACHE_DEFAULT_TIMEOUT = 43200


class ProductionConfig(BaseConfig):
    ENV = 'prod'

    TEMPLATES_AUTO_RELOAD = False
    SECRET_KEY = "m6LbqS5RnPbtOhzBzfsUzfwQsPpOqD59Va6nrZrb"

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = '11'
    CACHE_KEY_PREFIX = '@DanglingJournal'
    CACHE_DEFAULT_TIMEOUT = 43200

    DANGLINGJOURNAL_DB_PORT = 3306
    DANGLINGJOURNAL_DB_HOST = "127.0.0.1"
    DANGLINGJOURNAL_DB_USER = "DanglingJournal"
    DANGLINGJOURNAL_DB_PASSWORD = "DanglingJournal"
    DANGLINGJOURNAL_DB_NAME = "DanglingJournal"


config = {
    "dev": "DanglingJournal.Configuration.configuration.DevelopmentConfig",
    "prod": "DanglingJournal.Configuration.configuration.ProductionConfig",
    "default": "DanglingJournal.Configuration.configuration.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('ENV', 'default')
    app.config.from_object(config[config_name])



