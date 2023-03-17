from celery import Celery
from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader

host = ConfigLoader.config('cache')['connection']['host']
port = ConfigLoader.config('cache')['connection']['port']
passw = SecretLoader.secret("redis")['pass']
redis_conn = f'redis://default:{passw}@{host}:{port}'
worker = Celery('tasks', backend =redis_conn, broker=redis_conn)
worker.conf.task_create_missing_queues = True