import os
S=object
b=staticmethod
A=None
I=True
q=len
y=False
f=Exception
i=int
z=str
m=range
from datetime import datetime,timedelta
u=datetime.now
import traceback
D=traceback.format_exc
import logging
import subprocess
import time
import re
import threading
import json
n=json.loads
import requests
import urllib
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.library import ShowSection
from lxml import etree as ET
w=ET.SubElement
c=ET.tostring
U=ET.ElementTree
O=ET.Element
import lxml
B=lxml.html
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,socketio,py_urllib2
X=py_urllib2.urlopen
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.plugin import logger,package_name
j=logger.error
d=logger.debug
from.model import ModelSetting
H=ModelSetting.get
class LogicM3U(S):
 channel_index=1
 @b
 def make_m3u():
  try:
   from.logic import Logic
   server_url=H('server_url')
   server_token=H('server_token')
   if Logic.server is A:
    Logic.server=PlexServer(server_url,server_token)
   json_info=n(H('tivimate_json'))
   data="#EXTM3U\n"
   root=O('tv')
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
     d(url)
     doc=B.parse(X(url))
     videos=doc.xpath("//video")
     if channel_title=='':
      channel_title=doc.xpath("//mediacontainer")[0].attrib['librarysectiontitle']
     data,root=LogicM3U.make_list(data,root,videos,info,channel_title)
    elif info['type']=='show':
     url='%s/library/metadata/%s/children?X-Plex-Token=%s'%(server_url,info['metadata'],server_token)
     d(url)
     doc=B.parse(X(url))
     seasons=doc.xpath("//directory")
     d(seasons)
     if seasons:
      channel_title=doc.xpath("//mediacontainer")[0].attrib['title2']
      include_parent=I if q(seasons)>1 else y
      for s in seasons:
       d(s.attrib)
       if 'ratingkey' in s.attrib:
        d(s.attrib['ratingkey'])
        url='%s/library/metadata/%s/children?X-Plex-Token=%s'%(server_url,s.attrib['ratingkey'],server_token)
        doc2=B.parse(X(url))
        videos=doc2.xpath("//video")
        data,root=LogicM3U.make_list(data,root,videos,info,channel_title,include_parent=include_parent)
     else:
      channel_title='%s %s'%(doc.xpath("//mediacontainer")[0].attrib['title1'],doc.xpath("//mediacontainer")[0].attrib['title2'])
      videos=doc.xpath("//video")
      data,root=LogicM3U.make_list(data,root,videos,info,channel_title,include_parent=I)
   tree=U(root)
   ret=c(root,pretty_print=I,xml_declaration=I,encoding="utf-8")
   return data,ret
  except f as e:
   j('Exception:%s',e)
   j(D()) 
 @b
 def make_list(data,root,videos,info,channel_title,include_parent=y):
  server_url=H('server_url')
  server_token=H('server_token')
  current_count=0
  for tag_video in videos:
   channel_tag=A
   program_tag=A
   try:
    tmp=tag_video.xpath('.//media')
    if tmp:
     tag_media=tmp[0]
    else:
     d('continue1')
     continue
    tag_part=tag_media.xpath('.//part')[0]
    if 'duration' not in tag_media.attrib:
     d('continue3')
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
    duration=i(tag_media.attrib['duration'])
    video_url='%s%s?X-Plex-Token=%s&dummy=/series/'%(server_url,tag_part.attrib['key'],server_token)
    icon_url='%s%s?X-Plex-Token=%s'%(server_url,tag_video.attrib['thumb'],server_token)
    tmp='#EXTINF:-1 tvg-id="{channel_number}" tvg-name="{channel_title}" tvh-chno="{channel_number}" tvg-logo="{logo}" group-title="{channel_title}",{title}\n{url}\n'
    data+=tmp.format(channel_title=channel_title,channel_number=LogicM3U.channel_index,logo=icon_url,url=video_url,title=title)
    channel_tag=w(root,'channel')
    channel_tag.set('id',z(LogicM3U.channel_index))
    channel_tag.set('repeat-programs','true')
    display_name_tag=w(channel_tag,'display-name')
    display_name_tag.text='%s(%s)'%(channel_title,LogicM3U.channel_index)
    display_name_tag=w(channel_tag,'display-number')
    display_name_tag.text=z(LogicM3U.channel_index)
    datetime_start=u()
    for i in m(3):
     datetime_stop=datetime_start+timedelta(seconds=duration/1000+1)
     program_tag=w(root,'programme')
     program_tag.set('start',datetime_start.strftime('%Y%m%d%H%M%S')+' +0900')
     program_tag.set('stop',datetime_stop.strftime('%Y%m%d%H%M%S')+' +0900')
     program_tag.set('channel',z(LogicM3U.channel_index))
     datetime_start=datetime_stop
     title_tag=w(program_tag,'title')
     title_tag.set('lang','ko')
     title_tag.text=title
     icon_tag=w(program_tag,'icon')
     icon_tag.set('src',icon_url)
     if 'summary' in tag_video.attrib:
      desc_tag=w(program_tag,'desc')
      desc_tag.set('lang','ko')
      desc_tag.text=tag_video.attrib['summary']
    channel_tag=A
    program_tag=A
    LogicM3U.channel_index+=1
    current_count+=1
    if 'count' in info and current_count>info['count']:
     break
   except f as e:
    j('Exception:%s',e)
    j(D())
    if channel_tag is not A:
     root.remove(channel_tag)
    if program_tag is not A:
     root.remove(channel_tag)
  return data,root
# Created by pyminifier (https://github.com/liftoff/pyminifier)
