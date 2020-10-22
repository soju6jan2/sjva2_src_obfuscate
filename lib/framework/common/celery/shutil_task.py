import os
l=False
j=Exception
G=True
r=os.remove
D=os.path
import traceback
c=traceback.format_exc
import shutil
X=shutil.rmtree
n=shutil.copy
u=shutil.copytree
H=shutil.move
from framework import app,celery,logger
w=logger.debug
x=logger.error
b=celery.task
p=app.config
def move(source_path,target_path,run_in_celery=l):
 try:
  if p['config']['use_celery']and run_in_celery==l:
   result=_move_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _move_task(source_path,target_path)
 except j as e:
  x('Exception:%s',e)
  x(c())
  return _move_task(source_path,target_path)
@b
def _move_task(source_path,target_path):
 try:
  w('_move_task:%s %s',source_path,target_path)
  H(source_path,target_path)
  w('_move_task end')
  return G
 except j as e:
  x('Exception:%s',e)
  x(c())
  return l
def move_exist_remove(source_path,target_path,run_in_celery=l):
 try:
  if p['config']['use_celery']and run_in_celery==l:
   result=_move_exist_remove_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _move_exist_remove_task(source_path,target_path)
 except j as e:
  x('Exception:%s',e)
  x(c())
  return _move_exist_remove_task(source_path,target_path)
@b
def _move_exist_remove_task(source_path,target_path):
 try:
  target_file_path=D.join(target_path,D.basename(source_path))
  if D.exists(target_file_path):
   r(source_path)
   return G
  w('_move_exist_remove:%s %s',source_path,target_path)
  H(source_path,target_path)
  w('_move_exist_remove end')
  return G
 except j as e:
  x('Exception:%s',e)
  x(c())
  return l
def copytree(source_path,target_path):
 try:
  if p['config']['use_celery']:
   result=_copytree_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _copytree_task(source_path,target_path)
 except j as e:
  x('Exception:%s',e)
  x(c())
  return _copytree_task(source_path,target_path)
@b
def _copytree_task(source_path,target_path):
 try:
  u(source_path,target_path)
  return G
 except j as e:
  x('Exception:%s',e)
  x(c())
  return l
def copy(source_path,target_path):
 try:
  if p['config']['use_celery']:
   result=_copy_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _copy_task(source_path,target_path)
 except j as e:
  x('Exception:%s',e)
  x(c())
  return _copy_task(source_path,target_path)
@b
def _copy_task(source_path,target_path):
 try:
  n(source_path,target_path)
  return G
 except j as e:
  x('Exception:%s',e)
  x(c())
  return l
def rmtree(source_path):
 try:
  if p['config']['use_celery']:
   result=_rmtree_task.apply_async((source_path,))
   return result.get()
  else:
   return _rmtree_task(source_path)
 except j as e:
  x('Exception:%s',e)
  x(c())
  return _rmtree_task(source_path)
@b
def _rmtree_task(source_path):
 try:
  X(source_path)
  return G
 except j as e:
  x('Exception:%s',e)
  x(c())
  return l 
def remove(remove_path):
 try:
  w('CELERY os.remove start : %s',remove_path)
  if p['config']['use_celery']:
   result=_remove_task.apply_async((remove_path,))
   return result.get()
  else:
   return _remove_task(remove_path)
 except j as e:
  x('Exception:%s',e)
  x(c())
  return _remove_task(remove_path)
 finally:
  w('CELERY os.remove end : %s',remove_path)
@b
def _remove_task(remove_path):
 try:
  r(remove_path)
  return G
 except j as e:
  x('Exception:%s',e)
  x(c())
  return l 
# Created by pyminifier (https://github.com/liftoff/pyminifier)
