import traceback
y=True
M=False
R=repr
E=getattr
q=staticmethod
e=Exception
j=None
D=int
h=set
from framework import db
from framework.util import Util
def get_model_setting(package_name,logger):
 class ModelSetting(db.Model):
  __tablename__='%s_setting'%package_name
  __table_args__={'mysql_collate':'utf8_general_ci'}
  __bind_key__=package_name
  id=db.Column(db.Integer,primary_key=y)
  key=db.Column(db.String,unique=y,nullable=M)
  value=db.Column(db.String,nullable=M)
  def __init__(self,key,value):
   self.key=key
   self.value=value
  def __repr__(self):
   return R(self.as_dict())
  def as_dict(self):
   return{x.name:E(self,x.name)for x in self.__table__.columns}
  @q
  def get(key):
   try:
    return db.session.query(ModelSetting).filter_by(key=key).first().value.strip()
   except e as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @q
  def has_key(key):
   return(db.session.query(ModelSetting).filter_by(key=key).first()is not j)
  @q
  def get_int(key):
   try:
    return D(ModelSetting.get(key))
   except e as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @q
  def get_bool(key):
   try:
    return(ModelSetting.get(key)=='True')
   except e as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @q
  def h(key,value):
   try:
    item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    if item is not j:
     item.value=value.strip()if value is not j else value
     db.session.commit()
    else:
     db.session.add(ModelSetting(key,value.strip()))
   except e as e:
    logger.error('Exception:%s %s',e,key)
    logger.error(traceback.format_exc())
  @q
  def to_dict():
   try:
    ret=Util.db_list_to_dict(db.session.query(ModelSetting).all())
    ret['package_name']=package_name
    return ret 
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
  @q
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
    return y 
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
    logger.debug('Error Key:%s Value:%s',key,value)
    return M
  @q
  def get_list(key,delimeter,comment=' #'):
   try:
    value=ModelSetting.get(key).replace('\n',delimeter)
    if comment is j:
     values=[x.strip()for x in value.split(delimeter)]
    else:
     values=[x.split(comment)[0].strip()for x in value.split(delimeter)]
    values=Util.get_list_except_empty(values)
    return values
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
    logger.error('Error Key:%s Value:%s',key,value)
 return ModelSetting
# Created by pyminifier (https://github.com/liftoff/pyminifier)
