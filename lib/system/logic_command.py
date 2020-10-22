import os
c=object
C=None
V=staticmethod
F=True
l=False
H=Exception
M=str
e=iter
A=format
X=enumerate
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
class SystemLogicCommand(c):
 commands=C
 process=C
 stdout_queue=C
 thread=C
 send_to_ui_thread=C
 return_log=C
 @V
 def start(title,commands,clear=F,wait=l,show_modal=F):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",C,namespace='/framework',broadcast=F)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(F)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @V
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",C,namespace='/framework',broadcast=F)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=F)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=F)
     os.system(command[1])
    else:
     show_command=F
     if command[0]=='hide':
      show_command=l
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=F,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not C:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except H as e:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=F)
    socketio.emit("command_modal_add_text",M(e),namespace='/framework',broadcast=F)
    socketio.emit("command_modal_add_text",M(traceback.format_exc()),namespace='/framework',broadcast=F)
 @V
 def start_communicate(current_command,show_command=F):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=l)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while F:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(C)
      break
    logger.debug('END RDR')
    queue.put(C)
    time.sleep(1)
   def clct():
    active=F
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is C:
      break
     try:
      while F:
       r1=queue.get(timeout=0.005)
       if r1 is C:
        active=l
        break
       else:
        r+=r1
     except:
      pass
     if r is not C:
      try:
       r=r.decode('utf-8')
      except H as e:
       try:
        r=r.decode('cp949')
       except H as e:
        logger.error('Exception:%s',e)
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
    th.setDaemon(F)
    th.start()
  Pump(sout)
 @V
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=F)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=F)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=F)
   SystemLogicCommand.send_to_ui_thread=C
   SystemLogicCommand.stdout_queue=C
   SystemLogicCommand.process=C
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is C:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @V
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not C and SystemLogicCommand.process.poll()is C:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=F):
     proc.kill()
    SystemLogicCommand.process.kill()
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @V
 def execute_command_return(command,A=C,force_log=l):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=F,bufsize=1)
   ret=[]
   with process.stdout:
    for line in e(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if A is C:
    ret2='\n'.join(ret)
   elif A=='json':
    try:
     index=0
     for idx,tmp in X(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=C
   return ret2
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
