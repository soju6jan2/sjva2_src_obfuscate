import os
v=set
U=ValueError
i=len
class MyEvent:
 def __init__(self):
  self.handlers=v()
 def handle(self,handler):
  self.handlers.add(handler)
  return self
 def unhandle(self,handler):
  try:
   self.handlers.remove(handler)
  except:
   raise U("Handler is not handling this event, so cannot unhandle it.")
  return self
 def fire(self,*args,**kargs):
  for handler in self.handlers:
   handler(*args,**kargs)
 def getHandlerCount(self):
  return i(self.handlers)
 __iadd__=handle
 __isub__=unhandle
 __call__=fire
 __len__ =getHandlerCount
# Created by pyminifier (https://github.com/liftoff/pyminifier)
