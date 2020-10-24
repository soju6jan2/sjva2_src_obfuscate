import traceback
import os
import json
import time
import copy
from framework import logger
from framework.common.daum import DaumTV
from system.model import ModelSetting as SystemModelSetting
from.process_movie import ProcessMovie
from.process_av import ProcessAV
class TorrentProcess:
 @staticmethod
 def is_broadcast_member():
  if SystemModelSetting.get('ddns').find('https://sjva-server.soju6jan.com')!=-1:
   return True
  return False
 @staticmethod
 def server_process(save_list,category=None):
  if TorrentProcess.is_broadcast_member():
   logger.debug(category)
   if category=='KTV':
    TorrentProcess.server_process_ktv(save_list)
   elif category=='MOVIE':
    return TorrentProcess.server_process_movie(save_list)
   elif category=='AV':
    return TorrentProcess.server_process_av(save_list)
 @staticmethod
 def server_process_ktv(save_list):
  for item in save_list:
   item=item.as_dict()
   if item['torrent_info']is not None:
    try:
     for info in item['torrent_info']:
      logger.debug('Magnet : %s',info['magnet_uri'])
      logger.debug('Name : %s',info['name'])
      info['video_count']=0
      info['files_original']=copy.deepcopy(info['files'])
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
        if entity.daum_info is not None:
         daum=entity.daum_info.as_dict()
         f['daum']={'daum_id':str(daum['daum_id']),'poster_url':daum['poster_url'],'genre':daum['genre'],'title':daum['title'],}
        else:
         f['daum']=None
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
       text=json.dumps(telegram,indent=2)
       from framework.common.telegram_bot import TelegramBot
       TelegramBot.super_send_message(text)
       time.sleep(0.5)
    except Exception as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc()) 
 @staticmethod
 def server_process_movie(save_list):
  lists=[]
  for item in save_list:
   item=item.as_dict()
   sub=[]
   if item['files']:
    for tmp in item['files']:
     ext=os.path.splitext(tmp[1])[1].lower()
     if ext in['.smi','.srt','.ass']:
      sub.append(tmp)
   if item['torrent_info']is not None:
    try:
     for info in item['torrent_info']:
      fileinfo=TorrentProcess.get_max_size_fileinfo(info)
      movie=ProcessMovie.get_info_from_rss(fileinfo['filename'])
      torrent_info={}
      torrent_info['name']=info['name']
      torrent_info['size']=info['total_size']
      torrent_info['num']=info['num_files']
      torrent_info['hash']=info['info_hash']
      torrent_info['filename']=fileinfo['filename']
      torrent_info['dirname']=fileinfo['dirname']
      torrent_info['url']=item['url']
      movie_info={}
      if movie['movie']is not None:
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
       movie_info=None
      ret={}
      ret['server_id']=item['id']
      if len(sub)>0:
       ret['s']=sub
      if movie_info is not None:
       ret['m']=movie_info
      ret['t']=torrent_info
      lists.append(ret)
      telegram={}
      telegram['plugin']='bot_downloader_movie'
      telegram['data']=ret
      text=json.dumps(telegram,indent=2)
      from framework.common.telegram_bot import TelegramBot
      TelegramBot.super_send_message(text)
      time.sleep(0.5)
    except Exception as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc()) 
  return lists
 @staticmethod
 def server_process_av(save_list):
  lists=[]
  for item in save_list:
   item=item.as_dict()
   av_type=item['board']
   av_type='censored' if av_type in['NONE','torrent_ymav','censored_tor']else av_type
   av_type='uncensored' if av_type in['torrent_nmav','uncensored_tor']else av_type
   av_type='western' if av_type in['torrent_amav','white_tor']else av_type
   if item['torrent_info']is not None:
    try:
     for info in item['torrent_info']:
      fileinfo=TorrentProcess.get_max_size_fileinfo(info)
      av=ProcessAV.process(fileinfo['filename'],av_type)
      if av is None:
       if av_type=='western' and fileinfo['dirname']!='':
        av=ProcessAV.process(fileinfo['dirname'],av_type)
      if av is None:
       logger.debug(u'AV 검색 실패')
       logger.debug(fileinfo['filename'])
       logger.debug(av_type)
       continue
      torrent_info={}
      torrent_info['name']=info['name']
      torrent_info['size']=info['total_size']
      torrent_info['num']=info['num_files']
      torrent_info['hash']=info['info_hash']
      torrent_info['filename']=fileinfo['filename']
      torrent_info['dirname']=fileinfo['dirname']
      torrent_info['url']=item['url']
      av_info=None
      if av is not None:
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
       logger.debug('AV 검색 실패')
       logger.debug(fileinfo['filename'])
      ret={'av_type':av_type}
      ret['server_id']=item['id']
      if av_info is not None:
       ret['av']=av_info
      ret['t']=torrent_info
      lists.append(ret)
      telegram={}
      telegram['plugin']='bot_downloader_av'
      telegram['data']=ret
      text=json.dumps(telegram,indent=2)
      from framework.common.telegram_bot import TelegramBot
      TelegramBot.super_send_message(text)
      time.sleep(0.5)
    except Exception as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc()) 
  return lists
 @staticmethod
 def analyse_torrent_info_file(file_info):
  try:
   file_info['dirs']=os.path.split(file_info['path'])
   file_info['filename']=os.path.basename(file_info['dirs'][-1])
   file_info['filename_except_ext'],file_info['ext']=os.path.splitext(file_info['filename'])
   if file_info['ext'].lower()in['.mp4','.mkv','.avi','.wmv']:
    file_info['type']='video'
   elif file_info['ext'].lower()in['.srt','.smi','.ass']:
    file_info['type']='sub'
   else:
    file_info['type']=None
   return file_info
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @staticmethod
 def get_max_size_fileinfo(torrent_info):
  try:
   ret={}
   max_size=-1
   max_filename=None
   for t in torrent_info['files']:
    if t['size']>max_size:
     max_size=t['size']
     max_filename=str(t['path'])
   t=max_filename.split('/')
   ret['filename']=t[-1]
   if len(t)==1:
    ret['dirname']=''
   elif len(t)==2:
    ret['dirname']=t[0]
   else:
    ret['dirname']=max_filename.replace('/%s'%ret['filename'],'')
   ret['max_size']=max_size
   return ret
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @staticmethod
 def receive_new_data(entity,package_name):
  try:
   if not TorrentProcess.is_broadcast_member():
    return
   if SystemModelSetting.get('ddns').find('https://sjva-dev.soju6jan.com')!=-1:
    return
   if package_name=='bot_downloader_ktv':
    TorrentProcess.append('ktv',entity)
   elif package_name=='bot_downloader_movie':
    TorrentProcess.append('movie',entity)
   elif package_name=='bot_downloader_av':
    TorrentProcess.append('av',entity)
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @staticmethod
 def append(type,data):
  try:
   import requests
   import json
   response=requests.post("https://sjva.me/sjva/torrent_%s.php"%type,data={'data':json.dumps(data.as_dict())})
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
