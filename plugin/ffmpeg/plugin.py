import os
e=str
q=Exception
E=None
g=os.makedirs
x=os.path
import traceback
T=traceback.format_exc
import time
from datetime import datetime
c=datetime.now
from pytz import timezone
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory
I=session.query
u=request.args
y=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework import app,db,scheduler,path_app_root,socketio,path_data
Y=socketio.on
M=db.session
from framework.logger import get_logger
from framework.util import Util
xi=Util.db_list_to_dict
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from ffmpeg.logic import Logic
xN=Logic.get_setting_value
xT=Logic.setting_save
o=Logic.path_ffmpeg
xC=Logic.plugin_unload
xW=Logic.plugin_load
from ffmpeg.model import ModelSetting
from ffmpeg.interface_program_ffmpeg import Ffmpeg
xp=Ffmpeg.get_ffmpeg_by_caller
xH=Ffmpeg.instance_list
xs=Ffmpeg.ffmpeg_by_idx
xh=Ffmpeg.stop_by_idx
xn=Ffmpeg.get_version
from system.model import ModelSetting as SystemModelSetting
xr=SystemModelSetting.get
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'FFMPEG'],'sub':[['setting',u'설정'],['download',u'다운로드'],['list',u'목록'],['log',u'로그'],]}
def plugin_load():
 xW() 
def plugin_unload():
 xC() 
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 if sub=='setting':
  setting_list=db.I(ModelSetting).all()
  arg=xi(setting_list)
  arg['ffmpeg_path']=o
  return render_template('plugin_ffmpeg.html',sub=sub,arg=arg)
 elif sub=='download':
  now=e(c(timezone('Asia/Seoul'))).replace(':','').replace('-','').replace(' ','-')
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
    ret=xT(request)
    return jsonify(ret)
   except q as e:
    logger.error('Exception:%s',e)
    logger.error(T())
  elif sub=='ffmpeg_version':
   ret=xn()
   return jsonify(ret)
  elif sub=='download':
   url=y['url']
   filename=y['filename']
   ffmpeg=Ffmpeg(url,filename,call_plugin=package_name)
   data=ffmpeg.start()
   return jsonify([])
  elif sub=='stop':
   idx=y['idx']
   xh(idx)
   return jsonify([])
  elif sub=='play':
   idx=y['idx']
   ffmpeg=xs(idx)
   tmp=ffmpeg.save_fullpath.replace(path_app_root,'')
   tmp=tmp.replace('\\','/')
   logger.debug('play : %s',tmp)
   return jsonify(tmp)
  elif sub=='list':
   ret=[]
   for ffmpeg in xH:
    ret.append(ffmpeg.get_data())
   return jsonify(ret)
 except q as e:
  logger.error('Exception:%s',e)
  logger.error(T())
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 sjva_token=u.get('token')
 if sjva_token!=xr('unique'):
  ret={}
  ret['ret']='wrong_token'
  return jsonify(ret)
 if sub=='download':
  ret={}
  try:
   max_pf_count=xN('max_pf_count')
   url=u.get('url')
   filename=u.get('filename')
   caller_id=u.get('id')
   package_name=u.get('caller')
   save_path=u.get('save_path')
   if save_path is E:
    save_path=xN('save_path')
   else:
    if not x.exists(save_path):
     g(save_path) 
   logger.debug('url : %s',url)
   logger.debug('filename : %s',filename)
   logger.debug('caller_id : %s',caller_id)
   logger.debug('caller : %s',package_name)
   logger.debug('save_path : %s',save_path)
   f=Ffmpeg(url,filename,plugin_id=caller_id,listener=E,max_pf_count=max_pf_count,call_plugin=package_name,save_path=save_path)
   f.start()
   ret['ret']='success'
   ret['data']=f.get_data()
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
   ret['ret']='exception'
   ret['log']=T() 
  return jsonify(ret)
 elif sub=='stop':
  ret={}
  try:
   caller_id=u.get('id')
   package_name=u.get('caller')
   f=xp(package_name,caller_id)
   xh(f.idx)
   ret['ret']='success'
   ret['data']=f.get_data()
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
   ret['ret']='exception'
   ret['log']=T()
  return jsonify(ret)
 elif sub=='status':
  ret={}
  try:
   caller_id=u.get('id')
   package_name=u.get('caller')
   f=xp(package_name,caller_id)
   ret['ret']='success'
   ret['data']=f.get_data()
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
   ret['ret']='exception'
   ret['log']=T()
  return jsonify(ret)
@Y('connect',namespace='/%s'%package_name)
def connect():
 logger.debug('ffmpeg socketio connect')
@Y('disconnect',namespace='/%s'%package_name)
def disconnect():
 logger.debug('ffmpeg socketio disconnect')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
