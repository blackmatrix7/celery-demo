# Celery 简单实现
一个celery使用的简单实现示例

- 异步执行任务
- 为不同任务分配不同的队列
- 为不同队列设置优先级
- 计划任务

## 创建Celery

### 配置Celery参数

在创建celery实例之前，需要对celery的参数进行一些配置。

在这里列出一些比较常用的Celery配置项：

| 配置项名称               | 说明                                                   |
| ------------------------ | ------------------------------------------------------ |
| CELERY_DEFAULT_QUEUE     | 默认的队列名称，当没有为task特别指定队列时，采用此队列 |
| CELERY_BROKER_URL        | 消息代理，用于发布者传递消息给消费者，推荐RabbitMQ     |
| CELERY_RESULT_BACKEND    | 后端，用于存储任务执行结果，推荐redis                  |
| CELERY_TASK_SERIALIZER   | 任务的序列化方式                                       |
| CELERY_RESULT_SERIALIZER | 任务执行结果的序列化方式                               |
| CELERY_ACCEPT_CONTENT    |                                                        |
| CELERYD_CONCURRENCY      | 任务消费者的并发数                                     |
| CELERY_TIMEZONE          | 时区设置，计划任务需要，推荐 Asia/Shanghai             |
| CELERY_QUEUES            | Celery队列设定                                         |
| CELERY_ROUTES            | Celery路由设定，用于给不同的任务指派不同的队列         |
| CELERYBEAT_SCHEDULE      | Celery计划任务设定                                     |

*为了使用方便，在这里引入了之前写的[config模块](https://github.com/blackmatrix7/matrix-toolkit/blob/master/toolkit/config.py)（支持本地配置不提交到github），本身是非必须的，用dict存储celery配置一样可以。所以在下面的示例代码中，会以注释的形式，演示不使用config模块实现celery配置。*

```python
# 等价于直接定义一个broker，如
# broker = 'amqp://user:password@127.0.0.1:5672//'
broker = current_config.CELERY_BROKER_URL
# 将config模块的配置转换成dict，等价于直接通过dict定义一组celery配置
celery_conf = {k: v for k, v in current_config.items()}
```

### 创建celery实例

将之前创建的broker和celery_conf传递给celery，用于创建celery实例。

manage.py

```python
# 创建celery实例
celery = Celery('demo',  broker=broker)
# 载入celery配置
celery.config_from_object(celery_conf)
```

### 定义模拟函数

在项目的handlers下，定义一些用来异步任务或计划任务的调用的函数。

这里定义了两个py文件，分别是[async_tasks.py](https://github.com/blackmatrix7/celery-demo/blob/master/handlers/async_tasks.py)和[schedules.py](https://github.com/blackmatrix7/celery-demo/blob/master/handlers/schedules.py)，前者用于异步任务，后者用于计划任务。

异步任务下有两个函数，模拟发送邮件和推送消息；计划任务下有数个根据计划任务执行事件定义的模拟函数。

## 创建celery worker

推荐以celery.start的方式来启动celery

#### 启动参数

在创建完celery实例后，调用celery实例的start方法，来启动celery。

*在demo中，在manage.py中创建celery实例。*

```python
celery = Celery('demo',  broker=broker)
celery.config_from_object(celery_conf)
# argv中传入启动celery所需的参数
celery.start(argv=['celery', 'worker', '-l', 'info', '-f', 'logs/celery.log'])
```

第一个参数是固定的，用于启动celery

第二个参数是启动的celery组件，这里启动的是worker，用于执行任务

第三个参数和第四个参数为一组，指定日志的级别，这里记录级别为info的日子

第五个参数和第六个参数为一组，指定日志文件的位置，这里将日志记录在log/celery.log

#### 指定消费的队列

在启动命令中，增加一个-Q的参数，用于指定消费的队列。

```python
celery.start(argv=['celery', 'worker', '-Q', 'message_queue', '-l', 'info', '-f', 'logs/message.log'])
```

上述的参数中，'-Q', 'message_queue'两个参数，是指定这个worker消费名为“message_queue”的队列。

### 创建异步任务

对于需要在celery中异步执行的函数，只需要在函数上增加一个装饰器。

```python
# 导入manage.py中创建的celery实例
from manage import celery

# 需要在celery中异步执行的函数，增加celery.task装饰器
@celery.task
def async_send_email(send_from, send_to, subject, content):
    """
    忽略方法实现
    """
    pass
```

### 异步执行任务

对于以celery.task装饰的函数，可以同步运行，也可以异步运行。

接上一个例子的async_send_email函数。

同步执行时，直接调用这个函数即可。

```python
async_push_message(send_to=['张三', '李四'], content='老板喊你来背锅了')
async_push_message(send_to=['刘五', '赵六'], content='老板喊你来领奖金了')
```

需要异步执行时，调用函数的delay()方法执行，此时会将任务委托给celery后台的worker执行。

```python
async_push_message.delay(send_to=['张三', '李四'], content='老板喊你来背锅了')
async_push_message.delay(send_to=['刘五', '赵六'], content='老板喊你来领奖金了')
```

### 为任务指定不同队列

其实在之前配置celery参数时，就已经实现为不同任务指定不同队列的目标。

在这里详细说明下配置项：

```python
# 导入Queue
from kombu import Queue
# 导入Task所在的模块，所有使用celery.task装饰器装饰过的函数，所需要把所在的模块导入
# 我们之前创建的几个测试用函数，都在handlers.async_tasks和handlers.schedules中
# 所以在这里需要导入这两个模块，以str表示模块的位置，模块组成tuple后赋值给CELERY_IMPORTS
# 这样Celery在启动时，会自动找到这些模块，并导入模块内的task
CELERY_IMPORTS = ('handlers.async_tasks', 'handlers.schedules')
# 为Celery设定多个队列，CELERY_QUEUES是个tuple，每个tuple的元素都是由一个Queue的实例组成
# 创建Queue的实例时，传入name和routing_key，name即队列名称
CELERY_QUEUES = (
    Queue(name='email_queue', routing_key='email_router'),
    Queue(name='message_queue', routing_key='message_router'),
    Queue(name='schedules_queue', routing_key='schedules_router'),
)
# 最后，为不同的task指派不同的队列
# 将所有的task组成dict，key为task的名称，即task所在的模块，及函数名
# 如async_send_email所在的模块为handlers.async_tasks
# 那么task名称就是handlers.async_tasks.async_send_email
# 每个task的value值也是为dict，设定需要指派的队列name，及对应的routing_key
# 这里的name和routing_key需要和CELERY_QUEUES设定的完全一致
CELERY_ROUTES = {
    'handlers.async_tasks.async_send_email': {
        'queue': 'email_queue',
        'routing_key': 'vcan.email_router',
    },
    'handlers.async_tasks.async_push_message': {
        'queue': 'message_queue',
        'routing_key': 'message_router',
    },
    'handlers.schedules.every_30_seconds': {
        'queue': 'schedules_queue',
        'routing_key': 'schedules_router',
    }
}
```

配置完成后，不同的task会根据CELERY_ROUTES的设置，指派到不同的消息队列。

## 计划任务

celery除用于异步执行任务外，还可以用于执行计划任务。

### 设定celery时区

在开始配置计划任务之前对配置文件中设定celery时区。

```python
# 设定 Celery 时区
CELERY_TIMEZONE = 'Asia/Shanghai'
```

### 定义计划任务

celery可以通过多种方式定义计划任务，如在配置文件中，通过代码动态添加等等。

#### 在配置文件中定义计划任务

<u>计划任务也是异步执行任务的一种方式，所以也需要参考之前的说明，为计划任务分配不同的队列。</u>

在配置文件中，新增一项CELERYBEAT_SCHEDULE的配置

```python
from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
	# 给计划任务取一个独一无二的名字吧
    'every-30-seconds': {
    	# task就是需要执行计划任务的函数
         'task': 'handlers.schedules.every_30_seconds',
         # 配置计划任务的执行时间，这里是每30秒执行一次
         'schedule': timedelta(seconds=30),
         # 传入给计划任务函数的参数
         'args': {'value': '2333333'}
    }
}
```

CELERYBEAT_SCHEDULE是一个dict，每个key为计划任务的名称，value也是dict，包含task、schedule、args。

task即需要执行计划任务的函数，这里是`handlers.schedules.every_30_seconds`，即handlers的schedules的every_30_seconds函数，如需配置其他的函数，依照此规则定义即可。

args是传递给计划任务函数的参数，在这个例子中，即传递给every_30_seconds的参数，如果无需参数，则args配置为None。

schedule即配置计划任务的执行时间，例子中使用的是timedelta实例，用于实现固定间隔某些时间执行。除此之外，还可以设定某个时间点执行，或重复某个时间点执行。这个就需要用到celery的crontab类。

```python
'push_occupancy_rates': {
            'task': 'handlers.schedules.test_func_b',
            # 每天中午12点执行
            'schedule': crontab(hour='12', minute='0'),
            'args': None
        },
```

关于crontab更详细的配置方式，可以参考[官方手册](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)：

| **Example**                                                  | **Meaning**                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| crontab()                                                    | Execute every minute.                                        |
| crontab(minute=0, hour=0)                                    | Execute daily at midnight.                                   |
| crontab(minute=0, hour='*/3')                                | Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm. |
| crontab(minute=0, hour='0,3,6,9,12,15,18,21')                | Same as previous.                                            |
| crontab(minute='*/15')                                       | Execute every 15 minutes.                                    |
| crontab(day_of_week='sunday')                                | Execute every minute (!) at Sundays.                         |
| crontab(minute='*', hour='*', day_of_week='sun')             | Same as previous.                                            |
| crontab(minute='*/10', hour='3,17,22', day_of_week='thu,fri') | Execute every ten minutes, but only between 3-4 am, 5-6 pm, and 10-11 pm on Thursdays or Fridays. |
| crontab(minute=0,hour='*/2,*/3')                             | Execute every even hour, and every hour divisible by three. This means: at every hour *except*: 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm |
| crontab(minute=0, hour='*/5')                                | Execute hour divisible by 5. This means that it is triggered at 3pm, not 5pm (since 3pm equals the 24-hour clock value of “15”, which is divisible by 5). |
| crontab(minute=0,hour='*/3,8-17')                            | Execute every hour divisible by 3, and every hour during office hours (8am-5pm). |
| crontab(0, 0,day_of_month='2')                               | Execute on the second day of every month.                    |
| crontab(0, 0, day_of_month='2-30/3')                         | Execute on every even numbered day.                          |
| crontab(0, 0, day_of_month='1-7,15-21')                      | Execute on the first and third weeks of the month.           |
| crontab(0, 0,day_of_month='11', month_of_year='5')           | Execute on the eleventh of May every year.                   |
| crontab(0, 0, month_of_year='*/3')                           | Execute on the first month of every quarter.                 |

