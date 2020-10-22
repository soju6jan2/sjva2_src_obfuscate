import os
E=None
h=Exception
o=super
g=False
z=True
F=open
e=classmethod
import traceback
import time
import threading
from flask import request
from flask_socketio import SocketIO,emit
from framework import app,socketio,path_data,logger
from framework.logger import get_logger
from framework.util import SingletonClass
namespace='log'
@socketio.on('connect',namespace='/%s'%namespace)
def socket_connect():
 logger.debug('log connect')
@socketio.on('start',namespace='/%s'%namespace)
def socket_file(data):
 try:
  package=filename=E
  if 'package' in data:
   package=data['package']
  else:
   filename=data['filename']
  LogViewer.instance().start(package,filename,request.sid)
  logger.debug('start package:%s filename:%s sid:%s',package,filename,request.sid)
 except h as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@socketio.on('disconnect',namespace='/%s'%namespace)
def disconnect():
 try:
  LogViewer.instance().disconnect(request.sid)
  logger.debug('disconnect sid:%s',request.sid)
 except h as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
class WatchThread(threading.Thread):
 def __init__(self,package,filename):
  o(WatchThread,self).__init__()
  self.stop_flag=g
  self.package=package
  self.filename=filename
  self.daemon=z
 def stop(self):
  self.stop_flag=z
 def run(self):
  logger.debug('WatchThread.. Start %s',self.package)
  if self.package is not E:
   logfile=os.path.join(path_data,'log','%s.log'%self.package)
   key='package'
   value=self.package
  else:
   logfile=os.path.join(path_data,'log',self.filename)
   key='filename'
   value=self.filename
  if os.path.exists(logfile):
   with F(logfile,'r')as f:
    f.seek(0,os.SEEK_END)
    while not self.stop_flag:
     line=f.readline()
     if not line:
      time.sleep(0.1)
      continue
     socketio.emit("add",{key:value,'data':line},namespace='/log',broadcast=z)
   logger.debug('WatchThread.. End %s',value)
  else:
   socketio.emit("add",{key:value,'data':'not exist logfile'},namespace='/log',broadcast=z)
class LogViewer(SingletonClass):
 watch_list={}
 @e
 def start(cls,package,filename,sid):
  def thread_function():
   if package is not E:
    logfile=os.path.join(path_data,'log','%s.log'%package)
   else:
    logfile=os.path.join(path_data,'log',filename)
   if os.path.exists(logfile):
    ins_file=F(logfile,'r') 
    line=ins_file.read()
    socketio.emit("on_start",{'data':line},namespace='/log')
    logger.debug('on_start end')
   else:
    socketio.emit("on_start",{'data':'not exist logfile'},namespace='/log')
  if package is not E:
   key=package
  else:
   key=filename
  thread=threading.Thread(target=thread_function,args=())
  thread.daemon=z
  thread.start()
  if key not in cls.watch_list:
   cls.watch_list[key]={}
   cls.watch_list[key]['sid']=[]
   cls.watch_list[key]['thread']=WatchThread(package,filename)
   cls.watch_list[key]['thread'].start()
  cls.watch_list[key]['sid'].append(sid)
 @e
 def disconnect(cls,sid):
  find=g
  find_key=E
  for key,value in cls.watch_list.items():
   logger.debug('key:%s value:%s',key,value)
   for s in value['sid']:
    if sid==s:
     find=z
     find_key=key
     value['sid'].remove(s)
     break
   if find:
    break
  if not find:
   return
  if not cls.watch_list[find_key]['sid']:
   logger.debug('thread kill')
   cls.watch_list[find_key]['thread'].stop()
   del cls.watch_list[find_key]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
