import traceback
E=None
T=object
Y=False
i=len
f=True
tP=isinstance
th=unicode
tV=str
R=int
P=Exception
t=traceback.format_exc
import threading
tY=threading.Thread
from datetime import datetime
S=datetime.now
from pytz import timezone
from random import randint
from framework import scheduler,app
e=app.config
tf=scheduler.remove_job_instance
tE=scheduler.is_include
tT=scheduler.get_job_instance
from framework.logger import get_logger
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
def multiprocessing_target(*a,**b):
 job_id=a[0]
 job=tT(job_id)
 if job.args is E:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(T):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=E):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=Y
  self.thread=E
  self.start_time=E
  self.end_time=E
  self.running_timedelta=E
  self.status=E
  self.count=0
  self.make_time=S(timezone('Asia/Seoul'))
  if i(self.interval.strip().split(' '))==5:
   self.is_cron=f
   self.is_interval=Y
  else:
   self.is_cron=Y
   self.is_interval=f
  if self.is_interval:
   if e['config']['is_py2']:
    if tP(self.interval,th)or tP(self.interval,tV):
     self.interval=R(self.interval)
   else:
    if tP(self.interval,tV):
     self.interval=R(self.interval)
  self.args=args
  self.run=f
 def job_function(self):
  try:
   self.is_running=f
   self.start_time=S(timezone('Asia/Seoul'))
   if self.args is E:
    self.thread=tY(target=self.target_function,args=())
   else:
    self.thread=tY(target=self.target_function,args=(self.args,))
   self.thread.daemon=f
   self.thread.start()
   self.thread.join()
   self.end_time=S(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not tE(self.job_id):
    tf(self.job_id)
   self.count+=1
  except P as e:
   self.status='exception'
   logger.error('Exception:%s',e)
   logger.error(t())
  finally:
   self.is_running=Y
# Created by pyminifier (https://github.com/liftoff/pyminifier)
