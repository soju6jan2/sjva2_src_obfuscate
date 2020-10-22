import os
R=int
E=None
f=True
b=os.path
import logging
tN=logging.StreamHandler
te=logging.Formatter
tu=logging.DEBUG
ti=logging.getLogger
tL=logging.handlers
import tL
from datetime import datetime
tz=datetime.utcnow
from framework import path_data
from pytz import timezone,utc
tB=utc.localize
level_unset_logger_list=[]
logger_list=[]
def get_logger(name):
 logger=ti(name)
 if not logger.handlers:
  global level_unset_logger_list
  global logger_list
  level=tu
  from framework import flag_system_loading 
  try:
   if flag_system_loading:
    try:
     from system.model import ModelSetting as SystemModelSetting
     level=SystemModelSetting.get('log_level')
     level=R(level)
    except:
     level=tu
    if level_unset_logger_list is not E:
     for item in level_unset_logger_list:
      item.setLevel(level)
     level_unset_logger_list=E
   else:
    level_unset_logger_list.append(logger)
  except:
   pass
  logger.setLevel(level)
  formatter=te(u'[%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s] %(message)s')
  def customTime(*args):
   utc_dt=tB(tz())
   my_tz=timezone("Asia/Seoul")
   converted=utc_dt.astimezone(my_tz)
   return converted.timetuple()
  formatter.converter=customTime
  file_max_bytes=1*1024*1024 
  fileHandler=tL.RotatingFileHandler(filename=b.join(path_data,'log','%s.log'%name),maxBytes=file_max_bytes,backupCount=5,encoding='utf8',delay=f)
  streamHandler=tN()
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
