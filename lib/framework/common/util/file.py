import io
K=Exception
a=open
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.a(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except K as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def download(url,file_name):
 try:
  import requests
  with a(file_name,"wb")as file_is: 
   response=requests.get(url) 
   file_is.write(response.content) 
 except K as exception:
  logger.debug('Exception:%s',exception)
  logger.debug(traceback.format_exc()) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.a(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except K as exception:
  logger.debug('Exception:%s',exception)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
