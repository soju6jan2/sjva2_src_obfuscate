import os
n=object
t=None
X=staticmethod
P=True
O=False
H=Exception
D=str
u=iter
m=format
R=enumerate
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
class SystemLogicCommand(n):
 commands=t
 process=t
 stdout_queue=t
 thread=t
 send_to_ui_thread=t
 return_log=t
 @X
 def start(title,commands,clear=P,wait=O,show_modal=P):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",t,namespace='/framework',broadcast=P)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(P)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @X
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",t,namespace='/framework',broadcast=P)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=P)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=P)
     os.system(command[1])
    else:
     show_command=P
     if command[0]=='hide':
      show_command=O
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=P,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not t:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except H as e:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=P)
    socketio.emit("command_modal_add_text",D(e),namespace='/framework',broadcast=P)
    socketio.emit("command_modal_add_text",D(traceback.format_exc()),namespace='/framework',broadcast=P)
 @X
 def start_communicate(current_command,show_command=P):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=O)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while P:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(t)
      break
    logger.debug('END RDR')
    queue.put(t)
    time.sleep(1)
   def clct():
    active=P
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is t:
      break
     try:
      while P:
       r1=queue.get(timeout=0.005)
       if r1 is t:
        active=O
        break
       else:
        r+=r1
     except:
      pass
     if r is not t:
      try:
       r=r.decode('utf-8')
      except H as e:
       try:
        r=r.decode('cp949')
       except H as e:
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
    th.setDaemon(P)
    th.start()
  Pump(sout)
 @X
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=P)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=P)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=P)
   SystemLogicCommand.send_to_ui_thread=t
   SystemLogicCommand.stdout_queue=t
   SystemLogicCommand.process=t
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is t:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @X
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not t and SystemLogicCommand.process.poll()is t:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=P):
     proc.kill()
    SystemLogicCommand.process.kill()
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @X
 def execute_command_return(command,m=t,force_log=O):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=P,bufsize=1)
   ret=[]
   with process.stdout:
    for line in u(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if m is t:
    ret2='\n'.join(ret)
   elif m=='json':
    try:
     index=0
     for idx,tmp in R(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=t
   return ret2
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
