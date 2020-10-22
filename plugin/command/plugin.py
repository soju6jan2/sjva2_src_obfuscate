import os
i=Exception
M=True
V=int
J=False
h=str
a=os.remove
Y=os.path
import traceback
Q=traceback.format_exc
import time
from datetime import datetime
import urllib
import requests
m=requests.get
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory
G=request.form
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,check_api
f=socketio.on
from framework.util import Util
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.logic_normal import LogicNormal
Yb=LogicNormal.send_queue_start
Yt=LogicNormal.save
YQ=LogicNormal.send_process_command
YC=LogicNormal.process_list
Yx=LogicNormal.process_close
YN=LogicNormal.job_background
B=LogicNormal.scheduler_switch0
X=LogicNormal.foreground_command_close
y=LogicNormal.foreground_command
D=LogicNormal.command_file_list
W=LogicNormal.plugin_unload
P=LogicNormal.plugin_load
from.model import ModelCommand
q=ModelCommand.get_job_by_id
YU=ModelCommand.job_remove
YA=ModelCommand.job_save
Ye=ModelCommand.job_list
Yw=ModelCommand.job_new
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder=Y.join(Y.dirname(__file__),'templates'))
menu={'main':[package_name,u'Command'],'sub':[['setting',u'작업설정'],['log',u'로그']],}
plugin_info={'version':'1.0','name':'command','category_name':'system','developer':'soju6jan','description':'Command','home':'https://github.com/soju6jan/command','more':'',}
def plugin_load():
 P()
def plugin_unload():
 W()
@blueprint.route('/')
def home():
 return redirect('/%s/setting'%package_name)
@blueprint.route('/<sub>',methods=['GET','POST'])
@login_required
def first_menu(sub):
 try:
  if sub=='setting':
   arg={}
   arg['command_file_list']=D()
   arg['package_name']=package_name
   arg['command_by_plugin']=''
   if 'command_by_plugin' in G:
    arg['command_by_plugin']=G['command_by_plugin']
   return render_template('%s_setting.html'%package_name,arg=arg)
  elif sub=='log':
   return render_template('log.html',package=package_name)
  return render_template('sample.html',title='%s - %s'%(package_name,sub))
 except i as e:
  logger.error('Exception:%s',e)
  logger.error(Q()) 
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 try:
  if sub=='foreground_command':
   command=G['command']
   ret=y(command)
   return jsonify(ret)
  elif sub=='foreground_command_close':
   ret=X()
   return jsonify(ret)
  elif sub=='job_new':
   ret={}
   ret['ret']=Yw(request)
   ret['list']=Ye()
   return jsonify(ret)
  elif sub=='job_save':
   ret={}
   ret['ret']=YA(request)
   ret['list']=Ye()
   return jsonify(ret)
  elif sub=='scheduler_switch':
   ret={}
   ret['ret']=B(request)
   ret['list']=Ye()
   return jsonify(ret)
  elif sub=='job_remove':
   ret={}
   ret['ret']=YU(request)
   ret['list']=Ye()
   return jsonify(ret)
  elif sub=='job_log_show':
   ret={}
   job_id=G['job_id']
   ret['filename']='%s_%s.log'%(package_name,job_id)
   ret['ret']=Y.exists(Y.join(path_data,'log',ret['filename']))
   return jsonify(ret)
  elif sub=='job_background':
   ret={}
   job_id=G['job_id']
   ret['ret']=YN(job_id)
   return jsonify(ret)
  elif sub=='job_file_edit':
   ret={}
   job_id=G['job_id']
   job=q(job_id)
   import framework.common.util as CommonUtil
   ret['data']=CommonUtil.read_file(job.filename)
   ret['ret']=M
   return jsonify(ret)
  elif sub=='file_save':
   ret={}
   job_id=G['file_job_id']
   logger.debug(job_id)
   data=G['file_textarea']
   job=q(job_id)
   import framework.common.util as CommonUtil
   logger.debug(job.filename)
   CommonUtil.write_file(data,job.filename)
   ret['ret']=M
   return jsonify(ret)
  elif sub=='foreground_command_by_job':
   ret={}
   job_id=G['job_id']
   job=q(job_id)
   ret['ret']=y(job.command,job_id=job_id)
   return jsonify(ret)
  elif sub=='process_close':
   ret={'ret':'fail'}
   job_id=G['job_id']
   if Yx(YC[V(job_id)]):
    ret['ret']='success'
   return jsonify(ret)
  elif sub=='send_process_command':
   ret=YQ(request)
   return jsonify(ret)
  elif sub=='command_list':
   ret={}
   ret['list']=Ye()
   return jsonify(ret)
  elif sub=='save':
   ret={}
   ret['ret']=Yt(request)
   ret['list']=Ye()
   return jsonify(ret)
 except i as e:
  logger.error('Exception:%s',e)
  logger.error(Q())
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
   filename=G['filename']
   file_url=G['file_url']
   logger.debug(filename)
   logger.debug(file_url)
   r=m(file_url)
   download_path=Y.join(path_data,'command',filename)
   update=J
   if Y.exists(download_path):
    a(download_path)
    update=M
   import framework.common.util as CommonUtil
   CommonUtil.write_file(r.text,download_path)
   ret['ret']='success'
   if update:
    ret['log']=u'정상적으로 설치하였습니다.<br>파일을 업데이트 하였습니다.'
   else:
    ret['log']=u'정상적으로 설치하였습니다.'
 except i as e:
  logger.error('Exception:%s',e)
  logger.error(Q()) 
  ret['ret']='exception'
  ret['log']=h(e)
 return jsonify(ret)
@f('connect',namespace='/%s'%package_name)
def connect():
 try:
  logger.debug('socket_connect')
  Yb()
 except i as e:
  logger.error('Exception:%s',e)
  logger.error(Q())
@f('disconnect',namespace='/%s'%package_name)
def disconnect():
 try:
  logger.debug('socket_disconnect')
 except i as e:
  logger.error('Exception:%s',e)
  logger.error(Q())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
