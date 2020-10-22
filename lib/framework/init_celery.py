import os
i=False
n=os.environ
import sys
from framework import app,logger,path_app_root
p=app.name
f=app.config
from celery import Celery
try:
 redis_port=n['REDIS_PORT']
except:
 redis_port='6379'
f['CELERY_BROKER_URL']='redis://localhost:%s/0'%redis_port
f['CELERY_RESULT_BACKEND']='redis://localhost:%s/0'%redis_port
celery=Celery(p,broker=f['CELERY_BROKER_URL'],backend=f['CELERY_RESULT_BACKEND'])
celery.conf['CELERY_ENABLE_UTC']=i
celery.conf.update(task_serializer='pickle',result_serializer='pickle',accept_content=['pickle'],timezone='Asia/Seoul')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
