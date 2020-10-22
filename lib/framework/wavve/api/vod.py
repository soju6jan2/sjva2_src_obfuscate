import traceback
X=int
V=type
n=Exception
W=False
B=None
P=len
import json
from framework.wavve.api import session,get_baseparameter,config,logger
from framework.util import Util
from framework import py_urllib
def vod_newcontents(page=1,limit=20,genre='all'):
 try:
  page=X(page)if V(page)!=X else page
  param=get_baseparameter()
  param['genre']='all'
  param['channel']='all'
  param['type']='all'
  param['weekday']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']='new' 
  url="%s/vod/newcontents?%s"%(config['base_url'],py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def vod_contents(page=1,limit=20,content_type='newcontents',genre='all',orderby='new',is_cf=W):
 try:
  page=X(page)if V(page)!=X else page
  param=get_baseparameter()
  param['genre']=genre
  param['channel']='all'
  param['type']='all'
  param['weekday']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']=orderby 
  if is_cf:
   url="%s/cf/vod/%s?%s"%(config['base_url'],content_type,py_urllib.urlencode(param))
  else:
   url="%s/vod/%s?%s"%(config['base_url'],content_type,py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def vod_allprograms(page=1,limit=20,contenttype='program',genre='all',subgenre=B,orderby='new',is_cf=W):
 try:
  page=X(page)if V(page)!=X else page
  param=get_baseparameter()
  param['genre']=genre
  param['contenttype']=contenttype
  param['type']='all'
  param['weekday']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']=orderby 
  if subgenre is not B:
   param['subgenre']=subgenre
  if is_cf:
   url="%s/cf/vod/allprograms?%s"%(config['base_url'],py_urllib.urlencode(param))
  else:
   url="%s/vod/allprograms?%s"%(config['base_url'],py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def vod_contents_contentid(contentid):
 try:
  param=get_baseparameter()
  url="%s/vod/contents/%s?%s"%(config['base_url'],contentid,py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def vod_programs_programid(programid):
 try:
  param=get_baseparameter()
  url="%s/vod/programs/%s?%s"%(config['base_url'],programid,py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def vod_program_contents_programid(programid,page=1,limit=20):
 try:
  page=X(page)if V(page)!=X else page
  param=get_baseparameter()
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']='new'
  url="%s/vod/programs-contents/%s?%s"%(config['base_url'],programid,py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def get_filename(data,quality):
 try:
  if 'movieid' in data:
   title=Util.change_text_for_use_filename(data['title'])
   releasedate=data['releasedate'][:4]
   ret="%s.%s.%s-SW.mp4"%(title,releasedate,quality)
   return ret
  else:
   title=Util.change_text_for_use_filename(data['programtitle'])
   tmp=data["episodenumber"]
   episodeno=''
   if P(tmp):
    if tmp=='특집':
     episodeno='.특집'
    else:
     tmps=tmp.split('-')
     episodeno='.E0%s'%tmps[0]if P(tmps[0])==1 else '.E%s'%tmps[0]
   airdate=data["releasedate"].replace('-','')[2:]
   release="SW"
   if data['type']=='onair':
    release='SWQ'
   ret="%s%s.%s.%s-%s.mp4"%(title,episodeno,airdate,quality,release)
   return ret
  if episode_data['result']['contentType']=='movie':
   title=episode_data["result"]["programTitle"]
   title=title.replace("<","").replace(">","").replace("\\","").replace("/","").replace(":","").replace("*","").replace("\"","").replace("|","").replace("?","").replace("  "," ").strip()
   currentQuality=episode_data["result"]["qualityList"]['qualityCurrent']
   qualityRes=PooqAPI.get_quality_to_res(currentQuality)
   airDate=episode_data["result"]["airDate"]
   ret="%s.%s.%s-SP.mp4"%(title,airDate[:4],qualityRes)
   return ret
  else:
   title=episode_data["result"]["programTitle"]
   title=title.replace("<","").replace(">","").replace("\\","").replace("/","").replace(":","").replace("*","").replace("\"","").replace("|","").replace("?","").replace("  "," ").strip()
   episodeno=episode_data["result"]["episodeNo"]
   airdate=episode_data["result"]["airDate"].replace('-','')[2:]
   currentQuality=episode_data["result"]["qualityList"]['qualityCurrent']
   qualityRes=PooqAPI.get_quality_to_res(currentQuality)
   release="SP"
   if episode_data["result"]["contentType"]=='qvod':
    release='SPQ'
   if P(episodeno):
    if P(episodeno)==1:
     episodeno="0"+episodeno
    if episodeno=="특집":
     ret="%s.%s.%s.%s-%s.mp4"%(title,episodeno,airdate,qualityRes,release)
    else:
     ret="%s.E%s.%s.%s-%s.mp4"%(title,episodeno,airdate,qualityRes,release)
   else:
    ret="%s.%s.%s-%s.mp4"%(title,airdate,qualityRes,release)
   return ret
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def movie_contents_detail(movie_id):
 try:
  param=get_baseparameter()
  url="%s/movie/contents/%s?%s"%(config['base_url'],movie_id,py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except n as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
