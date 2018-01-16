#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/1/16 下午3:58
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : manager.py.py
# @Software: PyCharm
import logging.config
from celery import Celery
from config import current_config
from toolkit.cmdline import cmdline

__author__ = 'blackmatrix'

# 实例化一个celery对象
celery = Celery('apizen',  broker=current_config.CELERY_BROKER_URL)
celery.config_from_object('config.current_config')

# 日志
logging.config.fileConfig('logging.cfg', disable_existing_loggers=False)
logger = logging.getLogger('root')


def runcelery():
    """
    启动celery
    :return:
    """
    celery.start(argv=['celery', 'worker', '-l', 'info', '-f', 'logs/celery.log'])


def runbeat():
    """
    启动celery
    :return:
    """
    celery.start(argv=['celery', 'beat', '-l', 'info', '-f', 'logs/beat.log'])


def schedules():
    """
    与runcelery的唯一区别是增加了-Q的参数，用于指定队列名称
    :return:
    """
    celery.start(argv=['celery', 'worker', '-Q', 'schedules', '-l', 'info', '-f', 'logs/schedules.log'])


if __name__ == '__main__':

    logger.info('config name: {}'.format(cmdline.config))

    cmds = {
        # 启动celery
        'runcelery': runcelery,
        # 根据task启动不同的worker
        'schedules': schedules,
        # 启动celery beat
        'runbeat': runbeat,
    }.get(cmdline.command, 'runcelery')()
