import traceback
Q=Exception
q=traceback.format_exc
import json
from framework import py_urllib
M=py_urllib.urlencode
from framework.wavve.api import session,get_baseparameter,config,logger
w=logger.error
y=logger.debug
F=session.get
def movie_contents_movieid(movie_id):
 try:
  param=get_baseparameter()
  url="%s/movie/contents/%s?%s"%(config['base_url'],movie_id,M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
def movie_contents(page=0,limit=20,genre='all'):
 try:
  param=get_baseparameter()
  param['targetage']='auto'
  param['genre']=genre
  param['country']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']='viewtime'
  url="%s/movie/contents?%s"%(config['base_url'],M(param))
  response=F(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
