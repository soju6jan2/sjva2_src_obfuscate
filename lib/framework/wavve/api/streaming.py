import traceback
g=range
v=str
p=None
W=Exception
C=int
a=traceback.format_exc
import json
from framework.wavve.api import session,logger,get_baseparameter,config
G=logger.error
j=logger.debug
t=session.get
from framework import py_urllib
f=py_urllib.urlencode
def get_guid():
 try:
  from system.model import ModelSetting as SystemModelSetting
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
  for i in g(0,num):
   s=v(randint(1,5))
   rstr+=s
  return rstr
 uuid=GenerateID("POOQ")
 m.update(uuid)
 return v(m.hexdigest())
def streaming(contenttype,contentid,quality,credential,action='hls',ishevc='y',isabr='y',proxy=p):
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
 if credential is p:
  credential='none'
 try:
  param=get_baseparameter()
  param['credential']=credential
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
  url="%s/streaming?%s"%(config['base_url'],f(param))
  proxies=p
  if proxy is not p:
   proxies={"https":proxy,'http':proxy}
  response=t(url,headers=config['headers'],proxies=proxies)
  data=response.json()
  if response.status_code==200:
   try:
    if data['playurl'].startswith('https://event.pca.wavve.com'):
     j('playurl startswith https://event.pca.wavve.com!!!!!')
     return streaming_imsi(contenttype,contentid,quality,credential,action=action,ishevc=ishevc,isabr=isabr)
   except:
    j('https://event.pca.wavve.com error')
   return data
  else:
   if 'resultcode' in data:
    pass
 except W as e:
  G('Exception:%s',e)
  G(a())
def streaming_imsi(contenttype,contentid,quality,credential,action='hls',ishevc='y',isabr='y',proxy=p):
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
 if credential is p:
  credential='none'
 try:
  param=get_baseparameter()
  param['credential']=credential
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
  url="%s/streaming?%s"%(config['base_url'],f(param))
  response=t(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   j(data['playurl'])
   return data
  else:
   if 'resultcode' in data:
    pass
 except W as e:
  G('Exception:%s',e)
  G(a())
def get_prefer_url(url):
 try:
  response=t(url,headers=config['headers'])
  data=response.text.strip()
  last_url=p
  last_quality=0
  for t in data.split('\n'):
   if t.strip().find('chunklist.m3u8')!=-1:
    t_quality=C(t.split('/')[0])
    if t_quality>last_quality:
     last_quality=t_quality
     last_url=t
  if last_url is not p and last_url!='':
   last_url=url.split('chunklist')[0]+last_url
   return last_url
 except W as e:
  G('Exception:%s',e)
  G(a())
 return url
"""
 https://vod.cdn.wavve.com/hls/E01/E01_20241954.1/1/chunklist5000.m3u8?authtoken=g8fzFN4NgPAowe29k7tVyhFOUHDFWuIrK3GlEjoGyxweyoGUXtnWk2LFCEZDWKlDfBTXnbWG16PvhdgHjYIiNiA9ypJrs0EuBk3UFDEveWoAA_h_XRoSTVjveRiaBU0Mo25IV4mIEgepfI7712-0KneO-a7tucrHBYJwpcZ4QWCN53z13cdyA1GjdwPkhgCTYOWf2A
5000/chunklist.m3u8?authtoken=g8fzFN4NgPAowe29k7tVyhFOUHDFWuIrK3GlEjoGyxweyoGUXtnWk2LFCEZDWKlDfBTXnbWG16PvhdgHjYIiNiA9ypJrs0EuBk3UFDEveWoAA_h_XRoSTVjveRiaBU0Mo25IV4mIEgepfI7712-0KneO-a7tucrHBYJwpcZ4QWCN53z13cdyA1GjdwPkhgCTYOWf2A
 https://apis.pooq.co.kr/streaming?credential=Zbi2TxCuEsdktgNrGBrjNuGjE8BKEZocboUC8%2FDpGLCktIdUURykKALOPhBrlszlxuP7np1nJxdwL3UWinH6B1iQUoDl9USk2I%2F2JNJZhelF2CU0nxFgGaDhBElXatI6gPgf8iNgEW2Fvpkrrl8cYMl5kN4%2Fi%2FjSgqKWFjuE%2FyLyRDYwLctu5aytUq%2BVJMV1hAJJ4LkCDrRv7NEx5Z1CU76UdxIFqgyQB2yiIW6eHueyLeliCrLvBEizrdOcCbdj
 authtype=url
 apikey=E5F3E0D30947AA5440556471321BB6D9
 contenttype=vod
 contentid=M_EP202001235626.1
 region=kor
 targetage=auto
 deviceModelId=Windows+10
 drm=wm
 pooqzone=none
 device=pc
 partner=pooq
 guid=636bd06c38161b9c066fe0a2c6fde0f0
 quality=1080p
 action=hls
 isabr=y
 ishevc=y
https://apis.pooq.co.kr/streaming?device=pc
partner=pooq
pooqzone=none
region=kor
drm=wm
targetage=auto
apikey=E5F3E0D30947AA5440556471321BB6D9
credential=aiqk%2FPx6%2BLfWxuBH87cit1wgagHqiA%2Fy7B1SCnB%2FxeoyafsmznGAh%2BP62%2F8R7Pqw1J9auwQ%2Ba902Su%2FgpPR3Bp96sGhk1rEgult3Y0iyu7zEG42sXrc9ynMyool6Fa603DDrLJKSWKBIKDKndMqwFxKPHB2cpvN3hvuRW%2FF%2BI3rgZGc%2B8APVD0l7l3OFDuHeqSUl6KBjwyH4IgjbTXVgcjqPcZlskS6QHf4G90Fv7tDvC%2Bgt4vyH%2BzcP9Glv5%2B%2Fx
contentid=M_EP202001235626.1
contenttype=vod
action=hls
quality=1080p
deviceModelId=Windows%2010
guid=fa324b92-42a3-11ea-909b-c230188c31d3
lastplayid=3d734859ba424632afd0fc952dda0e2e
authtype=cookie
isabr=y
ishevc=n
https://vod-su.cdn.pooq.co.kr/hls/CA01/MV_CA01_DY0000011394.1/8/chunklist5000.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKi9obHMvQ0EwMS9NVl9DQTAxX0RZMDAwMDAxMTM5NC4xLzgvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU3NDYxMTU3MX0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIxMjUuMTgzLjIwNC4wLzI0In19fV0sInRpZCI6IjczNTA3NDI5OTcxIiwidmVyIjoiMyJ9
Signature=dvPJjCch7k28JuNF9FgtSigFpAw9QKGYsM3k~oYmVXbarnKY0XJSp7Q8ZCWD7QI4MnjBHvHL~NkvqkGlyItYHGQOh9W7nGUbIXoiBF0QSjQVh86uk9J1JEWm59i3SRQJomNKhBVfA8I9SdZ7~RuJVsCfXposnIWahYAQyHn1Hwm26vnqzLdq9SFoZZg6ZGXAj716onEfKbNV9sv9ZwJdhNtUgfb~7OMeCwkcIjrITwgaKvdsoSwSZPBKnpFR~WW2FrH-DW0lWIr0gIXaBABm~1~gsw6bCgVYImsEpTWNztA8evpprwUFXyEF7bIWITMoUXBn8RFHGv1cLgJh8~gV1A__&Key-Pair-Id=APKAJ6KCI2B6BKBQMD4A
https://vod-su.cdn.pooq.co.kr/hls/CA01/MV_CA01_DY0000011394.1/8/5000/chunklist.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKi9obHMvQ0EwMS9NVl9DQTAxX0RZMDAwMDAxMTM5NC4xLzgvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU3NDYxMTU3MX0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIxMjUuMTgzLjIwNC4wLzI0In19fV0sInRpZCI6IjczNTA3NDI5OTcxIiwidmVyIjoiMyJ9&Signature=dvPJjCch7k28JuNF9FgtSigFpAw9QKGYsM3k~oYmVXbarnKY0XJSp7Q8ZCWD7QI4MnjBHvHL~NkvqkGlyItYHGQOh9W7nGUbIXoiBF0QSjQVh86uk9J1JEWm59i3SRQJomNKhBVfA8I9SdZ7~RuJVsCfXposnIWahYAQyHn1Hwm26vnqzLdq9SFoZZg6ZGXAj716onEfKbNV9sv9ZwJdhNtUgfb~7OMeCwkcIjrITwgaKvdsoSwSZPBKnpFR~WW2FrH-DW0lWIr0gIXaBABm~1~gsw6bCgVYImsEpTWNztA8evpprwUFXyEF7bIWITMoUXBn8RFHGv1cLgJh8~gV1A__&Key-Pair-Id=APKAJ6KCI2B6BKBQMD4A
header = {'DNT': '1', 'Origin': 'https://www.wavve.com', 'Referer': 'https://www.wavve.com/player/movie?movieid=%s' % code, 'Sec-Fetch-Mode': 'cors', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'Content-type': 'application/octet-stream', 'pallycon-customdata': drm['customdata']}
                item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                item.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
                item.setProperty('inputstream.adaptive.license_key', '%s|%s|R{SSM}|' % (drm['drmhost'], urlencode(header)))
"""
# Created by pyminifier (https://github.com/liftoff/pyminifier)
