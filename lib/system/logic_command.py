import os
d=object
R=None
o=staticmethod
m=True
w=False
V=Exception
A=str
q=iter
J=format
W=enumerate
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
class SystemLogicCommand(d):
 commands=R
 process=R
 stdout_queue=R
 thread=R
 send_to_ui_thread=R
 return_log=R
 @o
 def start(title,commands,clear=m,wait=w,show_modal=m):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",R,namespace='/framework',broadcast=m)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(m)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @o
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",R,namespace='/framework',broadcast=m)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=m)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=m)
     os.system(command[1])
    else:
     show_command=m
     if command[0]=='hide':
      show_command=w
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=m,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not R:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except V as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=m)
    socketio.emit("command_modal_add_text",A(xception),namespace='/framework',broadcast=m)
    socketio.emit("command_modal_add_text",A(traceback.format_exc()),namespace='/framework',broadcast=m)
 @o
 def start_communicate(current_command,show_command=m):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=w)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while m:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(R)
      break
    logger.debug('END RDR')
    queue.put(R)
    time.sleep(1)
   def clct():
    active=m
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is R:
      break
     try:
      while m:
       r1=queue.get(timeout=0.005)
       if r1 is R:
        active=w
        break
       else:
        r+=r1
     except:
      pass
     if r is not R:
      try:
       r=r.decode('utf-8')
      except V as exception:
       try:
        r=r.decode('cp949')
       except V as exception:
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
    th.setDaemon(m)
    th.start()
  Pump(sout)
 @o
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=m)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=m)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=m)
   SystemLogicCommand.send_to_ui_thread=R
   SystemLogicCommand.stdout_queue=R
   SystemLogicCommand.process=R
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is R:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @o
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not R and SystemLogicCommand.process.poll()is R:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=m):
     proc.kill()
    SystemLogicCommand.process.kill()
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @o
 def execute_command_return(command,J=R,force_log=w):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=m,bufsize=1)
   ret=[]
   with process.stdout:
    for line in q(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if J is R:
    ret2='\n'.join(ret)
   elif J=='json':
    try:
     index=0
     for idx,tmp in W(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=R
   return ret2
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
