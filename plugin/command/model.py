import os
P=True
w=False
B=repr
S=getattr
r=staticmethod
G=str
L=None
a=Exception
H=id
Y=int
f=os.path
import traceback
y=traceback.format_exc
import json
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified
from framework import db,app,path_app_root,scheduler
z=scheduler.is_running
D=scheduler.is_include
p=app.config
l=db.session
h=db.Boolean
R=db.String
Q=db.Integer
E=db.Column
j=db.Model
from.plugin import logger,package_name
u=logger.error
p['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(f.join(path_app_root,'data','db','%s.db'%package_name))
class ModelCommand(j):
 __tablename__='%s_job'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 H=E(Q,primary_key=P)
 filename=E(R) 
 command=E(R)
 description=E(R)
 schedule_auto_start=E(h) 
 schedule_type=E(R)
 schedule_info=E(R) 
 def __init__(self,command):
  self.description=''
  self.schedule_auto_start=w
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
  return B(self.as_dict())
 def as_dict(self):
  return{x.name:S(self,x.name)for x in self.__table__.columns}
 @r
 def job_list():
  try:
   db_list=l.query(ModelCommand).filter().all()
   db_list=[x.as_dict()for x in db_list]
   from.logic_normal import LogicNormal
   for item in db_list:
    item['is_include']=G(D('command_%s'%item['id']))
    item['is_running']=G(z('command_%s'%item['id']))
    item['process_id']=LogicNormal.process_list[item['id']].pid if item['id']in LogicNormal.process_list and LogicNormal.process_list[item['id']]is not L else L
   return db_list
  except a as e:
   u('Exception:%s',e)
   u(y())
 @r
 def job_new(request):
  try:
   command=request.form['command']
   item=ModelCommand(command)
   l.add(item)
   l.commit()
   return 'success'
  except a as e:
   u('Exception:%s',e)
   u(y())
   return 'fail'
 @r
 def job_save(request):
  try:
   H=request.form['job_id']
   entity=l.query(ModelCommand).filter_by(H=H).with_for_update().first()
   entity.set_command(request.form['job_command'])
   entity.description=request.form['job_description'] 
   entity.schedule_type=request.form['job_schedule_type']
   entity.schedule_info=request.form['job_schedule_info']if 'job_schedule_info' in request.form else ''
   entity.schedule_auto_start=(request.form['job_schedule_auto_start']=='True')
   l.commit()
   from.logic_normal import LogicNormal
   LogicNormal.scheduler_switch(H,w)
   return 'success'
  except a as e:
   u('Exception:%s',e)
   u(y())
   return 'fail'
 @r
 def get_job_by_id(job_id):
  try:
   return l.query(ModelCommand).filter_by(H=Y(job_id)).first()
  except a as e:
   u('Exception:%s',e)
   u(y())
 @r
 def job_remove(request):
  try:
   H=request.form['job_id']
   entity=l.query(ModelCommand).filter_by(H=H).first()
   l.delete(entity)
   l.commit()
   from.logic_normal import LogicNormal
   LogicNormal.scheduler_switch(H,w)
   return 'success'
  except a as e:
   u('Exception:%s',e)
   u(y())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
