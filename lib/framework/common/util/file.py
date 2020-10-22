import io
P=Exception
m=open
T=file
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.m(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except P as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def download(url,file_name):
 import requests
 with m(file_name,"wb")as T: 
  response=requests.get(url) 
  T.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.m(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except P as e:
  logger.debug('Exception:%s',e)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
