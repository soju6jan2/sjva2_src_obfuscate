import io
i=False
J=True
A=Exception
import traceback
z=traceback.format_exc
import platform
w=platform.platform
b=platform.system
from framework import app,logger
N=logger.error
o=app.config
def is_arm():
 try:
  ret=i
  import platform
   w=platform.platform
   b=platform.system
  if b()=='Linux':
   if w().find('86')==-1 and w().find('64')==-1:
    ret=J
   if w().find('arch')!=-1:
    ret=J
   if w().find('arm')!=-1:
    ret=J
  return ret
 except A as e:
  N('Exception:%s',e)
  N(z())
def is_native():
 try:
  return(o['config']['running_type']=='native')
 except A as e:
  N('Exception:%s',e)
  N(z())
def is_termux():
 try:
  return(o['config']['running_type']=='termux')
 except A as e:
  N('Exception:%s',e)
  N(z())
def is_windows():
 try:
  return(o['config']['running_type']=='native' and b()=='Windows')
 except A as e:
  N('Exception:%s',e)
  N(z())
def is_mac():
 try:
  return(o['config']['running_type']=='native' and b()=='Darwin')
 except A as e:
  N('Exception:%s',e)
  N(z())
def is_docker():
 try:
  return(o['config']['running_type']=='docker')
 except A as e:
  N('Exception:%s',e)
  N(z())
def is_linux():
 try:
  return(b()=='Linux')
 except A as e:
  N('Exception:%s',e)
  N(z())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
