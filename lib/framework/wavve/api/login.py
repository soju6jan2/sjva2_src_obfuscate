import traceback
j=id
U=False
Q=Exception
q=traceback.format_exc
import json
from framework import py_urllib
M=py_urllib.urlencode
from framework.wavve.api import logger,session,config,logger
s=session.post
w=logger.error
w=logger.error
y=logger.debug
y=logger.debug
def do_login(j,pw,json_return=U):
 try:
  body={"type":"general","id":j,"pushid":"","password":pw,"profile":"0","networktype":"","carrier":"","mcc":"","mnc":"","markettype":"unknown","adid":"","simoperator":"","installerpackagename":""}
  url="%s/login?%s"%(config['base_url'],M(config['base_parameter']))
  response=s(url,json=body,headers=config['headers'])
  data=response.json()
  if 'credential' in data:
   if json_return:
    return data
   else:
    return data['credential']
  else:
   y('login fail!!')
   if 'resultcode' in data:
    y(data['resultmessage'])
 except Q as e:
  w('Exception:%s',e)
  w(q())
 return
def get_baseparameter():
 try:
  return config['base_parameter'].copy()
 except Q as e:
  w('Exception:%s',e)
  w(q())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
