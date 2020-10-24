import os
D=True
a=False
L=Exception
M=sorted
h=getattr
G=len
import sys
import traceback
from framework import app,db,logger,plugin_instance_list,plugin_menu
import system
def is_include_menu(plugin_name):
 try:
  if plugin_name not in['daum_tv','ffmpeg','fileprocess_movie','gdrive_scan','ktv','plex','rclone']:
   return D
  if system.SystemLogic.get_setting_value('use_plugin_%s'%plugin_name)=='True':
   return D
  elif system.SystemLogic.get_setting_value('use_plugin_%s'%plugin_name)=='False':
   return a
 except L as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc()) 
 return D
def plugin_init():
 try:
  if not app.config['config']['auth_status']:
   return
  import inspect
  plugin_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'plugin')
  sys.path.insert(0,plugin_path)
  try:
   from system.model import ModelSetting as SystemModelSetting
   plugins=['command']
   for plugin in os.listdir(plugin_path):
    if SystemModelSetting.get_bool('use_plugin_{}'.format(plugin)):
     plugins.append(plugin)
  except:
   plugins=os.listdir(plugin_path)
  pass_include=[]
  except_plugin_list=[]
  if app.config['config']['run_by_migration']==a:
   if app.config['config']['server']or app.config['config']['is_debug']:
    server_plugin_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'server')
    if os.path.exists(server_plugin_path):
     sys.path.insert(0,server_plugin_path)
     plugins=plugins+os.listdir(server_plugin_path)
     pass_include=pass_include+os.listdir(server_plugin_path)
   try:
    server_plugin_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'data','custom')
    sys.path.append(server_plugin_path)
    tmps=os.listdir(server_plugin_path)
    add_plugin_list=[]
    for t in tmps:
     if not t.startswith('_'):
      add_plugin_list.append(t)
    plugins=plugins+add_plugin_list
    pass_include=pass_include+add_plugin_list
   except L as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
   try:
    server_plugin_path=system.SystemLogic.get_setting_value('plugin_dev_path')
    if server_plugin_path!='':
     if os.path.exists(server_plugin_path):
      sys.path.append(server_plugin_path)
      tmps=os.listdir(server_plugin_path)
      add_plugin_list=[]
      for t in tmps:
       if not t.startswith('_'):
        add_plugin_list.append(t)
        if app.config['config']['level']<=4:
         break
      plugins=plugins+add_plugin_list
      pass_include=pass_include+add_plugin_list
   except L as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
   plugins=M(plugins)
  """
        try: plugins.remove('epg')
        except: pass
        try: plugins.remove('epg_maker')
        except: pass
        """  
  for plugin_name in plugins:
   if plugin_name.startswith('_'):
    continue
   if plugin_name in except_plugin_list:
    logger.debug('Except plugin : %s'%plugin_menu)
    continue
   logger.debug('plugin_name:%s',plugin_name)
   try:
    mod=__import__('%s'%(plugin_name),fromlist=[])
    try:
     mod_plugin_info=h(mod,'plugin_info') 
     if 'policy_point' in mod_plugin_info:
      if mod_plugin_info['policy_point']>app.config['config']['point']:
       continue
     if 'policy_level' in mod_plugin_info:
      if mod_plugin_info['policy_level']>app.config['config']['level']:
       continue
    except:
     logger.debug('no plugin_info : %s',plugin_name)
    mod_blue_print=h(mod,'blueprint')
    if mod_blue_print:
     if plugin_name in pass_include or is_include_menu(plugin_name):
      app.register_blueprint(mod_blue_print)
    plugin_instance_list[plugin_name]=mod
   except L as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
    logger.debug('no blueprint')
  if not app.config['config']['run_by_worker']:
   try:
    db.create_all()
   except L as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
    logger.debug('db.create_all error')
  if not app.config['config']['run_by_real']:
   return
  for key,mod in plugin_instance_list.items():
   try:
    logger.debug('### plugin_load start : %s',key)
    mod_plugin_load=h(mod,'plugin_load')
    if mod_plugin_load and(key in pass_include or is_include_menu(key)):
     mod.plugin_load()
    logger.debug('### plugin_load return : %s',key)
   except L as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
    logger.debug('no init_scheduler')
   try:
    mod_menu=h(mod,'menu')
    if mod_menu and(key in pass_include or is_include_menu(key)):
     plugin_menu.append(mod_menu)
   except L as exception:
    logger.debug('no menu')
  logger.debug('Plugin Log completed.. : %s ',G(plugin_instance_list))
 except L as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def plugin_unload():
 for key,mod in plugin_instance_list.items():
  try:
   mod_plugin_unload=h(mod,'plugin_unload')
   if mod_plugin_unload:
    mod.plugin_unload()
  except L as exception:
   logger.error('module:%s',key)
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 system.plugin_unload()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
