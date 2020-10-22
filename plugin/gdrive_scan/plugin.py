import os
a=Exception
ru=str
import traceback
S=traceback.format_exc
import time
from datetime import datetime
import urllib
import json
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
E=session.query
p=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,path_app_root
O=scheduler.is_running
t=scheduler.is_include
P=db.session
from framework.util import Util,AlchemyEncoder
s=Util.db_list_to_dict
from system.logic import SystemLogic
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.model import ModelSetting
from.logic import Logic
rx=Logic.receive_scan_result
rJ=Logic.reset_db
rT=Logic.setting_save
ri=Logic.filelist
rX=Logic.scheduler_stop
rY=Logic.scheduler_start
rn=Logic.gdrive_delete
rR=Logic.gdrive_list
rS=Logic.gdrive_save
rN=Logic.plugin_unload
B=Logic.plugin_load
from.gdrive import GDrive,Auth
rL=Auth.make_token_cli
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'GDrive 스캔'],'sub':[['setting',u'설정'],['list',u'목록'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  B()
 except a as e:
  logger.error('Exception:%s',e) 
  logger.error(S())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  rN()
 except a as e:
  logger.error('Exception:%s',e)
  logger.error(S())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.E(ModelSetting).all()
  arg=s(setting_list)
  arg['is_include']=ru(t(package_name))
  arg['is_running']=ru(O(package_name))
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
   ret=rL(p['account_type'])
   logger.debug(ret)
   return jsonify(ret)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 elif sub=='gdrive_save':
  try:
   ret={}
   ret['ret']=rS(request)
   ret['gdrive_list']=rR()
   return jsonify(ret)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 elif sub=='load':
  try:
   ret={}
   ret['gdrive_list']=rR()
   return jsonify(ret)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 elif sub=='gdrive_delete':
  try:
   ret={}
   ret['ret']=rn(request)
   ret['gdrive_list']=rR()
   return jsonify(ret)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 elif sub=='scheduler':
  try:
   go=p['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    rY()
   else:
    rX()
   return jsonify(go)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return jsonify('fail')
 elif sub=='filelist':
  try:
   ret=ri(request)
   return jsonify(ret)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 elif sub=='setting_save':
  try:
   ret=rT(request)
   return jsonify(ret)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 elif sub=='reset_db':
  try:
   ret=rJ()
   return jsonify(ret)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return jsonify('fail')
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 if sub=='scan_completed':
  try:
   filename=p['filename']
   db_id=p['id']
   logger.debug('SCAN COMPLETED:%s %s',filename,db_id)
   rx(db_id,filename)
   return 'ok'
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
