import traceback
Q=None
U=object
O=False
h=len
v=True
b=type
J=int
W=isinstance
N=str
u=Exception
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
 if job.args is Q:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(U):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=Q):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=O
  self.thread=Q
  self.start_time=Q
  self.end_time=Q
  self.running_timedelta=Q
  self.status=Q
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if h(self.interval.strip().split(' '))==5:
   self.is_cron=v
   self.is_interval=O
  else:
   self.is_cron=O
   self.is_interval=v
  if self.is_interval:
   if app.config['config']['is_py2']:
    if b(self.interval)==b(u'')or b(self.interval)==b(''):
     self.interval=J(self.interval)
   else:
    if W(self.interval,N):
     self.interval=J(self.interval)
  self.args=args
  self.run=v
 def job_function(self):
  try:
   self.is_running=v
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is Q:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=v
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except u as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=O
# Created by pyminifier (https://github.com/liftoff/pyminifier)
