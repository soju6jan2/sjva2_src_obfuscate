import os
R=object
Y=True
L=False
w=None
f=Exception
l=str
s=classmethod
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
class SystemLogicCommand2(R):
 instance_list=[]
 def __init__(self,title,commands,clear=Y,wait=L,show_modal=Y):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=w
  self.stdout_queue=w
  self.thread=w
  self.send_to_ui_thread=w
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",w,namespace='/framework',broadcast=Y)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(Y)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except f as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",w,namespace='/framework',broadcast=Y)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=Y)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=Y)
     os.system(command[1])
    else:
     show_command=Y
     if command[0]=='hide':
      show_command=L
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=Y,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not w:
      self.process.wait()
    time.sleep(1)
  except f as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=Y)
    socketio.emit("command_modal_add_text",l(exception),namespace='/framework',broadcast=Y)
    socketio.emit("command_modal_add_text",l(traceback.format_exc()),namespace='/framework',broadcast=Y)
 def start_communicate(self,current_command,show_command=Y):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=L)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while Y:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(w)
      break
    queue.put(w)
    time.sleep(1)
   def clct():
    active=Y
    while active:
     r=queue.get()
     if r is w:
      break
     try:
      while Y:
       r1=queue.get(timeout=0.005)
       if r1 is w:
        active=L
        break
       else:
        r+=r1
     except:
      pass
     if r is not w:
      try:
       r=r.decode('utf-8')
      except f as exception:
       try:
        r=r.decode('cp949')
       except f as exception:
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
    th.setDaemon(Y)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=Y)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=Y)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=Y)
   self.send_to_ui_thread=w
   self.stdout_queue=w
   self.process=w
  if self.send_to_ui_thread is w:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @s
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not w and instance.process.poll()is w:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=Y):
      proc.kill()
     instance.process.kill()
   except f as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
