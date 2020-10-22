import os
c=True
w=False
J=repr
W=getattr
M=staticmethod
j=str
H=None
B=Exception
Y=id
p=int
import traceback
import json
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified
from framework import db,app,path_app_root,scheduler
from.plugin import logger,package_name
app.config['SQLALCHEMY_BINDS'][package_name]='sqlite:///%s'%(os.path.join(path_app_root,'data','db','%s.db'%package_name))
class ModelCommand(db.Model):
 __tablename__='%s_job'%package_name
 __table_args__={'mysql_collate':'utf8_general_ci'}
 __bind_key__=package_name
 Y=db.Column(db.Integer,primary_key=c)
 filename=db.Column(db.String) 
 command=db.Column(db.String)
 description=db.Column(db.String)
 schedule_auto_start=db.Column(db.Boolean) 
 schedule_type=db.Column(db.String)
 schedule_info=db.Column(db.String) 
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
  return J(self.as_dict())
 def as_dict(self):
  return{x.name:W(self,x.name)for x in self.__table__.columns}
 @M
 def job_list():
  try:
   db_list=db.session.query(ModelCommand).filter().all()
   db_list=[x.as_dict()for x in db_list]
   from.logic_normal import LogicNormal
   for item in db_list:
    item['is_include']=j(scheduler.is_include('command_%s'%item['id']))
    item['is_running']=j(scheduler.is_running('command_%s'%item['id']))
    item['process_id']=LogicNormal.process_list[item['id']].pid if item['id']in LogicNormal.process_list and LogicNormal.process_list[item['id']]is not H else H
   return db_list
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @M
 def job_new(request):
  try:
   command=request.form['command']
   item=ModelCommand(command)
   db.session.add(item)
   db.session.commit()
   return 'success'
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @M
 def job_save(request):
  try:
   Y=request.form['job_id']
   entity=db.session.query(ModelCommand).filter_by(Y=Y).with_for_update().first()
   entity.set_command(request.form['job_command'])
   entity.description=request.form['job_description'] 
   entity.schedule_type=request.form['job_schedule_type']
   entity.schedule_info=request.form['job_schedule_info']if 'job_schedule_info' in request.form else ''
   entity.schedule_auto_start=(request.form['job_schedule_auto_start']=='True')
   db.session.commit()
   from.logic_normal import LogicNormal
   LogicNormal.scheduler_switch(Y,w)
   return 'success'
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
 @M
 def get_job_by_id(job_id):
  try:
   return db.session.query(ModelCommand).filter_by(Y=p(job_id)).first()
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @M
 def job_remove(request):
  try:
   Y=request.form['job_id']
   entity=db.session.query(ModelCommand).filter_by(Y=Y).first()
   db.session.delete(entity)
   db.session.commit()
   from.logic_normal import LogicNormal
   LogicNormal.scheduler_switch(Y,w)
   return 'success'
  except B as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return 'fail'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
