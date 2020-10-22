import os
q=object
u=None
F=staticmethod
Q=True
y=Exception
s=False
S=str
J=len
import traceback
import logging
import platform
import time
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,path_data,socketio,scheduler
from framework.job import Job
from.plugin import logger,package_name
from.model import ModelSetting
class SystemLogicSite(q):
 daum_cookie=u
 @F
 def process_ajax(sub,req):
  try:
   ret={}
   if sub=='site_daum_test':
    site_daum_test=req.form['site_daum_test']
    ModelSetting.set('site_daum_test',site_daum_test)
    from framework.common.daum import DaumTV,MovieSearch
    ret['TV']=DaumTV.get_daum_tv_info(site_daum_test)
    if ret['TV']is not u and 'episode_list' in ret['TV']:
     del ret['TV']['episode_list']
    ret['MOVIE']=MovieSearch.search_movie(site_daum_test,-1)
    return jsonify(ret)
   elif sub=='site_daum_cookie_refresh':
    ret=SystemLogicSite.get_daum_cookie_by_selenium(notify=Q)
    return jsonify(ret)
   elif sub=='scheduler':
    go=req.form['scheduler']
    if go=='true':
     SystemLogicSite.scheduler_start()
    else:
     SystemLogicSite.scheduler_stop()
    return jsonify(go)
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']=s
   ret['log']=S(traceback.format_exc())
  return jsonify(ret)
 @F
 def process_api(sub,req):
  ret={}
  try:
   if sub=='daum_cookie':
    return ModelSetting.get('site_daum_cookie')
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['data']=S(exception)
  return jsonify(ret)
 @F
 def plugin_load():
  return
  SystemLogicSite.get_daum_cookies(force=Q)
  if ModelSetting.get_bool('site_daum_auto_start'):
   SystemLogicSite.scheduler_start()
 @F
 def scheduler_start():
  job=Job(package_name,'%s_site'%package_name,ModelSetting.get('site_daum_interval'),SystemLogicSite.scheduler_function,u"Daum cookie refresh",s)
  scheduler.add_job_instance(job)
 @F
 def scheduler_stop():
  scheduler.remove_job('%s_site'%package_name)
 @F
 def scheduler_function():
  try:
   data=SystemLogicSite.get_daum_cookie_by_selenium()
   if data['ret']:
    ModelSetting.set('site_daum_cookie',data['data'])
    SystemLogicSite.get_daum_cookies(force=Q)
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @F 
 def get_daum_cookie_by_selenium(notify=s):
  try:
   ret={}
   ret['ret']=s
   from.logic_selenium import SystemLogicSelenium
   if notify:
    data={'type':'success','msg':u'<strong>사이트 접속중입니다.</strong>'}
    socketio.emit("notify",data,namespace='/framework',broadcast=Q) 
   SystemLogicSelenium.get_pagesoruce_by_selenium('https://www.daum.net','//*[@id="daumFoot"]/div/a[1]/img')
   if notify:
    data={'type':'success','msg':u'쿠키 확인'}
    socketio.emit("notify",data,namespace='/framework',broadcast=Q) 
   driver=SystemLogicSelenium.get_driver()
   cookies=driver.get_cookies()
   for tmp in cookies:
    if tmp['name']=='TIARA':
     ret['ret']=Q
     ret['data']='TIARA=%s'%tmp['value']
     return ret
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  return ret
 @F
 def get_daum_cookies(force=s):
  try:
   if SystemLogicSite.daum_cookie is u or force:
    ret={}
    tmp=ModelSetting.get('site_daum_cookie')
    tmps=tmp.split(';')
    for t in tmps:
     t2=t.split('=')
     if J(t2)==2:
      ret[t2[0]]=t2[1]
    SystemLogicSite.daum_cookie=ret
   return SystemLogicSite.daum_cookie
  except y as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return{'TIARA':'gaXEIPluo-wWAFlwZN6l8gN3yzhkoo_piP.Kymhuy.6QBt4Q6.cRtxbKDaWpWajcyteRHzrlTVpJRxLjwLoMvyYLVi_7xJ1L'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
