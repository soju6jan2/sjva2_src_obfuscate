import os
F=True
AW=repr
Au=getattr
d=None
g=staticmethod
E=int
i=Exception
A=os.path
import traceback
P=traceback.format_exc
import datetime
o=datetime.timedelta
w=datetime.now
u=datetime.datetime
from framework.logger import get_logger
from framework import db,app,path_data
S=app.config
f=db.session
AJ=db.DateTime
Aj=db.String
AG=db.Integer
Ap=db.Column
V=db.Model
from sqlalchemy import or_,and_,func,not_
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
S['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(A.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelKtvLibrary(V):
 __tablename__='%s_library'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=Ap(AG,primary_key=F)
 library_type=Ap(AG)
 library_path=Ap(Aj)
 rclone_path=Ap(Aj)
 replace_for_plex_source=Ap(Aj)
 replace_for_plex_target=Ap(Aj)
 index=Ap(AG)
 def __repr__(self):
  return AW(self.as_dict())
 def as_dict(self):
  return{x.name:Au(self,x.name)for x in self.__table__.columns}
class ModelKtvFile(V):
 __tablename__='%s_file'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=Ap(AG,primary_key=F)
 original_filename=Ap(Aj)
 filename=Ap(Aj)
 created_time=Ap(AJ)
 move_type=Ap(AG)
 match_folder_name=Ap(Aj) 
 move_abspath_local=Ap(Aj) 
 move_abspath_sync=Ap(Aj) 
 move_abspath_cloud=Ap(Aj) 
 send_command_time=Ap(AJ) 
 scan_status=Ap(AG) 
 scan_time=Ap(AJ) 
 scan_abspath=Ap(Aj) 
 plex_section_id=Ap(AG) 
 plex_show_id=Ap(AG) 
 plex_daum_id=Ap(AG) 
 plex_title=Ap(Aj) 
 plex_image=Ap(Aj) 
 plex_abspath=Ap(Aj)
 plex_part=Ap(Aj)
 log=Ap(Aj)
 def __repr__(self):
  return AW(self.as_dict())
 def as_dict(self):
  ret={x.name:Au(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')if self.created_time is not d else ''
  ret['send_command_time']=self.send_command_time.strftime('%m-%d %H:%M:%S')if self.send_command_time is not d else ''
  ret['scan_time']=self.scan_time.strftime('%m-%d %H:%M:%S')if self.scan_time is not d else ''
  return ret
 @g
 def create(entity):
  try:
   f=ModelKtvFile()
   f.original_filename=entity.original_filename
   f.filename=entity.filename
   f.created_time=entity.download_time
   f.move_type=E(entity.move_type)
   f.match_folder_name=entity.match_folder_name
   f.move_abspath_local=entity.move_abspath_local
   f.move_abspath_sync=entity.move_abspath_sync
   f.move_abspath_cloud=entity.move_abspath_cloud
   if entity.send_command_time!='':
    f.send_command_time=entity.send_command_time
   f.scan_status=E(entity.scan_status)
   f.scan_abspath=entity.scan_abspath
   f.plex_section_id=entity.plex_section_id
   f.plex_show_id=entity.plex_show_id
   f.plex_daum_id=entity.plex_daum_id
   f.plex_title=entity.plex_title
   f.plex_image=entity.plex_image
   f.plex_abspath=entity.plex_abspath
   f.log=entity.log
   return f
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
 @g
 def get_library_check_list():
  try:
   query=f.query(ModelKtvFile).filter_by(scan_status=1)
   query=query.filter(or_(ModelKtvFile.send_command_time.is_(d),ModelKtvFile.send_command_time<u.now()+o(hours=-1)))
   query=query.filter(ModelKtvFile.created_time>u.now()+o(hours=-24))
   ret=query.all()
   return ret
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
 @g
 def get_image_empty_list():
  try:
   query=f.query(ModelKtvFile).filter_by(scan_status=3)
   query=query.filter(ModelKtvFile.plex_image.is_(d))
   query=query.filter(ModelKtvFile.plex_show_id!=-1)
   query=query.filter(ModelKtvFile.created_time>u.now()+o(hours=-24))
   ret=query.all()
   return ret
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
