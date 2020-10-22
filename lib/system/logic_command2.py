import os
L=object
o=True
j=False
Q=None
e=Exception
F=str
q=classmethod
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
from framework.logger import get_logger
from framework import path_app_root,socketio,logger,py_queue
b=py_queue.Queue
J=logger.error
g=socketio.emit
package_name=__name__.split('.')[0]
class SystemLogicCommand2(L):
 instance_list=[]
 def __init__(self,title,commands,clear=o,wait=j,show_modal=o):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=Q
  self.stdout_queue=Q
  self.thread=Q
  self.send_to_ui_thread=Q
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     g("command_modal_clear",Q,namespace='/framework',broadcast=o)
   self.thread=i(target=self.execute_thread_function,args=())
   self.thread.setDaemon(o)
   self.thread.start()
   if self.wait:
    R(1)
    self.thread.join()
    return self.return_log
  except e as e:
   J('Exception:%s',e)
   J(H())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    g("loading_hide",Q,namespace='/framework',broadcast=o)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      g("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=o)
    elif command[0]=='system':
     if self.show_modal:
      g("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=o)
     l(command[1])
    else:
     show_command=o
     if command[0]=='hide':
      show_command=j
      command=command[1:]
     self.process=f(command,stdin=V,stdout=V,stderr=w,universal_newlines=o,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not Q:
      self.process.wait()
    R(1)
  except e as e:
   if self.show_modal:
    g("command_modal_show",self.title,namespace='/framework',broadcast=o)
    g("command_modal_add_text",F(e),namespace='/framework',broadcast=o)
    g("command_modal_add_text",F(H()),namespace='/framework',broadcast=o)
 def start_communicate(self,current_command,show_command=o):
  self.stdout_queue=b()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=O(self.process.stdout.fileno(),'rb',closefd=j)
  def Pump(stream):
   queue=b()
   def rdr():
    while o:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(Q)
      break
    queue.put(Q)
    R(1)
   def clct():
    active=o
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
        J('Exception:%s',e)
        J(H())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      self.stdout_queue.put(r)
      self.return_log+=r.split('\n')
    self.stdout_queue.put('<END>')
   for tgt in[rdr,clct]:
    th=i(target=tgt)
    th.setDaemon(o)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    g("command_modal_show",self.title,namespace='/framework',broadcast=o)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      g("command_modal_add_text","\n",namespace='/framework',broadcast=o)
      break
    else:
     if self.show_modal:
      g("command_modal_add_text",line,namespace='/framework',broadcast=o)
   self.send_to_ui_thread=Q
   self.stdout_queue=Q
   self.process=Q
  if self.send_to_ui_thread is Q:
   self.send_to_ui_thread=i(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @q
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not Q and instance.process.poll()is Q:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=o):
      proc.kill()
     instance.process.kill()
   except e as e:
    J('Exception:%s',e)
    J(H()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
