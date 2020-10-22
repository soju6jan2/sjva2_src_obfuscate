import os
v=True
f=repr
U=getattr
I=None
F=staticmethod
r=os.path
from datetime import datetime
c=datetime.now
from framework import db,app,path_data
Q=app.config
P=db.session
h=db.DateTime
j=db.Boolean
C=db.String
l=db.Integer
y=db.Column
q=db.Model
from.plugin import logger,package_name
Q['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(r.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelGDriveScanJob(q):
 __tablename__='%s_job'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=y(l,primary_key=v)
 name=y(C)
 gdrive_path=y(C)
 plex_path=y(C)
 def __repr__(self):
  return f(self.as_dict())
 def as_dict(self):
  return{x.name:U(self,x.name)for x in self.__table__.columns}
class ModelGDriveScanFile(q):
 __tablename__='%s_file'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=y(l,primary_key=v)
 gdrive_name=y(C)
 name=y(C)
 section_id=y(l)
 is_file=y(j)
 is_add=y(j)
 created_time=y(h)
 scan_time=y(h)
 def __init__(self,gdrive_name,name,section_id,is_file,is_add):
  self.gdrive_name=gdrive_name
  self.name=name
  self.section_id=section_id
  self.is_file=is_file
  self.is_add=is_add
  self.created_time=c()
 def __repr__(self):
  return f(self.as_dict())
 def as_dict(self):
  ret={x.name:U(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')if self.created_time is not I else ''
  ret['scan_time']=self.scan_time.strftime('%m-%d %H:%M:%S')if self.scan_time is not I else ''
  return ret
 @F
 def add(gdrive_name,name,section_id,is_file,is_add):
  item=ModelGDriveScanFile(gdrive_name,name,section_id,is_file,is_add)
  P.add(item)
  P.commit()
  return item.id
# Created by pyminifier (https://github.com/liftoff/pyminifier)
