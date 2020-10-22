import io
r=Exception
S=open
L=file
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.S(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except r as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def download(url,file_name):
 import requests
 with S(file_name,"wb")as L: 
  response=requests.get(url) 
  L.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.S(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except r as e:
  logger.debug('Exception:%s',e)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
