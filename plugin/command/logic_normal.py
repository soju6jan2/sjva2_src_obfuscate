import os
j=list
t=Exception
b=object
H=None
x=staticmethod
w=True
m=False
W=id
B=iter
Q=int
h=reload
r=getattr
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
class Capturing(j):
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
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return self
class LogicNormal(b):
 foreground_process=H
 command_queue=H
 send_queue_thread=H
 process_list={}
 load_log_list=H
 @x
 def plugin_load():
  def plugin_load_thread():
   try:
    db_list=db.session.query(ModelCommand).filter().all()
    for item in db_list:
     if '%s'%item.schedule_type=='1':
      th=threading.Thread(target=LogicNormal.execute_thread_function,args=(item.command,item.W))
      th.setDaemon(w)
      th.start()
     elif '%s'%item.schedule_type=='2' and item.schedule_auto_start:
      LogicNormal.scheduler_switch(item.W,w)
   except t as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
  try:
   th=threading.Thread(target=plugin_load_thread)
   th.setDaemon(w)
   th.start()
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @x
 def plugin_unload():
  try:
   LogicNormal.foreground_command_close()
   for key,p in LogicNormal.process_list.items():
    LogicNormal.process_close(p)
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @x
 def foreground_command(command,job_id=H):
  try:
   command=command.split(' ')
   if command[0]=='LOAD':
    def func():
     LogicNormal.load_log_list=[]
     with Capturing()as LogicNormal.load_log_list: 
      LogicNormal.start_communicate_load()
      if job_id is not H:
       command_logger=get_logger('%s_%s'%(package_name,job_id))
       LogicNormal.module_load(command,logger=command_logger)
      else:
       LogicNormal.module_load(command)
     for t in LogicNormal.load_log_list:
      LogicNormal.command_queue.put(t+'\n')
     LogicNormal.command_queue.put('<END>')
    th=threading.Thread(target=func,args=())
    th.setDaemon(w)
    th.start()
    return 'success'
   else:
    if LogicNormal.foreground_process is not H:
     LogicNormal.foreground_command_close()
     time.sleep(0.5)
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=w,bufsize=1)
    LogicNormal.foreground_process=process
    LogicNormal.start_communicate2(process)
   return 'success'
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @x
 def foreground_command_close():
  LogicNormal.process_close(LogicNormal.foreground_process)
 @x
 def process_close(process):
  try:
   if process is H:
    return
   try:
    import psutil
    ps_process=psutil.Process(process.pid)
    for proc in ps_process.children(recursive=w):
     proc.kill()
    ps_process.kill()
    return w
   except:
    pass
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return m
 @x
 def scheduler_switch0(request):
  try:
   switch=request.form['switch']
   job_id=request.form['job_id']
   LogicNormal.scheduler_switch(job_id,(switch=='true'))
   return 'success'
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @x
 def scheduler_switch(W,switch):
  try:
   job=ModelCommand.get_job_by_id(W)
   s_id='command_%s'%W
   if switch:
    job_instance=Job(package_name,s_id,job.schedule_info,LogicNormal.execute_thread_function_by_scheduler,u"%s %s : %s"%(package_name,job.W,job.description),w,args=job.W)
    scheduler.add_job_instance(job_instance)
   else:
    if scheduler.is_include(s_id):
     scheduler.remove_job(s_id)
   return 'success'
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @x
 def job_background(job_id):
  try:
   th=threading.Thread(target=LogicNormal.execute_thread_function_job,args=(job_id,))
   th.setDaemon(w)
   th.start()
   return w
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return m
 @x
 def execute_thread_function_job(job_id):
  job=ModelCommand.get_job_by_id(job_id)
  LogicNormal.execute_thread_function(job.command,command_id=job.W)
 @x
 def execute_thread_function(command,command_id=-1):
  try:
   logger.debug('COMMAND RUN START : %s %s',command,command_id)
   ret=[]
   import platform
   if platform.system()=='Windows':
    command=command.encode('cp949')
   command=command.split(' ')
   new_command=[]
   flag=m
   tmp=H
   for c in command:
    if c.startswith('"')and c.endswith('"'):
     new_command.append(c[1:-1])
    elif c.startswith('"'):
     flag=w
     tmp=c[1:]
    elif flag and c.endswith('"'):
     flag=m
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
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=w,bufsize=1)
    command_logger=H
    logger.debug(LogicNormal.process_list)
    if command_id!=-1:
     command_logger=get_logger('%s_%s'%(package_name,command_id))
     if command_id in LogicNormal.process_list and LogicNormal.process_list[command_id]is not H:
      LogicNormal.process_close(LogicNormal.process_list[command_id])
     LogicNormal.process_list[command_id]=p
    logger.debug(LogicNormal.process_list)
    with p.stdout:
     for line in B(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except t as exception:
       try:
        line=line.decode('cp949')
       except t as exception:
        pass
      if command_logger is not H:
       command_logger.debug(line.strip())
      ret.append(line.strip())
     p.wait()
    logger.debug('COMMAND RUN END : %s',command)
    p=H
    if command_id in LogicNormal.process_list:
     del LogicNormal.process_list[command_id]
    return ret
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @x
 def execute_thread_function_by_scheduler(*args,**kwargs):
  try:
   logger.debug('COMMAND RUN START BY SCHEDULE :%s',args[0])
   job=db.session.query(ModelCommand).filter_by(W=Q(args[0])).first()
   LogicNormal.execute_thread_function(job.command,command_id=job.W)
   logger.debug('COMMAND RUN END BY SCHEDULE :%s',args[0])
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @x
 def start_communicate2(process):
  LogicNormal.command_queue=py_queue.Queue()
  sout=io.open(process.stdout.fileno(),'rb',closefd=m)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    logger.debug('START RDR')
    while w:
     buf=process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(H)
      break
    logger.debug('END RDR')
    queue.put(H)
    time.sleep(1)
   def clct():
    active=w
    logger.debug('START clct')
    while active:
     r=queue.get()
     if r is H:
      break
     try:
      while w:
       r1=queue.get(timeout=0.005)
       if r1 is H:
        active=m
        break
       else:
        r+=r1
     except:
      pass
     if r is not H:
      try:
       r=r.decode('utf-8')
      except t as exception:
       try:
        r=r.decode('cp949')
       except t as exception:
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
    th.setDaemon(w)
    th.start()
  Pump(sout)
 @x
 def start_communicate_load():
  LogicNormal.command_queue=py_queue.Queue()
  def func():
   position=0
   flag=w
   while LogicNormal.command_queue is not H:
    logs=LogicNormal.load_log_list.get_log()
    if logs:
     for log in logs:
      LogicNormal.command_queue.put(log.strip()+'\n')
    time.sleep(1)
  th=threading.Thread(target=func)
  th.setDaemon(w)
  th.start()
 @x
 def send_queue_start():
  def send_queue_thread_function():
   logger.debug('send_queue_thread_function START')
   while LogicNormal.command_queue:
    line=LogicNormal.command_queue.get()
    if line=='<END>':
     socketio.emit("end",H,namespace='/%s'%package_name,broadcast=w)
     break
    else:
     socketio.emit("add",line,namespace='/%s'%package_name,broadcast=w)
   LogicNormal.send_queue_thread=H
   LogicNormal.command_queue=H
   LogicNormal.foreground_process=H
   logger.debug('send_queue_thread_function END')
  if LogicNormal.send_queue_thread is H:
   LogicNormal.send_queue_thread=threading.Thread(target=send_queue_thread_function,args=())
   LogicNormal.send_queue_thread.start()
 @x
 def send_process_command(req):
  try:
   command=req.form['command']
   LogicNormal.foreground_process.stdin.write(b'%s\n'%command)
   LogicNormal.foreground_process.stdin.flush()
   return w
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return m
 @x
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
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @x
 def module_load(command,**kwargs):
  try:
   python_filename=command[1]
   python_sys_path=os.path.dirname(python_filename)
   if python_sys_path not in sys.path:
    sys.path.insert(0,python_sys_path)
   logger.debug(sys.path)
   module_name=os.path.basename(python_filename).split('.py')[0]
   mod=__import__(module_name,fromlist=[])
   h(mod)
   args=command
   mod_command_load=r(mod,'main')
   if mod_command_load:
    mod_command_load(*args,**kwargs)
   return 'success'
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
