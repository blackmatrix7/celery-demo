#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/1/16 下午3:58
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : manager.py.py
# @Software: PyCharm
import os
import logging.config
from celery import Celery
from config import current_config
from toolkit.cmdline import cmdline

__author__ = 'blackmatrix'


# 为了使用方便，在这里引入了之前写的config模块（支持本地配置不提交到github）
# 本身是非必须的，用dict存储celery配置一样可以
# 所以在这里以注释的形式，增加一个不适用config模块的实现

# 等价于直接定义一个broker，如
# broker = 'amqp://user:password@127.0.0.1:5672//'
broker = current_config.CELERY_BROKER_URL
# 将config模块的配置转换成dict，等价于直接通过dict定义一组celery配置
celery_conf = {k: v for k, v in current_config.items()}

# 创建celery实例
celery = Celery('demo',  broker=broker)
# 如果使用config模块，可以：
# celery.config_from_object('config.current_config')
# 使用dict的情况下，直接把dict作为参数传递给config_from_object
celery.config_from_object(celery_conf)

# 日志
logging.config.fileConfig(os.path.abspath('logging.cfg'), disable_existing_loggers=False)
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
    当然还有输出日志文件的区别
    :return:
    """
    celery.start(argv=['celery', 'worker', '-Q', 'schedules_queue', '-l', 'info', '-f', 'logs/schedules.log'])


def send_email():
    """
    发送邮件worker
    与runcelery的唯一区别是增加了-Q的参数，用于指定队列名称
    当然还有输出日志文件的区别
    :return:
    """
    celery.start(argv=['celery', 'worker', '-Q', 'email_queue', '-l', 'info', '-f', 'logs/email.log'])


def push_message():
    """
    推送消息worker
    与runcelery的唯一区别是增加了-Q的参数，用于指定队列名称
    当然还有输出日志文件的区别
    :return:
    """
    celery.start(argv=['celery', 'worker', '-Q', 'message_queue', '-l', 'info', '-f', 'logs/message.log'])


if __name__ == '__main__':

    cmds = {
        # 启动celery
        'runcelery': runcelery,
        # 根据task启动不同的worker
        'schedules': schedules,
        'push_message': push_message,
        'send_email': send_email,
        # 启动celery beat
        'runbeat': runbeat,
    }.get(cmdline.command, 'runcelery')()
