import os
import traceback
import sys
import requests
import time
import json
import base64
from framework import app,py_urllib,SystemModelSetting
from framework.logger import get_logger
from framework.util import Util
logger=get_logger('tving_api')
from.base import get_proxies,session
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36','Accept':'application/json, text/plain, */*','Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7','origin':'https://www.tving.com','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin',}
def get_stream_info_by_web(content_type,media_code,quality):
 ooc='isTrusted=false^type=oocCreate^eventPhase=0^bubbles=false^cancelable=false^defaultPrevented=false^composed=false^timeStamp=3336.340000038035^returnValue=true^cancelBubble=false^NONE=0^CAPTURING_PHASE=1^AT_TARGET=2^BUBBLING_PHASE=3^'
 try:
  data={'apiKey':'1e7952d0917d6aab1f0293a063697610','info':'Y','networkCode':'CSND0900','osCode':'CSOD0900','teleCode':'CSCD0900','mediaCode':media_code,'screenCode':'CSSD0100','callingFrom':'HTML5','streamCode':quality,'deviceId':SystemModelSetting.get('site_tving_deviceid'),'adReq':'adproxy','ooc':ooc,'wm':'Y','uuid':SystemModelSetting.get('site_tving_uuid')}
  cookies={'_tving_token':SystemModelSetting.get('site_tving_token').split('=')[1],'onClickEvent2':py_urllib.quote(ooc),'TP2wgas1K9Q8F7B359108383':'Y',}
  if True or content_type=='live':
   headers['referer']='https://www.tving.com/%s/player/%s'%(content_type,media_code)
   url='https://www.tving.com/streaming/info'
   res=requests.post(url,data=data,headers=headers,cookies=cookies,proxies=get_proxies())
   data=res.json()
   ret={}
   if 'widevine' in data['stream']['broadcast']:
    ret['uri']=data['stream']['broadcast']['widevine']['broad_url']
    ret['drm_scheme']='widevine'
    ret['drm_license_uri']='http://cj.drmkeyserver.com/widevine_license'
    ret['drm_key_request_properties']={'origin':'https://www.tving.com','sec-fetch-site':'cross-site','sec-fetch-mode':'cors','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','Host':'cj.drmkeyserver.com','referer':'https://www.tving.com/','AcquireLicenseAssertion':data['stream']['drm_license_assertion'],}
    data['play_info']=ret
    return data
   else:
    data['play_info']={'hls':data['stream']['broadcast']['broad_url']}
    return data
 except Exception as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
