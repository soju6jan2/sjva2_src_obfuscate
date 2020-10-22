import os
p=object
G=True
V=False
u=None
P=Exception
r=str
T=classmethod
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
class SystemLogicCommand2(p):
 instance_list=[]
 def __init__(self,title,commands,clear=G,wait=V,show_modal=G):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=u
  self.stdout_queue=u
  self.thread=u
  self.send_to_ui_thread=u
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",u,namespace='/framework',broadcast=G)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(G)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",u,namespace='/framework',broadcast=G)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=G)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=G)
     os.system(command[1])
    else:
     show_command=G
     if command[0]=='hide':
      show_command=V
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=G,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not u:
      self.process.wait()
    time.sleep(1)
  except P as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=G)
    socketio.emit("command_modal_add_text",r(exception),namespace='/framework',broadcast=G)
    socketio.emit("command_modal_add_text",r(traceback.format_exc()),namespace='/framework',broadcast=G)
 def start_communicate(self,current_command,show_command=G):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=V)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while G:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(u)
      break
    queue.put(u)
    time.sleep(1)
   def clct():
    active=G
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
      self.stdout_queue.put(r)
      self.return_log+=r.split('\n')
    self.stdout_queue.put('<END>')
   for tgt in[rdr,clct]:
    th=threading.Thread(target=tgt)
    th.setDaemon(G)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=G)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=G)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=G)
   self.send_to_ui_thread=u
   self.stdout_queue=u
   self.process=u
  if self.send_to_ui_thread is u:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @T
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not u and instance.process.poll()is u:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=G):
      proc.kill()
     instance.process.kill()
   except P as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
