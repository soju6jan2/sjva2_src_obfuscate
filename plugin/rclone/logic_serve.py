import os
K=object
u=staticmethod
J=str
X=None
Y=Exception
W=True
c=os.path
from datetime import datetime
import traceback
b=traceback.format_exc
import logging
import subprocess
e=subprocess.Popen
import time
import re
import threading
import json
import platform
Q=platform.system
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root
y=db.session
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.model import ModelRcloneServe
from.logic import Logic
d=Logic.path_config
x=Logic.path_rclone
import plugin
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class LogicServe(K):
 serve_process={}
 @u
 def serve_list():
  try:
   job_list=y.query(ModelRcloneServe).filter_by().all()
   ret=[x.as_dict()for x in job_list]
   for t in ret:
    t['current_status']=(J(t['id'])in LogicServe.serve_process and LogicServe.serve_process[J(t['id'])]is not X)
   return ret
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def serve_save(req):
  try:
   serve_id=req.form['id']
   if serve_id=='-1':
    item=ModelRcloneServe()
   else:
    item=y.query(ModelRcloneServe).filter_by(id=serve_id).with_for_update().first()
   item.name=req.form['serve_name'].strip()
   item.command=req.form['serve_command']
   item.remote=req.form['serve_remote']
   item.remote_path=req.form['serve_remote_path'].strip()
   item.port=req.form['serve_port'].strip()
   item.option=req.form['serve_option'].strip()
   item.auto_start=(req.form['auto_start']=='True')
   y.add(item)
   y.commit()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
 @u
 def serve_execute(serve_id):
  try:
   item=y.query(ModelRcloneServe).filter_by(id=serve_id).with_for_update().first()
   remote_path='%s:%s'%(item.remote,item.remote_path)
   if Q()=='Windows':
    remote_path=remote_path.encode('cp949')
   options=item.option.strip().split(' ')
   command=[x,'--config',d,'serve',item.command,remote_path,'--addr','0.0.0.0:%s'%item.port]
   command+=options
   command.append('--log-file')
   if item.name=='':
    log_filename='serve_%s'%item.id
   else:
    log_filename='serve_%s'%item.name
   log_filename=c.join(path_app_root,'data','log','%s.log'%log_filename)
   command.append(log_filename)
   logger.debug(command)
   process=e(command)
   LogicServe.serve_process[serve_id]=process
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
 @u
 def serve_stop(req):
  serve_id=req.form['id']
  logger.debug('serve stop:%s'%serve_id)
  return LogicServe.serve_kill(serve_id)
 @u
 def serve_kill(serve_id):
  try:
   if serve_id in LogicServe.serve_process:
    process=LogicServe.serve_process[serve_id]
    logger.debug('process:%s,%s',process,process.poll())
    if process is not X and process.poll()is X:
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
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
  finally:
   LogicServe.serve_process[serve_id]=X
 @u
 def serve_remove(serve_id):
  try:
   logger.debug('remove_job id:%s',serve_id)
   job=y.query(ModelRcloneServe).filter_by(id=serve_id).first()
   y.delete(job)
   y.commit()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b()) 
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
