import io
m=False
J=True
O=Exception
import traceback
import platform
from framework import app,logger
def is_arm():
 try:
  ret=m
  import platform
  if platform.system()=='Linux':
   if platform.platform().find('86')==-1 and platform.platform().find('64')==-1:
    ret=J
   if platform.platform().find('arch')!=-1:
    ret=J
   if platform.platform().find('arm')!=-1:
    ret=J
  return ret
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def is_native():
 try:
  return(app.config['config']['running_type']=='native')
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def is_termux():
 try:
  return(app.config['config']['running_type']=='termux')
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def is_windows():
 try:
  return(app.config['config']['running_type']=='native' and platform.system()=='Windows')
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def is_mac():
 try:
  return(app.config['config']['running_type']=='native' and platform.system()=='Darwin')
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def is_docker():
 try:
  return(app.config['config']['running_type']=='docker')
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def is_linux():
 try:
  return(platform.system()=='Linux')
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
