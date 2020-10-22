import os
R=None
A=str
V=Exception
m=True
U=super
w=False
I=classmethod
import traceback
import logging
import threading
import time
import json
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import app,db,scheduler,socketio,check_api,path_app_root,path_data
from framework.util import Util,SingletonClass
from flask_login import login_user,logout_user,current_user,login_required
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.logic import SystemLogic
from.model import ModelSetting
from.logic_plugin import LogicPlugin
from.logic_selenium import SystemLogicSelenium
from.logic_command import SystemLogicCommand
from.logic_command2 import SystemLogicCommand2
from.logic_notify import SystemLogicNotify
from.logic_telegram_bot import SystemLogicTelegramBot
from.logic_auth import SystemLogicAuth
from.logic_env import SystemLogicEnv
from.logic_site import SystemLogicSite
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'설정'],'sub':[['setting',u'일반설정'],['plugin',u'플러그인'],['information',u'정보'],['log',u'로그']],'sub2':{'setting':[['basic',u'기본'],['auth',u'인증'],['env',u'시스템'],['notify',u'알림'],['telegram_bot',u'텔레그램 봇'],['selenium',u'Selenium'],['trans',u'번역'],['site',u'Site'],['memo',u'메모']],'rss':[['setting',u'설정'],['job',u'작업'],['list',u'목록']],'cache':[['setting',u'설정'],['list',u'목록']]},} 
def plugin_load():
 logger.debug('plugin_load:%s',package_name)
 SystemLogic.plugin_load()
 SystemLogicTelegramBot.plugin_load()
 SystemLogicSite.plugin_load()
def plugin_unload():
 logger.debug('plugin_load:%s',package_name)
 SystemLogicSelenium.plugin_unload()
 SystemLogicCommand.plugin_unload()
 SystemLogicCommand2.plugin_unload()
@blueprint.route('/')
def normal():
 return redirect('/%s/setting'%package_name)
@login_required
def home():
 return render_template('info.html',arg=R)
@blueprint.route('/<sub>',methods=['GET','POST'])
@login_required
def first_menu(sub):
 arg=R
 if sub=='home':
  return render_template('%s_%s.html'%(package_name,sub),arg=R)
 elif sub=='setting':
  return redirect('/%s/%s/basic'%(package_name,sub))
 elif sub=='plugin':
  arg=ModelSetting.to_dict()
  return render_template('system_plugin.html',arg=arg)
 elif sub=='information':
  return render_template('manual.html',sub=sub,arg='system.json')
 elif sub=='log':
  log_files=os.listdir(os.path.join(path_data,'log'))
  log_files.sort()
  log_list=[]
  arg={'package_name':package_name,'sub':sub}
  for x in log_files:
   if x.endswith('.log'):
    log_list.append(x)
  arg['log_list']='|'.join(log_list)
  arg['all_list']='|'.join(log_files)
  arg['filename']=''
  if 'filename' in request.form:
   arg['filename']=request.form['filename']
  logger.debug(arg)
  return render_template('%s_%s.html'%(package_name,sub),arg=arg)
 elif sub=='restart':
  restart()
  return render_template('system_restart.html',sub=sub,referer=request.headers.get("Referer"))
 elif sub=='shutdown':
  shutdown()
  return render_template('system_restart.html',sub=sub,referer=request.headers.get("Referer"))
 elif sub=='telegram':
  return redirect('/%s/%s/setting'%(package_name,sub))
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/<sub>/<sub2>')
@login_required
def second_menu(sub,sub2):
 try:
  if sub=='setting':
   arg=ModelSetting.to_dict()
   arg['sub']=sub2
   if sub2=='basic':
    arg['point']=SystemLogic.point
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2 in['trans','selenium','notify']:
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='auth':
    arg['auth_result']=SystemLogicAuth.get_auth_status()
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='telegram_bot':
    arg['scheduler']=A(scheduler.is_include('%s_%s'%(package_name,sub2)))
    arg['is_running']=A(scheduler.is_running('%s_%s'%(package_name,sub2)))
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='env':
    arg['export']=SystemLogicEnv.load_export()
    if arg['export']is R:
     arg['export']=u'export.sh 파일이 없습니다.'
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='site':
    arg['scheduler']=A(scheduler.is_include('%s_%s'%(package_name,sub2)))
    arg['is_running']=A(scheduler.is_running('%s_%s'%(package_name,sub2)))
    from system.model import ModelSetting as SystemModelSetting
    arg['site_get_daum_cookie_url']='{ddns}/{package_name}/api/{sub2}/daum_cookie'.format(ddns=SystemModelSetting.get('ddns'),package_name=package_name,sub2=sub2)
    if SystemModelSetting.get_bool('auth_use_apikey'):
     arg['site_get_daum_cookie_url']+='?apikey={apikey}'.format(apikey=SystemModelSetting.get('auth_apikey'))
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='memo':
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def restart():
 try:
  try:
   import framework
   framework.exit_code=1
   app_close()
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def shutdown():
 try:
  try:
   nginx_kill='/app/data/custom/nginx/files/kill.sh'
   if os.path.exists(nginx_kill):
    SystemLogicCommand.execute_command_return([nginx_kill])
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  import framework
  framework.exit_code=0
  app_close()
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
def app_close():
 try:
  from framework.init_plugin import plugin_unload
  plugin_unload()
  socketio.stop()
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@blueprint.route('/ajax/<sub>/<sub2>',methods=['GET','POST'])
@login_required
def second_ajax(sub,sub2):
 logger.debug('System AJAX sub:%s',sub)
 try: 
  if sub=='trans':
   from.logic_trans import SystemLogicTrans
   return SystemLogicTrans.process_ajax(sub2,request)
  elif sub=='auth':
   from.logic_auth import SystemLogicAuth
   return SystemLogicAuth.process_ajax(sub2,request)
  elif sub=='selenium':
   return SystemLogicSelenium.process_ajax(sub2,request)
  elif sub=='notify':
   return SystemLogicNotify.process_ajax(sub2,request)
  elif sub=='telegram_bot':
   return SystemLogicTelegramBot.process_ajax(sub2,request)
  elif sub=='env':
   return SystemLogicEnv.process_ajax(sub2,request)
  elif sub=='site':
   return SystemLogicSite.process_ajax(sub2,request) 
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 try: 
  if sub=='info':
   try:
    ret={}
    ret['system']=SystemLogic.get_info()
    ret['scheduler']=scheduler.get_job_list_info()
    return jsonify(ret)
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
    return jsonify()
  elif sub=='setting_save_system':
   try:
    ret=SystemLogic.setting_save_system(request)
    return jsonify(ret)
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='setting_save':
   ret=ModelSetting.setting_save(request)
   SystemLogic.setting_save_after()
   return jsonify(ret)
  elif sub=='ddns_test':
   try:
    url=request.form['ddns']+'/version'
    res=requests.get(url)
    data=res.text
    return jsonify(data)
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
    return jsonify('fail')
  elif sub=='celery_test':
   try:
    try:
     import framework
     framework.exit_code=1
     socketio.stop()
    except V as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc())
    return jsonify()
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='command_run':
   try:
    command_text=request.form['command_text']
    ret=SystemLogic.command_run(command_text)
    return jsonify(ret)
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='get_link_list':
   try:
    link_json=SystemLogic.get_setting_value('link_json')
    j=json.loads(link_json)
    return jsonify(j)
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='link_save':
   try:
    link_data_str=request.form['link_data']
    ret=SystemLogic.link_save(link_data_str)
    return jsonify(ret)
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='plugin_list':
   try:
    return jsonify(LogicPlugin.get_plugin_list())
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='plugin_install':
   try:
    plugin_git=request.form['plugin_git']
    return jsonify(LogicPlugin.plugin_install_by_api(plugin_git))
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='plugin_uninstall':
   try:
    plugin_name=request.form['plugin_name']
    return jsonify(LogicPlugin.plugin_uninstall(plugin_name))
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
  elif sub=='recent_version':
   ret=SystemLogic.get_recent_version()
   ret={'ret':ret,'version':SystemLogic.recent_version}
   return jsonify(ret)
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@socketio.on('connect',namespace='/%s'%package_name)
def connect():
 try:
  InfoProcess.instance().connect(request.sid)
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@socketio.on('disconnect',namespace='/%s'%package_name)
def disconnect():
 try:
  InfoProcess.instance().disconnect(request.sid)
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@socketio.on('connect',namespace='/system_restart')
def connect_system_restart():
 try:
  socketio.emit("on_connect",'restart',namespace='/system_restart',broadcast=m)
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@socketio.on('disconnect',namespace='/system_restart')
def disconnect_system_restart():
 try:
  pass
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
class InfoThread(threading.Thread):
 def __init__(self):
  U(InfoThread,self).__init__()
  self.stop_flag=w
  self.daemon=m
 def stop(self):
  self.stop_flag=m
 def run(self):
  while not self.stop_flag:
   ret={}
   ret['system']=SystemLogic.get_info()
   ret['scheduler']=scheduler.get_job_list_info()
   socketio.emit("status",ret,namespace='/system',broadcast=m)
   time.sleep(1)
class InfoProcess(SingletonClass):
 sid_list=[]
 thread=R
 @I
 def connect(cls,sid):
  logger.debug('Info connect:%s',InfoProcess.sid_list)
  if not InfoProcess.sid_list:
   InfoProcess.thread=InfoThread()
   InfoProcess.thread.start()
  InfoProcess.sid_list.append(sid)
 @I
 def disconnect(cls,sid):
  logger.debug('Info disconnect:%s',InfoProcess.sid_list)
  InfoProcess.sid_list.remove(sid)
  if not InfoProcess.sid_list:
   InfoProcess.thread.stop()
@blueprint.route('/api/<sub>',methods=['GET','POST'])
@check_api
def first_api(sub):
 try:
  if sub=='plugin_add':
   plugin_git=request.form['plugin_git']
   from system.logic_plugin import LogicPlugin
   ret=LogicPlugin.plugin_install_by_api(plugin_git)
   return jsonify(ret)
  elif sub=='restart':
   logger.debug('web restart')
   import system
   system.restart()
   return jsonify({'ret':'success'})
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
@blueprint.route('/api/<sub>/<sub2>',methods=['GET','POST'])
@check_api
def second_api(sub,sub2):
 try:
  if sub=='trans':
   from.logic_trans import SystemLogicTrans
   return SystemLogicTrans.process_api(sub2,request)
  elif sub=='site':
   from.logic_site import SystemLogicSite
   return SystemLogicSite.process_api(sub2,request)
 except V as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
