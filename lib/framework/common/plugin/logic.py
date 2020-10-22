import os
B=object
v=None
V=Exception
z=False
import traceback
u=traceback.format_exc
import time
T=time.sleep
import threading
F=threading.Thread
import platform
from framework import db,scheduler
o=scheduler.execute_job
C=scheduler.is_running
X=scheduler.is_include
G=scheduler.remove_job
A=scheduler.add_job_instance
c=db.session
from framework.job import Job
from framework.util import Util
class Logic(B):
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
   if self.P.ModelSetting is not v:
    for module in self.P.module_list:
     key='{sub}_auto_start'.format(sub=module.name)
     if self.P.ModelSetting.has_key(key)and self.P.ModelSetting.get_bool(key):
      self.scheduler_start(module.name)
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def db_init(self):
  try:
   if self.P.ModelSetting is v:
    return
   for key,value in Logic.db_default.items():
    if c.query(self.P.ModelSetting).filter_by(key=key).count()==0:
     c.add(self.P.ModelSetting(key,value))
   for module in self.P.module_list:
    if module.db_default is not v:
     for key,value in module.db_default.items():
      if c.query(self.P.ModelSetting).filter_by(key=key).count()==0:
       c.add(self.P.ModelSetting(key,value))
   c.commit()
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def plugin_unload(self):
  try:
   self.P.logger.debug('%s plugin_unload',self.P.package_name)
   for module in self.P.module_list:
    module.plugin_unload()
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def scheduler_start(self,sub):
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   module=self.get_module(sub)
   job=Job(self.P.package_name,job_id,module.get_scheduler_interval(),self.scheduler_function,module.get_scheduler_desc(),z,args=sub)
   A(job)
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def scheduler_stop(self,sub):
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   G(job_id)
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def scheduler_function(self,sub):
  try:
   module=self.get_module(sub)
   module.scheduler_function()
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def reset_db(self,sub):
  try:
   module=self.get_module(sub)
   return module.reset_db()
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def one_execute(self,sub):
  self.P.logger.debug('one_execute :%s',sub)
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   if X(job_id):
    if C(job_id):
     ret='is_running'
    else:
     o(job_id)
     ret='scheduler'
   else:
    def func():
     T(2)
     self.scheduler_function(sub)
    F(target=func,args=()).start()
    ret='thread'
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
   ret='fail'
  return ret
 def get_module(self,sub):
  try:
   for module in self.P.module_list:
    if module.name==sub:
     return module
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def process_telegram_data(self,data,target=v):
  try:
   for module in self.P.module_list:
    if target is v or target.startswith(module.name):
     module.process_telegram_data(data,target=target)
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
