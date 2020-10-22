import traceback
p=object
t=staticmethod
J=False
N=None
l=True
w=Exception
j=traceback.format_exc
import os
import json
import time
import copy
import re
y=re.sub
R=re.compile
from guessit import guessit
from framework.common.torrent import logger
L=logger.error
n=logger.debug
from framework.common.daum import MovieSearch
H=MovieSearch.search_imdb
d=MovieSearch.search_movie
from system.model import ModelSetting as SystemModelSetting
class ProcessMovie(p):
 @t
 def get_info_from_rss(f):
  try:
   n('INFO: [%s]',f)
   item={}
   item['flag_move']=J
   item['name']=f
   item['guessit']=guessit(f)
   if 'language' in item['guessit']:
    item['guessit']['language']=''
   if 'screen_size' not in item['guessit']:
    item['guessit']['screen_size']='--'
   if 'source' not in item['guessit']:
    item['guessit']['source']='--'
   item['search_name']=N
   item['movie']=N
   match=R(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
   if match:
    item['search_name']=match.group('name').replace('.',' ').strip()
    item['search_name']=y(r'\[(.*?)\]','',item['search_name'])
   else:
    return
   if 'year' in item['guessit']:
    item['is_include_kor'],movie=d(item['search_name'],item['guessit']['year'])
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
     item['flag_move']=l
    else:
     n('NO META!!!!!!!!!!')
     if item['is_include_kor']==J:
      n('imdb search %s %s ',item['search_name'].lower(),item['guessit']['year'])
      movie=H(item['search_name'].lower(),item['guessit']['year'])
      if movie is not N:
       n('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
       item['movie']=movie
       item['target']='imdb'
       item['flag_move']=l
   item['guessit']=''
   return item
  except w as e:
   L('Exxception:%s',e)
   L(j())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
