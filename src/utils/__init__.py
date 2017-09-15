# -*- coding: utf-8 -*-
from __future__ import absolute_import

__author__ = 'yudan.chen'


import httplib
import logging
import uuid
import json
import re
from flask import (
    Response,
    jsonify,
    g
)
from flask_restful import Api as _Api
from werkzeug.exceptions import (
    BadRequest,
    MethodNotAllowed,
)


from src.exc import ServerBaseException
from src.utils.datetime_util import (
    epoch2datetime,
)

_logger = logging.getLogger(__name__)


class Singleton(type):
    '''Usage:
    class Foo(Base):
        __metaclass__ = Singleton
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def make_response(
    data=None, message='success', code=200, status_code=None, description=''):
    if isinstance(data, Response):
        if data.status_code == 302:
            return data

    response_body = {
        'code': code,
        'msg': message,
        'data': data,
        'description': description,
    }
    response = jsonify(response_body)
    response.status_code = status_code or httplib.OK
    return response


class Api(_Api):
    def handle_error(self, e):
        # handle service error here, return 500

        # handle reqparse error
        try:
            if isinstance(e, BadRequest):
                # unwrap flask-restful error message to avoid multi-layer headover
                if hasattr(e, 'data'):
                    if isinstance(e.data, dict):
                        k = e.data.keys()
                        if len(k) == 1 and 'message' in k:
                            e.data = e.data['message']
                    return make_response(message=json.dumps(e.data), code=400, status_code=400)
                else:
                    return make_response(message=str(e), code=400, status_code=400)
            if isinstance(e, MethodNotAllowed):
                return make_response(message=e.description, code=405, status_code=405)
        except Exception:
            uuid_ = uuid.uuid4()
            _logger.error('unknow error(%s)', uuid_, exc_info=True)
            return make_response(message='unknow error(%s)' % uuid_, code=500, status_code=500)

        try:
            if isinstance(e, ServerBaseException):
                if e.output_error_log:
                    uuid_ = uuid.uuid4().hex
                    _logger.error('server exception(%s): %s', uuid_, json.dumps(e.args, ensure_ascii=False),
                                  exc_info=True)
                    return make_response(message=e.name, code=e.code, description=e.description,
                                         data=uuid_,
                                         status_code=e.status_code)
                else:
                    return make_response(message=e.name, code=e.code, description=e.description,
                                         status_code=e.status_code)
        except:
            _logger.error('', exc_info=True)

        # handle all other errors here, treat them as 400 error
        uuid_ = uuid.uuid4()
        _logger.error('unknow error(%s)', uuid_, exc_info=True)
        return make_response(message="unknow error(%s)" % uuid_, code=400, status_code=400)


# filters used in RESTful API argument `type` setting
def argument_filter(conditions, val_type):
    def wrapper(val):
        if val_type(val) in conditions:
            return val_type(val)
        raise ValueError('given value not valid')
    return wrapper


def positive_int_validator(v):
    try:
        iv = int(v)
        if iv < 0:
            raise ValueError
        return iv
    except:
        raise ValueError('ONLY_ACCEPT_POSITIVE_INT_ARGUMENT')


def ts_validator(js_ts):
    try:
        return epoch2datetime(float(js_ts) / 1000)
    except:
        raise ValueError('INVALID_TIMESTAMP')


def int_range_validator(begin, end):
    def func(v):
        try:
            v = int(v)
            assert begin <= v < end
            return v
        except:
            raise ValueError("only accept int with range [{}, {})".format(begin, end))
    return func


def in_list_validator(l, val_type):
    def func(v):
        try:
            v = val_type(v)
            assert v in l
            return v
        except:
            raise ValueError('only accept args in {}'.format(l))
    return func


def list_validator(l, val_type):
    def func(v):
        try:
            assert isinstance(v, list)
            for x in v:
                assert val_type(x) in l
            return [val_type(x) for x in v]
        except:
            raise ValueError('only accept args in {}'.format(l))
    return func


def str_with_length_limit(_min, _max):
    def func(v):
        try:
            v = str(v)
            assert _min <= len(v) <= _max
            return v
        except:
            raise ValueError("only accept str length {} to {}".format(_min, _max))
    return func


def unicode_with_length_limit(min_, max_):
    def func(v):
        try:
            v = unicode(v)
            assert min_ <= len(v) < max_
            return v
        except:
            raise ValueError("only accept unicode length in [{}, {})".format(min_, max_))
    return func


def filter_dict_none_value(d):
    if not isinstance(d, dict):
        return False
    return {k: v for k, v in d.iteritems() if v is not None}


def sort_by_id_list(obj_dict_list, id_list):
    id_map = {}
    for obj_dict in obj_dict_list:
        id_map[obj_dict['id']] = obj_dict
    rv = []
    for id_ in id_list:
        if id_ in id_map:
            rv.append(id_map[id_])
    return rv


