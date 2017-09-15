#!/usr/bin/env python
# coding=utf-8

__author__ = 'yudan.chen'

import logging.config


def init_logging():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'generic': {
                'format': '%(asctime)s [%(process)d] [%(levelname)s] %(name)s: %(message)s',  # noqa
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'generic',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    })


def debug_init():
    logger = logging.getLogger('durandal')
    logger.setLevel(logging.DEBUG)
    s = logging.StreamHandler()
    fmt = logging.Formatter('%(asctime)s [%(process)d] [%(levelname)s] [%(filename)s:%(lineno)s] %(name)s: %(message)s')
    s.setFormatter(fmt)
    logger.addHandler(s)
