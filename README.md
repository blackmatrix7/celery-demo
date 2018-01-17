# Celery 简单实现示例
celery使用的简单实现，含有：

- 异步执行任务
- 为不同任务分配不同的队列
- 为不同队列设置优先级
- 计划任务

## 实现说明

### 配置Celery参数

*为了使用方便，在这里引入了之前写的[config模块](https://github.com/blackmatrix7/matrix-toolkit/blob/master/toolkit/config.py)（支持本地配置不提交到github），本身是非必须的，用dict存储celery配置一样可以。所以在下面的示例代码中，会以注释的形式，演示不使用config模块实现celery配置。*

```python
# 等价于直接定义一个broker，如
# broker = 'amqp://user:password@127.0.0.1:5672//'
broker = current_config.CELERY_BROKER_URL
# 将config模块的配置转换成dict，等价于直接通过dict定义一组celery配置
celery_conf = {k: v for k, v in current_config.items() if k.startswith('CELERY')}
```

### 创建celery实例

将之前创建的broker和celery_conf传递给celery，用于创建celery实例。

manage.py

```python
# 创建celery实例
celery = Celery('demo',  broker=broker)
celery.config_from_object(celery_conf)
```

### 定义模拟函数

在项目的handlers下，定义一些用来异步任务或计划任务的调用的函数。

这里定义了两个py文件，分别是[async_tasks.py](https://github.com/blackmatrix7/celery-demo/blob/master/handlers/async_tasks.py)和[schedules.py](https://github.com/blackmatrix7/celery-demo/blob/master/handlers/schedules.py)，前者用于异步任务，后者用于计划任务。

异步任务下有两个函数，模拟发送邮件和推送消息；计划任务下有数个根据计划任务执行事件定义的模拟函数。

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

