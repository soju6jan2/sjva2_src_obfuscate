import os
A=None
D=Exception
m=print
from datetime import datetime,timedelta
from flask import request,abort
from functools import wraps
def check_api(original_function):
 @wraps(original_function)
 def wrapper_function(*args,**kwargs): 
  from framework import logger
  logger.debug('CHECK API... {}'.format(original_function.__module__))
  try:
   from system import ModelSetting as SystemModelSetting
   if SystemModelSetting.get_bool('auth_use_apikey'):
    if request.method=='POST':
     apikey=request.form['apikey']
    else:
     apikey=request.args.get('apikey')
    if apikey is A or apikey!=SystemModelSetting.get('auth_apikey'):
     logger.debug('CHECK API : ABORT no match ({})'.format(apikey))
     logger.debug(request.environ.get('HTTP_X_REAL_IP',request.remote_addr))
     abort(403)
     return 
  except D as exception:
   m('Exception:%s',exception)
   import traceback
   m(traceback.format_exc())
   logger.debug('CHECK API : ABORT exception')
   abort(403)
   return 
  return original_function(*args,**kwargs) 
 return wrapper_function
def make_default_dir(path_data):
 try:
  if not os.path.exists(path_data):
   os.mkdir(path_data)
  tmp=os.path.join(path_data,'tmp')
  try:
   import shutil
   if os.path.exists(tmp):
    shutil.rmtree(tmp)
  except:
   pass
  sub=['db','log','download','bin','download_tmp','command','custom','output','upload','tmp']
  for item in sub:
   tmp=os.path.join(path_data,item)
   if not os.path.exists(tmp):
    os.mkdir(tmp)
 except D as exception:
  m('Exception:%s',exception)
  import traceback
  m(traceback.format_exc())
def pip_install():
 from framework import app
 m('pip_install start')
 try:
  import discord_webhook
  m('discord_webhook already installed..')
 except:
  try:
   os.system("{} install discord-webhook".format(app.config['config']['pip']))
   m('discord-webhook install..')
  except:
   m('discord-webhook fail..')
 m('pip_install end')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
