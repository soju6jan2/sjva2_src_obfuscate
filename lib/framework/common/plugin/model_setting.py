import traceback
S=True
g=False
D=repr
n=getattr
l=staticmethod
G=Exception
J=None
B=int
L=set
from framework import db
from framework.util import Util
def get_model_setting(package_name,logger):
 class ModelSetting(db.Model):
  __tablename__='%s_setting'%package_name
  __table_args__={'mysql_collate':'utf8_general_ci'}
  __bind_key__=package_name
  id=db.Column(db.Integer,primary_key=S)
  key=db.Column(db.String,unique=S,nullable=g)
  value=db.Column(db.String,nullable=g)
  def __init__(self,key,value):
   self.key=key
   self.value=value
  def __repr__(self):
   return D(self.as_dict())
  def as_dict(self):
   return{x.name:n(self,x.name)for x in self.__table__.columns}
  @l
  def get(key):
   try:
    return db.session.query(ModelSetting).filter_by(key=key).first().value.strip()
   except G as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @l
  def has_key(key):
   return(db.session.query(ModelSetting).filter_by(key=key).first()is not J)
  @l
  def get_int(key):
   try:
    return B(ModelSetting.get(key))
   except G as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @l
  def get_bool(key):
   try:
    return(ModelSetting.get(key)=='True')
   except G as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @l
  def L(key,value):
   try:
    item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    if item is not J:
     item.value=value.strip()if value is not J else value
     db.session.commit()
    else:
     db.session.add(ModelSetting(key,value.strip()))
   except G as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @l
  def to_dict():
   try:
    ret=Util.db_list_to_dict(db.session.query(ModelSetting).all())
    ret['package_name']=package_name
    return ret 
   except G as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
  @l
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
    return S 
   except G as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
    logger.debug('Error Key:%s Value:%s',key,value)
    return g
  @l
  def get_list(key,delimeter,comment=' #'):
   try:
    value=ModelSetting.get(key).replace('\n',delimeter)
    if comment is J:
     values=[x.strip()for x in value.split(delimeter)]
    else:
     values=[x.split(comment)[0].strip()for x in value.split(delimeter)]
    values=Util.get_list_except_empty(values)
    return values
   except G as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
    logger.error('Error Key:%s Value:%s',key,value)
 return ModelSetting
# Created by pyminifier (https://github.com/liftoff/pyminifier)
