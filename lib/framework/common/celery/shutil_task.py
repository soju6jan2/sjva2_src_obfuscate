import os
D=False
v=Exception
B=True
j=os.remove
u=os.path
import traceback
r=traceback.format_exc
import shutil
W=shutil.rmtree
L=shutil.copy
y=shutil.copytree
a=shutil.move
from framework import app,celery,logger
g=logger.debug
V=logger.error
S=celery.task
k=app.config
def move(source_path,target_path,run_in_celery=D):
 try:
  if k['config']['use_celery']and run_in_celery==D:
   result=_move_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _move_task(source_path,target_path)
 except v as e:
  V('Exception:%s',e)
  V(r())
  return _move_task(source_path,target_path)
@S
def _move_task(source_path,target_path):
 try:
  g('_move_task:%s %s',source_path,target_path)
  a(source_path,target_path)
  g('_move_task end')
  return B
 except v as e:
  V('Exception:%s',e)
  V(r())
  return D
def move_exist_remove(source_path,target_path,run_in_celery=D):
 try:
  if k['config']['use_celery']and run_in_celery==D:
   result=_move_exist_remove_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _move_exist_remove_task(source_path,target_path)
 except v as e:
  V('Exception:%s',e)
  V(r())
  return _move_exist_remove_task(source_path,target_path)
@S
def _move_exist_remove_task(source_path,target_path):
 try:
  target_file_path=u.join(target_path,u.basename(source_path))
  if u.exists(target_file_path):
   j(source_path)
   return B
  g('_move_exist_remove:%s %s',source_path,target_path)
  a(source_path,target_path)
  g('_move_exist_remove end')
  return B
 except v as e:
  V('Exception:%s',e)
  V(r())
  return D
def copytree(source_path,target_path):
 try:
  if k['config']['use_celery']:
   result=_copytree_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _copytree_task(source_path,target_path)
 except v as e:
  V('Exception:%s',e)
  V(r())
  return _copytree_task(source_path,target_path)
@S
def _copytree_task(source_path,target_path):
 try:
  y(source_path,target_path)
  return B
 except v as e:
  V('Exception:%s',e)
  V(r())
  return D
def copy(source_path,target_path):
 try:
  if k['config']['use_celery']:
   result=_copy_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _copy_task(source_path,target_path)
 except v as e:
  V('Exception:%s',e)
  V(r())
  return _copy_task(source_path,target_path)
@S
def _copy_task(source_path,target_path):
 try:
  L(source_path,target_path)
  return B
 except v as e:
  V('Exception:%s',e)
  V(r())
  return D
def rmtree(source_path):
 try:
  if k['config']['use_celery']:
   result=_rmtree_task.apply_async((source_path,))
   return result.get()
  else:
   return _rmtree_task(source_path)
 except v as e:
  V('Exception:%s',e)
  V(r())
  return _rmtree_task(source_path)
@S
def _rmtree_task(source_path):
 try:
  W(source_path)
  return B
 except v as e:
  V('Exception:%s',e)
  V(r())
  return D 
def remove(remove_path):
 try:
  g('CELERY os.remove start : %s',remove_path)
  if k['config']['use_celery']:
   result=_remove_task.apply_async((remove_path,))
   return result.get()
  else:
   return _remove_task(remove_path)
 except v as e:
  V('Exception:%s',e)
  V(r())
  return _remove_task(remove_path)
 finally:
  g('CELERY os.remove end : %s',remove_path)
@S
def _remove_task(remove_path):
 try:
  j(remove_path)
  return B
 except v as e:
  V('Exception:%s',e)
  V(r())
  return D 
# Created by pyminifier (https://github.com/liftoff/pyminifier)
