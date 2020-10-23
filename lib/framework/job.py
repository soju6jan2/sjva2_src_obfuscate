import traceback
V=None
w=object
u=False
C=len
M=True
W=type
H=int
F=isinstance
I=str
X=Exception
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
 if job.args is V:
  job.target_function()
 else:
  job.target_function(job.args)
class Job(w):
 def __init__(self,plugin,job_id,interval,target_function,description,can_remove_by_framework,args=V):
  self.plugin=plugin
  self.job_id=job_id
  self.interval='%s'%interval
  self.interval_seconds=randint(1,59)
  self.target_function=target_function
  self.description=description
  self.can_remove_by_framework=can_remove_by_framework
  self.is_running=u
  self.thread=V
  self.start_time=V
  self.end_time=V
  self.running_timedelta=V
  self.status=V
  self.count=0
  self.make_time=datetime.now(timezone('Asia/Seoul'))
  if C(self.interval.strip().split(' '))==5:
   self.is_cron=M
   self.is_interval=u
  else:
   self.is_cron=u
   self.is_interval=M
  if self.is_interval:
   if app.config['config']['is_py2']:
    if W(self.interval)==W(u'')or W(self.interval)==W(''):
     self.interval=H(self.interval)
   else:
    if F(self.interval,I):
     self.interval=H(self.interval)
  self.args=args
  self.run=M
 def job_function(self):
  try:
   self.is_running=M
   self.start_time=datetime.now(timezone('Asia/Seoul'))
   if self.args is V:
    self.thread=threading.Thread(target=self.target_function,args=())
   else:
    self.thread=threading.Thread(target=self.target_function,args=(self.args,))
   self.thread.daemon=M
   self.thread.start()
   self.thread.join()
   self.end_time=datetime.now(timezone('Asia/Seoul'))
   self.running_timedelta=self.end_time-self.start_time
   self.status='success'
   if not scheduler.is_include(self.job_id):
    scheduler.remove_job_instance(self.job_id)
   self.count+=1
  except X as exception:
   self.status='exception'
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  finally:
   self.is_running=u
# Created by pyminifier (https://github.com/liftoff/pyminifier)
