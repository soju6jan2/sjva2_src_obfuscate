import os
m=object
j=None
h=staticmethod
z=True
r=False
e=Exception
g=str
x=iter
b=format
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
class SystemLogicCommand(m):
 commands=j
 process=j
 stdout_queue=j
 thread=j
 send_to_ui_thread=j
 return_log=j
 @h
 def start(title,commands,clear=z,wait=r,show_modal=z):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",j,namespace='/framework',broadcast=z)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(z)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @h
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",j,namespace='/framework',broadcast=z)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=z)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=z)
     os.system(command[1])
    else:
     show_command=z
     if command[0]=='hide':
      show_command=r
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=z,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not j:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except e as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=z)
    socketio.emit("command_modal_add_text",g(xception),namespace='/framework',broadcast=z)
    socketio.emit("command_modal_add_text",g(traceback.format_exc()),namespace='/framework',broadcast=z)
 @h
 def start_communicate(current_command,show_command=z):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=r)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while z:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(j)
      break
    logger.debug('END RDR')
    queue.put(j)
    time.sleep(1)
   def clct():
    active=z
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is j:
      break
     try:
      while z:
       r1=queue.get(timeout=0.005)
       if r1 is j:
        active=r
        break
       else:
        r+=r1
     except:
      pass
     if r is not j:
      try:
       r=r.decode('utf-8')
      except e as exception:
       try:
        r=r.decode('cp949')
       except e as exception:
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
    th.setDaemon(z)
    th.start()
  Pump(sout)
 @h
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=z)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=z)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=z)
   SystemLogicCommand.send_to_ui_thread=j
   SystemLogicCommand.stdout_queue=j
   SystemLogicCommand.process=j
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is j:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @h
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not j and SystemLogicCommand.process.poll()is j:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=z):
     proc.kill()
    SystemLogicCommand.process.kill()
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @h
 def execute_command_return(command,b=j,force_log=r):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=z,bufsize=1)
   ret=[]
   with process.stdout:
    for line in x(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if b is j:
    ret2='\n'.join(ret)
   elif b=='json':
    try:
     index=0
     for idx,tmp in U(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=j
   return ret2
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
