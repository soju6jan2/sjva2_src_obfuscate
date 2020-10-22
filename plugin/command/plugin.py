import os
a=Exception
P=True
Y=int
w=False
G=str
M=os.remove
f=os.path
import traceback
y=traceback.format_exc
import time
from datetime import datetime
import urllib
import requests
q=requests.get
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory
t=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,check_api
i=socketio.on
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.logic_normal import LogicNormal
fv=LogicNormal.send_queue_start
fn=LogicNormal.save
fy=LogicNormal.send_process_command
fW=LogicNormal.process_list
fo=LogicNormal.process_close
fs=LogicNormal.job_background
V=LogicNormal.scheduler_switch0
x=LogicNormal.foreground_command_close
U=LogicNormal.foreground_command
e=LogicNormal.command_file_list
b=LogicNormal.plugin_unload
d=LogicNormal.plugin_load
from.model import ModelCommand
T=ModelCommand.get_job_by_id
fk=ModelCommand.job_remove
fO=ModelCommand.job_save
fI=ModelCommand.job_list
fA=ModelCommand.job_new
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder=f.join(f.dirname(__file__),'templates'))
menu={'main':[package_name,u'Command'],'sub':[['setting',u'작업설정'],['log',u'로그']],}
plugin_info={'version':'1.0','name':'command','category_name':'system','developer':'soju6jan','description':'Command','home':'https://github.com/soju6jan/command','more':'',}
def plugin_load():
 d()
def plugin_unload():
 b()
@blueprint.route('/')
def home():
 return redirect('/%s/setting'%package_name)
@blueprint.route('/<sub>',methods=['GET','POST'])
@login_required
def first_menu(sub):
 try:
  if sub=='setting':
   arg={}
   arg['command_file_list']=e()
   arg['package_name']=package_name
   arg['command_by_plugin']=''
   if 'command_by_plugin' in t:
    arg['command_by_plugin']=t['command_by_plugin']
   return render_template('%s_setting.html'%package_name,arg=arg)
  elif sub=='log':
   return render_template('log.html',package=package_name)
  return render_template('sample.html',title='%s - %s'%(package_name,sub))
 except a as e:
  logger.error('Exception:%s',e)
  logger.error(y()) 
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 try:
  if sub=='foreground_command':
   command=t['command']
   ret=U(command)
   return jsonify(ret)
  elif sub=='foreground_command_close':
   ret=x()
   return jsonify(ret)
  elif sub=='job_new':
   ret={}
   ret['ret']=fA(request)
   ret['list']=fI()
   return jsonify(ret)
  elif sub=='job_save':
   ret={}
   ret['ret']=fO(request)
   ret['list']=fI()
   return jsonify(ret)
  elif sub=='scheduler_switch':
   ret={}
   ret['ret']=V(request)
   ret['list']=fI()
   return jsonify(ret)
  elif sub=='job_remove':
   ret={}
   ret['ret']=fk(request)
   ret['list']=fI()
   return jsonify(ret)
  elif sub=='job_log_show':
   ret={}
   job_id=t['job_id']
   ret['filename']='%s_%s.log'%(package_name,job_id)
   ret['ret']=f.exists(f.join(path_data,'log',ret['filename']))
   return jsonify(ret)
  elif sub=='job_background':
   ret={}
   job_id=t['job_id']
   ret['ret']=fs(job_id)
   return jsonify(ret)
  elif sub=='job_file_edit':
   ret={}
   job_id=t['job_id']
   job=T(job_id)
   import framework.common.util as CommonUtil
   ret['data']=CommonUtil.read_file(job.filename)
   ret['ret']=P
   return jsonify(ret)
  elif sub=='file_save':
   ret={}
   job_id=t['file_job_id']
   logger.debug(job_id)
   data=t['file_textarea']
   job=T(job_id)
   import framework.common.util as CommonUtil
   logger.debug(job.filename)
   CommonUtil.write_file(data,job.filename)
   ret['ret']=P
   return jsonify(ret)
  elif sub=='foreground_command_by_job':
   ret={}
   job_id=t['job_id']
   job=T(job_id)
   ret['ret']=U(job.command,job_id=job_id)
   return jsonify(ret)
  elif sub=='process_close':
   ret={'ret':'fail'}
   job_id=t['job_id']
   if fo(fW[Y(job_id)]):
    ret['ret']='success'
   return jsonify(ret)
  elif sub=='send_process_command':
   ret=fy(request)
   return jsonify(ret)
  elif sub=='command_list':
   ret={}
   ret['list']=fI()
   return jsonify(ret)
  elif sub=='save':
   ret={}
   ret['ret']=fn(request)
   ret['list']=fI()
   return jsonify(ret)
 except a as e:
  logger.error('Exception:%s',e)
  logger.error(y())
"""
@blueprint.route('/api/<sub>', methods=['POST'])
def api(sub):
    logger.debug('API %s %s', package_name, sub)
    try:
        if sub == 'command':
            arg = {}
            command = request.form['command']
            arg['command_file_list'] = LogicNormal.command_file_list()
            arg['api_command'] = command
            return render_template('%s_setting.html' % package_name, arg=arg, mode="api")
        elif sub == 'command_return':
            command = request.form['command']
            logger.debug('command_return :%s', command)
            return jsonify(LogicNormal.execute_thread_function(command))
    except Exception as e: 
        logger.error('Exception:%s', e)
        logger.error(traceback.format_exc())
"""
@blueprint.route('/api/<sub>',methods=['GET','POST'])
@check_api
def api(sub):
 ret={}
 try:
  if sub=='command_add':
   filename=t['filename']
   file_url=t['file_url']
   logger.debug(filename)
   logger.debug(file_url)
   r=q(file_url)
   download_path=f.join(path_data,'command',filename)
   update=w
   if f.exists(download_path):
    M(download_path)
    update=P
   import framework.common.util as CommonUtil
   CommonUtil.write_file(r.text,download_path)
   ret['ret']='success'
   if update:
    ret['log']=u'정상적으로 설치하였습니다.<br>파일을 업데이트 하였습니다.'
   else:
    ret['log']=u'정상적으로 설치하였습니다.'
 except a as e:
  logger.error('Exception:%s',e)
  logger.error(y()) 
  ret['ret']='exception'
  ret['log']=G(e)
 return jsonify(ret)
@i('connect',namespace='/%s'%package_name)
def connect():
 try:
  logger.debug('socket_connect')
  fv()
 except a as e:
  logger.error('Exception:%s',e)
  logger.error(y())
@i('disconnect',namespace='/%s'%package_name)
def disconnect():
 try:
  logger.debug('socket_disconnect')
 except a as e:
  logger.error('Exception:%s',e)
  logger.error(y())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
