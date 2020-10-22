import os
E=None
P=Exception
D=print
B=os.system
z=os.mkdir
b=os.path
from datetime import datetime,timedelta
from flask import request,abort
v=request.remote_addr
I=request.environ
J=request.args
U=request.form
O=request.method
from functools import wraps
def check_api(original_function):
 @wraps(original_function)
 def wrapper_function(*args,**kwargs): 
  from framework import logger
  logger.debug('CHECK API... {}'.format(original_function.__module__))
  try:
   from system import ModelSetting as SystemModelSetting
   if SystemModelSetting.get_bool('auth_use_apikey'):
    if O=='POST':
     apikey=U['apikey']
    else:
     apikey=J.get('apikey')
    if apikey is E or apikey!=SystemModelSetting.get('auth_apikey'):
     logger.debug('CHECK API : ABORT no match ({})'.format(apikey))
     logger.debug(I.get('HTTP_X_REAL_IP',v))
     abort(403)
     return 
  except P as e:
   D('Exception:%s',e)
   import traceback
   D(traceback.format_exc())
   logger.debug('CHECK API : ABORT exception')
   abort(403)
   return 
  return original_function(*args,**kwargs) 
 return wrapper_function
def make_default_dir(path_data):
 try:
  if not b.exists(path_data):
   z(path_data)
  tmp=b.join(path_data,'tmp')
  try:
   import shutil
   if b.exists(tmp):
    shutil.rmtree(tmp)
  except:
   pass
  sub=['db','log','download','bin','download_tmp','command','custom','output','upload','tmp']
  for item in sub:
   tmp=b.join(path_data,item)
   if not b.exists(tmp):
    z(tmp)
 except P as e:
  D('Exception:%s',e)
  import traceback
  D(traceback.format_exc())
def pip_install():
 from framework import app
 e=app.config
 D('pip_install start')
 try:
  import discord_webhook
  D('discord_webhook already installed..')
 except:
  try:
   B("{} install discord-webhook".format(e['config']['pip']))
   D('discord-webhook install..')
  except:
   D('discord-webhook fail..')
 D('pip_install end')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
