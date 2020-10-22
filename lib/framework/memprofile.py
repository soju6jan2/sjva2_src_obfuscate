import os
n=True
b=False
u=staticmethod
S=isinstance
T=int
g=long
K=float
A=None
x=str
import traceback
import logging
import xml.etree.ElementTree as ET
from framework.logger import get_logger
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class HeapMon:
 def __init__(self):
  try:
   from guppy import hpy
   self.enabled=n
  except:
   self.enabled=b
  if self.enabled:
   self._h=hpy()
  self.hsize=0L
  self.hdiff=0L
 @u
 def getReadableSize(lv):
  if not S(lv,(T,g)):
   return '0'
  if lv>=1024*1024*1024*1024:
   s="%4.2f TB"%(K(lv)/(1024*1024*1024*1024))
  elif lv>=1024*1024*1024:
   s="%4.2f GB"%(K(lv)/(1024*1024*1024))
  elif lv>=1024*1024:
   s="%4.2f MB"%(K(lv)/(1024*1024))
  elif lv>=1024:
   s="%4.2f KB"%(K(lv)/1024)
  else:
   s="%d B"%lv
  return s
 def __repr__(self):
  if not self.enabled:
   return 'Not enabled. guppy module not found!'
  if self.hdiff>0:
   s='Total %s, %s incresed'% (self.getReadableSize(self.hsize),self.getReadableSize(self.hdiff))
  elif self.hdiff<0:
   s='Total %s, %s decresed'% (self.getReadableSize(self.hsize),self.getReadableSize(-self.hdiff))
  else:
   s='Total %s, not changed'%self.getReadableSize(self.hsize)
  return s
 def getHeap(self):
  if not self.enabled:
   return A
  return x(self._h.heap())
 def check(self,msg=''):
  if not self.enabled:
   return 'Not enabled. guppy module not found!'
  hdr=self.getHeap().split('\n')[0]
  chsize=g(hdr.split()[-2])
  self.hdiff=chsize-self.hsize
  self.hsize=chsize
  return '%s: %s'%(msg,x(self))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
