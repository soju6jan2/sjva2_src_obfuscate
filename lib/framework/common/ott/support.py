import os
L=object
w=staticmethod
N=None
j=Exception
g=int
U=max
import io
import traceback
V=traceback.format_exc
import requests
O=requests.get
import re
z=re.compile
import json
m=json.loads
from framework import logger
F=logger.debug
B=logger.error
class OTTSupport(L):
 @w
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
    url=O(tmp).json()['secUrl']
   else:
    data=O(target_url).text
    match=z(r"sApiF:\s'(?P<url>.*?)',").search(data)
    if match is not N:
     json_url=match.group('url')
     data=O(json_url).json()
     url=N
     for tmp in data['streams']:
      if tmp['qualityId']==quality:
       url=tmp['url']
       break
   return url
  except j as e:
   B('Exception:%s',e)
   B(V())
 @w
 def get_kakao_url(target):
  try:
   tmp="https://tv.kakao.com/api/v5/ft/livelinks/impress?player=monet_html5&service=kakao_tv&section=kakao_tv&dteType=PC&profile=BASE&liveLinkId={liveid}&withRaw=true&contentType=HLS".format(liveid=target)
   url=O(tmp).json()['raw']['videoLocation']['url']
   return url
  except j as e:
   B('Exception:%s',e)
   B(V())
 @w
 def get_kbs_url(source_id):
  try:
   tmp='http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=%s'%source_id
   data=O(tmp).text
   idx1=data.find('var channel = JSON.parse')+26
   idx2=data.find(');',idx1)-1
   data=data[idx1:idx2].replace('\\','')
   data=m(data)
   U=0
   url=N
   for item in data['channel_item']:
    F(item)
    tmp=g(item['bitrate'].replace('Kbps',''))
    if tmp>U:
     url=item['service_url']
     U=tmp
   return url
  except j as e:
   B('Exception:%s',e)
   B(V())
 @w
 def get_sbs_url(source_id):
  try:
   prefix='' if g(source_id[1:])<20 else 'virtual/'
   tmp='http://apis.sbs.co.kr/play-api/1.0/onair/%schannel/%s?v_type=2&platform=pcweb&protocol=hls&ssl=N&jwt-token=%s&rnd=462'%(prefix,source_id,'')
   data=O(tmp).json()
   url=data['onair']['source']['mediasource']['mediaurl']
   return url
  except j as e:
   B('Exception:%s',e)
   B(V())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
