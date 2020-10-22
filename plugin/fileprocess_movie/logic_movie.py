import os
E=object
G=staticmethod
l=Exception
T=None
D=OSError
W=len
J=True
V=False
P=os.mkdir
O=os.makedirs
C=os.rmdir
a=os.remove
d=os.listdir
x=os.path
import sys
import traceback
c=traceback.format_exc
import logging
import threading
import re
K=re.compile
v=re.sub
import shutil
L=shutil.move
A=shutil.rmtree
import time
p=time.sleep
from sqlalchemy import desc,or_,and_,func,not_
from guessit import guessit
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,celery
e=celery.task
i=app.config
from framework.job import Job
from framework.util import Util
from framework.common.daum import MovieSearch
Y=MovieSearch.search_imdb
r=MovieSearch.search_movie
from.model import ModelSetting,ModelFileprocessMovieItem
m=ModelFileprocessMovieItem.save
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class LogicMovie(E):
 @G
 def set_movie(data,movie):
  try:
   data['movie']=movie
   data['dest_folder_name']='%s (%s)'%(v('[\\/:*?\"<>|]','',movie['title']).replace('  ',' '),movie['year'])
   if 'more' in movie:
    from.logic import Logic
    folder_rule=Logic.get_setting_value('folder_rule')
    tmp=folder_rule.replace('%TITLE%',movie['title']).replace('%YEAR%',movie['year']).replace('%ENG_TITLE%',movie['more']['eng_title']).replace('%COUNTRY%',movie['more']['country']).replace('%GENRE%',movie['more']['genre']).replace('%DATE%',movie['more']['date']).replace('%RATE%',movie['more']['rate']).replace('%DURING%',movie['more']['during'])
    tmp=v('[\\/:*?\"<>|]','',tmp).replace('  ',' ').replace('[]','')
    data['dest_folder_name']=tmp
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
 def set_no_movie(data):
  try:
   data['movie']=T
   if data['is_file']:
    data['dest_folder_name']='%s'%v('[\\/:*?\"<>|]','',x.splitext(data['name'])[0].replace('  ',' '))
   else:
    data['dest_folder_name']=data['name']
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
 def clear_folder(target):
  try:
   datas=d(target)
   for data in datas:
    p=x.join(target,data)
    if x.isdir(p):
     if data.lower()in['subs','sample']:
      try:
       A(p)
      except D as e:
       if e.errno==2:
        pass
       else:
        raise
     else:
      LogicMovie.clear_folder(p)
    else:
     ext=x.splitext(data)[1].lower()[1:]
     if ext in['nfo','txt','rtf','url','html','jpg','png','exe','idx','sub']:
      a(p)
     elif data.lower()=='rarbg.com.mp4':
      a(p)
   datas=d(target)
   if not datas:
    C(target)
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
 def move_dir_to_dir(src,dest):
  logger.debug('move_dir_to_dir : %s %s',src,dest)
  try:
   if not x.exists(dest):
    L(src,dest)
   else:
    for t in d(src):
     try:
      if x.isdir(x.join(src,t)):
       if x.exists(x.join(dest,t))and x.isdir(x.join(dest,t)):
        LogicMovie.move_dir_to_dir(x.join(src,t),x.join(dest,t))
       else:
        L(x.join(src,t),dest) 
      else:
       if x.exists(x.join(dest,t)):
        a(x.join(src,t))
       else:
        L(x.join(src,t),dest)
     except l as e:
      logger.error('Exxception:%s',e)
      logger.error(c())
    if x.exists(src)and W(d(src))==0:
     C(src)
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
  logger.debug('move_dir_to_dir end: %s %s',src,dest)
 @G
 def move(data,target_path):
  try:
   if data['is_file']:
    dest_folder_path=x.join(target_path,data['target'],data['dest_folder_name'])
    if not x.exists(dest_folder_path):
     O(dest_folder_path)
    if x.exists(x.join(dest_folder_path,data['name'])):
     a(data['fullpath'])
    else:
     L(data['fullpath'],dest_folder_path)
   else:
    LogicMovie.clear_folder(data['fullpath'])
    dest_folder_path=x.join(target_path,data['target'],data['dest_folder_name'])
    LogicMovie.move_dir_to_dir(data['fullpath'],dest_folder_path)
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
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
         L(item['fullpath'],t['fullpath'])
         filelist.remove(item)
         break
    else:
     try:
      if(item['ext']!='.mkv' and 'mimetype' not in item['guessit'])or('mimetype' in item['guessit']and item['guessit']['mimetype']in['application/x-bittorrent']):
       LogicMovie.set_no_movie(item)
       item['dest_folder_name']=''
       item['target']=x.join('no_movie','unknown')
       LogicMovie.move(item,target)
       item['flag_move']=J
     except l as e:
      logger.error('Exxception:%s',e)
      logger.error(c())
      logger.error(item)
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
 def prepare_target(target_path):
  try:
   child=['kor','kor_vod','vod','sub_o','sub_x','no_movie']
   for c in child:
    t=x.join(target_path,c)
    if not x.exists(t):
     try:
      P(t)
     except:
      pass
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
 def make_list(source_path):
  try:
   filelist=[]
   for path in source_path:
    logger.debug('path:%s',path)
    lists=d(path)
    for f in lists:
     try:
      item={}
      item['flag_move']=V
      item['path']=path
      item['name']=f
      item['fullpath']=x.join(path,f)
      item['is_file']=J if x.isfile(item['fullpath'])else V
      item['is_folder']=not item['is_file']
      item['guessit']=guessit(f)
      item['ext']=x.splitext(f)[1].lower()
      item['search_name']=T
      match=K(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
      if match:
       item['search_name']=match.group('name').replace('.',' ').strip()
       item['search_name']=v(r'\[(.*?)\]','',item['search_name'])
      filelist.append(item)
     except l as e:
      logger.error('Exxception:%s',e)
      logger.error(c())
   return filelist
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
 def get_info_from_rss(f):
  try:
   item={}
   item['flag_move']=V
   item['name']=f
   item['guessit']=guessit(f)
   if 'language' in item['guessit']:
    item['guessit']['language']=''
   if 'screen_size' not in item['guessit']:
    item['guessit']['screen_size']='--'
   if 'source' not in item['guessit']:
    item['guessit']['source']='--'
   item['search_name']=T
   item['movie']=T
   match=K(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
   if match:
    item['search_name']=match.group('name').replace('.',' ').strip()
    item['search_name']=v(r'\[(.*?)\]','',item['search_name'])
   if 'year' in item['guessit']:
    item['is_include_kor'],movie=r(item['search_name'],item['guessit']['year'])
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
     item['flag_move']=J
    else:
     logger.debug('NO META!!!!!!!!!!')
     if item['is_include_kor']==V:
      logger.debug('imdb search %s %s ',item['search_name'].lower(),item['guessit']['year'])
      movie=Y(item['search_name'].lower(),item['guessit']['year'])
      if movie is not T:
       logger.debug('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
       item['movie']=movie
       item['target']='imdb'
       item['flag_move']=J
   item['guessit']=''
   return item
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
 @G
 def save_db(arg):
  try:
   logger.debug('FOR save_db : %s'%arg)
   if arg['status']=='SAVE_ITEM':
    item=arg['result']['item']
    logger.debug('DB SAVE 3')
    m(item)
    logger.debug('DB SAVE 4')
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
 @G
 def start(source_path,target_path):
  if i['config']['use_celery']:
   result=LogicMovie.start_task.apply_async((source_path,target_path))
   try:
    result.get(on_message=LogicMovie.save_db,propagate=J)
   except:
    logger.debug('CELERY on_message not process.. only get() start')
    try:
     result.get()
    except:
     pass
  else:
   LogicMovie.start_task(source_path,target_path)
 @G
 @e(bind=J)
 def start_task(self,source_path,target_path):
  logger.debug('movie %s, %s',source_path,target_path)
  LogicMovie.prepare_target(target_path)
  try:
   filelist=LogicMovie.make_list(source_path)
   LogicMovie.process_sub_file_and_trash_file(filelist,target_path)
   for item in filelist:
    try:
     if not item['flag_move']and 'year' in item['guessit']:
      item['is_include_kor'],movie=r(item['search_name'],item['guessit']['year'])
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
       item['flag_move']=J
      else:
       logger.debug('NO META!!!!!!!!!!')
       logger.debug(item)
       logger.debug(item['search_name'])
       if item['is_include_kor']==V and item['search_name']is not T:
        movie=Y(item['search_name'].lower(),item['guessit']['year'])
        if movie is not T:
         logger.debug('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
         LogicMovie.set_movie(item,movie)
         item['target']='imdb'
         LogicMovie.move(item,target_path)
         item['flag_move']=J
     if not item['flag_move']:
      logger.debug('NOT MOVE!!!!!!!!!!!')
      if item['ext']=='.smi' or item['ext']=='.srt':
       LogicMovie.set_no_movie(item)
       item['dest_folder_name']=''
       item['target']=x.join('no_movie','sub')
       LogicMovie.move(item,target_path)
       item['flag_move']=J
      else:
       LogicMovie.set_no_movie(item)
       if 'year' not in item['guessit']:
        item['target']=x.join('no_movie','no_year')
       else:
        item['target']=x.join('no_movie','no_meta')
       LogicMovie.move(item,target_path)
       item['flag_move']=J
     if 'guessit' in item:
      del item['guessit']
     logger.debug('DB SAVE 1')
     m(item)
     logger.debug('DB SAVE 2')
     p(1)
    except l as e:
     logger.error('Exxception:%s',e)
     logger.error(c())
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
  LogicMovie.process_smi(target_path)
 @G
 def process_smi(target):
  try:
   sub_x_path=x.join(target,'sub_x')
   sub_o_path=x.join(target,'sub_o')
   movies=d(sub_x_path)
   for movie in movies:
    movie_path=x.join(sub_x_path,movie)
    smi_count=0
    srt_count=0
    srt_file=T
    video_count=0
    video_file=T
    for f in d(movie_path):
     tmp=x.splitext(f.lower())
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
      video_split=x.splitext(video_file)
      srt_split=x.splitext(srt_file)
      new=video_split[0]
      if srt_file.endswith('.ko.srt'):
       new+='.ko'
      if srt_split[0]!=new:
       L(x.join(movie_path,srt_file),x.join(movie_path,'%s%s'%(new,srt_split[1])))
     LogicMovie.move_dir_to_dir(movie_path,x.join(sub_o_path,movie))
  except l as e:
   logger.error('Exxception:%s',e)
   logger.error(c())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
