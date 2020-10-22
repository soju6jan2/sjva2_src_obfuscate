import io
J=Exception
b=open
O=file
import traceback
from framework import logger
def read_file(filename):
 try:
  import codecs
  ifp=codecs.b(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except J as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
def download(url,file_name):
 import requests
 with b(file_name,"wb")as O: 
  response=requests.get(url) 
  O.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.b(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except J as e:
  logger.debug('Exception:%s',e)
  logger.debug(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
