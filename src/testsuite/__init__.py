# coding=utf-8

"""
写一些测试用例
"""
import hashlib
import json
import unittest
import datetime
import time

import requests


class ApiTestCase(unittest.TestCase):
    """
    测试的基础类,自动完成认证等功能
    """

    def __init__(self, *args, **kwargs):
        super(ApiTestCase, self).__init__(*args, **kwargs)
        self.headers = {'Content-Type': 'application/json', }
        self.data = None
        self.uri = ''
        self.host = 'http://127.0.0.1:7690'
        self.mode = 'testing'
        if self.mode == 'prod':
            self.first_code = '43157800'
            self.card_id = '3239'
        else:
            self.first_code = '43157800'
            self.card_id = '3239'


    def args(self):
        if self.mode == 'testing':
            return 'ock3svreqelk3uqfu51a48fnsz8jlwv1', 'onqstlf2p8sglb8mnpbuu6cek5nrhhet', \
                   'http://openapi-test.billbear.cn/asset'
        elif self.mode == 'prod':
            return 'ta3gzb9lovq424zrgzkl0o13jqc4f7yd', 'wud1sfd3mrdmygs1z5l8bk4glo9v9qlz', \
                   'https://openapi.billbear.cn/asset'
        return 'ock3svreqelk3uqfu51a48fnsz8jlwv1', 'onqstlf2p8sglb8mnpbuu6cek5nrhhet', \
               'http://127.0.0.1:7690'        #随手记公司

    def fetch(self, uri, headers=None, data=None, method="GET", host=None, mode=''):
        if headers:
            self.headers.update(headers)
        if mode:
            self.mode = mode
        self.access_key, self.secret_key, self.host = self.args()
        self.uri = uri
        if data:
            self.data = data
        if host:
            self.host = host
        self.method = method.upper()
        self.data['sign'] = self.sign()
        url = '{}{}'.format(self.host, uri)
        if method.upper() == 'GET':
            url += '?' + '&'.join(['{}={}'.format(k, v, k, v) for k, v in data.items()])
        print(url)
        return requests.request(self.method, url,
                                headers=self.headers, data=json.dumps(data))

    def sign(self):
        params = self.data
        string_a = '&'.join(
            ['{}:{}'.format(k, params[k]) for k in sorted(params.keys()) if params[k] and k != 'sign'])
        string_sign_temp = "{}&secret_key={}".format(string_a, self.secret_key)
        hlb = hashlib.md5()
        hlb.update(string_sign_temp.encode('utf-8'))
        md5 = hlb.hexdigest().upper()
        return md5

    def get_token(self):
        self.access_key, self.secret_key, self.host = self.args()
        self.data = {'access_key': self.access_key, 'time': int(time.time()), }
        resp = self.fetch('/core/v1/token', data=self.data, method='post')
        resp_obj = json.loads(resp.text)
        print(resp_obj)
