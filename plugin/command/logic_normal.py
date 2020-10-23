import os
z=list
L=Exception
n=object
Y=None
d=staticmethod
F=True
T=False
h=id
A=iter
v=int
g=getattr
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
from framework import app,db,scheduler,path_data,socketio,py_queue,py_reload
from framework.job import Job
from framework.util import Util
from.plugin import package_name,logger
from.model import ModelCommand
from io import BytesIO as StringIO
import sys
class Capturing(z):
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
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return self
class LogicNormal(n):
 foreground_process=Y
 command_queue=Y
 send_queue_thread=Y
 process_list={}
 load_log_list=Y
 @d
 def plugin_load():
  def plugin_load_thread():
   try:
    db_list=db.session.query(ModelCommand).filter().all()
    for item in db_list:
     if '%s'%item.schedule_type=='1':
      th=threading.Thread(target=LogicNormal.execute_thread_function,args=(item.command,item.h))
      th.setDaemon(F)
      th.start()
     elif '%s'%item.schedule_type=='2' and item.schedule_auto_start:
      LogicNormal.scheduler_switch(item.h,F)
   except L as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
  try:
   th=threading.Thread(target=plugin_load_thread)
   th.setDaemon(F)
   th.start()
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def plugin_unload():
  try:
   LogicNormal.foreground_command_close()
   for key,p in LogicNormal.process_list.items():
    LogicNormal.process_close(p)
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def foreground_command(command,job_id=Y):
  try:
   command=command.split(' ')
   if command[0]=='LOAD':
    def func():
     LogicNormal.load_log_list=[]
     with Capturing()as LogicNormal.load_log_list: 
      LogicNormal.start_communicate_load()
      if job_id is not Y:
       command_logger=get_logger('%s_%s'%(package_name,job_id))
       LogicNormal.module_load(command,logger=command_logger)
      else:
       LogicNormal.module_load(command)
     for t in LogicNormal.load_log_list:
      LogicNormal.command_queue.put(t+'\n')
     LogicNormal.command_queue.put('<END>')
    th=threading.Thread(target=func,args=())
    th.setDaemon(F)
    th.start()
    return 'success'
   else:
    if LogicNormal.foreground_process is not Y:
     LogicNormal.foreground_command_close()
     time.sleep(0.5)
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=F,bufsize=1)
    LogicNormal.foreground_process=process
    LogicNormal.start_communicate2(process)
   return 'success'
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @d
 def foreground_command_close():
  LogicNormal.process_close(LogicNormal.foreground_process)
 @d
 def process_close(process):
  try:
   if process is Y:
    return
   try:
    import psutil
    ps_process=psutil.Process(process.pid)
    for proc in ps_process.children(recursive=F):
     proc.kill()
    ps_process.kill()
    return F
   except:
    pass
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return T
 @d
 def scheduler_switch0(request):
  try:
   switch=request.form['switch']
   job_id=request.form['job_id']
   LogicNormal.scheduler_switch(job_id,(switch=='true'))
   return 'success'
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @d
 def scheduler_switch(h,switch):
  try:
   job=ModelCommand.get_job_by_id(h)
   s_id='command_%s'%h
   if switch:
    job_instance=Job(package_name,s_id,job.schedule_info,LogicNormal.execute_thread_function_by_scheduler,u"%s %s : %s"%(package_name,job.h,job.description),F,args=job.h)
    scheduler.add_job_instance(job_instance)
   else:
    if scheduler.is_include(s_id):
     scheduler.remove_job(s_id)
   return 'success'
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @d
 def job_background(job_id):
  try:
   th=threading.Thread(target=LogicNormal.execute_thread_function_job,args=(job_id,))
   th.setDaemon(F)
   th.start()
   return F
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return T
 @d
 def execute_thread_function_job(job_id):
  job=ModelCommand.get_job_by_id(job_id)
  LogicNormal.execute_thread_function(job.command,command_id=job.h)
 @d
 def execute_thread_function(command,command_id=-1):
  try:
   logger.debug('COMMAND RUN START : %s %s',command,command_id)
   ret=[]
   import platform
   if platform.system()=='Windows':
    command=command.encode('cp949')
   command=command.split(' ')
   new_command=[]
   flag=T
   tmp=Y
   for c in command:
    if c.startswith('"')and c.endswith('"'):
     new_command.append(c[1:-1])
    elif c.startswith('"'):
     flag=F
     tmp=c[1:]
    elif flag and c.endswith('"'):
     flag=T
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
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=F,bufsize=1)
    command_logger=Y
    logger.debug(LogicNormal.process_list)
    if command_id!=-1:
     command_logger=get_logger('%s_%s'%(package_name,command_id))
     if command_id in LogicNormal.process_list and LogicNormal.process_list[command_id]is not Y:
      LogicNormal.process_close(LogicNormal.process_list[command_id])
     LogicNormal.process_list[command_id]=p
    logger.debug(LogicNormal.process_list)
    with p.stdout:
     for line in A(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except L as exception:
       try:
        line=line.decode('cp949')
       except L as exception:
        pass
      if command_logger is not Y:
       command_logger.debug(line.strip())
      ret.append(line.strip())
     p.wait()
    logger.debug('COMMAND RUN END : %s',command)
    p=Y
    if command_id in LogicNormal.process_list:
     del LogicNormal.process_list[command_id]
    return ret
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @d
 def execute_thread_function_by_scheduler(*args,**kwargs):
  try:
   logger.debug('COMMAND RUN START BY SCHEDULE :%s',args[0])
   job=db.session.query(ModelCommand).filter_by(h=v(args[0])).first()
   LogicNormal.execute_thread_function(job.command,command_id=job.h)
   logger.debug('COMMAND RUN END BY SCHEDULE :%s',args[0])
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @d
 def start_communicate2(process):
  LogicNormal.command_queue=py_queue.Queue()
  sout=io.open(process.stdout.fileno(),'rb',closefd=T)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while F:
     buf=process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(Y)
      break
    logger.debug('END RDR')
    queue.put(Y)
    time.sleep(1)
   def clct():
    active=F
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is Y:
      break
     try:
      while F:
       r1=queue.get(timeout=0.005)
       if r1 is Y:
        active=T
        break
       else:
        r+=r1
     except:
      pass
     if r is not Y:
      try:
       r=r.decode('utf-8')
      except L as exception:
       try:
        r=r.decode('cp949')
       except L as exception:
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
    th.setDaemon(F)
    th.start()
  Pump(sout)
 @d
 def start_communicate_load():
  LogicNormal.command_queue=py_queue.Queue()
  def func():
   position=0
   flag=F
   while LogicNormal.command_queue is not Y:
    logs=LogicNormal.load_log_list.get_log()
    if logs:
     for log in logs:
      LogicNormal.command_queue.put(log.strip()+'\n')
    time.sleep(1)
  th=threading.Thread(target=func)
  th.setDaemon(F)
  th.start()
 @d
 def send_queue_start():
  def send_queue_thread_function():
   logger.debug('send_queue_thread_function START')
   while LogicNormal.command_queue:
    line=LogicNormal.command_queue.get()
    if line=='<END>':
     socketio.emit("end",Y,namespace='/%s'%package_name,broadcast=F)
     break
    else:
     socketio.emit("add",line,namespace='/%s'%package_name,broadcast=F)
   LogicNormal.send_queue_thread=Y
   LogicNormal.command_queue=Y
   LogicNormal.foreground_process=Y
   logger.debug('send_queue_thread_function END')
  if LogicNormal.send_queue_thread is Y:
   LogicNormal.send_queue_thread=threading.Thread(target=send_queue_thread_function,args=())
   LogicNormal.send_queue_thread.start()
 @d
 def send_process_command(req):
  try:
   command=req.form['command']
   LogicNormal.foreground_process.stdin.write(b'%s\n'%command)
   LogicNormal.foreground_process.stdin.flush()
   return F
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return T
 @d
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
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def module_load(command,**kwargs):
  try:
   python_filename=command[1]
   python_sys_path=os.path.dirname(python_filename)
   if python_sys_path not in sys.path:
    sys.path.insert(0,python_sys_path)
   logger.debug(sys.path)
   module_name=os.path.basename(python_filename).split('.py')[0]
   mod=__import__(module_name,fromlist=[])
   py_reload(mod)
   args=command
   mod_command_load=g(mod,'main')
   if mod_command_load:
    mod_command_load(*args,**kwargs)
   return 'success'
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
