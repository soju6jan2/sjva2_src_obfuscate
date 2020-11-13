import traceback
import json
from framework.wavve.api import session,logger,get_baseparameter,config
from framework import py_urllib,SystemModelSetting
def get_guid():
 try:
  tmp=SystemModelSetting.get('wavve_guid')
  if tmp!='':
   return tmp
 except:
  pass
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
  for i in range(0,num):
   s=str(randint(1,5))
   rstr+=s
  return rstr
 uuid=GenerateID("POOQ")
 m.update(uuid)
 return str(m.hexdigest())
def streaming(contenttype,contentid,quality,action='hls',ishevc='y',isabr='y',proxy=None):
 if quality=='FHD':
  quality='1080p'
 elif quality=='HD':
  quality='720p'
 elif quality=='SD':
  quality='480p'
 elif quality=='UHD':
  quality='2160p'
 if contenttype=='live':
  ishevc='n'
  isabr='n'
 try:
  param=get_baseparameter()
  param['credential']=SystemModelSetting.get('site_wavve_credential')
  if contenttype=='general':
   contenttype='vod'
  elif contenttype=='onair':
   contenttype='onairvod'
  param['contenttype']=contenttype
  param['contentid']=contentid
  param['action']=action
  param['quality']=quality
  param['guid']=''
  param['deviceModelId']='Windows 10'
  param['authtype']='url' 
  param['isabr']=isabr
  param['ishevc']=ishevc
  param['lastplayid']='none'
  url="%s/streaming?%s"%(config['base_url'],py_urllib.urlencode(param))
  proxies=None
  if proxy is not None:
   proxies={"https":proxy,'http':proxy}
  response=session.get(url,headers=config['headers'],proxies=proxies)
  data=response.json()
  if response.status_code==200:
   logger.debug(url)
   logger.debug(data)
   try:
    if data['playurl'].startswith('https://event.pca.wavve.com'):
     logger.debug('playurl startswith https://event.pca.wavve.com!!!!!')
     return streaming_imsi(contenttype,contentid,quality,action=action,ishevc=ishevc,isabr=isabr)
   except:
    logger.debug('https://event.pca.wavve.com error')
   if data['playurl'].endswith('.mpd'):
    ret={}
    ret['uri']=data['playurl']
    ret['drm_scheme']='widevine'
    ret['drm_license_uri']=data['drm']['drmhost']
    ret['drm_key_request_properties']={'origin':'https://www.wavve.com','sec-fetch-site':'same-site','sec-fetch-mode':'cors','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36','pallycon-customdata':data['drm']['customdata'],'cookie':data['awscookie']}
    data['playurl']=ret
   return data
  else:
   if 'resultcode' in data:
    pass
 except Exception as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def streaming_imsi(contenttype,contentid,quality,action='hls',ishevc='y',isabr='y',proxy=None):
 if quality=='FHD':
  quality='1080p'
 elif quality=='HD':
  quality='720p'
 elif quality=='SD':
  quality='480p'
 elif quality=='UHD':
  quality='2160p'
 if contenttype=='live':
  ishevc='n'
  isabr='n'
 try:
  param=get_baseparameter()
  param['credential']=SystemModelSetting.get('site_wavve_credential')
  if contenttype=='general':
   contenttype='vod'
  elif contenttype=='onair':
   contenttype='onairvod'
  param['contenttype']=contenttype
  param['contentid']=contentid
  param['action']=action
  param['quality']=quality
  param['guid']=''
  param['authtype']='url' 
  param['isabr']=isabr
  param['ishevc']=ishevc
  param['lastplayid']='none'
  param['device']='smarttv'
  url="%s/streaming?%s"%(config['base_url'],py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   logger.debug(data['playurl'])
   return data
  else:
   if 'resultcode' in data:
    pass
 except Exception as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def streaming(contenttype,contentid,quality,action='hls',ishevc='y',isabr='y',proxy=None):
 if quality=='FHD':
  quality='1080p'
 elif quality=='HD':
  quality='720p'
 elif quality=='SD':
  quality='480p'
 elif quality=='UHD':
  quality='2160p'
 if contenttype=='live':
  ishevc='n'
  isabr='n'
 try:
  param=get_baseparameter()
  param['credential']=SystemModelSetting.get('site_wavve_credential')
  if contenttype=='general':
   contenttype='vod'
  elif contenttype=='onair':
   contenttype='onairvod'
  param['contenttype']=contenttype
  param['contentid']=contentid
  param['action']=action
  param['quality']=quality
  param['guid']=''
  param['deviceModelId']='Windows 10'
  param['authtype']='url' 
  param['isabr']=isabr
  param['ishevc']=ishevc
  param['lastplayid']='none'
  url="%s/streaming?%s"%(config['base_url'],py_urllib.urlencode(param))
  proxies=None
  if proxy is not None:
   proxies={"https":proxy,'http':proxy}
  response=session.get(url,headers=config['headers'],proxies=proxies)
  data=response.json()
  if response.status_code==200:
   try:
    if data['playurl'].startswith('https://event.pca.wavve.com'):
     logger.debug('playurl startswith https://event.pca.wavve.com!!!!!')
     return streaming_imsi(contenttype,contentid,quality,action=action,ishevc=ishevc,isabr=isabr)
   except:
    logger.debug('https://event.pca.wavve.com error')
   return data
  else:
   if 'resultcode' in data:
    pass
 except Exception as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_prefer_url(url):
 try:
  response=session.get(url,headers=config['headers'])
  data=response.text.strip()
  last_url=None
  last_quality=0
  for t in data.split('\n'):
   if t.strip().find('chunklist.m3u8')!=-1:
    t_quality=int(t.split('/')[0])
    if t_quality>last_quality:
     last_quality=t_quality
     last_url=t
  if last_url is not None and last_url!='':
   last_url=url.split('chunklist')[0]+last_url
   return last_url
 except Exception as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
 return url
def streaming2(contenttype,contentid,quality,action='dash',ishevc='n',isabr='y',proxy=None):
 if quality=='FHD':
  quality='1080p'
 elif quality=='HD':
  quality='720p'
 elif quality=='SD':
  quality='480p'
 elif quality=='UHD':
  quality='2160p'
 if contenttype=='live':
  ishevc='n'
  isabr='n'
 try:
  param=get_baseparameter()
  param['credential']=SystemModelSetting.get('site_wavve_credential')
  if contenttype=='general':
   contenttype='vod'
  elif contenttype=='onair':
   contenttype='onairvod'
  param['contenttype']=contenttype
  param['contentid']=contentid
  param['action']=action
  param['quality']=quality
  param['guid']=''
  param['deviceModelId']='Windows 10'
  param['authtype']='url' 
  param['isabr']=isabr
  param['ishevc']=ishevc
  param['lastplayid']='none'
  url="%s/streaming?%s"%(config['base_url'],py_urllib.urlencode(param))
  proxies=None
  if proxy is not None:
   proxies={"https":proxy,'http':proxy}
  response=session.get(url,headers=config['headers'],proxies=proxies)
  data=response.json()
  if response.status_code==200:
   if data['playurl'].find('.mpd')!=-1:
    if data['playurl'].endswith('.mpd'):
     data['playurl']+='?'+data['awscookie']
    ret={}
    ret['uri']=data['playurl']
    ret['drm_scheme']='widevine'
    ret['drm_license_uri']=data['drm']['drmhost']
    ret['drm_key_request_properties']={'origin':'https://www.wavve.com','sec-fetch-site':'same-site','sec-fetch-mode':'cors','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36','referer':'https://www.wavve.com','pallycon-customdata':data['drm']['customdata'],'cookie':data['awscookie'],'content-type':'application/octet-stream',}
    data['playurl']=ret
   else:
    return streaming(contenttype,contentid,quality,ishevc='n',proxy=proxy)
   return data
  else:
   if 'resultcode' in data:
    pass
 except Exception as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
