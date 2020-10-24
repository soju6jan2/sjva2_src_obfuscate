import os
K=object
S=None
h=staticmethod
l=True
R=False
r=Exception
g=str
v=iter
z=format
q=enumerate
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
class SystemLogicCommand(K):
 commands=S
 process=S
 stdout_queue=S
 thread=S
 send_to_ui_thread=S
 return_log=S
 @h
 def start(title,commands,clear=l,wait=R,show_modal=l):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",S,namespace='/framework',broadcast=l)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(l)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @h
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",S,namespace='/framework',broadcast=l)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=l)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=l)
     os.system(command[1])
    else:
     show_command=l
     if command[0]=='hide':
      show_command=R
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=l,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not S:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except r as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=l)
    socketio.emit("command_modal_add_text",g(xception),namespace='/framework',broadcast=l)
    socketio.emit("command_modal_add_text",g(traceback.format_exc()),namespace='/framework',broadcast=l)
 @h
 def start_communicate(current_command,show_command=l):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=R)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while l:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(S)
      break
    logger.debug('END RDR')
    queue.put(S)
    time.sleep(1)
   def clct():
    active=l
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is S:
      break
     try:
      while l:
       r1=queue.get(timeout=0.005)
       if r1 is S:
        active=R
        break
       else:
        r+=r1
     except:
      pass
     if r is not S:
      try:
       r=r.decode('utf-8')
      except r as exception:
       try:
        r=r.decode('cp949')
       except r as exception:
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
    th.setDaemon(l)
    th.start()
  Pump(sout)
 @h
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=l)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=l)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=l)
   SystemLogicCommand.send_to_ui_thread=S
   SystemLogicCommand.stdout_queue=S
   SystemLogicCommand.process=S
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is S:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @h
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not S and SystemLogicCommand.process.poll()is S:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=l):
     proc.kill()
    SystemLogicCommand.process.kill()
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @h
 def execute_command_return(command,z=S,force_log=R):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=l,bufsize=1)
   ret=[]
   with process.stdout:
    for line in v(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if z is S:
    ret2='\n'.join(ret)
   elif z=='json':
    try:
     index=0
     for idx,tmp in q(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=S
   return ret2
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
