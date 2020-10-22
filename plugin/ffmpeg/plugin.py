import os
u=str
f=Exception
A=None
g=os.makedirs
P=os.path
import traceback
N=traceback.format_exc
import time
from datetime import datetime
r=datetime.now
from pytz import timezone
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory
v=session.query
e=request.args
i=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework import app,db,scheduler,path_app_root,socketio,path_data
Q=socketio.on
c=db.session
from framework.logger import get_logger
from framework.util import Util
PI=Util.db_list_to_dict
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from ffmpeg.logic import Logic
PB=Logic.get_setting_value
PN=Logic.setting_save
W=Logic.path_ffmpeg
PT=Logic.plugin_unload
Pp=Logic.plugin_load
from ffmpeg.model import ModelSetting
from ffmpeg.interface_program_ffmpeg import Ffmpeg
PS=Ffmpeg.get_ffmpeg_by_caller
PL=Ffmpeg.instance_list
Ph=Ffmpeg.ffmpeg_by_idx
PG=Ffmpeg.stop_by_idx
PU=Ffmpeg.get_version
from system.model import ModelSetting as SystemModelSetting
Po=SystemModelSetting.get
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'FFMPEG'],'sub':[['setting',u'설정'],['download',u'다운로드'],['list',u'목록'],['log',u'로그'],]}
def plugin_load():
 Pp() 
def plugin_unload():
 PT() 
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 if sub=='setting':
  setting_list=db.v(ModelSetting).all()
  arg=PI(setting_list)
  arg['ffmpeg_path']=W
  return render_template('plugin_ffmpeg.html',sub=sub,arg=arg)
 elif sub=='download':
  now=u(r(timezone('Asia/Seoul'))).replace(':','').replace('-','').replace(' ','-')
  return render_template('plugin_ffmpeg.html',sub=sub,arg=('%s'%now).split('.')[0]+'.mp4')
 elif sub=='list':
  return render_template('plugin_ffmpeg_list2.html')
 elif sub=='log':
  logger.debug(package_name)
  return render_template('log.html',package=package_name)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 try: 
  if sub=='setting_save':
   try:
    ret=PN(request)
    return jsonify(ret)
   except f as e:
    logger.error('Exception:%s',e)
    logger.error(N())
  elif sub=='ffmpeg_version':
   ret=PU()
   return jsonify(ret)
  elif sub=='download':
   url=i['url']
   filename=i['filename']
   ffmpeg=Ffmpeg(url,filename,call_plugin=package_name)
   data=ffmpeg.start()
   return jsonify([])
  elif sub=='stop':
   idx=i['idx']
   PG(idx)
   return jsonify([])
  elif sub=='play':
   idx=i['idx']
   ffmpeg=Ph(idx)
   tmp=ffmpeg.save_fullpath.replace(path_app_root,'')
   tmp=tmp.replace('\\','/')
   logger.debug('play : %s',tmp)
   return jsonify(tmp)
  elif sub=='list':
   ret=[]
   for ffmpeg in PL:
    ret.append(ffmpeg.get_data())
   return jsonify(ret)
 except f as e:
  logger.error('Exception:%s',e)
  logger.error(N())
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 sjva_token=e.get('token')
 if sjva_token!=Po('unique'):
  ret={}
  ret['ret']='wrong_token'
  return jsonify(ret)
 if sub=='download':
  ret={}
  try:
   max_pf_count=PB('max_pf_count')
   url=e.get('url')
   filename=e.get('filename')
   caller_id=e.get('id')
   package_name=e.get('caller')
   save_path=e.get('save_path')
   if save_path is A:
    save_path=PB('save_path')
   else:
    if not P.exists(save_path):
     g(save_path) 
   logger.debug('url : %s',url)
   logger.debug('filename : %s',filename)
   logger.debug('caller_id : %s',caller_id)
   logger.debug('caller : %s',package_name)
   logger.debug('save_path : %s',save_path)
   f=Ffmpeg(url,filename,plugin_id=caller_id,listener=A,max_pf_count=max_pf_count,call_plugin=package_name,save_path=save_path)
   f.start()
   ret['ret']='success'
   ret['data']=f.get_data()
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
   ret['ret']='exception'
   ret['log']=N() 
  return jsonify(ret)
 elif sub=='stop':
  ret={}
  try:
   caller_id=e.get('id')
   package_name=e.get('caller')
   f=PS(package_name,caller_id)
   PG(f.idx)
   ret['ret']='success'
   ret['data']=f.get_data()
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
   ret['ret']='exception'
   ret['log']=N()
  return jsonify(ret)
 elif sub=='status':
  ret={}
  try:
   caller_id=e.get('id')
   package_name=e.get('caller')
   f=PS(package_name,caller_id)
   ret['ret']='success'
   ret['data']=f.get_data()
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
   ret['ret']='exception'
   ret['log']=N()
  return jsonify(ret)
@Q('connect',namespace='/%s'%package_name)
def connect():
 logger.debug('ffmpeg socketio connect')
@Q('disconnect',namespace='/%s'%package_name)
def disconnect():
 logger.debug('ffmpeg socketio disconnect')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
