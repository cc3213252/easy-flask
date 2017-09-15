# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'

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


class TokenHistory(DeclarativeBase, BasicMethodMixin):

    __tablename__ = 'token_history'
    __ignore_fields__ = ['status']

    id = Column(Integer, primary_key=True)
    token = Column(TEXT)
    access_key = Column(TEXT)
    create_time = Column(DateTime, default=func.now())

    @classmethod
    def set_invaild_token(cls, token):
        row = DBSession().query(cls).filter(cls.token == token).first()
        if not row:
            row.status = 0
            row.save()


class AccessKey(DeclarativeBase, BasicMethodMixin):

    __tablename__ = 'access_key'
    __ignore_fields__ = ['status']

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    create_id = Column(Integer)
    access_key = Column(TEXT)
    secret_key = Column(TEXT)
    create_time = Column(DateTime, default=func.now())


class UriAccessRef(DeclarativeBase, BasicMethodMixin):

    __tablename__ = 'uri_access_ref'
    __ignore_fields__ = ['status']

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    create_id = Column(Integer)
    uri_id = Column(Integer)
    create_time = Column(DateTime, default=func.now())


class Uri(DeclarativeBase, BasicMethodMixin):

    __tablename__ = 'uri'
    __ignore_fields__ = ['status']

    id = Column(Integer, primary_key=True)
    uri = Column(TEXT)
    endpoint = Column(TEXT)
    note = Column(TEXT)
    create_id = Column(Integer)
    name = Column(TEXT)
    create_time = Column(DateTime, default=func.now())