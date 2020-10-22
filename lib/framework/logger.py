import os
A=int
E=None
R=True
k=os.path
import logging
Op=logging.StreamHandler
Of=logging.Formatter
On=logging.DEBUG
Ox=logging.getLogger
Ot=logging.handlers
import Ot
from datetime import datetime
Ow=datetime.utcnow
from framework import path_data
from pytz import timezone,utc
OD=utc.localize
level_unset_logger_list=[]
logger_list=[]
def get_logger(name):
 logger=Ox(name)
 if not logger.handlers:
  global level_unset_logger_list
  global logger_list
  level=On
  from framework import flag_system_loading 
  try:
   if flag_system_loading:
    try:
     from system.model import ModelSetting as SystemModelSetting
     level=SystemModelSetting.get('log_level')
     level=A(level)
    except:
     level=On
    if level_unset_logger_list is not E:
     for item in level_unset_logger_list:
      item.setLevel(level)
     level_unset_logger_list=E
   else:
    level_unset_logger_list.append(logger)
  except:
   pass
  logger.setLevel(level)
  formatter=Of(u'[%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s] %(message)s')
  def customTime(*args):
   utc_dt=OD(Ow())
   my_tz=timezone("Asia/Seoul")
   converted=utc_dt.astimezone(my_tz)
   return converted.timetuple()
  formatter.converter=customTime
  file_max_bytes=1*1024*1024 
  fileHandler=Ot.RotatingFileHandler(filename=k.join(path_data,'log','%s.log'%name),maxBytes=file_max_bytes,backupCount=5,encoding='utf8',delay=R)
  streamHandler=Op()
  fileHandler.setFormatter(formatter)
  streamHandler.setFormatter(formatter)
  logger.addHandler(fileHandler)
  logger.addHandler(streamHandler)
 return logger
get_logger('apscheduler.scheduler')
get_logger('apscheduler.executors.default')
def set_level(level):
 global logger_list
 try:
  for l in logger_list:
   l.setLevel(level)
 except:
  pass 
# Created by pyminifier (https://github.com/liftoff/pyminifier)
