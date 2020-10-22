import os
K=object
Q=None
U=Exception
s=False
import traceback
I=traceback.format_exc
import time
O=time.sleep
import threading
a=threading.Thread
import platform
from framework import db,scheduler
T=scheduler.execute_job
J=scheduler.is_running
X=scheduler.is_include
M=scheduler.remove_job
y=scheduler.add_job_instance
F=db.session
from framework.job import Job
from framework.util import Util
class Logic(K):
 db_default={'recent_menu_plugin':'',}
 def __init__(self,P):
  self.P=P
 def plugin_load(self):
  try:
   self.P.logger.debug('%s plugin_load',self.P.package_name)
   self.db_init()
   for module in self.P.module_list:
    module.migration()
   for module in self.P.module_list:
    module.plugin_load()
   if self.P.ModelSetting is not Q:
    for module in self.P.module_list:
     key='{sub}_auto_start'.format(sub=module.name)
     if self.P.ModelSetting.has_key(key)and self.P.ModelSetting.get_bool(key):
      self.scheduler_start(module.name)
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def db_init(self):
  try:
   if self.P.ModelSetting is Q:
    return
   for key,value in Logic.db_default.items():
    if F.query(self.P.ModelSetting).filter_by(key=key).count()==0:
     F.add(self.P.ModelSetting(key,value))
   for module in self.P.module_list:
    if module.db_default is not Q:
     for key,value in module.db_default.items():
      if F.query(self.P.ModelSetting).filter_by(key=key).count()==0:
       F.add(self.P.ModelSetting(key,value))
   F.commit()
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def plugin_unload(self):
  try:
   self.P.logger.debug('%s plugin_unload',self.P.package_name)
   for module in self.P.module_list:
    module.plugin_unload()
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def scheduler_start(self,sub):
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   module=self.get_module(sub)
   job=Job(self.P.package_name,job_id,module.get_scheduler_interval(),self.scheduler_function,module.get_scheduler_desc(),s,args=sub)
   y(job)
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def scheduler_stop(self,sub):
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   M(job_id)
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def scheduler_function(self,sub):
  try:
   module=self.get_module(sub)
   module.scheduler_function()
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def reset_db(self,sub):
  try:
   module=self.get_module(sub)
   return module.reset_db()
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def one_execute(self,sub):
  self.P.logger.debug('one_execute :%s',sub)
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   if X(job_id):
    if J(job_id):
     ret='is_running'
    else:
     T(job_id)
     ret='scheduler'
   else:
    def func():
     O(2)
     self.scheduler_function(sub)
    a(target=func,args=()).start()
    ret='thread'
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
   ret='fail'
  return ret
 def get_module(self,sub):
  try:
   for module in self.P.module_list:
    if module.name==sub:
     return module
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def process_telegram_data(self,data,target=Q):
  try:
   for module in self.P.module_list:
    if target is Q or target.startswith(module.name):
     module.process_telegram_data(data,target=target)
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
