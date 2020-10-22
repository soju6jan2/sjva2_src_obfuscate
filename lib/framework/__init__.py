version='0.2.16.30'
s=False
U=True
M=len
w=int
u=Exception
import os
import sys
path_app_root=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_data=os.path.join(path_app_root,'data')
flag_system_loading=s
from datetime import datetime,timedelta
import json
import traceback
from flask import Flask,redirect,render_template,Response,request,jsonify,send_file,send_from_directory,abort,Markup
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,emit 
from flask_login import LoginManager
from flask_login import login_user,logout_user,current_user,login_required
if sys.version_info[0]==2:
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
 app.secret_key=os.urandom(24)
 app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data/db/sjva.db?check_same_thread=False'
 app.config['SQLALCHEMY_BINDS']={'sjva':'sqlite:///data/db/sjva.db'}
 app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=s
 app.config['config']={}
 logger.debug('======================================')
 logger.debug(sys.argv)
 app.config['config']['run_by_real']=U if sys.argv[0]=='sjva.py' else s
 app.config['config']['run_by_migration']=U if sys.argv[-2]=='db' else s
 app.config['config']['run_by_worker']=U if sys.argv[0].find('celery')!=-1 else s
 app.config['config']['run_by_init_db']=U if sys.argv[-1]=='init_db' else s
 if sys.version_info[0]==2:
  app.config['config']['pip']='pip'
  app.config['config']['is_py2']=U
  app.config['config']['is_py3']=s
 else:
  app.config['config']['is_py2']=s
  app.config['config']['is_py3']=U
  app.config['config']['pip']='pip3'
 pip_install()
 db=SQLAlchemy(app,session_options={"autoflush":s})
 scheduler=Scheduler()
 socketio=SocketIO(app,cors_allowed_origins="*")
 login_manager=LoginManager()
 login_manager.init_app(app)
 login_manager.login_view="login"
 exit_code=-1
 from.log_viewer import*
 from.manual import*
 USERS={"sjva"+version:User("sjva"+version,passwd_hash="sjva"+version),}
 app.config['config']['is_debug']=s
 app.config['config']['repeat']=-1
 if app.config['config']['run_by_real']:
  if M(sys.argv)>2:
   app.config['config']['repeat']=w(sys.argv[2])
 if M(sys.argv)>3:
  app.config['config']['is_debug']=(sys.argv[-1]=='debug')
 app.config['config']['use_celery']=U
 for tmp in sys.argv:
  if tmp=='no_celery':
   app.config['config']['use_celery']=s
   break
 logger.debug('use_celery : %s',app.config['config']['use_celery'])
 logger.debug('======================================')
 from.init_celery import celery
 import framework.common.celery
 import system
 from system.model import ModelSetting as SystemModelSetting
 try:
  db.create_all()
 except u as e:
  logger.error('CRITICAL db.create_all()!!!')
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
 from system.logic_auth import SystemLogicAuth
 tmp=SystemLogicAuth.get_auth_status()
 app.config['config']['auth_status']=tmp['ret']
 app.config['config']['auth_desc']=tmp['desc']
 app.config['config']['level']=tmp['level']
 app.config['config']['point']=tmp['point']
 system.plugin_load()
 flag_system_loading=U 
 if app.config['config']['run_by_init_db']:
  logger.debug('================================================')
  logger.debug('Run by init db.. exit')
  sys.exit()
 app.register_blueprint(system.blueprint)
 try:
  if SystemModelSetting.get('ddns').find('sjva-server.soju6jan.com')!=-1:
   app.config['config']['is_sjva_server']=U
   app.config['config']['is_server']=U
   app.config['config']['is_admin']=U
  else:
   app.config['config']['is_sjva_server']=s
   app.config['config']['is_server']=s
   app.config['config']['is_admin']=s
  app.config['config']['rss_subtitle_webhook']='https://discordapp.com/api/webhooks/689800985887113329/GBTUBpP9L0dOegqL4sH-u1fwpssPKq0gBOGPb50JQjim22gUqskYCtj-wnup6BsY3vvc'
 except:
  app.config['config']['is_sjva_server']=s
  app.config['config']['is_server']=s
 if app.config['config']['is_sjva_server']or app.config['config']['is_debug']or SystemModelSetting.get('ddns').find('sjva-dev.soju6jan.com')!=-1:
  app.config['config']['server']=U
  app.config['config']['is_admin']=U
 else:
  app.config['config']['server']=s
  app.config['config']['is_admin']=s
 app.config['config']['running_type']='native'
 if 'SJVA_RUNNING_TYPE' in os.environ:
  app.config['config']['running_type']=os.environ['SJVA_RUNNING_TYPE']
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
 if sys.argv[0]=='sjva.py':
  try:
   app.config['config']['port']=SystemModelSetting.get_int('port')
   if app.config['config']['port']==19999 and app.config['config']['running_type']=='docker' and not os.path.exists('/usr/sbin/nginx'):
    SystemModelSetting.set('port','9999')
    app.config['config']['port']=9999
  except:
   app.config['config']['port']=9999
  logger.debug('PORT:%s',app.config['config']['port'])
 logger.debug('### LAST')
except u as e:
 logger.error('Exception:%s',e)
 logger.error(traceback.format_exc())
from.init_route import*
# Created by pyminifier (https://github.com/liftoff/pyminifier)
