import os
Q=object
J=None
b=int
x=str
V=False
w=len
D=Exception
q=True
X=iter
Y=staticmethod
import traceback
import threading
import subprocess
import platform
import re
from datetime import datetime
from pytz import timezone
import requests
from framework.logger import get_logger
from framework.util import Util
from ffmpeg.logic import Logic,Status
from ffmpeg.model import ModelSetting 
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Ffmpeg(Q):
 instance_list=[]
 idx=1
 def __init__(self,url,filename,plugin_id=J,listener=J,max_pf_count=J,call_plugin=J,temp_path=J,save_path=J,proxy=J,headers=J):
  self.thread=J
  self.url=url
  self.filename=filename
  self.plugin_id=plugin_id
  self.listener=listener
  self.max_pf_count=b(ModelSetting.query.filter_by(key='max_pf_count').first().value if max_pf_count is J else max_pf_count)
  self.call_plugin=call_plugin
  self.process=J
  self.temp_path=ModelSetting.query.filter_by(key='temp_path').first().value if temp_path is J else temp_path
  self.save_path=ModelSetting.query.filter_by(key='save_path').first().value if save_path is J else save_path
  self.proxy=proxy
  self.temp_fullpath=os.path.join(self.temp_path,filename)
  self.save_fullpath=os.path.join(self.save_path,filename)
  self.log_thread=J
  self.status=Status.READY
  self.duration=0
  self.duration_str=''
  self.current_duration=0
  self.percent=0
  self.current_pf_count=0
  self.idx=x(Ffmpeg.idx)
  Ffmpeg.idx+=1
  self.current_bitrate=''
  self.current_speed=''
  self.start_time=J
  self.end_time=J
  self.download_time=J
  self.start_event=threading.Event()
  self.exist=V
  self.filesize=0
  self.filesize_str=''
  self.download_speed=''
  self.headers=headers
  Ffmpeg.instance_list.append(self)
  logger.debug('Ffmpeg.instance_list LEN:%s',w(Ffmpeg.instance_list))
  if w(Ffmpeg.instance_list)>30:
   for f in Ffmpeg.instance_list:
    if f.thread is J and f.status!=Status.READY:
     Ffmpeg.instance_list.remove(f)
     break
    else:
     logger.debug('remove fail %s %s',f.thread,self.status)
 def start(self):
  self.thread=threading.Thread(target=self.thread_fuction,args=())
  self.thread.start()
  self.start_time=datetime.now()
  return self.get_data()
 def start_and_wait(self):
  self.start()
  self.thread.join(timeout=60*70)
 def stop(self):
  try:
   self.status=Status.USER_STOP
   self.kill()
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def kill(self):
  try:
   if self.process is not J and self.process.poll()is J:
    import psutil
    process=psutil.Process(self.process.pid)
    for proc in process.children(recursive=q):
     proc.kill()
    process.kill()
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def thread_fuction(self):
  try:
   import system
   user=x(system.ModelSetting.get('sjva_me_user_id'))
   try:
    from framework.common.util import AESCipher
    user=AESCipher.encrypt(user)
   except D as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
   if self.proxy is J:
    if self.headers is J:
     command=[Logic.path_ffmpeg,'-y','-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
    else:
     headers_command=[]
     for key,value in self.headers.items():
      if key.lower()=='user-agent':
       headers_command.append('-user_agent')
       headers_command.append('value')
      else:
       headers_command.append('-headers')
       headers_command.append('\'%s: "%s"\''%(key,value))
     command=[Logic.path_ffmpeg,'-y']+headers_command+['-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
   else:
    command=[Logic.path_ffmpeg,'-y','-http_proxy',self.proxy,'-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
   if platform.system()=='Windows':
    now=x(datetime.now()).replace(':','').replace('-','').replace(' ','-')
    filename=('%s'%now)+'.mp4'
    self.temp_fullpath=os.path.join(self.temp_path,filename)
    command.append(self.temp_fullpath)
   else:
    command.append(self.temp_fullpath)
   try:
    logger.debug(' '.join(command))
    if os.path.exists(self.temp_fullpath):
     for f in Ffmpeg.instance_list:
      if f.idx!=self.idx and f.temp_fullpath==self.temp_fullpath and f.status in[Status.DOWNLOADING,Status.READY]:
       self.status=Status.ALREADY_DOWNLOADING
       logger.debug('temp_fullpath ALREADY_DOWNLOADING')
       return
   except:
    pass
   self.process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=q,bufsize=1)
   self.status=Status.READY
   self.log_thread=threading.Thread(target=self.log_thread_fuction,args=())
   self.log_thread.start()
   self.start_event.wait(timeout=60)
   logger.debug('start_event awake.. ')
   if self.log_thread is J:
    logger.debug('log_thread is none')
    if self.status==Status.READY:
     self.status=Status.ERROR
    self.kill()
   elif self.status==Status.READY:
    logger.debug('still status.ready kill')
    self.status=Status.ERROR
    self.kill()
   else:
    logger.debug('normally process wait()')
    process_ret=self.process.wait(timeout=60*ModelSetting.get_int('timeout_minute'))
    logger.debug('process_ret :%s'%process_ret)
    if process_ret is J:
     if self.status!=Status.COMPLETED and self.status!=Status.USER_STOP and self.status!=Status.PF_STOP:
      self.status=Status.TIME_OVER
      self.kill()
    else:
     logger.debug('process end')
     if self.status==Status.DOWNLOADING:
      self.status=Status.FORCE_STOP
   self.end_time=datetime.now()
   self.download_time=self.end_time-self.start_time
   try:
    if self.status==Status.COMPLETED:
     if self.save_fullpath!=self.temp_fullpath:
      if os.path.exists(self.save_fullpath):
       os.remove(self.save_fullpath)
      os.chmod(self.temp_fullpath,777)
      import shutil
      shutil.move(self.temp_fullpath,self.save_fullpath)
      self.filesize=os.stat(self.save_fullpath).st_size
    else:
     if os.path.exists(self.temp_fullpath):
      os.remove(self.temp_fullpath)
   except D as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
   arg={'type':'last','status':self.status,'data':self.get_data()}
   self.send_to_listener(**arg)
   self.process=J
   self.thread=J
   logger.debug('ffmpeg thread end')
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   try:
    self.status=Status.EXCEPTION
    arg={'type':'last','status':self.status,'data':self.get_data()}
    self.send_to_listener(**arg)
   except:
    pass
 def log_thread_fuction(self):
  with self.process.stdout:
   for line in X(self.process.stdout.readline,b''):
    try:
     if self.status==Status.READY:
      if line.find('Server returned 404 Not Found')!=-1 or line.find('Unknown error')!=-1:
       self.status=Status.WRONG_URL
       self.start_event.set()
       logger.debug('start_event set by 404 not found')
      elif line.find('No such file or directory')!=-1:
       self.status=Status.WRONG_DIRECTORY
       self.start_event.set()
       logger.debug('start_event set by WRONG_DIR')
      else:
       match=re.compile(r'Duration\:\s(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\,\sstart').search(line)
       if match:
        self.duration_str='%s:%s:%s'%(match.group(1),match.group(2),match.group(3))
        self.duration=b(match.group(4))
        self.duration+=b(match.group(3))*100
        self.duration+=b(match.group(2))*100*60
        self.duration+=b(match.group(1))*100*60*60
        logger.debug('Duration : %s',self.duration)
        if match:
         self.status=Status.READY
         arg={'type':'status_change','status':self.status,'data':self.get_data()}
         self.send_to_listener(**arg)
        continue
       match=re.compile(r'time\=(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\sbitrate\=\s*(?P<bitrate>\d+).*?[$|\s](\s?speed\=\s*(?P<speed>.*?)x)?').search(line)
       if match:
        self.status=Status.DOWNLOADING
        arg={'type':'status_change','status':self.status,'data':self.get_data()}
        self.send_to_listener(**arg)
        self.start_event.set()
        logger.debug('start_event set by DOWNLOADING')
     elif self.status==Status.DOWNLOADING:
      if line.find('PES packet size mismatch')!=-1:
       self.current_pf_count+=1
       if self.current_pf_count>self.max_pf_count:
        logger.debug('%s : PF_STOP!',self.idx)
        self.status=Status.PF_STOP
        self.kill()
       continue
      if line.find('HTTP error 403 Forbidden')!=-1:
       logger.debug('HTTP error 403 Forbidden')
       self.status=Status.HTTP_FORBIDDEN
       self.kill()
       continue
      match=re.compile(r'time\=(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\sbitrate\=\s*(?P<bitrate>\d+).*?[$|\s](\s?speed\=\s*(?P<speed>.*?)x)?').search(line)
      if match:
       self.current_duration=b(match.group(4))
       self.current_duration+=b(match.group(3))*100
       self.current_duration+=b(match.group(2))*100*60
       self.current_duration+=b(match.group(1))*100*60*60
       self.percent=b(self.current_duration*100/self.duration)
       self.current_bitrate=match.group('bitrate')
       self.current_speed=match.group('speed')
       self.download_time=datetime.now()-self.start_time
       arg={'type':'normal','status':self.status,'data':self.get_data()}
       self.send_to_listener(**arg)
       continue
      match=re.compile(r'video\:\d*kB\saudio\:\d*kB').search(line)
      if match:
       self.status=Status.COMPLETED
       self.end_time=datetime.now()
       self.download_time=self.end_time-self.start_time
       self.percent=100
       arg={'type':'status_change','status':self.status,'data':self.get_data()}
       self.send_to_listener(**arg)
       continue
    except D as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc())
  logger.debug('ffmpeg log thread end')
  self.start_event.set()
  self.log_thread=J
 def get_data(self):
  data={'url':self.url,'filename':self.filename,'max_pf_count':self.max_pf_count,'call_plugin':self.call_plugin,'temp_path':self.temp_path,'save_path':self.save_path,'temp_fullpath':self.temp_fullpath,'save_fullpath':self.save_fullpath,'status':b(self.status),'status_str':self.status.name,'status_kor':x(self.status),'duration':self.duration,'duration_str':self.duration_str,'current_duration':self.current_duration,'percent':self.percent,'current_pf_count':self.current_pf_count,'idx':self.idx,'current_bitrate':self.current_bitrate,'current_speed':self.current_speed,'start_time':'' if self.start_time is J else x(self.start_time).split('.')[0][5:],'end_time':'' if self.end_time is J else x(self.end_time).split('.')[0][5:],'download_time':'' if self.download_time is J else '%02d:%02d'%(self.download_time.seconds/60,self.download_time.seconds%60),'exist':os.path.exists(self.save_fullpath),} 
  if self.status==Status.COMPLETED:
   data['filesize']=self.filesize
   data['filesize_str']=Util.sizeof_fmt(self.filesize)
   data['download_speed']=Util.sizeof_fmt(self.filesize/self.download_time.seconds,suffix='Bytes/Second')
  return data
 def send_to_listener(self,**arg):
  Logic.ffmpeg_listener(**arg)
  if self.listener is not J:
   arg['plugin_id']=self.plugin_id
   self.listener(**arg) 
 @Y
 def get_version():
  try:
   command=u'%s -version'%(Logic.path_ffmpeg)
   command=command.split(' ')
   logger.debug(command)
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=q,bufsize=1)
   ret=[]
   with process.stdout:
    for line in X(process.stdout.readline,b''):
     ret.append(line)
    process.wait()
   return ret
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @Y
 def stop_by_idx(idx):
  try:
   for f in Ffmpeg.instance_list:
    if f.idx==idx:
     f.stop()
     break
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @Y
 def ffmpeg_by_idx(idx):
  try:
   for f in Ffmpeg.instance_list:
    if f.idx==idx:
     return f
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @Y
 def get_ffmpeg_by_caller(caller,caller_id):
  try:
   for f in Ffmpeg.instance_list:
    if f.plugin_id==caller_id and f.call_plugin==caller:
     return f
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @Y
 def plugin_unload():
  try:
   for f in Ffmpeg.instance_list:
    f.stop()
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
