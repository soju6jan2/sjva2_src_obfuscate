import os
n=object
P=True
O=False
t=None
H=Exception
D=str
x=classmethod
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
class SystemLogicCommand2(n):
 instance_list=[]
 def __init__(self,title,commands,clear=P,wait=O,show_modal=P):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=t
  self.stdout_queue=t
  self.thread=t
  self.send_to_ui_thread=t
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",t,namespace='/framework',broadcast=P)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(P)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",t,namespace='/framework',broadcast=P)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=P)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=P)
     os.system(command[1])
    else:
     show_command=P
     if command[0]=='hide':
      show_command=O
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=P,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not t:
      self.process.wait()
    time.sleep(1)
  except H as e:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=P)
    socketio.emit("command_modal_add_text",D(e),namespace='/framework',broadcast=P)
    socketio.emit("command_modal_add_text",D(traceback.format_exc()),namespace='/framework',broadcast=P)
 def start_communicate(self,current_command,show_command=P):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=O)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while P:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(t)
      break
    queue.put(t)
    time.sleep(1)
   def clct():
    active=P
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
      self.stdout_queue.put(r)
      self.return_log+=r.split('\n')
    self.stdout_queue.put('<END>')
   for tgt in[rdr,clct]:
    th=threading.Thread(target=tgt)
    th.setDaemon(P)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=P)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=P)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=P)
   self.send_to_ui_thread=t
   self.stdout_queue=t
   self.process=t
  if self.send_to_ui_thread is t:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @x
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not t and instance.process.poll()is t:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=P):
      proc.kill()
     instance.process.kill()
   except H as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
