import traceback,os
H=True
B=None
w=repr
Q=getattr
t=Exception
e=len
U=staticmethod
i=os.path
s=traceback.format_exc
from datetime import datetime
c=datetime.now
import json
K=json.loads
from framework.logger import get_logger
from framework import db,path_data,app
O=app.config
j=db.session
F=db.DateTime
b=db.JSON
S=db.String
G=db.Integer
n=db.Column
J=db.Model
from sqlalchemy import or_,and_,func,not_
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
O['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(i.join(path_data,'db','%s.db'%package_name))
from framework.common.plugin import get_model_setting
ModelSetting=get_model_setting(package_name,logger)
class ModelDaumTVShow(J):
 __tablename__='%s_show_library'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 id=n(G,primary_key=H)
 daum_id=n(G)
 title=n(S)
 status=n(G)
 studio=n(S)
 broadcast_info=n(S)
 broadcast_term=n(S)
 start_date=n(S)
 genre=n(S)
 summary=n(S)
 poster_url=n(S)
 episode_count_one_day=n(G)
 episode_list_json=n(b)
 update_time=n(F)
 last_episode_no=n(S)
 last_episode_date=n(S)
 search_title=n(S)
 def __init__(self,daum_id):
  self.daum_id=daum_id
  self.episode_count_one_day=1
  self.studio=''
  self.broadcast_info=''
  self.broadcast_term=''
  self.episode_list=B
 def __repr__(self):
  return w(self.as_dict())
 def as_dict(self):
  ret={x.name:Q(self,x.name)for x in self.__table__.columns}
  ret['episode_list_json']=K(ret['episode_list_json'])
  ret['update_time']=self.update_time.strftime('%m-%d %H:%M:%S')
  return ret
 def save(self):
  try:
   self.update_time=c()
   self.search_title=self.title.replace(' ','').replace('-','').replace('/','').replace('!','').replace('(','').replace(')','').replace('#','')
   j.add(self)
   j.commit()
  except t as e:
   logger.error('Exception:%s',e)
   logger.error(s()) 
 def has_episode_info(self):
  return e(self.episode_list)>0
 @U
 def get(daum_id):
  try:
   logger.debug('GET DaumID:%s',daum_id)
   item=j.query(ModelDaumTVShow).filter_by(daum_id=daum_id).with_for_update().first()
   if not item:
    item=ModelDaumTVShow(daum_id)
   if item.episode_list_json is not B:
    item.episode_list=K(item.episode_list_json)
   return item
  except t as e:
   logger.error('Exception:%s',e)
   logger.error(s())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
