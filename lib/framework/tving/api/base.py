import os
N=None
g=Exception
m=len
a=True
t=False
w=ord
D=str
q=range
L=reversed
import traceback
import sys
import requests
import time
import json
import base64
from framework import app
from framework.logger import get_logger
from framework.util import Util
logger=get_logger('tving_api')
session=requests.session()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7','Referer':'',}
config={'token':N,'param':"&free=all&lastFrequency=y&order=broadDate",'program_param':'&free=all&order=frequencyDesc&programCode=%s','default_param':'&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610'}
def do_login(user_id,user_pw,login_type):
 try:
  url='https://user.tving.com/user/doLogin.tving'
  if login_type=='0':
   login_type_value='10'
  else:
   login_type_value='20'
  params={'userId':user_id,'password':user_pw,'loginType':login_type_value}
  res=session.post(url,data=params)
  cookie=res.headers['Set-Cookie']
  for c in cookie.split(','):
   c=c.strip()
   if c.startswith('_tving_token'):
    ret=c.split(';')[0]
    return ret
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_vod_list(p=N,page=1):
 try:
  url='http://api.tving.com/v1/media/episodes?pageNo=%s&pageSize=18&adult=all&guest=all&scope=all&personal=N'%page
  if p is not N:
   url+=p
  else:
   url+=config['param']
  url+=config['default_param']
  res=requests.get(url)
  return res.json()
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_episode_json_default(episode_code,quality,token,proxy=N):
 ts='%d'%time.time()
 if token is N:
  token=config['token']
 try:
  if quality=='stream70':
   tmp_param=config['default_param'].replace('CSSD0100','CSSD1200')
   url='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(tmp_param,ts,episode_code,quality) 
  else:
   url='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config['default_param'],ts,episode_code,quality)
  proxies=N
  if proxy is not N:
   proxies={"https":proxy,'http':proxy}
  headers['Cookie']=token
  r=session.get(url,headers=headers,proxies=proxies)
  data=r.json()
  url=data['body']['stream']['broadcast']['broad_url']
  logger.debug(url)
  decrypted_url=decrypt(episode_code,ts,url)
  logger.debug(decrypted_url)
  if decrypted_url.find('m3u8')==-1:
   decrypted_url=decrypted_url.replace('rtmp','http')
   decrypted_url=decrypted_url.replace('?','/playlist.m3u8?')
  if decrypted_url.find('smil/playlist.m3u8')!=-1 and decrypted_url.find('content_type=VOD')!=-1:
   tmps=decrypted_url.split('playlist.m3u8')
   r=session.get(decrypted_url,headers=headers,proxies=proxies)
   lines=r.text.split('\n')
   i=-1
   last=''
   while m(last)==0:
    last=lines[i].strip()
    i-=1
   decrypted_url='%s%s'%(tmps[0],last)
  return data,decrypted_url
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_episode_json_default_live(episode_code,quality,token,proxy=N,inc_quality=a):
 ts='%d'%time.time()
 if token is N:
  token=config['token']
 try:
  if inc_quality:
   url='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config['default_param'],ts,episode_code,quality)
  else:
   url='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&callingFrom=FLASH'%(config['default_param'],ts,episode_code)
  proxies=N
  if proxy is not N:
   proxies={"https":proxy,'http':proxy}
  headers['Cookie']=token
  r=session.get(url,headers=headers,proxies=proxies)
  data=r.json()
  url=data['body']['stream']['broadcast']['broad_url']
  decrypted_url=decrypt(episode_code,ts,url)
  if decrypted_url.find('.mp4')!=-1 and decrypted_url.find('/VOD/')!=-1:
   return data,decrypted_url
  if decrypted_url.find('Policy=')==-1:
   data,ret=get_episode_json_default_live(episode_code,quality,token,proxy=proxy,inc_quality=t)
   if quality=='stream50' and ret.find('live2000.smil'):
    ret=ret.replace('live2000.smil','live5000.smil')
    return data,ret
  return data,decrypted_url
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
"""
def get_episode_json_proxy(episode_code, quality, proxy_url, token):
    ts = '%d' % time.time()
    if token is None:
        token = config['token']
    try:
        #https://www.tving.com/streaming/info?networkCode=CSND0900&apiKey=1e7952d0917d6aab1f0293a063697610&ooc=composed%3Dfalse%5ECAPTURING_PHASE%3D1%5Ecancelable%3Dfalse%5EreturnValue%3Dtrue%5EcancelBubble%3Dfalse%5Ebubbles%3Dfalse%5EdefaultPrevented%3Dfalse%5ENONE%3D0%5EAT_TARGET%3D2%5EBUBBLING_PHASE%3D3%5EtimeStamp%3D2158.7350000045262%5EisTrusted%3Dfalse%5Etype%3DoocCreate%5EeventPhase%3D0%5E&screenCode=CSSD0100&callingFrom=HTML5&deviceId=2357832822&osCode=CSOD0900&teleCode=CSCD0900&info=Y&adReq=none&streamCode=stream50&mediaCode=E002837703
        if quality == 'stream70':
            tmp_param = config['default_param'].replace('CSSD0100', 'CSSD1200')
            url = 'http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH' % (tmp_param, ts, episode_code, quality)
        else:
            url = 'http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH' % (config['default_param'], ts, episode_code, quality)
        data = {'url' : url, 'cookie' : token}
        res = session.post(proxy_url, data=data)
        data = res.json()
        url = data['body']['stream']['broadcast']['broad_url']
        decrypted_url = decrypt(episode_code, ts, url)
        if decrypted_url.find('m3u8') == -1:
            decrypted_url = decrypted_url.replace('rtmp', 'http')
            decrypted_url = decrypted_url.replace('?', '/playlist.m3u8?')
        return data, decrypted_url
    except Exception as exception:
        logger.error('Exception:%s', exception)
        logger.error(traceback.format_exc())
"""
def get_episode_json(episode_code,quality,token,proxy=N,is_live=t):
 try:
  if is_live:
   return get_episode_json_default_live(episode_code,quality,token=token,proxy=proxy)
  else:
   return get_episode_json_default(episode_code,quality,token=token,proxy=proxy)
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def decrypt(code,key,value):
 try:
  from Crypto.Cipher import DES3 
  data=base64.decodestring(value.encode())
  cryptoCode='cjhv*tving**good/%s/%s'%(code[-3:],key)
  key=cryptoCode[:24]
  des3=DES3.new(key,DES3.MODE_ECB)
  ret=des3.decrypt(data)
  if app.config['config']['is_py2']:
   pad_len=w(ret[-1])
  else:
   pad_len=ret[-1]
  ret=ret[:-pad_len]
  return ret.decode()
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_filename(episode_data):
 try:
  title=episode_data["body"]["content"]["program_name"]
  title=title.replace("<","").replace(">","").replace("\\","").replace("/","").replace(":","").replace("*","").replace("\"","").replace("|","").replace("?","").replace("  "," ").strip()
  episodeno=episode_data["body"]["content"]["frequency"]
  airdate=D(episode_data["body"]["content"]["info"]["episode"]["broadcast_date"])[2:]
  currentQuality=N
  if episode_data["body"]["stream"]["quality"]is N:
   currentQuality="stream40"
  else:
   qualityCount=m(episode_data["body"]["stream"]["quality"])
   for i in q(qualityCount):
    if episode_data["body"]["stream"]["quality"][i]["selected"]=="Y":
     currentQuality=episode_data["body"]["stream"]["quality"][i]["code"]
     break
  if currentQuality is N:
   return
  qualityRes=get_quality_to_res(currentQuality)
  episodeno_str=D(episodeno)
  if episodeno<10:
   episodeno_str='0'+episodeno_str
  ret='%s.E%s.%s.%s-ST.mp4'%(title,episodeno_str,airdate,qualityRes)
  return ret
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_quality_to_tving(quality):
 if quality=='FHD':
  return 'stream50'
 elif quality=='HD':
  return 'stream40'
 elif quality=='SD':
  return 'stream30'
 elif quality=='UHD':
  return 'stream70'
 return 'stream50'
def get_quality_to_res(quality):
 if quality=='stream50':
  return '1080p'
 elif quality=='stream40':
  return '720p'
 elif quality=='stream30':
  return '480p'
 elif quality=='stream70':
  return '2160p'
 elif quality=='stream25':
  return '270p'
 return '1080p'
def get_live_list(list_type=0,order='rating'):
 if list_type==0:
  params=['&channelType=CPCS0100']
 elif list_type==1:
  params=['&channelType=CPCS0300']
 else:
  params=['&channelType=CPCS0100','&channelType=CPCS0300']
 ret=[]
 for param in params:
  page=1
  while a:
   hasMore,data=get_live_list2(param,page,order=order)
   for i in data:
    ret.append(i)
   if hasMore=='N':
    break
   page+=1
 return ret
def get_live_list2(param,page,order='rating'):
 has_more='N'
 try:
  result=[]
  url='http://api.tving.com/v1/media/lives?pageNo=%s&pageSize=20&order=%s&adult=all&free=all&guest=all&scope=all'%(page,order)
  if param is not N:
   url+=param
  url+=config['default_param'] 
  res=requests.get(url)
  data=res.json()
  for item in data["body"]["result"]:
   try:
    if item["live_code"]in['C07381','C05661','C44441','C04601','C07382']:
     continue
    info={}
    if a:
     info['id']=item["live_code"]
     info['title']=item['schedule']['channel']['name']['ko']
     info['episode_title']=' '
     info['img']='http://image.tving.com/upload/cms/caic/CAIC1900/%s.png'%item["live_code"]
     if item['schedule']['episode']is not N:
      info['episode_title']=item['schedule']['episode']['name']['ko']
      if info['title'].startswith('CH.')and m(item['schedule']['episode']['image'])>0:
       info['img']='http://image.tving.com'+item['schedule']['episode']['image'][0]['url']
     info['free']=(item['schedule']['broadcast_url'][0]['broad_url1'].find('drm')==-1)
     info['summary']=info['episode_title']
    result.append(info)
   except g as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  has_more=data["body"]["has_more"]
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
 return has_more,result
def get_movie_json(code,deviceid,token,proxy=N):
 ts='%d'%time.time()
 if token is N:
  token=config['token']
 try:
  quality='stream70'
  if quality=='stream70':
   tmp_param=config['default_param'].replace('CSSD0100','CSSD1200')
   url='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(tmp_param,ts,code,quality) 
  else:
   url='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config['default_param'],ts,code,quality)
  url+='&deviceId=%s'%deviceid
  proxies=N
  if proxy is not N:
   proxies={"https":proxy,'http':proxy}
  headers['Cookie']=token
  r=session.get(url,headers=headers,proxies=proxies)
  data=r.json()
  logger.debug(data)
  data['ret']={}
  if data['body']['result']['code']=="000":
   if '4k_nondrm_url' in data['body']['stream']['broadcast']:
    decrypted_url=decrypt(code,ts,data['body']['stream']['broadcast']['4k_nondrm_url'])
    if decrypted_url.find('5000k_PC.mp4')!=-1:
     data['ret']['ret']='ok'
     data['ret']['decrypted_url']=decrypted_url
     data['ret']['filename']=Util.change_text_for_use_filename('%s.%s.%s.2160p-ST.mp4'%(data['body']['content']['info']['movie']['name']['ko'],D(data['body']['content']['info']['movie']['release_date'])[:4],data['body']['content']['info']['movie']['name']['en']))
    else:
     data['ret']['ret']='no_4k'
     data['ret']['decrypted_url']=decrypted_url
  else:
   data['ret']['ret']='need_pay'
  return data
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_prefer_url(url):
 try:
  response=session.get(url,headers=config['headers'])
  data=response.text.strip()
  last_url=N
  for t in L(data.split('\n')):
   if t.strip().find('chunklist.m3u8')!=-1:
    last_url=t
    break
  if last_url is not N and last_url!='':
   last_url=url.split('chunklist')[0]+last_url
   return last_url
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
 return url
def get_vod_list2(param=N,page=1,genre='all'):
 try:
  url='https://api.tving.com/v2/media/episodes?pageNo=%s&pageSize=24&order=new&adult=all&free=all&guest=all&scope=all&lastFrequency=y&personal=N'%(page)
  if genre!='all':
   url+='&categoryCode=%s'%genre
  if param is not N:
   url+=param
  url+=config['default_param']
  res=requests.get(url)
  return res.json()
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_program_programid(programid):
 try:
  url='https://api.tving.com/v2/media/program/%s?pageNo=1&pageSize=10&order=name'%programid
  url+=config['default_param']
  res=requests.get(url)
  return res.json()
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_frequency_programid(programid,page=1):
 try:
  url='https://api.tving.com/v2/media/frequency/program/%s?pageNo=%s&pageSize=10&order=new&free=all&adult=all&scope=all'%(programid,page)
  url+=config['default_param']
  res=requests.get(url)
  return res.json()
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_movies(page=1,category='all'):
 try:
  url='https://api.tving.com/v2/media/movies?pageNo=%s&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&productPackageCode=338723&personal=N&diversityYn=N'%(page)
  if category!='all':
   url+='&multiCategoryCode=%s'%category
  url+=config['default_param']
  res=requests.get(url)
  return res.json()
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
"""
https://api.tving.com/v2/media/movies?pageNo=1&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&personal=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489117&drm_yn=N
https://api.tving.com/v2/media/movies?callback=jQuery112307642887056924332_1603081489114&pageNo=1&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&productPackageCode=1513561%2C338723&personal=N&diversityYn=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489120
https://api.tving.com/v2/media/movies?callback=jQuery112307642887056924332_1603081489114&pageNo=1&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&productPackageCode=338723&multiCategoryCode=MG100%2CMG190%2CMG230%2CMG270%2CMG290&personal=N&diversityYn=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489122
https://api.tving.com/v2/media/movies?callback=jQuery112307642887056924332_1603081489114&pageNo=1&pageSize=24&order=new&free=all&adult=all&guest=all&scope=all&productPackageCode=338723&personal=N&diversityYn=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489123
&multiCategoryCode=MG100%2CMG190%2CMG230%2CMG270%2CMG290  %2C = ,
"""
def get_movie_json2(code,deviceid,token,proxy=N,quality='stream50'):
 ts='%d'%time.time()
 if token is N:
  token=config['token']
 try:
  url='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config['default_param'],ts,code,quality)
  url+='&deviceId=%s'%deviceid
  proxies=N
  if proxy is not N:
   proxies={"https":proxy,'http':proxy}
  headers['Cookie']=token
  r=session.get(url,headers=headers,proxies=proxies)
  data=r.json()
  if 'broad_url' in data['body']['stream']['broadcast']:
   data['body']['decrypted_url']=decrypt(code,ts,data['body']['stream']['broadcast']['broad_url'])
  return data
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def get_schedules(code,date,start_time,end_time):
 try:
  url='https://api.tving.com/v2/media/schedules?pageNo=1&pageSize=20&order=chno&scope=all&adult=n&free=all&broadDate=%s&broadcastDate=%s&startBroadTime=%s&endBroadTime=%s&channelCode=%s'%(date,date,start_time,end_time,','.join(code))
  url+=config['default_param']
  res=requests.get(url)
  return res.json()
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
