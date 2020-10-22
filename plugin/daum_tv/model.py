import traceback,os
s=True
h=None
J=repr
A=getattr
g=Exception
M=len
i=staticmethod
a=os.path
c=traceback.format_exc
from datetime import datetime
E=datetime.now
import json
H=json.loads
from framework.logger import get_logger
from framework import db,path_data,app
R=app.config
j=db.session
I=db.DateTime
x=db.JSON
k=db.String
O=db.Integer
N=db.Column
o=db.Model
from sqlalchemy import or_,and_,func,not_
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
R['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(a.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelDaumTVShow(o):
 __tablename__='%s_show_library'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=N(O,primary_key=s)
 daum_id=N(O)
 title=N(k)
 status=N(O)
 studio=N(k)
 broadcast_info=N(k)
 broadcast_term=N(k)
 start_date=N(k)
 genre=N(k)
 summary=N(k)
 poster_url=N(k)
 episode_count_one_day=N(O)
 episode_list_json=N(x)
 update_time=N(I)
 last_episode_no=N(k)
 last_episode_date=N(k)
 search_title=N(k)
 def __init__(self,daum_id):
  self.daum_id=daum_id
  self.episode_count_one_day=1
  self.studio=''
  self.broadcast_info=''
  self.broadcast_term=''
  self.episode_list=h
 def __repr__(self):
  return J(self.as_dict())
 def as_dict(self):
  ret={x.name:A(self,x.name)for x in self.__table__.columns}
  ret['episode_list_json']=H(ret['episode_list_json'])
  ret['update_time']=self.update_time.strftime('%m-%d %H:%M:%S')
  return ret
 def save(self):
  try:
   self.update_time=E()
   self.search_title=self.title.replace(' ','').replace('-','').replace('/','').replace('!','').replace('(','').replace(')','').replace('#','')
   j.add(self)
   j.commit()
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(c()) 
 def has_episode_info(self):
  return M(self.episode_list)>0
 @i
 def get(daum_id):
  try:
   logger.debug('GET DaumID:%s',daum_id)
   item=j.query(ModelDaumTVShow).filter_by(daum_id=daum_id).with_for_update().first()
   if not item:
    item=ModelDaumTVShow(daum_id)
   if item.episode_list_json is not h:
    item.episode_list=H(item.episode_list_json)
   return item
  except g as e:
   logger.error('Exception:%s',e)
   logger.error(c())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
