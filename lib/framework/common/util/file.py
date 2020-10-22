import io
u=Exception
d=open
z=file
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.d(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except u as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def download(url,file_name):
 import requests
 with d(file_name,"wb")as z: 
  response=requests.get(url) 
  z.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.d(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except u as e:
  logger.debug('Exception:%s',e)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
