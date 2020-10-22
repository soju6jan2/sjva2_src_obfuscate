import os
i=object
k=staticmethod
S=None
n=Exception
x=int
V=max
import io
import traceback
import requests
import re
import json
from framework import logger
class OTTSupport(i):
 @k
 def get_naver_url(target_url,quality):
  try:
   if target_url.startswith('SPORTS_'):
    target_ch=target_url.split('_')[1]
    if not target_ch.startswith('ad')and not target_ch.startswith('ch'):
     target_ch='ch'+target_ch
    qua='5000'
    tmp={'480':'800','720':'2000','1080':'5000'}
    qua=tmp[quality]if quality in tmp else qua
    tmp='https://apis.naver.com/pcLive/livePlatform/sUrl?ch=%s&q=%s&p=hls&cc=KR&env=pc'%(target_ch,qua)
    url=requests.get(tmp).json()['secUrl']
   else:
    data=requests.get(target_url).text
    match=re.compile(r"sApiF:\s'(?P<url>.*?)',").search(data)
    if match is not S:
     json_url=match.group('url')
     data=requests.get(json_url).json()
     url=S
     for tmp in data['streams']:
      if tmp['qualityId']==quality:
       url=tmp['url']
       break
   return url
  except n as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @k
 def get_kakao_url(target):
  try:
   tmp="https://tv.kakao.com/api/v5/ft/livelinks/impress?player=monet_html5&service=kakao_tv&section=kakao_tv&dteType=PC&profile=BASE&liveLinkId={liveid}&withRaw=true&contentType=HLS".format(liveid=target)
   url=requests.get(tmp).json()['raw']['videoLocation']['url']
   return url
  except n as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @k
 def get_kbs_url(source_id):
  try:
   tmp='http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=%s'%source_id
   data=requests.get(tmp).text
   idx1=data.find('var channel = JSON.parse')+26
   idx2=data.find(');',idx1)-1
   data=data[idx1:idx2].replace('\\','')
   data=json.loads(data)
   V=0
   url=S
   for item in data['channel_item']:
    logger.debug(item)
    tmp=x(item['bitrate'].replace('Kbps',''))
    if tmp>V:
     url=item['service_url']
     V=tmp
   return url
  except n as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @k
 def get_sbs_url(source_id):
  try:
   prefix='' if x(source_id[1:])<20 else 'virtual/'
   tmp='http://apis.sbs.co.kr/play-api/1.0/onair/%schannel/%s?v_type=2&platform=pcweb&protocol=hls&ssl=N&jwt-token=%s&rnd=462'%(prefix,source_id,'')
   data=requests.get(tmp).json()
   url=data['onair']['source']['mediasource']['mediaurl']
   return url
  except n as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
