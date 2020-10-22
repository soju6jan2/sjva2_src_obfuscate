import os
o=object
J=None
G=Exception
g=False
import traceback
import time
import threading
import platform
from framework import db,scheduler
from framework.job import Job
from framework.util import Util
class Logic(o):
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
   if self.P.ModelSetting is not J:
    for module in self.P.module_list:
     key='{sub}_auto_start'.format(sub=module.name)
     if self.P.ModelSetting.has_key(key)and self.P.ModelSetting.get_bool(key):
      self.scheduler_start(module.name)
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def db_init(self):
  try:
   if self.P.ModelSetting is J:
    return
   for key,value in Logic.db_default.items():
    if db.session.query(self.P.ModelSetting).filter_by(key=key).count()==0:
     db.session.add(self.P.ModelSetting(key,value))
   for module in self.P.module_list:
    if module.db_default is not J:
     for key,value in module.db_default.items():
      if db.session.query(self.P.ModelSetting).filter_by(key=key).count()==0:
       db.session.add(self.P.ModelSetting(key,value))
   db.session.commit()
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def plugin_unload(self):
  try:
   self.P.logger.debug('%s plugin_unload',self.P.package_name)
   for module in self.P.module_list:
    module.plugin_unload()
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def scheduler_start(self,sub):
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   module=self.get_module(sub)
   job=Job(self.P.package_name,job_id,module.get_scheduler_interval(),self.scheduler_function,module.get_scheduler_desc(),g,args=sub)
   scheduler.add_job_instance(job)
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def scheduler_stop(self,sub):
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   scheduler.remove_job(job_id)
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def scheduler_function(self,sub):
  try:
   module=self.get_module(sub)
   module.scheduler_function()
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def reset_db(self,sub):
  try:
   module=self.get_module(sub)
   return module.reset_db()
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def one_execute(self,sub):
  self.P.logger.debug('one_execute :%s',sub)
  try:
   job_id='%s_%s'%(self.P.package_name,sub)
   if scheduler.is_include(job_id):
    if scheduler.is_running(job_id):
     ret='is_running'
    else:
     scheduler.execute_job(job_id)
     ret='scheduler'
   else:
    def func():
     time.sleep(2)
     self.scheduler_function(sub)
    threading.Thread(target=func,args=()).start()
    ret='thread'
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
   ret='fail'
  return ret
 def get_module(self,sub):
  try:
   for module in self.P.module_list:
    if module.name==sub:
     return module
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def process_telegram_data(self,data,target=J):
  try:
   for module in self.P.module_list:
    if target is J or target.startswith(module.name):
     module.process_telegram_data(data,target=target)
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
