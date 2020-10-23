import os
l=object
U=staticmethod
b=str
i=None
X=Exception
T=True
from datetime import datetime
import traceback
import logging
import subprocess
import time
import re
import threading
import json
import platform
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.model import ModelRcloneServe
from.logic import Logic
import plugin
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class LogicServe(l):
 serve_process={}
 @U
 def serve_list():
  try:
   job_list=db.session.query(ModelRcloneServe).filter_by().all()
   ret=[x.as_dict()for x in job_list]
   for t in ret:
    t['current_status']=(b(t['id'])in LogicServe.serve_process and LogicServe.serve_process[b(t['id'])]is not i)
   return ret
  except X as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @U
 def serve_save(req):
  try:
   serve_id=req.form['id']
   if serve_id=='-1':
    item=ModelRcloneServe()
   else:
    item=db.session.query(ModelRcloneServe).filter_by(id=serve_id).with_for_update().first()
   item.name=req.form['serve_name'].strip()
   item.command=req.form['serve_command']
   item.remote=req.form['serve_remote']
   item.remote_path=req.form['serve_remote_path'].strip()
   item.port=req.form['serve_port'].strip()
   item.option=req.form['serve_option'].strip()
   item.auto_start=(req.form['auto_start']=='True')
   db.session.add(item)
   db.session.commit()
   return 'success'
  except X as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @U
 def serve_execute(serve_id):
  try:
   item=db.session.query(ModelRcloneServe).filter_by(id=serve_id).with_for_update().first()
   remote_path='%s:%s'%(item.remote,item.remote_path)
   if platform.system()=='Windows':
    remote_path=remote_path.encode('cp949')
   options=item.option.strip().split(' ')
   command=[Logic.path_rclone,'--config',Logic.path_config,'serve',item.command,remote_path,'--addr','0.0.0.0:%s'%item.port]
   command+=options
   command.append('--log-file')
   if item.name=='':
    log_filename='serve_%s'%item.id
   else:
    log_filename='serve_%s'%item.name
   log_filename=os.path.join(path_app_root,'data','log','%s.log'%log_filename)
   command.append(log_filename)
   logger.debug(command)
   process=subprocess.Popen(command)
   LogicServe.serve_process[serve_id]=process
   return 'success'
  except X as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @U
 def serve_stop(req):
  serve_id=req.form['id']
  logger.debug('serve stop:%s'%serve_id)
  return LogicServe.serve_kill(serve_id)
 @U
 def serve_kill(serve_id):
  try:
   if serve_id in LogicServe.serve_process:
    process=LogicServe.serve_process[serve_id]
    logger.debug('process:%s,%s',process,process.poll())
    if process is not i and process.poll()is i:
     import psutil
     p=psutil.Process(process.pid)
     for proc in p.children(recursive=T):
      proc.kill()
     p.kill()
     return 'success'
    else:
     return 'already_stop'
   else:
    return 'not_running'
  except X as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
  finally:
   LogicServe.serve_process[serve_id]=i
 @U
 def serve_remove(serve_id):
  try:
   logger.debug('remove_job id:%s',serve_id)
   job=db.session.query(ModelRcloneServe).filter_by(id=serve_id).first()
   db.session.delete(job)
   db.session.commit()
   return 'success'
  except X as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
