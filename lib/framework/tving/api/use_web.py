import os
import traceback
import sys
import requests
import time
import json
import base64
from framework import app,py_urllib
from framework.logger import get_logger
from framework.util import Util
logger=get_logger('tving_api')
from.base import get_proxies,session
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36','Accept':'application/json, text/plain, */*','Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7','origin':'https://www.tving.com','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin',}
def get_stream_info_by_web(content_type,media_code,quality):
 ooc='isTrusted=false^type=oocCreate^eventPhase=0^bubbles=false^cancelable=false^defaultPrevented=false^composed=false^timeStamp=3336.340000038035^returnValue=true^cancelBubble=false^NONE=0^CAPTURING_PHASE=1^AT_TARGET=2^BUBBLING_PHASE=3^'
 try:
  data={'apiKey':'1e7952d0917d6aab1f0293a063697610','info':'Y','networkCode':'CSND0900','osCode':'CSOD0900','teleCode':'CSCD0900','mediaCode':media_code,'screenCode':'CSSD0100','callingFrom':'HTML5','streamCode':quality,'deviceId':SystemModelSetting.get('site_tving_deviceid'),'adReq':'adproxy','ooc':ooc,'wm':'Y',}
  cookies={'_tving_token':SystemModelSetting.get('site_tving_token').split('=')[1],'onClickEvent2':py_urllib.quote(ooc)}
  if True or content_type=='live':
   headers['referer']='https://www.tving.com/%s/player/%s'%(content_type,media_code)
   url='https://www.tving.com/streaming/info'
   res=requests.post(url,data=data,headers=headers,cookies=cookies,proxies=get_proxies())
   data=res.json()
   ret={}
   ret['uri']=data['stream']['broadcast']['widevine']['broad_url']
   ret['drm_scheme']='widevine'
   ret['drm_license_uri']='http://cj.drmkeyserver.com/widevine_license'
   ret['drm_key_request_properties']={'origin':'https://www.tving.com','sec-fetch-site':'cross-site','sec-fetch-mode':'cors','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','Host':'cj.drmkeyserver.com','referer':'https://www.tving.com/','AcquireLicenseAssertion':data['stream']['drm_license_assertion'],}
   data['play_info']=ret
   return data
 except Exception as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
"""
          case "name":
            title = reader.nextString();
            break;
          case "uri":
            uri = Uri.parse(reader.nextString());
            break;
          case "extension":
            extension = reader.nextString();
            break;
          case "clip_start_position_ms":
            mediaItem.setClipStartPositionMs(reader.nextLong());
            break;
          case "clip_end_position_ms":
            mediaItem.setClipEndPositionMs(reader.nextLong());
            break;
          case "ad_tag_uri":
            mediaItem.setAdTagUri(reader.nextString());
            break;
          case "drm_scheme":
            mediaItem.setDrmUuid(Util.getDrmUuid(reader.nextString()));
            break;
          case "drm_license_uri":
          case "drm_license_url": // For backward compatibility only.
            mediaItem.setDrmLicenseUri(reader.nextString());
            break;
          case "drm_key_request_properties":
            Map<String, String> requestHeaders = new HashMap<>();
            reader.beginObject();
            while (reader.hasNext()) {requestHeaders.put(reader.nextName(), reader.nextString()); }
            reader.endObject();
            mediaItem.setDrmLicenseRequestHeaders(requestHeaders);
            Log.e(TAG, "Error loading sample list: " + requestHeaders, null);
            break;
          case "drm_session_for_clear_content":
            if (reader.nextBoolean()) {mediaItem.setDrmSessionForClearTypes(ImmutableList.of(C.TRACK_TYPE_VIDEO, C.TRACK_TYPE_AUDIO)); }
            break;
          case "drm_multi_session":
            mediaItem.setDrmMultiSession(reader.nextBoolean());
            break;
          case "drm_force_default_license_uri":
            mediaItem.setDrmForceDefaultLicenseUri(reader.nextBoolean());
            break;
          case "subtitle_uri":
            subtitleUri = Uri.parse(reader.nextString());
            break;
          case "subtitle_mime_type":
            subtitleMimeType = reader.nextString();
            break;
          case "subtitle_language":
            subtitleLanguage = reader.nextString();
            break;
          case "playlist":
            checkState(!insidePlaylist, "Invalid nesting of playlists");
            children = new ArrayList<>();
            reader.beginArray();
            while (reader.hasNext()) {children.add(readEntry(reader, /* insidePlaylist= */ true)); }
            reader.endArray();
            break;
          default:
            throw new ParserException("Unsupported attribute name: " + name);
config = {'token': None, 'param' : "&free=all&lastFrequency=y&order=broadDate", #최신 'program_param' : '&free=all&order=frequencyDesc&programCode=%s', 'default_param' : '&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610'}
import requests
def get_stream_info():
    print('aaa') 
    url = 'https://www.tving.com/streaming/info'
    ooc = 'isTrusted=false^type=oocCreate^eventPhase=0^bubbles=false^cancelable=false^defaultPrevented=false^composed=false^timeStamp=4459.404999972321^returnValue=true^cancelBubble=false^NONE=0^CAPTURING_PHASE=1^AT_TARGET=2^BUBBLING_PHASE=3^'
    ooc = 'composed=false^CAPTURING_PHASE=1^cancelable=false^returnValue=true^cancelBubble=false^bubbles=false^defaultPrevented=false^NONE=0^AT_TARGET=2^BUBBLING_PHASE=3^timeStamp=2158.7350000045262^isTrusted=false^type=oocCreate^eventPhase=0'
    data = {'apiKey' : '1e7952d0917d6aab1f0293a063697610', 'info' : 'Y', 'networkCode' : 'CSND0900', 'osCode' : 'CSOD0400', 'teleCode' : 'CSCD0900', 'mediaCode' : 'C07381', 'screenCode' : 'CSSD0100', 'callingFrom' : 'HTML5', 'streamCode' : 'stream40', 'deviceId' : '18747739', 'adReq' : 'adproxy', 'ooc' : ooc }
    url2 = "http://api.tving.com/v1/user/device/list?model=PC&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610"
    #params= {'networkCode': 'CSND0900', 'apiKey': '1e7952d0917d6aab1f0293a063697610', 'guest': 'all', 'screenCode': 'CSSD0100', 'free': 'all', 'scope': 'all', 'osCode': 'CSOD0900', 'order': 'rating', 'teleCode': 'CSCD0900'}
    #print(requests.get(url2, headers=headers).text)
    res2 = requests.get(url2, headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'} , cookies = {'_tving_token': 'GZ2lHPOGpKyNhJY8FZgFmw%3D%3D', 'POC_USERINFO': 'aeSjz7IMYkx%2Fj0Ss7YLkzcPMJAQnttf5uFn1sdCanThpnYhJFsxWcAn6UDS2BeBvOSgrDXYFD5vQgt%2BteF9K5vesy60ntBs0BgcPN9kt5Vjwi%2BYnUFMRao0ggX%2BGaH3oK69ZTUxC7Bq9yq3hrffbKSSfdfHlcn9fZ4E%2BgYdi8VkycY7rFSWfWCRg4y7S6WkmePnc0oBWVz7n7E5Owfw3sSlIFEqlxD%2BhJtagzPbWR6PGUrRgXvUTFjKJy4kLzOIbT2pdtprGKHXCWTz87WjpjE7SkuJnblay6iD7L%2Fq%2FL1zevsW%2BLzihmDmQAY%2BraNExwxhpVZd2jYQxknpUO%2FjL%2FEwIjRR8uLxoOuDMp6Kbir3QZyAhjIjCGWyqRJhelRuAxn1qBPWDMBc6jXJP3%2BDKgGQ8iIHvVYmSAaZ6bjl%2BbwRFeCNRTREXbjBw03E%2F2GG2%2BZXyoZR3iXLnJQ00c3MFVw240OpLzGUu0NdtQVumdLZ868dEcqWIaPErjPlCspllZZvJrSGbhdXaGfp%2Bm6gLzFp8H0LVAYSl0a6IwaMA5qEtRPJRCCl1biSFh%2BOzuCSBCnZBmASb2aC5jw0KspfWy%2BLG4XfZ4ej26ae9yrL3NkqIU9y1eTI4NKeC2yh2bivY7iK%2BXwR9C6aW%2FOFZ5mFk3mOtQX%2F70HCaf8AyX97WrxY%3D'} )
    print(res2.text)
    import time
    print(time.time())
    return
    #res = requests.post(url, headers=headers, json=data)
    #res = requests.post(url, data={'info': 'N', 'networkCode': 'CSND0900', 'apiKey': '1e7952d0917d6aab1f0293a063697610', 'adReq': 'none', 'ooc': 'composed=false^CAPTURING_PHASE=1^cancelable=false^returnValue=true^cancelBubble=false^bubbles=false^defaultPrevented=false^NONE=0^AT_TARGET=2^BUBBLING_PHASE=3^timeStamp=2158.7350000045262^isTrusted=false^type=oocCreate^eventPhase=0^', 'streamCode': 'stream50', 'screenCode': 'CSSD0100', 'mediaCode': 'C07381', 'callingFrom': 'HTML5', 'deviceId': '18747739', 'osCode': 'CSOD0400', 'teleCode': 'CSCD0900'}, headers={'origin': 'https://www.tving.com', 'Referer': 'https://www.tving.com/vod/player/C07381', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}, cookies = {'_tving_token': 'GZ2lHPOGpKyNhJY8FZgFmw%3D%3D', 'POC_USERINFO': 'aeSjz7IMYkx%2Fj0Ss7YLkzcPMJAQnttf5uFn1sdCanThpnYhJFsxWcAn6UDS2BeBvOSgrDXYFD5vQgt%2BteF9K5vesy60ntBs0BgcPN9kt5Vjwi%2BYnUFMRao0ggX%2BGaH3oK69ZTUxC7Bq9yq3hrffbKSSfdfHlcn9fZ4E%2BgYdi8VkycY7rFSWfWCRg4y7S6WkmePnc0oBWVz7n7E5Owfw3sSlIFEqlxD%2BhJtagzPbWR6PGUrRgXvUTFjKJy4kLzOIbT2pdtprGKHXCWTz87WjpjE7SkuJnblay6iD7L%2Fq%2FL1zevsW%2BLzihmDmQAY%2BraNExwxhpVZd2jYQxknpUO%2FjL%2FEwIjRR8uLxoOuDMp6Kbir3QZyAhjIjCGWyqRJhelRuAxn1qBPWDMBc6jXJP3%2BDKgGQ8iIHvVYmSAaZ6bjl%2BbwRFeCNRTREXbjBw03E%2F2GG2%2BZXyoZR3iXLnJQ00c3MFVw240OpLzGUu0NdtQVumdLZ868dEcqWIaPErjPlCspllZZvJrSGbhdXaGfp%2Bm6gLzFp8H0LVAYSl0a6IwaMA5qEtRPJRCCl1biSFh%2BOzuCSBCnZBmASb2aC5jw0KspfWy%2BLG4XfZ4ej26ae9yrL3NkqIU9y1eTI4NKeC2yh2bivY7iK%2BXwR9C6aW%2FOFZ5mFk3mOtQX%2F70HCaf8AyX97WrxY%3D', 'onClickEvent2': 'composed%3Dfalse%5ECAPTURING_PHASE%3D1%5Ecancelable%3Dfalse%5EreturnValue%3Dtrue%5EcancelBubble%3Dfalse%5Ebubbles%3Dfalse%5EdefaultPrevented%3Dfalse%5ENONE%3D0%5EAT_TARGET%3D2%5EBUBBLING_PHASE%3D3%5EtimeStamp%3D2158.7350000045262%5EisTrusted%3Dfalse%5Etype%3DoocCreate%5EeventPhase%3D0%5E'} , )
    #composed=false^CAPTURING_PHASE=1^cancelable=false^returnValue=true^cancelBubble=false^bubbles=false^defaultPrevented=false^NONE=0^AT_TARGET=2^BUBBLING_PHASE=3^timeStamp=2158.7350000045262^isTrusted=false^type=oocCreate^eventPhase=0
    #composed=false^CAPTURING_PHASE=1^cancelable=false^returnValue=true^cancelBubble=false^bubbles=false^defaultPrevented=false^NONE=0^AT_TARGET=2^BUBBLING_PHASE=3^timeStamp=2158.7350000045262^isTrusted=false^type=oocCreate^eventPhase=0
    #res = requests.post(url, data={'info': 'N', 'networkCode': 'CSND0900', 'apiKey': '1e7952d0917d6aab1f0293a063697610', 'adReq': 'none', 'ooc': 'composed=false^CAPTURING_PHASE=1^cancelable=false^returnValue=true^cancelBubble=false^bubbles=false^defaultPrevented=false^NONE=0^AT_TARGET=2^BUBBLING_PHASE=3^timeStamp=2158.7350000045262^isTrusted=false^type=oocCreate^eventPhase=0^', 'streamCode': 'stream50', 'screenCode': 'CSSD0100', 'mediaCode': 'C07381', 'callingFrom': 'HTML5', 'deviceId': '18747739', 'osCode': 'CSOD0400', 'teleCode': 'CSCD0900'}, headers={'origin': 'https://www.tving.com', 'Referer': 'https://www.tving.com/vod/player/C07381', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}, cookies = {'_tving_token': 'GZ2lHPOGpKyNhJY8FZgFmw%3D%3D', 'POC_USERINFO': 'aeSjz7IMYkx%2Fj0Ss7YLkzcPMJAQnttf5uFn1sdCanThpnYhJFsxWcAn6UDS2BeBvOSgrDXYFD5vQgt%2BteF9K5vesy60ntBs0BgcPN9kt5Vjwi%2BYnUFMRao0ggX%2BGaH3oK69ZTUxC7Bq9yq3hrffbKSSfdfHlcn9fZ4E%2BgYdi8VkycY7rFSWfWCRg4y7S6WkmePnc0oBWVz7n7E5Owfw3sSlIFEqlxD%2BhJtagzPbWR6PGUrRgXvUTFjKJy4kLzOIbT2pdtprGKHXCWTz87WjpjE7SkuJnblay6iD7L%2Fq%2FL1zevsW%2BLzihmDmQAY%2BraNExwxhpVZd2jYQxknpUO%2FjL%2FEwIjRR8uLxoOuDMp6Kbir3QZyAhjIjCGWyqRJhelRuAxn1qBPWDMBc6jXJP3%2BDKgGQ8iIHvVYmSAaZ6bjl%2BbwRFeCNRTREXbjBw03E%2F2GG2%2BZXyoZR3iXLnJQ00c3MFVw240OpLzGUu0NdtQVumdLZ868dEcqWIaPErjPlCspllZZvJrSGbhdXaGfp%2Bm6gLzFp8H0LVAYSl0a6IwaMA5qEtRPJRCCl1biSFh%2BOzuCSBCnZBmASb2aC5jw0KspfWy%2BLG4XfZ4ej26ae9yrL3NkqIU9y1eTI4NKeC2yh2bivY7iK%2BXwR9C6aW%2FOFZ5mFk3mOtQX%2F70HCaf8AyX97WrxY%3D', 'onClickEvent2': 'composed%3Dfalse%5ECAPTURING_PHASE%3D1%5Ecancelable%3Dfalse%5EreturnValue%3Dtrue%5EcancelBubble%3Dfalse%5Ebubbles%3Dfalse%5EdefaultPrevented%3Dfalse%5ENONE%3D0%5EAT_TARGET%3D2%5EBUBBLING_PHASE%3D3%5EtimeStamp%3D2158.7350000045262%5EisTrusted%3Dfalse%5Etype%3DoocCreate%5EeventPhase%3D0%5E'} , )
    import urllib
    print (urllib.quote(ooc))
    res = requests.post(url, data=data, headers=headers, cookies = {'_tving_token': 'GZ2lHPOGpKyNhJY8FZgFmw%3D%3D', 'onClickEvent2': urllib.quote(ooc)})
    print(res.status_code)
    ret = res.text
    print(ret)
"""
# Created by pyminifier (https://github.com/liftoff/pyminifier)
