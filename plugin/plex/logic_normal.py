import os
d=object
v=None
C=staticmethod
h=len
Q=Exception
F=False
J=int
H=True
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
class LogicNormal(d):
 server_instance=v
 @C
 def get_section_id_by_filepath(filepath):
  try:
   if LogicNormal.server_instance is v:
    LogicNormal.server_instance=PlexServer(ModelSetting.get('server_url'),ModelSetting.get('server_token'))
   if LogicNormal.server_instance is v:
    return
   sections=LogicNormal.server_instance.library.sections()
   tmp_len=0
   tmp_section_id=-1
   for section in sections:
    for location in section.locations:
     if filepath.find(location)!=-1:
      if h(location)>tmp_len:
       tmp_len=h(location)
       tmp_section_id=section.key
   logger.debug('PLEX get_section_id_by_filepath %s:%s',tmp_section_id,filepath)
   return tmp_section_id
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  return-1
 @C
 def is_exist_in_library_using_bundle(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/count_in_library?filename=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(filepath.encode('utf8')),ModelSetting.get('server_token'))
   data=requests.get(url).text
   if data=='0':
    return F
   else:
    try:
     tmp=J(data)
     if tmp>0:
      return H
    except:
     return F
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return F
 @C
 def get_library_key_using_bundle(filepath,section_id=-1):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_metadata_id_by_filepath&args=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(filepath.encode('utf8')),ModelSetting.get('server_token'))
   data=requests.get(url).text
   return data
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 def get_filepath_list_by_metadata_id_using_bundle(metadata_id):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_filepath_list_by_metadata_id&args=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),metadata_id,ModelSetting.get('server_token'))
   data=requests.get(url).text
   ret=[x.strip()for x in data.split('\n')]
   return ret
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 def metadata_refresh(filepath=v,metadata_id=v):
  try:
   if metadata_id is v:
    if filepath is not v:
     metadata_id=LogicNormal.get_library_key_using_bundle(filepath)
   if metadata_id is v:
    return F 
   url='%s/library/metadata/%s/refresh?X-Plex-Token=%s' %(ModelSetting.get('server_url'),metadata_id,ModelSetting.get('server_token'))
   data=requests.put(url).text
   return H
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return F
 @C
 def os_path_exists(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/os_path_exists?filepath=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(filepath.encode('utf8')),ModelSetting.get('server_token'))
   data=requests.get(url).text
   return(data=='True')
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return F
 @C
 def find_by_filename_part(keyword):
  try:
   query="SELECT metadata_items.id, media_items.id, file, media_items.duration, media_items.bitrate, media_parts.created_at, media_items.size, media_items.width, media_items.height, media_items.video_codec, media_items.audio_codec FROM media_parts, media_items, metadata_items WHERE media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and LOWER(media_parts.file) LIKE '%{keyword}%' and media_items.width > 0 ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(query.encode('utf8')),ModelSetting.get('server_token'))
   data1=requests.get(url).json()
   query="SELECT metadata_items.id, media_items.id, file, media_streams.url FROM media_parts, media_items, metadata_items, media_streams WHERE media_streams.media_item_id = media_items.id and media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and media_streams.stream_type_id = 3 and media_parts.file LIKE '%{keyword}%' ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(ModelSetting.get('server_url'),py_urllib.quote(query.encode('utf8')),ModelSetting.get('server_token'))
   data2=requests.get(url).json()
   ret={'ret':H}
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
    item['duration']=J(tmp[3])
    item['bitrate']=J(tmp[4])
    item['created_at']=tmp[5]
    item['size']=J(tmp[6])
    item['size_str']=Util.sizeof_fmt(item['size'],suffix='B')
    item['width']=J(tmp[7])
    item['height']=J(tmp[8])
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
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return v
 @C
 def execute_query(query):
  try:
   url='{server}/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query={query}&X-Plex-Token={token}'.format(server=ModelSetting.get('server_url'),query=query,token=ModelSetting.get('server_token'))
   return requests.get(url).json()
  except Q as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return F
# Created by pyminifier (https://github.com/liftoff/pyminifier)
