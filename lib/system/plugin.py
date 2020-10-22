import os
H=None
e=str
j=Exception
i=True
XR=super
C=False
x=classmethod
u=os.path
p=os.listdir
import traceback
V=traceback.format_exc
import logging
import threading
v=threading.Thread
import time
T=time.sleep
import json
t=json.loads
import requests
Y=requests.get
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
VM=request.sid
Vk=request.headers
Vg=request.form
from framework.logger import get_logger
from framework import app,db,scheduler,socketio,check_api,path_app_root,path_data
k=socketio.emit
Vn=socketio.on
VG=socketio.stop
Vt=scheduler.get_job_list_info
Vx=scheduler.is_running
S=scheduler.is_include
from framework.util import Util,SingletonClass
from flask_login import login_user,logout_user,current_user,login_required
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.logic import SystemLogic
Vq=SystemLogic.recent_version
VY=SystemLogic.get_recent_version
VQ=SystemLogic.link_save
Vp=SystemLogic.get_setting_value
Vs=SystemLogic.command_run
VN=SystemLogic.setting_save_after
VE=SystemLogic.setting_save_system
Vm=SystemLogic.get_info
Vu=SystemLogic.point
Vy=SystemLogic.plugin_load
from.model import ModelSetting
VP=ModelSetting.setting_save
VF=ModelSetting.to_dict
from.logic_plugin import LogicPlugin
VS=LogicPlugin.plugin_uninstall
VK=LogicPlugin.plugin_install_by_api
Vd=LogicPlugin.get_plugin_list
from.logic_selenium import SystemLogicSelenium
VU=SystemLogicSelenium.process_ajax
Vb=SystemLogicSelenium.plugin_unload
from.logic_command import SystemLogicCommand
XB=SystemLogicCommand.execute_command_return
XV=SystemLogicCommand.plugin_unload
from.logic_command2 import SystemLogicCommand2
Xc=SystemLogicCommand2.plugin_unload
from.logic_notify import SystemLogicNotify
Xr=SystemLogicNotify.process_ajax
from.logic_telegram_bot import SystemLogicTelegramBot
XA=SystemLogicTelegramBot.process_ajax
Xa=SystemLogicTelegramBot.plugin_load
from.logic_auth import SystemLogicAuth
XD=SystemLogicAuth.process_ajax
Xo=SystemLogicAuth.get_auth_status
from.logic_env import SystemLogicEnv
Xz=SystemLogicEnv.process_ajax
Xw=SystemLogicEnv.load_export
from.logic_site import SystemLogicSite
Xj=SystemLogicSite.process_api
Xh=SystemLogicSite.process_ajax
XI=SystemLogicSite.plugin_load
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'설정'],'sub':[['setting',u'일반설정'],['plugin',u'플러그인'],['information',u'정보'],['log',u'로그']],'sub2':{'setting':[['basic',u'기본'],['auth',u'인증'],['env',u'시스템'],['notify',u'알림'],['telegram_bot',u'텔레그램 봇'],['selenium',u'Selenium'],['trans',u'번역'],['site',u'Site'],['memo',u'메모']],'rss':[['setting',u'설정'],['job',u'작업'],['list',u'목록']],'cache':[['setting',u'설정'],['list',u'목록']]},} 
def plugin_load():
 logger.debug('plugin_load:%s',package_name)
 Vy()
 Xa()
 XI()
def plugin_unload():
 logger.debug('plugin_load:%s',package_name)
 Vb()
 XV()
 Xc()
@blueprint.route('/')
def normal():
 return redirect('/%s/setting'%package_name)
@login_required
def home():
 return render_template('info.html',arg=H)
@blueprint.route('/<sub>',methods=['GET','POST'])
@login_required
def first_menu(sub):
 arg=H
 if sub=='home':
  return render_template('%s_%s.html'%(package_name,sub),arg=H)
 elif sub=='setting':
  return redirect('/%s/%s/basic'%(package_name,sub))
 elif sub=='plugin':
  arg=VF()
  return render_template('system_plugin.html',arg=arg)
 elif sub=='information':
  return render_template('manual.html',sub=sub,arg='system.json')
 elif sub=='log':
  log_files=p(u.join(path_data,'log'))
  log_files.sort()
  log_list=[]
  arg={'package_name':package_name,'sub':sub}
  for x in log_files:
   if x.endswith('.log'):
    log_list.append(x)
  arg['log_list']='|'.join(log_list)
  arg['all_list']='|'.join(log_files)
  arg['filename']=''
  if 'filename' in Vg:
   arg['filename']=Vg['filename']
  logger.debug(arg)
  return render_template('%s_%s.html'%(package_name,sub),arg=arg)
 elif sub=='restart':
  restart()
  return render_template('system_restart.html',sub=sub,referer=Vk.get("Referer"))
 elif sub=='shutdown':
  shutdown()
  return render_template('system_restart.html',sub=sub,referer=Vk.get("Referer"))
 elif sub=='telegram':
  return redirect('/%s/%s/setting'%(package_name,sub))
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/<sub>/<sub2>')
@login_required
def second_menu(sub,sub2):
 try:
  if sub=='setting':
   arg=VF()
   arg['sub']=sub2
   if sub2=='basic':
    arg['point']=Vu
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2 in['trans','selenium','notify']:
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='auth':
    arg['auth_result']=Xo()
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='telegram_bot':
    arg['scheduler']=e(S('%s_%s'%(package_name,sub2)))
    arg['is_running']=e(Vx('%s_%s'%(package_name,sub2)))
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='env':
    arg['export']=Xw()
    if arg['export']is H:
     arg['export']=u'export.sh 파일이 없습니다.'
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='site':
    arg['scheduler']=e(S('%s_%s'%(package_name,sub2)))
    arg['is_running']=e(Vx('%s_%s'%(package_name,sub2)))
    from system.model import ModelSetting as SystemModelSetting
          VP=ModelSetting.setting_save
          VF=ModelSetting.to_dict
    arg['site_get_daum_cookie_url']='{ddns}/{package_name}/api/{sub2}/daum_cookie'.format(ddns=SystemModelSetting.get('ddns'),package_name=package_name,sub2=sub2)
    if SystemModelSetting.get_bool('auth_use_apikey'):
     arg['site_get_daum_cookie_url']+='?apikey={apikey}'.format(apikey=SystemModelSetting.get('auth_apikey'))
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='memo':
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
def restart():
 try:
  try:
   import framework
   framework.exit_code=1
   app_close()
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V())
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
def shutdown():
 try:
  try:
   nginx_kill='/app/data/custom/nginx/files/kill.sh'
   if u.exists(nginx_kill):
    XB([nginx_kill])
  except j as e:
   logger.error('Exception:%s',e)
   logger.error(V()) 
  import framework
  framework.exit_code=0
  app_close()
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
def app_close():
 try:
  from framework.init_plugin import plugin_unload
  plugin_unload()
  VG()
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
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
   return XD(sub2,request)
      XD=SystemLogicAuth.process_ajax
      Xo=SystemLogicAuth.get_auth_status
  elif sub=='selenium':
   return VU(sub2,request)
  elif sub=='notify':
   return Xr(sub2,request)
  elif sub=='telegram_bot':
   return XA(sub2,request)
  elif sub=='env':
   return Xz(sub2,request)
  elif sub=='site':
   return Xh(sub2,request) 
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 try: 
  if sub=='info':
   try:
    ret={}
    ret['system']=Vm()
    ret['scheduler']=Vt()
    return jsonify(ret)
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
    return jsonify()
  elif sub=='setting_save_system':
   try:
    ret=VE(request)
    return jsonify(ret)
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='setting_save':
   ret=VP(request)
   VN()
   return jsonify(ret)
  elif sub=='ddns_test':
   try:
    url=Vg['ddns']+'/version'
    res=Y(url)
    data=res.text
    return jsonify(data)
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
    return jsonify('fail')
  elif sub=='celery_test':
   try:
    try:
     import framework
     framework.exit_code=1
     VG()
    except j as e:
     logger.error('Exception:%s',e)
     logger.error(V())
    return jsonify()
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='command_run':
   try:
    command_text=Vg['command_text']
    ret=Vs(command_text)
    return jsonify(ret)
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='get_link_list':
   try:
    link_json=Vp('link_json')
    j=t(link_json)
    return jsonify(j)
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='link_save':
   try:
    link_data_str=Vg['link_data']
    ret=VQ(link_data_str)
    return jsonify(ret)
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='plugin_list':
   try:
    return jsonify(Vd())
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='plugin_install':
   try:
    plugin_git=Vg['plugin_git']
    return jsonify(VK(plugin_git))
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='plugin_uninstall':
   try:
    plugin_name=Vg['plugin_name']
    return jsonify(VS(plugin_name))
   except j as e:
    logger.error('Exception:%s',e)
    logger.error(V())
  elif sub=='recent_version':
   ret=VY()
   ret={'ret':ret,'version':Vq}
   return jsonify(ret)
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
@Vn('connect',namespace='/%s'%package_name)
def connect():
 try:
  InfoProcess.instance().connect(VM)
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
@Vn('disconnect',namespace='/%s'%package_name)
def disconnect():
 try:
  InfoProcess.instance().disconnect(VM)
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
@Vn('connect',namespace='/system_restart')
def connect_system_restart():
 try:
  k("on_connect",'restart',namespace='/system_restart',broadcast=i)
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
@Vn('disconnect',namespace='/system_restart')
def disconnect_system_restart():
 try:
  pass
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
class InfoThread(v):
 def __init__(self):
  XR(InfoThread,self).__init__()
  self.stop_flag=C
  self.daemon=i
 def stop(self):
  self.stop_flag=i
 def run(self):
  while not self.stop_flag:
   ret={}
   ret['system']=Vm()
   ret['scheduler']=Vt()
   k("status",ret,namespace='/system',broadcast=i)
   T(1)
class InfoProcess(SingletonClass):
 sid_list=[]
 thread=H
 @x
 def connect(cls,sid):
  logger.debug('Info connect:%s',InfoProcess.sid_list)
  if not InfoProcess.sid_list:
   InfoProcess.thread=InfoThread()
   InfoProcess.thread.start()
  InfoProcess.sid_list.append(sid)
 @x
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
   plugin_git=Vg['plugin_git']
   from system.logic_plugin import LogicPlugin
   ret=VK(plugin_git)
      VS=LogicPlugin.plugin_uninstall
      VK=LogicPlugin.plugin_install_by_api
      Vd=LogicPlugin.get_plugin_list
   return jsonify(ret)
  elif sub=='restart':
   logger.debug('web restart')
   import system
   system.restart()
   return jsonify({'ret':'success'})
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
@blueprint.route('/api/<sub>/<sub2>',methods=['GET','POST'])
@check_api
def second_api(sub,sub2):
 try:
  if sub=='trans':
   from.logic_trans import SystemLogicTrans
   return SystemLogicTrans.process_api(sub2,request)
  elif sub=='site':
   from.logic_site import SystemLogicSite
   return Xj(sub2,request)
      Xj=SystemLogicSite.process_api
      Xh=SystemLogicSite.process_ajax
      XI=SystemLogicSite.plugin_load
 except j as e:
  logger.error('Exception:%s',e)
  logger.error(V())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
