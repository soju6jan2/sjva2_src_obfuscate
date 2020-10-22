import os
u=object
v=staticmethod
K=False
e=enumerate
S=ord
q=True
Q=None
i=range
b=len
L=Exception
t=list
m=reversed
V=sorted
r=int
import sys
import re
import traceback
import logging
import urllib
import lxml
import requests
from framework import logger,py_urllib,app
class MovieSearch(u):
 @v
 def search_movie(movie_name,movie_year):
  try:
   movie_year='%s'%movie_year
   movie_list=[]
   split_index=-1
   is_include_kor=K
   for index,c in e(movie_name):
    if app.config['config']['is_py2']:
     if S(u'가')<=S(c)<=S(u'힣'):
      is_include_kor=q
      split_index=-1
     elif S('a')<=S(c.lower())<=S('z'):
      is_include_eng=q
      if split_index==-1:
       split_index=index
     elif S('0')<=S(c.lower())<=S('9')or S(' '):
      pass
     else:
      split_index=-1
    else:
     if(u'가')<=(c)<=(u'힣'):
      is_include_kor=q
      split_index=-1
     elif('a')<=(c.lower())<=('z'):
      is_include_eng=q
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
    kor=Q
    eng=Q
   logger.debug('SEARCH_MOVIE : [%s] [%s] [%s] [%s]'%(movie_name,is_include_kor,kor,eng))
   movie_list=MovieSearch.search_movie_web(movie_list,movie_name,movie_year)
   if movie_list and movie_list[0]['score']==100:
    logger.debug('SEARCH_MOVIE STEP 1 : %s'%movie_list)
    return is_include_kor,movie_list
   if kor is not Q:
    movie_list=MovieSearch.search_movie_web(movie_list,kor,movie_year)
    if movie_list and movie_list[0]['score']==100:
     logger.debug('SEARCH_MOVIE STEP 2 : %s'%movie_list)
     return is_include_kor,movie_list
   if eng is not Q:
    movie_list=MovieSearch.search_movie_web(movie_list,eng,movie_year)
    if movie_list and movie_list[0]['score']==100:
     logger.debug('SEARCH_MOVIE STEP 3 : %s'%movie_list)
     return is_include_kor,movie_list
   if kor is not Q:
    tmps=kor.split(' ')
    index=-1
    for i in i(b(tmps)):
     if app.config['config']['is_py2']:
      if S(u'가')<=S(tmps[i][0])<=S(u'힣')or S('0')<=S(tmps[i][0])<=S('9'):
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
      logger.debug('SEARCH_MOVIE STEP 4 : %s'%movie_list)
      return is_include_kor,movie_list
   if q:
    if movie_list and movie_list[0]['score']==95:
     movie_list=MovieSearch.search_movie_web(movie_list,movie_list[0]['title'],movie_year)
     if movie_list and movie_list[0]['score']==100:
      logger.debug('SEARCH_MOVIE STEP 5 : %s'%movie_list)
      return is_include_kor,movie_list
   if is_include_kor==K:
    movie=MovieSearch.search_imdb(movie_name.lower(),movie_year)
    if movie is not Q:
     movie_list=MovieSearch.search_movie_web(movie_list,movie['title'],movie_year)
     if movie_list and movie_list[0]['score']==100:
      logger.debug('SEARCH_MOVIE STEP IMDB : %s'%movie_list)
      return is_include_kor,movie_list
   logger.debug('SEARCH_MOVIE STEP LAST : %s'%movie_list)
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  return is_include_kor,movie_list
 @v
 def movie_append(movie_list,data):
  try:
   exist_data=Q
   for tmp in movie_list:
    if tmp['id']==data['id']:
     exist_data=tmp
     break
   if exist_data is not Q:
    movie_list.remove(exist_data)
   movie_list.append(data)
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @v
 def get_movie_info_from_home(url):
  try:
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   res=session.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies())
   data=res.text
   html=lxml.html.document_fromstring(data)
   movie=Q
   try:
    movie=html.get_element_by_id('movieEColl')
   except L as exception:
    pass
   if movie is Q:
    return Q
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
   if b(tmp)==5:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=tmp[2].replace(u'개봉','').strip()
    more['rate']=tmp[3].strip()
    more['during']=tmp[4].strip()
   elif b(tmp)==4:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=''
    more['rate']=tmp[2].strip()
    more['during']=tmp[3].strip()
   elif b(tmp)==3:
    more['country']=tmp[0].replace(u'외','').strip()
    more['genre']=tmp[1].replace(u'외','').strip()
    more['date']=''
    more['rate']=''
    more['during']=tmp[2].strip()
   daum_id=href.split('=')[1]
   return{'movie':movie,'title':title,'daum_id':daum_id,'year':tmp_year,'country':country,'more':more}
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @v
 def search_movie_web(movie_list,movie_name,movie_year):
  try:
   url='https://suggest-bar.daum.net/suggest?id=movie&cate=movie&multiple=1&mod=json&code=utf_in_out&q=%s'%(py_urllib.quote(movie_name.encode('utf8')))
   from framework.common.daum import headers,session
   from system.logic_site import SystemLogicSite
   res=session.get(url,headers=headers,cookies=SystemLogicSite.get_daum_cookies())
   data=res.json()
   for index,item in e(data['items']['movie']):
    tmps=item.split('|')
    score=85-(index*5)
    if tmps[0].find(movie_name)!=-1 and tmps[3]==movie_year:
     score=95
    elif tmps[3]==movie_year:
     score=score+5
    if score<10:
     score=10
    MovieSearch.movie_append(movie_list,{'id':tmps[1],'title':tmps[0],'year':tmps[3],'score':score})
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  try:
   url='https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=%s%s'%('%EC%98%81%ED%99%94+',py_urllib.quote(movie_name.encode('utf8')))
   ret=MovieSearch.get_movie_info_from_home(url)
   if ret is not Q:
    if ret['year']==movie_year:
     score=100
     need_another_search=K
    else:
     score=90
     need_another_search=q
    MovieSearch.movie_append(movie_list,{'id':ret['daum_id'],'title':ret['title'],'year':ret['year'],'score':score,'country':ret['country'],'more':ret['more']})
    logger.debug('need_another_search : %s'%need_another_search)
    movie=ret['movie']
    if need_another_search:
     tmp=movie.find('div[@class="coll_etc"]')
     if tmp is not Q:
      tag_list=tmp.findall('.//a')
      first_url=Q
      for tag in tag_list:
       match=re.compile(r'(.*?)\((.*?)\)').search(tag.text_content())
       if match:
        daum_id=tag.attrib['href'].split('||')[1]
        score=80
        if match.group(1)==movie_name and match.group(2)==movie_year:
         first_url='https://search.daum.net/search?%s'%tag.attrib['href']
        elif match.group(2)==movie_year and first_url is not Q:
         first_url='https://search.daum.net/search?%s'%tag.attrib['href']
        MovieSearch.movie_append(movie_list,{'id':daum_id,'title':match.group(1),'year':match.group(2),'score':score})
      logger.debug('first_url : %s'%first_url)
      if need_another_search and first_url is not Q:
       new_ret=MovieSearch.get_movie_info_from_home(first_url)
       MovieSearch.movie_append(movie_list,{'id':new_ret['daum_id'],'title':new_ret['title'],'year':new_ret['year'],'score':100,'country':new_ret['country'],'more':new_ret['more']})
     tmp=movie.find('.//ul[@class="list_thumb list_few"]')
     logger.debug('SERIES:%s'%tmp)
     if tmp is not Q:
      tag_list=tmp.findall('.//div[@class="wrap_cont"]')
      first_url=Q
      score=80
      for tag in tag_list:
       a_tag=tag.find('a')
       daum_id=a_tag.attrib['href'].split('||')[1]
       daum_name=a_tag.text_content()
       span_tag=tag.find('span')
       year=span_tag.text_content()
       logger.debug('daum_id:%s %s %s'%(daum_id,year,daum_name))
       if daum_name==movie_name and year==movie_year:
        first_url='https://search.daum.net/search?%s'%a_tag.attrib['href']
       elif year==movie_year and first_url is not Q:
        first_url='https://search.daum.net/search?%s'%tag.attrib['href']
       MovieSearch.movie_append(movie_list,{'id':daum_id,'title':daum_name,'year':year,'score':score})
       logger.debug('first_url : %s'%first_url)
      if need_another_search and first_url is not Q:
       new_ret=MovieSearch.get_movie_info_from_home(first_url)
       MovieSearch.movie_append(movie_list,{'id':new_ret['daum_id'],'title':new_ret['title'],'year':new_ret['year'],'score':100,'country':new_ret['country'],'more':new_ret['more']})
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  movie_list=t(m(V(movie_list,key=lambda k:k['score'])))
  return movie_list
 @v
 def search_imdb(title,year):
  try:
   year=r(year)
   title=title.replace(' ','_')
   url='https://v2.sg.media-imdb.com/suggestion/%s/%s.json'%(title[0],title)
   tmp=requests.get(url).json()
   if 'd' in tmp:
    for t in tmp['d']:
     title_imdb=t['l'].lower().replace("'",'').replace(':','').replace('&','and').replace('?','')
     if title.lower().replace("'",'').replace('.',' ').replace('_',' ')==title_imdb and 'y' in t and t['y']==year:
      return{'id':t['id'],'title':t['l'],'year':year,'score':100}
  except L as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
