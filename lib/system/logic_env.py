import os
L=object
N=staticmethod
e=Exception
j=False
k=open
o=True
l=os.system
a=os.path
import traceback
H=traceback.format_exc
import logging
import platform
m=platform.system
import time
R=time.sleep
import threading
i=threading.Thread
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from r import TimeoutError,NotRegistered
from framework.logger import get_logger
from framework import path_app_root,path_data,celery,app
X=app.config
U=celery.task
r=celery.exceptions
from.plugin import logger,package_name
G=logger.debug
J=logger.error
from.model import ModelSetting
class SystemLogicEnv(L):
 @N
 def load_export():
  try:
   from framework.common.util import read_file
   f=a.join(path_app_root,'export.sh')
   if a.exists(f):
    return read_file(f)
  except e as e:
   J('Exception:%s',e)
   J(H()) 
 @N
 def process_ajax(sub,req):
  ret=j
  try:
   if sub=='setting_save':
    data=req.form['export']
    data=data.replace("\r\n","\n").replace("\r","\n")
    ret=j
    if m()!='Windows':
     f=a.join(path_app_root,'export.sh')
     with k(f,'w')as f:
      f.write(data)
     ret=o
   elif sub=='ps':
    def func():
     import system
     commands=[['msg',u'잠시만 기다려주세요.'],['ps','-ef'],['top','-n1']]
     system.SystemLogicCommand.start('ps',commands)
    t=i(target=func,args=())
    t.setDaemon(o)
    t.start()
   elif sub=='celery_test':
    ret=SystemLogicEnv.celery_test()
   elif sub=='worker_start':
    l('sh worker_start.sh &')
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
    ret=o
  except e as e:
   J('Exception:%s',e)
   J(H())
  return jsonify(ret)
 @N
 def celery_test():
  if X['config']['use_celery']:
   from celery import Celery
   data={}
   try:
    result=SystemLogicEnv.celery_test2.apply_async()
    G(result)
    try:
     tmp=result.get(timeout=5,propagate=o)
    except e as e:
     J('Exception:%s',e)
     J(H())
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
 @U
 def celery_test2():
  try:
   G('!!!! celery_test2222')
   import time
   R(1)
      R=time.sleep
   data=u'정상입니다. 이 메시지는 celery 에서 반환됩니다. '
   return data
  except e as e:
   J('Exception:%s',e)
   J(H())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
