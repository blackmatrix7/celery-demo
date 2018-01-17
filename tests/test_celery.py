#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/1/16 下午4:50
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : test_celery.py
# @Software: PyCharm
from unittest import TestCase

__author__ = 'blackmatrix'


class CeleryTestCase(TestCase):

    @staticmethod
    def test_push_message():
        """
        直接调用推送消息的task，task同步执行
        从tests/logs/manage.log来看，任务一次执行，第一次执行后休眠10秒执行下一个任务
        2018/01/17 14:37:03 - root - INFO - 模拟异步推送消息 - [async_tasks.py:40]
        2018/01/17 14:37:03 - root - INFO - send_to: ['张三', '李四'] - [async_tasks.py:41]
        2018/01/17 14:37:03 - root - INFO - content: 老板喊你来背锅了 - [async_tasks.py:42]
        2018/01/17 14:37:13 - root - INFO - 模拟异步推送消息 - [async_tasks.py:40]
        2018/01/17 14:37:13 - root - INFO - send_to: ['刘五', '赵六'] - [async_tasks.py:41]
        2018/01/17 14:37:13 - root - INFO - content: 老板喊你来领奖金了 - [async_tasks.py:42]
        :return:
        """
        from handlers.async_tasks import async_push_message
        async_push_message(send_to=['张三', '李四'], content='老板喊你来背锅了')
        async_push_message(send_to=['刘五', '赵六'], content='老板喊你来领奖金了')

    @staticmethod
    def test_async_push_message():
        """
        测试前，请确保push_message的worker已经正常启动
        通过delay调用celery的task, task将异步执行
        从logs/message.log来看，基本上是同时执行，同时完成
        [2018-01-17 14:34:28,151: INFO/ForkPoolWorker-4] 模拟异步推送消息
        [2018-01-17 14:34:28,153: INFO/ForkPoolWorker-4] send_to: ['张三', '李四']
        [2018-01-17 14:34:28,154: INFO/ForkPoolWorker-4] content: 老板喊你来背锅了
        [2018-01-17 14:34:28,154: INFO/ForkPoolWorker-1] 模拟异步推送消息
        [2018-01-17 14:34:28,156: INFO/ForkPoolWorker-1] send_to: ['刘五', '赵六']
        [2018-01-17 14:34:28,158: INFO/ForkPoolWorker-1] content: 老板喊你来领奖金了
        [2018-01-17 14:34:40,348: INFO/ForkPoolWorker-1] Task handlers.async_tasks.async_push_message[4c1b7d67-328b-4891-bc54-3fba4b05783b] succeeded in 12.194373386038933s: None
        [2018-01-17 14:34:40,350: INFO/ForkPoolWorker-4] Task handlers.async_tasks.async_push_message[6ec03a25-092a-4387-9ce6-b498dbec683f] succeeded in 12.200127992022317s: None
        :return:
        """
        from handlers.async_tasks import async_push_message
        async_push_message.delay(send_to=['张三', '李四'], content='老板喊你来背锅了')
        async_push_message.delay(send_to=['刘五', '赵六'], content='老板喊你来领奖金了')

if __name__ == '__main__':
    pass
