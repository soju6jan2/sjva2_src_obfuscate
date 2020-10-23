import os
N=Exception
import traceback
import requests
import json
from flask import request,Markup,jsonify
import markdown
from framework.logger import get_logger
from framework import app,db,scheduler,path_app_root,path_data
from framework.job import Job
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
@app.route('/manual/<sub>',methods=['GET','POST'])
def manual(sub):
 logger.debug('MANUAL %s %s',package_name,sub)
 if sub=='menu':
  try:
   url=request.form['url']
   ret={}
   if url.startswith('http'):
    ret['menu']=requests.get(url).json()
   else:
    data=fileread(url)
    ret['menu']=json.loads(data)
   for r in ret['menu']:
    if r['type']=='file':
     r['content']=Markup(markdown.markdown(fileread(r['arg'])))
    elif r['type']=='url':
     if r['url'].startswith('http'):
      res=requests.get(r['url'])
      r['content']=Markup(markdown.markdown(res.text))
   return jsonify(ret)
  except N as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
def fileread(filename):
 try:
  import io
  filename=os.path.join(path_app_root,'manual',filename)
  file_is=io.open(filename,'r',encoding="utf8") 
  text_str=file_is.read() 
  file_is.close() 
  return text_str
 except N as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
