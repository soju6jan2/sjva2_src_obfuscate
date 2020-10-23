import os
M=object
N=None
c=staticmethod
J=True
f=False
U=Exception
D=str
b=iter
s=format
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
class SystemLogicCommand(M):
 commands=N
 process=N
 stdout_queue=N
 thread=N
 send_to_ui_thread=N
 return_log=N
 @c
 def start(title,commands,clear=J,wait=f,show_modal=J):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",N,namespace='/framework',broadcast=J)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(J)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except U as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @c
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",N,namespace='/framework',broadcast=J)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=J)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=J)
     os.system(command[1])
    else:
     show_command=J
     if command[0]=='hide':
      show_command=f
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=J,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not N:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except U as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=J)
    socketio.emit("command_modal_add_text",D(xception),namespace='/framework',broadcast=J)
    socketio.emit("command_modal_add_text",D(traceback.format_exc()),namespace='/framework',broadcast=J)
 @c
 def start_communicate(current_command,show_command=J):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=f)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while J:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(N)
      break
    logger.debug('END RDR')
    queue.put(N)
    time.sleep(1)
   def clct():
    active=J
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is N:
      break
     try:
      while J:
       r1=queue.get(timeout=0.005)
       if r1 is N:
        active=f
        break
       else:
        r+=r1
     except:
      pass
     if r is not N:
      try:
       r=r.decode('utf-8')
      except U as exception:
       try:
        r=r.decode('cp949')
       except U as exception:
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
    th.setDaemon(J)
    th.start()
  Pump(sout)
 @c
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=J)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=J)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=J)
   SystemLogicCommand.send_to_ui_thread=N
   SystemLogicCommand.stdout_queue=N
   SystemLogicCommand.process=N
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is N:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @c
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not N and SystemLogicCommand.process.poll()is N:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=J):
     proc.kill()
    SystemLogicCommand.process.kill()
  except U as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @c
 def execute_command_return(command,s=N,force_log=f):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=J,bufsize=1)
   ret=[]
   with process.stdout:
    for line in b(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if s is N:
    ret2='\n'.join(ret)
   elif s=='json':
    try:
     index=0
     for idx,tmp in Y(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=N
   return ret2
  except U as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
