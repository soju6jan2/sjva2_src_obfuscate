import os
C=object
D=staticmethod
x=Exception
M=None
v=str
W=False
import traceback
import json
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,py_urllib2
from framework.util import Util
from.plugin import package_name,logger
from.model import ModelSetting
class SystemLogicTrans(C):
 @D
 def process_ajax(sub,req):
  try:
   if sub=='trans_test':
    ret=SystemLogicTrans.trans_test(req)
    return jsonify(ret)
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @D
 def process_api(sub,req):
  ret={}
  try:
   if sub=='do':
    text=req.args.get('text')
    source=req.args.get('source')
    target=req.args.get('target')
    if source is M:
     source='ja'
    if target is M:
     target='ko'
    tmp=SystemLogicTrans.trans(text,source=source,target=target)
    if tmp is not M:
     ret['ret']='success'
     ret['data']=tmp
    else:
     ret['ret']='fail'
     ret['data']=''
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['data']=v(exception)
  return jsonify(ret)
 @D
 def trans_test(req):
  try:
   source=req.form['source']
   trans_type=req.form['trans_type']
   if trans_type=='0':
    return source
   elif trans_type=='1':
    return SystemLogicTrans.trans_google(source)
   elif trans_type=='2':
    return SystemLogicTrans.trans_papago(source)
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return W
 @D
 def trans(text,source='ja',target='ko'):
  try:
   trans_type=ModelSetting.get('trans_type')
   if trans_type=='0':
    return text
   elif trans_type=='1':
    return SystemLogicTrans.trans_google(text,source,target)
   elif trans_type=='2':
    return SystemLogicTrans.trans_papago(text,source,target)
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @D
 def trans_papago(text,source='ja',target='ko'):
  trans_papago_key=ModelSetting.get_list('trans_papago_key')
  for tmp in trans_papago_key:
   client_id,client_secret=tmp.split(',')
   try:
    if client_id=='' or client_id is M or client_secret=='' or client_secret is M:
     return text
    data="source=%s&target=%s&text=%s"%(source,target,text)
    url="https://openapi.naver.com/v1/papago/n2mt"
    requesturl=py_urllib2.Request(url)
    requesturl.add_header("X-Naver-Client-Id",client_id)
    requesturl.add_header("X-Naver-Client-Secret",client_secret)
    response=py_urllib2.urlopen(requesturl,data=data.encode("utf-8"))
    data=json.load(response,encoding="utf-8")
    rescode=response.getcode()
    if rescode==200:
     return data['message']['result']['translatedText']
    else:
     continue
   except x as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
  return text
 @D
 def trans_google(text,source='ja',target='ko'):
  try:
   google_api_key=ModelSetting.get('trans_google_api_key')
   if google_api_key=='' or google_api_key is M:
    return text
   data="key=%s&source=%s&target=%s&q=%s"%(google_api_key,source,target,text)
   url="https://www.googleapis.com/language/translate/v2"
   requesturl=py_urllib2.Request(url)
   requesturl.add_header("X-HTTP-Method-Override","GET")
   response=py_urllib2.urlopen(requesturl,data=data.encode("utf-8"))
   data=json.load(response,encoding="utf-8")
   rescode=response.getcode()
   if rescode==200:
    return data['data']['translations'][0]['translatedText']
   else:
    return text
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return text
# Created by pyminifier (https://github.com/liftoff/pyminifier)
