import os
M=True
J=False
k=repr
z=getattr
O=staticmethod
h=str
S=None
i=Exception
H=id
V=int
Y=os.path
import traceback
Q=traceback.format_exc
import json
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified
from framework import db,app,path_app_root,scheduler
v=scheduler.is_running
n=scheduler.is_include
I=app.config
j=db.session
T=db.Boolean
F=db.String
E=db.Integer
R=db.Column
K=db.Model
from.plugin import logger,package_name
s=logger.error
I['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(Y.join(path_app_root,'data','db','%s.db'%package_name))
class ModelCommand(K):
 __tablename__='%s_job'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 H=R(E,primary_key=M)
 filename=R(F) 
 command=R(F)
 description=R(F)
 schedule_auto_start=R(T) 
 schedule_type=R(F)
 schedule_info=R(F) 
 def __init__(self,command):
  self.description=''
  self.schedule_auto_start=J
  self.schedule_type="0"
  self.schedule_info=''
  self.set_command(command)
 def set_command(self,command):
  self.command=command
  tmp=command.split(' ')
  for t in tmp:
   if t.endswith('.py'):
    self.filename=t
    break
   elif t.endswith('.sh'):
    self.filename=t
    break
 def __repr__(self):
  return k(self.as_dict())
 def as_dict(self):
  return{x.name:z(self,x.name)for x in self.__table__.columns}
 @O
 def job_list():
  try:
   db_list=j.query(ModelCommand).filter().all()
   db_list=[x.as_dict()for x in db_list]
   from.logic_normal import LogicNormal
   for item in db_list:
    item['is_include']=h(n('command_%s'%item['id']))
    item['is_running']=h(v('command_%s'%item['id']))
    item['process_id']=LogicNormal.process_list[item['id']].pid if item['id']in LogicNormal.process_list and LogicNormal.process_list[item['id']]is not S else S
   return db_list
  except i as e:
   s('Exception:%s',e)
   s(Q())
 @O
 def job_new(request):
  try:
   command=request.form['command']
   item=ModelCommand(command)
   j.add(item)
   j.commit()
   return 'success'
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return 'fail'
 @O
 def job_save(request):
  try:
   H=request.form['job_id']
   entity=j.query(ModelCommand).filter_by(H=H).with_for_update().first()
   entity.set_command(request.form['job_command'])
   entity.description=request.form['job_description'] 
   entity.schedule_type=request.form['job_schedule_type']
   entity.schedule_info=request.form['job_schedule_info']if 'job_schedule_info' in request.form else ''
   entity.schedule_auto_start=(request.form['job_schedule_auto_start']=='True')
   j.commit()
   from.logic_normal import LogicNormal
   LogicNormal.scheduler_switch(H,J)
   return 'success'
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return 'fail'
 @O
 def get_job_by_id(job_id):
  try:
   return j.query(ModelCommand).filter_by(H=V(job_id)).first()
  except i as e:
   s('Exception:%s',e)
   s(Q())
 @O
 def job_remove(request):
  try:
   H=request.form['job_id']
   entity=j.query(ModelCommand).filter_by(H=H).first()
   j.delete(entity)
   j.commit()
   from.logic_normal import LogicNormal
   LogicNormal.scheduler_switch(H,J)
   return 'success'
  except i as e:
   s('Exception:%s',e)
   s(Q())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
