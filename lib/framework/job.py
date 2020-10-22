import traceback
R=None
b=object
l=False
L=len
q=True
k=type
Y=int
M=isinstance
a=str
G=Exception
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
 if job.args is R:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(b):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=R):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=l
  self.thread=R
  self.start_time=R
  self.end_time=R
  self.running_timedelta=R
  self.status=R
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if L(self.interval.strip().split(' '))==5:
   self.is_cron=q
   self.is_interval=l
  else:
   self.is_cron=l
   self.is_interval=q
  if self.is_interval:
   if app.config['config']['is_py2']:
    if k(self.interval)==k(u'')or k(self.interval)==k(''):
     self.interval=Y(self.interval)
   else:
    if M(self.interval,a):
     self.interval=Y(self.interval)
  self.args=args
  self.run=q
 def job_function(self):
  try:
   self.is_running=q
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is R:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=q
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except G as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=l
# Created by pyminifier (https://github.com/liftoff/pyminifier)
