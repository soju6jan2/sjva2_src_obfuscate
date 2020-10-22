import os
S=object
A=None
b=staticmethod
q=len
f=Exception
y=False
i=int
I=True
import traceback
D=traceback.format_exc
import time
import shutil
import re
import requests
s=requests.put
x=requests.get
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.library import ShowSection
from framework import app,db,scheduler,path_app_root,celery,py_urllib
F=py_urllib.quote
from framework.job import Job
from framework.util import Util
K=Util.sizeof_fmt
from.plugin import logger,package_name
j=logger.error
d=logger.debug
from.model import ModelSetting
H=ModelSetting.get
class LogicNormal(S):
 server_instance=A
 @b
 def get_section_id_by_filepath(filepath):
  try:
   if LogicNormal.server_instance is A:
    LogicNormal.server_instance=PlexServer(H('server_url'),H('server_token'))
   if LogicNormal.server_instance is A:
    return
   sections=LogicNormal.server_instance.library.sections()
   tmp_len=0
   tmp_section_id=-1
   for section in sections:
    for location in section.locations:
     if filepath.find(location)!=-1:
      if q(location)>tmp_len:
       tmp_len=q(location)
       tmp_section_id=section.key
   d('PLEX get_section_id_by_filepath %s:%s',tmp_section_id,filepath)
   return tmp_section_id
  except f as e:
   j('Exception:%s',e)
   j(D()) 
  return-1
 @b
 def is_exist_in_library_using_bundle(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/count_in_library?filename=%s&X-Plex-Token=%s'%(H('server_url'),F(filepath.encode('utf8')),H('server_token'))
   data=x(url).text
   if data=='0':
    return y
   else:
    try:
     tmp=i(data)
     if tmp>0:
      return I
    except:
     return y
  except f as e:
   j('Exception:%s',e)
   j(D())
   return y
 @b
 def get_library_key_using_bundle(filepath,section_id=-1):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_metadata_id_by_filepath&args=%s&X-Plex-Token=%s'%(H('server_url'),F(filepath.encode('utf8')),H('server_token'))
   data=x(url).text
   return data
  except f as e:
   j('Exception:%s',e)
   j(D())
 @b
 def get_filepath_list_by_metadata_id_using_bundle(metadata_id):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_handle?action=get_filepath_list_by_metadata_id&args=%s&X-Plex-Token=%s'%(H('server_url'),metadata_id,H('server_token'))
   data=x(url).text
   ret=[x.strip()for x in data.split('\n')]
   return ret
  except f as e:
   j('Exception:%s',e)
   j(D())
 @b
 def metadata_refresh(filepath=A,metadata_id=A):
  try:
   if metadata_id is A:
    if filepath is not A:
     metadata_id=LogicNormal.get_library_key_using_bundle(filepath)
   if metadata_id is A:
    return y 
   url='%s/library/metadata/%s/refresh?X-Plex-Token=%s' %(H('server_url'),metadata_id,H('server_token'))
   data=s(url).text
   return I
  except f as e:
   j('Exception:%s',e)
   j(D())
  return y
 @b
 def os_path_exists(filepath):
  try:
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/os_path_exists?filepath=%s&X-Plex-Token=%s'%(H('server_url'),F(filepath.encode('utf8')),H('server_token'))
   data=x(url).text
   return(data=='True')
  except f as e:
   j('Exception:%s',e)
   j(D())
  return y
 @b
 def find_by_filename_part(keyword):
  try:
   query="SELECT metadata_items.id, media_items.id, file, media_items.duration, media_items.bitrate, media_parts.created_at, media_items.size, media_items.width, media_items.height, media_items.video_codec, media_items.audio_codec FROM media_parts, media_items, metadata_items WHERE media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and LOWER(media_parts.file) LIKE '%{keyword}%' and media_items.width > 0 ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(H('server_url'),F(query.encode('utf8')),H('server_token'))
   data1=x(url).json()
   query="SELECT metadata_items.id, media_items.id, file, media_streams.url FROM media_parts, media_items, metadata_items, media_streams WHERE media_streams.media_item_id = media_items.id and media_parts.media_item_id = media_items.id and media_items.metadata_item_id = metadata_items.id and media_streams.stream_type_id = 3 and media_parts.file LIKE '%{keyword}%' ORDER BY media_items.bitrate DESC".format(keyword=keyword)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query=%s&X-Plex-Token=%s'%(H('server_url'),F(query.encode('utf8')),H('server_token'))
   data2=x(url).json()
   ret={'ret':I}
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
    item['duration']=i(tmp[3])
    item['bitrate']=i(tmp[4])
    item['created_at']=tmp[5]
    item['size']=i(tmp[6])
    item['size_str']=K(item['size'],suffix='B')
    item['width']=i(tmp[7])
    item['height']=i(tmp[8])
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
   d(ret)
   return ret
  except f as e:
   j('Exception:%s',e)
   j(D())
  return A
 @b
 def execute_query(query):
  try:
   url='{server}/:/plugins/com.plexapp.plugins.SJVA/function/db_query?query={query}&X-Plex-Token={token}'.format(server=H('server_url'),query=query,token=H('server_token'))
   return x(url).json()
  except f as e:
   j('Exception:%s',e)
   j(D())
  return y
# Created by pyminifier (https://github.com/liftoff/pyminifier)
