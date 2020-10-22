import traceback
W=Exception
a=traceback.format_exc
import json
from framework import py_urllib
f=py_urllib.urlencode
from framework.wavve.api import session,get_baseparameter,config,logger
G=logger.error
j=logger.debug
t=session.get
def movie_contents_movieid(movie_id):
 try:
  param=get_baseparameter()
  url="%s/movie/contents/%s?%s"%(config['base_url'],movie_id,f(param))
  response=t(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    j(data['resultmessage'])
 except W as e:
  G('Exception:%s',e)
  G(a())
def movie_contents(page=0,limit=20,genre='all'):
 try:
  param=get_baseparameter()
  param['targetage']='auto'
  param['genre']=genre
  param['country']='all'
  param['offset']=(page-1)*limit
  param['limit']=limit
  param['orderby']='viewtime'
  url="%s/movie/contents?%s"%(config['base_url'],f(param))
  response=t(url,headers=config['headers'])
  data=response.json()
  if response.status_code==200:
   return data
  else:
   if 'resultcode' in data:
    j(data['resultmessage'])
 except W as e:
  G('Exception:%s',e)
  G(a())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
