import traceback
E=object
n=staticmethod
V=False
A=None
G=True
o=Exception
X=traceback.format_exc
import os
import json
import time
import copy
import re
t=re.sub
m=re.compile
from guessit import guessit
from framework.common.torrent import logger
D=logger.error
C=logger.debug
from framework.common.daum import MovieSearch
c=MovieSearch.search_imdb
f=MovieSearch.search_movie
from system.model import ModelSetting as SystemModelSetting
class ProcessMovie(E):
 @n
 def get_info_from_rss(f):
  try:
   C('INFO: [%s]',f)
   item={}
   item['flag_move']=V
   item['name']=f
   item['guessit']=guessit(f)
   if 'language' in item['guessit']:
    item['guessit']['language']=''
   if 'screen_size' not in item['guessit']:
    item['guessit']['screen_size']='--'
   if 'source' not in item['guessit']:
    item['guessit']['source']='--'
   item['search_name']=A
   item['movie']=A
   match=m(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
   if match:
    item['search_name']=match.group('name').replace('.',' ').strip()
    item['search_name']=t(r'\[(.*?)\]','',item['search_name'])
   else:
    return
   if 'year' in item['guessit']:
    item['is_include_kor'],movie=f(item['search_name'],item['guessit']['year'])
    if movie and movie[0]['score']==100:
     item['movie']=movie[0]
     if item['movie']['country'].startswith(u'한국'):
      if item['is_include_kor']:
       item['target']='kor_vod'
      else:
       item['target']='kor'
     else:
      if item['is_include_kor']:
       item['target']='vod'
      elif item['name'].lower().find('.kor')!=-1:
       item['target']='vod'
      else:
       item['target']='sub_x'
     item['flag_move']=G
    else:
     C('NO META!!!!!!!!!!')
     if item['is_include_kor']==V:
      C('imdb search %s %s ',item['search_name'].lower(),item['guessit']['year'])
      movie=c(item['search_name'].lower(),item['guessit']['year'])
      if movie is not A:
       C('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
       item['movie']=movie
       item['target']='imdb'
       item['flag_move']=G
   item['guessit']=''
   return item
  except o as e:
   D('Exxception:%s',e)
   D(X())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
