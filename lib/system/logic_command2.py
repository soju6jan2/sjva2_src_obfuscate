import os
I=object
i=True
C=False
H=None
j=Exception
e=str
x=classmethod
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
from framework.logger import get_logger
from framework import path_app_root,socketio,logger,py_queue
M=py_queue.Queue
D=logger.error
k=socketio.emit
package_name=__name__.split('.')[0]
class SystemLogicCommand2(I):
 instance_list=[]
 def __init__(self,title,commands,clear=i,wait=C,show_modal=i):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=H
  self.stdout_queue=H
  self.thread=H
  self.send_to_ui_thread=H
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     k("command_modal_clear",H,namespace='/framework',broadcast=i)
   self.thread=v(target=self.execute_thread_function,args=())
   self.thread.setDaemon(i)
   self.thread.start()
   if self.wait:
    T(1)
    self.thread.join()
    return self.return_log
  except j as e:
   D('Exception:%s',e)
   D(V())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    k("loading_hide",H,namespace='/framework',broadcast=i)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      k("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=i)
    elif command[0]=='system':
     if self.show_modal:
      k("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=i)
     J(command[1])
    else:
     show_command=i
     if command[0]=='hide':
      show_command=C
      command=command[1:]
     self.process=f(command,stdin=W,stdout=W,stderr=O,universal_newlines=i,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not H:
      self.process.wait()
    T(1)
  except j as e:
   if self.show_modal:
    k("command_modal_show",self.title,namespace='/framework',broadcast=i)
    k("command_modal_add_text",e(e),namespace='/framework',broadcast=i)
    k("command_modal_add_text",e(V()),namespace='/framework',broadcast=i)
 def start_communicate(self,current_command,show_command=i):
  self.stdout_queue=M()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=L(self.process.stdout.fileno(),'rb',closefd=C)
  def Pump(stream):
   queue=M()
   def rdr():
    while i:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(H)
      break
    queue.put(H)
    T(1)
   def clct():
    active=i
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
        D('Exception:%s',e)
        D(V())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      self.stdout_queue.put(r)
      self.return_log+=r.split('\n')
    self.stdout_queue.put('<END>')
   for tgt in[rdr,clct]:
    th=v(target=tgt)
    th.setDaemon(i)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    k("command_modal_show",self.title,namespace='/framework',broadcast=i)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      k("command_modal_add_text","\n",namespace='/framework',broadcast=i)
      break
    else:
     if self.show_modal:
      k("command_modal_add_text",line,namespace='/framework',broadcast=i)
   self.send_to_ui_thread=H
   self.stdout_queue=H
   self.process=H
  if self.send_to_ui_thread is H:
   self.send_to_ui_thread=v(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @x
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not H and instance.process.poll()is H:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=i):
      proc.kill()
     instance.process.kill()
   except j as e:
    D('Exception:%s',e)
    D(V()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
