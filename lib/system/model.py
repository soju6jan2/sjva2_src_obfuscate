import traceback
k=True
C=False
q=getattr
v=staticmethod
V=Exception
Y=int
D=set
W=None
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class ModelSetting(db.Model):
 __tablename__='system_setting'
 id=db.Column(db.Integer,primary_key=k)
 key=db.Column(db.String(100),unique=k,nullable=C)
 value=db.Column(db.String(100),nullable=C)
 def __init__(self,key,value):
  self.key=key
  self.value=value
 def __repr__(self):
  return "<SystemSetting(id:%s, key:%s, value:%s)>"%(self.id,self.key,self.value)
 def as_dict(self):
  return{x.name:q(self,x.name)for x in self.__table__.columns}
 @v
 def get(key):
  try:
   return db.session.query(ModelSetting).filter_by(key=key).first().value.strip()
  except V as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @v
 def get_int(key):
  try:
   return Y(ModelSetting.get(key))
  except V as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @v
 def get_bool(key):
  try:
   return(ModelSetting.get(key)=='True')
  except V as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @v
 def D(key,value):
  try:
   logger.debug(key)
   item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
   if item is not W:
    item.value=value.strip()if value is not W else value
    db.session.commit()
   else:
    db.session.add(ModelSetting(key,value.strip()))
  except V as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @v
 def to_dict():
  try:
   from framework.util import Util
   arg=Util.db_list_to_dict(db.session.query(ModelSetting).all())
   arg['package_name']=package_name
   return arg
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @v
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
   return k 
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.debug('Error Key:%s Value:%s',key,value)
   return C
 @v
 def get_list(key):
  try:
   value=ModelSetting.get(key)
   values=[x.strip().replace(' ','').strip()for x in value.replace('\n','|').split('|')]
   values=Util.get_list_except_empty(values)
   return values
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('Error Key:%s Value:%s',key,value)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
