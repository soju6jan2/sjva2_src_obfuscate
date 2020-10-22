import os
L=object
Q=None
N=staticmethod
o=True
e=Exception
j=False
F=str
S=len
import traceback
H=traceback.format_exc
import logging
import platform
import time
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from framework.logger import get_logger
from framework import path_app_root,path_data,socketio,scheduler
v=scheduler.remove_job
K=scheduler.add_job_instance
g=socketio.emit
from framework.job import Job
from.plugin import logger,package_name
J=logger.error
from.model import ModelSetting
HQ=ModelSetting.get_bool
I=ModelSetting.get
h=ModelSetting.set
class SystemLogicSite(L):
 daum_cookie=Q
 @N
 def process_ajax(sub,req):
  try:
   ret={}
   if sub=='site_daum_test':
    site_daum_test=req.form['site_daum_test']
    h('site_daum_test',site_daum_test)
    from framework.common.daum import DaumTV,MovieSearch
    ret['TV']=DaumTV.get_daum_tv_info(site_daum_test)
    if ret['TV']is not Q and 'episode_list' in ret['TV']:
     del ret['TV']['episode_list']
    ret['MOVIE']=MovieSearch.search_movie(site_daum_test,-1)
    return jsonify(ret)
   elif sub=='site_daum_cookie_refresh':
    ret=SystemLogicSite.get_daum_cookie_by_selenium(notify=o)
    return jsonify(ret)
   elif sub=='scheduler':
    go=req.form['scheduler']
    if go=='true':
     SystemLogicSite.scheduler_start()
    else:
     SystemLogicSite.scheduler_stop()
    return jsonify(go)
  except e as e:
   J('Exception:%s',e)
   J(H())
   ret['ret']=j
   ret['log']=F(H())
  return jsonify(ret)
 @N
 def process_api(sub,req):
  ret={}
  try:
   if sub=='daum_cookie':
    return I('site_daum_cookie')
  except e as e:
   J('Exception:%s',e)
   J(H())
   ret['ret']='exception'
   ret['data']=F(e)
  return jsonify(ret)
 @N
 def plugin_load():
  return
  SystemLogicSite.get_daum_cookies(force=o)
  if HQ('site_daum_auto_start'):
   SystemLogicSite.scheduler_start()
 @N
 def scheduler_start():
  job=Job(package_name,'%s_site'%package_name,I('site_daum_interval'),SystemLogicSite.scheduler_function,u"Daum cookie refresh",j)
  K(job)
 @N
 def scheduler_stop():
  v('%s_site'%package_name)
 @N
 def scheduler_function():
  try:
   data=SystemLogicSite.get_daum_cookie_by_selenium()
   if data['ret']:
    h('site_daum_cookie',data['data'])
    SystemLogicSite.get_daum_cookies(force=o)
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N 
 def get_daum_cookie_by_selenium(notify=j):
  try:
   ret={}
   ret['ret']=j
   from.logic_selenium import SystemLogicSelenium
   if notify:
    data={'type':'success','msg':u'<strong>사이트 접속중입니다.</strong>'}
    g("notify",data,namespace='/framework',broadcast=o) 
   SystemLogicSelenium.get_pagesoruce_by_selenium('https://www.daum.net','//*[@id="daumFoot"]/div/a[1]/img')
   if notify:
    data={'type':'success','msg':u'쿠키 확인'}
    g("notify",data,namespace='/framework',broadcast=o) 
   driver=SystemLogicSelenium.get_driver()
   cookies=driver.get_cookies()
   for tmp in cookies:
    if tmp['name']=='TIARA':
     ret['ret']=o
     ret['data']='TIARA=%s'%tmp['value']
     return ret
  except e as e:
   J('Exception:%s',e)
   J(H()) 
  return ret
 @N
 def get_daum_cookies(force=j):
  try:
   if SystemLogicSite.daum_cookie is Q or force:
    ret={}
    tmp=I('site_daum_cookie')
    tmps=tmp.split(';')
    for t in tmps:
     t2=t.split('=')
     if S(t2)==2:
      ret[t2[0]]=t2[1]
    SystemLogicSite.daum_cookie=ret
   return SystemLogicSite.daum_cookie
  except e as e:
   J('Exception:%s',e)
   J(H())
   return{'TIARA':'gaXEIPluo-wWAFlwZN6l8gN3yzhkoo_piP.Kymhuy.6QBt4Q6.cRtxbKDaWpWajcyteRHzrlTVpJRxLjwLoMvyYLVi_7xJ1L'}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
