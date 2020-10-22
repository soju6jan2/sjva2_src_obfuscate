import os
X=True
oe=repr
ot=getattr
K=None
C=staticmethod
i=Exception
S=False
o=os.path
import traceback
B=traceback.format_exc
from datetime import datetime
N=datetime.now
import json
r=json.dumps
A=json.loads
from framework.logger import get_logger
from framework import db,app,path_data
L=app.config
g=db.session
m=db.JSON
O=db.Boolean
a=db.String
E=db.DateTime
M=db.Integer
Q=db.Column
n=db.Model
from sqlalchemy import or_,and_,func,not_
from sqlalchemy.orm import backref
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
L['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(o.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelFileprocessMovieItem(n):
 __tablename__='%s_item'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=Q(M,primary_key=X)
 created_time=Q(E)
 filename=Q(a)
 source_dir=Q(a)
 is_file=Q(O)
 flag_move=Q(O)
 target=Q(a)
 dest_folder_name=Q(a)
 movie_title=Q(a)
 movie_id=Q(a)
 movie_poster=Q(a)
 movie_more_title=Q(a)
 movie_more_info=Q(a)
 json=Q(m)
 def __init__(self):
  self.created_time=N()
 def __repr__(self):
  return oe(self.as_dict())
 def as_dict(self):
  ret={x.name:ot(self,x.name)for x in self.__table__.columns}
  ret['created_time']=self.created_time.strftime('%m-%d %H:%M:%S')
  if self.json is not K:
   ret['json']=A(ret['json'])
  else:
   ret['json']={}
  return ret
 @C
 def save(item):
  try:
   model=ModelFileprocessMovieItem()
   model.filename=item['name']
   model.source_dir=item['path']
   model.is_file=item['is_file']
   model.flag_move=item['flag_move']
   model.target=item['target']
   model.dest_folder_name=item['dest_folder_name']
   if item['movie']is not K:
    model.movie_title=item['movie']['title']
    model.movie_id=item['movie']['id']
    if 'more' in item['movie']:
     model.movie_poster=item['movie']['more']['poster']
     model.movie_more_title=item['movie']['more']['title']
     model.movie_more_info=item['movie']['more']['info'][0]
   if 'guessit' in item:
    del item['guessit']
   model.json=r(item)
   g.add(model)
   g.commit()
   return X
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(B())
   logger.debug(item)
   g.rollback()
   logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
   return S
# Created by pyminifier (https://github.com/liftoff/pyminifier)
