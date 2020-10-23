import os
u=False
import sys
from framework import app,logger,path_app_root
from celery import Celery
try:
 redis_port=os.environ['REDIS_PORT']
except:
 redis_port='6379'
app.config['CELERY_BROKER_URL']='redis://localhost:%s/0'%redis_port
app.config['CELERY_RESULT_BACKEND']='redis://localhost:%s/0'%redis_port
celery=Celery(app.name,broker=app.config['CELERY_BROKER_URL'],backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf['CELERY_ENABLE_UTC']=u
celery.conf.update(task_serializer='pickle',result_serializer='pickle',accept_content=['pickle'],timezone='Asia/Seoul')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
