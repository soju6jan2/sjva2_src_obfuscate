import io
j=False
H=True
x=Exception
import traceback
U=traceback.format_exc
import platform
M=platform.platform
C=platform.system
from framework import app,logger
b=logger.error
y=app.config
def is_arm():
 try:
  ret=j
  import platform
   M=platform.platform
   C=platform.system
  if C()=='Linux':
   if M().find('86')==-1 and M().find('64')==-1:
    ret=H
   if M().find('arch')!=-1:
    ret=H
   if M().find('arm')!=-1:
    ret=H
  return ret
 except x as e:
  b('Exception:%s',e)
  b(U())
def is_native():
 try:
  return(y['config']['running_type']=='native')
 except x as e:
  b('Exception:%s',e)
  b(U())
def is_termux():
 try:
  return(y['config']['running_type']=='termux')
 except x as e:
  b('Exception:%s',e)
  b(U())
def is_windows():
 try:
  return(y['config']['running_type']=='native' and C()=='Windows')
 except x as e:
  b('Exception:%s',e)
  b(U())
def is_mac():
 try:
  return(y['config']['running_type']=='native' and C()=='Darwin')
 except x as e:
  b('Exception:%s',e)
  b(U())
def is_docker():
 try:
  return(y['config']['running_type']=='docker')
 except x as e:
  b('Exception:%s',e)
  b(U())
def is_linux():
 try:
  return(C()=='Linux')
 except x as e:
  b('Exception:%s',e)
  b(U())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
