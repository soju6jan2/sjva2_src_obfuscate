import os
J=Exception
OG=file
k=os.path
import traceback
O=traceback.format_exc
import requests
Og=requests.get
import json
OL=json.loads
from flask import request,Markup,jsonify
Y=request.form
import markdown
OB=markdown.markdown
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,path_data
h=app.route
from framework.job import Job
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
@h('/manual/<sub>',methods=['GET','POST'])
def manual(sub):
 logger.debug('MANUAL %s %s',package_name,sub)
 if sub=='menu':
  try:
   url=Y['url']
   ret={}
   if url.startswith('http'):
    ret['menu']=Og(url).json()
   else:
    data=fileread(url)
    ret['menu']=OL(data)
   for r in ret['menu']:
    if r['type']=='file':
     r['content']=Markup(OB(fileread(r['arg'])))
    elif r['type']=='url':
     if r['url'].startswith('http'):
      res=Og(r['url'])
      r['content']=Markup(OB(res.text))
   return jsonify(ret)
  except J as e:
   logger.error('Exception:%s',e)
   logger.error(O())
def fileread(filename):
 try:
  import io
  filename=k.join(path_app_root,'manual',filename)
  OG=io.open(filename,'r',encoding="utf8") 
  text_str=OG.read() 
  OG.close() 
  return text_str
 except J as e:
  logger.error('Exception:%s',e)
  logger.error(O())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
