import os
I=object
h=staticmethod
j=Exception
H=None
e=str
C=False
import traceback
V=traceback.format_exc
import json
Ve=json.load
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,py_urllib2
VJ=py_urllib2.urlopen
Vl=py_urllib2.Request
from framework.util import Util
from.plugin import package_name,logger
D=logger.error
from.model import ModelSetting
Vi=ModelSetting.get_list
w=ModelSetting.get
class SystemLogicTrans(I):
 @h
 def process_ajax(sub,req):
  try:
   if sub=='trans_test':
    ret=SystemLogicTrans.trans_test(req)
    return jsonify(ret)
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def process_api(sub,req):
  ret={}
  try:
   if sub=='do':
    text=req.args.get('text')
    source=req.args.get('source')
    target=req.args.get('target')
    if source is H:
     source='ja'
    if target is H:
     target='ko'
    tmp=SystemLogicTrans.trans(text,source=source,target=target)
    if tmp is not H:
     ret['ret']='success'
     ret['data']=tmp
    else:
     ret['ret']='fail'
     ret['data']=''
  except j as e:
   D('Exception:%s',e)
   D(V())
   ret['ret']='exception'
   ret['data']=e(e)
  return jsonify(ret)
 @h
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
  except j as e:
   D('Exception:%s',e)
   D(V())
   return C
 @h
 def trans(text,source='ja',target='ko'):
  try:
   trans_type=w('trans_type')
   if trans_type=='0':
    return text
   elif trans_type=='1':
    return SystemLogicTrans.trans_google(text,source,target)
   elif trans_type=='2':
    return SystemLogicTrans.trans_papago(text,source,target)
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def trans_papago(text,source='ja',target='ko'):
  trans_papago_key=Vi('trans_papago_key')
  for tmp in trans_papago_key:
   client_id,client_secret=tmp.split(',')
   try:
    if client_id=='' or client_id is H or client_secret=='' or client_secret is H:
     return text
    data="source=%s&target=%s&text=%s"%(source,target,text)
    url="https://openapi.naver.com/v1/papago/n2mt"
    requesturl=Vl(url)
    requesturl.add_header("X-Naver-Client-Id",client_id)
    requesturl.add_header("X-Naver-Client-Secret",client_secret)
    response=VJ(requesturl,data=data.encode("utf-8"))
    data=Ve(response,encoding="utf-8")
    rescode=response.getcode()
    if rescode==200:
     return data['message']['result']['translatedText']
    else:
     continue
   except j as e:
    D('Exception:%s',e)
    D(V()) 
  return text
 @h
 def trans_google(text,source='ja',target='ko'):
  try:
   google_api_key=w('trans_google_api_key')
   if google_api_key=='' or google_api_key is H:
    return text
   data="key=%s&source=%s&target=%s&q=%s"%(google_api_key,source,target,text)
   url="https://www.googleapis.com/language/translate/v2"
   requesturl=Vl(url)
   requesturl.add_header("X-HTTP-Method-Override","GET")
   response=VJ(requesturl,data=data.encode("utf-8"))
   data=Ve(response,encoding="utf-8")
   rescode=response.getcode()
   if rescode==200:
    return data['data']['translations'][0]['translatedText']
   else:
    return text
  except j as e:
   D('Exception:%s',e)
   D(V())
   return text
# Created by pyminifier (https://github.com/liftoff/pyminifier)
