import traceback
Y=None
S=object
W=False
N=len
B=True
q=type
b=int
V=isinstance
p=str
r=Exception
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
 if job.args is Y:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(S):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=Y):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=W
  self.thread=Y
  self.start_time=Y
  self.end_time=Y
  self.running_timedelta=Y
  self.status=Y
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if N(self.interval.strip().split(' '))==5:
   self.is_cron=B
   self.is_interval=W
  else:
   self.is_cron=W
   self.is_interval=B
  if self.is_interval:
   if app.config['config']['is_py2']:
    if q(self.interval)==q(u'')or q(self.interval)==q(''):
     self.interval=b(self.interval)
   else:
    if V(self.interval,p):
     self.interval=b(self.interval)
  self.args=args
  self.run=B
 def job_function(self):
  try:
   self.is_running=B
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is Y:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=B
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except r as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=W
# Created by pyminifier (https://github.com/liftoff/pyminifier)
