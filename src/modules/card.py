# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'

import time
import datetime
from flask import g
from src.exc import ServerExceptions
from src.models import (
    DBSession,
    Act,
    Card,
    ActCardRef,
    CardBenefit,
    CardBenefitRef,
    BenefitRecord,
)
from sqlalchemy import func
import logging
logger = logging.getLogger(__name__)


def verify_and_get(first_code, last_code, card_id):
    if not first_code or len(first_code) != 8 or not first_code.isdigit() or \
            not last_code or len(last_code) != 4 or not last_code.isdigit() or not card_id:
        raise ServerExceptions.FORMAT_ERROR

    card_info = Card.get(card_id)
    if not card_info:
        raise ServerExceptions.DATA_NOT_FOUND

    if not [bc for bc in card_info.bin_code if bc.startswith(first_code[:6])]:
        raise ServerExceptions.DATA_NOT_FOUND

    return card_info


def get_card_values(first_code, last_code, card_id):
    """
    银行卡：获取卡片年度权益价值和消费收益价值
    :param random_str: 8位随机字符串
    :param token:
    :param first_code:
    :param last_code:
    :param card_id:
    :return: 卡片年度权益价值和消费收益价值
    """
    if not first_code or len(first_code) != 8 or not first_code.isdigit() or \
            not last_code or len(last_code) != 4 or not last_code.isdigit() or not card_id:
        raise ServerExceptions.FORMAT_ERROR

    end_date = time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time()))

    # TODO ORM化
    sql = 'select id, bin_code, (select sum(repay) from act  where status=1 and end_date > \'{}\' and ' \
          'id in (select act_id from act_card_ref where card_id={})) from card where id={};'.format(
           end_date, card_id, card_id)
    card_info = DBSession().execute(sql).fetchone()
    card_id, bin_code, cost_value = card_info

    # 判断bin 的前6位是不是一样的
    if not [bc for bc in bin_code if bc.startswith(first_code[:6])]:
        raise ServerExceptions.DATA_NOT_FOUND

    benefits = DBSession().query(CardBenefit.id, CardBenefit.pay, CardBenefit.repay, CardBenefit.usage_count, CardBenefit.period_type).filter(
        CardBenefitRef.benefit_id == CardBenefit.id, CardBenefitRef.card_id == card_id,
        CardBenefitRef.status == 1, CardBenefit.status == 1).all()

    benefit_keys = ("id", "pay", "repay", "usage_count", "period_type")
    benefit_data = [dict(zip(benefit_keys, cf)) for cf in benefits]
    year_benefit = 0.0
    for benefit in benefit_data:
        if benefit.get('period_type') == CardBenefit.PERIOD_TYPE_SEASON and benefit['usage_count']:
            benefit['usage_count'] *= 4
        elif benefit.get('period_type') == CardBenefit.PERIOD_TYPE_MONTH and benefit['usage_count']:
            benefit['usage_count'] *= 12
        if benefit['repay'] and float(benefit['repay']) and benefit['usage_count'] and int(benefit['usage_count']):
            year_benefit += float(benefit['repay']) * benefit['usage_count']

    return {
        'year_benefit': year_benefit,
        'cost_value': cost_value,
        'currency': u'人民币',
    }


def get_card_benefits(first_code, last_code, card_id):
    verify_and_get(first_code, last_code, card_id)
    benefits = DBSession().query(CardBenefit.id, CardBenefit.pay, CardBenefit.repay).filter(
        CardBenefitRef.card_id == card_id, CardBenefitRef.status == 1, CardBenefitRef.benefit_id == CardBenefit.id,
        CardBenefit.status == 1).all()

    benefit_keys = ("id", "pay", "repay")
    benefit_data = [dict(zip(benefit_keys, cf)) for cf in benefits]
    for benefit in benefit_data:
        benefit.update({'pay_currency': u'人民币' if benefit.get('pay') else None, 'repay_currency': u'人民币' if benefit.get('repay') else None})
    card_info = {
        'card_benefit': benefit_data,
    }
    return card_info


def get_card_benefits_graphics(first_code, last_code, card_id, category_style):
    if not category_style in (1, 2):
        raise ServerExceptions.FORMAT_ERROR

    verify_and_get(first_code, last_code, card_id)
    benefits = DBSession().query(CardBenefit.id, CardBenefit.pay, CardBenefit.repay, CardBenefit.tags).filter(
        CardBenefitRef.card_id == card_id, CardBenefitRef.status == 1, CardBenefitRef.benefit_id == CardBenefit.id,
        CardBenefit.status == 1).all()

    benefit_keys = ("id", "pay", "repay", "tags")
    benefit_data = [dict(zip(benefit_keys, cf)) for cf in benefits]
    all_repay = 0
    benefit_dict = {}

    for benefit in benefit_data:
        tag_list = benefit['tags']
        new_category = None
        if len(tag_list) > 1:
            if category_style == 1:
                new_category = tag_list[0]['name']
            elif category_style == 2:
                new_category = u'综合'
        else:
            new_category = tag_list[0]['name'] if len(tag_list) == 1 else u'其他'

        repay = float(benefit['repay']) if benefit['repay'] else 0.0
        all_repay += repay
        if benefit_dict.get(new_category, None):
            benefit_dict[new_category] += repay
        else:
            benefit_dict[new_category] = repay

    result = []
    for (key, val) in benefit_dict.items():
        result.append({
            'category': key,
            'rate': float(val / all_repay),
        })
    return result


def get_card_benefit(benefit):
    benefits = CardBenefit.mget_fields([row['id'] for row in benefit])
    keys = ("id", "repay")
    benefit_info = [dict(zip(keys, cf)) for cf in benefits]

    def get_count(id):
        for b in benefit:
            if b.get('id') == id and b.get('count'):
                return float(b.get('count'))
        return 0

    year_repay = 0.0
    for row in benefit_info:
        id = row['id']
        if row['repay']:
            year_repay += get_count(id)*float(row['repay'])

    return {
        'year_benefit': year_repay,
        'currency': u'人民币',
    }


def update_card_benefit(card_id, benefit_id, direction, count, year_benefit):
    benefit = CardBenefit.get(benefit_id)
    if not benefit:
        raise ServerExceptions.DATA_NOT_FOUND
    repay = float(benefit.repay) or 0.0
    if direction == 1:
        count -= 1
        year_benefit -= repay
    elif direction == -1:
        count += 1
        year_benefit += repay

    kw = {
        'company_id': g.company_id,
        'card_id': card_id,
        'benefit_id': benefit_id,
        'count': count,
        'direction': direction,
    }
    record = BenefitRecord.new(**kw)
    record.save()

    return {
        'year_benefit': year_benefit,
        'count': count,
        'benefit_id': benefit_id,
        'currency': u'人民币'
    }