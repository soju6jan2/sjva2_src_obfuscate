import os
I=object
H=None
h=staticmethod
i=True
j=Exception
C=False
e=str
l=len
import traceback
V=traceback.format_exc
import logging
import platform
import time
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,path_data,socketio,scheduler
b=scheduler.remove_job
U=scheduler.add_job_instance
k=socketio.emit
from framework.job import Job
from.plugin import logger,package_name
D=logger.error
from.model import ModelSetting
VH=ModelSetting.get_bool
w=ModelSetting.get
z=ModelSetting.set
class SystemLogicSite(I):
 daum_cookie=H
 @h
 def process_ajax(sub,req):
  try:
   ret={}
   if sub=='site_daum_test':
    site_daum_test=req.form['site_daum_test']
    z('site_daum_test',site_daum_test)
    from framework.common.daum import DaumTV,MovieSearch
    ret['TV']=DaumTV.get_daum_tv_info(site_daum_test)
    if ret['TV']is not H and 'episode_list' in ret['TV']:
     del ret['TV']['episode_list']
    ret['MOVIE']=MovieSearch.search_movie(site_daum_test,-1)
    return jsonify(ret)
   elif sub=='site_daum_cookie_refresh':
    ret=SystemLogicSite.get_daum_cookie_by_selenium(notify=i)
    return jsonify(ret)
   elif sub=='scheduler':
    go=req.form['scheduler']
    if go=='true':
     SystemLogicSite.scheduler_start()
    else:
     SystemLogicSite.scheduler_stop()
    return jsonify(go)
  except j as e:
   D('Exception:%s',e)
   D(V())
   ret['ret']=C
   ret['log']=e(V())
  return jsonify(ret)
 @h
 def process_api(sub,req):
  ret={}
  try:
   if sub=='daum_cookie':
    return w('site_daum_cookie')
  except j as e:
   D('Exception:%s',e)
   D(V())
   ret['ret']='exception'
   ret['data']=e(e)
  return jsonify(ret)
 @h
 def plugin_load():
  return
  SystemLogicSite.get_daum_cookies(force=i)
  if VH('site_daum_auto_start'):
   SystemLogicSite.scheduler_start()
 @h
 def scheduler_start():
  job=Job(package_name,'%s_site'%package_name,w('site_daum_interval'),SystemLogicSite.scheduler_function,u"Daum cookie refresh",C)
  U(job)
 @h
 def scheduler_stop():
  b('%s_site'%package_name)
 @h
 def scheduler_function():
  try:
   data=SystemLogicSite.get_daum_cookie_by_selenium()
   if data['ret']:
    z('site_daum_cookie',data['data'])
    SystemLogicSite.get_daum_cookies(force=i)
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h 
 def get_daum_cookie_by_selenium(notify=C):
  try:
   ret={}
   ret['ret']=C
   from.logic_selenium import SystemLogicSelenium
   if notify:
    data={'type':'success','msg':u'<strong>사이트 접속중입니다.</strong>'}
    k("notify",data,namespace='/framework',broadcast=i) 
   SystemLogicSelenium.get_pagesoruce_by_selenium('https://www.daum.net','//*[@id="daumFoot"]/div/a[1]/img')
   if notify:
    data={'type':'success','msg':u'쿠키 확인'}
    k("notify",data,namespace='/framework',broadcast=i) 
   driver=SystemLogicSelenium.get_driver()
   cookies=driver.get_cookies()
   for tmp in cookies:
    if tmp['name']=='TIARA':
     ret['ret']=i
     ret['data']='TIARA=%s'%tmp['value']
     return ret
  except j as e:
   D('Exception:%s',e)
   D(V()) 
  return ret
 @h
 def get_daum_cookies(force=C):
  try:
   if SystemLogicSite.daum_cookie is H or force:
    ret={}
    tmp=w('site_daum_cookie')
    tmps=tmp.split(';')
    for t in tmps:
     t2=t.split('=')
     if l(t2)==2:
      ret[t2[0]]=t2[1]
    SystemLogicSite.daum_cookie=ret
   return SystemLogicSite.daum_cookie
  except j as e:
   D('Exception:%s',e)
   D(V())
   return{'TIARA':'gaXEIPluo-wWAFlwZN6l8gN3yzhkoo_piP.Kymhuy.6QBt4Q6.cRtxbKDaWpWajcyteRHzrlTVpJRxLjwLoMvyYLVi_7xJ1L'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
