import os
E=None
J=Exception
U=print
D=os.system
w=os.mkdir
k=os.path
from datetime import datetime,timedelta
from flask import request,abort
F=request.remote_addr
V=request.environ
r=request.args
Y=request.form
j=request.method
from functools import wraps
def check_api(original_function):
 @wraps(original_function)
 def wrapper_function(*args,**kwargs): 
  from framework import logger
  logger.debug('CHECK API... {}'.format(original_function.__module__))
  try:
   from system import ModelSetting as SystemModelSetting
   if SystemModelSetting.get_bool('auth_use_apikey'):
    if j=='POST':
     apikey=Y['apikey']
    else:
     apikey=r.get('apikey')
    if apikey is E or apikey!=SystemModelSetting.get('auth_apikey'):
     logger.debug('CHECK API : ABORT no match ({})'.format(apikey))
     logger.debug(V.get('HTTP_X_REAL_IP',F))
     abort(403)
     return 
  except J as e:
   U('Exception:%s',e)
   import traceback
   U(traceback.format_exc())
   logger.debug('CHECK API : ABORT exception')
   abort(403)
   return 
  return original_function(*args,**kwargs) 
 return wrapper_function
def make_default_dir(path_data):
 try:
  if not k.exists(path_data):
   w(path_data)
  tmp=k.join(path_data,'tmp')
  try:
   import shutil
   if k.exists(tmp):
    shutil.rmtree(tmp)
  except:
   pass
  sub=['db','log','download','bin','download_tmp','command','custom','output','upload','tmp']
  for item in sub:
   tmp=k.join(path_data,item)
   if not k.exists(tmp):
    w(tmp)
 except J as e:
  U('Exception:%s',e)
  import traceback
  U(traceback.format_exc())
def pip_install():
 from framework import app
 f=app.config
 U('pip_install start')
 try:
  import discord_webhook
  U('discord_webhook already installed..')
 except:
  try:
   D("{} install discord-webhook".format(f['config']['pip']))
   U('discord-webhook install..')
  except:
   U('discord-webhook fail..')
 U('pip_install end')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
