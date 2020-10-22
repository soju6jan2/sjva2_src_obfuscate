import traceback
E=None
y=object
i=False
x=len
R=True
OJ=isinstance
Ob=unicode
OM=str
A=int
J=Exception
O=traceback.format_exc
import threading
Oi=threading.Thread
from datetime import datetime
o=datetime.now
from pytz import timezone
from random import randint
from framework import scheduler,app
f=app.config
OR=scheduler.remove_job_instance
OE=scheduler.is_include
Oy=scheduler.get_job_instance
from framework.logger import get_logger
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
def multiprocessing_target(*a,**b):
 job_id=a[0]
 job=Oy(job_id)
 if job.args is E:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(y):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=E):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=i
  self.thread=E
  self.start_time=E
  self.end_time=E
  self.running_timedelta=E
  self.status=E
  self.count=0
  self.make_time=o(timezone('Asia/Seoul'))
  if x(self.interval.strip().split(' '))==5:
   self.is_cron=R
   self.is_interval=i
  else:
   self.is_cron=i
   self.is_interval=R
  if self.is_interval:
   if f['config']['is_py2']:
    if OJ(self.interval,Ob)or OJ(self.interval,OM):
     self.interval=A(self.interval)
   else:
    if OJ(self.interval,OM):
     self.interval=A(self.interval)
  self.args=args
  self.run=R
 def job_function(self):
  try:
   self.is_running=R
   self.start_time=o(timezone('Asia/Seoul'))
   if self.args is E:
    self.thread=Oi(target=self.target_function,args=())
   else:
    self.thread=Oi(target=self.target_function,args=(self.args,))
   self.thread.daemon=R
   self.thread.start()
   self.thread.join()
   self.end_time=o(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not OE(self.job_id):
    OR(self.job_id)
   self.count+=1
  except J as e:
   self.status='exception'
   logger.error('Exception:%s',e)
   logger.error(O())
  finally:
   self.is_running=i
# Created by pyminifier (https://github.com/liftoff/pyminifier)
