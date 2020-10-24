import os
P=Exception
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
from framework import app,db,scheduler,path_data,socketio
from framework.util import Util,AlchemyEncoder
from system.logic import SystemLogic
from.model import ModelSetting
from.logic import Logic
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'Daum TV'],'sub':[['list',u'목록'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  Logic.plugin_load()
 except P as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  Logic.plugin_unload()
 except P as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='list':
  return render_template('%s_list.html'%package_name)
 elif sub=='log':
  return render_template('log.html',package=package_name)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 if sub=='db_list':
  try:
   ret=Logic.db_list(request)
   return jsonify(ret)
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 elif sub=='refresh':
  try:
   ret=Logic.refresh(request)
   return jsonify(ret)
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
