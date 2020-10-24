import traceback
h=True
a=False
S=repr
T=getattr
U=staticmethod
t=None
o=Exception
f=int
X=set
from framework import db
from framework.util import Util
def get_model_setting(package_name,logger):
 class ModelSetting(db.Model):
  __tablename__='%s_setting'%package_name
  __table_args__={'mysql_collate':'utf8_general_ci'}
  __bind_key__=package_name
  id=db.Column(db.Integer,primary_key=h)
  key=db.Column(db.String,unique=h,nullable=a)
  value=db.Column(db.String,nullable=a)
  def __init__(self,key,value):
   self.key=key
   self.value=value
  def __repr__(self):
   return S(self.as_dict())
  def as_dict(self):
   return{x.name:T(self,x.name)for x in self.__table__.columns}
  @U
  def get(key):
   try:
    ret=db.session.query(ModelSetting).filter_by(key=key).first()
    if ret is not t:
     return ret.value.strip()
    return t
   except o as exception:
    logger.error('Exception:%s %s',exception,key)
    logger.error(traceback.format_exc())
  @U
  def has_key(key):
   return(db.session.query(ModelSetting).filter_by(key=key).first()is not t)
  @U
  def get_int(key):
   try:
    return f(ModelSetting.get(key))
   except o as exception:
    logger.error('Exception:%s %s',exception,key)
    logger.error(traceback.format_exc())
  @U
  def get_bool(key):
   try:
    return(ModelSetting.get(key)=='True')
   except o as exception:
    logger.error('Exception:%s %s',exception,key)
    logger.error(traceback.format_exc())
  @U
  def X(key,value):
   try:
    item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    if item is not t:
     item.value=value.strip()if value is not t else value
     db.session.commit()
    else:
     db.session.add(ModelSetting(key,value.strip()))
   except o as exception:
    logger.error('Exception:%s %s',exception,key)
    logger.error(traceback.format_exc())
  @U
  def to_dict():
   try:
    ret=Util.db_list_to_dict(db.session.query(ModelSetting).all())
    ret['package_name']=package_name
    return ret 
   except o as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  @U
  def setting_save(req):
   try:
    for key,value in req.form.items():
     if key in['scheduler','is_running']:
      continue
     if key.startswith('global_')or key.startswith('tmp_'):
      continue
     logger.debug('Key:%s Value:%s',key,value)
     entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
     entity.value=value
    db.session.commit()
    return h 
   except o as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
    logger.debug('Error Key:%s Value:%s',key,value)
    return a
  @U
  def get_list(key,delimeter,comment=' #'):
   try:
    value=ModelSetting.get(key).replace('\n',delimeter)
    if comment is t:
     values=[x.strip()for x in value.split(delimeter)]
    else:
     values=[x.split(comment)[0].strip()for x in value.split(delimeter)]
    values=Util.get_list_except_empty(values)
    return values
   except o as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
    logger.error('Error Key:%s Value:%s',key,value)
 return ModelSetting
# Created by pyminifier (https://github.com/liftoff/pyminifier)
