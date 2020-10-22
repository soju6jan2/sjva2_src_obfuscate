import os
d=list
i=Exception
r=object
S=None
O=staticmethod
M=True
J=False
H=id
L=iter
V=int
g=reload
z=getattr
N=os.listdir
Y=os.path
import sys
C=sys.path
x=sys.stdout
from datetime import datetime
import traceback
Q=traceback.format_exc
import logging
import subprocess
w=subprocess.STDOUT
b=subprocess.PIPE
t=subprocess.Popen
import threading
e=threading.Thread
import time
A=time.sleep
import io
U=io.open
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,py_queue
c=py_queue.Queue
o=socketio.emit
p=scheduler.remove_job
n=scheduler.is_include
u=scheduler.add_job_instance
j=db.session
from framework.job import Job
from framework.util import Util
from.plugin import package_name,logger
l=logger.debug
s=logger.error
from.model import ModelCommand
q=ModelCommand.get_job_by_id
from io import BytesIO as StringIO
import sys
C=sys.path
x=sys.stdout
class Capturing(d):
 def __enter__(self):
  self._stdout=x
  x=self._stringio=StringIO()
  return self
 def __exit__(self,*args):
  self.extend(self._stringio.getvalue().splitlines())
  del self._stringio 
  x=self._stdout
 def get_log(self):
  try:
   ret=self._stringio.getvalue().splitlines()
   self._stringio.truncate(0)
   return ret
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return self
class LogicNormal(r):
 foreground_process=S
 command_queue=S
 send_queue_thread=S
 process_list={}
 load_log_list=S
 @O
 def plugin_load():
  def plugin_load_thread():
   try:
    db_list=j.query(ModelCommand).filter().all()
    for item in db_list:
     if '%s'%item.schedule_type=='1':
      th=e(target=LogicNormal.execute_thread_function,args=(item.command,item.H))
      th.setDaemon(M)
      th.start()
     elif '%s'%item.schedule_type=='2' and item.schedule_auto_start:
      LogicNormal.scheduler_switch(item.H,M)
   except i as e:
    s('Exception:%s',e)
    s(Q()) 
  try:
   th=e(target=plugin_load_thread)
   th.setDaemon(M)
   th.start()
  except i as e:
   s('Exception:%s',e)
   s(Q())
 @O
 def plugin_unload():
  try:
   LogicNormal.foreground_command_close()
   for key,p in LogicNormal.process_list.items():
    LogicNormal.process_close(p)
  except i as e:
   s('Exception:%s',e)
   s(Q())
 @O
 def foreground_command(command,job_id=S):
  try:
   command=command.split(' ')
   if command[0]=='LOAD':
    def func():
     LogicNormal.load_log_list=[]
     with Capturing()as LogicNormal.load_log_list: 
      LogicNormal.start_communicate_load()
      if job_id is not S:
       command_logger=get_logger('%s_%s'%(package_name,job_id))
       LogicNormal.module_load(command,logger=command_logger)
      else:
       LogicNormal.module_load(command)
     for t in LogicNormal.load_log_list:
      LogicNormal.command_queue.put(t+'\n')
     LogicNormal.command_queue.put('<END>')
    th=e(target=func,args=())
    th.setDaemon(M)
    th.start()
    return 'success'
   else:
    if LogicNormal.foreground_process is not S:
     LogicNormal.foreground_command_close()
     A(0.5)
    process=t(command,stdin=b,stdout=b,stderr=w,universal_newlines=M,bufsize=1)
    LogicNormal.foreground_process=process
    LogicNormal.start_communicate2(process)
   return 'success'
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return 'fail'
 @O
 def foreground_command_close():
  LogicNormal.process_close(LogicNormal.foreground_process)
 @O
 def process_close(process):
  try:
   if process is S:
    return
   try:
    import psutil
    ps_process=psutil.Process(process.pid)
    for proc in ps_process.children(recursive=M):
     proc.kill()
    ps_process.kill()
    return M
   except:
    pass
  except i as e:
   s('Exception:%s',e)
   s(Q())
  return J
 @O
 def scheduler_switch0(request):
  try:
   switch=request.form['switch']
   job_id=request.form['job_id']
   LogicNormal.scheduler_switch(job_id,(switch=='true'))
   return 'success'
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return 'fail'
 @O
 def scheduler_switch(H,switch):
  try:
   job=q(H)
   s_id='command_%s'%H
   if switch:
    job_instance=Job(package_name,s_id,job.schedule_info,LogicNormal.execute_thread_function_by_scheduler,u"%s %s : %s"%(package_name,job.H,job.description),M,args=job.H)
    u(job_instance)
   else:
    if n(s_id):
     p(s_id)
   return 'success'
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return 'fail'
 @O
 def job_background(job_id):
  try:
   th=e(target=LogicNormal.execute_thread_function_job,args=(job_id,))
   th.setDaemon(M)
   th.start()
   return M
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return J
 @O
 def execute_thread_function_job(job_id):
  job=q(job_id)
  LogicNormal.execute_thread_function(job.command,command_id=job.H)
 @O
 def execute_thread_function(command,command_id=-1):
  try:
   l('COMMAND RUN START : %s %s',command,command_id)
   ret=[]
   import platform
   if platform.system()=='Windows':
    command=command.encode('cp949')
   command=command.split(' ')
   new_command=[]
   flag=J
   tmp=S
   for c in command:
    if c.startswith('"')and c.endswith('"'):
     new_command.append(c[1:-1])
    elif c.startswith('"'):
     flag=M
     tmp=c[1:]
    elif flag and c.endswith('"'):
     flag=J
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
    p=t(command,stdin=b,stdout=b,stderr=w,universal_newlines=M,bufsize=1)
    command_logger=S
    l(LogicNormal.process_list)
    if command_id!=-1:
     command_logger=get_logger('%s_%s'%(package_name,command_id))
     if command_id in LogicNormal.process_list and LogicNormal.process_list[command_id]is not S:
      LogicNormal.process_close(LogicNormal.process_list[command_id])
     LogicNormal.process_list[command_id]=p
    l(LogicNormal.process_list)
    with p.stdout:
     for line in L(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except i as e:
       try:
        line=line.decode('cp949')
       except i as e:
        pass
      if command_logger is not S:
       command_logger.debug(line.strip())
      ret.append(line.strip())
     p.wait()
    l('COMMAND RUN END : %s',command)
    p=S
    if command_id in LogicNormal.process_list:
     del LogicNormal.process_list[command_id]
    return ret
  except i as e:
   s('Exception:%s',e)
   s(Q()) 
 @O
 def execute_thread_function_by_scheduler(*args,**kwargs):
  try:
   l('COMMAND RUN START BY SCHEDULE :%s',args[0])
   job=j.query(ModelCommand).filter_by(H=V(args[0])).first()
   LogicNormal.execute_thread_function(job.command,command_id=job.H)
   l('COMMAND RUN END BY SCHEDULE :%s',args[0])
  except i as e:
   s('Exception:%s',e)
   s(Q()) 
 @O
 def start_communicate2(process):
  LogicNormal.command_queue=c()
  sout=U(process.stdout.fileno(),'rb',closefd=J)
  def Pump(stream):
   queue=c()
   def rdr():
    l('START RDR')
    while M:
     buf=process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(S)
      break
    l('END RDR')
    queue.put(S)
    A(1)
   def clct():
    active=M
    l('START clct')
    while active:
     r=queue.get()
     if r is S:
      break
     try:
      while M:
       r1=queue.get(timeout=0.005)
       if r1 is S:
        active=J
        break
       else:
        r+=r1
     except:
      pass
     if r is not S:
      try:
       r=r.decode('utf-8')
      except i as e:
       try:
        r=r.decode('cp949')
       except i as e:
        s('Exception:%s',e)
        s(Q())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      LogicNormal.command_queue.put(r.replace('\x00',''))
    LogicNormal.command_queue.put('<END>')
    l('END clct')
   for tgt in[rdr,clct]:
    th=e(target=tgt)
    th.setDaemon(M)
    th.start()
  Pump(sout)
 @O
 def start_communicate_load():
  LogicNormal.command_queue=c()
  def func():
   position=0
   flag=M
   while LogicNormal.command_queue is not S:
    logs=LogicNormal.load_log_list.get_log()
    if logs:
     for log in logs:
      LogicNormal.command_queue.put(log.strip()+'\n')
    A(1)
  th=e(target=func)
  th.setDaemon(M)
  th.start()
 @O
 def send_queue_start():
  def send_queue_thread_function():
   l('send_queue_thread_function START')
   while LogicNormal.command_queue:
    line=LogicNormal.command_queue.get()
    if line=='<END>':
     o("end",S,namespace='/%s'%package_name,broadcast=M)
     break
    else:
     o("add",line,namespace='/%s'%package_name,broadcast=M)
   LogicNormal.send_queue_thread=S
   LogicNormal.command_queue=S
   LogicNormal.foreground_process=S
   l('send_queue_thread_function END')
  if LogicNormal.send_queue_thread is S:
   LogicNormal.send_queue_thread=e(target=send_queue_thread_function,args=())
   LogicNormal.send_queue_thread.start()
 @O
 def send_process_command(req):
  try:
   command=req.form['command']
   LogicNormal.foreground_process.stdin.write(b'%s\n'%command)
   LogicNormal.foreground_process.stdin.flush()
   return M
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return J
 @O
 def command_file_list():
  try:
   command_path=Y.join(path_data,'command')
   file_list=N(command_path)
   ret=[]
   for f in file_list:
    c=Y.join(command_path,f)
    if f.endswith('.py'):
     c='python %s'%c
    ret.append({'text':f,'value':c})
   return ret
  except i as e:
   s('Exception:%s',e)
   s(Q())
 @O
 def module_load(command,**kwargs):
  try:
   python_filename=command[1]
   python_sys_path=Y.dirname(python_filename)
   if python_sys_path not in C:
    C.insert(0,python_sys_path)
   l(C)
   module_name=Y.basename(python_filename).split('.py')[0]
   mod=__import__(module_name,fromlist=[])
   g(mod)
   args=command
   mod_command_load=z(mod,'main')
   if mod_command_load:
    mod_command_load(*args,**kwargs)
   return 'success'
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
