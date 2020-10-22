import os
J=object
C=staticmethod
i=Exception
K=None
V=OSError
f=len
X=True
S=False
w=os.mkdir
W=os.makedirs
F=os.rmdir
t=os.remove
e=os.listdir
o=os.path
import sys
import traceback
B=traceback.format_exc
import logging
import threading
import re
T=re.compile
j=re.sub
import shutil
k=shutil.move
y=shutil.rmtree
import time
P=time.sleep
from sqlalchemy import desc,or_,and_,func,not_
from guessit import guessit
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,celery
v=celery.task
L=app.config
from framework.job import Job
from framework.util import Util
from framework.common.daum import MovieSearch
u=MovieSearch.search_imdb
U=MovieSearch.search_movie
from.model import ModelSetting,ModelFileprocessMovieItem
z=ModelFileprocessMovieItem.save
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class LogicMovie(J):
 @C
 def set_movie(data,movie):
  try:
   data['movie']=movie
   data['dest_folder_name']='%s (%s)'%(j('[\\/:*?\"<>|]','',movie['title']).replace('  ',' '),movie['year'])
   if 'more' in movie:
    from.logic import Logic
    folder_rule=Logic.get_setting_value('folder_rule')
    tmp=folder_rule.replace('%TITLE%',movie['title']).replace('%YEAR%',movie['year']).replace('%ENG_TITLE%',movie['more']['eng_title']).replace('%COUNTRY%',movie['more']['country']).replace('%GENRE%',movie['more']['genre']).replace('%DATE%',movie['more']['date']).replace('%RATE%',movie['more']['rate']).replace('%DURING%',movie['more']['during'])
    tmp=j('[\\/:*?\"<>|]','',tmp).replace('  ',' ').replace('[]','')
    data['dest_folder_name']=tmp
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def set_no_movie(data):
  try:
   data['movie']=K
   if data['is_file']:
    data['dest_folder_name']='%s'%j('[\\/:*?\"<>|]','',o.splitext(data['name'])[0].replace('  ',' '))
   else:
    data['dest_folder_name']=data['name']
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def clear_folder(target):
  try:
   datas=e(target)
   for data in datas:
    p=o.join(target,data)
    if o.isdir(p):
     if data.lower()in['subs','sample']:
      try:
       y(p)
      except V as e:
       if e.errno==2:
        pass
       else:
        raise
     else:
      LogicMovie.clear_folder(p)
    else:
     ext=o.splitext(data)[1].lower()[1:]
     if ext in['nfo','txt','rtf','url','html','jpg','png','exe','idx','sub']:
      t(p)
     elif data.lower()=='rarbg.com.mp4':
      t(p)
   datas=e(target)
   if not datas:
    F(target)
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def move_dir_to_dir(src,dest):
  logger.debug('move_dir_to_dir : %s %s',src,dest)
  try:
   if not o.exists(dest):
    k(src,dest)
   else:
    for t in e(src):
     try:
      if o.isdir(o.join(src,t)):
       if o.exists(o.join(dest,t))and o.isdir(o.join(dest,t)):
        LogicMovie.move_dir_to_dir(o.join(src,t),o.join(dest,t))
       else:
        k(o.join(src,t),dest) 
      else:
       if o.exists(o.join(dest,t)):
        t(o.join(src,t))
       else:
        k(o.join(src,t),dest)
     except i as e:
      logger.error('Exxception:%s',e)
      logger.error(B())
    if o.exists(src)and f(e(src))==0:
     F(src)
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
  logger.debug('move_dir_to_dir end: %s %s',src,dest)
 @C
 def move(data,target_path):
  try:
   if data['is_file']:
    dest_folder_path=o.join(target_path,data['target'],data['dest_folder_name'])
    if not o.exists(dest_folder_path):
     W(dest_folder_path)
    if o.exists(o.join(dest_folder_path,data['name'])):
     t(data['fullpath'])
    else:
     k(data['fullpath'],dest_folder_path)
   else:
    LogicMovie.clear_folder(data['fullpath'])
    dest_folder_path=o.join(target_path,data['target'],data['dest_folder_name'])
    LogicMovie.move_dir_to_dir(data['fullpath'],dest_folder_path)
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def process_sub_file_and_trash_file(filelist,target):
  try:
   for item in filelist:
    if item['is_folder']:
     continue
    if item['ext']=='.smi' or item['ext']=='.srt':
     if 'title' in item['guessit']:
      for t in filelist:
       if t['is_folder']and 'title' in t['guessit']:
        if t['guessit']['title']==item['guessit']['title']or t['guessit']['title'].replace(' ','')==item['guessit']['title'].replace(' ',''):
         k(item['fullpath'],t['fullpath'])
         filelist.remove(item)
         break
    else:
     try:
      if(item['ext']!='.mkv' and 'mimetype' not in item['guessit'])or('mimetype' in item['guessit']and item['guessit']['mimetype']in['application/x-bittorrent']):
       LogicMovie.set_no_movie(item)
       item['dest_folder_name']=''
       item['target']=o.join('no_movie','unknown')
       LogicMovie.move(item,target)
       item['flag_move']=X
     except i as e:
      logger.error('Exxception:%s',e)
      logger.error(B())
      logger.error(item)
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def prepare_target(target_path):
  try:
   child=['kor','kor_vod','vod','sub_o','sub_x','no_movie']
   for c in child:
    t=o.join(target_path,c)
    if not o.exists(t):
     try:
      w(t)
     except:
      pass
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def make_list(source_path):
  try:
   filelist=[]
   for path in source_path:
    logger.debug('path:%s',path)
    lists=e(path)
    for f in lists:
     try:
      item={}
      item['flag_move']=S
      item['path']=path
      item['name']=f
      item['fullpath']=o.join(path,f)
      item['is_file']=X if o.isfile(item['fullpath'])else S
      item['is_folder']=not item['is_file']
      item['guessit']=guessit(f)
      item['ext']=o.splitext(f)[1].lower()
      item['search_name']=K
      match=T(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
      if match:
       item['search_name']=match.group('name').replace('.',' ').strip()
       item['search_name']=j(r'\[(.*?)\]','',item['search_name'])
      filelist.append(item)
     except i as e:
      logger.error('Exxception:%s',e)
      logger.error(B())
   return filelist
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def get_info_from_rss(f):
  try:
   item={}
   item['flag_move']=S
   item['name']=f
   item['guessit']=guessit(f)
   if 'language' in item['guessit']:
    item['guessit']['language']=''
   if 'screen_size' not in item['guessit']:
    item['guessit']['screen_size']='--'
   if 'source' not in item['guessit']:
    item['guessit']['source']='--'
   item['search_name']=K
   item['movie']=K
   match=T(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
   if match:
    item['search_name']=match.group('name').replace('.',' ').strip()
    item['search_name']=j(r'\[(.*?)\]','',item['search_name'])
   if 'year' in item['guessit']:
    item['is_include_kor'],movie=U(item['search_name'],item['guessit']['year'])
    if movie and movie[0]['score']==100:
     item['movie']=movie[0]
     if item['movie']['country'].startswith(u'한국'):
      if item['is_include_kor']:
       item['target']='kor_vod'
      else:
       item['target']='kor'
     else:
      if item['is_include_kor']:
       item['target']='vod'
      elif item['name'].lower().find('.kor')!=-1:
       item['target']='vod'
      else:
       item['target']='sub_x'
     item['flag_move']=X
    else:
     logger.debug('NO META!!!!!!!!!!')
     if item['is_include_kor']==S:
      logger.debug('imdb search %s %s ',item['search_name'].lower(),item['guessit']['year'])
      movie=u(item['search_name'].lower(),item['guessit']['year'])
      if movie is not K:
       logger.debug('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
       item['movie']=movie
       item['target']='imdb'
       item['flag_move']=X
   item['guessit']=''
   return item
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
 @C
 def save_db(arg):
  try:
   logger.debug('FOR save_db : %s'%arg)
   if arg['status']=='SAVE_ITEM':
    item=arg['result']['item']
    logger.debug('DB SAVE 3')
    z(item)
    logger.debug('DB SAVE 4')
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
 @C
 def start(source_path,target_path):
  if L['config']['use_celery']:
   result=LogicMovie.start_task.apply_async((source_path,target_path))
   try:
    result.get(on_message=LogicMovie.save_db,propagate=X)
   except:
    logger.debug('CELERY on_message not process.. only get() start')
    try:
     result.get()
    except:
     pass
  else:
   LogicMovie.start_task(source_path,target_path)
 @C
 @v(bind=X)
 def start_task(self,source_path,target_path):
  logger.debug('movie %s, %s',source_path,target_path)
  LogicMovie.prepare_target(target_path)
  try:
   filelist=LogicMovie.make_list(source_path)
   LogicMovie.process_sub_file_and_trash_file(filelist,target_path)
   for item in filelist:
    try:
     if not item['flag_move']and 'year' in item['guessit']:
      item['is_include_kor'],movie=U(item['search_name'],item['guessit']['year'])
      if movie and movie[0]['score']==100:
       LogicMovie.set_movie(item,movie[0])
       if item['movie']['country'].startswith(u'한국'):
        if item['is_include_kor']:
         item['target']='kor_vod'
        else:
         item['target']='kor'
       else:
        if item['is_include_kor']:
         item['target']='vod'
        elif item['name'].lower().find('.kor')!=-1:
         item['target']='vod'
        else:
         item['target']='sub_x'
       LogicMovie.move(item,target_path)
       item['flag_move']=X
      else:
       logger.debug('NO META!!!!!!!!!!')
       logger.debug(item)
       logger.debug(item['search_name'])
       if item['is_include_kor']==S and item['search_name']is not K:
        movie=u(item['search_name'].lower(),item['guessit']['year'])
        if movie is not K:
         logger.debug('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
         LogicMovie.set_movie(item,movie)
         item['target']='imdb'
         LogicMovie.move(item,target_path)
         item['flag_move']=X
     if not item['flag_move']:
      logger.debug('NOT MOVE!!!!!!!!!!!')
      if item['ext']=='.smi' or item['ext']=='.srt':
       LogicMovie.set_no_movie(item)
       item['dest_folder_name']=''
       item['target']=o.join('no_movie','sub')
       LogicMovie.move(item,target_path)
       item['flag_move']=X
      else:
       LogicMovie.set_no_movie(item)
       if 'year' not in item['guessit']:
        item['target']=o.join('no_movie','no_year')
       else:
        item['target']=o.join('no_movie','no_meta')
       LogicMovie.move(item,target_path)
       item['flag_move']=X
     if 'guessit' in item:
      del item['guessit']
     logger.debug('DB SAVE 1')
     z(item)
     logger.debug('DB SAVE 2')
     P(1)
    except i as e:
     logger.error('Exxception:%s',e)
     logger.error(B())
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
  LogicMovie.process_smi(target_path)
 @C
 def process_smi(target):
  try:
   sub_x_path=o.join(target,'sub_x')
   sub_o_path=o.join(target,'sub_o')
   movies=e(sub_x_path)
   for movie in movies:
    movie_path=o.join(sub_x_path,movie)
    smi_count=0
    srt_count=0
    srt_file=K
    video_count=0
    video_file=K
    for f in e(movie_path):
     tmp=o.splitext(f.lower())
     if tmp[1]in['.smi']:
      smi_count+=1
     elif tmp[1]in['.srt']:
      srt_count+=1
      srt_file=f
     elif tmp[1]in['.mp4','.avi','.mkv','.wmv']:
      video_count+=1
      video_file=f
    logger.debug('MOVIE:%s VIDEO:%s SRT:%s SMI:%s',movie,video_file,srt_count,smi_count)
    if(smi_count>0 or srt_count>0)and video_count>0:
     if srt_count==1 and video_count==1:
      video_split=o.splitext(video_file)
      srt_split=o.splitext(srt_file)
      new=video_split[0]
      if srt_file.endswith('.ko.srt'):
       new+='.ko'
      if srt_split[0]!=new:
       k(o.join(movie_path,srt_file),o.join(movie_path,'%s%s'%(new,srt_split[1])))
     LogicMovie.move_dir_to_dir(movie_path,o.join(sub_o_path,movie))
  except i as e:
   logger.error('Exxception:%s',e)
   logger.error(B())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
