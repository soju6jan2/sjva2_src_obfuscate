import os
E=object
G=staticmethod
X=str
v=None
R=Exception
W=True
D=os.path
from datetime import datetime
import traceback
F=traceback.format_exc
import logging
import subprocess
i=subprocess.Popen
import time
import re
import threading
import json
import platform
b=platform.system
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root
B=db.session
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.model import ModelRcloneServe
from.logic import Logic
c=Logic.path_config
Q=Logic.path_rclone
import plugin
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class LogicServe(E):
 serve_process={}
 @G
 def serve_list():
  try:
   job_list=B.query(ModelRcloneServe).filter_by().all()
   ret=[x.as_dict()for x in job_list]
   for t in ret:
    t['current_status']=(X(t['id'])in LogicServe.serve_process and LogicServe.serve_process[X(t['id'])]is not v)
   return ret
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 @G
 def serve_save(req):
  try:
   serve_id=req.form['id']
   if serve_id=='-1':
    item=ModelRcloneServe()
   else:
    item=B.query(ModelRcloneServe).filter_by(id=serve_id).with_for_update().first()
   item.name=req.form['serve_name'].strip()
   item.command=req.form['serve_command']
   item.remote=req.form['serve_remote']
   item.remote_path=req.form['serve_remote_path'].strip()
   item.port=req.form['serve_port'].strip()
   item.option=req.form['serve_option'].strip()
   item.auto_start=(req.form['auto_start']=='True')
   B.add(item)
   B.commit()
   return 'success'
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
   return 'fail'
 @G
 def serve_execute(serve_id):
  try:
   item=B.query(ModelRcloneServe).filter_by(id=serve_id).with_for_update().first()
   remote_path='%s:%s'%(item.remote,item.remote_path)
   if b()=='Windows':
    remote_path=remote_path.encode('cp949')
   options=item.option.strip().split(' ')
   command=[Q,'--config',c,'serve',item.command,remote_path,'--addr','0.0.0.0:%s'%item.port]
   command+=options
   command.append('--log-file')
   if item.name=='':
    log_filename='serve_%s'%item.id
   else:
    log_filename='serve_%s'%item.name
   log_filename=D.join(path_app_root,'data','log','%s.log'%log_filename)
   command.append(log_filename)
   logger.debug(command)
   process=i(command)
   LogicServe.serve_process[serve_id]=process
   return 'success'
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
   return 'fail'
 @G
 def serve_stop(req):
  serve_id=req.form['id']
  logger.debug('serve stop:%s'%serve_id)
  return LogicServe.serve_kill(serve_id)
 @G
 def serve_kill(serve_id):
  try:
   if serve_id in LogicServe.serve_process:
    process=LogicServe.serve_process[serve_id]
    logger.debug('process:%s,%s',process,process.poll())
    if process is not v and process.poll()is v:
     import psutil
     p=psutil.Process(process.pid)
     for proc in p.children(recursive=W):
      proc.kill()
     p.kill()
     return 'success'
    else:
     return 'already_stop'
   else:
    return 'not_running'
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
   return 'fail'
  finally:
   LogicServe.serve_process[serve_id]=v
 @G
 def serve_remove(serve_id):
  try:
   logger.debug('remove_job id:%s',serve_id)
   job=B.query(ModelRcloneServe).filter_by(id=serve_id).first()
   B.delete(job)
   B.commit()
   return 'success'
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F()) 
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
