import os
g=Exception
import traceback
C=traceback.format_exc
import time
from datetime import datetime
import urllib
import json
e=json.dumps
J=json.loads
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
m=session.query
Y=request.args
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,SystemModelSetting
B=db.session
from framework.util import Util,AlchemyEncoder
N=Util.db_list_to_dict
from system.logic import SystemLogic
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.model import ModelSetting
from.logic import Logic
xI=Logic.plungin_command
xt=Logic.analyze_show_data
xw=Logic.get_server_hash
xJ=Logic.load_section_list
xC=Logic.analyze_show
d=Logic.get_sj_daum_version
o=Logic.get_sjva_plugin_version
T=Logic.connect_plex_server_by_url
S=Logic.connect_plex_server_by_name
F=Logic.setting_save
U=Logic.get_plex_server_list
O=Logic.db_default
Q=Logic.plugin_unload
V=Logic.plugin_load
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'PLEX'],'sub':[['setting',u'설정'],['plugin',u'플러그인'],['tool',u'툴'],['tivimate',u'Tivimate'],['lc',u'Live Channels'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  V()
 except g as e:
  logger.error('Exception:%s',e)
  logger.error(C())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  Q()
 except g as e:
  logger.error('Exception:%s',e)
  logger.error(C())
last_data={}
@blueprint.route('/')
def home():
 return redirect('/%s/setting'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.m(ModelSetting).all()
  arg=N(setting_list)
  return render_template('plex_setting.html',sub=sub,arg=arg)
 elif sub=='plugin':
  setting_list=db.m(ModelSetting).all()
  arg=N(setting_list)
  return render_template('plex_plugin.html',sub=sub,arg=arg)
 elif sub=='tool':
  return render_template('plex_tool.html')
 elif sub=='lc':
  setting_list=db.m(ModelSetting).all()
  arg=N(setting_list)
  try:
   if arg['lc_json']=='':
    arg['lc_json']="[]"
   tmp=J(arg['lc_json'])
   arg['lc_json']=e(tmp,indent=4)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
   arg['lc_json']=O['lc_json']
   tmp=J(arg['lc_json'])
   arg['lc_json']=e(tmp,indent=4)
  return render_template('plex_lc.html',arg=arg)
 elif sub=='tivimate':
  setting_list=db.m(ModelSetting).all()
  arg=N(setting_list)
  try:
   if arg['tivimate_json']=='':
    arg['tivimate_json']="[]"
   tmp=J(arg['tivimate_json'])
   arg['tivimate_json']=e(tmp,indent=4)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
   arg['tivimate_json']=O['tivimate_json']
   tmp=J(arg['tivimate_json'])
   arg['tivimate_json']=e(tmp,indent=4)
  return render_template('plex_tivimate.html',arg=arg) 
 elif sub=='log':
  return render_template('log.html',package=package_name)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 if sub=='server_list':
  try:
   ret=U(request)
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='setting_save':
  try:
   ret=F(request)
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='connect_by_name':
  try:
   ret=S(request)
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='connect_by_url':
  try:
   ret=T(request)
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='get_sjva_version':
  try:
   ret=o(request)
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C()) 
 elif sub=='get_sj_daum_version':
  try:
   ret=d(request)
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C()) 
 elif sub=='analyze_show':
  try:
   ret=xC(request)
   last_data['analyze_show']=ret
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='analyze_show_event':
  try:
   key=Y.get('key')
   return Response(xC(key),mimetype="text/event-stream")
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='load_tool':
  try:
   last_data['sections']=xJ()
   last_data['plex_server_hash']=xw()
   last_data['analyze_show']=xt
   return jsonify(last_data)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='send_command':
  try:
   ret=xI(request)
   return jsonify(ret)
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 if sub=='m3u' or sub=='get.php':
  try:
   from.logic_m3u import LogicM3U
   return LogicM3U.make_m3u()[0]
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
 elif sub=='xml' or sub=='xmltv.php':
  try:
   from.logic_m3u import LogicM3U
   data=LogicM3U.make_m3u()[1]
   return Response(data,mimetype='application/xml')
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(C())
@blueprint.route('/get.php')
def get_php():
 logger.debug('xtream codes server')
 logger.debug(Y)
 return redirect('/plex/api/m3u')
@blueprint.route('/xmltv.php')
def xmltv_php():
 logger.debug('xtream codes server xmltv')
 logger.debug(Y)
 return redirect('/plex/api/xml')
@blueprint.route('/player_api.php')
def player_api():
 pass
@blueprint.route('/login')
def login():
 logger.debug('xtream codes login')
 logger.debug(Y)
 return jsonify('')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
