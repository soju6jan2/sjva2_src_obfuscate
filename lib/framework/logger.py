import os
j=int
b=None
x=True
import logging
import logging.handlers
from datetime import datetime
from framework import path_data
from pytz import timezone,utc
level_unset_logger_list=[]
logger_list=[]
def get_logger(name):
 logger=logging.getLogger(name)
 if not logger.handlers:
  global level_unset_logger_list
  global logger_list
  level=logging.DEBUG
  from framework import flag_system_loading 
  try:
   if flag_system_loading:
    try:
     from system.model import ModelSetting as SystemModelSetting
     level=SystemModelSetting.get('log_level')
     level=j(level)
    except:
     level=logging.DEBUG
    if level_unset_logger_list is not b:
     for item in level_unset_logger_list:
      item.setLevel(level)
     level_unset_logger_list=b
   else:
    level_unset_logger_list.append(logger)
  except:
   pass
  logger.setLevel(level)
  formatter=logging.Formatter(u'[%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s] %(message)s')
  def customTime(*args):
   utc_dt=utc.localize(datetime.utcnow())
   my_tz=timezone("Asia/Seoul")
   converted=utc_dt.astimezone(my_tz)
   return converted.timetuple()
  formatter.converter=customTime
  file_max_bytes=1*1024*1024 
  fileHandler=logging.handlers.RotatingFileHandler(filename=os.path.join(path_data,'log','%s.log'%name),maxBytes=file_max_bytes,backupCount=5,encoding='utf8',delay=x)
  streamHandler=logging.StreamHandler()
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
