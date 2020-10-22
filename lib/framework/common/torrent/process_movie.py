import traceback
D=object
e=staticmethod
K=False
t=None
G=True
h=Exception
import os
import json
import time
import copy
import re
from guessit import guessit
from framework.common.torrent import logger
from framework.common.daum import MovieSearch
from system.model import ModelSetting as SystemModelSetting
class ProcessMovie(D):
 @e
 def get_info_from_rss(f):
  try:
   logger.debug('INFO: [%s]',f)
   item={}
   item['flag_move']=K
   item['name']=f
   item['guessit']=guessit(f)
   if 'language' in item['guessit']:
    item['guessit']['language']=''
   if 'screen_size' not in item['guessit']:
    item['guessit']['screen_size']='--'
   if 'source' not in item['guessit']:
    item['guessit']['source']='--'
   item['search_name']=t
   item['movie']=t
   match=re.compile(r'^(?P<name>.*?)[\s\.\[\_\(]\d{4}').match(item['name'])
   if match:
    item['search_name']=match.group('name').replace('.',' ').strip()
    item['search_name']=re.sub(r'\[(.*?)\]','',item['search_name'])
   else:
    return
   if 'year' in item['guessit']:
    item['is_include_kor'],movie=MovieSearch.search_movie(item['search_name'],item['guessit']['year'])
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
     logger.debug('NO META!!!!!!!!!!')
     if item['is_include_kor']==K:
      logger.debug('imdb search %s %s ',item['search_name'].lower(),item['guessit']['year'])
      movie=MovieSearch.search_imdb(item['search_name'].lower(),item['guessit']['year'])
      if movie is not t:
       logger.debug('IMDB TITLE:[%s][%s]',movie['title'],movie['year'])
       item['movie']=movie
       item['target']='imdb'
       item['flag_move']=G
   item['guessit']=''
   return item
  except h as e:
   logger.error('Exxception:%s',e)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
