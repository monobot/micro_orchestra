import logging
from os import path

from logging.config import dictConfig

LOGLEVEL = 'DEBUG'
FILE_NAME = 'processor.log'
LOG_DIR = path.join(path.curdir(), 'logs')

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '%(asctime)s %(name)s - %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': LOGLEVEL,
            'formatter': 'normal',
            'filename': path.join(LOG_DIR, 'django.log'),
            'maxBytes': 30 * 1024 * 1024,  # 30 megas filesize
            'backupCount': 0,  # allows 1 backup count, total 60 megas
        }
    },
    'loggers': {
        'processor_box': {
            'handlers': ['file_handler', ],
            'propagate': True,
            'level': LOGLEVEL,
        }
    }
}

dictConfig(logging_config)


logger = logging.getLogger('processor_box')
