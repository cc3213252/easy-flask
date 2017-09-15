# -*- coding: utf-8 -*-
"""
开发本地的配置文件
注意这里的地址需要使用外网地址,不能使用服务器内网地址
"""

from src.config.default import BaseConfig


class LocalConfig(BaseConfig):
    """

    """
    MODE = 'local'
    # debug开关
    DEBUG = True

    # 日志级别
    LOG_LEVEL = 10

    # 网络请求最大重试次数
    MAX_RETRY_NUM = 3

    DATABASE_CONFIG = {
        'database': 'bear_db',
        'host': 'localhost',
        'port': 10001,
        'user': 'yudan',
        'password': 'yudan',
    }

    # redis 配置
    REDIS_URL = "redis://127.0.0.1:10002/0"

    RDS_KEY = 'garen:local'

    MONGO_URL = 'mongodb://127.0.0.1:10003/tob_pro'


class LocalProductConfig(BaseConfig):
    """

    """
    MODE = 'local_prd'
    # debug开关
    DEBUG = True

    # 日志级别
    LOG_LEVEL = 10

    # 网络请求最大重试次数
    MAX_RETRY_NUM = 3

    DATABASE_CONFIG = {
        'database': 'data',
        'host': 'localhost',
        'port': 10010,
        'user': 'tob_pg_pro',
        'password': 'QX3cF4nwf6H',
    }

    # redis 配置
    REDIS_URL = "redis://127.0.0.1:10020/6"

    RDS_KEY = 'garen:production'

    MONGO_URL = 'mongodb://127.0.0.1:10003/tob_pro'