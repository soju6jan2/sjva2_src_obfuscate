import os
n=staticmethod
X=None
V=int
j=Exception
D=False
q=len
F=abs
d=round
s=float
u=sorted
from datetime import datetime
B=datetime.now
import traceback
N=traceback.format_exc
import logging
import subprocess
import time
import re
J=re.sub
M=re.compile
import threading
import json
import requests
import lxml.html
from enum import Enum
from framework import py_urllib
o=py_urllib.unquote
v=py_urllib.quote
from framework.common.daum import logger
L=logger.error
f=logger.debug
_REGEX_FILENAME=r'^(?P<name>.*?)\.E(?P<no>\d+)(\-E\d{1,4})?\.?(END\.)?(?P<date>\d{6})\.(?P<etc>.*?)(?P<quality>\d+)[p|P](\-?(?P<release>.*?))?(\.(.*?))?$'
_REGEX_FILENAME_NO_EPISODE_NUMBER=r'^(?P<name>.*?)\.(E(?P<no>\d+)\.?)?(END\.)?(?P<date>\d{6})\.(?P<etc>.*?)(?P<quality>\d+)[p|P](\-?(?P<release>.*?))?(\.(.*?))?$'
_REGEX_FILENAME_RENAME=r'(?P<title>.*?)[\s\.]E?(?P<no>\d{1,2})[\-\~\s\.]?E?\d{1,2}'
class DaumTV:
 @n
 def check_filename(filename):
  f('check_filename filename : %s',filename)
  try:
   ret=X
   match1=M(_REGEX_FILENAME).match(filename)
   match2=M(_REGEX_FILENAME_NO_EPISODE_NUMBER).match(filename)
   for regex in[_REGEX_FILENAME,_REGEX_FILENAME_NO_EPISODE_NUMBER]:
    match=M(regex).match(filename)
    if match:
     f('QQQQQQQQQQQ')
     ret={}
     ret['title']=match1.group('name')
     ret['no']=match1.group('no')
     ret['date']=match1.group('date')
     ret['etc']=match1.group('etc').replace('.','')
     ret['quality']=match1.group('quality')
     ret['release']=X
     if 'release' in match1.groupdict():
      ret['release']=match1.group('release')
     else:
      ret['release']=X
     if ret['no']is not X and ret['no']!='':
      ret['no']=V(ret['no'])
     else:
      ret['no']=-1
     return DaumTV.change_filename_continous_episode(ret)
  except j as e:
   L('Exception:%s',e)
   L(N())
 @n 
 def change_filename_continous_episode(ret):
  try:
   if ret['title'].find(u'합')==-1:
    return ret
   match=M(_REGEX_FILENAME_RENAME).match(ret['title'])
   if match:
    f(u'합본 : %s',ret['filename'])
    ret['title']=match.group('title').strip()
    if ret['no']==-1:
     ret['no']=V(match.group('no'))
   return ret
  except j as e:
   L('Exception:%s',e)
   L(N())
 @n
 def get_html(url):
  try:
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   res=session.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies())
   data=res.text
   return data
  except j as e:
   L('Exception:%s',e)
   L(N())
 @n
 def get_daum_tv_info(search_name,daum_id=X,on_home=D):
  try:
   entity={}
   search_name=DaumTV.get_search_name_from_original(search_name)
   if daum_id is not X:
    url='https://search.daum.net/search?w=tv&q=%s&irk=%s&irt=tv-program&DA=TVP'%(v(search_name.encode('utf8')),daum_id)
   else:
    url='https://search.daum.net/search?w=tv&q=%s'%(v(search_name.encode('utf8')))
   data=DaumTV.get_html(url)
   match=M(r'irk\=(?P<id>\d+)').search(data)
   root=lxml.html.fromstring(data)
   daum_id=match.group('id')if match else ''
   entity={}
   entity['daum_id']=daum_id
   items=root.xpath('//*[@id="tv_program"]/div[1]/div[2]/strong')
   if not items:
    return X
   if q(items)==1:
    entity['title']=items[0].text.strip()
    entity['title']=entity['title'].replace('?','').replace(':','')
   entity['status']=0
   items=root.xpath('//*[@id="tv_program"]/div[1]/div[2]/span')
   if items:
    if items[0].text.strip()==u'방송종료':
     entity['status']=1
    elif items[0].text.strip()==u'방송예정':
     entity['status']=2
   items=root.xpath('//*[@id="tv_program"]/div[1]/div[3]/span')
   if items:
    entity['studio']=items[0].text.strip()
    try:
     entity['broadcast_info']=items[1].text.strip()
    except:
     pass
    try:
     entity['broadcast_term']=items[2].text.strip()
    except:
     pass
    try:
     items=root.xpath('//*[@id="tv_program"]/div[1]/div[2]/span')
    except:
     pass
   else:
    if on_home:
     f('on_home : %s',search_name)
     xml_root=DaumTV.get_show_info_on_home_title(search_name,daum_id=daum_id)
     home_ret=DaumTV.get_show_info_on_home(xml_root)
     if home_ret:
      entity['studio']=home_ret['studio']
      entity['broadcast_info']=home_ret['broadcast_info']
      entity['broadcast_term']=home_ret['broadcast_term']
   try:
    match=M(r'(\d{4}\.\d{1,2}\.\d{1,2})~').search(entity['broadcast_term'])
    if match:
     entity['start_date']=match.group(1)
   except:
    pass
   items=root.xpath('//*[@id="tv_program"]/div[1]/dl[1]/dd')
   if q(items)==1:
    entity['genre']=items[0].text.strip().split(' ')[0]
    entity['genre']=entity['genre'].split('(')[0].strip()
   items=root.xpath('//*[@id="tv_program"]/div[1]/dl[2]/dd')
   if q(items)==1:
    entity['summary']=items[0].text.replace('&nbsp',' ')
   items=root.xpath('//*[@id="tv_program"]/div[1]/div[1]/a/img')
   if q(items)==1:
    entity['poster_url']='https:%s'%items[0].attrib['src']
   items=root.xpath('//*[@id="clipDateList"]/li')
   entity['episode_list']={}
   if q(items)>300:
    items=items[q(items)-300:]
   today=V(B().strftime('%Y%m%d'))
   for item in items:
    try:
     a_tag=item.xpath('a')
     if q(a_tag)==1:
      span_tag=a_tag[0].xpath('span[@class="txt_episode"]')
      if q(span_tag)==1:
       if item.attrib['data-clip']in entity['episode_list']:
        if entity['episode_list'][item.attrib['data-clip']][0]==span_tag[0].text.strip().replace(u'회',''):
         pass
        else:
         idx=q(entity['episode_list'][item.attrib['data-clip']])-1
         _=F(V(entity['episode_list'][item.attrib['data-clip']][idx])-V(span_tag[0].text.strip().replace(u'회','')))
         if _<=4:
          if item.attrib['data-clip']!='' and today>=V(item.attrib['data-clip']):
           entity['last_episode_date']=item.attrib['data-clip']
           entity['last_episode_no']=span_tag[0].text.strip().replace(u'회','')
          entity['episode_list'][item.attrib['data-clip']].append(span_tag[0].text.strip().replace(u'회',''))
         else:
          pass
       else:
        if item.attrib['data-clip']!='' and today>=V(item.attrib['data-clip']):
         entity['last_episode_date']=item.attrib['data-clip']
         entity['last_episode_no']=span_tag[0].text.strip().replace(u'회','')
        entity['episode_list'][item.attrib['data-clip']]=[span_tag[0].text.strip().replace(u'회','')]
    except j as e:
     L('Exception:%s',e)
     L(N())
   try:
    if q(entity['episode_list']):
     entity['episode_count_one_day']=V(d(s(q(items))/q(entity['episode_list'])))
     if entity['episode_count_one_day']==0:
      entity['episode_count_one_day']=1
    else:
     entity['episode_count_one_day']=1
   except:
    entity['episode_count_one_day']=1
   f('daum tv len(entity.episode_list) : %s %s %s',q(items),q(entity['episode_list']),entity['episode_count_one_day'])
   return entity 
  except j as e:
   L('Exception:%s',e)
   L(N())
 @n
 def get_search_name_from_original(search_name):
  search_name=search_name.replace('일일연속극','').strip()
  search_name=search_name.replace('특별기획드라마','').strip()
  search_name=J(r'\[.*?\]','',search_name).strip()
  channel_list=['채널 A','채널A']
  for tmp in channel_list:
   if search_name.startswith(tmp):
    search_name=search_name.replace(tmp,'').strip()
  search_name=J(r'^.{2,3}드라마','',search_name).strip()
  search_name=J(r'^.{1,3}특집','',search_name).strip()
  return search_name
 @n
 def get_show_info(title,no=X,date=X):
  try:
   title=DaumTV.get_search_name_from_original(title)
   url='https://search.daum.net/search?q=%s'%(v(title.encode('utf8')))
   data=DaumTV.get_html(url)
   root=lxml.html.fromstring(data)
   home_info=DaumTV.get_show_info_on_home(root)
   tv=DaumTV.get_daum_tv_info(title)
   ret={'home':home_info,'tv':tv}
   return ret
  except j as e:
   L('Exception:%s',e)
   L(N())
 @n
 def get_show_info_on_home(root):
  try:
   tags=root.xpath('//*[@id="tvpColl"]/div[2]/div/div[1]/span/a')
   if q(tags)<1:
    return
   tag_index=q(tags)-1
   entity={}
   entity['title']=tags[tag_index].text
   f('22222get_show_info_on_home title: %s',entity['title'])
   match=M(r'q\=(?P<title>.*?)&').search(tags[tag_index].attrib['href'])
   if match:
    entity['title']=o(match.group('title'))
   entity['id']=M(r'irk\=(?P<id>\d+)').search(tags[tag_index].attrib['href']).group('id')
   entity['status']=1 
   tags=root.xpath('//*[@id="tvpColl"]/div[2]/div/div[1]/span/span')
   if q(tags)==1:
    if tags[0].text==u'방송종료':
     entity['status']=2
    elif tags[0].text==u'방송예정':
     entity['status']=0
   f('get_show_info_on_home status: %s',entity['status'])
   tags=root.xpath('//*[@id="tvpColl"]/div[2]/div/div[1]/div')
   entity['extra_info']=tags[0].text_content().strip()
   f('get_show_info_on_home extra_info: %s',entity['extra_info'])
   entity['studio']=''
   tags=root.xpath('//*[@id="tvpColl"]/div[2]/div/div[1]/div/a')
   if q(tags)==1:
    entity['studio']=tags[0].text
   else:
    tags=root.xpath('//*[@id="tvpColl"]/div[2]/div/div[1]/div/span[1]')
    if q(tags)==1:
     entity['studio']=tags[0].text
   f('get_show_info_on_home studio: %s',entity['studio'])
   tags=root.xpath('//*[@id="tvpColl"]/div[2]/div/div[1]/div/span')
   entity['extra_info_array']=[tag.text for tag in tags]
   entity['broadcast_info']=entity['extra_info_array'][-2].strip()
   entity['broadcast_term']=entity['extra_info_array'][-1].split(',')[-1].strip()
   entity['year']=M(r'(?P<year>\d{4})').search(entity['extra_info_array'][-1]).group('year')
   f('get_show_info_on_home 1: %s',entity['status'])
   entity['series']=[]
   entity['series'].append({'title':entity['title'],'id':entity['id'],'year':entity['year']})
   tags=root.xpath('//*[@id="tv_series"]/div/ul/li')
   if tags:
    try:
     more=root.xpath('//*[@id="tv_series"]/div/div/a')
     url=more[0].attrib['href']
     if not url.startswith('http'):
      url='https://search.daum.net/search%s'%url
     f('MORE URL : %s',url)
     if more[0].xpath('span')[0].text==u'시리즈 더보기':
      more_root=HTML.ElementFromURL(url)
      tags=more_root.xpath('//*[@id="series"]/ul/li')
    except j as e:
     f('Not More!')
     f(N())
    for tag in tags:
     dic={}
     dic['title']=tag.xpath('a')[0].text
     dic['id']=M(r'irk\=(?P<id>\d+)').search(tag.xpath('a')[0].attrib['href']).group('id')
     if tag.xpath('span'):
      dic['date']=tag.xpath('span')[0].text
      dic['year']=M(r'(?P<year>\d{4})').search(dic['date']).group('year')
     else:
      dic['year']=X
     entity['series'].append(dic)
    entity['series']=u(entity['series'],key=lambda k:V(k['id']))
   f('SERIES : %s',q(entity['series']))
   entity['equal_name']=[]
   tags=root.xpath(u'//div[@id="tv_program"]//dt[contains(text(),"동명 콘텐츠")]//following-sibling::dd')
   if tags:
    tags=tags[0].xpath('*')
    for tag in tags:
     if tag.tag=='a':
      dic={}
      dic['title']=tag.text
      dic['id']=M(r'irk\=(?P<id>\d+)').search(tag.attrib['href']).group('id')
     elif tag.tag=='span':
      match=M(r'\((?P<studio>.*?),\s*(?P<year>\d{4})?\)').search(tag.text)
      if match:
       dic['studio']=match.group('studio')
       dic['year']=match.group('year')
      elif tag.text==u'(동명프로그램)':
       entity['equal_name'].append(dic)
      elif tag.text==u'(동명회차)':
       continue
   f(entity)
   return entity
  except j as e:
   f('Exception get_show_info_by_html : %s',e)
   f(N())
 @n
 def get_show_info_on_home_title(title,daum_id=X):
  try:
   title=title.replace(u'[종영]','')
   if daum_id is X:
    url='https://search.daum.net/search?q=%s'%(v(title.encode('utf8')))
   else:
    url='https://search.daum.net/search?q=%s&irk=%s&irt=tv-program&DA=TVP'%(v(title.encode('utf8')),daum_id)
   return DaumTV.get_lxml_by_url(url)
  except j as e:
   L('Exception:%s',e)
   L(N())
 @n
 def get_lxml_by_url(url):
  try:
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   res=session.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies())
   data=res.text
   root=lxml.html.fromstring(data)
   return root
  except j as e:
   L('Exception:%s',e)
   L(N())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
