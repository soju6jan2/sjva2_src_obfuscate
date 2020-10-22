import os
R=True
i=False
J=Exception
v=sorted
d=getattr
x=len
l=os.listdir
k=os.path
import sys
Q=sys.path
import traceback
O=traceback.format_exc
from framework import app,db,logger,plugin_instance_list,plugin_menu
s=plugin_menu.append
c=plugin_instance_list.items
G=logger.debug
B=logger.error
L=db.create_all
g=app.register_blueprint
f=app.config
import system
N=system.plugin_unload
K=system.SystemLogic
def is_include_menu(plugin_name):
 try:
  if plugin_name not in['daum_tv','ffmpeg','fileprocess_movie','gdrive_scan','ktv','plex','rclone']:
   return R
  if K.get_setting_value('use_plugin_%s'%plugin_name)=='True':
   return R
  elif K.get_setting_value('use_plugin_%s'%plugin_name)=='False':
   return i
 except J as e:
  B('Exception:%s',e)
  B(O()) 
 return R
def plugin_init():
 try:
  if not f['config']['auth_status']:
   return
  import inspect
  plugin_path=k.join(k.dirname(k.dirname(k.dirname(k.abspath(__file__)))),'plugin')
  Q.insert(0,plugin_path)
  plugins=l(plugin_path)
  pass_include=[]
  except_plugin_list=[]
  if f['config']['run_by_migration']==i:
   if f['config']['server']or f['config']['is_debug']:
    server_plugin_path=k.join(k.dirname(k.dirname(k.dirname(k.abspath(__file__)))),'server')
    if k.exists(server_plugin_path):
     Q.insert(0,server_plugin_path)
     plugins=plugins+l(server_plugin_path)
     pass_include=pass_include+l(server_plugin_path)
   try:
    server_plugin_path=k.join(k.dirname(k.dirname(k.dirname(k.abspath(__file__)))),'data','custom')
    Q.append(server_plugin_path)
    tmps=l(server_plugin_path)
    add_plugin_list=[]
    for t in tmps:
     if not t.startswith('_'):
      add_plugin_list.append(t)
    plugins=plugins+add_plugin_list
    pass_include=pass_include+add_plugin_list
   except J as e:
    B('Exception:%s',e)
    B(O())
   try:
    server_plugin_path=K.get_setting_value('plugin_dev_path')
    if server_plugin_path!='':
     if k.exists(server_plugin_path):
      Q.append(server_plugin_path)
      tmps=l(server_plugin_path)
      add_plugin_list=[]
      for t in tmps:
       if not t.startswith('_'):
        add_plugin_list.append(t)
        if f['config']['level']<=4:
         break
      plugins=plugins+add_plugin_list
      pass_include=pass_include+add_plugin_list
   except J as e:
    B('Exception:%s',e)
    B(O())
   plugins=v(plugins)
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
    G('Except plugin : %s'%plugin_menu)
    continue
   G('plugin_name:%s',plugin_name)
   try:
    mod=__import__('%s'%(plugin_name),fromlist=[])
    try:
     mod_plugin_info=d(mod,'plugin_info') 
     if 'policy_point' in mod_plugin_info:
      if mod_plugin_info['policy_point']>f['config']['point']:
       continue
     if 'policy_level' in mod_plugin_info:
      if mod_plugin_info['policy_level']>f['config']['level']:
       continue
    except:
     G('no plugin_info : %s',plugin_name)
    mod_blue_print=d(mod,'blueprint')
    if mod_blue_print:
     if plugin_name in pass_include or is_include_menu(plugin_name):
      g(mod_blue_print)
    plugin_instance_list[plugin_name]=mod
   except J as e:
    B('Exception:%s',e)
    B(O())
    G('no blueprint')
  if not f['config']['run_by_worker']:
   try:
    L()
   except J as e:
    B('Exception:%s',e)
    B(O())
    G('db.create_all error')
  if not f['config']['run_by_real']:
   return
  for key,mod in c():
   try:
    G('### plugin_load start : %s',key)
    mod_plugin_load=d(mod,'plugin_load')
    if mod_plugin_load and(key in pass_include or is_include_menu(key)):
     mod.plugin_load()
    G('### plugin_load return : %s',key)
   except J as e:
    B('Exception:%s',e)
    B(O())
    G('no init_scheduler')
   try:
    mod_menu=d(mod,'menu')
    if mod_menu and(key in pass_include or is_include_menu(key)):
     s(mod_menu)
   except J as e:
    G('no menu')
  G('Plugin Log completed.. : %s ',x(plugin_instance_list))
 except J as e:
  B('Exception:%s',e)
  B(O())
def plugin_unload():
 for key,mod in c():
  try:
   mod_plugin_unload=d(mod,'plugin_unload')
   if mod_plugin_unload:
    mod.plugin_unload()
  except J as e:
   B('module:%s',key)
   B('Exception:%s',e)
   B(O())
 N()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
