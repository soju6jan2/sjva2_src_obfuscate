import os
I=object
H=None
h=staticmethod
i=True
C=False
j=Exception
e=str
G=iter
n=format
y=enumerate
J=os.system
import traceback
V=traceback.format_exc
import logging
import platform
import subprocess
O=subprocess.STDOUT
W=subprocess.PIPE
f=subprocess.Popen
import threading
v=threading.Thread
import sys
import io
L=io.open
import time
T=time.sleep
import json
t=json.loads
from framework.logger import get_logger
from framework import path_app_root,socketio,py_queue
M=py_queue.Queue
k=socketio.emit
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class SystemLogicCommand(I):
 commands=H
 process=H
 stdout_queue=H
 thread=H
 send_to_ui_thread=H
 return_log=H
 @h
 def start(title,commands,clear=i,wait=C,show_modal=i):
  try:
   if show_modal:
    if clear:
     k("command_modal_clear",H,namespace='/framework',broadcast=i)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=v(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(i)
   SystemLogicCommand.thread.start()
   if wait:
    T(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V())
 @h
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    k("loading_hide",H,namespace='/framework',broadcast=i)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      k("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=i)
    elif command[0]=='system':
     if show_modal:
      k("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=i)
     J(command[1])
    else:
     show_command=i
     if command[0]=='hide':
      show_command=C
      command=command[1:]
     SystemLogicCommand.process=f(command,stdin=W,stdout=W,stderr=O,universal_newlines=i,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not H:
      SystemLogicCommand.process.wait()
    T(1)
  except j as e:
   if show_modal:
    k("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=i)
    k("command_modal_add_text",e(e),namespace='/framework',broadcast=i)
    k("command_modal_add_text",e(V()),namespace='/framework',broadcast=i)
 @h
 def start_communicate(current_command,show_command=i):
  SystemLogicCommand.stdout_queue=M()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=L(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=C)
  def Pump(stream):
   queue=M()
   def rdr():
    logger.debug('START RDR')
    while i:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(H)
      break
    logger.debug('END RDR')
    queue.put(H)
    T(1)
   def clct():
    active=i
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is H:
      break
     try:
      while i:
       r1=queue.get(timeout=0.005)
       if r1 is H:
        active=C
        break
       else:
        r+=r1
     except:
      pass
     if r is not H:
      try:
       r=r.decode('utf-8')
      except j as e:
       try:
        r=r.decode('cp949')
       except j as e:
        logger.error('Exception:%s',e)
        logger.error(V())
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
    th=v(target=tgt)
    th.setDaemon(i)
    th.start()
  Pump(sout)
 @h
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    k("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=i)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      k("command_modal_add_text","\n",namespace='/framework',broadcast=i)
      break
    else:
     if show_modal:
      k("command_modal_add_text",line,namespace='/framework',broadcast=i)
   SystemLogicCommand.send_to_ui_thread=H
   SystemLogicCommand.stdout_queue=H
   SystemLogicCommand.process=H
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is H:
   SystemLogicCommand.send_to_ui_thread=v(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @h
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not H and SystemLogicCommand.process.poll()is H:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=i):
     proc.kill()
    SystemLogicCommand.process.kill()
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V()) 
 @h
 def execute_command_return(command,n=H,force_log=C):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=f(command,stdout=W,stderr=O,universal_newlines=i,bufsize=1)
   ret=[]
   with process.stdout:
    for line in G(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if n is H:
    ret2='\n'.join(ret)
   elif n=='json':
    try:
     index=0
     for idx,tmp in y(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=t(''.join(ret[index:]))
    except:
     ret2=H
   return ret2
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
