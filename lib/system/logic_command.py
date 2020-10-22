import os
s=object
O=None
Q=staticmethod
B=True
W=False
t=Exception
u=str
J=iter
b=format
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
class SystemLogicCommand(s):
 commands=O
 process=O
 stdout_queue=O
 thread=O
 send_to_ui_thread=O
 return_log=O
 @Q
 def start(title,commands,clear=B,wait=W,show_modal=B):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",O,namespace='/framework',broadcast=B)
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
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @Q
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",O,namespace='/framework',broadcast=B)
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
      show_command=W
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=B,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not O:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except t as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=B)
    socketio.emit("command_modal_add_text",u(xception),namespace='/framework',broadcast=B)
    socketio.emit("command_modal_add_text",u(traceback.format_exc()),namespace='/framework',broadcast=B)
 @Q
 def start_communicate(current_command,show_command=B):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=W)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while B:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(O)
      break
    logger.debug('END RDR')
    queue.put(O)
    time.sleep(1)
   def clct():
    active=B
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is O:
      break
     try:
      while B:
       r1=queue.get(timeout=0.005)
       if r1 is O:
        active=W
        break
       else:
        r+=r1
     except:
      pass
     if r is not O:
      try:
       r=r.decode('utf-8')
      except t as exception:
       try:
        r=r.decode('cp949')
       except t as exception:
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
    th.setDaemon(B)
    th.start()
  Pump(sout)
 @Q
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
   SystemLogicCommand.send_to_ui_thread=O
   SystemLogicCommand.stdout_queue=O
   SystemLogicCommand.process=O
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is O:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @Q
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not O and SystemLogicCommand.process.poll()is O:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=B):
     proc.kill()
    SystemLogicCommand.process.kill()
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @Q
 def execute_command_return(command,b=O,force_log=W):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=B,bufsize=1)
   ret=[]
   with process.stdout:
    for line in J(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if b is O:
    ret2='\n'.join(ret)
   elif b=='json':
    try:
     index=0
     for idx,tmp in V(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=O
   return ret2
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
