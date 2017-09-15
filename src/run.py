#!/usr/bin/env python
# coding=utf-8

__author__ = 'yudan.chen'

from src import app
from src.utils.logger import debug_init
from src.config import cfg


if __name__ == '__main__':
    debug_init()
    app.run(host='0.0.0.0', port=cfg.APP_LISTEN_PORT)
