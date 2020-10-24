import os
P=object
s=None
e=staticmethod
W=True
U=False
J=Exception
Y=str
X=iter
T=format
i=enumerate
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
class SystemLogicCommand(P):
 commands=s
 process=s
 stdout_queue=s
 thread=s
 send_to_ui_thread=s
 return_log=s
 @e
 def start(title,commands,clear=W,wait=U,show_modal=W):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",s,namespace='/framework',broadcast=W)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(W)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except J as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @e
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",s,namespace='/framework',broadcast=W)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=W)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=W)
     os.system(command[1])
    else:
     show_command=W
     if command[0]=='hide':
      show_command=U
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=W,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not s:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except J as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=W)
    socketio.emit("command_modal_add_text",Y(xception),namespace='/framework',broadcast=W)
    socketio.emit("command_modal_add_text",Y(traceback.format_exc()),namespace='/framework',broadcast=W)
 @e
 def start_communicate(current_command,show_command=W):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=U)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while W:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(s)
      break
    logger.debug('END RDR')
    queue.put(s)
    time.sleep(1)
   def clct():
    active=W
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is s:
      break
     try:
      while W:
       r1=queue.get(timeout=0.005)
       if r1 is s:
        active=U
        break
       else:
        r+=r1
     except:
      pass
     if r is not s:
      try:
       r=r.decode('utf-8')
      except J as exception:
       try:
        r=r.decode('cp949')
       except J as exception:
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
    th.setDaemon(W)
    th.start()
  Pump(sout)
 @e
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=W)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=W)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=W)
   SystemLogicCommand.send_to_ui_thread=s
   SystemLogicCommand.stdout_queue=s
   SystemLogicCommand.process=s
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is s:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @e
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not s and SystemLogicCommand.process.poll()is s:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=W):
     proc.kill()
    SystemLogicCommand.process.kill()
  except J as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @e
 def execute_command_return(command,T=s,force_log=U):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=W,bufsize=1)
   ret=[]
   with process.stdout:
    for line in X(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if T is s:
    ret2='\n'.join(ret)
   elif T=='json':
    try:
     index=0
     for idx,tmp in i(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=s
   return ret2
  except J as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
