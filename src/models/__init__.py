#!/usr/bin/env python
# encoding: utf-8

__author__ = 'yudan.chen'

import functools
import logging
import decimal
import datetime
import sys
from gevent import local

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    Session as _Session,
    scoped_session,
    sessionmaker,
)

from src.utils.datetime_util import datetime2epoch
from src.utils import gevent_psycopg2
gevent_psycopg2.monkey_patch()

logger = logging.getLogger(__name__)

db_ctx = local.local()


def gen_commit_deco(DBSession):
    def wrap(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            register_db_commit = getattr(db_ctx, 'register_db_commit', None)
            if not register_db_commit:
                db_ctx.register_db_commit = [DBSession]
            session = DBSession()
            if register_db_commit:
                result = func(*args, **kwargs)
                return result
            try:
                result = func(*args, **kwargs)
                session.flush()
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise e
            finally:
                session.close()
                db_ctx.register_db_commit = None
            return result
        return wrapper
    return wrap


def make_engine(config):
    config.setdefault('scheme', 'postgresql+psycopg2')
    default_url = ("{scheme}://{user}:{password}"
                   "@{host}:{port}/{database}")
    dsn = default_url.format(**config)
    return create_engine(dsn, pool_size=30, max_overflow=10, pool_recycle=1200)


def make_session(engine):
    return scoped_session(
        sessionmaker(
            class_=_Session,
            expire_on_commit=False,
            autoflush=False,
            bind=engine,
        )
    )


from sqlalchemy import (
    Column,
    DateTime,
    func,
    SmallInteger,
)
from sqlalchemy.ext.declarative import declarative_base
from src.config import cfg


engine = make_engine(cfg.DATABASE_CONFIG)
DBSession = make_session(engine)
db_commit = gen_commit_deco(DBSession)
DeclarativeBase = declarative_base()


class TimestampMixin(object):
    create_time = Column(DateTime, default=func.now(), index=True)
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)


class BasicMethodMixin(object):

    status = Column(SmallInteger, default=1)

    def serialize(self, include_columns=None, exclude_columns=None):
        """
        :rtype: dict
        """
        obj_dict = {}

        if include_columns is not None:
            fields = set(include_columns)
        else:
            fields = set(self.__mapper__.columns.keys()) - \
                     set(getattr(self, '__ignore_fields__', []))
        if exclude_columns is not None:
            fields -= set(exclude_columns)

        for field in fields:
            item = getattr(self, field)
            if isinstance(item, decimal.Decimal):
                item = float(item)
            if isinstance(item, datetime.datetime):
                item = datetime2epoch(item)
            if isinstance(item, datetime.time):
                item = int(item.strftime('%H%M%S'))
            obj_dict.update({field: item})

        return obj_dict

    @classmethod
    def serialize_list(cls, objs, include_columns=None, exclude_columns=None):
        rv = []
        if not objs or len(objs) == 0:
            return rv
        for obj in objs:
            if not isinstance(obj, cls):
                logger.info('obj type is wrong:{}'.format(type(obj)))
                continue
            rv.append(obj.serialize(include_columns=include_columns,
                                    exclude_columns=exclude_columns))
        return rv

    @classmethod
    def get(cls, oid):
        return DBSession().query(cls).filter(
            cls.id==oid, cls.status==1).first()

    @classmethod
    def get_no_condition(cls, oid):
        return DBSession().query(cls).filter(cls.id == oid).first()

    @classmethod
    def all(cls):
        return DBSession().query(cls).filter(cls.status==1)

    @classmethod
    def new(cls, **fields):
        obj = cls()
        for key, val in fields.iteritems():
            if hasattr(obj, key):
                setattr(obj, key, val)
        return obj

    @db_commit
    def save(self, cb=None, *args, **kw):
        DBSession().add(self)
        DBSession().flush()
        if cb:
            for _args in args:
                if isinstance(_args, dict) and not _args.get('id'):
                    _args['id'] = self.id
            cb(*args, **kw)
        return self

    @classmethod
    def mget(cls, ids):
        if not ids:
            return []
        return DBSession().query(cls).filter(
            cls.id.in_(ids), cls.status == 1).all()


    def update(self, **kw):
        for key, val in kw.items():
            if hasattr(self, key):
                setattr(self, key, val)

        return self.save()


from .card     import *
from .act import *


