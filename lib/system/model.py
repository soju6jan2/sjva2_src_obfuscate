import traceback
P=True
O=False
C=getattr
X=staticmethod
H=Exception
i=int
Q=set
t=None
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class ModelSetting(db.Model):
 __tablename__='system_setting'
 id=db.Column(db.Integer,primary_key=P)
 key=db.Column(db.String(100),unique=P,nullable=O)
 value=db.Column(db.String(100),nullable=O)
 def __init__(self,key,value):
  self.key=key
  self.value=value
 def __repr__(self):
  return "<SystemSetting(id:%s, key:%s, value:%s)>"%(self.id,self.key,self.value)
 def as_dict(self):
  return{x.name:C(self,x.name)for x in self.__table__.columns}
 @X
 def get(key):
  try:
   return db.session.query(ModelSetting).filter_by(key=key).first().value.strip()
  except H as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @X
 def get_int(key):
  try:
   return i(ModelSetting.get(key))
  except H as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @X
 def get_bool(key):
  try:
   return(ModelSetting.get(key)=='True')
  except H as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @X
 def Q(key,value):
  try:
   logger.debug(key)
   item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
   if item is not t:
    item.value=value.strip()if value is not t else value
    db.session.commit()
   else:
    db.session.add(ModelSetting(key,value.strip()))
  except H as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(traceback.format_exc())
 @X
 def to_dict():
  try:
   from framework.util import Util
   arg=Util.db_list_to_dict(db.session.query(ModelSetting).all())
   arg['package_name']=package_name
   return arg
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @X
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
   return P 
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.debug('Error Key:%s Value:%s',key,value)
   return O
 @X
 def get_list(key):
  try:
   value=ModelSetting.get(key)
   values=[x.strip().replace(' ','').strip()for x in value.replace('\n','|').split('|')]
   values=Util.get_list_except_empty(values)
   return values
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   logger.error('Error Key:%s Value:%s',key,value)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
