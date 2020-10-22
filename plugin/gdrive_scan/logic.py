import os
K=object
p=staticmethod
B=Exception
Y=True
c=False
w=int
A=id
U=None
from datetime import datetime
import traceback
import logging
import subprocess
import time
import re
import threading
import json
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,path_data
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.model import ModelSetting,ModelGDriveScanJob,ModelGDriveScanFile
from.gdrive import GDrive,Auth
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(K):
 db_default={'auto_start':'False','web_page_size':'30'}
 gdrive_instance_list=[]
 @p
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     db.session.add(ModelSetting(key,value))
   db.session.commit()
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @p
 def plugin_load():
  try:
   Logic.db_init()
   json_folder=os.path.join(path_data,'db','gdrive')
   if not os.path.exists(json_folder):
    os.mkdir(json_folder)
   if ModelSetting.query.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @p
 def plugin_unload():
  try:
   Logic.scheduler_stop()
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @p
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   db.session.commit()
   return Y 
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return c
 @p
 def scheduler_start():
  try:
   interval=9999
   """
            for item in lists:
                job = Job(package_name, '%s_%s' % (package_name, item.name), interval, Logic.start_gdrive, u"GDrive Scan : %s" % item.name, True, args=item.id)
                scheduler.add_job_instance(job)
            """   
   job=Job(package_name,package_name,interval,Logic.scheduler_thread_function,u"GDrive Scan",Y)
   scheduler.add_job_instance(job)
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @p
 def start_gdrive(*args,**kwargs):
  logger.debug('start_gdrive:%s id:%s',args,args[0])
  try:
   job=db.session.query(ModelGDriveScanJob).filter_by(A=w(args[0])).first()
   match_rule='%s:%s,%s'%(job.name,job.gdrive_path,job.plex_path)
   gdrive=GDrive(match_rule)
   gdrive.start_change_watch()
   gdrive.thread.join()
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @p
 def scheduler_thread_function(*args,**kwargs):
  try:
   lists=db.session.query(ModelGDriveScanJob).filter().all()
   Logic.gdrive_instance_list=[]
   for job in lists:
    match_rule='%s:%s,%s'%(job.name,job.gdrive_path,job.plex_path)
    gdrive=GDrive(match_rule)
    gdrive.start_change_watch()
    Logic.gdrive_instance_list.append(gdrive)
   for ins in Logic.gdrive_instance_list:
    ins.thread.join()
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @p
 def scheduler_stop():
  try:
   for ins in Logic.gdrive_instance_list:
    ins.stop()
   scheduler.remove_job(package_name)
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @p
 def gdrive_save(req):
  try:
   code=req.form['gdrive_code']
   name=req.form['gdrive_name']
   Auth.save_token(code,name)
   job=ModelGDriveScanJob()
   job.name=name
   job.gdrive_path=req.form['gdrive_path']
   job.plex_path=req.form['plex_path']
   db.session.add(job)
   db.session.commit()
   return Y
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return c
 @p
 def gdrive_list():
  try:
   lists=db.session.query(ModelGDriveScanJob).filter().all()
   ret=[item.as_dict()for item in lists]
   return ret
   """
            folder = os.path.join(path_data, 'db', 'gdrive')
            lists = os.listdir(folder)
            for item in lists:
                if item.find('.json') != -1:
                    ret.append(item.split('.')[0])
            return ret            
            """   
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return c
 @p
 def gdrive_delete(req):
  try:
   job_id=w(req.form['id'])
   job=db.session.query(ModelGDriveScanJob).filter_by(A=job_id).first()
   name=job.name
   tokenfile=os.path.join(path_data,'db','gdrive','%s.json'%name)
   if os.path.exists(tokenfile):
    os.remove(tokenfile)
   dbfile=os.path.join(path_data,'db','gdrive','%s.db'%name)
   if os.path.exists(dbfile):
    os.remove(dbfile)
   db.session.delete(job)
   db.session.commit()
   return Y
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return c
 @p
 def receive_scan_result(A,filename):
  try:
   if Y:
    logger.debug('Receive Scan Completed : %s-%s',A,filename)
    modelfile=db.session.query(ModelGDriveScanFile).filter_by(A=w(A)).with_for_update().first()
    if modelfile is not U:
     modelfile.scan_time=datetime.now()
     db.session.commit()
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
 @p
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=w(db.session.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=w(req.form['page'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=db.session.query(ModelGDriveScanFile)
   if search!='':
    query=query.filter(ModelGDriveScanFile.name.like('%'+search+'%'))
   count=query.count()
   query=(query.order_by(desc(ModelGDriveScanFile.A)).limit(page_size).offset((page-1)*page_size))
   logger.debug('ModelGDriveScanFile count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=Util.get_paging_info(count,page,page_size)
   return ret
  except B as exception:
   logger.debug('Exception:%s',exception)
   logger.debug(traceback.format_exc())
 @p
 def reset_db():
  try:
   db.session.query(ModelGDriveScanFile).delete()
   db.session.commit()
   return Y
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return c
 from framework.event import MyEvent
 listener=MyEvent()
 @p
 def add_listener(f):
  try:
   Logic.listener+=f
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return c
 @p
 def remove_listener(f):
  try:
   Logic.listener-=f
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return c
 @p
 def send_to_listener(type_add_remove,is_file,filepath):
  try:
   args=[]
   kargs={'plugin':package_name,'type':type_add_remove.lower(),'filepath':filepath,'is_file':is_file}
   Logic.listener.fire(*args,**kargs)
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
