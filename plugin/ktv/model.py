import os
V=True
G=repr
C=getattr
f=None
L=staticmethod
M=int
P=Exception
import traceback
import datetime
from framework.logger import get_logger
from framework import db,app,path_data
from sqlalchemy import or_,and_,func,not_
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
app.config['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(os.path.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelKtvLibrary(db.Model):
 __tablename__='%s_library'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=db.Column(db.Integer,primary_key=V)
 library_type=db.Column(db.Integer)
 library_path=db.Column(db.String)
 rclone_path=db.Column(db.String)
 replace_for_plex_source=db.Column(db.String)
 replace_for_plex_target=db.Column(db.String)
 index=db.Column(db.Integer)
 def __repr__(self):
  return G(self.as_dict())
 def as_dict(self):
  return{x.name:C(self,x.name)for x in self.__table__.columns}
class ModelKtvFile(db.Model):
 __tablename__='%s_file'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=db.Column(db.Integer,primary_key=V)
 original_filename=db.Column(db.String)
 filename=db.Column(db.String)
 created_time=db.Column(db.DateTime)
 move_type=db.Column(db.Integer)
 match_folder_name=db.Column(db.String) 
 move_abspath_local=db.Column(db.String) 
 move_abspath_sync=db.Column(db.String) 
 move_abspath_cloud=db.Column(db.String) 
 send_command_time=db.Column(db.DateTime) 
 scan_status=db.Column(db.Integer) 
 scan_time=db.Column(db.DateTime) 
 scan_abspath=db.Column(db.String) 
 plex_section_id=db.Column(db.Integer) 
 plex_show_id=db.Column(db.Integer) 
 plex_daum_id=db.Column(db.Integer) 
 plex_title=db.Column(db.String) 
 plex_image=db.Column(db.String) 
 plex_abspath=db.Column(db.String)
 plex_part=db.Column(db.String)
 log=db.Column(db.String)
 def __repr__(self):
  return G(self.as_dict())
 def as_dict(self):
  ret={x.name:C(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')if self.created_time is not f else ''
  ret['send_command_time']=self.send_command_time.strftime('%m-%d %H:%M:%S')if self.send_command_time is not f else ''
  ret['scan_time']=self.scan_time.strftime('%m-%d %H:%M:%S')if self.scan_time is not f else ''
  return ret
 @L
 def create(entity):
  try:
   f=ModelKtvFile()
   f.original_filename=entity.original_filename
   f.filename=entity.filename
   f.created_time=entity.download_time
   f.move_type=M(entity.move_type)
   f.match_folder_name=entity.match_folder_name
   f.move_abspath_local=entity.move_abspath_local
   f.move_abspath_sync=entity.move_abspath_sync
   f.move_abspath_cloud=entity.move_abspath_cloud
   if entity.send_command_time!='':
    f.send_command_time=entity.send_command_time
   f.scan_status=M(entity.scan_status)
   f.scan_abspath=entity.scan_abspath
   f.plex_section_id=entity.plex_section_id
   f.plex_show_id=entity.plex_show_id
   f.plex_daum_id=entity.plex_daum_id
   f.plex_title=entity.plex_title
   f.plex_image=entity.plex_image
   f.plex_abspath=entity.plex_abspath
   f.log=entity.log
   return f
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @L
 def get_library_check_list():
  try:
   query=db.session.query(ModelKtvFile).filter_by(scan_status=1)
   query=query.filter(or_(ModelKtvFile.send_command_time.is_(f),ModelKtvFile.send_command_time<datetime.datetime.now()+datetime.timedelta(hours=-1)))
   query=query.filter(ModelKtvFile.created_time>datetime.datetime.now()+datetime.timedelta(hours=-24))
   ret=query.all()
   return ret
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @L
 def get_image_empty_list():
  try:
   query=db.session.query(ModelKtvFile).filter_by(scan_status=3)
   query=query.filter(ModelKtvFile.plex_image.is_(f))
   query=query.filter(ModelKtvFile.plex_show_id!=-1)
   query=query.filter(ModelKtvFile.created_time>datetime.datetime.now()+datetime.timedelta(hours=-24))
   ret=query.all()
   return ret
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
