import io
g=Exception
q=open
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.q(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except g as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def download(url,file_name):
 import requests
 with q(file_name,"wb")as file_is: 
  response=requests.get(url) 
  file_is.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.q(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except g as exception:
  logger.debug('Exception:%s',exception)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
