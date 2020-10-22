import os
s=str
y=Exception
h=None
import traceback
import time
from datetime import datetime
from pytz import timezone
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework import app,db,scheduler,path_app_root,socketio,path_data
from framework.logger import get_logger
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from ffmpeg.logic import Logic
from ffmpeg.model import ModelSetting
from ffmpeg.interface_program_ffmpeg import Ffmpeg
from system.model import ModelSetting as SystemModelSetting
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'FFMPEG'],'sub':[['setting',u'설정'],['download',u'다운로드'],['list',u'목록'],['log',u'로그'],]}
def plugin_load():
 Logic.plugin_load() 
def plugin_unload():
 Logic.plugin_unload() 
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 if sub=='setting':
  setting_list=db.session.query(ModelSetting).all()
  arg=Util.db_list_to_dict(setting_list)
  arg['ffmpeg_path']=Logic.path_ffmpeg
  return render_template('plugin_ffmpeg.html',sub=sub,arg=arg)
 elif sub=='download':
  now=s(datetime.now(timezone('Asia/Seoul'))).replace(':','').replace('-','').replace(' ','-')
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
    ret=Logic.setting_save(request)
    return jsonify(ret)
   except y as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='ffmpeg_version':
   ret=Ffmpeg.get_version()
   return jsonify(ret)
  elif sub=='download':
   url=request.form['url']
   filename=request.form['filename']
   ffmpeg=Ffmpeg(url,filename,call_plugin=package_name)
   data=ffmpeg.start()
   return jsonify([])
  elif sub=='stop':
   idx=request.form['idx']
   Ffmpeg.stop_by_idx(idx)
   return jsonify([])
  elif sub=='play':
   idx=request.form['idx']
   ffmpeg=Ffmpeg.ffmpeg_by_idx(idx)
   tmp=ffmpeg.save_fullpath.replace(path_app_root,'')
   tmp=tmp.replace('\\','/')
   logger.debug('play : %s',tmp)
   return jsonify(tmp)
  elif sub=='list':
   ret=[]
   for ffmpeg in Ffmpeg.instance_list:
    ret.append(ffmpeg.get_data())
   return jsonify(ret)
 except y as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 sjva_token=request.args.get('token')
 if sjva_token!=SystemModelSetting.get('unique'):
  ret={}
  ret['ret']='wrong_token'
  return jsonify(ret)
 if sub=='download':
  ret={}
  try:
   max_pf_count=Logic.get_setting_value('max_pf_count')
   url=request.args.get('url')
   filename=request.args.get('filename')
   caller_id=request.args.get('id')
   package_name=request.args.get('caller')
   save_path=request.args.get('save_path')
   if save_path is h:
    save_path=Logic.get_setting_value('save_path')
   else:
    if not os.path.exists(save_path):
     os.makedirs(save_path) 
   logger.debug('url : %s',url)
   logger.debug('filename : %s',filename)
   logger.debug('caller_id : %s',caller_id)
   logger.debug('caller : %s',package_name)
   logger.debug('save_path : %s',save_path)
   f=Ffmpeg(url,filename,plugin_id=caller_id,listener=h,max_pf_count=max_pf_count,call_plugin=package_name,save_path=save_path)
   f.start()
   ret['ret']='success'
   ret['data']=f.get_data()
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['log']=traceback.format_exc() 
  return jsonify(ret)
 elif sub=='stop':
  ret={}
  try:
   caller_id=request.args.get('id')
   package_name=request.args.get('caller')
   f=Ffmpeg.get_ffmpeg_by_caller(package_name,caller_id)
   Ffmpeg.stop_by_idx(f.idx)
   ret['ret']='success'
   ret['data']=f.get_data()
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['log']=traceback.format_exc()
  return jsonify(ret)
 elif sub=='status':
  ret={}
  try:
   caller_id=request.args.get('id')
   package_name=request.args.get('caller')
   f=Ffmpeg.get_ffmpeg_by_caller(package_name,caller_id)
   ret['ret']='success'
   ret['data']=f.get_data()
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['log']=traceback.format_exc()
  return jsonify(ret)
@socketio.on('connect',namespace='/%s'%package_name)
def connect():
 logger.debug('ffmpeg socketio connect')
@socketio.on('disconnect',namespace='/%s'%package_name)
def disconnect():
 logger.debug('ffmpeg socketio disconnect')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
