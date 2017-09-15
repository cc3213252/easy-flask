# -*- coding: utf-8 -*-
"""
正式服务器的配置文件
"""

from src.config.default import BaseConfig


class ProductionConfig(BaseConfig):
    """

    """
    # debug开关
    DEBUG = False

    MODE = 'PRODUCTION'
    # 日志级别
    LOG_LEVEL = 10

    # 网络请求最大重试次数
    MAX_RETRY_NUM = 3

    DATABASE_CONFIG = {
        'database': 'data',
        'host': 'rm-2ze0t33k414784n8e.pg.rds.aliyuncs.com',
        'port': 3433,
        'user': 'tob_pg_pro',
        'password': 'QX3cF4nwf6H',
    }

    # redis 配置
    REDIS_URL = "redis://:5fd1081cec114831:Buerjia5023@5fd1081cec114831.m.cnbja.kvstore.aliyuncs.com:6379/6"

    RDS_KEY = 'easy:production'

    MONGO_URL = 'mongodb://pro:mydwtBxJ0F4=@dds-2ze976ed2b9e1d342.mongodb.rds.aliyuncs.com:3717,' \
                'dds-2ze976ed2b9e1d341.mongodb.rds.aliyuncs.com:3717/tob_pro?replicaSet=mgset-1184787'
