import os
import traceback
import sys
import requests
import time
import json
import base64
session=requests.session()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36','Accept':'application/json, text/plain, */*','Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7','origin':'https://www.tving.com','referer':'https://www.tving.com/live/player/C07381','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin',}
config={'token':None,'param':"&free=all&lastFrequency=y&order=broadDate",'program_param':'&free=all&order=frequencyDesc&programCode=%s','default_param':'&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610'}
import requests
def get_stream_info():
 print('aaa')
 url='https://www.tving.com/streaming/info'
 ooc='isTrusted=false^type=oocCreate^eventPhase=0^bubbles=false^cancelable=false^defaultPrevented=false^composed=false^timeStamp=4459.404999972321^returnValue=true^cancelBubble=false^NONE=0^CAPTURING_PHASE=1^AT_TARGET=2^BUBBLING_PHASE=3^'
 ooc='composed=false^CAPTURING_PHASE=1^cancelable=false^returnValue=true^cancelBubble=false^bubbles=false^defaultPrevented=false^NONE=0^AT_TARGET=2^BUBBLING_PHASE=3^timeStamp=2158.7350000045262^isTrusted=false^type=oocCreate^eventPhase=0'
 data={'apiKey':'1e7952d0917d6aab1f0293a063697610','info':'Y','networkCode':'CSND0900','osCode':'CSOD0400','teleCode':'CSCD0900','mediaCode':'C07381','screenCode':'CSSD0100','callingFrom':'HTML5','streamCode':'stream40','deviceId':'18747739','adReq':'adproxy','ooc':ooc}
 url2="http://api.tving.com/v1/user/device/list?model=PC&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610"
 res2=requests.get(url2,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'},cookies={'_tving_token':'GZ2lHPOGpKyNhJY8FZgFmw%3D%3D','POC_USERINFO':'aeSjz7IMYkx%2Fj0Ss7YLkzcPMJAQnttf5uFn1sdCanThpnYhJFsxWcAn6UDS2BeBvOSgrDXYFD5vQgt%2BteF9K5vesy60ntBs0BgcPN9kt5Vjwi%2BYnUFMRao0ggX%2BGaH3oK69ZTUxC7Bq9yq3hrffbKSSfdfHlcn9fZ4E%2BgYdi8VkycY7rFSWfWCRg4y7S6WkmePnc0oBWVz7n7E5Owfw3sSlIFEqlxD%2BhJtagzPbWR6PGUrRgXvUTFjKJy4kLzOIbT2pdtprGKHXCWTz87WjpjE7SkuJnblay6iD7L%2Fq%2FL1zevsW%2BLzihmDmQAY%2BraNExwxhpVZd2jYQxknpUO%2FjL%2FEwIjRR8uLxoOuDMp6Kbir3QZyAhjIjCGWyqRJhelRuAxn1qBPWDMBc6jXJP3%2BDKgGQ8iIHvVYmSAaZ6bjl%2BbwRFeCNRTREXbjBw03E%2F2GG2%2BZXyoZR3iXLnJQ00c3MFVw240OpLzGUu0NdtQVumdLZ868dEcqWIaPErjPlCspllZZvJrSGbhdXaGfp%2Bm6gLzFp8H0LVAYSl0a6IwaMA5qEtRPJRCCl1biSFh%2BOzuCSBCnZBmASb2aC5jw0KspfWy%2BLG4XfZ4ej26ae9yrL3NkqIU9y1eTI4NKeC2yh2bivY7iK%2BXwR9C6aW%2FOFZ5mFk3mOtQX%2F70HCaf8AyX97WrxY%3D'})
 print(res2.text)
 import time
 print(time.time())
 return
 import urllib
 print(urllib.quote(ooc))
 res=requests.post(url,data=data,headers=headers,cookies={'_tving_token':'GZ2lHPOGpKyNhJY8FZgFmw%3D%3D','onClickEvent2':urllib.quote(ooc)})
 print(res.status_code)
 ret=res.text
 print(ret)
"""
 'isTrusted' : 'false'
 , 'NONE' : '0'
 , 'CAPTURING_PHASE' : '1'
 , 'AT_TARGET' : '2'
 , 'BUBBLING_PHASE' : '3'
 , 'type' : 'oocCreate'
 , 'eventPhase' : '0'
 , 'bubbles' : 'false'
 , 'cancelable' : 'false'
 , 'defaultPrevented' : 'false'
 , 'composed' : 'false'
 , 'timeStamp' : '2158.7350000045262'
 , 'returnValue' : 'true'
 , 'cancelBubble' : 'false'
 }
"""
get_stream_info()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
