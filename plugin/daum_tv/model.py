import traceback,os
P=True
b=None
F=repr
S=getattr
z=Exception
d=len
D=staticmethod
from datetime import datetime
import json
from framework.logger import get_logger
from framework import db,path_data,app
from sqlalchemy import or_,and_,func,not_
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
app.config['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(os.path.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelDaumTVShow(db.Model):
 __tablename__='%s_show_library'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=db.Column(db.Integer,primary_key=P)
 daum_id=db.Column(db.Integer)
 title=db.Column(db.String)
 status=db.Column(db.Integer)
 studio=db.Column(db.String)
 broadcast_info=db.Column(db.String)
 broadcast_term=db.Column(db.String)
 start_date=db.Column(db.String)
 genre=db.Column(db.String)
 summary=db.Column(db.String)
 poster_url=db.Column(db.String)
 episode_count_one_day=db.Column(db.Integer)
 episode_list_json=db.Column(db.JSON)
 update_time=db.Column(db.DateTime)
 last_episode_no=db.Column(db.String)
 last_episode_date=db.Column(db.String)
 search_title=db.Column(db.String)
 def __init__(self,daum_id):
  self.daum_id=daum_id
  self.episode_count_one_day=1
  self.studio=''
  self.broadcast_info=''
  self.broadcast_term=''
  self.episode_list=b
 def __repr__(self):
  return F(self.as_dict())
 def as_dict(self):
  ret={x.name:S(self,x.name)for x in self.__table__.columns}
  ret['episode_list_json']=json.loads(ret['episode_list_json'])
  ret['update_time']=self.update_time.strftime('%m-%d %H:%M:%S')
  return ret
 def save(self):
  try:
   self.update_time=datetime.now()
   self.search_title=self.title.replace(' ','').replace('-','').replace('/','').replace('!','').replace('(','').replace(')','').replace('#','')
   db.session.add(self)
   db.session.commit()
  except z as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 def has_episode_info(self):
  return d(self.episode_list)>0
 @D
 def get(daum_id):
  try:
   logger.debug('GET DaumID:%s',daum_id)
   item=db.session.query(ModelDaumTVShow).filter_by(daum_id=daum_id).with_for_update().first()
   if not item:
    item=ModelDaumTVShow(daum_id)
   if item.episode_list_json is not b:
    item.episode_list=json.loads(item.episode_list_json)
   return item
  except z as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
