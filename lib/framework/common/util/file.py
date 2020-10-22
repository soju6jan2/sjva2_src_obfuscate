import io
A=Exception
W=open
y=file
import traceback
z=traceback.format_exc
from framework import logger
O=logger.debug
N=logger.error
def read_file(filename):
 try:
  import codecs
  ifp=codecs.W(filename,'r',encoding='utf8')
  data=ifp.read()
  ifp.close()
  return data
 except A as e:
  N('Exception:%s',e)
  N(z())
def download(url,file_name):
 import requests
 with W(file_name,"wb")as y: 
  response=requests.get(url) 
  y.write(response.text) 
def write_file(data,filename):
 try:
  import codecs
  ofp=codecs.W(filename,'w',encoding='utf8')
  ofp.write(data)
  ofp.close()
 except A as e:
  O('Exception:%s',e)
  O(z())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
