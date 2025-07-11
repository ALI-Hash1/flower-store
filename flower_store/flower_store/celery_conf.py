from celery import Celery
from datetime import timedelta
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_store.settings')

celery_app = Celery('flower_store')

celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://'

celery_app.conf.result_backend = 'rpc://'

celery_app.conf.task_serializer = 'json'

celery_app.conf.result_serializer = 'json'

celery_app.conf.accept_content = ('json',)

celery_app.conf.result_expire = timedelta(days=1)

celery_app.conf.task_always_eager = False
