import os
h=object
f=None
N=staticmethod
A=True
i=False
W=Exception
z=str
U=iter
Q=format
H=enumerate
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
class SystemLogicCommand(h):
 commands=f
 process=f
 stdout_queue=f
 thread=f
 send_to_ui_thread=f
 return_log=f
 @N
 def start(title,commands,clear=A,wait=i,show_modal=A):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",f,namespace='/framework',broadcast=A)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(A)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except W as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @N
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",f,namespace='/framework',broadcast=A)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=A)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=A)
     os.system(command[1])
    else:
     show_command=A
     if command[0]=='hide':
      show_command=i
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=A,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not f:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except W as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=A)
    socketio.emit("command_modal_add_text",z(xception),namespace='/framework',broadcast=A)
    socketio.emit("command_modal_add_text",z(traceback.format_exc()),namespace='/framework',broadcast=A)
 @N
 def start_communicate(current_command,show_command=A):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=i)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while A:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(f)
      break
    logger.debug('END RDR')
    queue.put(f)
    time.sleep(1)
   def clct():
    active=A
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is f:
      break
     try:
      while A:
       r1=queue.get(timeout=0.005)
       if r1 is f:
        active=i
        break
       else:
        r+=r1
     except:
      pass
     if r is not f:
      try:
       r=r.decode('utf-8')
      except W as exception:
       try:
        r=r.decode('cp949')
       except W as exception:
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
    th.setDaemon(A)
    th.start()
  Pump(sout)
 @N
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=A)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=A)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=A)
   SystemLogicCommand.send_to_ui_thread=f
   SystemLogicCommand.stdout_queue=f
   SystemLogicCommand.process=f
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is f:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @N
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not f and SystemLogicCommand.process.poll()is f:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=A):
     proc.kill()
    SystemLogicCommand.process.kill()
  except W as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @N
 def execute_command_return(command,Q=f,force_log=i):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=A,bufsize=1)
   ret=[]
   with process.stdout:
    for line in U(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if Q is f:
    ret2='\n'.join(ret)
   elif Q=='json':
    try:
     index=0
     for idx,tmp in H(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=f
   return ret2
  except W as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
