import traceback
y=None
a=object
Q=False
M=len
w=True
k=isinstance
r=unicode
C=str
b=int
d=Exception
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
 if job.args is y:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(a):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=y):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=Q
  self.thread=y
  self.start_time=y
  self.end_time=y
  self.running_timedelta=y
  self.status=y
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if M(self.interval.strip().split(' '))==5:
   self.is_cron=w
   self.is_interval=Q
  else:
   self.is_cron=Q
   self.is_interval=w
  if self.is_interval:
   if app.config['config']['is_py2']:
    if k(self.interval,r)or k(self.interval,C):
     self.interval=b(self.interval)
   else:
    if k(self.interval,C):
     self.interval=b(self.interval)
  self.args=args
  self.run=w
 def job_function(self):
  try:
   self.is_running=w
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is y:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=w
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except d as e:
   self.status='exception'
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=Q
# Created by pyminifier (https://github.com/liftoff/pyminifier)
