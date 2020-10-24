import os
D=None
F=print
import sys
from framework import logger,path_app_root
from huey import RedisHuey,SqliteHuey
huey=RedisHuey()
@huey.signal()
def all_signal_handler(signal,task,exc=D):
 F('%s - %s'%(signal,task))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
