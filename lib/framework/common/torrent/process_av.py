import traceback
E=object
n=staticmethod
A=None
o=Exception
X=traceback.format_exc
import os
I=os.path
import json
import time
import copy
import re
from guessit import guessit
from framework.common.torrent import logger
D=logger.error
from system.model import ModelSetting as SystemModelSetting
import framework.common.fileprocess as FileProcess
class ProcessAV(E):
 @n
 def process(filename,av_type):
  try:
   if av_type=='censored':
    tmp=FileProcess.change_filename_censored(filename)
    if tmp is not A:
     arg=I.splitext(tmp)[0].split('cd')[0]
     data=FileProcess.test_dmm(arg)
     if data and 'update' in data:
      from framework.common.notify import discord_proxy_image
      poster_ret=discord_proxy_image(data['update']['poster'])
      if poster_ret is not A:
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
    arg=I.splitext(tmp)[0].split('cd')[0]
    data=FileProcess.test_javdb(arg)
    if data and 'update' in data:
     data['update']['poster']=data['update']['poster'].split('url=')[1].split('&apikey')[0]
     ret={'type':'javdb','data':data}
     return ret
  except o as e:
   D('Exxception:%s',e)
   D(X())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
