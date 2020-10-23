import os
t=object
N=None
class LogicModuleBase(t):
 name=N
 db_default=N
 P=N
 scheduler_desc=N
 first_menu=N
 socketio_list=N
 def __init__(self,P,first_menu,scheduler_desc=N):
  self.P=P
  self.scheduler_desc=scheduler_desc
  self.first_menu=first_menu
 def process_menu(self,sub):
  pass
 def process_ajax(self,sub,req):
  pass
 def process_api(self,sub,req):
  pass
 def process_normal(self,sub,req):
  pass
 def scheduler_function():
  pass
 def reset_db(self):
  pass
 def plugin_load(self):
  pass
 def plugin_unload(self):
  pass
 def get_scheduler_interval(self):
  if self.P is not N and self.P.ModelSetting is not N and self.name is not N:
   return self.P.ModelSetting.get('{module_name}_interval'.format(module_name=self.name))
 def get_scheduler_desc(self):
  return self.scheduler_desc 
 def get_first_menu(self):
  return self.first_menu
 def setting_save_after(self):
  pass
 def process_telegram_data(self,data,target=N):
  pass
 def migration(self):
  pass
 def get_scheduler_name(self):
  return '%s_%s'%(self.P.package_name,self.name)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
