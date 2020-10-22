import os
s=object
z=None
J=staticmethod
h=True
x=False
Q=Exception
G=str
X=iter
S=format
I=enumerate
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
class SystemLogicCommand(s):
 commands=z
 process=z
 stdout_queue=z
 thread=z
 send_to_ui_thread=z
 return_log=z
 @J
 def start(title,commands,clear=h,wait=x,show_modal=h):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",z,namespace='/framework',broadcast=h)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(h)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except Q as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @J
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",z,namespace='/framework',broadcast=h)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=h)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=h)
     os.system(command[1])
    else:
     show_command=h
     if command[0]=='hide':
      show_command=x
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=h,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not z:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except Q as e:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=h)
    socketio.emit("command_modal_add_text",G(e),namespace='/framework',broadcast=h)
    socketio.emit("command_modal_add_text",G(traceback.format_exc()),namespace='/framework',broadcast=h)
 @J
 def start_communicate(current_command,show_command=h):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=x)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while h:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(z)
      break
    logger.debug('END RDR')
    queue.put(z)
    time.sleep(1)
   def clct():
    active=h
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is z:
      break
     try:
      while h:
       r1=queue.get(timeout=0.005)
       if r1 is z:
        active=x
        break
       else:
        r+=r1
     except:
      pass
     if r is not z:
      try:
       r=r.decode('utf-8')
      except Q as e:
       try:
        r=r.decode('cp949')
       except Q as e:
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
    th.setDaemon(h)
    th.start()
  Pump(sout)
 @J
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=h)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=h)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=h)
   SystemLogicCommand.send_to_ui_thread=z
   SystemLogicCommand.stdout_queue=z
   SystemLogicCommand.process=z
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is z:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @J
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not z and SystemLogicCommand.process.poll()is z:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=h):
     proc.kill()
    SystemLogicCommand.process.kill()
  except Q as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @J
 def execute_command_return(command,S=z,force_log=x):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=h,bufsize=1)
   ret=[]
   with process.stdout:
    for line in X(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if S is z:
    ret2='\n'.join(ret)
   elif S=='json':
    try:
     index=0
     for idx,tmp in I(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=z
   return ret2
  except Q as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
