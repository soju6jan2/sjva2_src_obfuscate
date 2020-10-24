import traceback
D=None
J=object
I=False
g=len
T=True
C=type
S=int
H=isinstance
v=str
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
 if job.args is D:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(J):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=D):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=I
  self.thread=D
  self.start_time=D
  self.end_time=D
  self.running_timedelta=D
  self.status=D
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if g(self.interval.strip().split(' '))==5:
   self.is_cron=T
   self.is_interval=I
  else:
   self.is_cron=I
   self.is_interval=T
  if self.is_interval:
   if app.config['config']['is_py2']:
    if C(self.interval)==C(u'')or C(self.interval)==C(''):
     self.interval=S(self.interval)
   else:
    if H(self.interval,v):
     self.interval=S(self.interval)
  self.args=args
  self.run=T
 def job_function(self):
  try:
   self.is_running=T
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is D:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=T
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
   self.is_running=I
# Created by pyminifier (https://github.com/liftoff/pyminifier)
