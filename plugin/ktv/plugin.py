import traceback
AD=str
i=Exception
P=traceback.format_exc
import logging
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
Aw=request.form
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler
v=scheduler.is_running
Aq=scheduler.is_include
f=db.session
from framework.util import Util
z=Util.db_list_to_dict
from.logic import Logic
AU=Logic.receive_scan_result
AE=Logic.reset_db
AQ=Logic.library_remove
AH=Logic.library_list
AF=Logic.library_save
Ad=Logic.scheduler_stop
AC=Logic.scheduler_start
Ar=Logic.filelist
AL=Logic.setting_save
AO=Logic.plugin_load
from.model import ModelSetting
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'국내TV'],'sub':[['setting',u'설정'],['list',u'목록'],['log',u'로그']]}
def plugin_load():
 AO()
def plugin_unload():
 pass
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 if sub=='setting':
  setting_list=f.query(ModelSetting).all()
  arg=z(setting_list)
  arg['is_include']=AD(Aq('ktv_process'))
  arg['is_running']=AD(v('ktv_process'))
  return render_template('ktv_setting.html',sub=sub,arg=arg)
 elif sub=='list':
  return render_template('ktv_list.html')
 elif sub=='log':
  return render_template('log.html',package=package_name)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 if sub=='setting_save':
  try:
   ret=AL(request)
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
 elif sub=='filelist':
  try:
   ret=Ar(request)
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
 elif sub=='scheduler':
  try:
   go=Aw['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    AC()
   else:
    Ad()
   return jsonify(go)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
   return jsonify('fail')
 elif sub=='library_save':
  try:
   ret={}
   ret['ret']=AF(request)
   ret['library_list']=[item.as_dict()for item in AH()]
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
   return jsonify('fail')
 elif sub=='library_list':
  try:
   ret={}
   ret['library_list']=[item.as_dict()for item in AH()]
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
   return jsonify('fail')
 elif sub=='library_remove':
  try:
   ret={}
   ret['ret']=AQ(request)
   ret['library_list']=[item.as_dict()for item in AH()]
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
   return jsonify('fail')
 elif sub=='reset_db':
  try:
   ret=AE()
   return jsonify(ret)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
   return jsonify('fail')
@blueprint.route('/api/<sub>',methods=['GET','POST'])
def api(sub):
 if sub=='scan_completed':
  try:
   filename=Aw['filename']
   db_id=Aw['id']
   logger.debug('SCAN COMPLETED:%s %s',filename,db_id)
   AU(db_id,filename)
   return 'ok'
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(P())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
