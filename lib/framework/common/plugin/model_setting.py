import traceback
x=True
s=False
N=repr
w=getattr
o=staticmethod
U=Exception
Q=None
t=int
P=set
I=traceback.format_exc
from framework import db
F=db.session
h=db.String
r=db.Integer
e=db.Column
i=db.Model
from framework.util import Util
b=Util.get_list_except_empty
l=Util.db_list_to_dict
def get_model_setting(package_name,logger):
 class ModelSetting(i):
  __tablename__='%s_setting'%package_name
  __table_args__={'mysql_collate':'utf8_general_ci'}
  __bind_key__=package_name
  id=e(r,primary_key=x)
  key=e(h,unique=x,nullable=s)
  value=e(h,nullable=s)
  def __init__(self,key,value):
   self.key=key
   self.value=value
  def __repr__(self):
   return N(self.as_dict())
  def as_dict(self):
   return{x.name:w(self,x.name)for x in self.__table__.columns}
  @o
  def get(key):
   try:
    return F.query(ModelSetting).filter_by(key=key).first().value.strip()
   except U as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(I())
  @o
  def has_key(key):
   return(F.query(ModelSetting).filter_by(key=key).first()is not Q)
  @o
  def get_int(key):
   try:
    return t(ModelSetting.get(key))
   except U as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(I())
  @o
  def get_bool(key):
   try:
    return(ModelSetting.get(key)=='True')
   except U as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(I())
  @o
  def P(key,value):
   try:
    item=F.query(ModelSetting).filter_by(key=key).with_for_update().first()
    if item is not Q:
     item.value=value.strip()if value is not Q else value
     F.commit()
    else:
     F.add(ModelSetting(key,value.strip()))
   except U as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(I())
  @o
  def to_dict():
   try:
    ret=l(F.query(ModelSetting).all())
    ret['package_name']=package_name
    return ret 
   except U as e:
    logger.error('Exception:%s',e)
    logger.error(I())
  @o
  def setting_save(req):
   try:
    for key,value in req.form.items():
     if key in['scheduler','is_running']:
      continue
     if key.startswith('global_')or key.startswith('tmp_'):
      continue
     logger.debug('Key:%s Value:%s',key,value)
     entity=F.query(ModelSetting).filter_by(key=key).with_for_update().first()
     entity.value=value
    F.commit()
    return x 
   except U as e:
    logger.error('Exception:%s',e)
    logger.error(I())
    logger.debug('Error Key:%s Value:%s',key,value)
    return s
  @o
  def get_list(key,delimeter,comment=' #'):
   try:
    value=ModelSetting.get(key).replace('\n',delimeter)
    if comment is Q:
     values=[x.strip()for x in value.split(delimeter)]
    else:
     values=[x.split(comment)[0].strip()for x in value.split(delimeter)]
    values=b(values)
    return values
   except U as e:
    logger.error('Exception:%s',e)
    logger.error(I())
    logger.error('Error Key:%s Value:%s',key,value)
 return ModelSetting
# Created by pyminifier (https://github.com/liftoff/pyminifier)
