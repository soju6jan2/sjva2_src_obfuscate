import traceback
Y=True
x=False
r=getattr
d=staticmethod
h=None
o=Exception
e=int
m=set
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class ModelSetting(db.Model):
 __tablename__='system_setting'
 id=db.Column(db.Integer,primary_key=Y)
 key=db.Column(db.String(100),unique=Y,nullable=x)
 value=db.Column(db.String(100),nullable=x)
 def __init__(self,key,value):
  self.key=key
  self.value=value
 def __repr__(self):
  return "<SystemSetting(id:%s, key:%s, value:%s)>"%(self.id,self.key,self.value)
 def as_dict(self):
  return{x.name:r(self,x.name)for x in self.__table__.columns}
 @d
 def get(key):
  try:
   ret=db.session.query(ModelSetting).filter_by(key=key).first()
   if ret is not h:
    return ret.value.strip()
   else:
    return ''
  except o as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @d
 def get_int(key):
  try:
   return e(ModelSetting.get(key))
  except o as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @d
 def get_bool(key):
  try:
   return(ModelSetting.get(key)=='True')
  except o as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @d
 def m(key,value):
  try:
   logger.debug(key)
   item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
   if item is not h:
    item.value=value.strip()if value is not h else value
    db.session.commit()
   else:
    db.session.add(ModelSetting(key,value.strip()))
  except o as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @d
 def to_dict():
  try:
   from framework.util import Util
   arg=Util.db_list_to_dict(db.session.query(ModelSetting).all())
   arg['package_name']=package_name
   return arg
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
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
   return Y 
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.debug('Error Key:%s Value:%s',key,value)
   return x
 @d
 def get_list(key):
  try:
   value=ModelSetting.get(key)
   values=[x.strip().replace(' ','').strip()for x in value.replace('\n','|').split('|')]
   values=Util.get_list_except_empty(values)
   return values
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('Error Key:%s Value:%s',key,value)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
