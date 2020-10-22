import os
J=True
xd=repr
xa=getattr
T=None
G=staticmethod
l=Exception
V=False
x=os.path
import traceback
c=traceback.format_exc
from datetime import datetime
H=datetime.now
import json
h=json.dumps
X=json.loads
from framework.logger import get_logger
from framework import db,app,path_data
i=app.config
R=db.session
z=db.JSON
j=db.Boolean
F=db.String
Q=db.DateTime
u=db.Integer
n=db.Column
M=db.Model
from sqlalchemy import or_,and_,func,not_
from sqlalchemy.orm import backref
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
i['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(x.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelFileprocessMovieItem(M):
 __tablename__='%s_item'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=n(u,primary_key=J)
 created_time=n(Q)
 filename=n(F)
 source_dir=n(F)
 is_file=n(j)
 flag_move=n(j)
 target=n(F)
 dest_folder_name=n(F)
 movie_title=n(F)
 movie_id=n(F)
 movie_poster=n(F)
 movie_more_title=n(F)
 movie_more_info=n(F)
 json=n(z)
 def __init__(self):
  self.created_time=H()
 def __repr__(self):
  return xd(self.as_dict())
 def as_dict(self):
  ret={x.name:xa(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  if self.json is not T:
   ret['json']=X(ret['json'])
  else:
   ret['json']={}
  return ret
 @G
 def save(item):
  try:
   model=ModelFileprocessMovieItem()
   model.filename=item['name']
   model.source_dir=item['path']
   model.is_file=item['is_file']
   model.flag_move=item['flag_move']
   model.target=item['target']
   model.dest_folder_name=item['dest_folder_name']
   if item['movie']is not T:
    model.movie_title=item['movie']['title']
    model.movie_id=item['movie']['id']
    if 'more' in item['movie']:
     model.movie_poster=item['movie']['more']['poster']
     model.movie_more_title=item['movie']['more']['title']
     model.movie_more_info=item['movie']['more']['info'][0]
   if 'guessit' in item:
    del item['guessit']
   model.json=h(item)
   R.add(model)
   R.commit()
   return J
  except l as e:
   logger.error('Exception:%s',e)
   logger.error(c())
   logger.debug(item)
   R.rollback()
   logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
   return V
# Created by pyminifier (https://github.com/liftoff/pyminifier)
