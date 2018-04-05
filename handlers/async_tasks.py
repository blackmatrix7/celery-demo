#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/1/16 下午4:12
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : async_task.py
# @Software: PyCharm
import logging
from time import sleep
from manage import celery

__author__ = 'blackmatrix'


@celery.task
def async_send_email(send_from, send_to, subject, content):
    """
    模拟异步发送邮件的操作
    :param send_from:
    :param send_to:
    :param subject:
    :param content:
    :return:
    """
    logging.info('模拟异步发送邮件的操作')
    logging.info(send_from, send_to, subject, content)
    # 休眠
    sleep(5)


@celery.task
def async_push_message(send_to, content):
    """
    模拟异步推送消息
    :param send_to:
    :param content:
    :return:
    """
    logging.info('模拟异步推送消息')
    logging.info('send_to: {}'.format(send_to))
    logging.info('content: {}'.format(content))
    # 休眠
    sleep(10)


if __name__ == '__main__':
    pass
