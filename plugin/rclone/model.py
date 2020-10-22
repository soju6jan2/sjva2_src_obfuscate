import os
W=True
X=str
N=getattr
v=None
l=int
H=False
D=os.path
from datetime import datetime
C=datetime.now
from framework import db,app,path_data
K=app.config
I=db.JSON
q=db.Boolean
T=db.DateTime
o=db.String
j=db.Integer
f=db.Column
m=db.Model
from.plugin import logger,package_name
K['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(D.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelRcloneJob(m):
 __tablename__='%s_job'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=f(j,primary_key=W)
 job_type=f(j)
 name=f(o)
 command=f(o)
 remote=f(o)
 remote_path=f(o)
 local_path=f(o)
 option_user=f(o)
 option_static=f(o)
 last_run_time=f(T)
 last_file_count=f(j)
 is_scheduling=f(q)
 def __init__(self):
  self.last_file_count=0
 def __repr__(self):
  return X(self.as_dict())
 def as_dict(self):
  ret={x.name:N(self,x.name)for x in self.__table__.columns}
  ret['last_run_time']=self.last_run_time.strftime('%m-%d %H:%M:%S')if self.last_run_time is not v else ''
  return ret
class ModelRcloneFile(m):
 __tablename__='%s_file'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=f(j,primary_key=W)
 job_id=f(j)
 folder=f(o)
 name=f(o)
 percent=f(j)
 size=f(o)
 speed=f(o)
 rt_hour=f(o)
 rt_min=f(o)
 rt_sec=f(o)
 log=f(o)
 created_time=f(T)
 finish_time=f(T)
 def __init__(self,job_id,folder,name):
  self.job_id=l(job_id)
  self.folder=folder
  self.name=name
  self.log=''
  self.created_time=C()
 def __repr__(self):
  return X(self.as_dict())
 def as_dict(self):
  ret={x.name:N(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  ret['finish_time']=self.finish_time.strftime('%m-%d %H:%M:%S')if self.finish_time is not v else ''
  ret['delta']=''
  try:
   ret['delta']=X(self.finish_time-self.created_time).split('.')[0]
  except:
   pass
  return ret
class ModelRcloneMount(m):
 __tablename__='%s_mount'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=f(j,primary_key=W)
 created_time=f(T)
 json=f(I)
 name=f(o)
 remote=f(o)
 remote_path=f(o)
 local_path=f(o)
 option=f(o)
 auto_start=f(q)
 def __init__(self):
  self.current_status=H
  self.created_time=C()
 def __repr__(self):
  return X(self.as_dict())
 def as_dict(self):
  ret={x.name:N(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  return ret
class ModelRcloneServe(m):
 __tablename__='%s_serve'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=f(j,primary_key=W)
 created_time=f(T)
 json=f(I)
 name=f(o)
 command=f(o)
 remote=f(o)
 remote_path=f(o)
 port=f(j)
 option=f(o)
 auto_start=f(q)
 def __init__(self):
  self.current_status=H
  self.created_time=C()
 def __repr__(self):
  return X(self.as_dict())
 def as_dict(self):
  ret={x.name:N(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  ret['command_ui']=ModelRcloneServe.commands[ret['command']]
  return ret
 commands={'webdav':'WebDav','ftp':'FTP','dlna':'DLNA','sftp':'SFTP','http':'HTTP'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
