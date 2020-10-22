import os
K=list
Y=Exception
l=object
f=None
k=staticmethod
n=True
S=False
I=id
m=iter
d=int
s=reload
V=getattr
import sys
from datetime import datetime
import traceback
import logging
import subprocess
import threading
import time
import io
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,py_queue
from framework.job import Job
from framework.util import Util
from.plugin import package_name,logger
from.model import ModelCommand
from io import BytesIO as StringIO
import sys
class Capturing(K):
 def __enter__(self):
  self._stdout=sys.stdout
  sys.stdout=self._stringio=StringIO()
  return self
 def __exit__(self,*args):
  self.extend(self._stringio.getvalue().splitlines())
  del self._stringio 
  sys.stdout=self._stdout
 def get_log(self):
  try:
   ret=self._stringio.getvalue().splitlines()
   self._stringio.truncate(0)
   return ret
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return self
class LogicNormal(l):
 foreground_process=f
 command_queue=f
 send_queue_thread=f
 process_list={}
 load_log_list=f
 @k
 def plugin_load():
  def plugin_load_thread():
   try:
    db_list=db.session.query(ModelCommand).filter().all()
    for item in db_list:
     if '%s'%item.schedule_type=='1':
      th=threading.Thread(target=LogicNormal.execute_thread_function,args=(item.command,item.I))
      th.setDaemon(n)
      th.start()
     elif '%s'%item.schedule_type=='2' and item.schedule_auto_start:
      LogicNormal.scheduler_switch(item.I,n)
   except Y as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
  try:
   th=threading.Thread(target=plugin_load_thread)
   th.setDaemon(n)
   th.start()
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @k
 def plugin_unload():
  try:
   LogicNormal.foreground_command_close()
   for key,p in LogicNormal.process_list.items():
    LogicNormal.process_close(p)
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @k
 def foreground_command(command,job_id=f):
  try:
   command=command.split(' ')
   if command[0]=='LOAD':
    def func():
     LogicNormal.load_log_list=[]
     with Capturing()as LogicNormal.load_log_list: 
      LogicNormal.start_communicate_load()
      if job_id is not f:
       command_logger=get_logger('%s_%s'%(package_name,job_id))
       LogicNormal.module_load(command,logger=command_logger)
      else:
       LogicNormal.module_load(command)
     for t in LogicNormal.load_log_list:
      LogicNormal.command_queue.put(t+'\n')
     LogicNormal.command_queue.put('<END>')
    th=threading.Thread(target=func,args=())
    th.setDaemon(n)
    th.start()
    return 'success'
   else:
    if LogicNormal.foreground_process is not f:
     LogicNormal.foreground_command_close()
     time.sleep(0.5)
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=n,bufsize=1)
    LogicNormal.foreground_process=process
    LogicNormal.start_communicate2(process)
   return 'success'
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @k
 def foreground_command_close():
  LogicNormal.process_close(LogicNormal.foreground_process)
 @k
 def process_close(process):
  try:
   if process is f:
    return
   try:
    import psutil
    ps_process=psutil.Process(process.pid)
    for proc in ps_process.children(recursive=n):
     proc.kill()
    ps_process.kill()
    return n
   except:
    pass
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return S
 @k
 def scheduler_switch0(request):
  try:
   switch=request.form['switch']
   job_id=request.form['job_id']
   LogicNormal.scheduler_switch(job_id,(switch=='true'))
   return 'success'
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @k
 def scheduler_switch(I,switch):
  try:
   job=ModelCommand.get_job_by_id(I)
   s_id='command_%s'%I
   if switch:
    job_instance=Job(package_name,s_id,job.schedule_info,LogicNormal.execute_thread_function_by_scheduler,u"%s %s : %s"%(package_name,job.I,job.description),n,args=job.I)
    scheduler.add_job_instance(job_instance)
   else:
    if scheduler.is_include(s_id):
     scheduler.remove_job(s_id)
   return 'success'
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @k
 def job_background(job_id):
  try:
   th=threading.Thread(target=LogicNormal.execute_thread_function_job,args=(job_id,))
   th.setDaemon(n)
   th.start()
   return n
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return S
 @k
 def execute_thread_function_job(job_id):
  job=ModelCommand.get_job_by_id(job_id)
  LogicNormal.execute_thread_function(job.command,command_id=job.I)
 @k
 def execute_thread_function(command,command_id=-1):
  try:
   logger.debug('COMMAND RUN START : %s %s',command,command_id)
   ret=[]
   import platform
   if platform.system()=='Windows':
    command=command.encode('cp949')
   command=command.split(' ')
   new_command=[]
   flag=S
   tmp=f
   for c in command:
    if c.startswith('"')and c.endswith('"'):
     new_command.append(c[1:-1])
    elif c.startswith('"'):
     flag=n
     tmp=c[1:]
    elif flag and c.endswith('"'):
     flag=S
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
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=n,bufsize=1)
    command_logger=f
    logger.debug(LogicNormal.process_list)
    if command_id!=-1:
     command_logger=get_logger('%s_%s'%(package_name,command_id))
     if command_id in LogicNormal.process_list and LogicNormal.process_list[command_id]is not f:
      LogicNormal.process_close(LogicNormal.process_list[command_id])
     LogicNormal.process_list[command_id]=p
    logger.debug(LogicNormal.process_list)
    with p.stdout:
     for line in m(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except Y as exception:
       try:
        line=line.decode('cp949')
       except Y as exception:
        pass
      if command_logger is not f:
       command_logger.debug(line.strip())
      ret.append(line.strip())
     p.wait()
    logger.debug('COMMAND RUN END : %s',command)
    p=f
    if command_id in LogicNormal.process_list:
     del LogicNormal.process_list[command_id]
    return ret
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @k
 def execute_thread_function_by_scheduler(*args,**kwargs):
  try:
   logger.debug('COMMAND RUN START BY SCHEDULE :%s',args[0])
   job=db.session.query(ModelCommand).filter_by(I=d(args[0])).first()
   LogicNormal.execute_thread_function(job.command,command_id=job.I)
   logger.debug('COMMAND RUN END BY SCHEDULE :%s',args[0])
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @k
 def start_communicate2(process):
  LogicNormal.command_queue=py_queue.Queue()
  sout=io.open(process.stdout.fileno(),'rb',closefd=S)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while n:
     buf=process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(f)
      break
    logger.debug('END RDR')
    queue.put(f)
    time.sleep(1)
   def clct():
    active=n
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is f:
      break
     try:
      while n:
       r1=queue.get(timeout=0.005)
       if r1 is f:
        active=S
        break
       else:
        r+=r1
     except:
      pass
     if r is not f:
      try:
       r=r.decode('utf-8')
      except Y as exception:
       try:
        r=r.decode('cp949')
       except Y as exception:
        logger.error('Exception:%s',exception)
        logger.error(traceback.format_exc())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      LogicNormal.command_queue.put(r.replace('\x00',''))
    LogicNormal.command_queue.put('<END>')
    logger.debug('END clct')
   for tgt in[rdr,clct]:
    th=threading.Thread(target=tgt)
    th.setDaemon(n)
    th.start()
  Pump(sout)
 @k
 def start_communicate_load():
  LogicNormal.command_queue=py_queue.Queue()
  def func():
   position=0
   flag=n
   while LogicNormal.command_queue is not f:
    logs=LogicNormal.load_log_list.get_log()
    if logs:
     for log in logs:
      LogicNormal.command_queue.put(log.strip()+'\n')
    time.sleep(1)
  th=threading.Thread(target=func)
  th.setDaemon(n)
  th.start()
 @k
 def send_queue_start():
  def send_queue_thread_function():
   logger.debug('send_queue_thread_function START')
   while LogicNormal.command_queue:
    line=LogicNormal.command_queue.get()
    if line=='<END>':
     socketio.emit("end",f,namespace='/%s'%package_name,broadcast=n)
     break
    else:
     socketio.emit("add",line,namespace='/%s'%package_name,broadcast=n)
   LogicNormal.send_queue_thread=f
   LogicNormal.command_queue=f
   LogicNormal.foreground_process=f
   logger.debug('send_queue_thread_function END')
  if LogicNormal.send_queue_thread is f:
   LogicNormal.send_queue_thread=threading.Thread(target=send_queue_thread_function,args=())
   LogicNormal.send_queue_thread.start()
 @k
 def send_process_command(req):
  try:
   command=req.form['command']
   LogicNormal.foreground_process.stdin.write(b'%s\n'%command)
   LogicNormal.foreground_process.stdin.flush()
   return n
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return S
 @k
 def command_file_list():
  try:
   command_path=os.path.join(path_data,'command')
   file_list=os.listdir(command_path)
   ret=[]
   for f in file_list:
    c=os.path.join(command_path,f)
    if f.endswith('.py'):
     c='python %s'%c
    ret.append({'text':f,'value':c})
   return ret
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @k
 def module_load(command,**kwargs):
  try:
   python_filename=command[1]
   python_sys_path=os.path.dirname(python_filename)
   if python_sys_path not in sys.path:
    sys.path.insert(0,python_sys_path)
   logger.debug(sys.path)
   module_name=os.path.basename(python_filename).split('.py')[0]
   mod=__import__(module_name,fromlist=[])
   s(mod)
   args=command
   mod_command_load=V(mod,'main')
   if mod_command_load:
    mod_command_load(*args,**kwargs)
   return 'success'
  except Y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
