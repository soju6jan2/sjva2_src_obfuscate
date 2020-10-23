import traceback
p=True
W=False
f=getattr
D=staticmethod
M=None
x=Exception
b=int
q=set
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class ModelSetting(db.Model):
 __tablename__='system_setting'
 id=db.Column(db.Integer,primary_key=p)
 key=db.Column(db.String(100),unique=p,nullable=W)
 value=db.Column(db.String(100),nullable=W)
 def __init__(self,key,value):
  self.key=key
  self.value=value
 def __repr__(self):
  return "<SystemSetting(id:%s, key:%s, value:%s)>"%(self.id,self.key,self.value)
 def as_dict(self):
  return{x.name:f(self,x.name)for x in self.__table__.columns}
 @D
 def get(key):
  try:
   ret=db.session.query(ModelSetting).filter_by(key=key).first()
   if ret is not M:
    return ret.value.strip()
   else:
    return ''
  except x as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @D
 def get_int(key):
  try:
   return b(ModelSetting.get(key))
  except x as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @D
 def get_bool(key):
  try:
   return(ModelSetting.get(key)=='True')
  except x as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @D
 def q(key,value):
  try:
   logger.debug(key)
   item=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
   if item is not M:
    item.value=value.strip()if value is not M else value
    db.session.commit()
   else:
    db.session.add(ModelSetting(key,value.strip()))
  except x as exception:
   logger.error('Exception:%s %s',exception,key)
   logger.error(traceback.format_exc())
 @D
 def to_dict():
  try:
   from framework.util import Util
   arg=Util.db_list_to_dict(db.session.query(ModelSetting).all())
   arg['package_name']=package_name
   return arg
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @D
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
   return p 
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.debug('Error Key:%s Value:%s',key,value)
   return W
 @D
 def get_list(key):
  try:
   value=ModelSetting.get(key)
   values=[x.strip().replace(' ','').strip()for x in value.replace('\n','|').split('|')]
   values=Util.get_list_except_empty(values)
   return values
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('Error Key:%s Value:%s',key,value)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
