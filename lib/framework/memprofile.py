import os
X=True
i=False
z=staticmethod
n=isinstance
C=int
I=long
b=float
q=None
S=str
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
   self.enabled=X
  except:
   self.enabled=i
  if self.enabled:
   self._h=hpy()
  self.hsize=0L
  self.hdiff=0L
 @z
 def getReadableSize(lv):
  if not n(lv,(C,I)):
   return '0'
  if lv>=1024*1024*1024*1024:
   s="%4.2f TB"%(b(lv)/(1024*1024*1024*1024))
  elif lv>=1024*1024*1024:
   s="%4.2f GB"%(b(lv)/(1024*1024*1024))
  elif lv>=1024*1024:
   s="%4.2f MB"%(b(lv)/(1024*1024))
  elif lv>=1024:
   s="%4.2f KB"%(b(lv)/1024)
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
   return q
  return S(self._h.heap())
 def check(self,msg=''):
  if not self.enabled:
   return 'Not enabled. guppy module not found!'
  hdr=self.getHeap().split('\n')[0]
  chsize=I(hdr.split()[-2])
  self.hdiff=chsize-self.hsize
  self.hsize=chsize
  return '%s: %s'%(msg,S(self))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
