import traceback
N=None
f=object
M=False
B=len
I=True
D=type
h=int
X=isinstance
P=str
S=Exception
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
 if job.args is N:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(f):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=N):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=M
  self.thread=N
  self.start_time=N
  self.end_time=N
  self.running_timedelta=N
  self.status=N
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if B(self.interval.strip().split(' '))==5:
   self.is_cron=I
   self.is_interval=M
  else:
   self.is_cron=M
   self.is_interval=I
  if self.is_interval:
   if app.config['config']['is_py2']:
    if D(self.interval)==D(u'')or D(self.interval)==D(''):
     self.interval=h(self.interval)
   else:
    if X(self.interval,P):
     self.interval=h(self.interval)
  self.args=args
  self.run=I
 def job_function(self):
  try:
   self.is_running=I
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is N:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=I
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except S as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=M
# Created by pyminifier (https://github.com/liftoff/pyminifier)
