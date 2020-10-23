import os
C=object
M=None
D=staticmethod
p=True
W=False
x=Exception
v=str
V=iter
d=format
t=enumerate
import traceback
import logging
import platform
import subprocess
import threading
import sys
import io
import time
import json
from framework.logger import get_logger
from framework import path_app_root,socketio,py_queue
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class SystemLogicCommand(C):
 commands=M
 process=M
 stdout_queue=M
 thread=M
 send_to_ui_thread=M
 return_log=M
 @D
 def start(title,commands,clear=p,wait=W,show_modal=p):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",M,namespace='/framework',broadcast=p)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(p)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @D
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",M,namespace='/framework',broadcast=p)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=p)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=p)
     os.system(command[1])
    else:
     show_command=p
     if command[0]=='hide':
      show_command=W
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=p,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not M:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except x as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=p)
    socketio.emit("command_modal_add_text",v(xception),namespace='/framework',broadcast=p)
    socketio.emit("command_modal_add_text",v(traceback.format_exc()),namespace='/framework',broadcast=p)
 @D
 def start_communicate(current_command,show_command=p):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=W)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while p:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(M)
      break
    logger.debug('END RDR')
    queue.put(M)
    time.sleep(1)
   def clct():
    active=p
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is M:
      break
     try:
      while p:
       r1=queue.get(timeout=0.005)
       if r1 is M:
        active=W
        break
       else:
        r+=r1
     except:
      pass
     if r is not M:
      try:
       r=r.decode('utf-8')
      except x as exception:
       try:
        r=r.decode('cp949')
       except x as exception:
        logger.error('Exception:%s',exception)
        logger.error(traceback.format_exc())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      SystemLogicCommand.stdout_queue.put(r)
      SystemLogicCommand.return_log+=r.split('\n')
      logger.debug('IN:%s',r)
    SystemLogicCommand.stdout_queue.put('<END>')
    logger.debug('END clct')
   for tgt in[rdr,clct]:
    th=threading.Thread(target=tgt)
    th.setDaemon(p)
    th.start()
  Pump(sout)
 @D
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=p)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=p)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=p)
   SystemLogicCommand.send_to_ui_thread=M
   SystemLogicCommand.stdout_queue=M
   SystemLogicCommand.process=M
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is M:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @D
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not M and SystemLogicCommand.process.poll()is M:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=p):
     proc.kill()
    SystemLogicCommand.process.kill()
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @D
 def execute_command_return(command,d=M,force_log=W):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=p,bufsize=1)
   ret=[]
   with process.stdout:
    for line in V(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if d is M:
    ret2='\n'.join(ret)
   elif d=='json':
    try:
     index=0
     for idx,tmp in t(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=M
   return ret2
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
