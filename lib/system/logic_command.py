import os
f=object
W=None
v=staticmethod
k=True
C=False
V=Exception
A=str
I=iter
G=format
U=enumerate
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
class SystemLogicCommand(f):
 commands=W
 process=W
 stdout_queue=W
 thread=W
 send_to_ui_thread=W
 return_log=W
 @v
 def start(title,commands,clear=k,wait=C,show_modal=k):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",W,namespace='/framework',broadcast=k)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(k)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @v
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",W,namespace='/framework',broadcast=k)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=k)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=k)
     os.system(command[1])
    else:
     show_command=k
     if command[0]=='hide':
      show_command=C
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=k,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not W:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except V as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=k)
    socketio.emit("command_modal_add_text",A(xception),namespace='/framework',broadcast=k)
    socketio.emit("command_modal_add_text",A(traceback.format_exc()),namespace='/framework',broadcast=k)
 @v
 def start_communicate(current_command,show_command=k):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=C)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while k:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(W)
      break
    logger.debug('END RDR')
    queue.put(W)
    time.sleep(1)
   def clct():
    active=k
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is W:
      break
     try:
      while k:
       r1=queue.get(timeout=0.005)
       if r1 is W:
        active=C
        break
       else:
        r+=r1
     except:
      pass
     if r is not W:
      try:
       r=r.decode('utf-8')
      except V as exception:
       try:
        r=r.decode('cp949')
       except V as exception:
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
    th.setDaemon(k)
    th.start()
  Pump(sout)
 @v
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=k)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=k)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=k)
   SystemLogicCommand.send_to_ui_thread=W
   SystemLogicCommand.stdout_queue=W
   SystemLogicCommand.process=W
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is W:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @v
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not W and SystemLogicCommand.process.poll()is W:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=k):
     proc.kill()
    SystemLogicCommand.process.kill()
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @v
 def execute_command_return(command,G=W,force_log=C):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=k,bufsize=1)
   ret=[]
   with process.stdout:
    for line in I(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if G is W:
    ret2='\n'.join(ret)
   elif G=='json':
    try:
     index=0
     for idx,tmp in U(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=W
   return ret2
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
