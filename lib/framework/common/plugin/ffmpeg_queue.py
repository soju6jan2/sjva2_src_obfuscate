import os,sys,traceback
K=object
Q=None
s=False
m=classmethod
x=True
U=Exception
t=int
A=str
I=traceback.format_exc
v=os.makedirs
z=os.path
import threading,time
O=time.sleep
a=threading.Thread
from datetime import datetime
u=datetime.now
import abc
D=abc.abstractmethod
d=abc.ABCMeta
from framework import py_queue
q=py_queue.Queue
class FfmpegQueueEntity(d('ABC',(K,),{'__slots__':()})):
 static_index=1
 entity_list=[]
 def __init__(self,P,module_logic,info):
  self.P=P
  self.module_logic=module_logic
  self.entity_id=FfmpegQueueEntity.static_index
  self.info=info
  self.url=Q
  self.ffmpeg_status=-1
  self.ffmpeg_status_kor=u'대기중'
  self.ffmpeg_percent=0
  self.ffmpeg_arg=Q
  self.cancel=s
  self.created_time=u().strftime('%m-%d %H:%M:%S')
  self.savepath=Q
  self.filename=Q
  self.filepath=Q
  self.quality=Q
  self.headers=Q
  FfmpegQueueEntity.static_index+=1
  FfmpegQueueEntity.entity_list.append(self)
 @m
 def get_entity_by_entity_id(cls,entity_id):
  for _ in cls.entity_list:
   if _.entity_id==entity_id:
    return _
  return Q
 def get_video_url(self):
  return self.url
 def get_video_filepath(self):
  return self.filepath
 @D
 def refresh_status(self):
  pass
 @D
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
 @m
 def get_entity_list(cls):
  ret=[]
  for x in cls.entity_list:
   tmp=x.as_dict()
   ret.append(tmp)
  return ret
class FfmpegQueue(K):
 download_queue=Q
 download_thread=Q
 current_ffmpeg_count=0
 max_ffmpeg_count=1
 P=Q
 def __init__(self,P,max_ffmpeg_count):
  self.P=P
  self.max_ffmpeg_count=max_ffmpeg_count
 def queue_start(self):
  try:
   if self.download_queue is Q:
    self.download_queue=q()
   if self.download_thread is Q:
    self.download_thread=a(target=self.download_thread_function,args=())
    self.download_thread.daemon=x 
    self.download_thread.start()
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
 def download_thread_function(self):
  while x:
   try:
    while x:
     if self.current_ffmpeg_count<self.max_ffmpeg_count:
      break
     O(5)
    entity=self.download_queue.get()
    if entity.cancel:
     continue
    video_url=entity.get_video_url()
    if video_url is Q:
     entity.ffmpeg_status_kor='URL실패'
     entity.refresh_status()
     continue
    import ffmpeg
    filepath=entity.get_video_filepath()
    if z.exists(filepath):
     entity.ffmpeg_status_kor='파일 있음'
     entity.ffmpeg_percent=100
     entity.refresh_status()
     continue
    dirname=z.dirname(filepath)
    if not z.exists(dirname):
     v(dirname)
    f=ffmpeg.Ffmpeg(video_url,z.basename(filepath),plugin_id=entity.entity_id,listener=self.ffmpeg_listener,call_plugin=self.P.package_name,save_path=dirname,headers=entity.headers)
    f.start()
    self.current_ffmpeg_count+=1
    self.download_queue.task_done() 
   except U as e:
    self.P.logger.error('Exception:%s',e)
    self.P.logger.error(I())
 def ffmpeg_listener(self,**arg):
  import ffmpeg
  entity=FfmpegQueueEntity.get_entity_by_entity_id(arg['plugin_id'])
  if entity is Q:
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
  entity.ffmpeg_status=t(arg['status'])
  entity.ffmpeg_status_kor=A(arg['status'])
  entity.ffmpeg_percent=arg['data']['percent']
  entity.ffmpeg_arg['status']= A(arg['status'])
  entity.refresh_status()
 def add_queue(self,entity):
  try:
   self.download_queue.put(entity)
   return x
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
  return s
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
    if entity is not Q:
     if entity.ffmpeg_status==-1:
      entity.cancel=x
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
    if self.download_queue is not Q:
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
  except U as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(I())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
