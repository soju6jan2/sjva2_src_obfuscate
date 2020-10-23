import os
b=object
M=None
H=staticmethod
h=True
f=False
k=Exception
X=str
n=iter
G=format
w=enumerate
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
class SystemLogicCommand(b):
 commands=M
 process=M
 stdout_queue=M
 thread=M
 send_to_ui_thread=M
 return_log=M
 @H
 def start(title,commands,clear=h,wait=f,show_modal=h):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",M,namespace='/framework',broadcast=h)
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
  except k as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @H
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",M,namespace='/framework',broadcast=h)
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
      show_command=f
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=h,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not M:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except k as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=h)
    socketio.emit("command_modal_add_text",X(xception),namespace='/framework',broadcast=h)
    socketio.emit("command_modal_add_text",X(traceback.format_exc()),namespace='/framework',broadcast=h)
 @H
 def start_communicate(current_command,show_command=h):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=f)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while h:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(M)
      break
    logger.debug('END RDR')
    queue.put(M)
    time.sleep(1)
   def clct():
    active=h
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is M:
      break
     try:
      while h:
       r1=queue.get(timeout=0.005)
       if r1 is M:
        active=f
        break
       else:
        r+=r1
     except:
      pass
     if r is not M:
      try:
       r=r.decode('utf-8')
      except k as exception:
       try:
        r=r.decode('cp949')
       except k as exception:
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
    th.setDaemon(h)
    th.start()
  Pump(sout)
 @H
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
   SystemLogicCommand.send_to_ui_thread=M
   SystemLogicCommand.stdout_queue=M
   SystemLogicCommand.process=M
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is M:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @H
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not M and SystemLogicCommand.process.poll()is M:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=h):
     proc.kill()
    SystemLogicCommand.process.kill()
  except k as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @H
 def execute_command_return(command,G=M,force_log=f):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=h,bufsize=1)
   ret=[]
   with process.stdout:
    for line in n(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if G is M:
    ret2='\n'.join(ret)
   elif G=='json':
    try:
     index=0
     for idx,tmp in w(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=M
   return ret2
  except k as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
