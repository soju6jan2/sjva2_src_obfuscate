import traceback
W=Exception
g=range
v=str
a=traceback.format_exc
import json
z=json.load
from framework import py_urllib,py_urllib2
q=py_urllib2.urlopen
n=py_urllib2.Request
f=py_urllib.urlencode
from framework.wavve.api import session,get_baseparameter,config,logger
G=logger.error
DEFAULT_PARAM={'deviceTypeId':'pc','marketTypeId':'generic','apiAccessCredential':'EEBE901F80B3A4C4E5322D58110BE95C','drm':'WC','country':'KOR'}
def get_live_list():
 try:
  url='https://wapie.pooq.co.kr/v1/livesgenresort30/'
  params=DEFAULT_PARAM.copy()
  params['credential']='none'
  params['orderby']='g'
  url='%s?%s'%(url,f(params))
  request=n(url)
  response=q(request)
  data=z(response,encoding='utf8')
  return data['result']['list']
 except W as e:
  G('Exception:%s',e)
  G(a()) 
def get_live_json(source_id,quality,credential):
 try:
  quality=get_quality_to_pooq(quality)
  quality_list=get_live_quality_list(source_id)
  if not quality in quality_list:
   quality=quality_list[0]
  url='https://wapie.pooq.co.kr/v1/lives30/%s/url'%source_id
  params=DEFAULT_PARAM.copy()
  params['deviceModelId']='Macintosh'
  params['authType']='cookie'
  params['guid']=get_guid()
  params['lastPlayId']='none'
  params['quality']=quality
  params['credential']=credential
  url='%s?%s'%(url,f(params))
  request=n(url)
  response=q(request)
  data=z(response,encoding='utf8')
  return data
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
def get_guid():
 import hashlib
 m=hashlib.md5()
 def GenerateID(media):
  from datetime import datetime
  requesttime=datetime.now().strftime('%Y%m%d%H%M%S')
  randomstr=GenerateRandomString(5)
  uuid=randomstr+media+requesttime
  return uuid
 def GenerateRandomString(num):
  from random import randint
  rstr=""
  for i in g(0,num):
   s=v(randint(1,5))
   rstr+=s
  return rstr
 uuid=GenerateID("POOQ")
 m.update(uuid)
 return v(m.hexdigest())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
