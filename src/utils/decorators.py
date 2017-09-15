# -*- coding: utf-8 -*-

import functools
import httplib
import logging
import json
import time
import traceback
from flask import (
    g,
    request,
    make_response,
)

import threading

from src.exc import ServerExceptions

logger = logging.getLogger(__name__)


def print_cost_time(f):
    def decorator(*args, **kwargs):
        t = time.time()
        result = f(*args, **kwargs)
        logging.info('<{}> cost time: {:.2f}ms'.format(f.__name__, (time.time() - t) * 1000))
        return result

    return decorator


def catch_except(func):
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logging.warning(traceback.format_exc())
            return None

    return decorator