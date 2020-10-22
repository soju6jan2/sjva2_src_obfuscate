import traceback
d=int
i=type
Q=Exception
U=False
a=None
x=len
q=traceback.format_exc
import json
from framework.wavve.api import session,get_baseparameter,config,logger
w=logger.error
y=logger.debug
F=session.get
from framework.util import Util
B=Util.change_text_for_use_filename
from framework import py_urllib
M=py_urllib.urlencode
def vod_newcontents(page=1,limit=20,genre='all'):
 try:
  page=d(page)if i(page)!=d else page
  param=get_baseparameter()
  param['genre']='all'
  param['channel']='all'
  param['type']='all'
  param['weekday']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']='new' 
  url="%s/vod/newcontents?%s"%(config['base_url'],M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
def vod_contents(page=1,limit=20,content_type='newcontents',genre='all',orderby='new',is_cf=U):
 try:
  page=d(page)if i(page)!=d else page
  param=get_baseparameter()
  param['genre']=genre
  param['channel']='all'
  param['type']='all'
  param['weekday']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']=orderby 
  if is_cf:
   url="%s/cf/vod/%s?%s"%(config['base_url'],content_type,M(param))
  else:
   url="%s/vod/%s?%s"%(config['base_url'],content_type,M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
def vod_allprograms(page=1,limit=20,contenttype='program',genre='all',subgenre=a,orderby='new',is_cf=U):
 try:
  page=d(page)if i(page)!=d else page
  param=get_baseparameter()
  param['genre']=genre
  param['contenttype']=contenttype
  param['type']='all'
  param['weekday']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']=orderby 
  if subgenre is not a:
   param['subgenre']=subgenre
  if is_cf:
   url="%s/cf/vod/allprograms?%s"%(config['base_url'],M(param))
  else:
   url="%s/vod/allprograms?%s"%(config['base_url'],M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
def vod_contents_contentid(contentid):
 try:
  param=get_baseparameter()
  url="%s/vod/contents/%s?%s"%(config['base_url'],contentid,M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
def vod_programs_programid(programid):
 try:
  param=get_baseparameter()
  url="%s/vod/programs/%s?%s"%(config['base_url'],programid,M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
def vod_program_contents_programid(programid,page=1,limit=20):
 try:
  page=d(page)if i(page)!=d else page
  param=get_baseparameter()
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']='new'
  url="%s/vod/programs-contents/%s?%s"%(config['base_url'],programid,M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
def get_filename(data,quality):
 try:
  if 'movieid' in data:
   title=B(data['title'])
   releasedate=data['releasedate'][:4]
   ret="%s.%s.%s-SW.mp4"%(title,releasedate,quality)
   return ret
  else:
   title=B(data['programtitle'])
   tmp=data["episodenumber"]
   episodeno=''
   if x(tmp):
    if tmp=='특집':
     episodeno='.특집'
    else:
     tmps=tmp.split('-')
     episodeno='.E0%s'%tmps[0]if x(tmps[0])==1 else '.E%s'%tmps[0]
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
   if x(episodeno):
    if x(episodeno)==1:
     episodeno="0"+episodeno
    if episodeno=="특집":
     ret="%s.%s.%s.%s-%s.mp4"%(title,episodeno,airdate,qualityRes,release)
    else:
     ret="%s.E%s.%s.%s-%s.mp4"%(title,episodeno,airdate,qualityRes,release)
   else:
    ret="%s.%s.%s-%s.mp4"%(title,airdate,qualityRes,release)
   return ret
 except Q as e:
  w('Exception:%s',e)
  w(q())
def movie_contents_detail(movie_id):
 try:
  param=get_baseparameter()
  url="%s/movie/contents/%s?%s"%(config['base_url'],movie_id,M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
