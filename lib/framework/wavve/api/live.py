import traceback
W=Exception
a=traceback.format_exc
import json
z=json.load
from framework import py_urllib,py_urllib2
q=py_urllib2.urlopen
n=py_urllib2.Request
f=py_urllib.urlencode
from framework.wavve.api import session,get_baseparameter,config,logger
G=logger.error
j=logger.debug
t=session.get
from framework.util import Util
def live_all_channels(genre='all'):
 try:
  param=get_baseparameter()
  param['genre']=genre
  param['type']='all'
  param['offset']=0
  param['limit']=999
  url="%s/live/all-channels?%s"%(config['base_url'],f(param))
  response=t(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    j(data['resultmessage'])
 except W as e:
  G('Exception:%s',e)
  G(a()) 
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
  url="%s/live/epgs/channels/%s?%s"%(config['base_url'],channel_id,f(param))
  response=t(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    j(data['resultmessage'])
 except W as e:
  G('Exception:%s',e)
  G(a())
def get_live_quality_list(source_id):
 try:
  url='https://wapie.pooq.co.kr/v1/lives30/%s'%source_id
  params=DEFAULT_PARAM.copy()
  params['credential']='none'
  url='%s?%s'%(url,f(params))
  request=n(url)
  response=q(request)
  data=z(response,encoding='utf8')
  result=data['result']['qualityList'][0]['quality']
  return result
 except W as e:
  G('Exception:%s',e)
  G(a())
def get_quality_to_pooq(quality):
 if quality=='FHD':
  return '5000'
 elif quality=='HD':
  return '2000'
 elif quality=='SD':
  return '1000'
 return '5000'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
