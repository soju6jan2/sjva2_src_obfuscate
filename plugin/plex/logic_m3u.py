import os
O=object
P=staticmethod
q=None
m=True
N=len
f=False
V=Exception
C=int
G=str
j=range
from datetime import datetime,timedelta
import traceback
import logging
import subprocess
import time
import re
import threading
import json
import requests
import urllib
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.library import ShowSection
from lxml import etree as ET
import lxml
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,socketio,py_urllib2
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.plugin import logger,package_name
from.model import ModelSetting
class LogicM3U(O):
 channel_index=1
 @P
 def make_m3u():
  try:
   from.logic import Logic
   server_url=ModelSetting.get('server_url')
   server_token=ModelSetting.get('server_token')
   if Logic.server is q:
    Logic.server=PlexServer(server_url,server_token)
   json_info=json.loads(ModelSetting.get('tivimate_json'))
   data="#EXTM3U\n"
   root=ET.Element('tv')
   root.set('generator-info-name',"plex")
   LogicM3U.channel_index=1
   for info in json_info:
    if info['type']=='recent_add':
     if info['section']=='episode':
      url='%s/hubs/home/recentlyAdded?type=2&X-Plex-Token=%s'%(server_url,server_token)
      channel_title=u'최신TV'
     elif info['section']=='movie':
      url='%s/hubs/home/recentlyAdded?type=1&X-Plex-Token=%s'%(server_url,server_token)
      channel_title=u'최신영화'
     else:
      url='%s/library/sections/%s/recentlyAdded?X-Plex-Token=%s'%(server_url,info['section'],server_token)
      channel_title=u''
     logger.debug(url)
     doc=lxml.html.parse(py_urllib2.urlopen(url))
     videos=doc.xpath("//video")
     if channel_title=='':
      channel_title=doc.xpath("//mediacontainer")[0].attrib['librarysectiontitle']
     data,root=LogicM3U.make_list(data,root,videos,info,channel_title)
    elif info['type']=='show':
     url='%s/library/metadata/%s/children?X-Plex-Token=%s'%(server_url,info['metadata'],server_token)
     logger.debug(url)
     doc=lxml.html.parse(py_urllib2.urlopen(url))
     seasons=doc.xpath("//directory")
     logger.debug(seasons)
     if seasons:
      channel_title=doc.xpath("//mediacontainer")[0].attrib['title2']
      include_parent=m if N(seasons)>1 else f
      for s in seasons:
       logger.debug(s.attrib)
       if 'ratingkey' in s.attrib:
        logger.debug(s.attrib['ratingkey'])
        url='%s/library/metadata/%s/children?X-Plex-Token=%s'%(server_url,s.attrib['ratingkey'],server_token)
        doc2=lxml.html.parse(py_urllib2.urlopen(url))
        videos=doc2.xpath("//video")
        data,root=LogicM3U.make_list(data,root,videos,info,channel_title,include_parent=include_parent)
     else:
      channel_title='%s %s'%(doc.xpath("//mediacontainer")[0].attrib['title1'],doc.xpath("//mediacontainer")[0].attrib['title2'])
      videos=doc.xpath("//video")
      data,root=LogicM3U.make_list(data,root,videos,info,channel_title,include_parent=m)
   tree=ET.ElementTree(root)
   ret=ET.tostring(root,pretty_print=m,xml_declaration=m,encoding="utf-8")
   return data,ret
  except V as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @P
 def make_list(data,root,videos,info,channel_title,include_parent=f):
  server_url=ModelSetting.get('server_url')
  server_token=ModelSetting.get('server_token')
  current_count=0
  for tag_video in videos:
   channel_tag=q
   program_tag=q
   try:
    tmp=tag_video.xpath('.//media')
    if tmp:
     tag_media=tmp[0]
    else:
     logger.debug('continue1')
     continue
    tag_part=tag_media.xpath('.//part')[0]
    if 'duration' not in tag_media.attrib:
     logger.debug('continue3')
     continue
    if tag_video.attrib['type']=='movie':
     title=tag_video.attrib['title']
    elif tag_video.attrib['type']=='episode':
     if 'index' in tag_video.attrib:
      title=u'%s %s (%s회)'%(tag_video.attrib['grandparenttitle'],(tag_video.attrib['parenttitle']if include_parent else ''),tag_video.attrib['index'])
     else:
      title=u'%s %s (%s)'%(tag_video.attrib['grandparenttitle'],(tag_video.attrib['parenttitle']if include_parent else ''),tag_video.attrib['title'])
    elif tag_video.attrib['type']=='clip':
     title=u'%s'%tag_video.attrib['title']
    title=title.replace('  ',' ')
    duration=C(tag_media.attrib['duration'])
    video_url='%s%s?X-Plex-Token=%s&dummy=/series/'%(server_url,tag_part.attrib['key'],server_token)
    icon_url='%s%s?X-Plex-Token=%s'%(server_url,tag_video.attrib['thumb'],server_token)
    tmp='#EXTINF:-1 tvg-id="{channel_number}" tvg-name="{channel_title}" tvh-chno="{channel_number}" tvg-logo="{logo}" group-title="{channel_title}",{title}\n{url}\n'
    data+=tmp.format(channel_title=channel_title,channel_number=LogicM3U.channel_index,logo=icon_url,url=video_url,title=title)
    channel_tag=ET.SubElement(root,'channel')
    channel_tag.set('id',G(LogicM3U.channel_index))
    channel_tag.set('repeat-programs','true')
    display_name_tag=ET.SubElement(channel_tag,'display-name')
    display_name_tag.text='%s(%s)'%(channel_title,LogicM3U.channel_index)
    display_name_tag=ET.SubElement(channel_tag,'display-number')
    display_name_tag.text=G(LogicM3U.channel_index)
    datetime_start=datetime.now()
    for i in j(3):
     datetime_stop=datetime_start+timedelta(seconds=duration/1000+1)
     program_tag=ET.SubElement(root,'programme')
     program_tag.set('start',datetime_start.strftime('%Y%m%d%H%M%S')+' +0900')
     program_tag.set('stop',datetime_stop.strftime('%Y%m%d%H%M%S')+' +0900')
     program_tag.set('channel',G(LogicM3U.channel_index))
     datetime_start=datetime_stop
     title_tag=ET.SubElement(program_tag,'title')
     title_tag.set('lang','ko')
     title_tag.text=title
     icon_tag=ET.SubElement(program_tag,'icon')
     icon_tag.set('src',icon_url)
     if 'summary' in tag_video.attrib:
      desc_tag=ET.SubElement(program_tag,'desc')
      desc_tag.set('lang','ko')
      desc_tag.text=tag_video.attrib['summary']
    channel_tag=q
    program_tag=q
    LogicM3U.channel_index+=1
    current_count+=1
    if 'count' in info and current_count>info['count']:
     break
   except V as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
    if channel_tag is not q:
     root.remove(channel_tag)
    if program_tag is not q:
     root.remove(channel_tag)
  return data,root
# Created by pyminifier (https://github.com/liftoff/pyminifier)
