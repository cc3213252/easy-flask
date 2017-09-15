# coding=utf-8

__author__ = 'yudan.chen'


from . import (
    act,
    card,
)


def init_app(g_app):
    apps = [
        act,
        card,
    ]
    for app in apps:
        app.init_app(g_app)
