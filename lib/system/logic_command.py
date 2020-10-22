import os
v=object
D=None
j=staticmethod
i=True
b=False
V=Exception
K=str
r=iter
U=format
z=enumerate
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
class SystemLogicCommand(v):
 commands=D
 process=D
 stdout_queue=D
 thread=D
 send_to_ui_thread=D
 return_log=D
 @j
 def start(title,commands,clear=i,wait=b,show_modal=i):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",D,namespace='/framework',broadcast=i)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(i)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except V as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @j
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",D,namespace='/framework',broadcast=i)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=i)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=i)
     os.system(command[1])
    else:
     show_command=i
     if command[0]=='hide':
      show_command=b
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=i,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not D:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except V as e:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=i)
    socketio.emit("command_modal_add_text",K(e),namespace='/framework',broadcast=i)
    socketio.emit("command_modal_add_text",K(traceback.format_exc()),namespace='/framework',broadcast=i)
 @j
 def start_communicate(current_command,show_command=i):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=b)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while i:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(D)
      break
    logger.debug('END RDR')
    queue.put(D)
    time.sleep(1)
   def clct():
    active=i
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is D:
      break
     try:
      while i:
       r1=queue.get(timeout=0.005)
       if r1 is D:
        active=b
        break
       else:
        r+=r1
     except:
      pass
     if r is not D:
      try:
       r=r.decode('utf-8')
      except V as e:
       try:
        r=r.decode('cp949')
       except V as e:
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
    th.setDaemon(i)
    th.start()
  Pump(sout)
 @j
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=i)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=i)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=i)
   SystemLogicCommand.send_to_ui_thread=D
   SystemLogicCommand.stdout_queue=D
   SystemLogicCommand.process=D
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is D:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @j
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not D and SystemLogicCommand.process.poll()is D:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=i):
     proc.kill()
    SystemLogicCommand.process.kill()
  except V as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @j
 def execute_command_return(command,U=D,force_log=b):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=i,bufsize=1)
   ret=[]
   with process.stdout:
    for line in r(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if U is D:
    ret2='\n'.join(ret)
   elif U=='json':
    try:
     index=0
     for idx,tmp in z(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=D
   return ret2
  except V as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
