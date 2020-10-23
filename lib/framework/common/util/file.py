import io
C=Exception
n=open
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.n(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except C as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def download(url,file_name):
 try:
  import requests
  with n(file_name,"wb")as file_is: 
   response=requests.get(url) 
   file_is.write(response.content) 
 except C as exception:
  logger.debug('Exception:%s',exception)
  logger.debug(traceback.format_exc()) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.n(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except C as exception:
  logger.debug('Exception:%s',exception)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
