import os
P=object
x=None
q=staticmethod
m=Exception
p=False
W=True
o=type
H=len
B=int
L=enumerate
U=sorted
u=range
E=str
from datetime import datetime,timedelta
import traceback
import logging
import subprocess
import time
import re
import threading
import json
import requests
from sqlalchemy import desc
from sqlalchemy import or_,and_,func,not_
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.library import ShowSection
from lxml import etree as ET
import lxml
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,socketio,SystemModelSetting,py_urllib2,py_urllib
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic
from framework.common.daum import DaumTV
from.model import ModelSetting
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Logic(P):
 db_default={'id':'','pw':'','server_name':'','server_url':'','server_token':'','download_path':'','machineIdentifier':'','scan_server':'','use_lc':'True','lc_json':'[{"type":"recent_add","section":"episode","count":40,"start_number":999,"reverse":true},{"type":"recent_add","section":"movie","count":40,"start_number":959,"reverse":true}]','tivimate_json':'[{"type":"recent_add","section":"episode","count":50},{"type":"recent_add","section":"movie","count":50}]'}
 account=x 
 server=x 
 """
    [{"type" : "recent_add", "section" : "episode", "count" : 40, "start_number" : 999, "reverse" : true }, {"type" : "recent_add", "section" : "movie", "count" : 40, "start_number" : 959, "reverse" : true }, {"type" : "section_to_channel", "section" : "0", "include_content_count" : 10, "channel_number" : 899, } ]
    """ 
 @q
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     db.session.add(ModelSetting(key,value))
   db.session.commit()
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @q
 def plugin_load():
  try:
   Logic.db_init()
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @q
 def plugin_unload():
  try:
   pass
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @q
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    if key in['lc_json','tivimate_json']:
     value=value.strip()
     value=value.replace('\r','')
     value=value.replace('\n','')
     value=value.replace(' ','')
     try:
      json.loads(value)
     except:
      logger.debug('Wrong JSON!')
      return p
    entity.value=value
   db.session.commit()
   return W 
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return p
 @q
 def get_setting_value(key):
  try:
   return db.session.query(ModelSetting).filter_by(key=key).first().value
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @q
 def get_plex_server_list(req):
  try:
   plex_id=req.form['id']
   plex_pw=req.form['pw']
   logger.debug('get_plex_server_list: %s, %s',plex_id,plex_pw)
   try:
    Logic.account=MyPlexAccount(plex_id,plex_pw)
   except BadRequest:
    logger.debug('login fail!!')
    return x
   devices=Logic.account.devices()
   ret=[]
   for device in devices:
    if 'server' in device.provides:
     logger.debug('type :%s',o(device))
     logger.debug('server : %s',device)
     ret.append(device.name)
   return ret
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @q
 def get_server_hash():
  return db.session.query(ModelSetting).filter_by(key='machineIdentifier').first().value
 @q
 def connect_plex_server_by_name(req):
  try:
   server_name=req.form['server_name']
   if Logic.account is x:
    return 'need_login'
   devices=Logic.account.devices()
   ret=[]
   for device in devices:
    if 'server' in device.provides:
     if server_name==device.name:
      server=device.connect()
      return[server._baseurl,server._token,server.machineIdentifier]
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return 'fail'
 @q
 def connect_plex_server_by_url(req):
  try:
   server_url=req.form['server_url']
   server_token=req.form['server_token']
   plex=PlexServer(server_url,server_token)
   sections=plex.library.sections()
   return H(sections)
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return 'fail'
 @q
 def get_sjva_plugin_version(req):
  try:
   server_url=req.form['server_url']
   server_token=req.form['server_token']
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/version?X-Plex-Token=%s'%(server_url,server_token)
   logger.debug(url)
   page=requests.get(url)
   return page.text
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return 'fail'
 @q
 def get_sj_daum_version(req):
  try:
   server_url=req.form['server_url']
   server_token=req.form['server_token']
   url='%s/:/plugins/com.plexapp.agents.sj_daum/function/version?X-Plex-Token=%s'%(server_url,server_token)
   logger.debug(url)
   page=requests.get(url)
   return page.text
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return 'fail'
 @q
 def get_section_id(entity,more=p):
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if Logic.server is x:
    Logic.server=PlexServer(server_url,server_token)
   logger.debug('get_section_id : %s',entity.plex_abspath)
   sections=Logic.server.library.sections()
   select_section=x
   for section in sections:
    if section.o=='show':
     for location in section.locations:
      if entity.plex_abspath.find(location)!=-1:
       logger.debug('Find Section section:%s location:%s id:%s',section.title,location,section.key)
       entity.plex_section_id=section.key
       select_section=section
       break
   if select_section is not x:
    for show in select_section.all():
     for location in show.locations:
      if entity.plex_abspath.find(location)!=-1:
       entity.plex_show_id=show.ratingKey
       match=re.compile(r'\/\/(?P<id>\d+)?').search(show.guid)
       entity.plex_daum_id=match.group('id')
       entity.plex_title=show.title
       entity.plex_image=show.thumbUrl
       logger.debug('Find Show:%s daum:%s',entity.plex_show_id,entity.plex_daum_id)
       if more:
        for episode in show.episodes():
         for location in episode.locations:
          if location==entity.plex_abspath:
           for part in episode.media[0].parts:
            if part.file==location:
             logger.debug('KEY :%s',part.key)
             entity.plex_part='%s%s?X-Plex-Token=%s'%(server_url,part.key,server_token)
             return entity.plex_section_id
   return-1
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @q
 def exist_file_in_library(entity):
  sections=Logic.server.library.sections()
  for section in sections:
   if section.o=='show' and B(section.key)==entity.plex_section_id:
    for show in section.all():
     if show.ratingKey==entity.plex_show_id:
      ret=p
      for episode in show.episodes():
       for location in episode.locations:
        if location==entity.plex_abspath:
         ret=W
         return ret
      return ret
  return x
 @q
 def send_scan_command(modelfile,plugin_name):
  entity=modelfile
  logger.debug('send_scan_command')
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if server_url=='':
    logger.debug('server_url is empty!')
    return
   callback_url='%s/%s/api/scan_completed'%(SystemModelSetting.get('ddns'),plugin_name)
   filename=entity.plex_abspath if entity.plex_abspath is not x else os.path.join(entity.scan_abspath,entity.filename)
   logger.debug('send_scan_command PATH:%s ID:%s',entity.plex_abspath,entity.plex_section_id)
   encode_filename=Logic.get_filename_encoding_for_plex(filename)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/WaitFile?section_id=%s&filename=%s&callback=%s&callback_id=%s&type_add_remove=ADD&call_from=FILE_MANAGER&X-Plex-Token=%s'%(server_url,entity.plex_section_id,encode_filename,py_urllib.quote(callback_url),entity.id,server_token)
   logger.debug('URL:%s',url)
   request=py_urllib2.Request(url)
   response=py_urllib2.urlopen(request)
   data=response.read()
   logger.debug(url)
   logger.debug('_send_scan_command ret:%s',data)
   entity.send_command_time=datetime.now()
   scan_server=db.session.query(ModelSetting).filter_by(key='scan_server').first().value
   if scan_server!='':
    servers=scan_server.split(',')
    for s in servers:
     try:
      s=s.strip()
      s_url,s_token=s.split('&')
      url='%s/:/plugins/com.plexapp.plugins.SJVA/function/WaitFile?section_id=&filename=%s&callback=&callback_id=&type_add_remove=ADD&call_from=FILE_MANAGER&X-Plex-Token=%s'%(s_url.strip(),encode_filename,s_token.strip())
      request=py_urllib2.Request(url)
      response=py_urllib2.urlopen(request)
      data=response.read()
      logger.debug(url)
      logger.debug('scan_server : %s ret:%s',s_url,data)
     except m as e:
      logger.debug('Exception:%s',e)
      logger.debug(traceback.format_exc()) 
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @q
 def get_section_id_by_file(filepath):
  try:
   if Logic.server is x:
    server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
    server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
    Logic.server=PlexServer(server_url,server_token)
   logger.debug('get_section_id : %s',filepath)
   sections=Logic.server.library.sections()
   select_section=x
   tmp_len=0
   tmp_section_id=-1
   for section in sections:
    for location in section.locations:
     if filepath.find(location)!=-1:
      if H(location)>tmp_len:
       tmp_len=H(location)
       tmp_section_id=section.key
   return tmp_section_id
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @q
 def is_exist_in_library(filename):
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if server_url=='' or server_token=='':
    return W
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/count_in_library?filename=%s&X-Plex-Token=%s'%(server_url,Logic.get_filename_encoding_for_plex(filename),server_token)
   logger.debug('URL:%s',url)
   request=py_urllib2.Request(url)
   response=py_urllib2.urlopen(request)
   data=response.read()
   logger.debug('is_exist_in_library ret:%s',data)
   if data=='0':
    return p
   else:
    try:
     tmp=B(data)
     if tmp>0:
      return W
    except:
     return p
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   return p
 @q
 def get_filename_encoding_for_plex(filename):
  try:
   ret=filename.encode('utf8')
  except m as e:
   logger.error('Exception1:%s',e)
   try:
    ret=filename.encode('utf8')
   except m as e:
    logger.error('Exception3:%s',e)
  return py_urllib.quote(ret)
 @q
 def send_scan_command2(plugin_name,section_id,filename,callback_id,type_add_remove,call_from):
  logger.debug('send_scan_command2')
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   callback_url='%s/%s/api/scan_completed'%(SystemModelSetting.get('ddns'),plugin_name)
   logger.debug('send_scan_command PATH:%s ID:%s',filename,section_id)
   encode_filename=Logic.get_filename_encoding_for_plex(filename)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/WaitFile?section_id=%s&filename=%s&callback=%s&callback_id=%s&type_add_remove=%s&call_from=%s&X-Plex-Token=%s'%(server_url,section_id,encode_filename,py_urllib.quote(callback_url),callback_id,type_add_remove,call_from,server_token)
   logger.debug('URL:%s',url)
   request=py_urllib2.Request(url)
   response=py_urllib2.urlopen(request)
   data=response.read()
   logger.debug('_send_scan_command ret:%s',data)
   scan_server=db.session.query(ModelSetting).filter_by(key='scan_server').first().value
   if scan_server!='':
    servers=scan_server.split(',')
    for s in servers:
     try:
      s=s.strip()
      s_url,s_token=s.split('&')
      url='%s/:/plugins/com.plexapp.plugins.SJVA/function/WaitFile?section_id=&filename=%s&callback=&callback_id=&type_add_remove=%s&call_from=%s&X-Plex-Token=%s'%(s_url.strip(),encode_filename,type_add_remove,call_from,s_token.strip())
      request=py_urllib2.Request(url)
      response=py_urllib2.urlopen(request)
      s_data=response.read()
      logger.debug('scan_server2 : %s ret:%s',s_url,s_data)
     except m as e:
      logger.debug('Exception:%s',e)
      logger.debug(traceback.format_exc()) 
   return data
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 analyze_show_data=x
 @q
 def analyze_show(key):
  try:
   Logic.analyze_show_data=[]
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if Logic.server is x:
    Logic.server=PlexServer(server_url,server_token)
   sections=Logic.server.library.sections()
   for section in sections:
    if section.o!='show':
     continue
    if section.key!=key:
     continue
    for index,show in L(section.all()):
     try:
      flag_media_season=p
      if H(show.seasons())>1:
       for season in show.seasons():
        if B(season.index)>1 and B(season.index)<1900:
         flag_media_season=W
         break
      if flag_media_season:
       season_data=DaumTV.get_show_info_on_home(DaumTV.get_show_info_on_home_title(show.title))
      item={}
      item['section']=section.title
      item['title']=show.title
      item['show_key']=show.key
      item['seasons']=[]
      item['guid']=show.guid
      for season in show.seasons():
       if season.index==0:
        continue
       season_entity={}
       season_entity['daum_info']=x
       if item['guid'].lower().find('daum'):
        tmp=x
        if flag_media_season and season_data is not x and H(season_data['series'])>1:
         search_title=season_data['series'][B(season.index)-1]['title']
         search_id=season_data['series'][B(season.index)-1]['id']
         tmp=DaumTV.get_daum_tv_info(search_title,daum_id=search_id,on_home=W)
        else:
         tmp=DaumTV.get_daum_tv_info(show.title,on_home=W)
        if tmp:
         season_entity['daum_info']=tmp
       season_entity['poster']=season.thumbUrl
       season_entity['season_key']=season.key
       episodes=season.episodes()
       season_entity['season_number']=season.index
       season_entity['episode_count']=H(episodes)
       season_entity['episode_index_list']=[]
       season_entity['episode_air_list']=[]
       season_entity['duplicate_list']=[]
       season_entity['episodes']={}
       flag_originallyAvailableAt=p
       flag_index=p
       epi_min=x
       epi_max=x
       epi_count_index=0
       epi_count_date=0
       for episode in episodes:
        episode_key=x
        if episode.index is x:
         episode_key=episode.originallyAvailableAt.strftime('%Y-%m-%d')
         flag_originallyAvailableAt=W
         season_entity['episode_air_list'].append(episode_key)
         epi_count_date+=1
        else:
         episode_key=episode.index
         flag_index=W
         if epi_min is x or epi_min>B(episode.index):
          epi_min=B(episode.index)
         if epi_max is x or epi_max<B(episode.index):
          epi_max=B(episode.index)
         season_entity['episode_index_list'].append(B(episode.index))
         epi_count_index+=1
        season_entity['episodes'][episode_key]=[]
        for part in episode.iterParts():
         part_entity={}
         part_entity['file']=part.file
         part_entity['part']='%s%s?X-Plex-Token=%s'%(server_url,part.key,server_token)
         season_entity['episodes'][episode_key].append(part_entity)
        if H(season_entity['episodes'][episode_key])>1:
         season_entity['duplicate_list'].append(episode_key)
       season_entity['flag_originallyAvailableAt']=flag_originallyAvailableAt
       season_entity['flag_index']=flag_index
       season_entity['episode_index_list']=U(season_entity['episode_index_list'])
       season_entity['episode_air_list']=U(season_entity['episode_air_list'])
       season_entity['duplicate_list']=U(season_entity['duplicate_list'])
       season_entity['epi_min']=epi_min
       season_entity['epi_max']=epi_max
       season_entity['epi_count_index']=epi_count_index
       season_entity['epi_count_date']=epi_count_date
       status=-1
       one_file_how_many_episodes=1
       msg=''
       if season_entity['daum_info']is not x:
        if season_entity['daum_info']['episode_count_one_day']>1:
         one_file_how_many_episodes=2
       if flag_index:
        if one_file_how_many_episodes==1:
         if epi_max-epi_min+1==epi_count_index:
          status=0
          msg='비어 있는 에피소드 없음'
         elif epi_max-epi_min+1>epi_count_index:
          status=1
          msg='비어 있는 에피소드 있음'
          empty_episode_no=[]
          for idx in u(season_entity['episode_index_list'][0],season_entity['episode_index_list'][-1],1):
           if idx not in season_entity['episode_index_list']:
            empty_episode_no.append(idx)
          season_entity['empty_episode_no']=empty_episode_no
        else:
         if(epi_max-epi_min)/one_file_how_many_episodes+1==epi_count_index:
          status=one_file_how_many_episodes
          msg='비어 있는 에피소드 없음'
         elif(epi_max-epi_min)/2+1>epi_count_index:
          status=3
          msg='비어 있는 에피소드 있음'
          empty_episode_no=[]
          for idx in u(season_entity['episode_index_list'][0],season_entity['episode_index_list'][-1],one_file_how_many_episodes):
           if idx not in season_entity['episode_index_list']:
            empty_episode_no.append(idx)
          season_entity['empty_episode_no']=empty_episode_no
         else:
          status=9
          msg='예상 보다 에피소드가 더 있음(1일 2회 방송인데 짝수 회차 파일)'
        if flag_originallyAvailableAt:
         status+=4
         msg+='<br>회차 없이 날짜만 있는 에피소드 있음'
        if season_entity['daum_info']is not x and season_entity['daum_info']['last_episode_no']is not x:
         if one_file_how_many_episodes==1:
          msg+='<br>마지막 회차 - PLEX:%s, DAUM:%s.'%(epi_max,season_entity['daum_info']['last_episode_no'])
         else:
          msg+='<br>마지막 회차 - PLEX:%s, DAUM:%s.'%(epi_max,B(season_entity['daum_info']['last_episode_no'])-1)
         if E(epi_max)==season_entity['daum_info']['last_episode_no']:
          msg+=' 일치'
         elif one_file_how_many_episodes==2 and E(epi_max+1)==season_entity['daum_info']['last_episode_no']:
          msg+=' 일치'
         else:
          msg+=' <strong><span style="color: red">불일치 (%s)</span></strong>'%season_entity['daum_info']['last_episode_date']
       else:
        status=8
        msg='전체 날짜 에피소드'
       season_entity['status']=status
       season_entity['msg']=msg
       logger.debug('one_file_how_many_episodes %s %s %s %s %s %s',one_file_how_many_episodes,show.title,flag_index,flag_originallyAvailableAt,status,msg)
       item['seasons'].append(season_entity)
      Logic.analyze_show_data.append(item)
      item['total']=H(section.all())
      item['index']=index
      """
                        noti_data = {'type':'info', 'msg' : u'%s / %s 분석중..' % ((index+1), item['total']), 'url':'/plex/list'}
                        socketio.emit("notify", noti_data, namespace='/framework', broadcast=True)
                        """      
      yield "data: %s\n\n"%json.dumps(item).decode('utf-8')
     except m as e:
      logger.error('Exception:%s',e)
      logger.error(traceback.format_exc()) 
    break
   yield "data: -1\n\n"
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
   yield "data: -1\n\n"
 @q
 def load_section_list():
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if Logic.server is x:
    Logic.server=PlexServer(server_url,server_token)
   sections=Logic.server.library.sections()
   ret=[]
   for section in sections:
    entity={}
    entity['type']=section.o
    entity['key']=section.key
    entity['title']=section.title
    ret.append(entity)
   return ret
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @q
 def library_search_show(title,daum_id):
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if Logic.server is x:
    Logic.server=PlexServer(server_url,server_token)
   ret=[]
   for video in Logic.server.search(title):
    if E(video.TYPE)=='show':
     if video.guid.find(daum_id)!=-1:
      ret.append(video)
   return ret
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @q
 def library_search_movie(title,daum_id):
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if server_url=='' or server_token=='':
    return
   if Logic.server is x:
    Logic.server=PlexServer(server_url,server_token)
   ret=[]
   for video in Logic.server.search(title):
    if E(video.TYPE)=='movie':
     if video.guid.find(daum_id)!=-1:
      ret.append(video)
   return ret
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @q
 def plungin_command(req):
  try:
   command=req.form['cmd']
   param1=req.form['param1']if 'param1' in req.form else ''
   param2=req.form['param2']if 'param2' in req.form else ''
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if param1!='':
    param1=py_urllib.quote(param1)
   url='%s/:/plugins/com.plexapp.plugins.SJVA/function/command?cmd=%s&param1=%s&param2=%s&X-Plex-Token=%s'%(server_url,command,param1,param2,server_token)
   logger.debug('URL:%s',url)
   request=py_urllib2.Request(url)
   response=py_urllib2.urlopen(request)
   data=response.read()
   data=json.loads(data)
   return data
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @q
 def make_xml(root):
  try:
   server_url=db.session.query(ModelSetting).filter_by(key='server_url').first().value
   server_token=db.session.query(ModelSetting).filter_by(key='server_token').first().value
   if Logic.server is x:
    Logic.server=PlexServer(server_url,server_token)
   lc_json=Logic.get_setting_value('lc_json')
   json_info=json.loads(lc_json)
   for info in json_info:
    logger.debug(info)
    if info['type']=='recent_add':
     channel_number=info['start_number']
     max_count=info['count']
     channel_index=1
     channel_step=1
     if info['reverse']:
      channel_step=-1
     if info['section']=='episode':
      url='%s/hubs/home/recentlyAdded?type=2&X-Plex-Token=%s'%(server_url,server_token)
      channel_title=u'최신TV'
     elif info['section']=='movie':
      url='%s/hubs/home/recentlyAdded?type=1&X-Plex-Token=%s'%(server_url,server_token)
      channel_title=u'최신영화'
     else:
      url='%s/hubs/home/recentlyAdded?type=1&sectionID=%s&X-Plex-Token=%s'%(server_url,info['section'],server_token)
      channel_title=u''
     doc=lxml.html.parse(py_urllib2.urlopen(url))
     videos=doc.xpath("//video")
     for tag_video in videos:
      channel_tag=x
      program_tag=x
      try:
       if channel_title=='':
        channel_title=tag_video.attrib['librarysectiontitle']
       tmp=tag_video.xpath('.//media')
       if tmp:
        tag_media=tmp[0]
       else:
        continue
       tag_part=tag_media.xpath('.//part')[0]
       if tag_video.attrib['type']=='movie':
        title=tag_video.attrib['title']
       elif tag_video.attrib['type']=='episode':
        if 'index' in tag_media.attrib:
         title=u'%s회 %s %s'%(tag_video.attrib['index'],tag_video.attrib['grandparenttitle'],tag_video.attrib['title'])
        else:
         title=u'%s %s'%(tag_video.attrib['grandparenttitle'],tag_video.attrib['title'])
       else:
        continue
       if 'duration' not in tag_media.attrib:
        continue
       duration=B(tag_media.attrib['duration'])
       video_url='%s%s?X-Plex-Token=%s'%(server_url,tag_part.attrib['key'],server_token)
       icon_url='%s%s?X-Plex-Token=%s'%(server_url,tag_video.attrib['thumb'],server_token)
       channel_tag=ET.SubElement(root,'channel')
       channel_tag.set('id',E(channel_number))
       channel_tag.set('repeat-programs','true')
       display_name_tag=ET.SubElement(channel_tag,'display-name')
       display_name_tag.text='%s(%s)'%(channel_title,channel_index)
       display_name_tag=ET.SubElement(channel_tag,'display-number')
       display_name_tag.text=E(channel_number)
       datetime_start=datetime(2019,1,1)+timedelta(hours=-9)
       datetime_stop=datetime_start+timedelta(seconds=duration/1000+1)
       program_tag=ET.SubElement(root,'programme')
       program_tag.set('start',datetime_start.strftime('%Y%m%d%H%M%S')+' +0900')
       program_tag.set('stop',datetime_stop.strftime('%Y%m%d%H%M%S')+' +0900')
       program_tag.set('channel',E(channel_number))
       program_tag.set('video-src',video_url)
       program_tag.set('video-type','HTTP_PROGRESSIVE')
       title_tag=ET.SubElement(program_tag,'title')
       title_tag.set('lang','ko')
       title_tag.text=title
       icon_tag=ET.SubElement(program_tag,'icon')
       icon_tag.set('src',icon_url)
       if 'summary' in tag_video.attrib:
        desc_tag=ET.SubElement(program_tag,'desc')
        desc_tag.set('lang','ko')
        desc_tag.text=tag_video.attrib['summary']
       channel_tag=x
       program_tag=x
       channel_index+=1
       channel_number+=channel_step
       if channel_index>max_count:
        break
      except m as e:
       logger.error('Exception:%s',e)
       logger.error(traceback.format_exc())
       if channel_tag is not x:
        root.remove(channel_tag)
       if program_tag is not x:
        root.remove(channel_tag)
  except m as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
  """
        [{"type" : "recent_add", "section" : "episode", "count" : 40, "start_number" : 999, "reverse" : true }, {"type" : "recent_add", "section" : "movie", "count" : 40, "start_number" : 959, "reverse" : true }, {"type" : "section_to_channel", "section" : "0", "include_content_count" : 10, "channel_number" : 899, } ]
        """  
# Created by pyminifier (https://github.com/liftoff/pyminifier)
