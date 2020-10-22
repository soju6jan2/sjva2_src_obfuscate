import os
W=Exception
S=str
import traceback
import time
from datetime import datetime
import urllib
import json
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,path_app_root
from framework.util import Util,AlchemyEncoder
from system.logic import SystemLogic
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.model import ModelSetting
from.logic import Logic
from.gdrive import GDrive,Auth
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'GDrive 스캔'],'sub':[['setting',u'설정'],['list',u'목록'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  Logic.plugin_load()
 except W as e:
  logger.error('Exception:%s',e) 
  logger.error(traceback.format_exc())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  Logic.plugin_unload()
 except W as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.session.query(ModelSetting).all()
  arg=Util.db_list_to_dict(setting_list)
  arg['is_include']=S(scheduler.is_include(package_name))
  arg['is_running']=S(scheduler.is_running(package_name))
  return render_template('%s_setting.html'%package_name,sub=sub,arg=arg)
 elif sub=='list':
  return render_template('%s_list.html'%package_name)
 elif sub=='log':
  return render_template('log.html',package=package_name)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 if sub=='make_token':
  try:
   ret=Auth.make_token_cli(request.form['account_type'])
   logger.debug(ret)
   return jsonify(ret)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 elif sub=='gdrive_save':
  try:
   ret={}
   ret['ret']=Logic.gdrive_save(request)
   ret['gdrive_list']=Logic.gdrive_list()
   return jsonify(ret)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 elif sub=='load':
  try:
   ret={}
   ret['gdrive_list']=Logic.gdrive_list()
   return jsonify(ret)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 elif sub=='gdrive_delete':
  try:
   ret={}
   ret['ret']=Logic.gdrive_delete(request)
   ret['gdrive_list']=Logic.gdrive_list()
   return jsonify(ret)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 elif sub=='scheduler':
  try:
   go=request.form['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    Logic.scheduler_start()
   else:
    Logic.scheduler_stop()
   return jsonify(go)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return jsonify('fail')
 elif sub=='filelist':
  try:
   ret=Logic.filelist(request)
   return jsonify(ret)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 elif sub=='setting_save':
  try:
   ret=Logic.setting_save(request)
   return jsonify(ret)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 elif sub=='reset_db':
  try:
   ret=Logic.reset_db()
   return jsonify(ret)
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return jsonify('fail')
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 if sub=='scan_completed':
  try:
   filename=request.form['filename']
   db_id=request.form['id']
   logger.debug('SCAN COMPLETED:%s %s',filename,db_id)
   Logic.receive_scan_result(db_id,filename)
   return 'ok'
  except W as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
