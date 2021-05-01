version='0.2.20.2'
import os
import sys
import platform
path_app_root=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_data=os.path.join(path_app_root,'data')
flag_system_loading=False
from datetime import datetime,timedelta
import json
import traceback
from flask import Flask,redirect,render_template,Response,request,jsonify,send_file,send_from_directory,abort,Markup
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,emit 
from flask_login import LoginManager,login_user,logout_user,current_user,login_required
from.init_args import args
from.py_version_func import*
from framework.class_scheduler import Scheduler
from framework.logger import get_logger
from.menu import init_menu
from.user import User
from.init_web import jinja_initialize
from.init_etc import check_api,make_default_dir,pip_install,config_initialize
make_default_dir(path_data)
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
try:
 logger.debug('Path app root : %s',path_app_root) 
 logger.debug('Path app data : %s',path_data)
 logger.debug('Platform : %s',platform.system())
 app=Flask('sjva')
 app.secret_key=os.urandom(24)
 app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data/db/sjva.db?check_same_thread=False'
 app.config['SQLALCHEMY_BINDS']={'sjva':'sqlite:///data/db/sjva.db'}
 app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
 app.config['config']={}
 config_initialize('start')
 pip_install()
 db=SQLAlchemy(app,session_options={"autoflush":False})
 scheduler=Scheduler(args)
 if args is not None and args.use_gevent==False:
  socketio=SocketIO(app,cors_allowed_origins="*",async_mode='threading')
 else:
  socketio=SocketIO(app,cors_allowed_origins="*")
 from flask_cors import CORS
 CORS(app)
 login_manager=LoginManager()
 login_manager.init_app(app)
 login_manager.login_view="login"
 exit_code=-1
 from.log_viewer import*
 from.manual import*
 USERS={"sjva"+version:User("sjva"+version,passwd_hash="sjva"+version),}
 from.init_celery import celery
 import framework.common.celery
 import system
 from system.model import ModelSetting as SystemModelSetting
 try:
  db.create_all()
 except Exception as exception:
  logger.error('CRITICAL db.create_all()!!!')
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
 config_initialize('auth')
 system.plugin_load()
 flag_system_loading=True 
 if app.config['config']['run_by_init_db']:
  logger.debug('================================================')
  logger.debug('Run by init db.. exit')
  sys.exit()
 app.register_blueprint(system.blueprint)
 config_initialize('system_loading_after')
 plugin_menu=[]
 plugin_menu.append(system.menu)
 plugin_instance_list={}
 jinja_initialize(app)
 system.LogicPlugin.custom_plugin_update()
 from.init_plugin import plugin_init
 plugin_init()
 logger.debug('### plugin loading completed') 
 init_menu(plugin_menu)
 system.SystemLogic.apply_menu_link()
 logger.debug('### menu loading completed')
 app.config['config']['port']=0
 if sys.argv[0]=='sjva.py' or sys.argv[0]=='sjva3.py':
  try:
   app.config['config']['port']=SystemModelSetting.get_int('port')
   if app.config['config']['port']==19999 and app.config['config']['running_type']=='docker' and not os.path.exists('/usr/sbin/nginx'):
    SystemModelSetting.set('port','9999')
    app.config['config']['port']=9999
  except:
   app.config['config']['port']=9999
 if args is not None:
  if args.port is not None:
   app.config['config']['port']=args.port
  app.config['config']['repeat']=args.repeat 
  app.config['config']['use_celery']=args.use_celery
  if platform.system()=='Windows':
   app.config['config']['use_celery']=False
  app.config['config']['use_gevent']=args.use_gevent
 logger.debug('### config ###')
 logger.debug(json.dumps(app.config['config'],indent=4))
 logger.debug('### LAST')
 logger.debug('### PORT:%s',app.config['config']['port'])
 logger.debug('### Now you can access SJVA by webbrowser!!')
except Exception as exception:
 logger.error('Exception:%s',exception)
 logger.error(traceback.format_exc())
from.init_route import*
from.util import Util
try:
 from tool_expand import TorrentProcess
 TorrentProcess.server_process(None,category='None')
except:
 pass
"""
try:
    from lib_metadata import *
except:
    pass
"""
# Created by pyminifier (https://github.com/liftoff/pyminifier)
