#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/1/16 下午3:58
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py.py
# @Software: PyCharm
from kombu import Queue
from datetime import timedelta
from toolkit.config import BaseConfig, get_current_config

__author__ = 'blackmatrix'


# 读取配置文件的名称，在具体的应用中，可以从环境变量、命令行参数等位置获取配置文件名称
config_name = 'default'
current_config = get_current_config(config_name)


class CommonConfig(BaseConfig):

    # Celery
    CELERY_BROKER_URL = 'amqp://user:password@127.0.0.1:5672//'
    CELERY_RESULT_BACKEND = 'amqp://user:password@127.0.0.1:5672//'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'pickle'
    CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    # 导入Task所在的模块
    CELERY_IMPORTS = ('handlers.async_task', 'handlers.schedules')
    # celery worker 的并发数
    CELERYD_CONCURRENCY = 3
    # 为Task指定不同的队列
    CELERY_QUEUES = (
        Queue('send_mail', routing_key='vcan.send_mail'),
        Queue('vcan_health_schedules', routing_key='vcan.health.schedules'),
    )
    CELERY_ROUTES = {
        'toolkit.vmail.async_send_mail': {
            'queue': 'send_mail',
            'routing_key': 'vcan.send_mail',
        },
        'apps.marketing.marketing.schedules.async_push_ext_contacts': {
            'queue': 'vcan_health_schedules',
            'routing_key': 'vcan.health.schedules',
        }
    }
    # Celery 时区，定时任务需要
    CELERY_TIMEZONE = 'Asia/Shanghai'
    # 定时任务 schedules
    CELERYBEAT_SCHEDULE = {
        'every-one-hour': {
             'task': 'apps.marketing.marketing.schedules.async_push_ext_contacts',
             # 每 30 秒执行一次
             'schedule': timedelta(seconds=3600),
             # 任务函数参数
             'args': None
        }
    }


class DefaultConfig(CommonConfig):
    pass

defcfg = DefaultConfig()

configs = {
    'default': defcfg
}
