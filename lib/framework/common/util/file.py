import io
x=Exception
P=open
k=file
import traceback
U=traceback.format_exc
from framework import logger
Y=logger.debug
b=logger.error
def read_file(filename):
 try:
  import codecs
  ifp=codecs.P(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except x as e:
  b('Exception:%s',e)
  b(U())
def download(url,file_name):
 import requests
 with P(file_name,"wb")as k: 
  response=requests.get(url) 
  k.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.P(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except x as e:
  Y('Exception:%s',e)
  Y(U())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
