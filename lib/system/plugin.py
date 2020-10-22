import os
Q=None
F=str
e=Exception
o=True
Wp=super
j=False
q=classmethod
a=os.path
t=os.listdir
import traceback
H=traceback.format_exc
import logging
import threading
i=threading.Thread
import time
R=time.sleep
import json
C=json.loads
import requests
A=requests.get
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
Hb=request.sid
Hg=request.headers
HE=request.form
from framework.logger import get_logger
from framework import app,db,scheduler,socketio,check_api,path_app_root,path_data
g=socketio.emit
HB=socketio.on
Hs=socketio.stop
HC=scheduler.get_job_list_info
Hq=scheduler.is_running
u=scheduler.is_include
from framework.util import Util,SingletonClass
from flask_login import login_user,logout_user,current_user,login_required
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.logic import SystemLogic
HP=SystemLogic.recent_version
HA=SystemLogic.get_recent_version
Hx=SystemLogic.link_save
Ht=SystemLogic.get_setting_value
Hk=SystemLogic.command_run
HU=SystemLogic.setting_save_after
Hr=SystemLogic.setting_save_system
Hm=SystemLogic.get_info
Ha=SystemLogic.point
HD=SystemLogic.plugin_load
from.model import ModelSetting
Hn=ModelSetting.setting_save
HT=ModelSetting.to_dict
from.logic_plugin import LogicPlugin
Hu=LogicPlugin.plugin_uninstall
Hc=LogicPlugin.plugin_install_by_api
Hy=LogicPlugin.get_plugin_list
from.logic_selenium import SystemLogicSelenium
HK=SystemLogicSelenium.process_ajax
Hv=SystemLogicSelenium.plugin_unload
from.logic_command import SystemLogicCommand
WY=SystemLogicCommand.execute_command_return
WH=SystemLogicCommand.plugin_unload
from.logic_command2 import SystemLogicCommand2
WM=SystemLogicCommand2.plugin_unload
from.logic_notify import SystemLogicNotify
Wz=SystemLogicNotify.process_ajax
from.logic_telegram_bot import SystemLogicTelegramBot
WX=SystemLogicTelegramBot.process_ajax
Wd=SystemLogicTelegramBot.plugin_load
from.logic_auth import SystemLogicAuth
WJ=SystemLogicAuth.process_ajax
WG=SystemLogicAuth.get_auth_status
from.logic_env import SystemLogicEnv
Wh=SystemLogicEnv.process_ajax
WI=SystemLogicEnv.load_export
from.logic_site import SystemLogicSite
We=SystemLogicSite.process_api
WN=SystemLogicSite.process_ajax
WL=SystemLogicSite.plugin_load
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder='templates')
menu={'main':[package_name,u'설정'],'sub':[['setting',u'일반설정'],['plugin',u'플러그인'],['information',u'정보'],['log',u'로그']],'sub2':{'setting':[['basic',u'기본'],['auth',u'인증'],['env',u'시스템'],['notify',u'알림'],['telegram_bot',u'텔레그램 봇'],['selenium',u'Selenium'],['trans',u'번역'],['site',u'Site'],['memo',u'메모']],'rss':[['setting',u'설정'],['job',u'작업'],['list',u'목록']],'cache':[['setting',u'설정'],['list',u'목록']]},} 
def plugin_load():
 logger.debug('plugin_load:%s',package_name)
 HD()
 Wd()
 WL()
def plugin_unload():
 logger.debug('plugin_load:%s',package_name)
 Hv()
 WH()
 WM()
@blueprint.route('/')
def normal():
 return redirect('/%s/setting'%package_name)
@login_required
def home():
 return render_template('info.html',arg=Q)
@blueprint.route('/<sub>',methods=['GET','POST'])
@login_required
def first_menu(sub):
 arg=Q
 if sub=='home':
  return render_template('%s_%s.html'%(package_name,sub),arg=Q)
 elif sub=='setting':
  return redirect('/%s/%s/basic'%(package_name,sub))
 elif sub=='plugin':
  arg=HT()
  return render_template('system_plugin.html',arg=arg)
 elif sub=='information':
  return render_template('manual.html',sub=sub,arg='system.json')
 elif sub=='log':
  log_files=t(a.join(path_data,'log'))
  log_files.sort()
  log_list=[]
  arg={'package_name':package_name,'sub':sub}
  for x in log_files:
   if x.endswith('.log'):
    log_list.append(x)
  arg['log_list']='|'.join(log_list)
  arg['all_list']='|'.join(log_files)
  arg['filename']=''
  if 'filename' in HE:
   arg['filename']=HE['filename']
  logger.debug(arg)
  return render_template('%s_%s.html'%(package_name,sub),arg=arg)
 elif sub=='restart':
  restart()
  return render_template('system_restart.html',sub=sub,referer=Hg.get("Referer"))
 elif sub=='shutdown':
  shutdown()
  return render_template('system_restart.html',sub=sub,referer=Hg.get("Referer"))
 elif sub=='telegram':
  return redirect('/%s/%s/setting'%(package_name,sub))
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
@blueprint.route('/<sub>/<sub2>')
@login_required
def second_menu(sub,sub2):
 try:
  if sub=='setting':
   arg=HT()
   arg['sub']=sub2
   if sub2=='basic':
    arg['point']=Ha
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2 in['trans','selenium','notify']:
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='auth':
    arg['auth_result']=WG()
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='telegram_bot':
    arg['scheduler']=F(u('%s_%s'%(package_name,sub2)))
    arg['is_running']=F(Hq('%s_%s'%(package_name,sub2)))
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='env':
    arg['export']=WI()
    if arg['export']is Q:
     arg['export']=u'export.sh 파일이 없습니다.'
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='site':
    arg['scheduler']=F(u('%s_%s'%(package_name,sub2)))
    arg['is_running']=F(Hq('%s_%s'%(package_name,sub2)))
    from system.model import ModelSetting as SystemModelSetting
          Hn=ModelSetting.setting_save
          HT=ModelSetting.to_dict
    arg['site_get_daum_cookie_url']='{ddns}/{package_name}/api/{sub2}/daum_cookie'.format(ddns=SystemModelSetting.get('ddns'),package_name=package_name,sub2=sub2)
    if SystemModelSetting.get_bool('auth_use_apikey'):
     arg['site_get_daum_cookie_url']+='?apikey={apikey}'.format(apikey=SystemModelSetting.get('auth_apikey'))
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
   elif sub2=='memo':
    return render_template('%s_%s_%s.html'%(package_name,sub,sub2),arg=arg)
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
def restart():
 try:
  try:
   import framework
   framework.exit_code=1
   app_close()
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H())
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
def shutdown():
 try:
  try:
   nginx_kill='/app/data/custom/nginx/files/kill.sh'
   if a.exists(nginx_kill):
    WY([nginx_kill])
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(H()) 
  import framework
  framework.exit_code=0
  app_close()
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
def app_close():
 try:
  from framework.init_plugin import plugin_unload
  plugin_unload()
  Hs()
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
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
   return WJ(sub2,request)
      WJ=SystemLogicAuth.process_ajax
      WG=SystemLogicAuth.get_auth_status
  elif sub=='selenium':
   return HK(sub2,request)
  elif sub=='notify':
   return Wz(sub2,request)
  elif sub=='telegram_bot':
   return WX(sub2,request)
  elif sub=='env':
   return Wh(sub2,request)
  elif sub=='site':
   return WN(sub2,request) 
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 try: 
  if sub=='info':
   try:
    ret={}
    ret['system']=Hm()
    ret['scheduler']=HC()
    return jsonify(ret)
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
    return jsonify()
  elif sub=='setting_save_system':
   try:
    ret=Hr(request)
    return jsonify(ret)
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='setting_save':
   ret=Hn(request)
   HU()
   return jsonify(ret)
  elif sub=='ddns_test':
   try:
    url=HE['ddns']+'/version'
    res=A(url)
    data=res.text
    return jsonify(data)
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
    return jsonify('fail')
  elif sub=='celery_test':
   try:
    try:
     import framework
     framework.exit_code=1
     Hs()
    except e as e:
     logger.error('Exception:%s',e)
     logger.error(H())
    return jsonify()
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='command_run':
   try:
    command_text=HE['command_text']
    ret=Hk(command_text)
    return jsonify(ret)
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='get_link_list':
   try:
    link_json=Ht('link_json')
    j=C(link_json)
    return jsonify(j)
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='link_save':
   try:
    link_data_str=HE['link_data']
    ret=Hx(link_data_str)
    return jsonify(ret)
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='plugin_list':
   try:
    return jsonify(Hy())
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='plugin_install':
   try:
    plugin_git=HE['plugin_git']
    return jsonify(Hc(plugin_git))
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='plugin_uninstall':
   try:
    plugin_name=HE['plugin_name']
    return jsonify(Hu(plugin_name))
   except e as e:
    logger.error('Exception:%s',e)
    logger.error(H())
  elif sub=='recent_version':
   ret=HA()
   ret={'ret':ret,'version':HP}
   return jsonify(ret)
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
@HB('connect',namespace='/%s'%package_name)
def connect():
 try:
  InfoProcess.instance().connect(Hb)
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
@HB('disconnect',namespace='/%s'%package_name)
def disconnect():
 try:
  InfoProcess.instance().disconnect(Hb)
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
@HB('connect',namespace='/system_restart')
def connect_system_restart():
 try:
  g("on_connect",'restart',namespace='/system_restart',broadcast=o)
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
@HB('disconnect',namespace='/system_restart')
def disconnect_system_restart():
 try:
  pass
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
class InfoThread(i):
 def __init__(self):
  Wp(InfoThread,self).__init__()
  self.stop_flag=j
  self.daemon=o
 def stop(self):
  self.stop_flag=o
 def run(self):
  while not self.stop_flag:
   ret={}
   ret['system']=Hm()
   ret['scheduler']=HC()
   g("status",ret,namespace='/system',broadcast=o)
   R(1)
class InfoProcess(SingletonClass):
 sid_list=[]
 thread=Q
 @q
 def connect(cls,sid):
  logger.debug('Info connect:%s',InfoProcess.sid_list)
  if not InfoProcess.sid_list:
   InfoProcess.thread=InfoThread()
   InfoProcess.thread.start()
  InfoProcess.sid_list.append(sid)
 @q
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
   plugin_git=HE['plugin_git']
   from system.logic_plugin import LogicPlugin
   ret=Hc(plugin_git)
      Hu=LogicPlugin.plugin_uninstall
      Hc=LogicPlugin.plugin_install_by_api
      Hy=LogicPlugin.get_plugin_list
   return jsonify(ret)
  elif sub=='restart':
   logger.debug('web restart')
   import system
   system.restart()
   return jsonify({'ret':'success'})
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
@blueprint.route('/api/<sub>/<sub2>',methods=['GET','POST'])
@check_api
def second_api(sub,sub2):
 try:
  if sub=='trans':
   from.logic_trans import SystemLogicTrans
   return SystemLogicTrans.process_api(sub2,request)
  elif sub=='site':
   from.logic_site import SystemLogicSite
   return We(sub2,request)
      We=SystemLogicSite.process_api
      WN=SystemLogicSite.process_ajax
      WL=SystemLogicSite.plugin_load
 except e as e:
  logger.error('Exception:%s',e)
  logger.error(H())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
