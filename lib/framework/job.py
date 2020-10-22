import traceback
o=None
P=object
y=False
f=len
G=True
i=isinstance
l=unicode
N=str
I=int
e=Exception
import threading
from datetime import datetime
from pytz import timezone
from random import randint
from framework import scheduler,app
from framework.logger import get_logger
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
def multiprocessing_target(*a,**b):
 job_id=a[0]
 job=scheduler.get_job_instance(job_id)
 if job.args is o:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(P):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=o):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=y
  self.thread=o
  self.start_time=o
  self.end_time=o
  self.running_timedelta=o
  self.status=o
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if f(self.interval.strip().split(' '))==5:
   self.is_cron=G
   self.is_interval=y
  else:
   self.is_cron=y
   self.is_interval=G
  if self.is_interval:
   if app.config['config']['is_py2']:
    if i(self.interval,l)or i(self.interval,N):
     self.interval=I(self.interval)
   else:
    if i(self.interval,N):
     self.interval=I(self.interval)
  self.args=args
  self.run=G
 def job_function(self):
  try:
   self.is_running=G
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is o:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=G
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except e as e:
   self.status='exception'
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=y
# Created by pyminifier (https://github.com/liftoff/pyminifier)
