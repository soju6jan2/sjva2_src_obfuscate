import os
U=Exception
WC=str
import traceback
i=traceback.format_exc
import time
from datetime import datetime
import urllib
import json
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
t=session.query
y=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,path_app_root
Y=scheduler.is_running
j=scheduler.is_include
G=db.session
from framework.util import Util,AlchemyEncoder
O=Util.db_list_to_dict
from system.logic import SystemLogic
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.model import ModelSetting
from.logic import Logic
WD=Logic.receive_scan_result
Wp=Logic.reset_db
WP=Logic.setting_save
Ws=Logic.filelist
WT=Logic.scheduler_stop
WJ=Logic.scheduler_start
WR=Logic.gdrive_delete
Wk=Logic.gdrive_list
Wi=Logic.gdrive_save
WN=Logic.plugin_unload
F=Logic.plugin_load
from.gdrive import GDrive,Auth
Wu=Auth.make_token_cli
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'GDrive 스캔'],'sub':[['setting',u'설정'],['list',u'목록'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  F()
 except U as e:
  logger.error('Exception:%s',e) 
  logger.error(i())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  WN()
 except U as e:
  logger.error('Exception:%s',e)
  logger.error(i())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.t(ModelSetting).all()
  arg=O(setting_list)
  arg['is_include']=WC(j(package_name))
  arg['is_running']=WC(Y(package_name))
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
   ret=Wu(y['account_type'])
   logger.debug(ret)
   return jsonify(ret)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 elif sub=='gdrive_save':
  try:
   ret={}
   ret['ret']=Wi(request)
   ret['gdrive_list']=Wk()
   return jsonify(ret)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 elif sub=='load':
  try:
   ret={}
   ret['gdrive_list']=Wk()
   return jsonify(ret)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 elif sub=='gdrive_delete':
  try:
   ret={}
   ret['ret']=WR(request)
   ret['gdrive_list']=Wk()
   return jsonify(ret)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 elif sub=='scheduler':
  try:
   go=y['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    WJ()
   else:
    WT()
   return jsonify(go)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return jsonify('fail')
 elif sub=='filelist':
  try:
   ret=Ws(request)
   return jsonify(ret)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 elif sub=='setting_save':
  try:
   ret=WP(request)
   return jsonify(ret)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 elif sub=='reset_db':
  try:
   ret=Wp()
   return jsonify(ret)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return jsonify('fail')
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 if sub=='scan_completed':
  try:
   filename=y['filename']
   db_id=y['id']
   logger.debug('SCAN COMPLETED:%s %s',filename,db_id)
   WD(db_id,filename)
   return 'ok'
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
