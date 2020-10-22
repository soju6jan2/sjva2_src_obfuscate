import traceback
k=id
A=False
h=Exception
import json
from framework import py_urllib
from framework.wavve.api import logger,session,config,logger
def do_login(k,pw,json_return=A):
 try:
  body={"type":"general","id":k,"pushid":"","password":pw,"profile":"0","networktype":"","carrier":"","mcc":"","mnc":"","markettype":"unknown","adid":"","simoperator":"","installerpackagename":""}
  url="%s/login?%s"%(config['base_url'],py_urllib.urlencode(config['base_parameter']))
  response=session.post(url,json=body,headers=config['headers'])
  data=response.json()
  if 'credential' in data:
   if json_return:
    return data
   else:
    return data['credential']
  else:
   logger.debug('login fail!!')
   if 'resultcode' in data:
    logger.debug(data['resultmessage'])
 except h as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
 return
def get_baseparameter():
 try:
  return config['base_parameter'].copy()
 except h as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
