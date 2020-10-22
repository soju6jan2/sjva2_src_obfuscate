import os
j=object
k=None
a=staticmethod
M=len
g=Exception
L=False
y=int
v=True
import traceback
C=traceback.format_exc
import time
import shutil
import re
import requests
K=requests.put
P=requests.get
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.library import ShowSection
from framework import app,db,scheduler,path_app_root,celery,py_urllib
D=py_urllib.quote
from framework.job import Job
from framework.util import Util
W=Util.sizeof_fmt
from.plugin import logger,package_name
X=logger.error
c=logger.debug
from.model import ModelSetting
r=ModelSetting.get
class LogicNormal(j):
 server_instance=k
 @a
 def get_section_id_by_filepath(filepath):
  try:
   if LogicNormal.server_instance is k:
    LogicNormal.server_instance=PlexServer(r('server_url'),r('server_token'))
   if LogicNormal.server_instance is k:
    return
   sections=LogicNormal.server_instance.library.sections()
   tmp_len=0
   tmp_section_id=-1
   for section in sections:
    for location in section.locations:
     if filepath.find(location)!=-1:
      if M(location)>tmp_len:
       tmp_len=M(location)
       tmp_section_id=section.key
   c('PLEX get_section_id_by_filepath %s:%s',tmp_section_id,filepath)
   return tmp_section_id
  except g as e:
   X('Exception:%s',e)
   X(C()) 
  return-1
 @a
 def is_exist_in_library_using_bundle(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/count_in_library?filename=%s&X-Plex-Token=%s'%(r('server_url'),D(filepath.encode('utf8')),r('server_token'))
   data=P(url).text
   if data=='0':
    return L
   else:
    try:
     tmp=y(data)
     if tmp>0:
      return v
    except:
     return L
  except g as e:
   X('Exception:%s',e)
   X(C())
   return L
 @a
 def get_library_key_using_bundle(filepath,section_id=-1):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_metadata_id_by_filepath&args=%s&X-Plex-Token=%s'%(r('server_url'),D(filepath.encode('utf8')),r('server_token'))
   data=P(url).text
   return data
  except g as e:
   X('Exception:%s',e)
   X(C())
 @a
 def get_filepath_list_by_metadata_id_using_bundle(metadata_id):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_filepath_list_by_metadata_id&args=%s&X-Plex-Token=%s'%(r('server_url'),metadata_id,r('server_token'))
   data=P(url).text
   ret=[x.strip()for x in data.split('\n')]
   return ret
  except g as e:
   X('Exception:%s',e)
   X(C())
 @a
 def metadata_refresh(filepath=k,metadata_id=k):
  try:
   if metadata_id is k:
    if filepath is not k:
     metadata_id=LogicNormal.get_library_key_using_bundle(filepath)
   if metadata_id is k:
    return L 
   url='%s/library/metadata/%s/refresh?X-Plex-Token=%s' %(r('server_url'),metadata_id,r('server_token'))
   data=K(url).text
   return v
  except g as e:
   X('Exception:%s',e)
   X(C())
  return L
 @a
 def os_path_exists(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/os_path_exists?filepath=%s&X-Plex-Token=%s'%(r('server_url'),D(filepath.encode('utf8')),r('server_token'))
   data=P(url).text
   return(data=='True')
  except g as e:
   X('Exception:%s',e)
   X(C())
  return L
 @a
 def find_by_filename_part(keyword):
  try:
   query="SELECT metadata_items.id, media_items.id, file, media_items.duration, media_items.bitrate, media_parts.created_at, media_items.size, media_items.width, media_items.height, media_items.video_codec, media_items.audio_codec FROM media_parts, media_items, metadata_items WHERE media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and LOWER(media_parts.file) LIKE '%{keyword}%' and media_items.width > 0 ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(r('server_url'),D(query.encode('utf8')),r('server_token'))
   data1=P(url).json()
   query="SELECT metadata_items.id, media_items.id, file, media_streams.url FROM media_parts, media_items, metadata_items, media_streams WHERE media_streams.media_item_id = media_items.id and media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and media_streams.stream_type_id = 3 and media_parts.file LIKE '%{keyword}%' ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(r('server_url'),D(query.encode('utf8')),r('server_token'))
   data2=P(url).json()
   ret={'ret':v}
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
    item['duration']=y(tmp[3])
    item['bitrate']=y(tmp[4])
    item['created_at']=tmp[5]
    item['size']=y(tmp[6])
    item['size_str']=W(item['size'],suffix='B')
    item['width']=y(tmp[7])
    item['height']=y(tmp[8])
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
   c(ret)
   return ret
  except g as e:
   X('Exception:%s',e)
   X(C())
  return k
 @a
 def execute_query(query):
  try:
   url='{server}/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query={query}&X-Plex-Token={token}'.format(server=r('server_url'),query=query,token=r('server_token'))
   return P(url).json()
  except g as e:
   X('Exception:%s',e)
   X(C())
  return L
# Created by pyminifier (https://github.com/liftoff/pyminifier)
