import os
d=object
m=True
w=False
R=None
V=Exception
A=str
I=classmethod
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
class SystemLogicCommand2(d):
 instance_list=[]
 def __init__(self,title,commands,clear=m,wait=w,show_modal=m):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=R
  self.stdout_queue=R
  self.thread=R
  self.send_to_ui_thread=R
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",R,namespace='/framework',broadcast=m)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(m)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",R,namespace='/framework',broadcast=m)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=m)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=m)
     os.system(command[1])
    else:
     show_command=m
     if command[0]=='hide':
      show_command=w
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=m,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not R:
      self.process.wait()
    time.sleep(1)
  except V as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=m)
    socketio.emit("command_modal_add_text",A(exception),namespace='/framework',broadcast=m)
    socketio.emit("command_modal_add_text",A(traceback.format_exc()),namespace='/framework',broadcast=m)
 def start_communicate(self,current_command,show_command=m):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=w)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while m:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(R)
      break
    queue.put(R)
    time.sleep(1)
   def clct():
    active=m
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
      self.stdout_queue.put(r)
      self.return_log+=r.split('\n')
    self.stdout_queue.put('<END>')
   for tgt in[rdr,clct]:
    th=threading.Thread(target=tgt)
    th.setDaemon(m)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=m)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=m)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=m)
   self.send_to_ui_thread=R
   self.stdout_queue=R
   self.process=R
  if self.send_to_ui_thread is R:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @I
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not R and instance.process.poll()is R:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=m):
      proc.kill()
     instance.process.kill()
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
