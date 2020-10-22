import traceback
B=True
U=False
Y=getattr
s=staticmethod
S=Exception
u=int
g=set
X=None
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class ModelSetting(db.Model):
 __tablename__='system_setting'
 id=db.Column(db.Integer,primary_key=B)
 key=db.Column(db.String(100),unique=B,nullable=U)
 value=db.Column(db.String(100),nullable=U)
 def __init__(self,key,value):
  self.key=key
  self.value=value
 def __repr__(self):
  return "<SystemSetting(id:%s, key:%s, value:%s)>"%(self.id,self.key,self.value)
 def as_dict(self):
  return{x.name:Y(self,x.name)for x in self.__table__.columns}
 @s
 def get(key):
  try:
   return db.session.query(ModelSetting).filter_by(key=key).first().value.strip()
  except S as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @s
 def get_int(key):
  try:
   return u(ModelSetting.get(key))
  except S as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @s
 def get_bool(key):
  try:
   return(ModelSetting.get(key)=='True')
  except S as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @s
 def g(key,value):
  try:
   logger.debug(key)
   item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
   if item is not X:
    item.value=value.strip()if value is not X else value
    db.session.commit()
   else:
    db.session.add(ModelSetting(key,value.strip()))
  except S as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @s
 def to_dict():
  try:
   from framework.util import Util
   arg=Util.db_list_to_dict(db.session.query(ModelSetting).all())
   arg['package_name']=package_name
   return arg
  except S as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @s
 def setting_save(req):
  try:
   for key,value in req.form.items():
    if key in['scheduler','is_running']:
     continue
    if key.startswith('tmp_'):
     continue
    logger.debug('Key:%s Value:%s',key,value)
    entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   db.session.commit()
   return B 
  except S as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.debug('Error Key:%s Value:%s',key,value)
   return U
 @s
 def get_list(key):
  try:
   value=ModelSetting.get(key)
   values=[x.strip().replace(' ','').strip()for x in value.replace('\n','|').split('|')]
   values=Util.get_list_except_empty(values)
   return values
  except S as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('Error Key:%s Value:%s',key,value)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
