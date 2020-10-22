import os
E=object
W=staticmethod
o=Exception
n=None
d=OSError
v=len
N=True
z=False
import sys
import traceback
import logging
import threading
import re
import shutil
import time
from sqlalchemy import desc,or_,and_,func,not_
from guessit import guessit
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,celery
from framework.job import Job
from framework.util import Util
from framework.common.daum import MovieSearch
from.model import ModelSetting,ModelFileprocessMovieItem
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class LogicMovie(E):
 @W
 def set_movie(data,movie):
  try:
   data['movie']=movie
   data['dest_folder_name']='%s (%s)'%(re.sub('[\\/:*?\"<>|]','',movie['title']).replace('  ',' '),movie['year'])
   if 'more' in movie:
    from.logic import Logic
    folder_rule=Logic.get_setting_value('folder_rule')
    tmp=folder_rule.replace('%TITLE%',movie['title']).replace('%YEAR%',movie['year']).replace('%ENG_TITLE%',movie['more']['eng_title']).replace('%COUNTRY%',movie['more']['country']).replace('%GENRE%',movie['more']['genre']).replace('%DATE%',movie['more']['date']).replace('%RATE%',movie['more']['rate']).replace('%DURING%',movie['more']['during'])
    tmp=re.sub('[\\/:*?\"<>|]','',tmp).replace('  ',' ').replace('[]','')
    data['dest_folder_name']=tmp
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def set_no_movie(data):
  try:
   data['movie']=n
   if data['is_file']:
    data['dest_folder_name']='%s'%re.sub('[\\/:*?\"<>|]','',os.path.splitext(data['name'])[0].replace('  ',' '))
   else:
    data['dest_folder_name']=data['name']
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def clear_folder(target):
  try:
   datas=os.listdir(target)
   for data in datas:
    p=os.path.join(target,data)
    if os.path.isdir(p):
     if data.lower()in['subs','sample']:
      try:
       shutil.rmtree(p)
      except d as exception:
       if e.errno==2:
        pass
       else:
        raise
     else:
      LogicMovie.clear_folder(p)
    else:
     ext=os.path.splitext(data)[1].lower()[1:]
     if ext in['nfo','txt','rtf','url','html','jpg','png','exe','idx','sub']:
      os.remove(p)
     elif data.lower()=='rarbg.com.mp4':
      os.remove(p)
   datas=os.listdir(target)
   if not datas:
    os.rmdir(target)
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def move_dir_to_dir(src,dest):
  logger.debug('move_dir_to_dir : %s %s',src,dest)
  try:
   if not os.path.exists(dest):
    shutil.move(src,dest)
   else:
    for t in os.listdir(src):
     try:
      if os.path.isdir(os.path.join(src,t)):
       if os.path.exists(os.path.join(dest,t))and os.path.isdir(os.path.join(dest,t)):
        LogicMovie.move_dir_to_dir(os.path.join(src,t),os.path.join(dest,t))
       else:
        shutil.move(os.path.join(src,t),dest) 
      else:
       if os.path.exists(os.path.join(dest,t)):
        os.remove(os.path.join(src,t))
       else:
        shutil.move(os.path.join(src,t),dest)
     except o as exception:
      logger.error('Exxception:%s',exception)
      logger.error(traceback.format_exc())
    if os.path.exists(src)and v(os.listdir(src))==0:
     os.rmdir(src)
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
  logger.debug('move_dir_to_dir end: %s %s',src,dest)
 @W
 def move(data,target_path):
  try:
   if data['is_file']:
    dest_folder_path=os.path.join(target_path,data['target'],data['dest_folder_name'])
    if not os.path.exists(dest_folder_path):
     os.makedirs(dest_folder_path)
    if os.path.exists(os.path.join(dest_folder_path,data['name'])):
     os.remove(data['fullpath'])
    else:
     shutil.move(data['fullpath'],dest_folder_path)
   else:
    LogicMovie.clear_folder(data['fullpath'])
    dest_folder_path=os.path.join(target_path,data['target'],data['dest_folder_name'])
    LogicMovie.move_dir_to_dir(data['fullpath'],dest_folder_path)
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
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
         shutil.move(item['fullpath'],t['fullpath'])
         filelist.remove(item)
         break
    else:
     try:
      if(item['ext']!='.mkv' and 'mimetype' not in item['guessit'])or('mimetype' in item['guessit']and item['guessit']['mimetype']in['application/x-bittorrent']):
       LogicMovie.set_no_movie(item)
       item['dest_folder_name']=''
       item['target']=os.path.join('no_movie','unknown')
       LogicMovie.move(item,target)
       item['flag_move']=N
     except o as exception:
      logger.error('Exxception:%s',exception)
      logger.error(traceback.format_exc())
      logger.error(item)
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def prepare_target(target_path):
  try:
   child=['kor','kor_vod','vod','sub_o','sub_x','no_movie']
   for c in child:
    t=os.path.join(target_path,c)
    if not os.path.exists(t):
     try:
      os.mkdir(t)
     except:
      pass
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def make_list(source_path):
  try:
   filelist=[]
   for path in source_path:
    logger.debug('path:%s',path)
    lists=os.listdir(path)
    for f in lists:
     try:
      item={}
      item['flag_move']=z
      item['path']=path
      item['name']=f
      item['fullpath']=os.path.join(path,f)
      item['is_file']=N if os.path.isfile(item['fullpath'])else z
      item['is_folder']=not item['is_file']
      item['guessit']=guessit(f)
      item['ext']=os.path.splitext(f)[1].lower()
      item['search_name']=n
      match=re.compile(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
      if match:
       item['search_name']=match.group('name').replace('.',' ').strip()
       item['search_name']=re.sub(r'\[(.*?)\]','',item['search_name'])
      filelist.append(item)
     except o as exception:
      logger.error('Exxception:%s',exception)
      logger.error(traceback.format_exc())
   return filelist
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def get_info_from_rss(f):
  try:
   item={}
   item['flag_move']=z
   item['name']=f
   item['guessit']=guessit(f)
   if 'language' in item['guessit']:
    item['guessit']['language']=''
   if 'screen_size' not in item['guessit']:
    item['guessit']['screen_size']='--'
   if 'source' not in item['guessit']:
    item['guessit']['source']='--'
   item['search_name']=n
   item['movie']=n
   match=re.compile(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
   if match:
    item['search_name']=match.group('name').replace('.',' ').strip()
    item['search_name']=re.sub(r'\[(.*?)\]','',item['search_name'])
   if 'year' in item['guessit']:
    item['is_include_kor'],movie=MovieSearch.search_movie(item['search_name'],item['guessit']['year'])
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
     item['flag_move']=N
    else:
     logger.debug('NO META!!!!!!!!!!')
     if item['is_include_kor']==z:
      logger.debug('imdb search %s %s ',item['search_name'].lower(),item['guessit']['year'])
      movie=MovieSearch.search_imdb(item['search_name'].lower(),item['guessit']['year'])
      if movie is not n:
       logger.debug('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
       item['movie']=movie
       item['target']='imdb'
       item['flag_move']=N
   item['guessit']=''
   return item
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def save_db(arg):
  try:
   logger.debug('FOR save_db : %s'%arg)
   if arg['status']=='SAVE_ITEM':
    item=arg['result']['item']
    logger.debug('DB SAVE 3')
    ModelFileprocessMovieItem.save(item)
    logger.debug('DB SAVE 4')
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @W
 def start(source_path,target_path):
  if app.config['config']['use_celery']:
   result=LogicMovie.start_task.apply_async((source_path,target_path))
   try:
    result.get(on_message=LogicMovie.save_db,propagate=N)
   except:
    logger.debug('CELERY on_message not process.. only get() start')
    try:
     result.get()
    except:
     pass
  else:
   LogicMovie.start_task(source_path,target_path)
 @W
 @celery.task(bind=N)
 def start_task(self,source_path,target_path):
  logger.debug('movie %s, %s',source_path,target_path)
  LogicMovie.prepare_target(target_path)
  try:
   filelist=LogicMovie.make_list(source_path)
   LogicMovie.process_sub_file_and_trash_file(filelist,target_path)
   for item in filelist:
    try:
     if not item['flag_move']and 'year' in item['guessit']:
      item['is_include_kor'],movie=MovieSearch.search_movie(item['search_name'],item['guessit']['year'])
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
       item['flag_move']=N
      else:
       logger.debug('NO META!!!!!!!!!!')
       logger.debug(item)
       logger.debug(item['search_name'])
       if item['is_include_kor']==z and item['search_name']is not n:
        movie=MovieSearch.search_imdb(item['search_name'].lower(),item['guessit']['year'])
        if movie is not n:
         logger.debug('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
         LogicMovie.set_movie(item,movie)
         item['target']='imdb'
         LogicMovie.move(item,target_path)
         item['flag_move']=N
     if not item['flag_move']:
      logger.debug('NOT MOVE!!!!!!!!!!!')
      if item['ext']=='.smi' or item['ext']=='.srt':
       LogicMovie.set_no_movie(item)
       item['dest_folder_name']=''
       item['target']=os.path.join('no_movie','sub')
       LogicMovie.move(item,target_path)
       item['flag_move']=N
      else:
       LogicMovie.set_no_movie(item)
       if 'year' not in item['guessit']:
        item['target']=os.path.join('no_movie','no_year')
       else:
        item['target']=os.path.join('no_movie','no_meta')
       LogicMovie.move(item,target_path)
       item['flag_move']=N
     if 'guessit' in item:
      del item['guessit']
     logger.debug('DB SAVE 1')
     ModelFileprocessMovieItem.save(item)
     logger.debug('DB SAVE 2')
     time.sleep(1)
    except o as exception:
     logger.error('Exxception:%s',exception)
     logger.error(traceback.format_exc())
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
  LogicMovie.process_smi(target_path)
 @W
 def process_smi(target):
  try:
   sub_x_path=os.path.join(target,'sub_x')
   sub_o_path=os.path.join(target,'sub_o')
   movies=os.listdir(sub_x_path)
   for movie in movies:
    movie_path=os.path.join(sub_x_path,movie)
    smi_count=0
    srt_count=0
    srt_file=n
    video_count=0
    video_file=n
    for f in os.listdir(movie_path):
     tmp=os.path.splitext(f.lower())
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
      video_split=os.path.splitext(video_file)
      srt_split=os.path.splitext(srt_file)
      new=video_split[0]
      if srt_file.endswith('.ko.srt'):
       new+='.ko'
      if srt_split[0]!=new:
       shutil.move(os.path.join(movie_path,srt_file),os.path.join(movie_path,'%s%s'%(new,srt_split[1])))
     LogicMovie.move_dir_to_dir(movie_path,os.path.join(sub_o_path,movie))
  except o as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
