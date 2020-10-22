import os
j=object
a=staticmethod
k=None
v=True
M=len
L=False
g=Exception
y=int
E=str
H=range
from datetime import datetime,timedelta
x=datetime.now
import traceback
C=traceback.format_exc
import logging
import subprocess
import time
import re
import threading
import json
J=json.loads
import requests
import urllib
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.library import ShowSection
from lxml import etree as ET
h=ET.SubElement
I=ET.tostring
t=ET.ElementTree
w=ET.Element
import lxml
q=lxml.html
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,socketio,py_urllib2
n=py_urllib2.urlopen
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from.plugin import logger,package_name
X=logger.error
c=logger.debug
from.model import ModelSetting
r=ModelSetting.get
class LogicM3U(j):
 channel_index=1
 @a
 def make_m3u():
  try:
   from.logic import Logic
   server_url=r('server_url')
   server_token=r('server_token')
   if Logic.server is k:
    Logic.server=PlexServer(server_url,server_token)
   json_info=J(r('tivimate_json'))
   data="#EXTM3U\n"
   root=w('tv')
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
     c(url)
     doc=q.parse(n(url))
     videos=doc.xpath("//video")
     if channel_title=='':
      channel_title=doc.xpath("//mediacontainer")[0].attrib['librarysectiontitle']
     data,root=LogicM3U.make_list(data,root,videos,info,channel_title)
    elif info['type']=='show':
     url='%s/library/metadata/%s/children?X-Plex-Token=%s'%(server_url,info['metadata'],server_token)
     c(url)
     doc=q.parse(n(url))
     seasons=doc.xpath("//directory")
     c(seasons)
     if seasons:
      channel_title=doc.xpath("//mediacontainer")[0].attrib['title2']
      include_parent=v if M(seasons)>1 else L
      for s in seasons:
       c(s.attrib)
       if 'ratingkey' in s.attrib:
        c(s.attrib['ratingkey'])
        url='%s/library/metadata/%s/children?X-Plex-Token=%s'%(server_url,s.attrib['ratingkey'],server_token)
        doc2=q.parse(n(url))
        videos=doc2.xpath("//video")
        data,root=LogicM3U.make_list(data,root,videos,info,channel_title,include_parent=include_parent)
     else:
      channel_title='%s %s'%(doc.xpath("//mediacontainer")[0].attrib['title1'],doc.xpath("//mediacontainer")[0].attrib['title2'])
      videos=doc.xpath("//video")
      data,root=LogicM3U.make_list(data,root,videos,info,channel_title,include_parent=v)
   tree=t(root)
   ret=I(root,pretty_print=v,xml_declaration=v,encoding="utf-8")
   return data,ret
  except g as e:
   X('Exception:%s',e)
   X(C()) 
 @a
 def make_list(data,root,videos,info,channel_title,include_parent=L):
  server_url=r('server_url')
  server_token=r('server_token')
  current_count=0
  for tag_video in videos:
   channel_tag=k
   program_tag=k
   try:
    tmp=tag_video.xpath('.//media')
    if tmp:
     tag_media=tmp[0]
    else:
     c('continue1')
     continue
    tag_part=tag_media.xpath('.//part')[0]
    if 'duration' not in tag_media.attrib:
     c('continue3')
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
    duration=y(tag_media.attrib['duration'])
    video_url='%s%s?X-Plex-Token=%s&dummy=/series/'%(server_url,tag_part.attrib['key'],server_token)
    icon_url='%s%s?X-Plex-Token=%s'%(server_url,tag_video.attrib['thumb'],server_token)
    tmp='#EXTINF:-1 tvg-id="{channel_number}" tvg-name="{channel_title}" tvh-chno="{channel_number}" tvg-logo="{logo}" group-title="{channel_title}",{title}\n{url}\n'
    data+=tmp.format(channel_title=channel_title,channel_number=LogicM3U.channel_index,logo=icon_url,url=video_url,title=title)
    channel_tag=h(root,'channel')
    channel_tag.set('id',E(LogicM3U.channel_index))
    channel_tag.set('repeat-programs','true')
    display_name_tag=h(channel_tag,'display-name')
    display_name_tag.text='%s(%s)'%(channel_title,LogicM3U.channel_index)
    display_name_tag=h(channel_tag,'display-number')
    display_name_tag.text=E(LogicM3U.channel_index)
    datetime_start=x()
    for i in H(3):
     datetime_stop=datetime_start+timedelta(seconds=duration/1000+1)
     program_tag=h(root,'programme')
     program_tag.set('start',datetime_start.strftime('%Y%m%d%H%M%S')+' +0900')
     program_tag.set('stop',datetime_stop.strftime('%Y%m%d%H%M%S')+' +0900')
     program_tag.set('channel',E(LogicM3U.channel_index))
     datetime_start=datetime_stop
     title_tag=h(program_tag,'title')
     title_tag.set('lang','ko')
     title_tag.text=title
     icon_tag=h(program_tag,'icon')
     icon_tag.set('src',icon_url)
     if 'summary' in tag_video.attrib:
      desc_tag=h(program_tag,'desc')
      desc_tag.set('lang','ko')
      desc_tag.text=tag_video.attrib['summary']
    channel_tag=k
    program_tag=k
    LogicM3U.channel_index+=1
    current_count+=1
    if 'count' in info and current_count>info['count']:
     break
   except g as e:
    X('Exception:%s',e)
    X(C())
    if channel_tag is not k:
     root.remove(channel_tag)
    if program_tag is not k:
     root.remove(channel_tag)
  return data,root
# Created by pyminifier (https://github.com/liftoff/pyminifier)
