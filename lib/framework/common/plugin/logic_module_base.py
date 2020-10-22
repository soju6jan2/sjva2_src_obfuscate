import os
u=object
F=None
class LogicModuleBase(u):
 name=F
 db_default=F
 P=F
 scheduler_desc=F
 first_menu=F
 socketio_list=F
 def __init__(self,P,first_menu,scheduler_desc=F):
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
  if self.P is not F and self.P.ModelSetting is not F and self.name is not F:
   return self.P.ModelSetting.get('{module_name}_interval'.format(module_name=self.name))
 def get_scheduler_desc(self):
  return self.scheduler_desc 
 def get_first_menu(self):
  return self.first_menu
 def setting_save_after(self):
  pass
 def process_telegram_data(self,data,target=F):
  pass
 def migration(self):
  pass
 def get_scheduler_name(self):
  return '%s_%s'%(self.P.package_name,self.name)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
