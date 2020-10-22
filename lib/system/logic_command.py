import os
L=object
Q=None
N=staticmethod
o=True
j=False
e=Exception
F=str
s=iter
B=format
D=enumerate
l=os.system
import traceback
H=traceback.format_exc
import logging
import platform
import subprocess
w=subprocess.STDOUT
V=subprocess.PIPE
f=subprocess.Popen
import threading
i=threading.Thread
import sys
import io
O=io.open
import time
R=time.sleep
import json
C=json.loads
from framework.logger import get_logger
from framework import path_app_root,socketio,py_queue
b=py_queue.Queue
g=socketio.emit
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class SystemLogicCommand(L):
 commands=Q
 process=Q
 stdout_queue=Q
 thread=Q
 send_to_ui_thread=Q
 return_log=Q
 @N
 def start(title,commands,clear=o,wait=j,show_modal=o):
  try:
   if show_modal:
    if clear:
     g("command_modal_clear",Q,namespace='/framework',broadcast=o)
   SystemLogicCommand.return_log=[]
   SystemLogicCommand.title=title
   SystemLogicCommand.commands=commands
   SystemLogicCommand.thread=i(target=SystemLogicCommand.execute_thread_function,args=(show_modal,))
   SystemLogicCommand.thread.setDaemon(o)
   SystemLogicCommand.thread.start()
   if wait:
    R(1)
    SystemLogicCommand.thread.join()
    return SystemLogicCommand.return_log
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H())
 @N
 def execute_thread_function(show_modal):
  try:
   if show_modal:
    g("loading_hide",Q,namespace='/framework',broadcast=o)
   for command in SystemLogicCommand.commands:
    if command[0]=='msg':
     if show_modal:
      g("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=o)
    elif command[0]=='system':
     if show_modal:
      g("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=o)
     l(command[1])
    else:
     show_command=o
     if command[0]=='hide':
      show_command=j
      command=command[1:]
     SystemLogicCommand.process=f(command,stdin=V,stdout=V,stderr=w,universal_newlines=o,bufsize=1)
     SystemLogicCommand.start_communicate(command,show_command=show_command)
     SystemLogicCommand.send_queue_start(show_modal)
     if SystemLogicCommand.process is not Q:
      SystemLogicCommand.process.wait()
    R(1)
  except e as e:
   if show_modal:
    g("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=o)
    g("command_modal_add_text",F(e),namespace='/framework',broadcast=o)
    g("command_modal_add_text",F(H()),namespace='/framework',broadcast=o)
 @N
 def start_communicate(current_command,show_command=o):
  SystemLogicCommand.stdout_queue=b()
  if show_command:
   SystemLogicCommand.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=O(SystemLogicCommand.process.stdout.fileno(),'rb',closefd=j)
  def Pump(stream):
   queue=b()
   def rdr():
    logger.debug('START RDR')
    while o:
     buf=SystemLogicCommand.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(Q)
      break
    logger.debug('END RDR')
    queue.put(Q)
    R(1)
   def clct():
    active=o
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is Q:
      break
     try:
      while o:
       r1=queue.get(timeout=0.005)
       if r1 is Q:
        active=j
        break
       else:
        r+=r1
     except:
      pass
     if r is not Q:
      try:
       r=r.decode('utf-8')
      except e as e:
       try:
        r=r.decode('cp949')
       except e as e:
        logger.error('Exception:%s',e)
        logger.error(H())
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
    th=i(target=tgt)
    th.setDaemon(o)
    th.start()
  Pump(sout)
 @N
 def send_queue_start(show_modal):
  def send_to_ui_thread_function():
   logger.debug('send_queue_thread_function START')
   if show_modal:
    g("command_modal_show",SystemLogicCommand.title,namespace='/framework',broadcast=o)
   while SystemLogicCommand.stdout_queue:
    line=SystemLogicCommand.stdout_queue.get()
    logger.debug('Send to UI :%s',line)
    if line=='<END>':
     if show_modal:
      g("command_modal_add_text","\n",namespace='/framework',broadcast=o)
      break
    else:
     if show_modal:
      g("command_modal_add_text",line,namespace='/framework',broadcast=o)
   SystemLogicCommand.send_to_ui_thread=Q
   SystemLogicCommand.stdout_queue=Q
   SystemLogicCommand.process=Q
   logger.debug('send_to_ui_thread_function END')
  if SystemLogicCommand.send_to_ui_thread is Q:
   SystemLogicCommand.send_to_ui_thread=i(target=send_to_ui_thread_function,args=())
   SystemLogicCommand.send_to_ui_thread.start()
 @N
 def plugin_unload():
  try:
   if SystemLogicCommand.process is not Q and SystemLogicCommand.process.poll()is Q:
    import psutil
    process=psutil.Process(SystemLogicCommand.process.pid)
    for proc in SystemLogicCommand.process.children(recursive=o):
     proc.kill()
    SystemLogicCommand.process.kill()
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H()) 
 @N
 def execute_command_return(command,B=Q,force_log=j):
  try:
   logger.debug('execute_command_return : %s',' '.join(command))
   process=f(command,stdout=V,stderr=w,universal_newlines=o,bufsize=1)
   ret=[]
   with process.stdout:
    for line in s(process.stdout.readline,b''):
     ret.append(line.strip())
     if force_log:
      logger.debug(line.strip())
    process.wait()
   if B is Q:
    ret2='\n'.join(ret)
   elif B=='json':
    try:
     index=0
     for idx,tmp in D(ret):
      if tmp.startswith('{')or tmp.startswith('['):
       index=idx
       break
     ret2=C(''.join(ret[index:]))
    except:
     ret2=Q
   return ret2
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H())
   logger.error('command : %s',command)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
