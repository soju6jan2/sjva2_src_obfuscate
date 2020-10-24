import traceback
N=Exception
import json
from framework import py_urllib
from framework.wavve.api import session,get_baseparameter,config,logger
def movie_contents_movieid(movie_id):
 try:
  param=get_baseparameter()
  url="%s/movie/contents/%s?%s"%(config['base_url'],movie_id,py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except N as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def movie_contents(page=0,limit=20,genre='all'):
 try:
  param=get_baseparameter()
  param['targetage']='auto'
  param['genre']=genre
  param['country']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']='viewtime'
  url="%s/movie/contents?%s"%(config['base_url'],py_urllib.urlencode(param))
  response=session.get(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except N as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
