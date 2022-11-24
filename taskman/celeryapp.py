from celery import Celery
from tools.config_loader import ConfigLoader

host = ConfigLoader.config('cache')['connection']['host']
port = ConfigLoader.config('cache')['connection']['port'] 
redis_conn = f'redis://{host}:{port}'
app = Celery('tasks', backend =redis_conn, broker=redis_conn)
app.conf.task_create_missing_queues = True