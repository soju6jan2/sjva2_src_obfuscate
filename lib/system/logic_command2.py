import os
M=object
J=True
f=False
N=None
U=Exception
D=str
Q=classmethod
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
from framework import path_app_root,socketio,logger,py_queue
package_name=__name__.split('.')[0]
class SystemLogicCommand2(M):
 instance_list=[]
 def __init__(self,title,commands,clear=J,wait=f,show_modal=J):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=N
  self.stdout_queue=N
  self.thread=N
  self.send_to_ui_thread=N
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",N,namespace='/framework',broadcast=J)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(J)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except U as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",N,namespace='/framework',broadcast=J)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=J)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=J)
     os.system(command[1])
    else:
     show_command=J
     if command[0]=='hide':
      show_command=f
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=J,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not N:
      self.process.wait()
    time.sleep(1)
  except U as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=J)
    socketio.emit("command_modal_add_text",D(exception),namespace='/framework',broadcast=J)
    socketio.emit("command_modal_add_text",D(traceback.format_exc()),namespace='/framework',broadcast=J)
 def start_communicate(self,current_command,show_command=J):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=f)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while J:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(N)
      break
    queue.put(N)
    time.sleep(1)
   def clct():
    active=J
    while active:
     r=queue.get()
     if r is N:
      break
     try:
      while J:
       r1=queue.get(timeout=0.005)
       if r1 is N:
        active=f
        break
       else:
        r+=r1
     except:
      pass
     if r is not N:
      try:
       r=r.decode('utf-8')
      except U as exception:
       try:
        r=r.decode('cp949')
       except U as exception:
        logger.error('Exception:%s',exception)
        logger.error(traceback.format_exc())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      self.stdout_queue.put(r)
      self.return_log+=r.split('\n')
    self.stdout_queue.put('<END>')
   for tgt in[rdr,clct]:
    th=threading.Thread(target=tgt)
    th.setDaemon(J)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=J)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=J)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=J)
   self.send_to_ui_thread=N
   self.stdout_queue=N
   self.process=N
  if self.send_to_ui_thread is N:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @Q
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not N and instance.process.poll()is N:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=J):
      proc.kill()
     instance.process.kill()
   except U as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
