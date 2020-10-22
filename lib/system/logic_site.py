import os
R=object
w=None
m=staticmethod
Y=True
f=Exception
L=False
l=str
a=len
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
class SystemLogicSite(R):
 daum_cookie=w
 @m
 def process_ajax(sub,req):
  try:
   ret={}
   if sub=='site_daum_test':
    site_daum_test=req.form['site_daum_test']
    ModelSetting.set('site_daum_test',site_daum_test)
    from framework.common.daum import DaumTV,MovieSearch
    ret['TV']=DaumTV.get_daum_tv_info(site_daum_test)
    if ret['TV']is not w and 'episode_list' in ret['TV']:
     del ret['TV']['episode_list']
    ret['MOVIE']=MovieSearch.search_movie(site_daum_test,-1)
    return jsonify(ret)
   elif sub=='site_daum_cookie_refresh':
    ret=SystemLogicSite.get_daum_cookie_by_selenium(notify=Y)
    return jsonify(ret)
   elif sub=='scheduler':
    go=req.form['scheduler']
    if go=='true':
     SystemLogicSite.scheduler_start()
    else:
     SystemLogicSite.scheduler_stop()
    return jsonify(go)
  except f as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']=L
   ret['log']=l(traceback.format_exc())
  return jsonify(ret)
 @m
 def process_api(sub,req):
  ret={}
  try:
   if sub=='daum_cookie':
    return ModelSetting.get('site_daum_cookie')
  except f as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['data']=l(exception)
  return jsonify(ret)
 @m
 def plugin_load():
  return
  SystemLogicSite.get_daum_cookies(force=Y)
  if ModelSetting.get_bool('site_daum_auto_start'):
   SystemLogicSite.scheduler_start()
 @m
 def scheduler_start():
  job=Job(package_name,'%s_site'%package_name,ModelSetting.get('site_daum_interval'),SystemLogicSite.scheduler_function,u"Daum cookie refresh",L)
  scheduler.add_job_instance(job)
 @m
 def scheduler_stop():
  scheduler.remove_job('%s_site'%package_name)
 @m
 def scheduler_function():
  try:
   data=SystemLogicSite.get_daum_cookie_by_selenium()
   if data['ret']:
    ModelSetting.set('site_daum_cookie',data['data'])
    SystemLogicSite.get_daum_cookies(force=Y)
  except f as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @m 
 def get_daum_cookie_by_selenium(notify=L):
  try:
   ret={}
   ret['ret']=L
   from.logic_selenium import SystemLogicSelenium
   if notify:
    data={'type':'success','msg':u'<strong>사이트 접속중입니다.</strong>'}
    socketio.emit("notify",data,namespace='/framework',broadcast=Y) 
   SystemLogicSelenium.get_pagesoruce_by_selenium('https://www.daum.net','//*[@id="daumFoot"]/div/a[1]/img')
   if notify:
    data={'type':'success','msg':u'쿠키 확인'}
    socketio.emit("notify",data,namespace='/framework',broadcast=Y) 
   driver=SystemLogicSelenium.get_driver()
   cookies=driver.get_cookies()
   for tmp in cookies:
    if tmp['name']=='TIARA':
     ret['ret']=Y
     ret['data']='TIARA=%s'%tmp['value']
     return ret
  except f as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  return ret
 @m
 def get_daum_cookies(force=L):
  try:
   if SystemLogicSite.daum_cookie is w or force:
    ret={}
    tmp=ModelSetting.get('site_daum_cookie')
    tmps=tmp.split(';')
    for t in tmps:
     t2=t.split('=')
     if a(t2)==2:
      ret[t2[0]]=t2[1]
    SystemLogicSite.daum_cookie=ret
   return SystemLogicSite.daum_cookie
  except f as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return{'TIARA':'gaXEIPluo-wWAFlwZN6l8gN3yzhkoo_piP.Kymhuy.6QBt4Q6.cRtxbKDaWpWajcyteRHzrlTVpJRxLjwLoMvyYLVi_7xJ1L'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
