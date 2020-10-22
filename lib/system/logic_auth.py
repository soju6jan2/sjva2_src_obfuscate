import os
I=object
h=staticmethod
j=Exception
R=range
i=True
C=False
H=None
g=int
e=str
l=len
import traceback
V=traceback.format_exc
import random
X=random.choice
import json
import string
c=string.digits
B=string.ascii_uppercase
import codecs
r=codecs.encode
import requests
a=requests.post
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,app
A=app.config
from framework.util import Util
from.plugin import package_name,logger
D=logger.error
o=logger.debug
from.model import ModelSetting
z=ModelSetting.set
w=ModelSetting.get
class SystemLogicAuth(I):
 @h
 def process_ajax(sub,req):
  o(sub)
  try:
   if sub=='apikey_generate':
    ret=SystemLogicAuth.apikey_generate()
    return jsonify(ret)
   elif sub=='do_auth':
    ret=SystemLogicAuth.do_auth()
    return jsonify(ret)
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def apikey_generate():
  try:
   value=''.join(X(B+c)for _ in R(10))
   return value
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def get_auth_status(retry=i):
  try:
   value=w('auth_status')
   ret={'ret':C,'desc':'','level':0,'point':0}
   if value=='':
    ret['desc']='미인증'
   elif value=='wrong_id':
    ret['desc']='미인증 - 홈페이지 아이디가 없습니다.'
   elif value=='too_many_sjva':
    ret['desc']='미인증 - 너무 많은 SJVA를 사용중입니다.'
   elif value=='wrong_apikey':
    ret['desc']='미인증 - 홈페이지에 등록된 APIKEY와 다릅니다.'
   else:
    status=SystemLogicAuth.check_auth_status(value)
    if status is not H and status['ret']:
     ret['ret']=status['ret']
     ret['desc']='인증되었습니다. (회원등급:%s, 포인트:%s)'%(status['level'],status['point'])
     ret['level']=status['level']
     ret['point']=status['point']
    else:
     if retry:
      SystemLogicAuth.do_auth()
      return SystemLogicAuth.get_auth_status(retry=C)
     else:
      ret['desc']='잘못된 값입니다. 다시 인증하세요.'
   return ret
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def check_auth_status(value=H):
  try:
   from framework.common.util import AESCipher
   if A['config']['is_py2']:
    tmp=AESCipher.decrypt(value,mykey=(SystemLogicAuth.get_ip().encode('hex')+w('auth_apikey').encode("hex")).zfill(32)[:32]).split('_')
   else:
    mykey=(r(SystemLogicAuth.get_ip().encode(),'hex').decode()+r(w('auth_apikey').encode(),'hex').decode()).zfill(32)[:32].encode()
    o(mykey)
    tmp=AESCipher.decrypt(value,mykey=mykey).decode()
    tmp=tmp.split('_')
   ret={}
   ret['ret']=(w('sjva_id')==tmp[0])
   ret['level']=g(tmp[1])
   ret['point']=g(tmp[2])
   return ret
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def make_auth_status(level,point):
  try:
   from framework.common.util import AESCipher
   if A['config']['is_py2']:
    ret=AESCipher.encrypt(e('%s_%s_%s'%(w('sjva_id'),level,point)),mykey=(r(SystemLogicAuth.get_ip().encode(),'hex')+r(w('auth_apikey').encode(),'hex')).zfill(32)[:32])
   else:
    mykey=(r(SystemLogicAuth.get_ip().encode(),'hex').decode()+r(w('auth_apikey').encode(),'hex').decode()).zfill(32)[:32].encode()
    ret= AESCipher.encrypt(e('%s_%s_%s'%(w('sjva_id'),level,point)),mykey=mykey)
   o(ret)
   return ret
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def get_ip():
  import socket
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  try:
   s.connect(('10.255.255.255',1))
   IP=s.getsockname()[0]
  except j:
   IP='127.0.0.1'
  finally:
   s.close()
  o('IP:%s',IP)
  return IP
 @h
 def do_auth():
  try:
   ret={'ret':C,'msg':'','level':0,'point':0}
   apikey=w('auth_apikey')
   user_id=w('sjva_me_user_id')
   if l(apikey)!=10:
    ret['msg']='APIKEY 문자 길이는 10자리여야합니다.'
    return ret
   if user_id=='':
    ret['msg']='홈페이지 ID가 없습니다.'
    return ret
   data=a('https://sjva.me/sjva/auth.php',data={'apikey':apikey,'user_id':user_id,'sjva_id':w('sjva_id')}).json()
   if data['result']=='success':
    ret['ret']=i
    ret['msg']=u'총 %s개 등록<br>레벨:%s, 포인트:%s'%(data['count'],data['level'],data['point'])
    ret['level']=g(data['level'])
    ret['point']=g(data['point'])
    z('auth_status',SystemLogicAuth.make_auth_status(ret['level'],ret['point']))
   else:
    z('auth_status',data['result'])
    tmp=SystemLogicAuth.get_auth_status(retry=C)
    ret['ret']=tmp['ret']
    ret['msg']=tmp['desc']
   return ret
  except j as e:
   D('Exception:%s',e)
   D(V())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
