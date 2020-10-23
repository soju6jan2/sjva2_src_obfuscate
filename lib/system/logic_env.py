import os
h=object
N=staticmethod
W=Exception
i=False
j=open
A=True
import traceback
import logging
import platform
import time
import threading
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from celery.exceptions import TimeoutError,NotRegistered
from framework.logger import get_logger
from framework import path_app_root,path_data,celery,app
from.plugin import logger,package_name
from.model import ModelSetting
class SystemLogicEnv(h):
 @N
 def load_export():
  try:
   from framework.common.util import read_file
   f=os.path.join(path_app_root,'export.sh')
   if os.path.exists(f):
    return read_file(f)
  except W as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @N
 def process_ajax(sub,req):
  ret=i
  try:
   if sub=='setting_save':
    data=req.form['export']
    data=data.replace("\r\n","\n").replace("\r","\n")
    ret=i
    if platform.system()!='Windows':
     f=os.path.join(path_app_root,'export.sh')
     with j(f,'w')as f:
      f.write(data)
     ret=A
   elif sub=='ps':
    def func():
     import system
     commands=[['msg',u'잠시만 기다려주세요.'],['ps','-ef'],['top','-n1']]
     system.SystemLogicCommand.start('ps',commands)
    t=threading.Thread(target=func,args=())
    t.setDaemon(A)
    t.start()
   elif sub=='celery_test':
    ret=SystemLogicEnv.celery_test()
   elif sub=='worker_start':
    os.system('sh worker_start.sh &')
    """
                def func():
                    import system
                    commands = [['msg', u'잠시만 기다려주세요.'], ['sh', 'worker_start.sh'], ]
                    #commands.append(['msg', u'설치가 완료되었습니다.'])
                    system.SystemLogicCommand.start('ps', commands)
                t = threading.Thread(target=func, args=())
                t.setDaemon(True)
                t.start()
                """    
    ret=A
  except W as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return jsonify(ret)
 @N
 def celery_test():
  if app.config['config']['use_celery']:
   from celery import Celery
   data={}
   try:
    result=SystemLogicEnv.celery_test2.apply_async()
    logger.debug(result)
    try:
     tmp=result.get(timeout=5,propagate=A)
    except W as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc())
    data['ret']='success'
    data['data']=tmp
   except TimeoutError:
    data['ret']='timeout'
    data['data']=u'celery가 동작중이 아니거나 모든 프로세스가 작업중입니다.'
   except NotRegistered:
    data['ret']='not_registered'
    data['data']=u'Not Registered'
  else:
   data['ret']='no_celery'
   data['data']=u'celery 실행환경이 아닙니다.'
  return data
 @N
 @celery.task
 def celery_test2():
  try:
   logger.debug('!!!! celery_test2222')
   import time
   time.sleep(1)
   data=u'정상입니다. 이 메시지는 celery 에서 반환됩니다. '
   return data
  except W as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
