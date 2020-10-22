import os
W=None
I=True
R=False
A=Exception
B=object
P=staticmethod
n=enumerate
t=ord
f=range
i=len
m=list
F=reversed
x=sorted
q=int
import sys
import re
import traceback
import logging
logger=W
is_sjva=I
is_shell=I
is_plex=I
try:
 import requests
 import lxml.html
 is_plex=R
except:
 is_sjva=R
 is_shell=R
from framework import py_urllib,app
try:
 from framework.util import Util
 package_name=__name__.split('.')[0]
 logger=logging.getLogger(package_name)
 is_shell=R
except:
 is_sjva=R
if is_shell:
 logger=logging.getLogger(__name__)
 logger.setLevel(logging.INFO)
 logger.addHandler(logging.StreamHandler())
def log_debug(msg,*args,**kwargs):
 if logger is not W:
  logger.debug(msg,*args,**kwargs)
 else:
  Log(msg,*args,**kwargs)
def log_error(msg,*args,**kwargs):
 if logger is not W:
  logger.error(msg,*args,**kwargs)
 else:
  Log(msg,*args,**kwargs)
def get_json(url):
 try:
  if is_plex:
   return JSON.ObjectFromURL(url)
  else:
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   return session.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies()).json()
 except A as e:
  log_error('Exception:%s',e)
  log_error(traceback.format_exc()) 
def get_html(url):
 try:
  if is_plex:
   return HTML.ElementFromURL(url)
  else:
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   return lxml.html.document_fromstring(requests.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies()).text)
 except A as e:
  log_error('Exception:%s',e)
  log_error(traceback.format_exc())
class MovieSearch(B):
 @P
 def search_movie(movie_name,movie_year):
  try:
   movie_year='%s'%movie_year
   movie_list=[]
   split_index=-1
   is_include_kor=R
   for index,c in n(movie_name):
    if app.config['config']['is_py2']:
     if t(u'가')<=t(c)<=t(u'힣'):
      is_include_kor=I
      split_index=-1
     elif t('a')<=t(c.lower())<=t('z'):
      is_include_eng=I
      if split_index==-1:
       split_index=index
     elif t('0')<=t(c.lower())<=t('9')or t(' '):
      pass
     else:
      split_index=-1
    else:
     if(u'가')<=(c)<=(u'힣'):
      is_include_kor=I
      split_index=-1
     elif('a')<=(c.lower())<=('z'):
      is_include_eng=I
      if split_index==-1:
       split_index=index
     elif('0')<=(c.lower())<=('9')or(' '):
      pass
     else:
      split_index=-1
   if is_include_kor and split_index!=-1:
    kor=movie_name[:split_index].strip()
    eng=movie_name[split_index:].strip()
   else:
    kor=W
    eng=W
   log_debug('SEARCH_MOVIE : [%s] [%s] [%s] [%s]'%(movie_name,is_include_kor,kor,eng))
   movie_list=MovieSearch.search_movie_web(movie_list,movie_name,movie_year)
   if movie_list and movie_list[0]['score']==100:
    log_debug('SEARCH_MOVIE STEP 1 : %s'%movie_list)
    return is_include_kor,movie_list
   if kor is not W:
    movie_list=MovieSearch.search_movie_web(movie_list,kor,movie_year)
    if movie_list and movie_list[0]['score']==100:
     log_debug('SEARCH_MOVIE STEP 2 : %s'%movie_list)
     return is_include_kor,movie_list
   if eng is not W:
    movie_list=MovieSearch.search_movie_web(movie_list,eng,movie_year)
    if movie_list and movie_list[0]['score']==100:
     log_debug('SEARCH_MOVIE STEP 3 : %s'%movie_list)
     return is_include_kor,movie_list
   if kor is not W:
    tmps=kor.split(' ')
    index=-1
    for i in f(i(tmps)):
     if app.config['config']['is_py2']:
      if t(u'가')<=t(tmps[i][0])<=t(u'힣')or t('0')<=t(tmps[i][0])<=t('9'):
       pass
      else:
       index=i
       break
     else:
      if(u'가')<=(tmps[i][0])<=(u'힣')or('0')<=(tmps[i][0])<=('9'):
       pass
      else:
       index=i
       break
    if index!=-1:
     movie_list=MovieSearch.search_movie_web(movie_list,' '.join(tmps[:index]),movie_year)
     if movie_list and movie_list[0]['score']==100:
      log_debug('SEARCH_MOVIE STEP 4 : %s'%movie_list)
      return is_include_kor,movie_list
   if is_plex==R:
    if movie_list and movie_list[0]['score']==95:
     movie_list=MovieSearch.search_movie_web(movie_list,movie_list[0]['title'],movie_year)
     if movie_list and movie_list[0]['score']==100:
      log_debug('SEARCH_MOVIE STEP 5 : %s'%movie_list)
      return is_include_kor,movie_list
   if is_include_kor==R:
    movie=MovieSearch.search_imdb(movie_name.lower(),movie_year)
    if movie is not W:
     movie_list=MovieSearch.search_movie_web(movie_list,movie['title'],movie_year)
     if movie_list and movie_list[0]['score']==100:
      log_debug('SEARCH_MOVIE STEP IMDB : %s'%movie_list)
      return is_include_kor,movie_list
   log_debug('SEARCH_MOVIE STEP LAST : %s'%movie_list)
  except A as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc()) 
  return is_include_kor,movie_list
 @P
 def movie_append(movie_list,data):
  try:
   exist_data=W
   for tmp in movie_list:
    if tmp['id']==data['id']:
     exist_data=tmp
     break
   if exist_data is not W:
    movie_list.remove(exist_data)
   movie_list.append(data)
  except A as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc()) 
 @P
 def get_movie_info_from_home(url):
  try:
   html=get_html(url)
   movie=W
   try:
    movie=html.get_element_by_id('movieEColl')
   except A as e:
    pass
   if movie is W:
    return W
   title_tag=movie.get_element_by_id('movieTitle')
   a_tag=title_tag.find('a')
   href=a_tag.attrib['href']
   title=a_tag.find('b').text_content()
   tmp=title_tag.text_content()
   tmp_year=''
   match=re.compile(r'(?P<year>\d{4})\s제작').search(tmp)
   more={}
   if match:
    tmp_year=match.group('year')
    more['eng_title']=tmp.replace(title,'').replace(tmp_year,'').replace(u'제작','').replace(u',','').strip()
   country_tag=movie.xpath('//div[3]/div/div[1]/div[2]/dl[1]/dd[2]')
   country=''
   if country_tag:
    country=country_tag[0].text_content().split('|')[0].strip()
    logger.debug(country)
   more['poster']=movie.xpath('//*[@id="nmovie_img_0"]/a/img')[0].attrib['src']
   more['title']=movie.xpath('//*[@id="movieTitle"]/span')[0].text_content()
   tmp=movie.xpath('//*[@id="movieEColl"]/div[3]/div/div[1]/div[2]/dl')
   more['info']=[]
   more['info'].append(country_tag[0].text_content().strip())
   logger.debug(more['info'][0])
   tmp=more['info'][0].split('|')
   if i(tmp)==5:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=tmp[2].replace(u'개봉','').strip()
    more['rate']=tmp[3].strip()
    more['during']=tmp[4].strip()
   elif i(tmp)==4:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=''
    more['rate']=tmp[2].strip()
    more['during']=tmp[3].strip()
   elif i(tmp)==3:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=''
    more['rate']=''
    more['during']=tmp[2].strip()
   daum_id=href.split('=')[1]
   return{'movie':movie,'title':title,'daum_id':daum_id,'year':tmp_year,'country':country,'more':more}
  except A as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc()) 
 @P
 def search_movie_web(movie_list,movie_name,movie_year):
  try:
   url='https://suggest-bar.daum.net/suggest?id=movie&cate=movie&multiple=1&mod=json&code=utf_in_out&q=%s'%(py_urllib.quote(movie_name.encode('utf8')))
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   res=session.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies())
   data=res.json()
   for index,item in n(data['items']['movie']):
    tmps=item.split('|')
    score=85-(index*5)
    if tmps[0].find(movie_name)!=-1 and tmps[3]==movie_year:
     score=95
    elif tmps[3]==movie_year:
     score=score+5
    if score<10:
     score=10
    MovieSearch.movie_append(movie_list,{'id':tmps[1],'title':tmps[0],'year':tmps[3],'score':score})
  except A as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc())
  try:
   url='https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=%s%s'%('%EC%98%81%ED%99%94+',py_urllib.quote(movie_name.encode('utf8')))
   ret=MovieSearch.get_movie_info_from_home(url)
   if ret is not W:
    if ret['year']==movie_year:
     score=100
     need_another_search=R
    else:
     score=90
     need_another_search=I
    MovieSearch.movie_append(movie_list,{'id':ret['daum_id'],'title':ret['title'],'year':ret['year'],'score':score,'country':ret['country'],'more':ret['more']})
    log_debug('need_another_search : %s'%need_another_search)
    movie=ret['movie']
    if need_another_search:
     tmp=movie.find('div[@class="coll_etc"]')
     if tmp is not W:
      tag_list=tmp.findall('.//a')
      first_url=W
      for tag in tag_list:
       match=re.compile(r'(.*?)\((.*?)\)').search(tag.text_content())
       if match:
        daum_id=tag.attrib['href'].split('||')[1]
        score=80
        if match.group(1)==movie_name and match.group(2)==movie_year:
         first_url='https://search.daum.net/search?%s'%tag.attrib['href']
        elif match.group(2)==movie_year and first_url is not W:
         first_url='https://search.daum.net/search?%s'%tag.attrib['href']
        MovieSearch.movie_append(movie_list,{'id':daum_id,'title':match.group(1),'year':match.group(2),'score':score})
      log_debug('first_url : %s'%first_url)
      if need_another_search and first_url is not W:
       new_ret=MovieSearch.get_movie_info_from_home(first_url)
       MovieSearch.movie_append(movie_list,{'id':new_ret['daum_id'],'title':new_ret['title'],'year':new_ret['year'],'score':100,'country':new_ret['country'],'more':new_ret['more']})
     tmp=movie.find('.//ul[@class="list_thumb list_few"]')
     log_debug('SERIES:%s'%tmp)
     if tmp is not W:
      tag_list=tmp.findall('.//div[@class="wrap_cont"]')
      first_url=W
      score=80
      for tag in tag_list:
       a_tag=tag.find('a')
       daum_id=a_tag.attrib['href'].split('||')[1]
       daum_name=a_tag.text_content()
       span_tag=tag.find('span')
       year=span_tag.text_content()
       log_debug('daum_id:%s %s %s'%(daum_id,year,daum_name))
       if daum_name==movie_name and year==movie_year:
        first_url='https://search.daum.net/search?%s'%a_tag.attrib['href']
       elif year==movie_year and first_url is not W:
        first_url='https://search.daum.net/search?%s'%tag.attrib['href']
       MovieSearch.movie_append(movie_list,{'id':daum_id,'title':daum_name,'year':year,'score':score})
       log_debug('first_url : %s'%first_url)
      if need_another_search and first_url is not W:
       new_ret=MovieSearch.get_movie_info_from_home(first_url)
       MovieSearch.movie_append(movie_list,{'id':new_ret['daum_id'],'title':new_ret['title'],'year':new_ret['year'],'score':100,'country':new_ret['country'],'more':new_ret['more']})
  except A as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc())
  movie_list=m(F(x(movie_list,key=lambda k:k['score'])))
  return movie_list
 @P
 def search_imdb(title,year):
  try:
   year=q(year)
   title=title.replace(' ','_')
   url='https://v2.sg.media-imdb.com/suggestion/%s/%s.json'%(title[0],title)
   tmp=get_json(url)
   if 'd' in tmp:
    for t in tmp['d']:
     title_imdb=t['l'].lower().replace("'",'').replace(':','').replace('&','and').replace('?','')
     if title.lower().replace("'",'').replace('.',' ').replace('_',' ')==title_imdb and 'y' in t and t['y']==year:
      return{'id':t['id'],'title':t['l'],'year':year,'score':100}
  except A as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
