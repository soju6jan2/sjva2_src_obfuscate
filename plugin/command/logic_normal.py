import os
g=list
a=Exception
F=object
L=None
r=staticmethod
P=True
w=False
H=id
J=iter
Y=int
m=reload
S=getattr
s=os.listdir
f=os.path
import sys
W=sys.path
o=sys.stdout
from datetime import datetime
import traceback
y=traceback.format_exc
import logging
import subprocess
A=subprocess.STDOUT
v=subprocess.PIPE
n=subprocess.Popen
import threading
I=threading.Thread
import time
O=time.sleep
import io
k=io.open
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,py_queue
X=py_queue.Queue
c=socketio.emit
C=scheduler.remove_job
D=scheduler.is_include
K=scheduler.add_job_instance
l=db.session
from framework.job import Job
from framework.util import Util
from.plugin import package_name,logger
N=logger.debug
u=logger.error
from.model import ModelCommand
T=ModelCommand.get_job_by_id
from io import BytesIO as StringIO
import sys
W=sys.path
o=sys.stdout
class Capturing(g):
 def __enter__(self):
  self._stdout=o
  o=self._stringio=StringIO()
  return self
 def __exit__(self,*args):
  self.extend(self._stringio.getvalue().splitlines())
  del self._stringio 
  o=self._stdout
 def get_log(self):
  try:
   ret=self._stringio.getvalue().splitlines()
   self._stringio.truncate(0)
   return ret
  except a as e:
   u('Exception:%s',e)
   u(y())
   return self
class LogicNormal(F):
 foreground_process=L
 command_queue=L
 send_queue_thread=L
 process_list={}
 load_log_list=L
 @r
 def plugin_load():
  def plugin_load_thread():
   try:
    db_list=l.query(ModelCommand).filter().all()
    for item in db_list:
     if '%s'%item.schedule_type=='1':
      th=I(target=LogicNormal.execute_thread_function,args=(item.command,item.H))
      th.setDaemon(P)
      th.start()
     elif '%s'%item.schedule_type=='2' and item.schedule_auto_start:
      LogicNormal.scheduler_switch(item.H,P)
   except a as e:
    u('Exception:%s',e)
    u(y()) 
  try:
   th=I(target=plugin_load_thread)
   th.setDaemon(P)
   th.start()
  except a as e:
   u('Exception:%s',e)
   u(y())
 @r
 def plugin_unload():
  try:
   LogicNormal.foreground_command_close()
   for key,p in LogicNormal.process_list.items():
    LogicNormal.process_close(p)
  except a as e:
   u('Exception:%s',e)
   u(y())
 @r
 def foreground_command(command,job_id=L):
  try:
   command=command.split(' ')
   if command[0]=='LOAD':
    def func():
     LogicNormal.load_log_list=[]
     with Capturing()as LogicNormal.load_log_list: 
      LogicNormal.start_communicate_load()
      if job_id is not L:
       command_logger=get_logger('%s_%s'%(package_name,job_id))
       LogicNormal.module_load(command,logger=command_logger)
      else:
       LogicNormal.module_load(command)
     for t in LogicNormal.load_log_list:
      LogicNormal.command_queue.put(t+'\n')
     LogicNormal.command_queue.put('<END>')
    th=I(target=func,args=())
    th.setDaemon(P)
    th.start()
    return 'success'
   else:
    if LogicNormal.foreground_process is not L:
     LogicNormal.foreground_command_close()
     O(0.5)
    process=n(command,stdin=v,stdout=v,stderr=A,universal_newlines=P,bufsize=1)
    LogicNormal.foreground_process=process
    LogicNormal.start_communicate2(process)
   return 'success'
  except a as e:
   u('Exception:%s',e)
   u(y())
   return 'fail'
 @r
 def foreground_command_close():
  LogicNormal.process_close(LogicNormal.foreground_process)
 @r
 def process_close(process):
  try:
   if process is L:
    return
   try:
    import psutil
    ps_process=psutil.Process(process.pid)
    for proc in ps_process.children(recursive=P):
     proc.kill()
    ps_process.kill()
    return P
   except:
    pass
  except a as e:
   u('Exception:%s',e)
   u(y())
  return w
 @r
 def scheduler_switch0(request):
  try:
   switch=request.form['switch']
   job_id=request.form['job_id']
   LogicNormal.scheduler_switch(job_id,(switch=='true'))
   return 'success'
  except a as e:
   u('Exception:%s',e)
   u(y())
   return 'fail'
 @r
 def scheduler_switch(H,switch):
  try:
   job=T(H)
   s_id='command_%s'%H
   if switch:
    job_instance=Job(package_name,s_id,job.schedule_info,LogicNormal.execute_thread_function_by_scheduler,u"%s %s : %s"%(package_name,job.H,job.description),P,args=job.H)
    K(job_instance)
   else:
    if D(s_id):
     C(s_id)
   return 'success'
  except a as e:
   u('Exception:%s',e)
   u(y())
   return 'fail'
 @r
 def job_background(job_id):
  try:
   th=I(target=LogicNormal.execute_thread_function_job,args=(job_id,))
   th.setDaemon(P)
   th.start()
   return P
  except a as e:
   u('Exception:%s',e)
   u(y())
   return w
 @r
 def execute_thread_function_job(job_id):
  job=T(job_id)
  LogicNormal.execute_thread_function(job.command,command_id=job.H)
 @r
 def execute_thread_function(command,command_id=-1):
  try:
   N('COMMAND RUN START : %s %s',command,command_id)
   ret=[]
   import platform
   if platform.system()=='Windows':
    command=command.encode('cp949')
   command=command.split(' ')
   new_command=[]
   flag=w
   tmp=L
   for c in command:
    if c.startswith('"')and c.endswith('"'):
     new_command.append(c[1:-1])
    elif c.startswith('"'):
     flag=P
     tmp=c[1:]
    elif flag and c.endswith('"'):
     flag=w
     tmp=tmp+' '+c[:-1]
     new_command.append(tmp)
    elif flag:
     tmp=tmp+' '+c
    else:
     new_command.append(c)
   command=new_command
   if command[0]=='LOAD':
    command_logger=get_logger('%s_%s'%(package_name,command_id))
    LogicNormal.module_load(command,logger=command_logger)
   else:
    p=n(command,stdin=v,stdout=v,stderr=A,universal_newlines=P,bufsize=1)
    command_logger=L
    N(LogicNormal.process_list)
    if command_id!=-1:
     command_logger=get_logger('%s_%s'%(package_name,command_id))
     if command_id in LogicNormal.process_list and LogicNormal.process_list[command_id]is not L:
      LogicNormal.process_close(LogicNormal.process_list[command_id])
     LogicNormal.process_list[command_id]=p
    N(LogicNormal.process_list)
    with p.stdout:
     for line in J(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except a as e:
       try:
        line=line.decode('cp949')
       except a as e:
        pass
      if command_logger is not L:
       command_logger.debug(line.strip())
      ret.append(line.strip())
     p.wait()
    N('COMMAND RUN END : %s',command)
    p=L
    if command_id in LogicNormal.process_list:
     del LogicNormal.process_list[command_id]
    return ret
  except a as e:
   u('Exception:%s',e)
   u(y()) 
 @r
 def execute_thread_function_by_scheduler(*args,**kwargs):
  try:
   N('COMMAND RUN START BY SCHEDULE :%s',args[0])
   job=l.query(ModelCommand).filter_by(H=Y(args[0])).first()
   LogicNormal.execute_thread_function(job.command,command_id=job.H)
   N('COMMAND RUN END BY SCHEDULE :%s',args[0])
  except a as e:
   u('Exception:%s',e)
   u(y()) 
 @r
 def start_communicate2(process):
  LogicNormal.command_queue=X()
  sout=k(process.stdout.fileno(),'rb',closefd=w)
  def Pump(stream):
   queue=X()
   def rdr():
    N('START RDR')
    while P:
     buf=process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(L)
      break
    N('END RDR')
    queue.put(L)
    O(1)
   def clct():
    active=P
    N('START clct')
    while active:
     r=queue.get()
     if r is L:
      break
     try:
      while P:
       r1=queue.get(timeout=0.005)
       if r1 is L:
        active=w
        break
       else:
        r+=r1
     except:
      pass
     if r is not L:
      try:
       r=r.decode('utf-8')
      except a as e:
       try:
        r=r.decode('cp949')
       except a as e:
        u('Exception:%s',e)
        u(y())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      LogicNormal.command_queue.put(r.replace('\x00',''))
    LogicNormal.command_queue.put('<END>')
    N('END clct')
   for tgt in[rdr,clct]:
    th=I(target=tgt)
    th.setDaemon(P)
    th.start()
  Pump(sout)
 @r
 def start_communicate_load():
  LogicNormal.command_queue=X()
  def func():
   position=0
   flag=P
   while LogicNormal.command_queue is not L:
    logs=LogicNormal.load_log_list.get_log()
    if logs:
     for log in logs:
      LogicNormal.command_queue.put(log.strip()+'\n')
    O(1)
  th=I(target=func)
  th.setDaemon(P)
  th.start()
 @r
 def send_queue_start():
  def send_queue_thread_function():
   N('send_queue_thread_function START')
   while LogicNormal.command_queue:
    line=LogicNormal.command_queue.get()
    if line=='<END>':
     c("end",L,namespace='/%s'%package_name,broadcast=P)
     break
    else:
     c("add",line,namespace='/%s'%package_name,broadcast=P)
   LogicNormal.send_queue_thread=L
   LogicNormal.command_queue=L
   LogicNormal.foreground_process=L
   N('send_queue_thread_function END')
  if LogicNormal.send_queue_thread is L:
   LogicNormal.send_queue_thread=I(target=send_queue_thread_function,args=())
   LogicNormal.send_queue_thread.start()
 @r
 def send_process_command(req):
  try:
   command=req.form['command']
   LogicNormal.foreground_process.stdin.write(b'%s\n'%command)
   LogicNormal.foreground_process.stdin.flush()
   return P
  except a as e:
   u('Exception:%s',e)
   u(y())
   return w
 @r
 def command_file_list():
  try:
   command_path=f.join(path_data,'command')
   file_list=s(command_path)
   ret=[]
   for f in file_list:
    c=f.join(command_path,f)
    if f.endswith('.py'):
     c='python %s'%c
    ret.append({'text':f,'value':c})
   return ret
  except a as e:
   u('Exception:%s',e)
   u(y())
 @r
 def module_load(command,**kwargs):
  try:
   python_filename=command[1]
   python_sys_path=f.dirname(python_filename)
   if python_sys_path not in W:
    W.insert(0,python_sys_path)
   N(W)
   module_name=f.basename(python_filename).split('.py')[0]
   mod=__import__(module_name,fromlist=[])
   m(mod)
   args=command
   mod_command_load=S(mod,'main')
   if mod_command_load:
    mod_command_load(*args,**kwargs)
   return 'success'
  except a as e:
   u('Exception:%s',e)
   u(y())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
