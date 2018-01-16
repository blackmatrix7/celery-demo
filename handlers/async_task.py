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

__author__ = 'blackmatrix'


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

if __name__ == '__main__':
    pass
