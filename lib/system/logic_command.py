import os
c=object
y=None
s=staticmethod
q=True
X=False
a=Exception
h=str
k=iter
d=format
Q=enumerate
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
 commands=y
 process=y
 stdout_queue=y
 thread=y
 send_to_ui_thread=y
 return_log=y
 @s
 def start(title,commands,clear=q,wait=X,show_modal=q):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",y,namespace='/framework',broadcast=q)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(q)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except a as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @s
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",y,namespace='/framework',broadcast=q)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=q)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=q)
     os.system(command[1])
    else:
     show_command=q
     if command[0]=='hide':
      show_command=X
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=q,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not y:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except a as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=q)
    socketio.emit("command_modal_add_text",h(xception),namespace='/framework',broadcast=q)
    socketio.emit("command_modal_add_text",h(traceback.format_exc()),namespace='/framework',broadcast=q)
 @s
 def start_communicate(current_command,show_command=q):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=X)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while q:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(y)
      break
    logger.debug('END RDR')
    queue.put(y)
    time.sleep(1)
   def clct():
    active=q
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is y:
      break
     try:
      while q:
       r1=queue.get(timeout=0.005)
       if r1 is y:
        active=X
        break
       else:
        r+=r1
     except:
      pass
     if r is not y:
      try:
       r=r.decode('utf-8')
      except a as exception:
       try:
        r=r.decode('cp949')
       except a as exception:
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
    th.setDaemon(q)
    th.start()
  Pump(sout)
 @s
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=q)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=q)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=q)
   SystemLogicCommand.send_to_ui_thread=y
   SystemLogicCommand.stdout_queue=y
   SystemLogicCommand.process=y
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is y:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @s
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not y and SystemLogicCommand.process.poll()is y:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=q):
     proc.kill()
    SystemLogicCommand.process.kill()
  except a as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @s
 def execute_command_return(command,d=y,force_log=X):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=q,bufsize=1)
   ret=[]
   with process.stdout:
    for line in k(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if d is y:
    ret2='\n'.join(ret)
   elif d=='json':
    try:
     index=0
     for idx,tmp in Q(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=y
   return ret2
  except a as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
