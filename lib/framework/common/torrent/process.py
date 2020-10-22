import traceback
t=staticmethod
l=True
J=False
N=None
P=str
w=Exception
f=len
F=type
j=traceback.format_exc
import os
h=os.path
import json
u=json.dumps
import time
I=time.sleep
import copy
C=copy.deepcopy
from framework import logger
L=logger.error
n=logger.debug
from framework.common.daum import DaumTV
from system.model import ModelSetting as SystemModelSetting
X=SystemModelSetting.get
from.process_movie import ProcessMovie
M=ProcessMovie.get_info_from_rss
from.process_av import ProcessAV
V=ProcessAV.process
class TorrentProcess:
 @t
 def is_broadcast_member():
  if X('ddns').find('https://sjva-server.soju6jan.com')!=-1:
   return l
  return J
 @t
 def server_process(save_list,category=N):
  if TorrentProcess.is_broadcast_member():
   n(category)
   if category=='KTV':
    TorrentProcess.server_process_ktv(save_list)
   elif category=='MOVIE':
    return TorrentProcess.server_process_movie(save_list)
   elif category=='AV':
    return TorrentProcess.server_process_av(save_list)
 @t
 def server_process_ktv(save_list):
  for item in save_list:
   item=item.as_dict()
   if item['torrent_info']is not N:
    try:
     for info in item['torrent_info']:
      n('Magnet : %s',info['magnet_uri'])
      n('Name : %s',info['name'])
      info['video_count']=0
      info['files_original']=C(info['files'])
      for f in info['files']:
       TorrentProcess.analyse_torrent_info_file(f)
       if f['type']=='video':
        import ktv
        entity=ktv.EntityShow(f['filename'],by='only_filename')
        f['ktv']={}
        f['ktv']['filename_rule']=entity.filename
        f['ktv']['name']=entity.filename_name
        f['ktv']['date']=entity.filename_date
        f['ktv']['number']=entity.filename_no
        f['ktv']['quality']=entity.filename_quality
        f['ktv']['release']=entity.filename_release
        if entity.daum_info is not N:
         daum=entity.daum_info.as_dict()
         f['daum']={'daum_id':P(daum['daum_id']),'poster_url':daum['poster_url'],'genre':daum['genre'],'title':daum['title'],}
        else:
         f['daum']=N
        info['video_count']+=1
      if info['video_count']==1:
       ret={}
       ret['server_id']=item['id']
       ret['broadcast_type']='auto'
       ret['hash']=info['info_hash']
       ret['file_count']=info['num_files']
       ret['files']=info['files_original']
       ret['total_size']=info['total_size']
       ret['video_count']=info['video_count']
       for f in info['files']:
        if f['type']=='video':
         ret['filename']=f['filename']
         ret['ktv']=f['ktv']
         ret['daum']=f['daum']
       info['broadcast']=ret
       telegram={}
       telegram['plugin']='bot_downloader_ktv'
       telegram['sub']='torrent'
       telegram['data']=ret
       text=u(telegram,indent=2)
       from framework.common.telegram_bot import TelegramBot
       TelegramBot.super_send_message(text)
       I(0.5)
    except w as e:
     L('Exception:%s',e)
     L(j()) 
 @t
 def server_process_movie(save_list):
  lists=[]
  for item in save_list:
   item=item.as_dict()
   sub=[]
   if item['files']:
    for tmp in item['files']:
     ext=h.splitext(tmp[1])[1].lower()
     if ext in['.smi','.srt','.ass']:
      sub.append(tmp)
   if item['torrent_info']is not N:
    try:
     for info in item['torrent_info']:
      fileinfo=TorrentProcess.get_max_size_fileinfo(info)
      movie=M(fileinfo['filename'])
      torrent_info={}
      torrent_info['name']=info['name']
      torrent_info['size']=info['total_size']
      torrent_info['num']=info['num_files']
      torrent_info['hash']=info['info_hash']
      torrent_info['filename']=fileinfo['filename']
      torrent_info['dirname']=fileinfo['dirname']
      torrent_info['url']=item['url']
      movie_info={}
      if movie['movie']is not N:
       movie_info['title']=movie['movie']['title']
       movie_info['target']=movie['target'].replace('sub_x','sub')
       movie_info['kor']=movie['is_include_kor']
       if movie_info['target']=='imdb':
        movie_info['id']=movie['movie']['id']
        movie_info['year']=movie['movie']['year']
       else:
        movie_info['daum']={}
        movie_info['id']=movie['movie']['id']
        movie_info['daum']['country']=movie['movie']['country']
        movie_info['year']=movie['movie']['year']
        movie_info['daum']['poster']=movie['movie']['more']['poster']
        movie_info['daum']['eng']=movie['movie']['more']['eng_title']
        movie_info['daum']['rate']=movie['movie']['more']['rate']
        movie_info['daum']['genre']=movie['movie']['more']['genre']
      else:
       movie_info=N
      ret={}
      ret['server_id']=item['id']
      if f(sub)>0:
       ret['s']=sub
      if movie_info is not N:
       ret['m']=movie_info
      ret['t']=torrent_info
      lists.append(ret)
      telegram={}
      telegram['plugin']='bot_downloader_movie'
      telegram['data']=ret
      text=u(telegram,indent=2)
      from framework.common.telegram_bot import TelegramBot
      TelegramBot.super_send_message(text)
      I(0.5)
    except w as e:
     L('Exception:%s',e)
     L(j()) 
  return lists
 @t
 def server_process_av(save_list):
  lists=[]
  for item in save_list:
   item=item.as_dict()
   av_type=item['board']
   av_type='censored' if av_type in['NONE','torrent_ymav','censored_tor']else av_type
   av_type='uncensored' if av_type in['torrent_nmav','uncensored_tor']else av_type
   av_type='western' if av_type in['torrent_amav','white_tor']else av_type
   if item['torrent_info']is not N:
    try:
     for info in item['torrent_info']:
      fileinfo=TorrentProcess.get_max_size_fileinfo(info)
      av=V(fileinfo['filename'],av_type)
      if av is N:
       if av_type=='western' and fileinfo['dirname']!='':
        av=V(fileinfo['dirname'],av_type)
      if av is N:
       n(u'AV 검색 실패')
       n(fileinfo['filename'])
       n(av_type)
       continue
      torrent_info={}
      torrent_info['name']=info['name']
      torrent_info['size']=info['total_size']
      torrent_info['num']=info['num_files']
      torrent_info['hash']=info['info_hash']
      torrent_info['filename']=fileinfo['filename']
      torrent_info['dirname']=fileinfo['dirname']
      torrent_info['url']=item['url']
      av_info=N
      if av is not N:
       av_info={}
       av_info['meta']=av['type']
       av_info['code_show']=av['data']['update']['code_show']
       av_info['title']=av['data']['update']['title_ko']
       av_info['poster']=av['data']['update']['poster']
       av_info['genre']=av['data']['update']['genre']
       av_info['performer']=[]
       for t in av['data']['update']['performer']:
        if t['name_kor']!='':
         av_info['performer'].append(t['name_kor'])
       av_info['studio']=av['data']['update']['studio_ko']
       av_info['date']=av['data']['update']['date']
      else:
       n('AV 검색 실패')
       n(fileinfo['filename'])
      ret={'av_type':av_type}
      ret['server_id']=item['id']
      if av_info is not N:
       ret['av']=av_info
      ret['t']=torrent_info
      lists.append(ret)
      telegram={}
      telegram['plugin']='bot_downloader_av'
      telegram['data']=ret
      text=u(telegram,indent=2)
      from framework.common.telegram_bot import TelegramBot
      TelegramBot.super_send_message(text)
      I(0.5)
    except w as e:
     L('Exception:%s',e)
     L(j()) 
  return lists
 @t
 def analyse_torrent_info_file(file_info):
  try:
   file_info['dirs']=h.split(file_info['path'])
   file_info['filename']=h.basename(file_info['dirs'][-1])
   file_info['filename_except_ext'],file_info['ext']=h.splitext(file_info['filename'])
   if file_info['ext'].lower()in['.mp4','.mkv','.avi','.wmv']:
    file_info['type']='video'
   elif file_info['ext'].lower()in['.srt','.smi','.ass']:
    file_info['type']='sub'
   else:
    file_info['type']=N
   return file_info
  except w as e:
   L('Exception:%s',e)
   L(j())
 @t
 def get_max_size_fileinfo(torrent_info):
  try:
   ret={}
   max_size=-1
   max_filename=N
   for t in torrent_info['files']:
    if t['size']>max_size:
     max_size=t['size']
     max_filename=P(t['path'])
   t=max_filename.split('/')
   ret['filename']=t[-1]
   if f(t)==1:
    ret['dirname']=''
   elif f(t)==2:
    ret['dirname']=t[0]
   else:
    ret['dirname']=max_filename.replace('/%s'%ret['filename'],'')
   ret['max_size']=max_size
   return ret
  except w as e:
   L('Exception:%s',e)
   L(j())
 @t
 def receive_new_data(entity,package_name):
  try:
   if not TorrentProcess.is_broadcast_member():
    return
   if X('ddns').find('https://sjva-dev.soju6jan.com')!=-1:
    return
   if package_name=='bot_downloader_ktv':
    TorrentProcess.append('ktv',entity)
   elif package_name=='bot_downloader_movie':
    TorrentProcess.append('movie',entity)
   elif package_name=='bot_downloader_av':
    TorrentProcess.append('av',entity)
  except w as e:
   L('Exception:%s',e)
   L(j())
 @t
 def append(F,data):
  try:
   import requests
   import json
   response=requests.post("https://sjva.me/sjva/torrent_%s.php"%F,data={'data':u(data.as_dict())})
      u=json.dumps
  except w as e:
   L('Exception:%s',e)
   L(j())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
