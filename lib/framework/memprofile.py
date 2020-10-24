import os
T=True
I=False
n=staticmethod
H=isinstance
S=int
U=long
l=float
D=None
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
   self.enabled=T
  except:
   self.enabled=I
  if self.enabled:
   self._h=hpy()
  self.hsize=0L
  self.hdiff=0L
 @n
 def getReadableSize(lv):
  if not H(lv,(S,U)):
   return '0'
  if lv>=1024*1024*1024*1024:
   s="%4.2f TB"%(l(lv)/(1024*1024*1024*1024))
  elif lv>=1024*1024*1024:
   s="%4.2f GB"%(l(lv)/(1024*1024*1024))
  elif lv>=1024*1024:
   s="%4.2f MB"%(l(lv)/(1024*1024))
  elif lv>=1024:
   s="%4.2f KB"%(l(lv)/1024)
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
   return D
  return v(self._h.heap())
 def check(self,msg=''):
  if not self.enabled:
   return 'Not enabled. guppy module not found!'
  hdr=self.getHeap().split('\n')[0]
  chsize=U(hdr.split()[-2])
  self.hdiff=chsize-self.hsize
  self.hsize=chsize
  return '%s: %s'%(msg,v(self))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
