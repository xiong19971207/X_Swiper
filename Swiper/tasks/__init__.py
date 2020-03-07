import os

from celery import Celery

from tasks import config


os.environ.setdefault("DJANGO_SETTING_MODULE", 'Swiper.settings')

celery_app = Celery('async_tasks')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks('')
