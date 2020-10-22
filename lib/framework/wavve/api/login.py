import traceback
d=id
h=False
W=Exception
a=traceback.format_exc
import json
from framework import py_urllib
f=py_urllib.urlencode
from framework.wavve.api import logger,session,config,logger
l=session.post
G=logger.error
G=logger.error
j=logger.debug
j=logger.debug
def do_login(d,pw,json_return=h):
 try:
  body={"type":"general","id":d,"pushid":"","password":pw,"profile":"0","networktype":"","carrier":"","mcc":"","mnc":"","markettype":"unknown","adid":"","simoperator":"","installerpackagename":""}
  url="%s/login?%s"%(config['base_url'],f(config['base_parameter']))
  response=l(url,json=body,headers=config['headers'])
  data=response.json()
  if 'credential' in data:
   if json_return:
    return data
   else:
    return data['credential']
  else:
   j('login fail!!')
   if 'resultcode' in data:
    j(data['resultmessage'])
 except W as e:
  G('Exception:%s',e)
  G(a())
 return
def get_baseparameter():
 try:
  return config['base_parameter'].copy()
 except W as e:
  G('Exception:%s',e)
  G(a())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
