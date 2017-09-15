# coding=utf-8
"""

"""
import datetime
import time
import logging
import traceback

from flask import Flask, request, Response, jsonify
from flask import current_app
from flask.json import JSONEncoder
from flask_redis import FlaskRedis
from psycopg2.pool import SimpleConnectionPool
from src.config import cfg


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            if isinstance(obj, datetime.date):
                return obj.strftime("%Y-%m-%d")
            iterable = iter(obj)
        except TypeError:
            logging.error('json化 出错， %s', obj)
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_app():
    """
    创建一个app并且加载配置
    :return:
    """
    application = Flask(__name__)
    # 加载配置文件
    application.config.from_object(cfg)
    FlaskRedis(application)
    application.json_encoder = CustomJSONEncoder
    return application


def make_response(sync_time=None, data=None, http_code=None):
    resp = {
        'status': '200',
        'msg': 'success',
        'data': data if data is not None else {}
    }
    if sync_time:
        resp['sync_time'] = sync_time
    resp = jsonify(resp)
    if http_code:
        resp.status_code = http_code
    else:
        resp.status_code = 200
    return resp


