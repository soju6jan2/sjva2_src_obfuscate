import os
C=object
A=None
y=int
u=str
H=False
O=len
f=Exception
t=True
q=iter
j=staticmethod
T=os.stat
p=os.chmod
I=os.remove
P=os.path
import traceback
N=traceback.format_exc
import threading
U=threading.Thread
B=threading.Event
import subprocess
L=subprocess.STDOUT
h=subprocess.PIPE
G=subprocess.Popen
import platform
S=platform.system
import re
o=re.compile
from datetime import datetime
r=datetime.now
from pytz import timezone
import requests
from framework.logger import get_logger
from framework.util import Util
w=Util.sizeof_fmt
from ffmpeg.logic import Logic,Status
X=Status.HTTP_FORBIDDEN
R=Status.WRONG_DIRECTORY
s=Status.WRONG_URL
b=Status.EXCEPTION
l=Status.FORCE_STOP
k=Status.TIME_OVER
M=Status.PF_STOP
J=Status.COMPLETED
D=Status.ERROR
a=Status.ALREADY_DOWNLOADING
n=Status.DOWNLOADING
m=Status.USER_STOP
Y=Status.READY
d=Logic.ffmpeg_listener
W=Logic.path_ffmpeg
from ffmpeg.model import ModelSetting 
E=ModelSetting.get_int
K=ModelSetting.get
z=ModelSetting.query
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Ffmpeg(C):
 instance_list=[]
 idx=1
 def __init__(self,url,filename,plugin_id=A,listener=A,max_pf_count=A,call_plugin=A,temp_path=A,save_path=A,proxy=A,headers=A):
  self.thread=A
  self.url=url
  self.filename=filename
  self.plugin_id=plugin_id
  self.listener=listener
  self.max_pf_count=y(z.filter_by(key='max_pf_count').first().value if max_pf_count is A else max_pf_count)
  self.call_plugin=call_plugin
  self.process=A
  self.temp_path=z.filter_by(key='temp_path').first().value if temp_path is A else temp_path
  self.save_path=z.filter_by(key='save_path').first().value if save_path is A else save_path
  self.proxy=proxy
  self.temp_fullpath=P.join(self.temp_path,filename)
  self.save_fullpath=P.join(self.save_path,filename)
  self.log_thread=A
  self.status=Y
  self.duration=0
  self.duration_str=''
  self.current_duration=0
  self.percent=0
  self.current_pf_count=0
  self.idx=u(Ffmpeg.idx)
  Ffmpeg.idx+=1
  self.current_bitrate=''
  self.current_speed=''
  self.start_time=A
  self.end_time=A
  self.download_time=A
  self.start_event=B()
  self.exist=H
  self.filesize=0
  self.filesize_str=''
  self.download_speed=''
  self.headers=headers
  Ffmpeg.instance_list.append(self)
  logger.debug('Ffmpeg.instance_list LEN:%s',O(Ffmpeg.instance_list))
  if O(Ffmpeg.instance_list)>30:
   for f in Ffmpeg.instance_list:
    if f.thread is A and f.status!=Y:
     Ffmpeg.instance_list.remove(f)
     break
    else:
     logger.debug('remove fail %s %s',f.thread,self.status)
 def start(self):
  self.thread=U(target=self.thread_fuction,args=())
  self.thread.start()
  self.start_time=r()
  return self.get_data()
 def start_and_wait(self):
  self.start()
  self.thread.join(timeout=60*70)
 def stop(self):
  try:
   self.status=m
   self.kill()
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
 def kill(self):
  try:
   if self.process is not A and self.process.poll()is A:
    import psutil
    process=psutil.Process(self.process.pid)
    for proc in process.children(recursive=t):
     proc.kill()
    process.kill()
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
 def thread_fuction(self):
  try:
   import system
   user=u(system.K('sjva_me_user_id'))
   try:
    from framework.common.util import AESCipher
    user=AESCipher.encrypt(user)
   except f as e:
    logger.error('Exception:%s',e)
    logger.error(N())
   if self.proxy is A:
    if self.headers is A:
     command=[W,'-y','-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
    else:
     headers_command=[]
     for key,value in self.headers.items():
      if key.lower()=='user-agent':
       headers_command.append('-user_agent')
       headers_command.append('value')
      else:
       headers_command.append('-headers')
       headers_command.append('\'%s: "%s"\''%(key,value))
     command=[W,'-y']+headers_command+['-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
   else:
    command=[W,'-y','-http_proxy',self.proxy,'-i',self.url,'-c','copy','-bsf:a','aac_adtstoasc','-metadata','network=%s'%user]
   if S()=='Windows':
    now=u(r()).replace(':','').replace('-','').replace(' ','-')
    filename=('%s'%now)+'.mp4'
    self.temp_fullpath=P.join(self.temp_path,filename)
    command.append(self.temp_fullpath)
   else:
    command.append(self.temp_fullpath)
   try:
    logger.debug(' '.join(command))
    if P.exists(self.temp_fullpath):
     for f in Ffmpeg.instance_list:
      if f.idx!=self.idx and f.temp_fullpath==self.temp_fullpath and f.status in[n,Y]:
       self.status=a
       logger.debug('temp_fullpath ALREADY_DOWNLOADING')
       return
   except:
    pass
   self.process=G(command,stdout=h,stderr=L,universal_newlines=t,bufsize=1)
   self.status=Y
   self.log_thread=U(target=self.log_thread_fuction,args=())
   self.log_thread.start()
   self.start_event.wait(timeout=60)
   logger.debug('start_event awake.. ')
   if self.log_thread is A:
    logger.debug('log_thread is none')
    if self.status==Y:
     self.status=D
    self.kill()
   elif self.status==Y:
    logger.debug('still status.ready kill')
    self.status=D
    self.kill()
   else:
    logger.debug('normally process wait()')
    process_ret=self.process.wait(timeout=60*E('timeout_minute'))
    logger.debug('process_ret :%s'%process_ret)
    if process_ret is A:
     if self.status!=J and self.status!=m and self.status!=M:
      self.status=k
      self.kill()
    else:
     logger.debug('process end')
     if self.status==n:
      self.status=l
   self.end_time=r()
   self.download_time=self.end_time-self.start_time
   try:
    if self.status==J:
     if self.save_fullpath!=self.temp_fullpath:
      if P.exists(self.save_fullpath):
       I(self.save_fullpath)
      p(self.temp_fullpath,777)
      import shutil
      shutil.move(self.temp_fullpath,self.save_fullpath)
      self.filesize=T(self.save_fullpath).st_size
    else:
     if P.exists(self.temp_fullpath):
      I(self.temp_fullpath)
   except f as e:
    logger.error('Exception:%s',e)
    logger.error(N())
   arg={'type':'last','status':self.status,'data':self.get_data()}
   self.send_to_listener(**arg)
   self.process=A
   self.thread=A
   logger.debug('ffmpeg thread end')
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
   try:
    self.status=b
    arg={'type':'last','status':self.status,'data':self.get_data()}
    self.send_to_listener(**arg)
   except:
    pass
 def log_thread_fuction(self):
  with self.process.stdout:
   for line in q(self.process.stdout.readline,b''):
    try:
     if self.status==Y:
      if line.find('Server returned 404 Not Found')!=-1 or line.find('Unknown error')!=-1:
       self.status=s
       self.start_event.set()
       logger.debug('start_event set by 404 not found')
      elif line.find('No such file or directory')!=-1:
       self.status=R
       self.start_event.set()
       logger.debug('start_event set by WRONG_DIR')
      else:
       match=o(r'Duration\:\s(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\,\sstart').search(line)
       if match:
        self.duration_str='%s:%s:%s'%(match.group(1),match.group(2),match.group(3))
        self.duration=y(match.group(4))
        self.duration+=y(match.group(3))*100
        self.duration+=y(match.group(2))*100*60
        self.duration+=y(match.group(1))*100*60*60
        logger.debug('Duration : %s',self.duration)
        if match:
         self.status=Y
         arg={'type':'status_change','status':self.status,'data':self.get_data()}
         self.send_to_listener(**arg)
        continue
       match=o(r'time\=(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\sbitrate\=\s*(?P<bitrate>\d+).*?[$|\s](\s?speed\=\s*(?P<speed>.*?)x)?').search(line)
       if match:
        self.status=n
        arg={'type':'status_change','status':self.status,'data':self.get_data()}
        self.send_to_listener(**arg)
        self.start_event.set()
        logger.debug('start_event set by DOWNLOADING')
     elif self.status==n:
      if line.find('PES packet size mismatch')!=-1:
       self.current_pf_count+=1
       if self.current_pf_count>self.max_pf_count:
        logger.debug('%s : PF_STOP!',self.idx)
        self.status=M
        self.kill()
       continue
      if line.find('HTTP error 403 Forbidden')!=-1:
       logger.debug('HTTP error 403 Forbidden')
       self.status=X
       self.kill()
       continue
      match=o(r'time\=(\d{2})\:(\d{2})\:(\d{2})\.(\d{2})\sbitrate\=\s*(?P<bitrate>\d+).*?[$|\s](\s?speed\=\s*(?P<speed>.*?)x)?').search(line)
      if match:
       self.current_duration=y(match.group(4))
       self.current_duration+=y(match.group(3))*100
       self.current_duration+=y(match.group(2))*100*60
       self.current_duration+=y(match.group(1))*100*60*60
       self.percent=y(self.current_duration*100/self.duration)
       self.current_bitrate=match.group('bitrate')
       self.current_speed=match.group('speed')
       self.download_time=r()-self.start_time
       arg={'type':'normal','status':self.status,'data':self.get_data()}
       self.send_to_listener(**arg)
       continue
      match=o(r'video\:\d*kB\saudio\:\d*kB').search(line)
      if match:
       self.status=J
       self.end_time=r()
       self.download_time=self.end_time-self.start_time
       self.percent=100
       arg={'type':'status_change','status':self.status,'data':self.get_data()}
       self.send_to_listener(**arg)
       continue
    except f as e:
     logger.error('Exception:%s',e)
     logger.error(N())
  logger.debug('ffmpeg log thread end')
  self.start_event.set()
  self.log_thread=A
 def get_data(self):
  data={'url':self.url,'filename':self.filename,'max_pf_count':self.max_pf_count,'call_plugin':self.call_plugin,'temp_path':self.temp_path,'save_path':self.save_path,'temp_fullpath':self.temp_fullpath,'save_fullpath':self.save_fullpath,'status':y(self.status),'status_str':self.status.name,'status_kor':u(self.status),'duration':self.duration,'duration_str':self.duration_str,'current_duration':self.current_duration,'percent':self.percent,'current_pf_count':self.current_pf_count,'idx':self.idx,'current_bitrate':self.current_bitrate,'current_speed':self.current_speed,'start_time':'' if self.start_time is A else u(self.start_time).split('.')[0][5:],'end_time':'' if self.end_time is A else u(self.end_time).split('.')[0][5:],'download_time':'' if self.download_time is A else '%02d:%02d'%(self.download_time.seconds/60,self.download_time.seconds%60),'exist':P.exists(self.save_fullpath),} 
  if self.status==J:
   data['filesize']=self.filesize
   data['filesize_str']=w(self.filesize)
   data['download_speed']=w(self.filesize/self.download_time.seconds,suffix='Bytes/Second')
  return data
 def send_to_listener(self,**arg):
  d(**arg)
  if self.listener is not A:
   arg['plugin_id']=self.plugin_id
   self.listener(**arg) 
 @j
 def get_version():
  try:
   command=u'%s -version'%(W)
   command=command.split(' ')
   logger.debug(command)
   process=G(command,stdout=h,stderr=L,universal_newlines=t,bufsize=1)
   ret=[]
   with process.stdout:
    for line in q(process.stdout.readline,b''):
     ret.append(line)
    process.wait()
   return ret
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
 @j
 def stop_by_idx(idx):
  try:
   for f in Ffmpeg.instance_list:
    if f.idx==idx:
     f.stop()
     break
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
 @j
 def ffmpeg_by_idx(idx):
  try:
   for f in Ffmpeg.instance_list:
    if f.idx==idx:
     return f
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
 @j
 def get_ffmpeg_by_caller(caller,caller_id):
  try:
   for f in Ffmpeg.instance_list:
    if f.plugin_id==caller_id and f.call_plugin==caller:
     return f
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
 @j
 def plugin_unload():
  try:
   for f in Ffmpeg.instance_list:
    f.stop()
  except f as e:
   logger.error('Exception:%s',e)
   logger.error(N())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
