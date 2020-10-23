import traceback
S=None
d=object
E=False
q=len
U=True
f=type
c=int
t=isinstance
a=str
N=Exception
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
 if job.args is S:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(d):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=S):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=E
  self.thread=S
  self.start_time=S
  self.end_time=S
  self.running_timedelta=S
  self.status=S
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if q(self.interval.strip().split(' '))==5:
   self.is_cron=U
   self.is_interval=E
  else:
   self.is_cron=E
   self.is_interval=U
  if self.is_interval:
   if app.config['config']['is_py2']:
    if f(self.interval)==f(u'')or f(self.interval)==f(''):
     self.interval=c(self.interval)
   else:
    if t(self.interval,a):
     self.interval=c(self.interval)
  self.args=args
  self.run=U
 def job_function(self):
  try:
   self.is_running=U
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is S:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=U
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except N as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=E
# Created by pyminifier (https://github.com/liftoff/pyminifier)
