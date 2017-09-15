# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'

import datetime
from flask import current_app, request, Response, g
from src.models import (
    DBSession,
)
from src.models.authority import TokenHistory, AccessKey, Uri, UriAccessRef
from src.utils.rds import get_rds, set_rds_ex
from src.utils.flk import make_response
from src.exc import ServerExceptions
import traceback
import time
import logging
logger = logging.getLogger(__name__)


def check_access_key(token, endpoint):
    config = current_app.config
    # 判断access_key是否有效, 如果redis里面有这个company id，就表示公司存在，如果没有就去数据库查找
    company_key = 'company:{}'.format(token)
    company_id = get_rds(company_key)
    if not company_id:
        companys = DBSession().query(AccessKey.company_id, TokenHistory.create_time)\
            .filter(TokenHistory.token == token, TokenHistory.status == 1,
                    AccessKey.access_key == TokenHistory.access_key, AccessKey.status == 1).first()
        if not companys:
            logger.error('没有找到用户账号, token:{}, company_id:{}'.format(token, company_id))
            raise ServerExceptions.TOKEN_ERROR
        company_id, token_create_time = companys
        # 判断token有没有过期
        t = token_create_time + datetime.timedelta(seconds=config['TOKEN_MAX_EFFECTIVE_SEC']) - datetime.datetime.now()
        if t <= datetime.timedelta(seconds=0):
            TokenHistory.set_invaild_token(token)
            raise ServerExceptions.TOKEN_ERROR
        set_rds_ex(company_key, company_id, t.seconds)

    print token, endpoint, company_id
    # 判断访问接口的权限
    access_right = get_rds('access_right:{}:{}'.format(token, endpoint))
    if not access_right:
        ref = DBSession().query(Uri).filter(Uri.endpoint == endpoint, UriAccessRef.company_id == company_id,
                                         Uri.id == UriAccessRef.uri_id, Uri.status == 1, UriAccessRef.status == 1).first()
        if not ref:
            logger.error('没有访问权限, token:{}, company_id:{}'.format(token, company_id))
            raise ServerExceptions.ACCESS_RIGHT_ERROR
        set_rds_ex('access_right:{}:{}'.format(token, endpoint), 1, config['RDS_TIME'])

    return company_id


def access_required(func):
    def wrapper(*args, **kwargs):
        t = time.time()
        token = g.token
        random_str = g.random_str
        if not random_str or not isinstance(random_str, str):
            raise ServerExceptions.RANDOM_STR_ERROR

        company_id = check_access_key(token, request.endpoint)
        g.company_id = company_id
        try:
            result = func(*args, **kwargs)
        except BaseException:
            logging.error(traceback.format_exc())
            raise ServerExceptions.UNKNOWN_ERROR

        # 记录处理结果
        logging.info('[company_id]:%s, [random_str]: %s, [endpoint]:%s, [cost time]:%s ms, [result]:%s ',
                     company_id, random_str, request.endpoint, (time.time()-t)*1000,  result)
        return make_response(data=result)

    return wrapper

