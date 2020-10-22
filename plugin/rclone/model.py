import os
W=True
J=str
f=getattr
X=None
p=int
R=False
c=os.path
from datetime import datetime
H=datetime.now
from framework import db,app,path_data
P=app.config
o=db.JSON
w=db.Boolean
s=db.DateTime
A=db.String
S=db.Integer
r=db.Column
B=db.Model
from.plugin import logger,package_name
P['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(c.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelRcloneJob(B):
 __tablename__='%s_job'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=r(S,primary_key=W)
 job_type=r(S)
 name=r(A)
 command=r(A)
 remote=r(A)
 remote_path=r(A)
 local_path=r(A)
 option_user=r(A)
 option_static=r(A)
 last_run_time=r(s)
 last_file_count=r(S)
 is_scheduling=r(w)
 def __init__(self):
  self.last_file_count=0
 def __repr__(self):
  return J(self.as_dict())
 def as_dict(self):
  ret={x.name:f(self,x.name)for x in self.__table__.columns}
  ret['last_run_time']=self.last_run_time.strftime('%m-%d %H:%M:%S')if self.last_run_time is not X else ''
  return ret
class ModelRcloneFile(B):
 __tablename__='%s_file'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=r(S,primary_key=W)
 job_id=r(S)
 folder=r(A)
 name=r(A)
 percent=r(S)
 size=r(A)
 speed=r(A)
 rt_hour=r(A)
 rt_min=r(A)
 rt_sec=r(A)
 log=r(A)
 created_time=r(s)
 finish_time=r(s)
 def __init__(self,job_id,folder,name):
  self.job_id=p(job_id)
  self.folder=folder
  self.name=name
  self.log=''
  self.created_time=H()
 def __repr__(self):
  return J(self.as_dict())
 def as_dict(self):
  ret={x.name:f(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  ret['finish_time']=self.finish_time.strftime('%m-%d %H:%M:%S')if self.finish_time is not X else ''
  ret['delta']=''
  try:
   ret['delta']=J(self.finish_time-self.created_time).split('.')[0]
  except:
   pass
  return ret
class ModelRcloneMount(B):
 __tablename__='%s_mount'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=r(S,primary_key=W)
 created_time=r(s)
 json=r(o)
 name=r(A)
 remote=r(A)
 remote_path=r(A)
 local_path=r(A)
 option=r(A)
 auto_start=r(w)
 def __init__(self):
  self.current_status=R
  self.created_time=H()
 def __repr__(self):
  return J(self.as_dict())
 def as_dict(self):
  ret={x.name:f(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  return ret
class ModelRcloneServe(B):
 __tablename__='%s_serve'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=r(S,primary_key=W)
 created_time=r(s)
 json=r(o)
 name=r(A)
 command=r(A)
 remote=r(A)
 remote_path=r(A)
 port=r(S)
 option=r(A)
 auto_start=r(w)
 def __init__(self):
  self.current_status=R
  self.created_time=H()
 def __repr__(self):
  return J(self.as_dict())
 def as_dict(self):
  ret={x.name:f(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  ret['command_ui']=ModelRcloneServe.commands[ret['command']]
  return ret
 commands={'webdav':'WebDav','ftp':'FTP','dlna':'DLNA','sftp':'SFTP','http':'HTTP'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
