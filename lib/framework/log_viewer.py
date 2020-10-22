import os
E=None
P=Exception
tD=super
Y=False
f=True
tj=open
td=classmethod
tO=os.SEEK_END
b=os.path
import traceback
t=traceback.format_exc
import time
tU=time.sleep
import threading
tY=threading.Thread
from flask import request
tJ=request.sid
from flask_socketio import SocketIO,emit
from framework import app,socketio,path_data,logger
o=logger.error
M=logger.debug
tv=socketio.emit
tI=socketio.on
from framework.logger import get_logger
from framework.util import SingletonClass
namespace='log'
@tI('connect',namespace='/%s'%namespace)
def socket_connect():
 M('log connect')
@tI('start',namespace='/%s'%namespace)
def socket_file(data):
 try:
  package=filename=E
  if 'package' in data:
   package=data['package']
  else:
   filename=data['filename']
  LogViewer.instance().start(package,filename,tJ)
  M('start package:%s filename:%s sid:%s',package,filename,tJ)
 except P as e:
  o('Exception:%s',e)
  o(t())
@tI('disconnect',namespace='/%s'%namespace)
def disconnect():
 try:
  LogViewer.instance().disconnect(tJ)
  M('disconnect sid:%s',tJ)
 except P as e:
  o('Exception:%s',e)
  o(t())
class WatchThread(tY):
 def __init__(self,package,filename):
  tD(WatchThread,self).__init__()
  self.stop_flag=Y
  self.package=package
  self.filename=filename
  self.daemon=f
 def stop(self):
  self.stop_flag=f
 def run(self):
  M('WatchThread.. Start %s',self.package)
  if self.package is not E:
   logfile=b.join(path_data,'log','%s.log'%self.package)
   key='package'
   value=self.package
  else:
   logfile=b.join(path_data,'log',self.filename)
   key='filename'
   value=self.filename
  if b.exists(logfile):
   with tj(logfile,'r')as f:
    f.seek(0,tO)
    while not self.stop_flag:
     line=f.readline()
     if not line:
      tU(0.1)
      continue
     tv("add",{key:value,'data':line},namespace='/log',broadcast=f)
   M('WatchThread.. End %s',value)
  else:
   tv("add",{key:value,'data':'not exist logfile'},namespace='/log',broadcast=f)
class LogViewer(SingletonClass):
 watch_list={}
 @td
 def start(cls,package,filename,sid):
  def thread_function():
   if package is not E:
    logfile=b.join(path_data,'log','%s.log'%package)
   else:
    logfile=b.join(path_data,'log',filename)
   if b.exists(logfile):
    ins_file=tj(logfile,'r') 
    line=ins_file.read()
    tv("on_start",{'data':line},namespace='/log')
    M('on_start end')
   else:
    tv("on_start",{'data':'not exist logfile'},namespace='/log')
  if package is not E:
   key=package
  else:
   key=filename
  thread=tY(target=thread_function,args=())
  thread.daemon=f
  thread.start()
  if key not in cls.watch_list:
   cls.watch_list[key]={}
   cls.watch_list[key]['sid']=[]
   cls.watch_list[key]['thread']=WatchThread(package,filename)
   cls.watch_list[key]['thread'].start()
  cls.watch_list[key]['sid'].append(sid)
 @td
 def disconnect(cls,sid):
  find=Y
  find_key=E
  for key,value in cls.watch_list.items():
   M('key:%s value:%s',key,value)
   for s in value['sid']:
    if sid==s:
     find=f
     find_key=key
     value['sid'].remove(s)
     break
   if find:
    break
  if not find:
   return
  if not cls.watch_list[find_key]['sid']:
   M('thread kill')
   cls.watch_list[find_key]['thread'].stop()
   del cls.watch_list[find_key]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
