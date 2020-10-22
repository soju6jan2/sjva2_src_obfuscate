import traceback
i=True
C=False
F=getattr
h=staticmethod
j=Exception
g=int
VT=set
H=None
V=traceback.format_exc
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler
K=db.session
Vv=db.String
VO=db.Integer
VW=db.Column
Vf=db.Model
from framework.util import Util
VL=Util.get_list_except_empty
Vc=Util.db_list_to_dict
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class ModelSetting(Vf):
 __tablename__='system_setting'
 id=VW(VO,primary_key=i)
 key=VW(Vv(100),unique=i,nullable=C)
 value=VW(Vv(100),nullable=C)
 def __init__(self,key,value):
  self.key=key
  self.value=value
 def __repr__(self):
  return "<SystemSetting(id:%s, key:%s, value:%s)>"%(self.id,self.key,self.value)
 def as_dict(self):
  return{x.name:F(self,x.name)for x in self.__table__.columns}
 @h
 def get(key):
  try:
   return K.query(ModelSetting).filter_by(key=key).first().value.strip()
  except j as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(V())
 @h
 def get_int(key):
  try:
   return g(ModelSetting.get(key))
  except j as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(V())
 @h
 def get_bool(key):
  try:
   return(ModelSetting.get(key)=='True')
  except j as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(V())
 @h
 def VT(key,value):
  try:
   logger.debug(key)
   item=K.query(ModelSetting).filter_by(key=key).with_for_update().first()
   if item is not H:
    item.value=value.strip()if value is not H else value
    K.commit()
   else:
    K.add(ModelSetting(key,value.strip()))
  except j as e:
   logger.error('Exception:%s %s',e,key)
   logger.error(V())
 @h
 def to_dict():
  try:
   from framework.util import Util
   arg=Vc(K.query(ModelSetting).all())
      VL=Util.get_list_except_empty
      Vc=Util.db_list_to_dict
   arg['package_name']=package_name
   return arg
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V())
 @h
 def setting_save(req):
  try:
   for key,value in req.form.items():
    if key in['scheduler','is_running']:
     continue
    if key.startswith('tmp_'):
     continue
    logger.debug('Key:%s Value:%s',key,value)
    entity=K.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   K.commit()
   return i 
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V())
   logger.debug('Error Key:%s Value:%s',key,value)
   return C
 @h
 def get_list(key):
  try:
   value=ModelSetting.get(key)
   values=[x.strip().replace(' ','').strip()for x in value.replace('\n','|').split('|')]
   values=VL(values)
   return values
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V())
   logger.error('Error Key:%s Value:%s',key,value)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
