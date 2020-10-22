import io
Y=Exception
e=open
f=file
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.e(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except Y as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def download(url,file_name):
 import requests
 with e(file_name,"wb")as f: 
  response=requests.get(url) 
  f.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.e(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except Y as e:
  logger.debug('Exception:%s',e)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
