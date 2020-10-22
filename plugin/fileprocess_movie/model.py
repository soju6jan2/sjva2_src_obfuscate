import os
c=True
h=repr
D=getattr
i=None
F=staticmethod
s=Exception
a=False
import traceback
from datetime import datetime
import json
from framework.logger import get_logger
from framework import db,app,path_data
from sqlalchemy import or_,and_,func,not_
from sqlalchemy.orm import backref
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
app.config['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(os.path.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelFileprocessMovieItem(db.Model):
 __tablename__='%s_item'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=db.Column(db.Integer,primary_key=c)
 created_time=db.Column(db.DateTime)
 filename=db.Column(db.String)
 source_dir=db.Column(db.String)
 is_file=db.Column(db.Boolean)
 flag_move=db.Column(db.Boolean)
 target=db.Column(db.String)
 dest_folder_name=db.Column(db.String)
 movie_title=db.Column(db.String)
 movie_id=db.Column(db.String)
 movie_poster=db.Column(db.String)
 movie_more_title=db.Column(db.String)
 movie_more_info=db.Column(db.String)
 json=db.Column(db.JSON)
 def __init__(self):
  self.created_time=datetime.now()
 def __repr__(self):
  return h(self.as_dict())
 def as_dict(self):
  ret={x.name:D(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  if self.json is not i:
   ret['json']=json.loads(ret['json'])
  else:
   ret['json']={}
  return ret
 @F
 def save(item):
  try:
   model=ModelFileprocessMovieItem()
   model.filename=item['name']
   model.source_dir=item['path']
   model.is_file=item['is_file']
   model.flag_move=item['flag_move']
   model.target=item['target']
   model.dest_folder_name=item['dest_folder_name']
   if item['movie']is not i:
    model.movie_title=item['movie']['title']
    model.movie_id=item['movie']['id']
    if 'more' in item['movie']:
     model.movie_poster=item['movie']['more']['poster']
     model.movie_more_title=item['movie']['more']['title']
     model.movie_more_info=item['movie']['more']['info'][0]
   if 'guessit' in item:
    del item['guessit']
   model.json=json.dumps(item)
   db.session.add(model)
   db.session.commit()
   return c
  except s as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.debug(item)
   db.session.rollback()
   logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
   return a
# Created by pyminifier (https://github.com/liftoff/pyminifier)
