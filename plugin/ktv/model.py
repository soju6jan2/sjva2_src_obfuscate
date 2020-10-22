import os
P=True
nY=repr
nN=getattr
V=None
b=staticmethod
f=int
D=Exception
n=os.path
import traceback
y=traceback.format_exc
import datetime
u=datetime.timedelta
g=datetime.now
N=datetime.datetime
from framework.logger import get_logger
from framework import db,app,path_data
p=app.config
C=db.session
nz=db.DateTime
nq=db.String
nK=db.Integer
nB=db.Column
I=db.Model
from sqlalchemy import or_,and_,func,not_
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
p['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(n.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelKtvLibrary(I):
 __tablename__='%s_library'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=nB(nK,primary_key=P)
 library_type=nB(nK)
 library_path=nB(nq)
 rclone_path=nB(nq)
 replace_for_plex_source=nB(nq)
 replace_for_plex_target=nB(nq)
 index=nB(nK)
 def __repr__(self):
  return nY(self.as_dict())
 def as_dict(self):
  return{x.name:nN(self,x.name)for x in self.__table__.columns}
class ModelKtvFile(I):
 __tablename__='%s_file'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=nB(nK,primary_key=P)
 original_filename=nB(nq)
 filename=nB(nq)
 created_time=nB(nz)
 move_type=nB(nK)
 match_folder_name=nB(nq) 
 move_abspath_local=nB(nq) 
 move_abspath_sync=nB(nq) 
 move_abspath_cloud=nB(nq) 
 send_command_time=nB(nz) 
 scan_status=nB(nK) 
 scan_time=nB(nz) 
 scan_abspath=nB(nq) 
 plex_section_id=nB(nK) 
 plex_show_id=nB(nK) 
 plex_daum_id=nB(nK) 
 plex_title=nB(nq) 
 plex_image=nB(nq) 
 plex_abspath=nB(nq)
 plex_part=nB(nq)
 log=nB(nq)
 def __repr__(self):
  return nY(self.as_dict())
 def as_dict(self):
  ret={x.name:nN(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')if self.created_time is not V else ''
  ret['send_command_time']=self.send_command_time.strftime('%m-%d %H:%M:%S')if self.send_command_time is not V else ''
  ret['scan_time']=self.scan_time.strftime('%m-%d %H:%M:%S')if self.scan_time is not V else ''
  return ret
 @b
 def create(entity):
  try:
   f=ModelKtvFile()
   f.original_filename=entity.original_filename
   f.filename=entity.filename
   f.created_time=entity.download_time
   f.move_type=f(entity.move_type)
   f.match_folder_name=entity.match_folder_name
   f.move_abspath_local=entity.move_abspath_local
   f.move_abspath_sync=entity.move_abspath_sync
   f.move_abspath_cloud=entity.move_abspath_cloud
   if entity.send_command_time!='':
    f.send_command_time=entity.send_command_time
   f.scan_status=f(entity.scan_status)
   f.scan_abspath=entity.scan_abspath
   f.plex_section_id=entity.plex_section_id
   f.plex_show_id=entity.plex_show_id
   f.plex_daum_id=entity.plex_daum_id
   f.plex_title=entity.plex_title
   f.plex_image=entity.plex_image
   f.plex_abspath=entity.plex_abspath
   f.log=entity.log
   return f
  except D as e:
   logger.error('Exception:%s',e)
   logger.error(y())
 @b
 def get_library_check_list():
  try:
   query=C.query(ModelKtvFile).filter_by(scan_status=1)
   query=query.filter(or_(ModelKtvFile.send_command_time.is_(V),ModelKtvFile.send_command_time<N.now()+u(hours=-1)))
   query=query.filter(ModelKtvFile.created_time>N.now()+u(hours=-24))
   ret=query.all()
   return ret
  except D as e:
   logger.error('Exception:%s',e)
   logger.error(y())
 @b
 def get_image_empty_list():
  try:
   query=C.query(ModelKtvFile).filter_by(scan_status=3)
   query=query.filter(ModelKtvFile.plex_image.is_(V))
   query=query.filter(ModelKtvFile.plex_show_id!=-1)
   query=query.filter(ModelKtvFile.created_time>N.now()+u(hours=-24))
   ret=query.all()
   return ret
  except D as e:
   logger.error('Exception:%s',e)
   logger.error(y())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
