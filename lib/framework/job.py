import traceback
c=None
N=object
j=False
K=len
s=True
A=isinstance
d=unicode
M=str
P=int
F=Exception
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
 if job.args is c:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(N):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=c):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=j
  self.thread=c
  self.start_time=c
  self.end_time=c
  self.running_timedelta=c
  self.status=c
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if K(self.interval.strip().split(' '))==5:
   self.is_cron=s
   self.is_interval=j
  else:
   self.is_cron=j
   self.is_interval=s
  if self.is_interval:
   if app.config['config']['is_py2']:
    if A(self.interval,d)or A(self.interval,M):
     self.interval=P(self.interval)
   else:
    if A(self.interval,M):
     self.interval=P(self.interval)
  self.args=args
  self.run=s
 def job_function(self):
  try:
   self.is_running=s
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is c:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=s
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except F as e:
   self.status='exception'
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=j
# Created by pyminifier (https://github.com/liftoff/pyminifier)
