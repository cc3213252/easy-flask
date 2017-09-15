# -*- coding: utf-8 -*-
"""
redis数据库相关的公共类
"""
import logging

from flask import current_app


def set_rds_ex(key, value, time=86400):
    """
    设置redis,
    注意处理公共前缀cfg.RDS_KEY
    :param key:
    :param value:
    :param time: 默认有效期是一天，当time小于等于0的时候，表示不设置有效期
    :return:
    """
    rds = current_app.extensions['redis']
    key = '{}:{}'.format(current_app.config['RDS_KEY'], key)
 #   logging.info('set redis key: %s, value: %s, time:%s', key, value, time)
    if time <= 0:
        rds.set(name=key, value=str(value))
    else:
        rds.setex(name=key, value=str(value), time=time)


def get_rds(key):
    """
    查询redis
    :param key:
    :return:
    """
    rds = current_app.extensions['redis']
    key = '{}:{}'.format(current_app.config['RDS_KEY'], key)
    v = rds.get(key)
    if v and isinstance(v, bytes):
        v = v.decode()
    return v


def ttl(key):
    """
    key的剩余有效时间
    :param key:
    :return:
    """
    rds = current_app.extensions['redis']
    return rds.ttl('{}:{}'.format(current_app.config['RDS_KEY'], key))
