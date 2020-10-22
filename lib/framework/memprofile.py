import os
j=True
x=False
w=staticmethod
E=isinstance
q=int
h=long
X=float
n=None
v=str
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
   self.enabled=j
  except:
   self.enabled=x
  if self.enabled:
   self._h=hpy()
  self.hsize=0L
  self.hdiff=0L
 @w
 def getReadableSize(lv):
  if not E(lv,(q,h)):
   return '0'
  if lv>=1024*1024*1024*1024:
   s="%4.2f TB"%(X(lv)/(1024*1024*1024*1024))
  elif lv>=1024*1024*1024:
   s="%4.2f GB"%(X(lv)/(1024*1024*1024))
  elif lv>=1024*1024:
   s="%4.2f MB"%(X(lv)/(1024*1024))
  elif lv>=1024:
   s="%4.2f KB"%(X(lv)/1024)
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
   return n
  return v(self._h.heap())
 def check(self,msg=''):
  if not self.enabled:
   return 'Not enabled. guppy module not found!'
  hdr=self.getHeap().split('\n')[0]
  chsize=h(hdr.split()[-2])
  self.hdiff=chsize-self.hsize
  self.hsize=chsize
  return '%s: %s'%(msg,v(self))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
