import os
q=True
H=repr
a=getattr
g=None
f=staticmethod
W=os.path
from datetime import datetime
v=datetime.now
from framework import db,app,path_data
z=app.config
G=db.session
S=db.DateTime
I=db.Boolean
A=db.String
r=db.Integer
K=db.Column
V=db.Model
from.plugin import logger,package_name
z['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(W.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelGDriveScanJob(V):
 __tablename__='%s_job'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=K(r,primary_key=q)
 name=K(A)
 gdrive_path=K(A)
 plex_path=K(A)
 def __repr__(self):
  return H(self.as_dict())
 def as_dict(self):
  return{x.name:a(self,x.name)for x in self.__table__.columns}
class ModelGDriveScanFile(V):
 __tablename__='%s_file'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=K(r,primary_key=q)
 gdrive_name=K(A)
 name=K(A)
 section_id=K(r)
 is_file=K(I)
 is_add=K(I)
 created_time=K(S)
 scan_time=K(S)
 def __init__(self,gdrive_name,name,section_id,is_file,is_add):
  self.gdrive_name=gdrive_name
  self.name=name
  self.section_id=section_id
  self.is_file=is_file
  self.is_add=is_add
  self.created_time=v()
 def __repr__(self):
  return H(self.as_dict())
 def as_dict(self):
  ret={x.name:a(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')if self.created_time is not g else ''
  ret['scan_time']=self.scan_time.strftime('%m-%d %H:%M:%S')if self.scan_time is not g else ''
  return ret
 @f
 def add(gdrive_name,name,section_id,is_file,is_add):
  item=ModelGDriveScanFile(gdrive_name,name,section_id,is_file,is_add)
  G.add(item)
  G.commit()
  return item.id
# Created by pyminifier (https://github.com/liftoff/pyminifier)
