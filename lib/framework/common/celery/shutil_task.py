import os
k=False
v=Exception
X=True
import traceback
import shutil
from framework import app,celery,logger
def move(source_path,target_path,run_in_celery=k):
 try:
  if app.config['config']['use_celery']and run_in_celery==k:
   result=_move_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _move_task(source_path,target_path)
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return _move_task(source_path,target_path)
@celery.task
def _move_task(source_path,target_path):
 try:
  logger.debug('_move_task:%s %s',source_path,target_path)
  shutil.move(source_path,target_path)
  logger.debug('_move_task end')
  return X
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return k
def move_exist_remove(source_path,target_path,run_in_celery=k):
 try:
  if app.config['config']['use_celery']and run_in_celery==k:
   result=_move_exist_remove_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _move_exist_remove_task(source_path,target_path)
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return _move_exist_remove_task(source_path,target_path)
@celery.task
def _move_exist_remove_task(source_path,target_path):
 try:
  target_file_path=os.path.join(target_path,os.path.basename(source_path))
  if os.path.exists(target_file_path):
   os.remove(source_path)
   return X
  logger.debug('_move_exist_remove:%s %s',source_path,target_path)
  shutil.move(source_path,target_path)
  logger.debug('_move_exist_remove end')
  return X
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return k
def copytree(source_path,target_path):
 try:
  if app.config['config']['use_celery']:
   result=_copytree_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _copytree_task(source_path,target_path)
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return _copytree_task(source_path,target_path)
@celery.task
def _copytree_task(source_path,target_path):
 try:
  shutil.copytree(source_path,target_path)
  return X
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return k
def copy(source_path,target_path):
 try:
  if app.config['config']['use_celery']:
   result=_copy_task.apply_async((source_path,target_path))
   return result.get()
  else:
   return _copy_task(source_path,target_path)
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return _copy_task(source_path,target_path)
@celery.task
def _copy_task(source_path,target_path):
 try:
  shutil.copy(source_path,target_path)
  return X
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return k
def rmtree(source_path):
 try:
  if app.config['config']['use_celery']:
   result=_rmtree_task.apply_async((source_path,))
   return result.get()
  else:
   return _rmtree_task(source_path)
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return _rmtree_task(source_path)
@celery.task
def _rmtree_task(source_path):
 try:
  shutil.rmtree(source_path)
  return X
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return k 
def remove(remove_path):
 try:
  logger.debug('CELERY os.remove start : %s',remove_path)
  if app.config['config']['use_celery']:
   result=_remove_task.apply_async((remove_path,))
   return result.get()
  else:
   return _remove_task(remove_path)
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return _remove_task(remove_path)
 finally:
  logger.debug('CELERY os.remove end : %s',remove_path)
@celery.task
def _remove_task(remove_path):
 try:
  os.remove(remove_path)
  return X
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  return k 
# Created by pyminifier (https://github.com/liftoff/pyminifier)
