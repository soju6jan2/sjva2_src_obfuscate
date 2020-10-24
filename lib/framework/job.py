import traceback
H=None
h=object
J=False
F=len
e=True
l=type
B=int
M=isinstance
G=str
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
 if job.args is H:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(h):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=H):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=J
  self.thread=H
  self.start_time=H
  self.end_time=H
  self.running_timedelta=H
  self.status=H
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if F(self.interval.strip().split(' '))==5:
   self.is_cron=e
   self.is_interval=J
  else:
   self.is_cron=J
   self.is_interval=e
  if self.is_interval:
   if app.config['config']['is_py2']:
    if l(self.interval)==l(u'')or l(self.interval)==l(''):
     self.interval=B(self.interval)
   else:
    if M(self.interval,G):
     self.interval=B(self.interval)
  self.args=args
  self.run=e
 def job_function(self):
  try:
   self.is_running=e
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is H:
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
  except I as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=J
# Created by pyminifier (https://github.com/liftoff/pyminifier)
