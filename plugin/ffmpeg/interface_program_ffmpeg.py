import os
L=object
E=None
O=int
e=str
z=False
U=len
q=Exception
k=True
j=iter
w=staticmethod
C=os.stat
W=os.chmod
i=os.remove
x=os.path
import traceback
T=traceback.format_exc
import threading
n=threading.Thread
N=threading.Event
import subprocess
H=subprocess.STDOUT
s=subprocess.PIPE
h=subprocess.Popen
import platform
p=platform.system
import re
r=re.compile
from datetime import datetime
c=datetime.now
from pytz import timezone
import requests
from framework.logger import get_logger
from framework.util import Util
d=Util.sizeof_fmt
from ffmpeg.logic import Logic,Status
Q=Status.HTTP_FORBIDDEN
X=Status.WRONG_DIRECTORY
f=Status.WRONG_URL
F=Status.EXCEPTION
P=Status.FORCE_STOP
A=Status.TIME_OVER
l=Status.PF_STOP
b=Status.COMPLETED
B=Status.ERROR
R=Status.ALREADY_DOWNLOADING
G=Status.DOWNLOADING
K=Status.USER_STOP
J=Status.READY
v=Logic.ffmpeg_listener
o=Logic.path_ffmpeg
from ffmpeg.model import ModelSetting 
V=ModelSetting.get_int
t=ModelSetting.get
a=ModelSetting.query
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Ffmpeg(L):
 instance_list=[]
 idx=1
 def __init__(self,url,filename,plugin_id=E,listener=E,max_pf_count=E,call_plugin=E,temp_path=E,save_path=E,proxy=E,headers=E):
  self.thread=E
  self.url=url
  self.filename=filename
  self.plugin_id=plugin_id
  self.listener=listener
  self.max_pf_count=O(a.filter_by(key='max_pf_count').first().value if max_pf_count is E else max_pf_count)
  self.call_plugin=call_plugin
  self.process=E
  self.temp_path=a.filter_by(key='temp_path').first().value if temp_path is E else temp_path
  self.save_path=a.filter_by(key='save_path').first().value if save_path is E else save_path
  self.proxy=proxy
  self.temp_fullpath=x.join(self.temp_path,filename)
  self.save_fullpath=x.join(self.save_path,filename)
  self.log_thread=E
  self.status=J
  self.duration=0
  self.duration_str=''
  self.current_duration=0
  self.percent=0
  self.current_pf_count=0
  self.idx=e(Ffmpeg.idx)
  Ffmpeg.idx+=1
  self.current_bitrate=''
  self.current_speed=''
  self.start_time=E
  self.end_time=E
  self.download_time=E
  self.start_event=N()
  self.exist=z
  self.filesize=0
  self.filesize_str=''
  self.download_speed=''
  self.headers=headers
  Ffmpeg.instance_list.append(self)
  logger.debug('Ffmpeg.instance_list LEN:%s',U(Ffmpeg.instance_list))
  if U(Ffmpeg.instance_list)>30:
   for f in Ffmpeg.instance_list:
    if f.thread is E and f.status!=J:
     Ffmpeg.instance_list.remove(f)
     break
    else:
     logger.debug('remove fail %s %s',f.thread,self.status)
 def start(self):
  self.thread=n(target=self.thread_fuction,args=())
  self.thread.start()
  self.start_time=c()
  return self.get_data()
 def start_and_wait(self):
  self.start()
  self.thread.join(timeout=60*70)
 def stop(self):
  try:
   self.status=K
   self.kill()
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
 def kill(self):
  try:
   if self.process is not E and self.process.poll()is E:
    import psutil
    process=psutil.Process(self.process.pid)
    for proc in process.children(recursive=k):
     proc.kill()
    process.kill()
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
 def thread_fuction(self):
  try:
   import system
   user=e(system.t('sjva_me_user_id'))
   try:
    from framework.common.util import AESCipher
    user=AESCipher.encrypt(user)
   except q as e:
    logger.error('Exception:%s',e)
    logger.error(T())
   if self.proxy is E:
    if self.headers is E:
     command=[o,'-y','-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
    else:
     headers_command=[]
     for key,value in self.headers.items():
      if key.lower()=='user-agent':
       headers_command.append('-user_agent')
       headers_command.append('value')
      else:
       headers_command.append('-headers')
       headers_command.append('\'%s: "%s"\''%(key,value))
     command=[o,'-y']+headers_command+['-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
   else:
    command=[o,'-y','-http_proxy',self.proxy,'-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
   if p()=='Windows':
    now=e(c()).replace(':','').replace('-','').replace(' ','-')
    filename=('%s'%now)+'.mp4'
    self.temp_fullpath=x.join(self.temp_path,filename)
    command.append(self.temp_fullpath)
   else:
    command.append(self.temp_fullpath)
   try:
    logger.debug(' '.join(command))
    if x.exists(self.temp_fullpath):
     for f in Ffmpeg.instance_list:
      if f.idx!=self.idx and f.temp_fullpath==self.temp_fullpath and f.status in[G,J]:
       self.status=R
       logger.debug('temp_fullpath ALREADY_DOWNLOADING')
       return
   except:
    pass
   self.process=h(command,stdout=s,stderr=H,universal_newlines=k,bufsize=1)
   self.status=J
   self.log_thread=n(target=self.log_thread_fuction,args=())
   self.log_thread.start()
   self.start_event.wait(timeout=60)
   logger.debug('start_event awake.. ')
   if self.log_thread is E:
    logger.debug('log_thread is none')
    if self.status==J:
     self.status=B
    self.kill()
   elif self.status==J:
    logger.debug('still status.ready kill')
    self.status=B
    self.kill()
   else:
    logger.debug('normally process wait()')
    process_ret=self.process.wait(timeout=60*V('timeout_minute'))
    logger.debug('process_ret :%s'%process_ret)
    if process_ret is E:
     if self.status!=b and self.status!=K and self.status!=l:
      self.status=A
      self.kill()
    else:
     logger.debug('process end')
     if self.status==G:
      self.status=P
   self.end_time=c()
   self.download_time=self.end_time-self.start_time
   try:
    if self.status==b:
     if self.save_fullpath!=self.temp_fullpath:
      if x.exists(self.save_fullpath):
       i(self.save_fullpath)
      W(self.temp_fullpath,777)
      import shutil
      shutil.move(self.temp_fullpath,self.save_fullpath)
      self.filesize=C(self.save_fullpath).st_size
    else:
     if x.exists(self.temp_fullpath):
      i(self.temp_fullpath)
   except q as e:
    logger.error('Exception:%s',e)
    logger.error(T())
   arg={'type':'last','status':self.status,'data':self.get_data()}
   self.send_to_listener(**arg)
   self.process=E
   self.thread=E
   logger.debug('ffmpeg thread end')
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
   try:
    self.status=F
    arg={'type':'last','status':self.status,'data':self.get_data()}
    self.send_to_listener(**arg)
   except:
    pass
 def log_thread_fuction(self):
  with self.process.stdout:
   for line in j(self.process.stdout.readline,b''):
    try:
     if self.status==J:
      if line.find('Server returned 404 Not Found')!=-1 or line.find('Unknown error')!=-1:
       self.status=f
       self.start_event.set()
       logger.debug('start_event set by 404 not found')
      elif line.find('No such file or directory')!=-1:
       self.status=X
       self.start_event.set()
       logger.debug('start_event set by WRONG_DIR')
      else:
       match=r(r'Duration\:\s(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\,\sstart').search(line)
       if match:
        self.duration_str='%s:%s:%s'%(match.group(1),match.group(2),match.group(3))
        self.duration=O(match.group(4))
        self.duration+=O(match.group(3))*100
        self.duration+=O(match.group(2))*100*60
        self.duration+=O(match.group(1))*100*60*60
        logger.debug('Duration : %s',self.duration)
        if match:
         self.status=J
         arg={'type':'status_change','status':self.status,'data':self.get_data()}
         self.send_to_listener(**arg)
        continue
       match=r(r'time\=(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\sbitrate\=\s*(?P<bitrate>\d+).*?[$|\s](\s?speed\=\s*(?P<speed>.*?)x)?').search(line)
       if match:
        self.status=G
        arg={'type':'status_change','status':self.status,'data':self.get_data()}
        self.send_to_listener(**arg)
        self.start_event.set()
        logger.debug('start_event set by DOWNLOADING')
     elif self.status==G:
      if line.find('PES packet size mismatch')!=-1:
       self.current_pf_count+=1
       if self.current_pf_count>self.max_pf_count:
        logger.debug('%s : PF_STOP!',self.idx)
        self.status=l
        self.kill()
       continue
      if line.find('HTTP error 403 Forbidden')!=-1:
       logger.debug('HTTP error 403 Forbidden')
       self.status=Q
       self.kill()
       continue
      match=r(r'time\=(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\sbitrate\=\s*(?P<bitrate>\d+).*?[$|\s](\s?speed\=\s*(?P<speed>.*?)x)?').search(line)
      if match:
       self.current_duration=O(match.group(4))
       self.current_duration+=O(match.group(3))*100
       self.current_duration+=O(match.group(2))*100*60
       self.current_duration+=O(match.group(1))*100*60*60
       self.percent=O(self.current_duration*100/self.duration)
       self.current_bitrate=match.group('bitrate')
       self.current_speed=match.group('speed')
       self.download_time=c()-self.start_time
       arg={'type':'normal','status':self.status,'data':self.get_data()}
       self.send_to_listener(**arg)
       continue
      match=r(r'video\:\d*kB\saudio\:\d*kB').search(line)
      if match:
       self.status=b
       self.end_time=c()
       self.download_time=self.end_time-self.start_time
       self.percent=100
       arg={'type':'status_change','status':self.status,'data':self.get_data()}
       self.send_to_listener(**arg)
       continue
    except q as e:
     logger.error('Exception:%s',e)
     logger.error(T())
  logger.debug('ffmpeg log thread end')
  self.start_event.set()
  self.log_thread=E
 def get_data(self):
  data={'url':self.url,'filename':self.filename,'max_pf_count':self.max_pf_count,'call_plugin':self.call_plugin,'temp_path':self.temp_path,'save_path':self.save_path,'temp_fullpath':self.temp_fullpath,'save_fullpath':self.save_fullpath,'status':O(self.status),'status_str':self.status.name,'status_kor':e(self.status),'duration':self.duration,'duration_str':self.duration_str,'current_duration':self.current_duration,'percent':self.percent,'current_pf_count':self.current_pf_count,'idx':self.idx,'current_bitrate':self.current_bitrate,'current_speed':self.current_speed,'start_time':'' if self.start_time is E else e(self.start_time).split('.')[0][5:],'end_time':'' if self.end_time is E else e(self.end_time).split('.')[0][5:],'download_time':'' if self.download_time is E else '%02d:%02d'%(self.download_time.seconds/60,self.download_time.seconds%60),'exist':x.exists(self.save_fullpath),} 
  if self.status==b:
   data['filesize']=self.filesize
   data['filesize_str']=d(self.filesize)
   data['download_speed']=d(self.filesize/self.download_time.seconds,suffix='Bytes/Second')
  return data
 def send_to_listener(self,**arg):
  v(**arg)
  if self.listener is not E:
   arg['plugin_id']=self.plugin_id
   self.listener(**arg) 
 @w
 def get_version():
  try:
   command=u'%s -version'%(o)
   command=command.split(' ')
   logger.debug(command)
   process=h(command,stdout=s,stderr=H,universal_newlines=k,bufsize=1)
   ret=[]
   with process.stdout:
    for line in j(process.stdout.readline,b''):
     ret.append(line)
    process.wait()
   return ret
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
 @w
 def stop_by_idx(idx):
  try:
   for f in Ffmpeg.instance_list:
    if f.idx==idx:
     f.stop()
     break
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
 @w
 def ffmpeg_by_idx(idx):
  try:
   for f in Ffmpeg.instance_list:
    if f.idx==idx:
     return f
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
 @w
 def get_ffmpeg_by_caller(caller,caller_id):
  try:
   for f in Ffmpeg.instance_list:
    if f.plugin_id==caller_id and f.call_plugin==caller:
     return f
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
 @w
 def plugin_unload():
  try:
   for f in Ffmpeg.instance_list:
    f.stop()
  except q as e:
   logger.error('Exception:%s',e)
   logger.error(T())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
