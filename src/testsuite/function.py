# coding=utf-8
import datetime
import json

import requests
import unittest
from src.testsuite import ApiTestCase
import time
import base64

class TestConfig(object):
    random_str = "c6b306cf"
    sync_time = 1482761570000000
    token = 'VXCugLhhnIB1kzsZiyxfTj341eBxl2bixqVx1sMircD9Ozdh7hWSdHariqiwwKYn'


class CheckTestCase(ApiTestCase):

    # 活动
    def test_acts_values(self):
        data = {
            "random_str": TestConfig.random_str,
            "token": TestConfig.token,
            "act_ids": [38862, 42921, 42919, 42774, 42896, 42906, 42932, 42913, 42893, 42903, 42930, 42912, 38869, 38869, 38868, 38868, 38867, 38866, 38864, 38860, 49763, 37518, 37518],
        }
        resp = self.fetch('/acts', data=data, method='POST')
        resp_obj = json.loads(resp.text)
        datas = resp_obj['data']
        print(datas)
        pay_sum, repay_sum = 0.0, 0.0
        for data in datas:
            print(data)
            if data['pay']:
                pay_sum += float(data['pay'])
            if data['repay']:
                repay_sum += float(data['repay'])
        print('pay_sum:', pay_sum)
        print('repay_sum:', repay_sum)
     #   print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        if resp_obj['code'] == '4000102':
            self.get_token()

        assert resp.status_code == 200


    # 银行卡
    # 测试环境  first_code: "62292266", card_id: "2286"
    # 生产环境  first_code: "62257600", card_id: "2920"
    def test_card_values(self):
        data = {
            "random_str": TestConfig.random_str,
            "token": TestConfig.token,
            "first_code": self.first_code,
            "last_code": "1234",
            "card_id": self.card_id,
        }
        resp = self.fetch('/card', data=data, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        if resp_obj['code'] == '4000102':
            self.get_token()

        assert resp.status_code == 200


    # 非刷卡权益
    def test_card_benefits(self):
        data = {
            "random_str": TestConfig.random_str,
            "token": TestConfig.token,
            "first_code": self.first_code,
            "last_code": "1234",
            "card_id": self.card_id,
        }
        resp = self.fetch('/card/benefits', data=data, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        if resp_obj['code'] == '4000102':
            self.get_token()

        assert resp.status_code == 200


    # 非刷卡权益图形化
    def test_asset_benefit_graphics(self):
        data = {
            "random_str": TestConfig.random_str,
            "token": TestConfig.token,
            "first_code": self.first_code,
            "last_code": "1234",
            "card_id": self.card_id,
            "category_style": 1
        }
        resp = self.fetch('/card/benefits/graphics', data=data, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        if resp_obj['code'] == '4000102':
            self.get_token()

        assert resp.status_code == 200


    # 优惠活动图形化
    def test_asset_act_graphics(self):
        data = {
            "random_str": TestConfig.random_str,
            "token": TestConfig.token,
            "act_ids": [38434, 37046, 38340, 13064],
            "category_style": 2
        }
        resp = self.fetch('/acts/graphics', data=data, method='POST')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        if resp_obj['code'] == '4000102':
            self.get_token()

        assert resp.status_code == 200


    # 权益记录-权益查询
    def test_benefit_query(self):
        data = {
            "random_str": TestConfig.random_str,
            "benefit": [{"id":400, "count":4}, {"id":399, "count":5}, {"id":401, "count":2}],
            "token": TestConfig.token
        }
        resp = self.fetch('/card/benefit', data=data, method='POST')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        if resp_obj['code'] == '4000102':
            self.get_token()

        assert resp.status_code == 200


    # 权益记录-修改记录
    def test_benefit_update(self):
        data = {
            "random_str": TestConfig.random_str,
            "card_id": 1791,
            "benefit_id": 1522,
            "direction": 1,
            "count": 3,
            "year_benefit": 400,
            "token": TestConfig.token
        }
        resp = self.fetch('/card/benefit', data=data, method='PATCH')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        if resp_obj['code'] == '4000102':
            self.get_token()

        assert resp.status_code == 200


if __name__ == '__main__':
    unittest.main()