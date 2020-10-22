import os
w=object
m=None
K=staticmethod
Q=True
a=False
A=Exception
v=str
D=iter
k=format
Y=enumerate
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
class SystemLogicCommand(w):
 commands=m
 process=m
 stdout_queue=m
 thread=m
 send_to_ui_thread=m
 return_log=m
 @K
 def start(title,commands,clear=Q,wait=a,show_modal=Q):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",m,namespace='/framework',broadcast=Q)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(Q)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except A as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @K
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",m,namespace='/framework',broadcast=Q)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=Q)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=Q)
     os.system(command[1])
    else:
     show_command=Q
     if command[0]=='hide':
      show_command=a
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=Q,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not m:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except A as e:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=Q)
    socketio.emit("command_modal_add_text",v(e),namespace='/framework',broadcast=Q)
    socketio.emit("command_modal_add_text",v(traceback.format_exc()),namespace='/framework',broadcast=Q)
 @K
 def start_communicate(current_command,show_command=Q):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=a)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while Q:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(m)
      break
    logger.debug('END RDR')
    queue.put(m)
    time.sleep(1)
   def clct():
    active=Q
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is m:
      break
     try:
      while Q:
       r1=queue.get(timeout=0.005)
       if r1 is m:
        active=a
        break
       else:
        r+=r1
     except:
      pass
     if r is not m:
      try:
       r=r.decode('utf-8')
      except A as e:
       try:
        r=r.decode('cp949')
       except A as e:
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
    th.setDaemon(Q)
    th.start()
  Pump(sout)
 @K
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=Q)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=Q)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=Q)
   SystemLogicCommand.send_to_ui_thread=m
   SystemLogicCommand.stdout_queue=m
   SystemLogicCommand.process=m
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is m:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @K
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not m and SystemLogicCommand.process.poll()is m:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=Q):
     proc.kill()
    SystemLogicCommand.process.kill()
  except A as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @K
 def execute_command_return(command,k=m,force_log=a):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=Q,bufsize=1)
   ret=[]
   with process.stdout:
    for line in D(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if k is m:
    ret2='\n'.join(ret)
   elif k=='json':
    try:
     index=0
     for idx,tmp in Y(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=m
   return ret2
  except A as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
