import os
q=object
F=staticmethod
y=Exception
d=range
Q=True
s=False
u=None
N=int
S=str
J=len
import traceback
import random
import json
import string
import codecs
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,app
from framework.util import Util
from.plugin import package_name,logger
from.model import ModelSetting
class SystemLogicAuth(q):
 @F
 def process_ajax(sub,req):
  logger.debug(sub)
  try:
   if sub=='apikey_generate':
    ret=SystemLogicAuth.apikey_generate()
    return jsonify(ret)
   elif sub=='do_auth':
    ret=SystemLogicAuth.do_auth()
    return jsonify(ret)
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @F
 def apikey_generate():
  try:
   value=''.join(random.choice(string.ascii_uppercase+string.digits)for _ in d(10))
   return value
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @F
 def get_auth_status(retry=Q):
  try:
   value=ModelSetting.get('auth_status')
   ret={'ret':s,'desc':'','level':0,'point':0}
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
    if status is not u and status['ret']:
     ret['ret']=status['ret']
     ret['desc']='인증되었습니다. (회원등급:%s, 포인트:%s)'%(status['level'],status['point'])
     ret['level']=status['level']
     ret['point']=status['point']
    else:
     if retry:
      SystemLogicAuth.do_auth()
      return SystemLogicAuth.get_auth_status(retry=s)
     else:
      ret['desc']='잘못된 값입니다. 다시 인증하세요.'
   return ret
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @F
 def check_auth_status(value=u):
  try:
   from framework.common.util import AESCipher
   if app.config['config']['is_py2']:
    tmp=AESCipher.decrypt(value,mykey=(SystemLogicAuth.get_ip().encode('hex')+ModelSetting.get('auth_apikey').encode("hex")).zfill(32)[:32]).split('_')
   else:
    mykey=(codecs.encode(SystemLogicAuth.get_ip().encode(),'hex').decode()+codecs.encode(ModelSetting.get('auth_apikey').encode(),'hex').decode()).zfill(32)[:32].encode()
    logger.debug(mykey)
    tmp=AESCipher.decrypt(value,mykey=mykey).decode()
    tmp=tmp.split('_')
   ret={}
   ret['ret']=(ModelSetting.get('sjva_id')==tmp[0])
   ret['level']=N(tmp[1])
   ret['point']=N(tmp[2])
   return ret
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @F
 def make_auth_status(level,point):
  try:
   from framework.common.util import AESCipher
   if app.config['config']['is_py2']:
    ret=AESCipher.encrypt(S('%s_%s_%s'%(ModelSetting.get('sjva_id'),level,point)),mykey=(codecs.encode(SystemLogicAuth.get_ip().encode(),'hex')+codecs.encode(ModelSetting.get('auth_apikey').encode(),'hex')).zfill(32)[:32])
   else:
    mykey=(codecs.encode(SystemLogicAuth.get_ip().encode(),'hex').decode()+codecs.encode(ModelSetting.get('auth_apikey').encode(),'hex').decode()).zfill(32)[:32].encode()
    ret= AESCipher.encrypt(S('%s_%s_%s'%(ModelSetting.get('sjva_id'),level,point)),mykey=mykey)
   logger.debug(ret)
   return ret
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @F
 def get_ip():
  import socket
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  try:
   s.connect(('10.255.255.255',1))
   IP=s.getsockname()[0]
  except y:
   IP='127.0.0.1'
  finally:
   s.close()
  logger.debug('IP:%s',IP)
  return IP
 @F
 def do_auth():
  try:
   ret={'ret':s,'msg':'','level':0,'point':0}
   apikey=ModelSetting.get('auth_apikey')
   user_id=ModelSetting.get('sjva_me_user_id')
   if J(apikey)!=10:
    ret['msg']='APIKEY 문자 길이는 10자리여야합니다.'
    return ret
   if user_id=='':
    ret['msg']='홈페이지 ID가 없습니다.'
    return ret
   data=requests.post('https://sjva.me/sjva/auth.php',data={'apikey':apikey,'user_id':user_id,'sjva_id':ModelSetting.get('sjva_id')}).json()
   if data['result']=='success':
    ret['ret']=Q
    ret['msg']=u'총 %s개 등록<br>레벨:%s, 포인트:%s'%(data['count'],data['level'],data['point'])
    ret['level']=N(data['level'])
    ret['point']=N(data['point'])
    ModelSetting.set('auth_status',SystemLogicAuth.make_auth_status(ret['level'],ret['point']))
   else:
    ModelSetting.set('auth_status',data['result'])
    tmp=SystemLogicAuth.get_auth_status(retry=s)
    ret['ret']=tmp['ret']
    ret['msg']=tmp['desc']
   return ret
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
