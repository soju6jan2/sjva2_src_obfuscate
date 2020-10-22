import os
f=object
W=None
v=staticmethod
k=True
V=Exception
C=False
A=str
Q=len
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
class SystemLogicSite(f):
 daum_cookie=W
 @v
 def process_ajax(sub,req):
  try:
   ret={}
   if sub=='site_daum_test':
    site_daum_test=req.form['site_daum_test']
    ModelSetting.set('site_daum_test',site_daum_test)
    from framework.common.daum import DaumTV,MovieSearch
    ret['TV']=DaumTV.get_daum_tv_info(site_daum_test)
    if ret['TV']is not W and 'episode_list' in ret['TV']:
     del ret['TV']['episode_list']
    ret['MOVIE']=MovieSearch.search_movie(site_daum_test,-1)
    return jsonify(ret)
   elif sub=='site_daum_cookie_refresh':
    ret=SystemLogicSite.get_daum_cookie_by_selenium(notify=k)
    return jsonify(ret)
   elif sub=='scheduler':
    go=req.form['scheduler']
    if go=='true':
     SystemLogicSite.scheduler_start()
    else:
     SystemLogicSite.scheduler_stop()
    return jsonify(go)
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']=C
   ret['log']=A(traceback.format_exc())
  return jsonify(ret)
 @v
 def process_api(sub,req):
  ret={}
  try:
   if sub=='daum_cookie':
    return ModelSetting.get('site_daum_cookie')
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['data']=A(exception)
  return jsonify(ret)
 @v
 def plugin_load():
  return
  SystemLogicSite.get_daum_cookies(force=k)
  if ModelSetting.get_bool('site_daum_auto_start'):
   SystemLogicSite.scheduler_start()
 @v
 def scheduler_start():
  job=Job(package_name,'%s_site'%package_name,ModelSetting.get('site_daum_interval'),SystemLogicSite.scheduler_function,u"Daum cookie refresh",C)
  scheduler.add_job_instance(job)
 @v
 def scheduler_stop():
  scheduler.remove_job('%s_site'%package_name)
 @v
 def scheduler_function():
  try:
   data=SystemLogicSite.get_daum_cookie_by_selenium()
   if data['ret']:
    ModelSetting.set('site_daum_cookie',data['data'])
    SystemLogicSite.get_daum_cookies(force=k)
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @v 
 def get_daum_cookie_by_selenium(notify=C):
  try:
   ret={}
   ret['ret']=C
   from.logic_selenium import SystemLogicSelenium
   if notify:
    data={'type':'success','msg':u'<strong>사이트 접속중입니다.</strong>'}
    socketio.emit("notify",data,namespace='/framework',broadcast=k) 
   SystemLogicSelenium.get_pagesoruce_by_selenium('https://www.daum.net','//*[@id="daumFoot"]/div/a[1]/img')
   if notify:
    data={'type':'success','msg':u'쿠키 확인'}
    socketio.emit("notify",data,namespace='/framework',broadcast=k) 
   driver=SystemLogicSelenium.get_driver()
   cookies=driver.get_cookies()
   for tmp in cookies:
    if tmp['name']=='TIARA':
     ret['ret']=k
     ret['data']='TIARA=%s'%tmp['value']
     return ret
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  return ret
 @v
 def get_daum_cookies(force=C):
  try:
   if SystemLogicSite.daum_cookie is W or force:
    ret={}
    tmp=ModelSetting.get('site_daum_cookie')
    tmps=tmp.split(';')
    for t in tmps:
     t2=t.split('=')
     if Q(t2)==2:
      ret[t2[0]]=t2[1]
    SystemLogicSite.daum_cookie=ret
   return SystemLogicSite.daum_cookie
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return{'TIARA':'gaXEIPluo-wWAFlwZN6l8gN3yzhkoo_piP.Kymhuy.6QBt4Q6.cRtxbKDaWpWajcyteRHzrlTVpJRxLjwLoMvyYLVi_7xJ1L'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
