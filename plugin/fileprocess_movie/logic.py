import os
X=object
G=staticmethod
n=Exception
t=False
x=True
a=int
I=None
import sys
import traceback
import logging
import threading
import time
from sqlalchemy import desc,or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.model import ModelSetting,ModelFileprocessMovieItem
from.logic_movie import LogicMovie
import plex
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(X):
 db_default={'interval':'17','auto_start':'False','web_page_size':'20','source_path':'','target_path':'','use_smi_to_srt':'True','folder_rule':'%TITLE% (%YEAR%)'}
 @G
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     db.session.add(ModelSetting(key,value))
   db.session.commit()
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @G
 def plugin_load():
  try:
   Logic.db_init()
   if ModelSetting.query.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @G
 def plugin_unload():
  try:
   pass
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @G
 def scheduler_start():
  try:
   interval=ModelSetting.query.filter_by(key='interval').first().value
   job=Job(package_name,package_name,interval,Logic.scheduler_function,u"영화 파일처리",t)
   scheduler.add_job_instance(job)
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @G
 def scheduler_stop():
  try:
   scheduler.remove_job(package_name)
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @G
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   db.session.commit()
   return x 
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return t
 @G
 def get_setting_value(key):
  try:
   return db.session.query(ModelSetting).filter_by(key=key).first().value
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @G
 def reset_db():
  try:
   db.session.query(ModelFileprocessMovieItem).delete()
   db.session.commit()
   return x
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return t
 @G
 def one_execute():
  try:
   if scheduler.is_include(package_name):
    if scheduler.is_running(package_name):
     ret='is_running'
    else:
     scheduler.execute_job(package_name)
     ret='scheduler'
   else:
    def func():
     time.sleep(2)
     Logic.scheduler_function()
    threading.Thread(target=func,args=()).start()
    ret='thread'
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   ret='fail'
  return ret
 @G
 def scheduler_function():
  try:
   logger.debug('%s scheduler_function',package_name)
   source_path=Logic.get_setting_value('source_path')
   target_path=Logic.get_setting_value('target_path')
   source_paths=[x.strip()for x in source_path.split(',')]
   if not source_paths:
    return
   if target_path=='':
    return
   if Logic.get_setting_value('use_smi_to_srt')=='True':
    try:
     import smi2srt
     if app.config['config']['use_celery']:
      result=smi2srt.Logic.start_by_path.apply_async((source_path,))
      result.get()
     else:
      smi2srt.Logic.start_by_path(work_path=source_path)
    except n as e:
     logger.error('Exception:%s',e)
     logger.error(traceback.format_exc())
   result_list=LogicMovie.start(source_paths,target_path)
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @G
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=a(db.session.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=a(req.form['page'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=db.session.query(ModelFileprocessMovieItem)
   if search!='':
    query=query.filter(ModelFileprocessMovieItem.filename.like('%'+search+'%'))
   option=req.form['option']
   if option=='all':
    pass
   elif option=='movie_o':
    query=query.filter(ModelFileprocessMovieItem.movie_id!=I)
   elif option=='movie_x':
    query=query.filter(ModelFileprocessMovieItem.movie_id==I)
   else:
    query=query.filter(ModelFileprocessMovieItem.target==option)
   order=req.form['order']if 'order' in req.form else 'desc'
   if order=='desc':
    query=query.order_by(desc(ModelFileprocessMovieItem.id))
   else:
    query=query.order_by(ModelFileprocessMovieItem.id)
   count=query.count()
   query=query.limit(page_size).offset((page-1)*page_size)
   logger.debug('ModelFileprocessMovieItem count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=Util.get_paging_info(count,page,page_size)
   ret['plex_server_hash']=plex.Logic.get_server_hash()
   return ret
  except n as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
