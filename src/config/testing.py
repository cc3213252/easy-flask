# -*- coding: utf-8 -*-
"""
测试的配置文件
"""

from src.config.default import BaseConfig


class TestingConfig(BaseConfig):
    """
    测试环境配置
    """
    DEBUG = True

    MODE = 'TESTING'
    # 日志级别
    LOG_LEVEL = 10

    # 网络请求最大重试次数
    MAX_RETRY_NUM = 3

    DATABASE_CONFIG = {
        'database': 'easy_db',
        'host': 'localhost',
        'port': 5432,
        'user': 'yudan',
        'password': 'yudan',
    }

    # redis 配置
    REDIS_URL = "redis://127.0.0.1:6379/0"

    RDS_KEY = 'easy:testing'


