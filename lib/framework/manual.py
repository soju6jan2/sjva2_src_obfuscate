import os
P=Exception
tM=file
b=os.path
import traceback
t=traceback.format_exc
import requests
tk=requests.get
import json
tX=json.loads
from flask import request,Markup,jsonify
U=request.form
import markdown
to=markdown.markdown
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,path_data
a=app.route
from framework.job import Job
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
@a('/manual/<sub>',methods=['GET','POST'])
def manual(sub):
 logger.debug('MANUAL %s %s',package_name,sub)
 if sub=='menu':
  try:
   url=U['url']
   ret={}
   if url.startswith('http'):
    ret['menu']=tk(url).json()
   else:
    data=fileread(url)
    ret['menu']=tX(data)
   for r in ret['menu']:
    if r['type']=='file':
     r['content']=Markup(to(fileread(r['arg'])))
    elif r['type']=='url':
     if r['url'].startswith('http'):
      res=tk(r['url'])
      r['content']=Markup(to(res.text))
   return jsonify(ret)
  except P as e:
   logger.error('Exception:%s',e)
   logger.error(t())
def fileread(filename):
 try:
  import io
  filename=b.join(path_app_root,'manual',filename)
  tM=io.open(filename,'r',encoding="utf8") 
  text_str=tM.read() 
  tM.close() 
  return text_str
 except P as e:
  logger.error('Exception:%s',e)
  logger.error(t())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
