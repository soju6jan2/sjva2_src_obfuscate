import os
E=object
G=staticmethod
l=Exception
V=False
J=True
I=int
T=None
import sys
import traceback
c=traceback.format_exc
import logging
import threading
w=threading.Thread
import time
p=time.sleep
from sqlalchemy import desc,or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root
U=scheduler.execute_job
t=scheduler.is_running
f=scheduler.is_include
B=scheduler.remove_job
s=scheduler.add_job_instance
R=db.session
i=app.config
from framework.job import Job
from framework.util import Util
b=Util.get_paging_info
from system.logic import SystemLogic
from.model import ModelSetting,ModelFileprocessMovieItem
S=ModelFileprocessMovieItem.id
q=ModelFileprocessMovieItem.target
k=ModelFileprocessMovieItem.movie_id
y=ModelFileprocessMovieItem.filename
N=ModelSetting.query
from.logic_movie import LogicMovie
o=LogicMovie.start
import plex
g=plex.Logic
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(E):
 db_default={'interval':'17','auto_start':'False','web_page_size':'20','source_path':'','target_path':'','use_smi_to_srt':'True','folder_rule':'%TITLE% (%YEAR%)'}
 @G
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if R.query(ModelSetting).filter_by(key=key).count()==0:
     R.add(ModelSetting(key,value))
   R.commit()
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def plugin_load():
  try:
   Logic.db_init()
   if N.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def plugin_unload():
  try:
   pass
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def scheduler_start():
  try:
   interval=N.filter_by(key='interval').first().value
   job=Job(package_name,package_name,interval,Logic.scheduler_function,u"영화 파일처리",V)
   s(job)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def scheduler_stop():
  try:
   B(package_name)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=R.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   R.commit()
   return J 
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
   return V
 @G
 def get_setting_value(key):
  try:
   return R.query(ModelSetting).filter_by(key=key).first().value
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def reset_db():
  try:
   R.query(ModelFileprocessMovieItem).delete()
   R.commit()
   return J
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
   return V
 @G
 def one_execute():
  try:
   if f(package_name):
    if t(package_name):
     ret='is_running'
    else:
     U(package_name)
     ret='scheduler'
   else:
    def func():
     p(2)
     Logic.scheduler_function()
    w(target=func,args=()).start()
    ret='thread'
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
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
     if i['config']['use_celery']:
      result=smi2srt.Logic.start_by_path.apply_async((source_path,))
      result.get()
     else:
      smi2srt.Logic.start_by_path(work_path=source_path)
    except l as e:
     logger.error('Exception:%s',e)
     logger.error(c())
   result_list=o(source_paths,target_path)
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=I(R.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=I(req.form['page'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=R.query(ModelFileprocessMovieItem)
   if search!='':
    query=query.filter(y.like('%'+search+'%'))
   option=req.form['option']
   if option=='all':
    pass
   elif option=='movie_o':
    query=query.filter(k!=T)
   elif option=='movie_x':
    query=query.filter(k==T)
   else:
    query=query.filter(q==option)
   order=req.form['order']if 'order' in req.form else 'desc'
   if order=='desc':
    query=query.order_by(desc(S))
   else:
    query=query.order_by(S)
   count=query.count()
   query=query.limit(page_size).offset((page-1)*page_size)
   logger.debug('ModelFileprocessMovieItem count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=b(count,page,page_size)
   ret['plex_server_hash']=g.get_server_hash()
   return ret
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
