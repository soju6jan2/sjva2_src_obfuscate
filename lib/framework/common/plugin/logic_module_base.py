class LogicModuleBase(b):
b=object
c=None
 name=c
 db_default=c
 P=c
 scheduler_desc=c
 first_menu=c
 socketio_list=c
 def __init__(self,P,first_menu,scheduler_desc=c):
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
  if self.P is not c and self.P.ModelSetting is not c and self.name is not c:
   return self.P.ModelSetting.get('{module_name}_interval'.format(module_name=self.name))
 def get_scheduler_desc(self):
  return self.scheduler_desc 
 def get_first_menu(self):
  return self.first_menu
 def setting_save_after(self):
  pass
 def process_telegram_data(self,data,target=c):
  pass
 def migration(self):
  pass
 def get_scheduler_name(self):
  return '%s_%s'%(self.P.package_name,self.name)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
