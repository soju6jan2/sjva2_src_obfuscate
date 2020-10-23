import os
L=None
J=False
N=True
W=UnicodeDecodeError
R=Exception
import traceback
import time
import threading
import shutil
from framework.common.fileprocess import logger
def remove_small_file_and_move_target(path,size,target=L,except_ext=L):
 try:
  if target is L:
   target=path
  if except_ext is L:
   except_ext=['.smi','.srt','ass']
  lists=os.listdir(path)
  for f in lists:
   try:
    file_path=os.path.join(path,f)
    except_file=J
    if os.path.splitext(file_path.lower())[1]in except_ext:
     except_file=N
    if os.path.isdir(file_path):
     remove_small_file_and_move_target(file_path,size,target=target,except_ext=except_ext)
     if not os.listdir(file_path):
      logger.info('REMOVE DIR : %s',file_path)
      os.rmdir(file_path)
    else:
     if os.stat(file_path).st_size>1024*1024*size or except_file:
      if path==target:
       continue
      try:
       logger.info('MOVE : %s',os.path.join(target,f))
      except:
       logger.info('MOVE')
      if os.path.exists(os.path.join(target,f)):
       logger.info(u'ALREADY in Target : %s',os.path.join(target,f))
       os.remove(file_path)
      else:
       shutil.move(file_path,os.path.join(target,f))
     else:
      try:
       logger.info(u'FILE REMOVE : %s %s',file_path,os.stat(file_path).st_size)
      except:
       logger.info(u'FILE REMOVE')
      os.remove(file_path)
   except W:
    pass
   except R as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
 except R as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def remove_match_ext(path,ext_list):
 try:
  lists=os.listdir(path)
  for f in lists:
   try:
    file_path=os.path.join(path,f)
    if os.path.isdir(file_path):
     remove_match_ext(file_path,ext_list)
    else:
     if os.path.splitext(file_path.lower())[1][1:]in ext_list:
      logger.info(u'REMOVE : %s',file_path)
      os.remove(file_path)
   except W:
    pass
   except R as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
 except R as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
