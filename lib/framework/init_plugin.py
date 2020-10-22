import os
f=True
Y=False
P=Exception
m=sorted
l=getattr
i=len
j=os.listdir
b=os.path
import sys
d=sys.path
import traceback
t=traceback.format_exc
from framework import app,db,logger,plugin_instance_list,plugin_menu
x=plugin_menu.append
C=plugin_instance_list.items
M=logger.debug
o=logger.error
X=db.create_all
k=app.register_blueprint
e=app.config
import system
s=system.plugin_unload
n=system.SystemLogic
def is_include_menu(plugin_name):
 try:
  if plugin_name not in['daum_tv','ffmpeg','fileprocess_movie','gdrive_scan','ktv','plex','rclone']:
   return f
  if n.get_setting_value('use_plugin_%s'%plugin_name)=='True':
   return f
  elif n.get_setting_value('use_plugin_%s'%plugin_name)=='False':
   return Y
 except P as e:
  o('Exception:%s',e)
  o(t()) 
 return f
def plugin_init():
 try:
  if not e['config']['auth_status']:
   return
  import inspect
  plugin_path=b.join(b.dirname(b.dirname(b.dirname(b.abspath(__file__)))),'plugin')
  d.insert(0,plugin_path)
  plugins=j(plugin_path)
  pass_include=[]
  except_plugin_list=[]
  if e['config']['run_by_migration']==Y:
   if e['config']['server']or e['config']['is_debug']:
    server_plugin_path=b.join(b.dirname(b.dirname(b.dirname(b.abspath(__file__)))),'server')
    if b.exists(server_plugin_path):
     d.insert(0,server_plugin_path)
     plugins=plugins+j(server_plugin_path)
     pass_include=pass_include+j(server_plugin_path)
   try:
    server_plugin_path=b.join(b.dirname(b.dirname(b.dirname(b.abspath(__file__)))),'data','custom')
    d.append(server_plugin_path)
    tmps=j(server_plugin_path)
    add_plugin_list=[]
    for t in tmps:
     if not t.startswith('_'):
      add_plugin_list.append(t)
    plugins=plugins+add_plugin_list
    pass_include=pass_include+add_plugin_list
   except P as e:
    o('Exception:%s',e)
    o(t())
   try:
    server_plugin_path=n.get_setting_value('plugin_dev_path')
    if server_plugin_path!='':
     if b.exists(server_plugin_path):
      d.append(server_plugin_path)
      tmps=j(server_plugin_path)
      add_plugin_list=[]
      for t in tmps:
       if not t.startswith('_'):
        add_plugin_list.append(t)
        if e['config']['level']<=4:
         break
      plugins=plugins+add_plugin_list
      pass_include=pass_include+add_plugin_list
   except P as e:
    o('Exception:%s',e)
    o(t())
   plugins=m(plugins)
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
    M('Except plugin : %s'%plugin_menu)
    continue
   M('plugin_name:%s',plugin_name)
   try:
    mod=__import__('%s'%(plugin_name),fromlist=[])
    try:
     mod_plugin_info=l(mod,'plugin_info') 
     if 'policy_point' in mod_plugin_info:
      if mod_plugin_info['policy_point']>e['config']['point']:
       continue
     if 'policy_level' in mod_plugin_info:
      if mod_plugin_info['policy_level']>e['config']['level']:
       continue
    except:
     M('no plugin_info : %s',plugin_name)
    mod_blue_print=l(mod,'blueprint')
    if mod_blue_print:
     if plugin_name in pass_include or is_include_menu(plugin_name):
      k(mod_blue_print)
    plugin_instance_list[plugin_name]=mod
   except P as e:
    o('Exception:%s',e)
    o(t())
    M('no blueprint')
  if not e['config']['run_by_worker']:
   try:
    X()
   except P as e:
    o('Exception:%s',e)
    o(t())
    M('db.create_all error')
  if not e['config']['run_by_real']:
   return
  for key,mod in C():
   try:
    M('### plugin_load start : %s',key)
    mod_plugin_load=l(mod,'plugin_load')
    if mod_plugin_load and(key in pass_include or is_include_menu(key)):
     mod.plugin_load()
    M('### plugin_load return : %s',key)
   except P as e:
    o('Exception:%s',e)
    o(t())
    M('no init_scheduler')
   try:
    mod_menu=l(mod,'menu')
    if mod_menu and(key in pass_include or is_include_menu(key)):
     x(mod_menu)
   except P as e:
    M('no menu')
  M('Plugin Log completed.. : %s ',i(plugin_instance_list))
 except P as e:
  o('Exception:%s',e)
  o(t())
def plugin_unload():
 for key,mod in C():
  try:
   mod_plugin_unload=l(mod,'plugin_unload')
   if mod_plugin_unload:
    mod.plugin_unload()
  except P as e:
   o('module:%s',key)
   o('Exception:%s',e)
   o(t())
 s()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
