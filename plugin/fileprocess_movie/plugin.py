import os
l=Exception
xr=str
import traceback
c=traceback.format_exc
import time
from datetime import datetime
import urllib
import json
import threading
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
xO=session.query
xC=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio
t=scheduler.is_running
f=scheduler.is_include
R=db.session
from framework.util import Util,AlchemyEncoder
xP=Util.db_list_to_dict
from system.logic import SystemLogic
from.model import ModelSetting
from.logic import Logic
xe=Logic.reset_db
xi=Logic.one_execute
xp=Logic.filelist
xL=Logic.scheduler_stop
xA=Logic.scheduler_start
xK=Logic.setting_save
xv=Logic.plugin_unload
xc=Logic.plugin_load
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'영화'],'sub':[['setting',u'설정'],['list',u'목록'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  xc()
 except l as e:
  logger.error('Exception:%s',e)
  logger.error(c())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  xv()
 except l as e:
  logger.error('Exception:%s',e)
  logger.error(c())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.xO(ModelSetting).all()
  arg=xP(setting_list)
  arg['scheduler']=xr(f(package_name))
  arg['is_running']=xr(t(package_name))
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
   ret=xK(request)
   return jsonify(ret)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 elif sub=='scheduler':
  try:
   go=xC['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    xA()
   else:
    xL()
   return jsonify(go)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
   return jsonify('fail')
 elif sub=='filelist':
  try:
   ret=xp(request)
   return jsonify(ret)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 elif sub=='one_execute':
  try:
   ret=xi()
   return jsonify(ret)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
   return jsonify('fail')
 elif sub=='reset_db':
  try:
   ret=xe()
   return jsonify(ret)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c()) 
# Created by pyminifier (https://github.com/liftoff/pyminifier)
