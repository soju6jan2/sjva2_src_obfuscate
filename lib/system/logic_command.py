import os
y=object
w=None
v=staticmethod
c=True
T=False
A=Exception
B=str
I=iter
Q=format
R=enumerate
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
class SystemLogicCommand(y):
 commands=w
 process=w
 stdout_queue=w
 thread=w
 send_to_ui_thread=w
 return_log=w
 @v
 def start(title,commands,clear=c,wait=T,show_modal=c):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",w,namespace='/framework',broadcast=c)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(c)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except A as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @v
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",w,namespace='/framework',broadcast=c)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=c)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=c)
     os.system(command[1])
    else:
     show_command=c
     if command[0]=='hide':
      show_command=T
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=c,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not w:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except A as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=c)
    socketio.emit("command_modal_add_text",B(xception),namespace='/framework',broadcast=c)
    socketio.emit("command_modal_add_text",B(traceback.format_exc()),namespace='/framework',broadcast=c)
 @v
 def start_communicate(current_command,show_command=c):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=T)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while c:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(w)
      break
    logger.debug('END RDR')
    queue.put(w)
    time.sleep(1)
   def clct():
    active=c
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is w:
      break
     try:
      while c:
       r1=queue.get(timeout=0.005)
       if r1 is w:
        active=T
        break
       else:
        r+=r1
     except:
      pass
     if r is not w:
      try:
       r=r.decode('utf-8')
      except A as exception:
       try:
        r=r.decode('cp949')
       except A as exception:
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
    th.setDaemon(c)
    th.start()
  Pump(sout)
 @v
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=c)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=c)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=c)
   SystemLogicCommand.send_to_ui_thread=w
   SystemLogicCommand.stdout_queue=w
   SystemLogicCommand.process=w
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is w:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @v
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not w and SystemLogicCommand.process.poll()is w:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=c):
     proc.kill()
    SystemLogicCommand.process.kill()
  except A as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @v
 def execute_command_return(command,Q=w,force_log=T):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=c,bufsize=1)
   ret=[]
   with process.stdout:
    for line in I(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if Q is w:
    ret2='\n'.join(ret)
   elif Q=='json':
    try:
     index=0
     for idx,tmp in R(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=w
   return ret2
  except A as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
