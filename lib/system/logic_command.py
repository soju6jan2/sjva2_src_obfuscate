import os
V=object
X=None
s=staticmethod
B=True
U=False
S=Exception
o=str
G=iter
H=format
e=enumerate
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
class SystemLogicCommand(V):
 commands=X
 process=X
 stdout_queue=X
 thread=X
 send_to_ui_thread=X
 return_log=X
 @s
 def start(title,commands,clear=B,wait=U,show_modal=B):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",X,namespace='/framework',broadcast=B)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(B)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except S as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @s
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",X,namespace='/framework',broadcast=B)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=B)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=B)
     os.system(command[1])
    else:
     show_command=B
     if command[0]=='hide':
      show_command=U
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=B,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not X:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except S as e:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=B)
    socketio.emit("command_modal_add_text",o(e),namespace='/framework',broadcast=B)
    socketio.emit("command_modal_add_text",o(traceback.format_exc()),namespace='/framework',broadcast=B)
 @s
 def start_communicate(current_command,show_command=B):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=U)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while B:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(X)
      break
    logger.debug('END RDR')
    queue.put(X)
    time.sleep(1)
   def clct():
    active=B
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is X:
      break
     try:
      while B:
       r1=queue.get(timeout=0.005)
       if r1 is X:
        active=U
        break
       else:
        r+=r1
     except:
      pass
     if r is not X:
      try:
       r=r.decode('utf-8')
      except S as e:
       try:
        r=r.decode('cp949')
       except S as e:
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
    th.setDaemon(B)
    th.start()
  Pump(sout)
 @s
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=B)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=B)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=B)
   SystemLogicCommand.send_to_ui_thread=X
   SystemLogicCommand.stdout_queue=X
   SystemLogicCommand.process=X
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is X:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @s
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not X and SystemLogicCommand.process.poll()is X:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=B):
     proc.kill()
    SystemLogicCommand.process.kill()
  except S as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @s
 def execute_command_return(command,H=X,force_log=U):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=B,bufsize=1)
   ret=[]
   with process.stdout:
    for line in G(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if H is X:
    ret2='\n'.join(ret)
   elif H=='json':
    try:
     index=0
     for idx,tmp in e(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=X
   return ret2
  except S as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
