import os
p=object
u=None
H=staticmethod
G=True
P=Exception
V=False
r=str
K=len
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
class SystemLogicSite(p):
 daum_cookie=u
 @H
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
    ret=SystemLogicSite.get_daum_cookie_by_selenium(notify=G)
    return jsonify(ret)
   elif sub=='scheduler':
    go=req.form['scheduler']
    if go=='true':
     SystemLogicSite.scheduler_start()
    else:
     SystemLogicSite.scheduler_stop()
    return jsonify(go)
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']=V
   ret['log']=r(traceback.format_exc())
  return jsonify(ret)
 @H
 def process_api(sub,req):
  ret={}
  try:
   if sub=='daum_cookie':
    return ModelSetting.get('site_daum_cookie')
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   ret['ret']='exception'
   ret['data']=r(exception)
  return jsonify(ret)
 @H
 def plugin_load():
  return
  SystemLogicSite.get_daum_cookies(force=G)
  if ModelSetting.get_bool('site_daum_auto_start'):
   SystemLogicSite.scheduler_start()
 @H
 def scheduler_start():
  job=Job(package_name,'%s_site'%package_name,ModelSetting.get('site_daum_interval'),SystemLogicSite.scheduler_function,u"Daum cookie refresh",V)
  scheduler.add_job_instance(job)
 @H
 def scheduler_stop():
  scheduler.remove_job('%s_site'%package_name)
 @H
 def scheduler_function():
  try:
   data=SystemLogicSite.get_daum_cookie_by_selenium()
   if data['ret']:
    ModelSetting.set('site_daum_cookie',data['data'])
    SystemLogicSite.get_daum_cookies(force=G)
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @H 
 def get_daum_cookie_by_selenium(notify=V):
  try:
   ret={}
   ret['ret']=V
   from.logic_selenium import SystemLogicSelenium
   if notify:
    data={'type':'success','msg':u'<strong>사이트 접속중입니다.</strong>'}
    socketio.emit("notify",data,namespace='/framework',broadcast=G) 
   SystemLogicSelenium.get_pagesoruce_by_selenium('https://www.daum.net','//*[@id="daumFoot"]/div/a[1]/img')
   if notify:
    data={'type':'success','msg':u'쿠키 확인'}
    socketio.emit("notify",data,namespace='/framework',broadcast=G) 
   driver=SystemLogicSelenium.get_driver()
   cookies=driver.get_cookies()
   for tmp in cookies:
    if tmp['name']=='TIARA':
     ret['ret']=G
     ret['data']='TIARA=%s'%tmp['value']
     return ret
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
  return ret
 @H
 def get_daum_cookies(force=V):
  try:
   if SystemLogicSite.daum_cookie is u or force:
    ret={}
    tmp=ModelSetting.get('site_daum_cookie')
    tmps=tmp.split(';')
    for t in tmps:
     t2=t.split('=')
     if K(t2)==2:
      ret[t2[0]]=t2[1]
    SystemLogicSite.daum_cookie=ret
   return SystemLogicSite.daum_cookie
  except P as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return{'TIARA':'gaXEIPluo-wWAFlwZN6l8gN3yzhkoo_piP.Kymhuy.6QBt4Q6.cRtxbKDaWpWajcyteRHzrlTVpJRxLjwLoMvyYLVi_7xJ1L'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
