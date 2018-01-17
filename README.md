# Celery 简单实现示例
celery使用的简单实现，含有：

- 异步执行任务
- 为不同任务分配不同的队列
- 为不同队列设置优先级
- 计划任务

## 实现说明

### 定义模拟函数

在项目的handlers下，定义一些用来异步任务或计划任务的调用的函数。

这里定义了两个py文件，分别是async_tasks.py和schedules.py，前者用于异步任务，后者用于计划任务。

异步任务下有两个函数，模拟发送邮件和推送消息；计划任务下有数个根据计划任务执行事件定义的模拟函数。

async_tasks.py

```python
import logging
from time import sleep

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

def async_push_message(send_to, content):
    """
    模拟异步推送消息
    :param send_to:
    :param content:
    :return:
    """
    logging.info('模拟异步推送消息')
    logging.info(send_to, content)
    # 休眠
    sleep(10)
```

schedules.py

```python
import logging

def every_30_seconds(value):
    logging.info('every_30_seconds({value})'.format(value=value))
```



## QuickStart

### 异步执行任务

以模拟异步发送邮件为例

启动worker

```
python manage.py send_email
```

运行单元测试

```
python tests/test_celery.py 
```

### 为任务指定不同队列

