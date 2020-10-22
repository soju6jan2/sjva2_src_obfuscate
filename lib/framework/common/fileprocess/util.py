import os
Q=None
b=False
v=True
L=UnicodeDecodeError
O=Exception
u=os.remove
k=os.stat
X=os.rmdir
z=os.path
r=os.listdir
import traceback
N=traceback.format_exc
import time
import threading
import shutil
p=shutil.move
from framework.common.fileprocess import logger
W=logger.error
F=logger.info
def remove_small_file_and_move_target(path,size,target=Q,except_ext=Q):
 try:
  if target is Q:
   target=path
  if except_ext is Q:
   except_ext=['.smi','.srt','ass']
  lists=r(path)
  for f in lists:
   try:
    file_path=z.join(path,f)
    except_file=b
    if z.splitext(file_path.lower())[1]in except_ext:
     except_file=v
    if z.isdir(file_path):
     remove_small_file_and_move_target(file_path,size,target=target,except_ext=except_ext)
     if not r(file_path):
      F('REMOVE DIR : %s',file_path)
      X(file_path)
    else:
     if k(file_path).st_size>1024*1024*size or except_file:
      if path==target:
       continue
      try:
       F('MOVE : %s',z.join(target,f))
      except:
       F('MOVE')
      if z.exists(z.join(target,f)):
       F(u'ALREADY in Target : %s',z.join(target,f))
       u(file_path)
      else:
       p(file_path,z.join(target,f))
     else:
      try:
       F(u'FILE REMOVE : %s %s',file_path,k(file_path).st_size)
      except:
       F(u'FILE REMOVE')
      u(file_path)
   except L:
    pass
   except O as e:
    W('Exception:%s',e)
    W(N())
 except O as e:
  W('Exception:%s',e)
  W(N())
def remove_match_ext(path,ext_list):
 try:
  lists=r(path)
  for f in lists:
   try:
    file_path=z.join(path,f)
    if z.isdir(file_path):
     remove_match_ext(file_path,ext_list)
    else:
     if z.splitext(file_path.lower())[1][1:]in ext_list:
      F(u'REMOVE : %s',file_path)
      u(file_path)
   except L:
    pass
   except O as e:
    W('Exception:%s',e)
    W(N())
 except O as e:
  W('Exception:%s',e)
  W(N())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
