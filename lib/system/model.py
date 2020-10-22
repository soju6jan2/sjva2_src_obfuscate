import traceback
o=True
j=False
T=getattr
N=staticmethod
e=Exception
E=int
HR=set
Q=None
H=traceback.format_exc
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler
c=db.session
Hi=db.String
Hw=db.Integer
HV=db.Column
Hf=db.Model
from framework.util import Util
HO=Util.get_list_except_empty
HM=Util.db_list_to_dict
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class ModelSetting(Hf):
 __tablename__='system_setting'
 id=HV(Hw,primary_key=o)
 key=HV(Hi(100),unique=o,nullable=j)
 value=HV(Hi(100),nullable=j)
 def __init__(self,key,value):
  self.key=key
  self.value=value
 def __repr__(self):
  return "<SystemSetting(id:%s, key:%s, value:%s)>"%(self.id,self.key,self.value)
 def as_dict(self):
  return{x.name:T(self,x.name)for x in self.__table__.columns}
 @N
 def get(key):
  try:
   return c.query(ModelSetting).filter_by(key=key).first().value.strip()
  except e as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(H())
 @N
 def get_int(key):
  try:
   return E(ModelSetting.get(key))
  except e as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(H())
 @N
 def get_bool(key):
  try:
   return(ModelSetting.get(key)=='True')
  except e as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(H())
 @N
 def HR(key,value):
  try:
   logger.debug(key)
   item=c.query(ModelSetting).filter_by(key=key).with_for_update().first()
   if item is not Q:
    item.value=value.strip()if value is not Q else value
    c.commit()
   else:
    c.add(ModelSetting(key,value.strip()))
  except e as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(H())
 @N
 def to_dict():
  try:
   from framework.util import Util
   arg=HM(c.query(ModelSetting).all())
      HO=Util.get_list_except_empty
      HM=Util.db_list_to_dict
   arg['package_name']=package_name
   return arg
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H())
 @N
 def setting_save(req):
  try:
   for key,value in req.form.items():
    if key in['scheduler','is_running']:
     continue
    if key.startswith('tmp_'):
     continue
    logger.debug('Key:%s Value:%s',key,value)
    entity=c.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   c.commit()
   return o 
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H())
   logger.debug('Error Key:%s Value:%s',key,value)
   return j
 @N
 def get_list(key):
  try:
   value=ModelSetting.get(key)
   values=[x.strip().replace(' ','').strip()for x in value.replace('\n','|').split('|')]
   values=HO(values)
   return values
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H())
   logger.error('Error Key:%s Value:%s',key,value)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
