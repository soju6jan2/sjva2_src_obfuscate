import io
F=Exception
X=open
a=file
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.X(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except F as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def download(url,file_name):
 import requests
 with X(file_name,"wb")as a: 
  response=requests.get(url) 
  a.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.X(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except F as e:
  logger.debug('Exception:%s',e)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
