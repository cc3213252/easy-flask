# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'


import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    TEXT,
    Float,
    func,
    desc,
    Boolean,
)
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    JSONB
)

from src.models import (
    DeclarativeBase,
    TimestampMixin,
    DBSession,
    BasicMethodMixin,
)


class Act(DeclarativeBase, TimestampMixin, BasicMethodMixin):

    __tablename__ = 'act'
    __ignore_fields__ = ['update_time', 'create_time', 'status']

    SUB_TYPE_BANK = 1
    SUB_TYPE_CARD_ORG = 2

    id = Column(Integer, primary_key=True)
    mongo_id = Column(String)

    subject_type = Column(Integer)
    title = Column(String, index=True)
    original_title = Column(String, index=True)
    content = Column(String)

    original_url = Column(String)
    small_img_url = Column(String)
    big_img_url = Column(String)

    bank_ids = Column(ARRAY(Integer), index=True)
    pay_org_ids = Column(ARRAY(Integer))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    zone_include = Column(ARRAY(String))
    zone_exclude = Column(ARRAY(String))
    category = Column(ARRAY(Integer))

    display_tags = Column(ARRAY(TEXT))
    pay = Column(Float)
    repay = Column(Float)
    act_yield = Column(Float)

    available_time_ranges = Column(JSONB, default={})
    unavailable_time_ranges = Column(JSONB, default={})
    quota = Column(TEXT)
    usage_scene = Column(ARRAY(Integer))


    @classmethod
    def mget_fields(cls, ids):
        if not ids:
            return []
        return DBSession().query(cls.id, cls.pay, cls.repay, cls.category, cls.usage_scene).filter(
            cls.id.in_(ids), cls.status == 1).all()


    @classmethod
    def mget_online(cls, ids):
        if not ids:
            return []
        return DBSession().query(cls).filter(
            cls.id.in_(ids), cls.status == 1, cls.end_date > datetime.datetime.today().date()).all()


class BaseCode(DeclarativeBase, TimestampMixin, BasicMethodMixin):
    __tablename__ = 'base_code'
    __ignore_fields__ = ['update_time', 'create_time', 'status']

    SCENARIO = 1     # 场景
    DISCOUNT = 2     # 折扣
    SOURCE = 3       # 来源
    BENEFIT = 4      # 权益
    HOT = 5          # 是否是热门活动
    RUSH_BUY = 6     # 是否是抢购活动
    GEO = 7          # 地理信息
    CONFIG = 8       # 配置
    CATEGORY = 9     # 分类
    PAYMENT = 10     # 支付渠道

    id = Column(Integer, primary_key=True)
    mongo_id = Column(String)
    name = Column(String)
    name_en = Column(TEXT)
    level = Column(Integer)
    type = Column(Integer)
    parent_id = Column(Integer)
