import traceback
I=True
z=False
P=repr
i=getattr
k=staticmethod
V=Exception
v=None
h=int
U=set
u=traceback.format_exc
from framework import db
c=db.session
q=db.String
e=db.Integer
s=db.Column
R=db.Model
from framework.util import Util
E=Util.get_list_except_empty
Y=Util.db_list_to_dict
def get_model_setting(package_name,logger):
 class ModelSetting(R):
  __tablename__='%s_setting'%package_name
  __table_args__={'mysql_collate':'utf8_general_ci'}
  __bind_key__=package_name
  id=s(e,primary_key=I)
  key=s(q,unique=I,nullable=z)
  value=s(q,nullable=z)
  def __init__(self,key,value):
   self.key=key
   self.value=value
  def __repr__(self):
   return P(self.as_dict())
  def as_dict(self):
   return{x.name:i(self,x.name)for x in self.__table__.columns}
  @k
  def get(key):
   try:
    return c.query(ModelSetting).filter_by(key=key).first().value.strip()
   except V as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(u())
  @k
  def has_key(key):
   return(c.query(ModelSetting).filter_by(key=key).first()is not v)
  @k
  def get_int(key):
   try:
    return h(ModelSetting.get(key))
   except V as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(u())
  @k
  def get_bool(key):
   try:
    return(ModelSetting.get(key)=='True')
   except V as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(u())
  @k
  def U(key,value):
   try:
    item=c.query(ModelSetting).filter_by(key=key).with_for_update().first()
    if item is not v:
     item.value=value.strip()if value is not v else value
     c.commit()
    else:
     c.add(ModelSetting(key,value.strip()))
   except V as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(u())
  @k
  def to_dict():
   try:
    ret=Y(c.query(ModelSetting).all())
    ret['package_name']=package_name
    return ret 
   except V as e:
    logger.error('Exception:%s',e)
    logger.error(u())
  @k
  def setting_save(req):
   try:
    for key,value in req.form.items():
     if key in['scheduler','is_running']:
      continue
     if key.startswith('global_')or key.startswith('tmp_'):
      continue
     logger.debug('Key:%s Value:%s',key,value)
     entity=c.query(ModelSetting).filter_by(key=key).with_for_update().first()
     entity.value=value
    c.commit()
    return I 
   except V as e:
    logger.error('Exception:%s',e)
    logger.error(u())
    logger.debug('Error Key:%s Value:%s',key,value)
    return z
  @k
  def get_list(key,delimeter,comment=' #'):
   try:
    value=ModelSetting.get(key).replace('\n',delimeter)
    if comment is v:
     values=[x.strip()for x in value.split(delimeter)]
    else:
     values=[x.split(comment)[0].strip()for x in value.split(delimeter)]
    values=E(values)
    return values
   except V as e:
    logger.error('Exception:%s',e)
    logger.error(u())
    logger.error('Error Key:%s Value:%s',key,value)
 return ModelSetting
# Created by pyminifier (https://github.com/liftoff/pyminifier)
