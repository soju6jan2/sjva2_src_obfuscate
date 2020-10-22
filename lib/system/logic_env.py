import os
I=object
h=staticmethod
j=Exception
C=False
s=open
i=True
J=os.system
u=os.path
import traceback
V=traceback.format_exc
import logging
import platform
m=platform.system
import time
T=time.sleep
import threading
v=threading.Thread
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from E import TimeoutError,NotRegistered
from framework.logger import get_logger
from framework import path_app_root,path_data,celery,app
A=app.config
N=celery.task
E=celery.exceptions
from.plugin import logger,package_name
o=logger.debug
D=logger.error
from.model import ModelSetting
class SystemLogicEnv(I):
 @h
 def load_export():
  try:
   from framework.common.util import read_file
   f=u.join(path_app_root,'export.sh')
   if u.exists(f):
    return read_file(f)
  except j as e:
   D('Exception:%s',e)
   D(V()) 
 @h
 def process_ajax(sub,req):
  ret=C
  try:
   if sub=='setting_save':
    data=req.form['export']
    data=data.replace("\r\n","\n").replace("\r","\n")
    ret=C
    if m()!='Windows':
     f=u.join(path_app_root,'export.sh')
     with s(f,'w')as f:
      f.write(data)
     ret=i
   elif sub=='ps':
    def func():
     import system
     commands=[['msg',u'잠시만 기다려주세요.'],['ps','-ef'],['top','-n1']]
     system.SystemLogicCommand.start('ps',commands)
    t=v(target=func,args=())
    t.setDaemon(i)
    t.start()
   elif sub=='celery_test':
    ret=SystemLogicEnv.celery_test()
   elif sub=='worker_start':
    J('sh worker_start.sh &')
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
    ret=i
  except j as e:
   D('Exception:%s',e)
   D(V())
  return jsonify(ret)
 @h
 def celery_test():
  if A['config']['use_celery']:
   from celery import Celery
   data={}
   try:
    result=SystemLogicEnv.celery_test2.apply_async()
    o(result)
    try:
     tmp=result.get(timeout=5,propagate=i)
    except j as e:
     D('Exception:%s',e)
     D(V())
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
 @h
 @N
 def celery_test2():
  try:
   o('!!!! celery_test2222')
   import time
   T(1)
      T=time.sleep
   data=u'정상입니다. 이 메시지는 celery 에서 반환됩니다. '
   return data
  except j as e:
   D('Exception:%s',e)
   D(V())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
