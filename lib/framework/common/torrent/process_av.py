import traceback
import os
import json
import time
import copy
import re
from framework.common.torrent import logger
from system.model import ModelSetting as SystemModelSetting
import framework.common.fileprocess as FileProcess
class ProcessAV(object):
 @staticmethod
 def process(filename,av_type):
  try:
   import framework.common.fileprocess as FileProcess
   tmp="http://soju6jan.iptime.org:3128"
   FileProcess.Vars.proxies={"http":tmp,"https":tmp,}
   if av_type=='censored':
    tmp=FileProcess.change_filename_censored(filename)
    if tmp is not None:
     arg=os.path.splitext(tmp)[0].split('cd')[0]
     data=FileProcess.test_dmm(arg)
     if data and 'update' in data:
      from framework.common.notify import discord_proxy_image
      poster_ret=discord_proxy_image(data['update']['poster'])
      if poster_ret is not None:
       data['update']['poster']=poster_ret
      ret={'type':'dmm','data':data}
      return ret
     data=FileProcess.test_javdb(arg)
     if data and 'update' in data:
      data['update']['poster']=data['update']['poster'].split('url=')[1].split('&apikey')[0]
      ret={'type':'javdb','data':data}
      return ret
   else:
    tmp=filename
    arg=os.path.splitext(tmp)[0].split('cd')[0]
    data=FileProcess.test_javdb(arg)
    if data and 'update' in data:
     data['update']['poster']=data['update']['poster'].split('url=')[1].split('&apikey')[0]
     ret={'type':'javdb','data':data}
     return ret
  except Exception as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
