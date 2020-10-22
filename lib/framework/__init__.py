version='0.2.16.30'
Y=False
f=True
i=len
R=int
P=Exception
import os
u=os.environ
F=os.urandom
b=os.path
import sys
q=sys.exit
r=sys.argv
g=sys.version_info
path_app_root=b.dirname(b.dirname(b.dirname(b.abspath(__file__))))
path_data=b.join(path_app_root,'data')
flag_system_loading=Y
from datetime import datetime,timedelta
import json
import traceback
t=traceback.format_exc
from flask import Flask,redirect,render_template,Response,request,jsonify,send_file,send_from_directory,abort,Markup
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,emit 
from flask_login import LoginManager
from flask_login import login_user,logout_user,current_user,login_required
if g[0]==2:
 import Queue as py_queue
 import urllib2 as py_urllib2 
 import urllib as py_urllib 
else:
 import queue as py_queue
 import urllib.request as py_urllib2
 import urllib.parse as py_urllib 
from framework.class_scheduler import Scheduler
from framework.logger import get_logger
from framework.menu import get_menu_map,init_menu,get_plugin_menu
from.user import User
from.init_web import get_menu,get_theme,get_login_status,get_web_title
from.init_etc import check_api,make_default_dir,pip_install
make_default_dir(path_data)
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
try:
 logger.debug('Path app root : %s',path_app_root) 
 logger.debug('Path app data : %s',path_data)
 import platform
 logger.debug('Platform : %s',platform.system())
 app=Flask('sjva')
 try:
  from flask_restful import Api
  api=Api(app)
 except:
  logger.debug('NOT INSTALLED FLASK_RESTFUL')
 app.secret_key=F(24)
 app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data/db/sjva.db?check_same_thread=False'
 app.config['SQLALCHEMY_BINDS']={'sjva':'sqlite:///data/db/sjva.db'}
 app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=Y
 app.config['config']={}
 logger.debug('======================================')
 logger.debug(r)
 app.config['config']['run_by_real']=f if r[0]=='sjva.py' else Y
 app.config['config']['run_by_migration']=f if r[-2]=='db' else Y
 app.config['config']['run_by_worker']=f if r[0].find('celery')!=-1 else Y
 app.config['config']['run_by_init_db']=f if r[-1]=='init_db' else Y
 if g[0]==2:
  app.config['config']['pip']='pip'
  app.config['config']['is_py2']=f
  app.config['config']['is_py3']=Y
 else:
  app.config['config']['is_py2']=Y
  app.config['config']['is_py3']=f
  app.config['config']['pip']='pip3'
 pip_install()
 db=SQLAlchemy(app,session_options={"autoflush":Y})
 scheduler=Scheduler()
 socketio=SocketIO(app,cors_allowed_origins="*")
 login_manager=LoginManager()
 login_manager.init_app(app)
 login_manager.login_view="login"
 exit_code=-1
 from.log_viewer import*
 from.manual import*
 USERS={"sjva"+version:User("sjva"+version,passwd_hash="sjva"+version),}
 app.config['config']['is_debug']=Y
 app.config['config']['repeat']=-1
 if app.config['config']['run_by_real']:
  if i(r)>2:
   app.config['config']['repeat']=R(r[2])
 if i(r)>3:
  app.config['config']['is_debug']=(r[-1]=='debug')
 app.config['config']['use_celery']=f
 for tmp in r:
  if tmp=='no_celery':
   app.config['config']['use_celery']=Y
   break
 logger.debug('use_celery : %s',app.config['config']['use_celery'])
 logger.debug('======================================')
 from.init_celery import celery
 import framework.common.celery
 import system
 from system.model import ModelSetting as SystemModelSetting
 try:
  db.create_all()
 except P as e:
  logger.error('CRITICAL db.create_all()!!!')
  logger.error('Exception:%s',e)
  logger.error(t())
 from system.logic_auth import SystemLogicAuth
 tmp=SystemLogicAuth.get_auth_status()
 app.config['config']['auth_status']=tmp['ret']
 app.config['config']['auth_desc']=tmp['desc']
 app.config['config']['level']=tmp['level']
 app.config['config']['point']=tmp['point']
 system.plugin_load()
 flag_system_loading=f 
 if app.config['config']['run_by_init_db']:
  logger.debug('================================================')
  logger.debug('Run by init db.. exit')
  q()
 app.register_blueprint(system.blueprint)
 try:
  if SystemModelSetting.get('ddns').find('sjva-server.soju6jan.com')!=-1:
   app.config['config']['is_sjva_server']=f
   app.config['config']['is_server']=f
   app.config['config']['is_admin']=f
  else:
   app.config['config']['is_sjva_server']=Y
   app.config['config']['is_server']=Y
   app.config['config']['is_admin']=Y
  app.config['config']['rss_subtitle_webhook']='https://discordapp.com/api/webhooks/689800985887113329/GBTUBpP9L0dOegqL4sH-u1fwpssPKq0gBOGPb50JQjim22gUqskYCtj-wnup6BsY3vvc'
 except:
  app.config['config']['is_sjva_server']=Y
  app.config['config']['is_server']=Y
 if app.config['config']['is_sjva_server']or app.config['config']['is_debug']or SystemModelSetting.get('ddns').find('sjva-dev.soju6jan.com')!=-1:
  app.config['config']['server']=f
  app.config['config']['is_admin']=f
 else:
  app.config['config']['server']=Y
  app.config['config']['is_admin']=Y
 app.config['config']['running_type']='native'
 if 'SJVA_RUNNING_TYPE' in u:
  app.config['config']['running_type']=u['SJVA_RUNNING_TYPE']
 """
    if app.config['config']['run_by_real']:
        import flaskfilemanager
        app.config['FLASKFILEMANAGER_FILE_PATH'] = r'/'
        flaskfilemanager.init(app)
    """ 
 plugin_menu=[]
 plugin_menu.append(system.menu)
 plugin_instance_list={}
 app.jinja_env.globals.update(get_menu=get_menu)
 app.jinja_env.globals.update(get_theme=get_theme)
 app.jinja_env.globals.update(get_menu_map=get_menu_map)
 app.jinja_env.globals.update(get_login_status=get_login_status)
 app.jinja_env.globals.update(get_web_title=get_web_title)
 app.jinja_env.globals.update(get_plugin_menu=get_plugin_menu)
 app.jinja_env.filters['get_menu']=get_menu
 app.jinja_env.filters['get_theme']=get_theme
 app.jinja_env.filters['get_menu_map']=get_menu_map
 app.jinja_env.filters['get_login_status']=get_login_status
 app.jinja_env.filters['get_web_title']=get_web_title
 app.jinja_env.filters['get_plugin_menu']=get_plugin_menu
 app.jinja_env.add_extension('jinja2.ext.loopcontrols')
 system.LogicPlugin.custom_plugin_update()
 from.init_plugin import plugin_init
 plugin_init()
 logger.debug('### plugin loading completed') 
 init_menu(plugin_menu)
 system.SystemLogic.apply_menu_link()
 logger.debug('### menu loading completed')
 if r[0]=='sjva.py':
  try:
   app.config['config']['port']=SystemModelSetting.get_int('port')
   if app.config['config']['port']==19999 and app.config['config']['running_type']=='docker' and not b.exists('/usr/sbin/nginx'):
    SystemModelSetting.set('port','9999')
    app.config['config']['port']=9999
  except:
   app.config['config']['port']=9999
  logger.debug('PORT:%s',app.config['config']['port'])
 logger.debug('### LAST')
except P as e:
 logger.error('Exception:%s',e)
 logger.error(t())
from.init_route import*
# Created by pyminifier (https://github.com/liftoff/pyminifier)
