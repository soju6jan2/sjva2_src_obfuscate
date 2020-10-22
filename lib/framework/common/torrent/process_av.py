import traceback
k=object
Y=staticmethod
J=None
E=Exception
import os
import json
import time
import copy
import re
from guessit import guessit
from framework.common.torrent import logger
from system.model import ModelSetting as SystemModelSetting
import framework.common.fileprocess as FileProcess
class ProcessAV(k):
 @Y
 def process(filename,av_type):
  try:
   if av_type=='censored':
    tmp=FileProcess.change_filename_censored(filename)
    if tmp is not J:
     arg=os.path.splitext(tmp)[0].split('cd')[0]
     data=FileProcess.test_dmm(arg)
     if data and 'update' in data:
      from framework.common.notify import discord_proxy_image
      poster_ret=discord_proxy_image(data['update']['poster'])
      if poster_ret is not J:
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
  except E as exception:
   logger.error('Exxception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
