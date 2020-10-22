import os
L=object
N=staticmethod
e=Exception
Q=None
F=str
j=False
import traceback
H=traceback.format_exc
import json
HF=json.load
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,py_urllib2
Hl=py_urllib2.urlopen
HS=py_urllib2.Request
from framework.util import Util
from.plugin import package_name,logger
J=logger.error
from.model import ModelSetting
Ho=ModelSetting.get_list
I=ModelSetting.get
class SystemLogicTrans(L):
 @N
 def process_ajax(sub,req):
  try:
   if sub=='trans_test':
    ret=SystemLogicTrans.trans_test(req)
    return jsonify(ret)
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def process_api(sub,req):
  ret={}
  try:
   if sub=='do':
    text=req.args.get('text')
    source=req.args.get('source')
    target=req.args.get('target')
    if source is Q:
     source='ja'
    if target is Q:
     target='ko'
    tmp=SystemLogicTrans.trans(text,source=source,target=target)
    if tmp is not Q:
     ret['ret']='success'
     ret['data']=tmp
    else:
     ret['ret']='fail'
     ret['data']=''
  except e as e:
   J('Exception:%s',e)
   J(H())
   ret['ret']='exception'
   ret['data']=F(e)
  return jsonify(ret)
 @N
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
  except e as e:
   J('Exception:%s',e)
   J(H())
   return j
 @N
 def trans(text,source='ja',target='ko'):
  try:
   trans_type=I('trans_type')
   if trans_type=='0':
    return text
   elif trans_type=='1':
    return SystemLogicTrans.trans_google(text,source,target)
   elif trans_type=='2':
    return SystemLogicTrans.trans_papago(text,source,target)
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def trans_papago(text,source='ja',target='ko'):
  trans_papago_key=Ho('trans_papago_key')
  for tmp in trans_papago_key:
   client_id,client_secret=tmp.split(',')
   try:
    if client_id=='' or client_id is Q or client_secret=='' or client_secret is Q:
     return text
    data="source=%s&target=%s&text=%s"%(source,target,text)
    url="https://openapi.naver.com/v1/papago/n2mt"
    requesturl=HS(url)
    requesturl.add_header("X-Naver-Client-Id",client_id)
    requesturl.add_header("X-Naver-Client-Secret",client_secret)
    response=Hl(requesturl,data=data.encode("utf-8"))
    data=HF(response,encoding="utf-8")
    rescode=response.getcode()
    if rescode==200:
     return data['message']['result']['translatedText']
    else:
     continue
   except e as e:
    J('Exception:%s',e)
    J(H()) 
  return text
 @N
 def trans_google(text,source='ja',target='ko'):
  try:
   google_api_key=I('trans_google_api_key')
   if google_api_key=='' or google_api_key is Q:
    return text
   data="key=%s&source=%s&target=%s&q=%s"%(google_api_key,source,target,text)
   url="https://www.googleapis.com/language/translate/v2"
   requesturl=HS(url)
   requesturl.add_header("X-HTTP-Method-Override","GET")
   response=Hl(requesturl,data=data.encode("utf-8"))
   data=HF(response,encoding="utf-8")
   rescode=response.getcode()
   if rescode==200:
    return data['data']['translations'][0]['translatedText']
   else:
    return text
  except e as e:
   J('Exception:%s',e)
   J(H())
   return text
# Created by pyminifier (https://github.com/liftoff/pyminifier)
