import os
x=object
H=None
R=staticmethod
Y=len
d=Exception
X=False
P=int
D=True
import traceback
import time
import shutil
import re
import requests
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.library import ShowSection
from framework import app,db,scheduler,path_app_root,celery,py_urllib
from framework.job import Job
from framework.util import Util
from.plugin import logger,package_name
from.model import ModelSetting
class LogicNormal(x):
 server_instance=H
 @R
 def get_section_id_by_filepath(filepath):
  try:
   if LogicNormal.server_instance is H:
    LogicNormal.server_instance=PlexServer(ModelSetting.get('server_url'),ModelSetting.get('server_token'))
   if LogicNormal.server_instance is H:
    return
   sections=LogicNormal.server_instance.library.sections()
   tmp_len=0
   tmp_section_id=-1
   for section in sections:
    for location in section.locations:
     if filepath.find(location)!=-1:
      if Y(location)>tmp_len:
       tmp_len=Y(location)
       tmp_section_id=section.key
   logger.debug('PLEX get_section_id_by_filepath %s:%s',tmp_section_id,filepath)
   return tmp_section_id
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  return-1
 @R
 def is_exist_in_library_using_bundle(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/count_in_library?filename=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(filepath.encode('utf8')),ModelSetting.get('server_token'))
   data=requests.get(url).text
   if data=='0':
    return X
   else:
    try:
     tmp=P(data)
     if tmp>0:
      return D
    except:
     return X
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return X
 @R
 def get_library_key_using_bundle(filepath,section_id=-1):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_metadata_id_by_filepath&args=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(filepath.encode('utf8')),ModelSetting.get('server_token'))
   data=requests.get(url).text
   return data
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @R
 def get_filepath_list_by_metadata_id_using_bundle(metadata_id):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_filepath_list_by_metadata_id&args=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),metadata_id,ModelSetting.get('server_token'))
   data=requests.get(url).text
   ret=[x.strip()for x in data.split('\n')]
   return ret
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @R
 def metadata_refresh(filepath=H,metadata_id=H):
  try:
   if metadata_id is H:
    if filepath is not H:
     metadata_id=LogicNormal.get_library_key_using_bundle(filepath)
   if metadata_id is H:
    return X 
   url='%s/library/metadata/%s/refresh?X-Plex-Token=%s' %(ModelSetting.get('server_url'),metadata_id,ModelSetting.get('server_token'))
   data=requests.put(url).text
   return D
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return X
 @R
 def os_path_exists(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/os_path_exists?filepath=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(filepath.encode('utf8')),ModelSetting.get('server_token'))
   data=requests.get(url).text
   return(data=='True')
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return X
 @R
 def find_by_filename_part(keyword):
  try:
   query="SELECT metadata_items.id, media_items.id, file, media_items.duration, media_items.bitrate, media_parts.created_at, media_items.size, media_items.width, media_items.height, media_items.video_codec, media_items.audio_codec FROM media_parts, media_items, metadata_items WHERE media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and LOWER(media_parts.file) LIKE '%{keyword}%' and media_items.width > 0 ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(query.encode('utf8')),ModelSetting.get('server_token'))
   data1=requests.get(url).json()
   query="SELECT metadata_items.id, media_items.id, file, media_streams.url FROM media_parts, media_items, metadata_items, media_streams WHERE media_streams.media_item_id = media_items.id and media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and media_streams.stream_type_id = 3 and media_parts.file LIKE '%{keyword}%' ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(query.encode('utf8')),ModelSetting.get('server_token'))
   data2=requests.get(url).json()
   ret={'ret':D}
   ret['list']=[]
   ret['metadata_id']=[]
   for tmp in data1['data']:
    if tmp=='':
     continue
    tmp=tmp.split('|')
    item={}
    item['metadata_id']='/library/metadata/%s'%tmp[0]
    item['media_id']=tmp[1]
    item['filepath']=tmp[2]
    item['filename']=tmp[2]
    lastindex=0
    if tmp[2][0]=='/':
     lastindex=tmp[2].rfind('/')
    else:
     lastindex=tmp[2].rfind('\\')
    item['dir']=tmp[2][:lastindex]
    item['filename']=tmp[2][lastindex+1:]
    item['duration']=P(tmp[3])
    item['bitrate']=P(tmp[4])
    item['created_at']=tmp[5]
    item['size']=P(tmp[6])
    item['size_str']=Util.sizeof_fmt(item['size'],suffix='B')
    item['width']=P(tmp[7])
    item['height']=P(tmp[8])
    item['video_codec']=tmp[9]
    item['audio_codec']=tmp[10]
    ret['list'].append(item)
    if item['metadata_id']not in ret['metadata_id']:
     ret['metadata_id'].append(item['metadata_id'])
   for tmp in data2['data']:
    if tmp=='':
     continue
    tmp=tmp.split('|')
    for item in ret['list']:
     if item['media_id']==tmp[1]and item['filepath']==tmp[2]:
      item['sub']=tmp[3]
      break
   logger.debug(ret)
   return ret
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return H
 @R
 def execute_query(query):
  try:
   url='{server}/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query={query}&X-Plex-Token={token}'.format(server=ModelSetting.get('server_url'),query=query,token=ModelSetting.get('server_token'))
   return requests.get(url).json()
  except d as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return X
# Created by pyminifier (https://github.com/liftoff/pyminifier)
