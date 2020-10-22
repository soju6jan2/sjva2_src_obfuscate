import traceback
Q=Exception
q=traceback.format_exc
import json
r=json.load
from framework import py_urllib,py_urllib2
S=py_urllib2.urlopen
X=py_urllib2.Request
M=py_urllib.urlencode
from framework.wavve.api import session,get_baseparameter,config,logger
w=logger.error
y=logger.debug
F=session.get
from framework.util import Util
def live_all_channels(genre='all'):
 try:
  param=get_baseparameter()
  param['genre']=genre
  param['type']='all'
  param['offset']=0
  param['limit']=999
  url="%s/live/all-channels?%s"%(config['base_url'],M(param))
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
def live_epgs_channels(channel_id,startdatetime,enddatetime):
 try:
  param=get_baseparameter()
  param['genre']='all'
  param['type']='all'
  param['offset']=0
  param['limit']=999
  param['startdatetime']=startdatetime
  param['enddatetime']=enddatetime
  param['orderby']='old'
  url="%s/live/epgs/channels/%s?%s"%(config['base_url'],channel_id,M(param))
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
def get_live_quality_list(source_id):
 try:
  url='https://wapie.pooq.co.kr/v1/lives30/%s'%source_id
  params=DEFAULT_PARAM.copy()
  params['credential']='none'
  url='%s?%s'%(url,M(params))
  request=X(url)
  response=S(request)
  data=r(response,encoding='utf8')
  result=data['result']['qualityList'][0]['quality']
  return result
 except Q as e:
  w('Exception:%s',e)
  w(q())
def get_quality_to_pooq(quality):
 if quality=='FHD':
  return '5000'
 elif quality=='HD':
  return '2000'
 elif quality=='SD':
  return '1000'
 return '5000'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
