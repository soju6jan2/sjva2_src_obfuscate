import os,sys,traceback
B=object
v=None
z=False
D=classmethod
I=True
V=Exception
h=int
n=str
u=traceback.format_exc
K=os.makedirs
m=os.path
import threading,time
T=time.sleep
F=threading.Thread
from datetime import datetime
f=datetime.now
import abc
N=abc.abstractmethod
b=abc.ABCMeta
from framework import py_queue
O=py_queue.Queue
class FfmpegQueueEntity(b('ABC',(B,),{'__slots__':()})):
 static_index=1
 entity_list=[]
 def __init__(self,P,module_logic,info):
  self.P=P
  self.module_logic=module_logic
  self.entity_id=FfmpegQueueEntity.static_index
  self.info=info
  self.url=v
  self.ffmpeg_status=-1
  self.ffmpeg_status_kor=u'대기중'
  self.ffmpeg_percent=0
  self.ffmpeg_arg=v
  self.cancel=z
  self.created_time=f().strftime('%m-%d %H:%M:%S')
  self.savepath=v
  self.filename=v
  self.filepath=v
  self.quality=v
  self.headers=v
  FfmpegQueueEntity.static_index+=1
  FfmpegQueueEntity.entity_list.append(self)
 @D
 def get_entity_by_entity_id(cls,entity_id):
  for _ in cls.entity_list:
   if _.entity_id==entity_id:
    return _
  return v
 def get_video_url(self):
  return self.url
 def get_video_filepath(self):
  return self.filepath
 @N
 def refresh_status(self):
  pass
 @N
 def info_dict(self,tmp):
  pass
 def donwload_completed(self):
  pass
 def as_dict(self):
  tmp={}
  tmp['entity_id']=self.entity_id
  tmp['url']=self.url
  tmp['ffmpeg_status']=self.ffmpeg_status
  tmp['ffmpeg_status_kor']=self.ffmpeg_status_kor
  tmp['ffmpeg_percent']=self.ffmpeg_percent
  tmp['ffmpeg_arg']=self.ffmpeg_arg
  tmp['cancel']=self.cancel
  tmp['created_time']=self.created_time
  tmp['savepath']=self.savepath
  tmp['filename']=self.filename
  tmp['filepath']=self.filepath
  tmp['quality']=self.quality
  tmp=self.info_dict(tmp)
  return tmp
 @D
 def get_entity_list(cls):
  ret=[]
  for x in cls.entity_list:
   tmp=x.as_dict()
   ret.append(tmp)
  return ret
class FfmpegQueue(B):
 download_queue=v
 download_thread=v
 current_ffmpeg_count=0
 max_ffmpeg_count=1
 P=v
 def __init__(self,P,max_ffmpeg_count):
  self.P=P
  self.max_ffmpeg_count=max_ffmpeg_count
 def queue_start(self):
  try:
   if self.download_queue is v:
    self.download_queue=O()
   if self.download_thread is v:
    self.download_thread=F(target=self.download_thread_function,args=())
    self.download_thread.daemon=I 
    self.download_thread.start()
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
 def download_thread_function(self):
  while I:
   try:
    while I:
     if self.current_ffmpeg_count<self.max_ffmpeg_count:
      break
     T(5)
    entity=self.download_queue.get()
    if entity.cancel:
     continue
    video_url=entity.get_video_url()
    if video_url is v:
     entity.ffmpeg_status_kor='URL실패'
     entity.refresh_status()
     continue
    import ffmpeg
    filepath=entity.get_video_filepath()
    if m.exists(filepath):
     entity.ffmpeg_status_kor='파일 있음'
     entity.ffmpeg_percent=100
     entity.refresh_status()
     continue
    dirname=m.dirname(filepath)
    if not m.exists(dirname):
     K(dirname)
    f=ffmpeg.Ffmpeg(video_url,m.basename(filepath),plugin_id=entity.entity_id,listener=self.ffmpeg_listener,call_plugin=self.P.package_name,save_path=dirname,headers=entity.headers)
    f.start()
    self.current_ffmpeg_count+=1
    self.download_queue.task_done() 
   except V as e:
    self.P.logger.error('Exception:%s',e)
    self.P.logger.error(u())
 def ffmpeg_listener(self,**arg):
  import ffmpeg
  entity=FfmpegQueueEntity.get_entity_by_entity_id(arg['plugin_id'])
  if entity is v:
   return
  if arg['type']=='status_change':
   if arg['status']==ffmpeg.Status.DOWNLOADING:
    pass
   elif arg['status']==ffmpeg.Status.COMPLETED:
    entity.donwload_completed()
   elif arg['status']==ffmpeg.Status.READY:
    pass
  elif arg['type']=='last':
   self.current_ffmpeg_count+=-1
  elif arg['type']=='log':
   pass
  elif arg['type']=='normal':
   pass
  entity.ffmpeg_arg=arg
  entity.ffmpeg_status=h(arg['status'])
  entity.ffmpeg_status_kor=n(arg['status'])
  entity.ffmpeg_percent=arg['data']['percent']
  entity.ffmpeg_arg['status']= n(arg['status'])
  entity.refresh_status()
 def add_queue(self,entity):
  try:
   self.download_queue.put(entity)
   return I
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
  return z
 def set_max_ffmpeg_count(self,max_ffmpeg_count):
  self.max_ffmpeg_count=max_ffmpeg_count
 def get_max_ffmpeg_count(self):
  return self.max_ffmpeg_count
 def command(self,cmd,entity_id):
  self.P.logger.debug('command :%s %s',cmd,entity_id)
  ret={}
  try:
   if cmd=='cancel':
    self.P.logger.debug('command :%s %s',cmd,entity_id)
    entity=FfmpegQueueEntity.get_entity_by_entity_id(entity_id)
    if entity is not v:
     if entity.ffmpeg_status==-1:
      entity.cancel=I
      entity.ffmpeg_status_kor="취소"
      ret['ret']='refresh'
     elif entity.ffmpeg_status!=5:
      ret['ret']='notify'
      ret['log']='다운로드중 상태가 아닙니다.'
     else:
      idx=entity.ffmpeg_arg['data']['idx']
      import ffmpeg
      ffmpeg.Ffmpeg.stop_by_idx(idx)
      entity.refresh_status()
      ret['ret']='refresh'
   elif cmd=='reset':
    if self.download_queue is not v:
     with self.download_queue.mutex:
      self.download_queue.queue.clear()
     for _ in FfmpegQueueEntity.entity_list:
      if _.ffmpeg_status==5:
       import ffmpeg
       idx=_.ffmpeg_arg['data']['idx']
       ffmpeg.Ffmpeg.stop_by_idx(idx)
    FfmpegQueueEntity.entity_list=[]
    ret['ret']='refresh'
   elif cmd=='delete_completed':
    new_list=[]
    for _ in FfmpegQueueEntity.entity_list:
     if _.ffmpeg_status_kor in[u'파일 있음',u'취소',u'사용자중지']:
      continue
     if _.ffmpeg_status!=7:
      new_list.append(_)
    FfmpegQueueEntity.entity_list=new_list
    ret['ret']='refresh'
   return ret
  except V as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(u())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
