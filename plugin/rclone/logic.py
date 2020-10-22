import os
K=object
X=None
u=staticmethod
Y=Exception
J=str
W=True
k=iter
t=open
R=False
V=type
j=len
N=isinstance
p=int
c=os.path
from datetime import datetime
H=datetime.now
import traceback
b=traceback.format_exc
import logging
import subprocess
m=subprocess.STDOUT
D=subprocess.PIPE
e=subprocess.Popen
import time
import re
h=re.compile
import threading
a=threading.Thread
import json
import platform
F=platform.platform
Q=platform.system
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root
v=scheduler.is_include
n=scheduler.remove_job
O=scheduler.add_job_instance
y=db.session
from framework.job import Job
from framework.util import Util
I=Util.get_paging_info
from system.logic import SystemLogic
from.model import ModelSetting,ModelRcloneJob,ModelRcloneFile,ModelRcloneMount,ModelRcloneServe
g=ModelRcloneFile.id
q=ModelRcloneFile.name
L=ModelRcloneFile.job_id
U=ModelRcloneJob.remote_path
l=ModelRcloneJob.remote
G=ModelRcloneJob.local_path
C=ModelSetting.query
i=ModelSetting.set
M=ModelSetting.get
import plugin
E=plugin.socketio_callback
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(K):
 db_default={'auto_start':'False','interval':'10','web_page_size':'30','auro_start_rcd':'False','rclone_bin_path':'','rclone_config_path':'',}
 path_bin=path_rclone=path_config=X
 default_rclone_setting={'static':'--config %s --log-level INFO --stats 1s --stats-file-name-length 0','user':'--transfers=4 --checkers=8','move':'--delete-empty-src-dirs --create-empty-src-dirs --delete-after --drive-chunk-size=256M','copy':'--create-empty-src-dirs --delete-after --drive-chunk-size=256M','sync':'--create-empty-src-dirs --delete-after --drive-chunk-size=256M',}
 @u
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if y.query(ModelSetting).filter_by(key=key).count()==0:
     y.add(ModelSetting(key,value))
   y.commit()
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def plugin_load():
  try:
   import platform
   Logic.path_bin=c.join(path_app_root,'bin',Q())
      F=platform.platform
      Q=platform.system
   if Q()=='Linux':
    if F().find('86')==-1 and F().find('64')==-1:
     Logic.path_bin=c.join(path_app_root,'bin','LinuxArm')
    if F().find('arch')!=-1:
     Logic.path_bin=c.join(path_app_root,'bin','LinuxArm')
    if F().find('arm')!=-1:
     Logic.path_bin=c.join(path_app_root,'bin','LinuxArm') 
   Logic.path_rclone=c.join(Logic.path_bin,'rclone')
   Logic.path_config=c.join(path_app_root,'data','db','rclone.conf')
   Logic.default_rclone_setting['static']=Logic.default_rclone_setting['static']%Logic.path_config
   if Q()=='Windows':
    Logic.path_rclone+='.exe'
   Logic.db_init()
   if M('rclone_bin_path')=='':
    i('rclone_bin_path',Logic.path_rclone)
   else:
    Logic.path_rclone=M('rclone_bin_path')
   if M('rclone_config_path')=='':
    i('rclone_config_path',Logic.path_config)
   else:
    Logic.path_config=M('rclone_config_path')
   if C.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
   mount_list=y.query(ModelRcloneMount).filter_by().all()
   for m in mount_list:
    if m.auto_start:
     Logic.mount_execute(J(m.id))
   serve_list=y.query(ModelRcloneServe).filter_by().all()
   from.logic_serve import LogicServe
   for s in serve_list:
    if s.auto_start:
     LogicServe.serve_execute(J(s.id))
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def plugin_unload():
  try:
   for key,value in Logic.mount_process.items():
    if value is not X:
     Logic.mount_kill(key)
   from.logic_serve import LogicServe
   for key,value in LogicServe.serve_process.items():
    if value is not X:
     LogicServe.serve_kill(key)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def rclone_version():
  try:
   command=u'%s version'%(Logic.path_rclone)
   command=command.split(' ')
   logger.debug(command)
   process=e(command,stdout=D,stderr=m,universal_newlines=W,bufsize=1)
   ret=[]
   with process.stdout:
    for line in k(process.stdout.readline,b''):
     ret.append(line)
    process.wait()
   return ret
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def load_remotes():
  try:
   f=t(Logic.path_config,'r')
   ret=[]
   entity=X
   while W:
    line=f.readline()
    if not line:
     break
    line=line.strip()
    if line=='':
     continue
    match=h(r'\[(?P<name>.*?)\]').search(line)
    if match:
     if entity is not X:
      ret.append(entity)
      entity=X
     entity={}
     entity['name']=match.group('name')
    match=h(r'(?P<key>.*?)\s\=\s(?P<value>.*?)$').search(line)
    if match:
     if entity is not X:
      entity[match.group('key')]=match.group('value')
   f.close()
   if entity is not X:
    ret.append(entity)
   return ret
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def job_save(req):
  try:
   job_id=req.form['id']
   logger.debug('job_save id:%s',job_id)
   if job_id=='-1':
    job=ModelRcloneJob()
   else:
    job=y.query(ModelRcloneJob).filter_by(id=job_id).with_for_update().first()
   job.job_type=req.form['job_type']
   job.name=req.form['job_name']
   job.command=req.form['job_command']
   job.remote=req.form['job_remote']
   job.remote_path=req.form['job_remote_path'].strip()
   job.local_path=req.form['job_local_path'].strip()
   job.option_user=req.form['job_option_user'].strip()
   job.option_static=req.form['job_option_static'].strip()
   job.is_scheduling=(req.form['is_scheduling']=='True')
   y.add(job)
   y.commit()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
 @u
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=y.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   y.commit()
   return W 
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return R
 @u
 def get_setting_value(key):
  try:
   return y.query(ModelSetting).filter_by(key=key).first().value
  except Y as e:
   logger.error('Exception:%s %s',key,e)
   logger.error(b())
 @u
 def scheduler_start():
  try:
   interval=C.filter_by(key='interval').first().value
   job=Job(package_name,package_name,interval,Logic.scheduler_function,u"Rclone 스케쥴링",W)
   O(job)
   logger.debug('Rclone scheduler_start %s',interval)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def scheduler_stop():
  try:
   logger.debug('auto scheduler_stop')
   Logic.kill() 
   n(package_name)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def get_jobs():
  try:
   job_list=y.query(ModelRcloneJob).filter_by().all()
   ret=[x.as_dict()for x in job_list]
   return ret
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 current_process=X
 current_log_thread=X
 current_data=X
 running_status=R 
 @u
 def scheduler_function():
  try:
   logger.debug('rclone scheduler_function')
   if not v(package_name):
    logger.debug('not in scheduler')
    return
   if Logic.running_status:
    logger.debug('Logic.running_status is TRUE!!!!')
    return
   else:
    logger.debug('Logic.running_status is FALSE!!!!')
   job_list=y.query(ModelRcloneJob).filter_by(is_scheduling=W).with_for_update().all()
   Logic.running_status=W
   for job in job_list:
    Logic.execute(job)
    if not v(package_name):
     logger.debug('scheduler is stopped by user button')
     break
   Logic.current_process=X 
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
  finally:
   Logic.running_status=R
 @u
 def get_user_command_list(data):
  ret=[]
  one=''
  flag=R
  for d in data:
   if d==' ':
    if flag==R:
     ret.append(one)
     one=''
     continue
   elif d=='"':
    flag=not flag
    logger.debug(flag)
    continue
   one+=d
  ret.append(one)
  return ret
 @u 
 def execute(job):
  try:
   logger.debug(job)
   command='%s %s %s %s:%s %s %s'%(Logic.path_rclone,job.command,job.local_path,job.remote,job.remote_path,job.option_static,job.option_user)
   import platform
   if Q()=='Windows':
      F=platform.platform
      Q=platform.system
    tmp=command
    tmp=command.encode('cp949')
   else:
    tmp=[Logic.path_rclone,job.command,job.local_path,'%s:%s'%(job.remote,job.remote_path)]+job.option_static.split(' ')+Logic.get_user_command_list(job.option_user)
   logger.debug('type : %s',V(tmp))
   logger.debug('tmp : %s',tmp)
   Logic.current_process=e(tmp,stdout=D,stderr=m,universal_newlines=W,bufsize=1)
   Logic.current_data={}
   Logic.current_data['job']=job.as_dict()
   Logic.current_data['command']=command
   Logic.current_data['log']=[]
   Logic.current_data['files']=[]
   Logic.trans_callback('start')
   Logic.current_log_thread=a(target=Logic.log_thread_fuction,args=())
   Logic.current_log_thread.start()
   logger.debug('normally process wait()')
   Logic.current_data['return_code']=Logic.current_process.wait()
   Logic.trans_callback('finish')
   job.last_run_time=H()
   job.last_file_count=j(Logic.current_data['files'])
   y.commit()
  except OperationalError as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   y.rollback()
   logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def execute_job(req):
  try:
   job_id=req.form['id']
   return Logic.execute_by_job_id(job_id)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b()) 
   return 'fail'
 @u
 def execute_by_job_id(job_id):
  try:
   job=y.query(ModelRcloneJob).filter_by(id=job_id).with_for_update().first()
   thread=a(target=Logic.execute,args=(job,))
   thread.start()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b()) 
   return 'fail'
 @u
 def remove_job(req):
  try:
   job_id=req.form['id']
   logger.debug('remove_job id:%s',job_id)
   job=y.query(ModelRcloneJob).filter_by(id=job_id).first()
   y.delete(job)
   y.commit()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b()) 
   return 'fail'
 trans_regexes=[r'Transferred\:\s*(?P<trans_data_current>\d.*?)\s\/\s(?P<trans_total_size>\d.*?)\,\s*((?P<trans_percent>\d+)\%)?\-?\,\s*(?P<trans_speed>\d.*?)\,\sETA\s(((?P<rt_hour>\d+)h)*((?P<rt_min>\d+)m)*((?P<rt_sec>.*?)s)*)?\-?',r'Errors\:\s*(?P<error>\d+)',r'Checks\:\s*(?P<check_1>\d+)\s\/\s(?P<check_2>\d+)\,\s*(?P<check_percent>\d+)?\-?',r'Transferred\:\s*(?P<file_1>\d+)\s\/\s(?P<file_2>\d+)\,\s*((?P<file_percent>\d+)\%)?\-?',r'Elapsed\stime\:\s*((?P<r_hour>\d+)h)*((?P<r_min>\d+)m)*((?P<r_sec>.*?)s)*',r'\s*\*\s((?P<folder>.*)\/)?(?P<name>.*?)\:\s*(?P<percent>\d+)\%\s*\/(?P<size>\d.*?)\,\s*(?P<speed>\d.*?)\,\s*((?P<rt_hour>\d+)h)*((?P<rt_min>\d+)m)*((?P<rt_sec>.*?)s)*',r'INFO\s*\:\s*((?P<folder>.*)\/)?(?P<name>.*?)\:\s*(?P<status>.*)']
 @u
 def log_thread_fuction():
  with Logic.current_process.stdout:
   ts=X
   for line in k(Logic.current_process.stdout.readline,b''):
    line=line.strip()
    try:
     try:
      line=line.decode('utf-8')
     except Y as e:
      try:
       line=line.decode('cp949')
      except Y as e:
       pass
     if line=='' or line.startswith('Checking'):
      continue
     if line.endswith('INFO  :'):
      continue
     if line.startswith('Deleted:'):
      continue
     if line.startswith('Transferring:'):
      ts.files=[]
      continue
     match=h(Logic.trans_regexes[0]).search(line)
     if match:
      if ts is not X:
       Logic.trans_callback('status',ts)
      ts=TransStatus()
      ts.trans_data_current=match.group('trans_data_current')
      ts.trans_total_size=match.group('trans_total_size')
      ts.trans_percent=match.group('trans_percent')if 'trans_percent' in match.groupdict()else '0'
      ts.trans_speed=match.group('trans_speed')
      ts.rt_hour=match.group('rt_hour')if 'rt_hour' in match.groupdict()else '0'
      ts.rt_min=match.group('rt_min')if 'rt_min' in match.groupdict()else '0'
      ts.rt_sec=match.group('rt_sec')if 'rt_sec' in match.groupdict()else '0'
      continue
     match=h(Logic.trans_regexes[1]).search(line)
     if match:
      ts.error=match.group('error')
      continue
     match=h(Logic.trans_regexes[2]).search(line)
     if match:
      ts.check_1=match.group('check_1')
      ts.check_2=match.group('check_2')
      ts.check_percent=match.group('check_percent')if 'check_percent' in match.groupdict()else '0'
      continue
     match=h(Logic.trans_regexes[3]).search(line)
     if match:
      ts.file_1=match.group('file_1')
      ts.file_2=match.group('file_2')
      ts.file_percent=match.group('file_percent')if 'file_percent' in match.groupdict()else '0'
      continue
     match=h(Logic.trans_regexes[4]).search(line)
     if match:
      ts.r_hour=match.group('r_hour')if 'r_hour' in match.groupdict()else '0'
      ts.r_min=match.group('r_min')if 'r_min' in match.groupdict()else '0'
      ts.r_sec=match.group('r_sec')if 'r_sec' in match.groupdict()else '0'
      continue
     match=h(Logic.trans_regexes[5]).search(line)
     if match:
      Logic.set_file(match)
      continue
     if line.startswith('Renamed:'):
      continue
     if line.find('INFO :')==-1:
      Logic.current_data['log'].append(line)
      Logic.trans_callback('log')
     match=h(Logic.trans_regexes[6]).search(line)
     if match:
      Logic.trans_callback('files',FileFinished(match))
      continue
     logger.debug('NOT PROCESS : %s',line) 
    except Y as e:
     logger.error('Exception:%s',e)
     logger.error(b())
   logger.debug('rclone log thread end')
  Logic.trans_callback('status',ts)
 @u
 def kill():
  try:
   if Logic.current_process is not X and Logic.current_process.poll()is X:
    import psutil
    process=psutil.Process(Logic.current_process.pid)
    for proc in process.children(recursive=W):
     proc.kill()
    process.kill()
    return 'success'
   return 'not_running'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
 @u
 def trans_callback(cmd,data=X):
  try:
   if data is not X:
    if N(data,FileFinished):
     f=Logic.get_by_name(data.folder,data.name)
     if f is not X:
      if f.log!='':
       f.log='%s,%s'%(f.log,data.status)
      else:
       f.log=data.status
      f.finish_time=H()if f.finish_time is X else f.finish_time
      y.add(f)
      y.commit()
     pass
    elif N(data,TransStatus):
     Logic.current_data['ts']=data.__dict__
   E(cmd,Logic.current_data)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def set_file(match):
  folder=match.group('folder')if 'folder' in match.groupdict()else ''
  name=match.group('name')
  instance=Logic.get_by_name(folder,name)
  if instance is X:
   instance=ModelRcloneFile(Logic.current_data['job']['id'],folder,name)
   Logic.current_data['files'].append(instance)
  instance.percent=p(match.group('percent'))
  instance.size=match.group('size')
  instance.speed=match.group('speed')
  instance.rt_hour=match.group('rt_hour')if 'rt_hour' in match.groupdict()else '0'
  instance.rt_min=match.group('rt_min')if 'rt_min' in match.groupdict()else '0'
  instance.rt_sec=match.group('rt_sec')if 'rt_sec' in match.groupdict()else '0'
  return instance
 @u
 def get_by_name(folder,name):
  instance=X
  for item in Logic.current_data['files']:
   if item.folder==folder and item.name==name:
    instance=item
    break
  return instance
 @u
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=p(y.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=p(req.form['page'])
   if 'job_select' in req.form:
    if req.form['job_select']!='all':
     job_id=p(req.form['job_select'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=y.query(ModelRcloneFile)
   if job_id!='':
    query=query.filter(L==job_id)
   if search!='':
    query=query.filter(q.like('%'+search+'%'))
   count=query.count()
   query=(query.order_by(desc(g)).limit(page_size).offset((page-1)*page_size))
   logger.debug('ModelRcloneFile count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=I(count,page,page_size)
   return ret
  except Y as e:
   logger.debug('Exception:%s',e)
   logger.debug(b())
 @u
 def rclone_job_by_ktv(local,remote,remove=R):
  try:
   logger.debug('job_save_by_ktv:%s %s %s',local,remote,remove)
   job=y.query(ModelRcloneJob) .filter(G==local) .filter(l==remote.split(':')[0]) .filter(U==remote.split(':')[1]).first()
   if job:
    if remove:
     y.delete(job)
     y.commit()
    else:
     pass
   else:
    if remove:
     pass
    else:
     job=ModelRcloneJob()
     job.job_type=1
     job.name='ktv_%s'%remote.split(':')[0]
     job.command='move'
     job.remote=remote.split(':')[0]
     job.remote_path=remote.split(':')[1]
     job.local_path=local
     job.option_user=Logic.default_rclone_setting['user']+' '+Logic.default_rclone_setting['move']
     job.option_static=Logic.default_rclone_setting['static']
     job.is_scheduling=W
     y.add(job)
     y.commit()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
 @u
 def reset_db():
  try:
   y.query(ModelRcloneFile).delete()
   y.commit()
   return W
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return R
 @u
 def get_log(req):
  try:
   ret={}
   ret['ret']=R
   where=req.form['type']
   db_id=req.form['id']
   log_filename=X
   if where=='serve':
    item=y.query(ModelRcloneServe).filter_by(id=db_id).first()
    if item is not X:
     if item.name=='':
      log_filename='serve_%s'%item.id
     else:
      log_filename='serve_%s'%item.name
     log_filename=c.join(path_app_root,'data','log','%s.log'%log_filename)
    else:
     ret['ret']='fail'
   elif where=='mount':
    item=y.query(ModelRcloneMount).filter_by(id=db_id).first()
    if item is not X:
     if item.name=='':
      log_filename='mount_%s'%item.id
     else:
      log_filename='mount_%s'%item.name
     log_filename=c.join(path_app_root,'data','log','%s.log'%log_filename)
    else:
     ret['ret']='fail'
   if log_filename is not X:
    logger.debug(log_filename)
    import codecs
    f=codecs.t(log_filename,'r',encoding='utf8')
    ret['data']=[]
    for line in f:
     ret['data'].append(line)
    f.close()
    ret['ret']='success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   ret['data']=J(e)
  return ret
 mount_process={}
 @u
 def mount_save(req):
  try:
   mount_id=req.form['id']
   if mount_id=='-1':
    item=ModelRcloneMount()
   else:
    item=y.query(ModelRcloneMount).filter_by(id=p(mount_id)).with_for_update().first()
   item.name=req.form['mount_name'].strip()
   item.remote=req.form['mount_remote']
   item.remote_path=req.form['mount_remote_path'].strip()
   item.local_path=req.form['mount_local_path'].strip()
   item.option=req.form['mount_option'].strip()
   item.auto_start=(req.form['auto_start']=='True')
   y.add(item)
   y.commit()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
 @u
 def mount_list():
  try:
   job_list=y.query(ModelRcloneMount).filter_by().all()
   ret=[x.as_dict()for x in job_list]
   for t in ret:
    t['current_status']=(J(t['id'])in Logic.mount_process and Logic.mount_process[J(t['id'])]is not X)
   return ret
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 @u
 def mount_execute(mount_id):
  try:
   item=y.query(ModelRcloneMount).filter_by(id=p(mount_id)).with_for_update().first()
   remote_path='%s:%s'%(item.remote,item.remote_path)
   local_path=item.local_path
   if Q()=='Windows':
    remote_path=remote_path.encode('cp949')
    local_path=local_path.encode('cp949')
   options=item.option.replace(' --daemon','').strip().split(' ')
   command=[Logic.path_rclone,'--config',Logic.path_config,'mount',remote_path,local_path]
   command+=options
   command.append('--log-file')
   if item.name=='':
    log_filename='mount_%s'%item.id
   else:
    log_filename='mount_%s'%item.name
   log_filename=c.join(path_app_root,'data','log','%s.log'%log_filename)
   command.append(log_filename)
   logger.debug(command)
   try:
    if Q()=='Linux':
     fuse_unmount_command=['fusermount','-uz',local_path]
     p1=e(fuse_unmount_command)
     p1.wait()
   except Y as e:
    logger.error('Exception:%s',e)
    logger.error(b())
   process=e(command)
   logger.debug('process.pid:%s',process)
   Logic.mount_process[mount_id]=process
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
 @u
 def mount_stop(req):
  mount_id=req.form['id']
  logger.debug('mount stop:%s'%mount_id)
  return Logic.mount_kill(mount_id)
 @u
 def mount_kill(mount_id):
  try:
   if mount_id in Logic.mount_process:
    process=Logic.mount_process[mount_id]
    logger.debug('process:%s,%s',process,process.poll())
    if process is not X and process.poll()is X:
     import psutil
     p=psutil.Process(process.pid)
     for proc in p.children(recursive=W):
      proc.kill()
     p.kill()
     try:
      job=y.query(ModelRcloneMount).filter_by(id=p(mount_id)).first()
      import platform
      if Q()!='Windows':
                     F=platform.platform
                     Q=platform.system
       tmp=['fusermount','-uz',job.local_path]
       e(tmp)
       logger.debug('execute fusermount -uz')
     except:
      logger.debug('fusermount error')
     return 'success'
    else:
     return 'already_stop'
   else:
    return 'not_running'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return 'fail'
  finally:
   Logic.mount_process[mount_id]=X
 @u
 def mount_remove(mount_id):
  try:
   logger.debug('remove_job id:%s',mount_id)
   job=y.query(ModelRcloneMount).filter_by(id=p(mount_id)).first()
   y.delete(job)
   y.commit()
   return 'success'
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b()) 
   return 'fail'
class TransStatus(K):
 def __init__(self):
  self.trans_data_current= self.trans_total_size= self.trans_percent= self.trans_speed= self.rt_hour=self.rt_min=self.rt_sec= self.error= self.check_1= self.check_2= self.check_percent= self.file_1= self.file_2= self.file_percent= self.r_hour=self.r_min=self.r_sec=""
class FileFinished(K):
 def __init__(self,match):
  self.folder=match.group('folder')if 'folder' in match.groupdict()else ''
  self.name=match.group('name')
  self.status=match.group('status')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
