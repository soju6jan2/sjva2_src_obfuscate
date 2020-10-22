import os,sys,traceback
o=object
J=None
g=False
m=classmethod
S=True
G=Exception
B=int
j=str
import threading,time
from datetime import datetime
import abc
from framework import py_queue
class FfmpegQueueEntity(abc.ABCMeta('ABC',(o,),{'__slots__':()})):
 static_index=1
 entity_list=[]
 def __init__(self,P,module_logic,info):
  self.P=P
  self.module_logic=module_logic
  self.entity_id=FfmpegQueueEntity.static_index
  self.info=info
  self.url=J
  self.ffmpeg_status=-1
  self.ffmpeg_status_kor=u'대기중'
  self.ffmpeg_percent=0
  self.ffmpeg_arg=J
  self.cancel=g
  self.created_time=datetime.now().strftime('%m-%d %H:%M:%S')
  self.savepath=J
  self.filename=J
  self.filepath=J
  self.quality=J
  self.headers=J
  FfmpegQueueEntity.static_index+=1
  FfmpegQueueEntity.entity_list.append(self)
 @m
 def get_entity_by_entity_id(cls,entity_id):
  for _ in cls.entity_list:
   if _.entity_id==entity_id:
    return _
  return J
 def get_video_url(self):
  return self.url
 def get_video_filepath(self):
  return self.filepath
 @abc.abstractmethod
 def refresh_status(self):
  pass
 @abc.abstractmethod
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
class FfmpegQueue(o):
 download_queue=J
 download_thread=J
 current_ffmpeg_count=0
 max_ffmpeg_count=1
 P=J
 def __init__(self,P,max_ffmpeg_count):
  self.P=P
  self.max_ffmpeg_count=max_ffmpeg_count
 def queue_start(self):
  try:
   if self.download_queue is J:
    self.download_queue=py_queue.Queue()
   if self.download_thread is J:
    self.download_thread=threading.Thread(target=self.download_thread_function,args=())
    self.download_thread.daemon=S 
    self.download_thread.start()
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
 def download_thread_function(self):
  while S:
   try:
    while S:
     if self.current_ffmpeg_count<self.max_ffmpeg_count:
      break
     time.sleep(5)
    entity=self.download_queue.get()
    if entity.cancel:
     continue
    video_url=entity.get_video_url()
    if video_url is J:
     entity.ffmpeg_status_kor='URL실패'
     entity.refresh_status()
     continue
    import ffmpeg
    filepath=entity.get_video_filepath()
    if os.path.exists(filepath):
     entity.ffmpeg_status_kor='파일 있음'
     entity.ffmpeg_percent=100
     entity.refresh_status()
     continue
    dirname=os.path.dirname(filepath)
    if not os.path.exists(dirname):
     os.makedirs(dirname)
    f=ffmpeg.Ffmpeg(video_url,os.path.basename(filepath),plugin_id=entity.entity_id,listener=self.ffmpeg_listener,call_plugin=self.P.package_name,save_path=dirname,headers=entity.headers)
    f.start()
    self.current_ffmpeg_count+=1
    self.download_queue.task_done() 
   except G as e:
    self.P.logger.error('Exception:%s',e)
    self.P.logger.error(traceback.format_exc())
 def ffmpeg_listener(self,**arg):
  import ffmpeg
  entity=FfmpegQueueEntity.get_entity_by_entity_id(arg['plugin_id'])
  if entity is J:
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
  entity.ffmpeg_status=B(arg['status'])
  entity.ffmpeg_status_kor=j(arg['status'])
  entity.ffmpeg_percent=arg['data']['percent']
  entity.ffmpeg_arg['status']= j(arg['status'])
  entity.refresh_status()
 def add_queue(self,entity):
  try:
   self.download_queue.put(entity)
   return S
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
  return g
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
    if entity is not J:
     if entity.ffmpeg_status==-1:
      entity.cancel=S
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
    if self.download_queue is not J:
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
  except G as e:
   self.P.logger.error('Exception:%s',e)
   self.P.logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
