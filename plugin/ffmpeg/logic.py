import os
p=int
v=staticmethod
q=object
c=None
U=Exception
y=True
m=False
from datetime import datetime
import traceback
import logging
import subprocess
import time
import re
import threading
import json
import enum
import platform
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,socketio,path_data
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.model import ModelSetting
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Status(enum.Enum):
 READY=0
 WRONG_URL=1
 WRONG_DIRECTORY=2
 EXCEPTION=3
 ERROR=4
 HTTP_FORBIDDEN=11
 DOWNLOADING=5
 USER_STOP=6
 COMPLETED=7
 TIME_OVER=8
 PF_STOP=9
 FORCE_STOP=10 
 ALREADY_DOWNLOADING=12 
 def __int__(self):
  return self.value
 def __str__(self):
  kor=[r'준비',r'URL에러',r'폴더에러',r'실패(Exception)',r'실패(에러)',r'다운로드중',r'사용자중지',r'완료',r'시간초과',r'PF중지',r'강제중지',r'403에러',r'임시파일이 이미 있음']
  return kor[p(self)]
 def __repr__(self):
  return self.name
 @v
 def get_instance(value):
  tmp=[Status.READY,Status.WRONG_URL,Status.WRONG_DIRECTORY,Status.EXCEPTION,Status.ERROR,Status.DOWNLOADING,Status.USER_STOP,Status.COMPLETED,Status.TIME_OVER,Status.PF_STOP,Status.FORCE_STOP,Status.HTTP_FORBIDDEN,Status.ALREADY_DOWNLOADING]
  return tmp[value]
class Logic(q):
 db_default={'temp_path':os.path.join(path_data,'download_tmp'),'save_path':os.path.join(path_data,'download'),'max_pf_count':'0','if_fail_remove_tmp_file':'True','timeout_minute':'60',}
 path_ffmpeg=c
 @v
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     db.session.add(ModelSetting(key,value))
   db.session.commit()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @v
 def plugin_load():
  try:
   Logic.db_init()
   Logic.path_ffmpeg=os.path.join(path_app_root,'bin',platform.system(),'ffmpeg')
   if platform.system()=='Windows':
    Logic.path_ffmpeg+='.exe'
   else:
    Logic.path_ffmpeg='ffmpeg'
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @v
 def plugin_unload():
  try:
   from ffmpeg.interface_program_ffmpeg import Ffmpeg
   Ffmpeg.plugin_unload()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @v
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   db.session.commit()
   return y 
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return m
 @v
 def get_setting_value(key):
  try:
   return db.session.query(ModelSetting).filter_by(key=key).first().value
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @v
 def ffmpeg_listener(**args):
  refresh_type=c
  if args['type']=='status_change':
   if args['status']==Status.DOWNLOADING:
    refresh_type='status_change'
   elif args['status']==Status.COMPLETED:
    refresh_type='status_change'
   elif args['status']==Status.READY:
    data={'type':'info','msg':u'다운로드중 Duration(%s)'%args['data']['duration_str']+'<br>'+args['data']['save_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y)
    refresh_type='add' 
  elif args['type']=='last':
   if args['status']==Status.WRONG_URL:
    data={'type':'warning','msg':u'잘못된 URL입니다'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y)
    refresh_type='add'
   elif args['status']==Status.WRONG_DIRECTORY:
    data={'type':'warning','msg':u'잘못된 디렉토리입니다.<br>'+args['data']['save_fullpath']}
    socketio.emit("notify",data,namespace='/framework',broadcast=y)
    refresh_type='add'
   elif args['status']==Status.ERROR or args['status']==Status.EXCEPTION:
    data={'type':'warning','msg':u'다운로드 시작 실패.<br>'+args['data']['save_fullpath']}
    socketio.emit("notify",data,namespace='/framework',broadcast=y)
    refresh_type='add'
   elif args['status']==Status.USER_STOP:
    data={'type':'warning','msg':u'다운로드가 중지 되었습니다.<br>'+args['data']['save_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y) 
    refresh_type='last'
   elif args['status']==Status.COMPLETED:
    data={'type':'success','msg':u'다운로드가 완료 되었습니다.<br>'+args['data']['save_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y) 
    refresh_type='last'
   elif args['status']==Status.TIME_OVER:
    data={'type':'warning','msg':u'시간초과로 중단 되었습니다.<br>'+args['data']['save_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y) 
    refresh_type='last'
   elif args['status']==Status.PF_STOP:
    data={'type':'warning','msg':u'PF초과로 중단 되었습니다.<br>'+args['data']['save_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y) 
    refresh_type='last'
   elif args['status']==Status.FORCE_STOP:
    data={'type':'warning','msg':u'강제 중단 되었습니다.<br>'+args['data']['save_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y) 
    refresh_type='last' 
   elif args['status']==Status.HTTP_FORBIDDEN:
    data={'type':'warning','msg':u'403에러로 중단 되었습니다.<br>'+args['data']['save_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y) 
    refresh_type='last' 
   elif args['status']==Status.ALREADY_DOWNLOADING:
    data={'type':'warning','msg':u'임시파일폴더에 파일이 있습니다.<br>'+args['data']['temp_fullpath'],'url':'/ffmpeg/list'}
    socketio.emit("notify",data,namespace='/framework',broadcast=y) 
    refresh_type='last'
  elif args['type']=='normal':
   if args['status']==Status.DOWNLOADING:
    refresh_type='status'
  if refresh_type is not c:
   socketio.emit(refresh_type,args['data'],namespace='/%s'%package_name,broadcast=y)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
