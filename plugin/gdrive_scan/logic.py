import os
C=object
f=staticmethod
U=Exception
q=True
B=False
L=int
x=id
g=None
n=os.remove
c=os.mkdir
W=os.path
from datetime import datetime
v=datetime.now
import traceback
i=traceback.format_exc
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
Q=scheduler.remove_job
e=scheduler.add_job_instance
G=db.session
from framework.job import Job
from framework.util import Util
d=Util.get_paging_info
from system.logic import SystemLogic
from.model import ModelSetting,ModelGDriveScanJob,ModelGDriveScanFile
w=ModelGDriveScanFile.x
l=ModelGDriveScanFile.name
h=ModelSetting.query
from.gdrive import GDrive,Auth
E=Auth.save_token
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(C):
 db_default={'auto_start':'False','web_page_size':'30'}
 gdrive_instance_list=[]
 @f
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if G.query(ModelSetting).filter_by(key=key).count()==0:
     G.add(ModelSetting(key,value))
   G.commit()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 @f
 def plugin_load():
  try:
   Logic.db_init()
   json_folder=W.join(path_data,'db','gdrive')
   if not W.exists(json_folder):
    c(json_folder)
   if h.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 @f
 def plugin_unload():
  try:
   Logic.scheduler_stop()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 @f
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=G.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   G.commit()
   return q 
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return B
 @f
 def scheduler_start():
  try:
   interval=9999
   """
            for item in lists:
                job = Job(package_name, '%s_%s' % (package_name, item.name), interval, Logic.start_gdrive, u"GDrive Scan : %s" % item.name, True, args=item.id)
                scheduler.add_job_instance(job)
            """   
   job=Job(package_name,package_name,interval,Logic.scheduler_thread_function,u"GDrive Scan",q)
   e(job)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 @f
 def start_gdrive(*args,**kwargs):
  logger.debug('start_gdrive:%s id:%s',args,args[0])
  try:
   job=G.query(ModelGDriveScanJob).filter_by(x=L(args[0])).first()
   match_rule='%s:%s,%s'%(job.name,job.gdrive_path,job.plex_path)
   gdrive=GDrive(match_rule)
   gdrive.start_change_watch()
   gdrive.thread.join()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 @f
 def scheduler_thread_function(*args,**kwargs):
  try:
   lists=G.query(ModelGDriveScanJob).filter().all()
   Logic.gdrive_instance_list=[]
   for job in lists:
    match_rule='%s:%s,%s'%(job.name,job.gdrive_path,job.plex_path)
    gdrive=GDrive(match_rule)
    gdrive.start_change_watch()
    Logic.gdrive_instance_list.append(gdrive)
   for ins in Logic.gdrive_instance_list:
    ins.thread.join()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 @f
 def scheduler_stop():
  try:
   for ins in Logic.gdrive_instance_list:
    ins.stop()
   Q(package_name)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
 @f
 def gdrive_save(req):
  try:
   code=req.form['gdrive_code']
   name=req.form['gdrive_name']
   E(code,name)
   job=ModelGDriveScanJob()
   job.name=name
   job.gdrive_path=req.form['gdrive_path']
   job.plex_path=req.form['plex_path']
   G.add(job)
   G.commit()
   return q
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return B
 @f
 def gdrive_list():
  try:
   lists=G.query(ModelGDriveScanJob).filter().all()
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
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return B
 @f
 def gdrive_delete(req):
  try:
   job_id=L(req.form['id'])
   job=G.query(ModelGDriveScanJob).filter_by(x=job_id).first()
   name=job.name
   tokenfile=W.join(path_data,'db','gdrive','%s.json'%name)
   if W.exists(tokenfile):
    n(tokenfile)
   dbfile=W.join(path_data,'db','gdrive','%s.db'%name)
   if W.exists(dbfile):
    n(dbfile)
   G.delete(job)
   G.commit()
   return q
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return B
 @f
 def receive_scan_result(x,filename):
  try:
   if q:
    logger.debug('Receive Scan Completed : %s-%s',x,filename)
    modelfile=G.query(ModelGDriveScanFile).filter_by(x=L(x)).with_for_update().first()
    if modelfile is not g:
     modelfile.scan_time=v()
     G.commit()
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
 @f
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=L(G.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=L(req.form['page'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=G.query(ModelGDriveScanFile)
   if search!='':
    query=query.filter(l.like('%'+search+'%'))
   count=query.count()
   query=(query.order_by(desc(w)).limit(page_size).offset((page-1)*page_size))
   logger.debug('ModelGDriveScanFile count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=d(count,page,page_size)
   return ret
  except U as e:
   logger.debug('Exception:%s',e)
   logger.debug(i())
 @f
 def reset_db():
  try:
   G.query(ModelGDriveScanFile).delete()
   G.commit()
   return q
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return B
 from framework.event import MyEvent
 listener=MyEvent()
 @f
 def add_listener(f):
  try:
   Logic.listener+=f
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return B
 @f
 def remove_listener(f):
  try:
   Logic.listener-=f
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return B
 @f
 def send_to_listener(type_add_remove,is_file,filepath):
  try:
   args=[]
   kargs={'plugin':package_name,'type':type_add_remove.lower(),'filepath':filepath,'is_file':is_file}
   Logic.listener.fire(*args,**kargs)
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
