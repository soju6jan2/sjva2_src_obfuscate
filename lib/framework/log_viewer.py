import os
E=None
J=Exception
OU=super
i=False
R=True
Ol=open
OQ=classmethod
Oj=os.SEEK_END
k=os.path
import traceback
O=traceback.format_exc
import time
OY=time.sleep
import threading
Oi=threading.Thread
from flask import request
Or=request.sid
from flask_socketio import SocketIO,emit
from framework import app,socketio,path_data,logger
B=logger.error
G=logger.debug
OF=socketio.emit
OV=socketio.on
from framework.logger import get_logger
from framework.util import SingletonClass
namespace='log'
@OV('connect',namespace='/%s'%namespace)
def socket_connect():
 G('log connect')
@OV('start',namespace='/%s'%namespace)
def socket_file(data):
 try:
  package=filename=E
  if 'package' in data:
   package=data['package']
  else:
   filename=data['filename']
  LogViewer.instance().start(package,filename,Or)
  G('start package:%s filename:%s sid:%s',package,filename,Or)
 except J as e:
  B('Exception:%s',e)
  B(O())
@OV('disconnect',namespace='/%s'%namespace)
def disconnect():
 try:
  LogViewer.instance().disconnect(Or)
  G('disconnect sid:%s',Or)
 except J as e:
  B('Exception:%s',e)
  B(O())
class WatchThread(Oi):
 def __init__(self,package,filename):
  OU(WatchThread,self).__init__()
  self.stop_flag=i
  self.package=package
  self.filename=filename
  self.daemon=R
 def stop(self):
  self.stop_flag=R
 def run(self):
  G('WatchThread.. Start %s',self.package)
  if self.package is not E:
   logfile=k.join(path_data,'log','%s.log'%self.package)
   key='package'
   value=self.package
  else:
   logfile=k.join(path_data,'log',self.filename)
   key='filename'
   value=self.filename
  if k.exists(logfile):
   with Ol(logfile,'r')as f:
    f.seek(0,Oj)
    while not self.stop_flag:
     line=f.readline()
     if not line:
      OY(0.1)
      continue
     OF("add",{key:value,'data':line},namespace='/log',broadcast=R)
   G('WatchThread.. End %s',value)
  else:
   OF("add",{key:value,'data':'not exist logfile'},namespace='/log',broadcast=R)
class LogViewer(SingletonClass):
 watch_list={}
 @OQ
 def start(cls,package,filename,sid):
  def thread_function():
   if package is not E:
    logfile=k.join(path_data,'log','%s.log'%package)
   else:
    logfile=k.join(path_data,'log',filename)
   if k.exists(logfile):
    ins_file=Ol(logfile,'r') 
    line=ins_file.read()
    OF("on_start",{'data':line},namespace='/log')
    G('on_start end')
   else:
    OF("on_start",{'data':'not exist logfile'},namespace='/log')
  if package is not E:
   key=package
  else:
   key=filename
  thread=Oi(target=thread_function,args=())
  thread.daemon=R
  thread.start()
  if key not in cls.watch_list:
   cls.watch_list[key]={}
   cls.watch_list[key]['sid']=[]
   cls.watch_list[key]['thread']=WatchThread(package,filename)
   cls.watch_list[key]['thread'].start()
  cls.watch_list[key]['sid'].append(sid)
 @OQ
 def disconnect(cls,sid):
  find=i
  find_key=E
  for key,value in cls.watch_list.items():
   G('key:%s value:%s',key,value)
   for s in value['sid']:
    if sid==s:
     find=R
     find_key=key
     value['sid'].remove(s)
     break
   if find:
    break
  if not find:
   return
  if not cls.watch_list[find_key]['sid']:
   G('thread kill')
   cls.watch_list[find_key]['thread'].stop()
   del cls.watch_list[find_key]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
