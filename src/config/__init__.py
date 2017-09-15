# -*- coding: utf-8 -*-

import logging
import os
import traceback

logging.basicConfig(format='[%(asctime)s %(process)d %(filename)s:%(lineno)d %(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def load_config():
    """加载配置类"""
    mode = os.environ.get('MODE')
    logging.info('start load_config, mode=%s', mode)
    try:
        if mode == 'PRODUCTION':
            from src.config.production import ProductionConfig as cfg
        elif mode == 'TESTING':
            from src.config.testing import TestingConfig as cfg
        elif mode == 'LOCAL_PRD':
            from src.config.local import LocalProductConfig as cfg
        else:
            from src.config.local import LocalConfig as cfg
    except ImportError:
        traceback.print_exc()
        raise
    return cfg


cfg = load_config()

__all__ = ['cfg']
