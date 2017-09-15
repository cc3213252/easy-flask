# coding=utf-8
from __future__ import absolute_import

__author__ = 'yudan.chen'


from flask import (
    g,
    request,
)
from flask_cors import CORS
from src.utils.flk import create_app

app = create_app()
CORS(app, supports_credentials=True)
import logging
logger = logging.getLogger(__name__)


def temp():
    from .api import init_app
    from .utils.logger import init_logging
    init_app(app)
    init_logging()

temp()


@app.before_request
def before_request_hook():
    # ignore preflight request
    if request.method == 'OPTIONS':
        return

    if request.method == 'GET':
        data = {k: request.args.get(k, '', type=str) for k in request.args.keys()}
    else:
        data = request.json

    logger.info('[data]:%s', data)
    g.token = data.get('token', '')
    g.random_str = str(data.get('random_str', ''))


@app.after_request
def after_request_hook(resp):
    from .models import DBSession
    DBSession.remove()
    if request.method == 'OPTIONS':
        return resp

    return resp