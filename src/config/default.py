# -*- coding: utf-8 -*-
"""
通用的配置文件
"""


class BaseConfig(object):
    """

    """
    APP_LISTEN_PORT = 7690
    HEADER_CONTENT_TYPE = 'application/json'
    JSONIFY_PRETTYPRINT_REGULAR = None

    # redis 有效时间
    RDS_TIME = 600
    # pg 扩展名称
    EXT_PG = 'postgres'

    # 请求最大时间(单位是微秒)
    REQ_TIME = 30000000

    # 默认一次返回的数据量
    COUNT = 100

    # https 地址
    IMAGE_HTTPS_HOST_NAME = 'qnpic.billbear.cn'

    # token 最大有效期
    TOKEN_MAX_EFFECTIVE_SEC = 86400
    # token每小时最大请求次数
    TOKEN_MAX_REQ_TIMES = 100

    # 延迟，
    DELAY_MIN = 5
