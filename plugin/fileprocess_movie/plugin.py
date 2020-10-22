import os
i=Exception
oU=str
import traceback
B=traceback.format_exc
import time
from datetime import datetime
import urllib
import json
import threading
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
oW=session.query
oF=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio
c=scheduler.is_running
l=scheduler.is_include
g=db.session
from framework.util import Util,AlchemyEncoder
ow=Util.db_list_to_dict
from system.logic import SystemLogic
from.model import ModelSetting
from.logic import Logic
ov=Logic.reset_db
oL=Logic.one_execute
oP=Logic.filelist
ok=Logic.scheduler_stop
oy=Logic.scheduler_start
oT=Logic.setting_save
oj=Logic.plugin_unload
oB=Logic.plugin_load
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'영화'],'sub':[['setting',u'설정'],['list',u'목록'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  oB()
 except i as e:
  logger.error('Exception:%s',e)
  logger.error(B())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  oj()
 except i as e:
  logger.error('Exception:%s',e)
  logger.error(B())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.oW(ModelSetting).all()
  arg=ow(setting_list)
  arg['scheduler']=oU(l(package_name))
  arg['is_running']=oU(c(package_name))
  return render_template('%s_%s.html'%(package_name,sub),arg=arg)
 elif sub=='list':
  arg={}
  return render_template('%s_%s.html'%(package_name,sub),arg=arg)
 elif sub=='log':
  return render_template('log.html',package=package_name)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 if sub=='setting_save':
  try:
   ret=oT(request)
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 elif sub=='scheduler':
  try:
   go=oF['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    oy()
   else:
    ok()
   return jsonify(go)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
   return jsonify('fail')
 elif sub=='filelist':
  try:
   ret=oP(request)
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 elif sub=='one_execute':
  try:
   ret=oL()
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
   return jsonify('fail')
 elif sub=='reset_db':
  try:
   ret=ov()
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B()) 
# Created by pyminifier (https://github.com/liftoff/pyminifier)
