# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    TEXT,
    Numeric,
    Boolean,
    desc,
    Float
)

from sqlalchemy.dialects.postgresql import (
    JSONB,
    ARRAY,
)

from src.models import (
    DeclarativeBase,
    TimestampMixin,
    DBSession,
    BasicMethodMixin,
)


class Card(DeclarativeBase, TimestampMixin, BasicMethodMixin):
    __tablename__ = 'card'

    __ignore_fields__ = ['update_time', 'create_time', 'status']

    id = Column(Integer, primary_key=True, index=True)
    mongo_id = Column(String, index=True)
    bank_id = Column(Integer)
    pay_org_ids = Column(ARRAY(Integer))
    bin_code = Column(ARRAY(TEXT), index=True, default=[])
    name = Column(String(50), index=True)
    img_url = Column(String)

    annual_fee = Column(Numeric(10, 2), default=0.0)
    annual_fee_free = Column(Integer)
    annual_fee_rule = Column(String)
    annual_fee_currency = Column(JSONB, default=[])

    point_rule = Column(JSONB, default=[])
    point_validity_description = Column(String)
    tags = Column(JSONB, default=[])
    is_hot = Column(Boolean, default=False)
    min_repayment_description = Column(TEXT)
    interest_free_period = Column(TEXT)
    hotlines = Column(JSONB, default=[])


class ActCardRef(DeclarativeBase, TimestampMixin, BasicMethodMixin):
    __tablename__ = 'act_card_ref'

    __ignore_fields__ = ['update_time', 'create_time', 'status']

    id = Column(Integer, primary_key=True, index=True)
    act_id = Column(Integer)
    card_id = Column(Integer)


class CardBenefit(DeclarativeBase, TimestampMixin, BasicMethodMixin):
    __tablename__ = 'card_benefit'

    __ignore_fields__ = ['update_time', 'create_time', 'status']

    PERIOD_TYPE_NONE = 0
    PERIOD_TYPE_YEAR = 1
    PERIOD_TYPE_SEASON = 2
    PERIOD_TYPE_MONTH = 3

    id = Column(Integer, primary_key=True, index=True)
    mongo_id = Column(String)
    title = Column(String)
    content = Column(TEXT)
    original_url = Column(TEXT)
    subject_type = Column(Integer)
    bank_id = Column(Integer)
    card_org_id = Column(Integer)
    tags = Column(JSONB, default=[])
    usage_count = Column(Integer)
    pay = Column(TEXT)
    repay = Column(TEXT)
    period_type = Column(Integer)


    @classmethod
    def mget_fields(cls, ids):
        if not ids:
            return []
        return DBSession().query(cls.id, cls.repay).filter(
            cls.id.in_(ids), cls.status == 1).all()


class CardBenefitRef(DeclarativeBase, TimestampMixin, BasicMethodMixin):
    __tablename__ = 'card_benefit_ref'

    __ignore_fields__ = ['update_time', 'create_time', 'status']

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer)
    benefit_id = Column(Integer)


class BenefitRecord(DeclarativeBase, BasicMethodMixin):
    __tablename__ = 'benefit_record'

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer)
    card_id = Column(Integer)
    benefit_id = Column(Integer)
    count = Column(Integer)
    direction = Column(Integer)
    create_time = Column(DateTime, default=func.now())