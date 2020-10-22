import os
import traceback
from datetime import datetime
import json
from sqlalchemy import or_,and_,func,not_
from sqlalchemy.orm import backref
from framework import db,app,path_data
from framework.util import Util
from.plugin import logger,package_name
app.config['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(os.path.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
