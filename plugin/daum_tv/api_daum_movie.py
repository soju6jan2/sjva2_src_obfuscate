import os
I=None
Q=True
r=False
G=Exception
T=object
V=staticmethod
y=enumerate
j=ord
m=range
f=len
H=list
X=reversed
L=sorted
a=int
import sys
import re
import traceback
import logging
logger=I
is_sjva=Q
is_shell=Q
is_plex=Q
try:
 import requests
 import lxml.html
 is_plex=r
except:
 is_sjva=r
 is_shell=r
from framework import py_urllib,app
try:
 from framework.util import Util
 package_name=__name__.split('.')[0]
 logger=logging.getLogger(package_name)
 is_shell=r
except:
 is_sjva=r
if is_shell:
 logger=logging.getLogger(__name__)
 logger.setLevel(logging.INFO)
 logger.addHandler(logging.StreamHandler())
def log_debug(msg,*args,**kwargs):
 if logger is not I:
  logger.debug(msg,*args,**kwargs)
 else:
  Log(msg,*args,**kwargs)
def log_error(msg,*args,**kwargs):
 if logger is not I:
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
 except G as e:
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
 except G as e:
  log_error('Exception:%s',e)
  log_error(traceback.format_exc())
class MovieSearch(T):
 @V
 def search_movie(movie_name,movie_year):
  try:
   movie_year='%s'%movie_year
   movie_list=[]
   split_index=-1
   is_include_kor=r
   for index,c in y(movie_name):
    if app.config['config']['is_py2']:
     if j(u'가')<=j(c)<=j(u'힣'):
      is_include_kor=Q
      split_index=-1
     elif j('a')<=j(c.lower())<=j('z'):
      is_include_eng=Q
      if split_index==-1:
       split_index=index
     elif j('0')<=j(c.lower())<=j('9')or j(' '):
      pass
     else:
      split_index=-1
    else:
     if(u'가')<=(c)<=(u'힣'):
      is_include_kor=Q
      split_index=-1
     elif('a')<=(c.lower())<=('z'):
      is_include_eng=Q
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
    kor=I
    eng=I
   log_debug('SEARCH_MOVIE : [%s] [%s] [%s] [%s]'%(movie_name,is_include_kor,kor,eng))
   movie_list=MovieSearch.search_movie_web(movie_list,movie_name,movie_year)
   if movie_list and movie_list[0]['score']==100:
    log_debug('SEARCH_MOVIE STEP 1 : %s'%movie_list)
    return is_include_kor,movie_list
   if kor is not I:
    movie_list=MovieSearch.search_movie_web(movie_list,kor,movie_year)
    if movie_list and movie_list[0]['score']==100:
     log_debug('SEARCH_MOVIE STEP 2 : %s'%movie_list)
     return is_include_kor,movie_list
   if eng is not I:
    movie_list=MovieSearch.search_movie_web(movie_list,eng,movie_year)
    if movie_list and movie_list[0]['score']==100:
     log_debug('SEARCH_MOVIE STEP 3 : %s'%movie_list)
     return is_include_kor,movie_list
   if kor is not I:
    tmps=kor.split(' ')
    index=-1
    for i in m(f(tmps)):
     if app.config['config']['is_py2']:
      if j(u'가')<=j(tmps[i][0])<=j(u'힣')or j('0')<=j(tmps[i][0])<=j('9'):
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
   if is_plex==r:
    if movie_list and movie_list[0]['score']==95:
     movie_list=MovieSearch.search_movie_web(movie_list,movie_list[0]['title'],movie_year)
     if movie_list and movie_list[0]['score']==100:
      log_debug('SEARCH_MOVIE STEP 5 : %s'%movie_list)
      return is_include_kor,movie_list
   if is_include_kor==r:
    movie=MovieSearch.search_imdb(movie_name.lower(),movie_year)
    if movie is not I:
     movie_list=MovieSearch.search_movie_web(movie_list,movie['title'],movie_year)
     if movie_list and movie_list[0]['score']==100:
      log_debug('SEARCH_MOVIE STEP IMDB : %s'%movie_list)
      return is_include_kor,movie_list
   log_debug('SEARCH_MOVIE STEP LAST : %s'%movie_list)
  except G as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc()) 
  return is_include_kor,movie_list
 @V
 def movie_append(movie_list,data):
  try:
   exist_data=I
   for tmp in movie_list:
    if tmp['id']==data['id']:
     exist_data=tmp
     break
   if exist_data is not I:
    movie_list.remove(exist_data)
   movie_list.append(data)
  except G as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc()) 
 @V
 def get_movie_info_from_home(url):
  try:
   html=get_html(url)
   movie=I
   try:
    movie=html.get_element_by_id('movieEColl')
   except G as e:
    pass
   if movie is I:
    return I
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
   if f(tmp)==5:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=tmp[2].replace(u'개봉','').strip()
    more['rate']=tmp[3].strip()
    more['during']=tmp[4].strip()
   elif f(tmp)==4:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=''
    more['rate']=tmp[2].strip()
    more['during']=tmp[3].strip()
   elif f(tmp)==3:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=''
    more['rate']=''
    more['during']=tmp[2].strip()
   daum_id=href.split('=')[1]
   return{'movie':movie,'title':title,'daum_id':daum_id,'year':tmp_year,'country':country,'more':more}
  except G as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc()) 
 @V
 def search_movie_web(movie_list,movie_name,movie_year):
  try:
   url='https://suggest-bar.daum.net/suggest?id=movie&cate=movie&multiple=1&mod=json&code=utf_in_out&q=%s'%(py_urllib.quote(movie_name.encode('utf8')))
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   res=session.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies())
   data=res.json()
   for index,item in y(data['items']['movie']):
    tmps=item.split('|')
    score=85-(index*5)
    if tmps[0].find(movie_name)!=-1 and tmps[3]==movie_year:
     score=95
    elif tmps[3]==movie_year:
     score=score+5
    if score<10:
     score=10
    MovieSearch.movie_append(movie_list,{'id':tmps[1],'title':tmps[0],'year':tmps[3],'score':score})
  except G as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc())
  try:
   url='https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=%s%s'%('%EC%98%81%ED%99%94+',py_urllib.quote(movie_name.encode('utf8')))
   ret=MovieSearch.get_movie_info_from_home(url)
   if ret is not I:
    if ret['year']==movie_year:
     score=100
     need_another_search=r
    else:
     score=90
     need_another_search=Q
    MovieSearch.movie_append(movie_list,{'id':ret['daum_id'],'title':ret['title'],'year':ret['year'],'score':score,'country':ret['country'],'more':ret['more']})
    log_debug('need_another_search : %s'%need_another_search)
    movie=ret['movie']
    if need_another_search:
     tmp=movie.find('div[@class="coll_etc"]')
     if tmp is not I:
      tag_list=tmp.findall('.//a')
      first_url=I
      for tag in tag_list:
       match=re.compile(r'(.*?)\((.*?)\)').search(tag.text_content())
       if match:
        daum_id=tag.attrib['href'].split('||')[1]
        score=80
        if match.group(1)==movie_name and match.group(2)==movie_year:
         first_url='https://search.daum.net/search?%s'%tag.attrib['href']
        elif match.group(2)==movie_year and first_url is not I:
         first_url='https://search.daum.net/search?%s'%tag.attrib['href']
        MovieSearch.movie_append(movie_list,{'id':daum_id,'title':match.group(1),'year':match.group(2),'score':score})
      log_debug('first_url : %s'%first_url)
      if need_another_search and first_url is not I:
       new_ret=MovieSearch.get_movie_info_from_home(first_url)
       MovieSearch.movie_append(movie_list,{'id':new_ret['daum_id'],'title':new_ret['title'],'year':new_ret['year'],'score':100,'country':new_ret['country'],'more':new_ret['more']})
     tmp=movie.find('.//ul[@class="list_thumb list_few"]')
     log_debug('SERIES:%s'%tmp)
     if tmp is not I:
      tag_list=tmp.findall('.//div[@class="wrap_cont"]')
      first_url=I
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
       elif year==movie_year and first_url is not I:
        first_url='https://search.daum.net/search?%s'%tag.attrib['href']
       MovieSearch.movie_append(movie_list,{'id':daum_id,'title':daum_name,'year':year,'score':score})
       log_debug('first_url : %s'%first_url)
      if need_another_search and first_url is not I:
       new_ret=MovieSearch.get_movie_info_from_home(first_url)
       MovieSearch.movie_append(movie_list,{'id':new_ret['daum_id'],'title':new_ret['title'],'year':new_ret['year'],'score':100,'country':new_ret['country'],'more':new_ret['more']})
  except G as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc())
  movie_list=H(X(L(movie_list,key=lambda k:k['score'])))
  return movie_list
 @V
 def search_imdb(title,year):
  try:
   year=a(year)
   title=title.replace(' ','_')
   url='https://v2.sg.media-imdb.com/suggestion/%s/%s.json'%(title[0],title)
   tmp=get_json(url)
   if 'd' in tmp:
    for t in tmp['d']:
     title_imdb=t['l'].lower().replace("'",'').replace(':','').replace('&','and').replace('?','')
     if title.lower().replace("'",'').replace('.',' ').replace('_',' ')==title_imdb and 'y' in t and t['y']==year:
      return{'id':t['id'],'title':t['l'],'year':year,'score':100}
  except G as e:
   log_error('Exception:%s',e)
   log_error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
