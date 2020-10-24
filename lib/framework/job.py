import traceback
u=None
z=object
C=False
i=len
h=True
s=type
K=int
j=isinstance
W=str
y=Exception
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
 if job.args is u:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(z):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=u):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=C
  self.thread=u
  self.start_time=u
  self.end_time=u
  self.running_timedelta=u
  self.status=u
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if i(self.interval.strip().split(' '))==5:
   self.is_cron=h
   self.is_interval=C
  else:
   self.is_cron=C
   self.is_interval=h
  if self.is_interval:
   if app.config['config']['is_py2']:
    if s(self.interval)==s(u'')or s(self.interval)==s(''):
     self.interval=K(self.interval)
   else:
    if j(self.interval,W):
     self.interval=K(self.interval)
  self.args=args
  self.run=h
 def job_function(self):
  try:
   self.is_running=h
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is u:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=h
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except y as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=C
# Created by pyminifier (https://github.com/liftoff/pyminifier)
