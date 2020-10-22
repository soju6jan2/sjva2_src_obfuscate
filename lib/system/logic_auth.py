import os
L=object
N=staticmethod
e=Exception
p=range
o=True
j=False
Q=None
E=int
F=str
S=len
import traceback
H=traceback.format_exc
import random
W=random.choice
import json
import string
M=string.digits
Y=string.ascii_uppercase
import codecs
z=codecs.encode
import requests
d=requests.post
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,app
X=app.config
from framework.util import Util
from.plugin import package_name,logger
J=logger.error
G=logger.debug
from.model import ModelSetting
h=ModelSetting.set
I=ModelSetting.get
class SystemLogicAuth(L):
 @N
 def process_ajax(sub,req):
  G(sub)
  try:
   if sub=='apikey_generate':
    ret=SystemLogicAuth.apikey_generate()
    return jsonify(ret)
   elif sub=='do_auth':
    ret=SystemLogicAuth.do_auth()
    return jsonify(ret)
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def apikey_generate():
  try:
   value=''.join(W(Y+M)for _ in p(10))
   return value
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def get_auth_status(retry=o):
  try:
   value=I('auth_status')
   ret={'ret':j,'desc':'','level':0,'point':0}
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
    if status is not Q and status['ret']:
     ret['ret']=status['ret']
     ret['desc']='인증되었습니다. (회원등급:%s, 포인트:%s)'%(status['level'],status['point'])
     ret['level']=status['level']
     ret['point']=status['point']
    else:
     if retry:
      SystemLogicAuth.do_auth()
      return SystemLogicAuth.get_auth_status(retry=j)
     else:
      ret['desc']='잘못된 값입니다. 다시 인증하세요.'
   return ret
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def check_auth_status(value=Q):
  try:
   from framework.common.util import AESCipher
   if X['config']['is_py2']:
    tmp=AESCipher.decrypt(value,mykey=(SystemLogicAuth.get_ip().encode('hex')+I('auth_apikey').encode("hex")).zfill(32)[:32]).split('_')
   else:
    mykey=(z(SystemLogicAuth.get_ip().encode(),'hex').decode()+z(I('auth_apikey').encode(),'hex').decode()).zfill(32)[:32].encode()
    G(mykey)
    tmp=AESCipher.decrypt(value,mykey=mykey).decode()
    tmp=tmp.split('_')
   ret={}
   ret['ret']=(I('sjva_id')==tmp[0])
   ret['level']=E(tmp[1])
   ret['point']=E(tmp[2])
   return ret
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def make_auth_status(level,point):
  try:
   from framework.common.util import AESCipher
   if X['config']['is_py2']:
    ret=AESCipher.encrypt(F('%s_%s_%s'%(I('sjva_id'),level,point)),mykey=(z(SystemLogicAuth.get_ip().encode(),'hex')+z(I('auth_apikey').encode(),'hex')).zfill(32)[:32])
   else:
    mykey=(z(SystemLogicAuth.get_ip().encode(),'hex').decode()+z(I('auth_apikey').encode(),'hex').decode()).zfill(32)[:32].encode()
    ret= AESCipher.encrypt(F('%s_%s_%s'%(I('sjva_id'),level,point)),mykey=mykey)
   G(ret)
   return ret
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def get_ip():
  import socket
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  try:
   s.connect(('10.255.255.255',1))
   IP=s.getsockname()[0]
  except e:
   IP='127.0.0.1'
  finally:
   s.close()
  G('IP:%s',IP)
  return IP
 @N
 def do_auth():
  try:
   ret={'ret':j,'msg':'','level':0,'point':0}
   apikey=I('auth_apikey')
   user_id=I('sjva_me_user_id')
   if S(apikey)!=10:
    ret['msg']='APIKEY 문자 길이는 10자리여야합니다.'
    return ret
   if user_id=='':
    ret['msg']='홈페이지 ID가 없습니다.'
    return ret
   data=d('https://sjva.me/sjva/auth.php',data={'apikey':apikey,'user_id':user_id,'sjva_id':I('sjva_id')}).json()
   if data['result']=='success':
    ret['ret']=o
    ret['msg']=u'총 %s개 등록<br>레벨:%s, 포인트:%s'%(data['count'],data['level'],data['point'])
    ret['level']=E(data['level'])
    ret['point']=E(data['point'])
    h('auth_status',SystemLogicAuth.make_auth_status(ret['level'],ret['point']))
   else:
    h('auth_status',data['result'])
    tmp=SystemLogicAuth.get_auth_status(retry=j)
    ret['ret']=tmp['ret']
    ret['msg']=tmp['desc']
   return ret
  except e as e:
   J('Exception:%s',e)
   J(H())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
