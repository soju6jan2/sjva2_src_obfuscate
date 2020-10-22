import os
J=object
C=staticmethod
i=Exception
S=False
X=True
I=int
K=None
import sys
import traceback
B=traceback.format_exc
import logging
import threading
H=threading.Thread
import time
P=time.sleep
from sqlalchemy import desc,or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root
Y=scheduler.execute_job
c=scheduler.is_running
l=scheduler.is_include
d=scheduler.remove_job
x=scheduler.add_job_instance
g=db.session
L=app.config
from framework.job import Job
from framework.util import Util
h=Util.get_paging_info
from system.logic import SystemLogic
from.model import ModelSetting,ModelFileprocessMovieItem
R=ModelFileprocessMovieItem.id
b=ModelFileprocessMovieItem.target
G=ModelFileprocessMovieItem.movie_id
q=ModelFileprocessMovieItem.filename
D=ModelSetting.query
from.logic_movie import LogicMovie
s=LogicMovie.start
import plex
p=plex.Logic
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(J):
 db_default={'interval':'17','auto_start':'False','web_page_size':'20','source_path':'','target_path':'','use_smi_to_srt':'True','folder_rule':'%TITLE% (%YEAR%)'}
 @C
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if g.query(ModelSetting).filter_by(key=key).count()==0:
     g.add(ModelSetting(key,value))
   g.commit()
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def plugin_load():
  try:
   Logic.db_init()
   if D.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def plugin_unload():
  try:
   pass
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def scheduler_start():
  try:
   interval=D.filter_by(key='interval').first().value
   job=Job(package_name,package_name,interval,Logic.scheduler_function,u"영화 파일처리",S)
   x(job)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def scheduler_stop():
  try:
   d(package_name)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=g.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   g.commit()
   return X 
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
   return S
 @C
 def get_setting_value(key):
  try:
   return g.query(ModelSetting).filter_by(key=key).first().value
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def reset_db():
  try:
   g.query(ModelFileprocessMovieItem).delete()
   g.commit()
   return X
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
   return S
 @C
 def one_execute():
  try:
   if l(package_name):
    if c(package_name):
     ret='is_running'
    else:
     Y(package_name)
     ret='scheduler'
   else:
    def func():
     P(2)
     Logic.scheduler_function()
    H(target=func,args=()).start()
    ret='thread'
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
   ret='fail'
  return ret
 @C
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
     if L['config']['use_celery']:
      result=smi2srt.Logic.start_by_path.apply_async((source_path,))
      result.get()
     else:
      smi2srt.Logic.start_by_path(work_path=source_path)
    except i as e:
     logger.error('Exception:%s',e)
     logger.error(B())
   result_list=s(source_paths,target_path)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=I(g.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=I(req.form['page'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=g.query(ModelFileprocessMovieItem)
   if search!='':
    query=query.filter(q.like('%'+search+'%'))
   option=req.form['option']
   if option=='all':
    pass
   elif option=='movie_o':
    query=query.filter(G!=K)
   elif option=='movie_x':
    query=query.filter(G==K)
   else:
    query=query.filter(b==option)
   order=req.form['order']if 'order' in req.form else 'desc'
   if order=='desc':
    query=query.order_by(desc(R))
   else:
    query=query.order_by(R)
   count=query.count()
   query=query.limit(page_size).offset((page-1)*page_size)
   logger.debug('ModelFileprocessMovieItem count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=h(count,page,page_size)
   ret['plex_server_hash']=p.get_server_hash()
   return ret
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
