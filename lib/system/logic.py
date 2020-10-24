import os
K=object
S=None
h=staticmethod
r=Exception
R=False
l=True
I=range
g=str
X=int
y=len
import traceback
import logging
from datetime import datetime
import string
import random
import json
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger,set_level
from framework import app,db,scheduler,version,path_app_root,path_data,USERS
from framework.util import Util
from framework import USERS
from framework.user import User
from framework import db,scheduler
from framework.job import Job
from.model import ModelSetting 
import system
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class SystemLogic(K):
 point=0
 db_default={'db_version':'1','port':'9999','ddns':'http://localhost:9999','url_filebrowser':'http://localhost:9998','id':'sjva','pw':'sjva','system_start_time':'','repeat':'','auto_restart_hour':'12','theme':'Default','log_level':'10','use_login':'False','link_json':'[]','plugin_dev_path':'','plugin_tving_level2':'False','web_title':'SJ Video Assistant','my_ip':'','wavve_guid':'','videoportal_adult':'False','trans_type':'0','trans_google_api_key':'','trans_papago_key':'','auth_use_apikey':'False','auth_apikey':'','selenium_remote_url':'','selenium_remote_default_option':'--no-sandbox\n--disable-gpu','selenium_binary_default_option':'','notify_telegram_use':'False','notify_telegram_token':'','notify_telegram_chat_id':'','notify_telegram_disable_notification':'False','notify_discord_use':'False','notify_discord_webhook':'','notify_advaned_use':'False','notify_advaned_policy':u"# 각 플러그인 설정 설명에 명시되어 있는 ID = 형식\n# DEFAULT 부터 주석(#) 제거 후 작성\n\n# DEFAULT = ",'telegram_bot_token':'','telegram_bot_auto_start':'False','telegram_resend':'False','telegram_resend_chat_id':'','sjva_me_user_id':'','auth_status':'','sjva_id':'','site_daum_interval':'0 4 */3 * *','site_daum_auto_start':'False','site_daum_cookie':'TIARA=gaXEIPluo-wWAFlwZN6l8gN3yzhkoo_piP.Kymhuy.6QBt4Q6.cRtxbKDaWpWajcyteRHzrlTVpJRxLjwLoMvyYLVi_7xJ1L','site_daum_test':u'나쁜 녀석들','site_wavve_id':'','site_wavve_pw':'','site_wavve_credential':'','memo':'',}
 db_default2={'use_category_vod':'True','use_category_file_process':'True','use_category_plex':'True','use_category_tool':'True'}
 db_default3={'use_plugin_ffmpeg':'False','use_plugin_ktv':'False','use_plugin_fileprocess_movie':'False','use_plugin_plex':'False','use_plugin_gdrive_scan':'False','use_plugin_rclone':'False','use_plugin_daum_tv':'False'}
 recent_version=S
 @h
 def plugin_load():
  try:
   SystemLogic.db_init()
   SystemLogic.init()
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @h
 def db_init():
  try:
   logger.debug('setting count : %s',db.session.query(ModelSetting).filter_by().count())
   is_first=R
   for key,value in SystemLogic.db_default.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     if key=='port':
      is_first=l
     if key=='sjva_id' or key=='auth_apikey':
      value=''.join(random.choice(string.ascii_uppercase+string.digits)for _ in I(10))
     db.session.add(ModelSetting(key,value))
     db.session.commit()
   for key,value in SystemLogic.db_default2.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     tmp=value
     if is_first==R:
      tmp='True'
     db.session.add(ModelSetting(key,tmp))
     db.session.commit()
   for key,value in SystemLogic.db_default3.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     tmp=value
     if is_first==R:
      tmp='True'
     db.session.add(ModelSetting(key,tmp))
     db.session.commit()
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @h
 def init():
  try:
   if app.config['config']['repeat']==0 or SystemLogic.get_setting_value('system_start_time')=='':
    item=db.session.query(ModelSetting).filter_by(key='system_start_time').with_for_update().first()
    item.value=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()
   item=db.session.query(ModelSetting).filter_by(key='repeat').with_for_update().first()
   item.value=g(app.config['config']['repeat'])
   db.session.commit()
   username=db.session.query(ModelSetting).filter_by(key='id').first().value
   passwd=db.session.query(ModelSetting).filter_by(key='pw').first().value
   USERS[username]=User(username,passwd_hash=passwd)
   SystemLogic.set_restart_scheduler()
   SystemLogic.set_scheduler_check_scheduler()
   SystemLogic.get_recent_version()
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @h
 def get_recent_version():
  try:
   import requests
   url='https://sjva-server.soju6jan.com/version'
   if ModelSetting.get('ddns')=='https://sjva-server.soju6jan.com':
    url='https://sjva-dev.soju6jan.com/version'
   SystemLogic.recent_version=requests.get(url).text
   return l
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return R
 @h
 def restart():
  import system
  system.restart()
 @h
 def get_info():
  info={}
  import platform
  info['platform']=platform.platform()
  info['processor']=platform.processor()
  import sys
  info['python_version']=sys.version
  info['version']=version
  info['recent_version']=SystemLogic.recent_version
  info['path_app_root']=path_app_root
  info['running_type']=u'%s.  비동기 작업 : %s'%(app.config['config']['running_type'],u"사용" if app.config['config']['use_celery']else "미사용")
  import system
  info['auth']=app.config['config']['auth_desc']
  try:
   import psutil
   from framework.util import Util
   info['cpu_percent']='%s %%'%psutil.cpu_percent()
   tmp=psutil.virtual_memory()
   info['memory']=u'전체 : %s   사용량 : %s   남은량 : %s  (%s%%)'%(Util.sizeof_fmt(tmp[0],suffix='B'),Util.sizeof_fmt(tmp[3],suffix='B'),Util.sizeof_fmt(tmp[1],suffix='B'),tmp[2])
  except:
   info['cpu_percent']='not supported'
   info['memory']='not supported'
  try:
   import platform
   if platform.system()=='Windows':
    s=os.path.splitdrive(path_app_root)
    root=s[0]
   else:
    root='/'
   tmp=psutil.disk_usage('/')
   info['disk']=u'전체 : %s   사용량 : %s   남은량 : %s  (%s%%) - 드라이브 (%s)'%(Util.sizeof_fmt(tmp[0],suffix='B'),Util.sizeof_fmt(tmp[1],suffix='B'),Util.sizeof_fmt(tmp[2],suffix='B'),tmp[3],root)
  except r as exception:
   info['disk']='not supported'
  try:
   tmp=SystemLogic.get_setting_value('system_start_time')
   tmp_datetime=datetime.strptime(tmp,'%Y-%m-%d %H:%M:%S')
   timedelta=datetime.now()-tmp_datetime
   info['time']=u'시작 : %s   경과 : %s   재시작 : %s'%(tmp,g(timedelta).split('.')[0],app.config['config']['repeat'])
  except r as exception:
   info['time']=g(exception)
  return info
 @h
 def setting_save_system(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   db.session.commit()
   lists=ModelSetting.query.all()
   SystemLogic.setting_list=Util.db_list_to_dict(lists)
   USERS[db.session.query(ModelSetting).filter_by(key='id').first().value]=User(db.session.query(ModelSetting).filter_by(key='id').first().value,passwd_hash=db.session.query(ModelSetting).filter_by(key='pw').first().value)
   SystemLogic.set_restart_scheduler()
   set_level(X(db.session.query(ModelSetting).filter_by(key='log_level').first().value))
   return l 
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return R
 @h
 def setting_save_after():
  try:
   USERS[ModelSetting.get('id')]=User(ModelSetting.get('id'),passwd_hash=ModelSetting.get('pw'))
   SystemLogic.set_restart_scheduler()
   set_level(X(db.session.query(ModelSetting).filter_by(key='log_level').first().value))
   from.logic_site import SystemLogicSite
   SystemLogicSite.get_daum_cookies(force=l)
   return l 
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return R
 @h
 def change_theme(theme):
  try:
   source=os.path.join(path_app_root,'static','css','theme','%s_bootstrap.min.css'%theme)
   target=os.path.join(path_app_root,'static','css','bootstrap.min.css')
   os.remove(target)
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return R
 @h
 def get_setting_value(key):
  try:
   entity=db.session.query(ModelSetting).filter_by(key=key).first()
   if entity is S:
    return S
   else:
    return entity.value
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.error('error key : %s',key)
   return R
 @h
 def set_restart_scheduler():
  name='%s_restart'%(package_name)
  if scheduler.is_include(name):
   scheduler.remove_job(name)
  interval=ModelSetting.get('auto_restart_hour')
  if interval!='0':
   if y(interval.split(' '))==1:
    interval='%s'%(X(interval)*60)
   job_instance=Job(package_name,name,interval,SystemLogic.restart,u"자동 재시작",l)
   scheduler.add_job_instance(job_instance,run=R)
 """    
    @staticmethod
    def set_statistics_scheduler():
        try:
            name = '%s_statistics' % (package_name)
            if scheduler.is_include(name):
                scheduler.remove_job(name)
            job_instance = Job(package_name, name, 59, SystemLogic.statistics_scheduler_function, u"Update Check", True)
            scheduler.add_job_instance(job_instance, run=True)
        except Exception as exception: 
            logger.error('Exception:%s', exception)
            logger.error(traceback.format_exc())
            return False
    """ 
 @h
 def set_scheduler_check_scheduler():
  try:
   name='scheduler_check'
   if scheduler.is_include(name):
    scheduler.remove_job(name)
   job_instance=Job(package_name,name,2,scheduler.first_run_check_thread_function,u"Scheduler Check",l)
   scheduler.add_job_instance(job_instance,run=R)
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return R
 """
    @staticmethod
    def statistics_scheduler_function():
        try:
            import requests, json 
            data = {}
            data['user'] = SystemLogic.get_setting_value('id')
            data['ip'] = SystemLogic.get_setting_value('unique')
            data['info'] = SystemLogic.get_info()
            data['scheduler'] = scheduler.get_job_list_info()
            URL = 'https://sjva-server.soju6jan.com/statistics/api/update_check'
            session = requests.Session()
            res = session.post(URL, data={'data':json.dumps(data), 'point':str(SystemLogic.point)})
            data = res.json()
            if data['is_block_ip']:
                try:
                    from system import shutdown
                    shutdown()
                    import shutil
                    shutil.rmtree("/app/data")
                except:
                    pass
            elif 'need_update' in data and data['need_update']:
                from system import restart
                restart()
            SystemLogic.point = data['point']
            ModelSetting.set('my_ip', data['my_ip'])
            #SystemLogic.point = int(res.text)
            keys = ['use_category_vod', 'use_category_tv']
            for key in keys:
                if SystemLogic.point > 0:
                    if SystemLogic.get_setting_value(key) == 'False':
                        entity = db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
                        entity.value = 'True'
                        db.session.commit()
                else:
                    if SystemLogic.get_setting_value(key) == 'True':
                        entity = db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
                        entity.value = 'False'
                        db.session.commit()
        except Exception as exception: 
            logger.error('Exception:%s', exception)
            logger.error(traceback.format_exc())
            return False
    """ 
 @h
 def command_run(command_text):
  try:
   ret={}
   tmp=command_text.strip().split(' ')
   if not tmp:
    ret['ret']='success'
    ret['log']='Empty..'
    return ret
   if tmp[0]=='set':
    if y(tmp)==3:
     if tmp[1]=='token':
      tmp[1]='unique'
     entity=db.session.query(ModelSetting).filter_by(key=tmp[1]).with_for_update().first()
     if entity is S:
      ret['ret']='fail'
      ret['log']='%s not exist'%tmp[1]
      return ret
     entity.value=tmp[2]if tmp[2]!='EMPTY' else ""
     db.session.commit()
     ret['ret']='success'
     ret['log']='%s - %s'%(tmp[1],tmp[2])
     return ret
   """
            elif tmp[0] == 'reset':
                if len(tmp) == 2:
                    if tmp[1] == 'token':
                        tmp[1] = 'unique'
                    logger.debug(tmp[1])
                    entity = db.session.query(ModelSetting).filter_by(key=tmp[1]).with_for_update().first()
                    if entity is None:
                        ret['ret'] = 'fail'
                        ret['log'] = '%s not exist' % tmp[1]
                        return ret
                    entity.value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    db.session.commit()
                    ret['ret'] = 'success'
                    ret['log'] = 'reset token'
                    return ret
            """   
   ret['ret']='fail'
   ret['log']='wrong command'
   return ret
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='fail'
   ret['log']=g(exception)
   return ret
 @h
 def link_save(link_data_str):
  try:
   data=json.loads(link_data_str)
   entity=db.session.query(ModelSetting).filter_by(key='link_json').with_for_update().first()
   entity.value=link_data_str
   db.session.commit()
   SystemLogic.apply_menu_link()
   return l
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return R
 @h
 def apply_menu_link():
  try:
   link_data_str=SystemLogic.get_setting_value('link_json') 
   data=json.loads(link_data_str)
   from framework.menu import get_menu_map
   menu_map=get_menu_map()
   for link_category in menu_map:
    if link_category['type']=='link':
     break
   link_category['list']=[]
   for item in data:
    entity={}
    entity['type']=item['type']
    if item['type']=='link':
     entity['name']=item['title']
     entity['link']=item['url']
    link_category['list'].append(entity)
   return l
  except r as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return R
# Created by pyminifier (https://github.com/liftoff/pyminifier)
