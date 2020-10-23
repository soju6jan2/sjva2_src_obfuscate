import os
t=None
B=print
import sys
from framework import logger,path_app_root
from huey import RedisHuey,SqliteHuey
huey=RedisHuey()
@huey.signal()
def all_signal_handler(signal,task,exc=t):
 B('%s - %s'%(signal,task))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
