import os
E=object
G=None
U=staticmethod
r=True
f=False
A=Exception
M=str
b=iter
P=format
V=enumerate
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
class SystemLogicCommand(E):
 commands=G
 process=G
 stdout_queue=G
 thread=G
 send_to_ui_thread=G
 return_log=G
 @U
 def start(title,commands,clear=r,wait=f,show_modal=r):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",G,namespace='/framework',broadcast=r)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(r)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except A as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @U
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",G,namespace='/framework',broadcast=r)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=r)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=r)
     os.system(command[1])
    else:
     show_command=r
     if command[0]=='hide':
      show_command=f
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=r,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not G:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except A as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=r)
    socketio.emit("command_modal_add_text",M(xception),namespace='/framework',broadcast=r)
    socketio.emit("command_modal_add_text",M(traceback.format_exc()),namespace='/framework',broadcast=r)
 @U
 def start_communicate(current_command,show_command=r):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=f)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while r:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(G)
      break
    logger.debug('END RDR')
    queue.put(G)
    time.sleep(1)
   def clct():
    active=r
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is G:
      break
     try:
      while r:
       r1=queue.get(timeout=0.005)
       if r1 is G:
        active=f
        break
       else:
        r+=r1
     except:
      pass
     if r is not G:
      try:
       r=r.decode('utf-8')
      except A as exception:
       try:
        r=r.decode('cp949')
       except A as exception:
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
    th.setDaemon(r)
    th.start()
  Pump(sout)
 @U
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=r)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=r)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=r)
   SystemLogicCommand.send_to_ui_thread=G
   SystemLogicCommand.stdout_queue=G
   SystemLogicCommand.process=G
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is G:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @U
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not G and SystemLogicCommand.process.poll()is G:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=r):
     proc.kill()
    SystemLogicCommand.process.kill()
  except A as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @U
 def execute_command_return(command,P=G,force_log=f):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=r,bufsize=1)
   ret=[]
   with process.stdout:
    for line in b(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if P is G:
    ret2='\n'.join(ret)
   elif P=='json':
    try:
     index=0
     for idx,tmp in V(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=G
   return ret2
  except A as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
