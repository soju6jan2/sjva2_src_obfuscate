import traceback
O=None
t=object
q=False
b=len
e=True
M=isinstance
S=unicode
Q=str
P=int
I=Exception
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
 if job.args is O:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(t):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=O):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=q
  self.thread=O
  self.start_time=O
  self.end_time=O
  self.running_timedelta=O
  self.status=O
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if b(self.interval.strip().split(' '))==5:
   self.is_cron=e
   self.is_interval=q
  else:
   self.is_cron=q
   self.is_interval=e
  if self.is_interval:
   if app.config['config']['is_py2']:
    if M(self.interval,S)or M(self.interval,Q):
     self.interval=P(self.interval)
   else:
    if M(self.interval,Q):
     self.interval=P(self.interval)
  self.args=args
  self.run=e
 def job_function(self):
  try:
   self.is_running=e
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is O:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=e
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except I as e:
   self.status='exception'
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=q
# Created by pyminifier (https://github.com/liftoff/pyminifier)
