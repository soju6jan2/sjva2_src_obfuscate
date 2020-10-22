import os
u=object
F=staticmethod
a=Exception
v=True
k=False
z=int
d=id
I=None
o=os.remove
D=os.mkdir
r=os.path
from datetime import datetime
c=datetime.now
import traceback
S=traceback.format_exc
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
b=scheduler.remove_job
W=scheduler.add_job_instance
P=db.session
from framework.job import Job
from framework.util import Util
V=Util.get_paging_info
from system.logic import SystemLogic
from.model import ModelSetting,ModelGDriveScanJob,ModelGDriveScanFile
g=ModelGDriveScanFile.d
m=ModelGDriveScanFile.name
K=ModelSetting.query
from.gdrive import GDrive,Auth
H=Auth.save_token
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(u):
 db_default={'auto_start':'False','web_page_size':'30'}
 gdrive_instance_list=[]
 @F
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if P.query(ModelSetting).filter_by(key=key).count()==0:
     P.add(ModelSetting(key,value))
   P.commit()
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 @F
 def plugin_load():
  try:
   Logic.db_init()
   json_folder=r.join(path_data,'db','gdrive')
   if not r.exists(json_folder):
    D(json_folder)
   if K.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 @F
 def plugin_unload():
  try:
   Logic.scheduler_stop()
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 @F
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=P.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   P.commit()
   return v 
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return k
 @F
 def scheduler_start():
  try:
   interval=9999
   """
            for item in lists:
                job = Job(package_name, '%s_%s' % (package_name, item.name), interval, Logic.start_gdrive, u"GDrive Scan : %s" % item.name, True, args=item.id)
                scheduler.add_job_instance(job)
            """   
   job=Job(package_name,package_name,interval,Logic.scheduler_thread_function,u"GDrive Scan",v)
   W(job)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 @F
 def start_gdrive(*args,**kwargs):
  logger.debug('start_gdrive:%s id:%s',args,args[0])
  try:
   job=P.query(ModelGDriveScanJob).filter_by(d=z(args[0])).first()
   match_rule='%s:%s,%s'%(job.name,job.gdrive_path,job.plex_path)
   gdrive=GDrive(match_rule)
   gdrive.start_change_watch()
   gdrive.thread.join()
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 @F
 def scheduler_thread_function(*args,**kwargs):
  try:
   lists=P.query(ModelGDriveScanJob).filter().all()
   Logic.gdrive_instance_list=[]
   for job in lists:
    match_rule='%s:%s,%s'%(job.name,job.gdrive_path,job.plex_path)
    gdrive=GDrive(match_rule)
    gdrive.start_change_watch()
    Logic.gdrive_instance_list.append(gdrive)
   for ins in Logic.gdrive_instance_list:
    ins.thread.join()
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 @F
 def scheduler_stop():
  try:
   for ins in Logic.gdrive_instance_list:
    ins.stop()
   b(package_name)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
 @F
 def gdrive_save(req):
  try:
   code=req.form['gdrive_code']
   name=req.form['gdrive_name']
   H(code,name)
   job=ModelGDriveScanJob()
   job.name=name
   job.gdrive_path=req.form['gdrive_path']
   job.plex_path=req.form['plex_path']
   P.add(job)
   P.commit()
   return v
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return k
 @F
 def gdrive_list():
  try:
   lists=P.query(ModelGDriveScanJob).filter().all()
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
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return k
 @F
 def gdrive_delete(req):
  try:
   job_id=z(req.form['id'])
   job=P.query(ModelGDriveScanJob).filter_by(d=job_id).first()
   name=job.name
   tokenfile=r.join(path_data,'db','gdrive','%s.json'%name)
   if r.exists(tokenfile):
    o(tokenfile)
   dbfile=r.join(path_data,'db','gdrive','%s.db'%name)
   if r.exists(dbfile):
    o(dbfile)
   P.delete(job)
   P.commit()
   return v
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return k
 @F
 def receive_scan_result(d,filename):
  try:
   if v:
    logger.debug('Receive Scan Completed : %s-%s',d,filename)
    modelfile=P.query(ModelGDriveScanFile).filter_by(d=z(d)).with_for_update().first()
    if modelfile is not I:
     modelfile.scan_time=c()
     P.commit()
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
 @F
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=z(P.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=z(req.form['page'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=P.query(ModelGDriveScanFile)
   if search!='':
    query=query.filter(m.like('%'+search+'%'))
   count=query.count()
   query=(query.order_by(desc(g)).limit(page_size).offset((page-1)*page_size))
   logger.debug('ModelGDriveScanFile count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=V(count,page,page_size)
   return ret
  except a as e:
   logger.debug('Exception:%s',e)
   logger.debug(S())
 @F
 def reset_db():
  try:
   P.query(ModelGDriveScanFile).delete()
   P.commit()
   return v
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return k
 from framework.event import MyEvent
 listener=MyEvent()
 @F
 def add_listener(f):
  try:
   Logic.listener+=f
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return k
 @F
 def remove_listener(f):
  try:
   Logic.listener-=f
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
   return k
 @F
 def send_to_listener(type_add_remove,is_file,filepath):
  try:
   args=[]
   kargs={'plugin':package_name,'type':type_add_remove.lower(),'filepath':filepath,'is_file':is_file}
   Logic.listener.fire(*args,**kargs)
  except a as e:
   logger.error('Exception:%s',e)
   logger.error(S())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
