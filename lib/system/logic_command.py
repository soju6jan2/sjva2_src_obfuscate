import os
p=object
u=None
H=staticmethod
G=True
V=False
P=Exception
r=str
A=iter
M=format
g=enumerate
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
class SystemLogicCommand(p):
 commands=u
 process=u
 stdout_queue=u
 thread=u
 send_to_ui_thread=u
 return_log=u
 @H
 def start(title,commands,clear=G,wait=V,show_modal=G):
  try:
   if show_modal:
    if clear:
     socketio.emit("command_modal_clear",u,namespace='/framework',broadcast=G)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=threading.Thread(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(G)
   SystemLogicCommand.thread.start()
   if wait:
    time.sleep(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @H
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    socketio.emit("loading_hide",u,namespace='/framework',broadcast=G)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=G)
    elif command[0]=='system':
     if show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=G)
     os.system(command[1])
    else:
     show_command=G
     if command[0]=='hide':
      show_command=V
      command=command[1:]
     SystemLogicCommand.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=G,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not u:
      SystemLogicCommand.process.wait()
    time.sleep(1)
  except P as exception:
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=G)
    socketio.emit("command_modal_add_text",r(xception),namespace='/framework',broadcast=G)
    socketio.emit("command_modal_add_text",r(traceback.format_exc()),namespace='/framework',broadcast=G)
 @H
 def start_communicate(current_command,show_command=G):
  SystemLogicCommand.stdout_queue=py_queue.Queue()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=V)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while G:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(u)
      break
    logger.debug('END RDR')
    queue.put(u)
    time.sleep(1)
   def clct():
    active=G
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is u:
      break
     try:
      while G:
       r1=queue.get(timeout=0.005)
       if r1 is u:
        active=V
        break
       else:
        r+=r1
     except:
      pass
     if r is not u:
      try:
       r=r.decode('utf-8')
      except P as exception:
       try:
        r=r.decode('cp949')
       except P as exception:
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
    th.setDaemon(G)
    th.start()
  Pump(sout)
 @H
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    socketio.emit("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=G)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=G)
      break
    else:
     if show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=G)
   SystemLogicCommand.send_to_ui_thread=u
   SystemLogicCommand.stdout_queue=u
   SystemLogicCommand.process=u
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is u:
   SystemLogicCommand.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @H
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not u and SystemLogicCommand.process.poll()is u:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=G):
     proc.kill()
    SystemLogicCommand.process.kill()
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @H
 def execute_command_return(command,M=u,force_log=V):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=G,bufsize=1)
   ret=[]
   with process.stdout:
    for line in A(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if M is u:
    ret2='\n'.join(ret)
   elif M=='json':
    try:
     index=0
     for idx,tmp in g(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=json.loads(''.join(ret[index:]))
    except:
     ret2=u
   return ret2
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
