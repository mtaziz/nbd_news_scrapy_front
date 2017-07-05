from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbd_news_scrapy_front.settings')

app = Celery('nbd_news_scrapy_front')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = "Asia/Shanghai"
app.autodiscover_tasks('scrapy_config')
