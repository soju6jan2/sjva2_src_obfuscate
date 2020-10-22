import os
Y=False
u=os.environ
import sys
from framework import app,logger,path_app_root
N=app.name
e=app.config
from celery import Celery
try:
 redis_port=u['REDIS_PORT']
except:
 redis_port='6379'
e['CELERY_BROKER_URL']='redis://localhost:%s/0'%redis_port
e['CELERY_RESULT_BACKEND']='redis://localhost:%s/0'%redis_port
celery=Celery(N,broker=e['CELERY_BROKER_URL'],backend=e['CELERY_RESULT_BACKEND'])
celery.conf['CELERY_ENABLE_UTC']=Y
celery.conf.update(task_serializer='pickle',result_serializer='pickle',accept_content=['pickle'],timezone='Asia/Seoul')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
