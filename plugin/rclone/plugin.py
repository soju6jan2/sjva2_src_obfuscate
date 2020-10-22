import os
Y=Exception
J=str
X=None
R=False
W=True
z=os.listdir
c=os.path
import traceback
b=traceback.format_exc
import time
from datetime import datetime
import urllib
import json
cH=json.loads
T=json.dumps
import platform
import requests
cb=requests.request
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
cF=session.query
cQ=request.sid
ca=request.form
ch=request.cookies
cm=request.get_data
cD=request.headers
ce=request.method
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio
cn=socketio.emit
cO=socketio.on
cy=scheduler.is_running
v=scheduler.is_include
y=db.session
from framework.util import Util,AlchemyEncoder
cv=Util.db_list_to_dict
from system.model import ModelSetting as SystemModelSetting
M=ModelSetting.get
cI=ModelSetting.setting_save
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.model import ModelSetting
M=ModelSetting.get
cI=ModelSetting.setting_save
from.logic import Logic
cN=Logic.current_data
cj=Logic.mount_remove
cV=Logic.mount_kill
cR=Logic.mount_stop
ct=Logic.mount_execute
ck=Logic.mount_save
cW=Logic.mount_list
cJ=Logic.get_log
cY=Logic.reset_db
cu=Logic.filelist
cX=Logic.remove_job
cK=Logic.execute_job
cE=Logic.scheduler_stop
cg=Logic.scheduler_start
cq=Logic.job_save
cL=Logic.get_jobs
cU=Logic.load_remotes
d=Logic.path_config
cl=Logic.rclone_version
cG=Logic.default_rclone_setting
x=Logic.path_rclone
cC=Logic.kill
ci=Logic.plugin_unload
cM=Logic.plugin_load
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder=c.join(c.dirname(__file__),'templates'),static_folder=c.join(c.dirname(__file__),'build'),static_url_path='build')
menu={'main':[package_name,u'RClone'],'sub':[['setting',u'설정'],['status',u'상태'],['list',u'목록'],['mount',u'Mount'],['serve_setting',u'Serve'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  cM()
 except Y as e:
  logger.error('Exception:%s',e)
  logger.error(b())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  ci()
  cC()
 except Y as e:
  logger.error('Exception:%s',e)
  logger.error(b())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.cF(ModelSetting).all()
  arg=cv(setting_list)
  arg['scheduler']=J(v(package_name))
  arg['is_running']=J(cy(package_name))
  arg['path_rclone']=x
  arg['default_rclone_setting']=cG
  return render_template('rclone_setting.html',sub=sub,arg=arg)
 elif sub=='status':
  return render_template('rclone_status.html')
 elif sub=='list':
  return render_template('rclone_list.html')
 elif sub=='log':
  return render_template('log.html',package=package_name)
 elif sub=='mount':
  return redirect('/%s/mount_setting'%package_name)
 elif sub=='mount_setting':
  arg={}
  arg['option']='--allow-other --fast-list --drive-skip-gdocs --poll-interval=1m --buffer-size=32M --vfs-read-chunk-size=32M --vfs-read-chunk-size-limit 2048M --vfs-cache-mode writes --dir-cache-time=1m --log-level INFO'
  return render_template('%s_%s.html'%(package_name,sub),arg=arg)
 elif sub=='serve_setting':
  arg={}
  arg['option']='--user sjva --pass sjva --fast-list --drive-skip-gdocs --poll-interval=1m --buffer-size=32M --vfs-read-chunk-size=32M --vfs-read-chunk-size-limit 2048M --vfs-cache-mode writes --dir-cache-time=1m --log-level INFO'
  return render_template('%s_%s.html'%(package_name,sub),arg=arg)
 else:
  return blueprint.send_static_file(sub)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
HTTP_METHODS=['GET','HEAD','POST','PUT','DELETE','CONNECT','OPTIONS','TRACE','PATCH']
@blueprint.route('/<sub>/<path:path>',methods=HTTP_METHODS)
@login_required
def detail2(sub,path):
 logger.debug('DETAIL2 %s %s',package_name,sub)
 if sub=='static':
  return blueprint.send_static_file('static/'+path)
 else:
  if path is X:
   return blueprint.send_static_file(sub)
  else:
   url='http://127.0.0.1:5572/%s/%s'%(sub,path)
   return proxy(request,url)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
def proxy(request,url):
 try:
  resp=cb(method=ce,url=url,headers={key:value for(key,value)in cD if key!='Host'},data=cm(),cookies=ch,allow_redirects=R)
  excluded_headers=['content-encoding','content-length','transfer-encoding','connection']
  headers=[(name,value)for(name,value)in resp.raw.headers.items()if name.lower()not in excluded_headers]
  response=Response(resp.text,resp.status_code,headers)
  return response
 except Y as e:
  logger.error('Exception:%s',e)
  logger.error(b())
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 if sub=='rclone_version':
  try:
   ret=cl()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='send_to_command_plugin':
  try:
   c=ca['command']
   ret='%s --config %s %s'%(x,d,c)
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='load_remotes':
  try:
   ret={}
   ret['remotes']=cU()
   ret['jobs']=cL()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='remote_ls':
  try:
   remote=ca['remote']
   remote_path=ca['remote_path']
   ret='%s --config %s lsf "%s:%s" --max-depth 1'%(x,d,remote,remote_path)
   import command 
   ret=command.LogicNormal.execute_thread_function(ret)
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='local_ls':
  try:
   local_path=ca['local_path']
   logger.debug('local_path:%s',local_path)
   if not c.exists(local_path):
    ret='NOT EXIST'
   else:
    ret=z(local_path)
    if not ret:
     ret='EMPTY'
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='job_save':
  try:
   ret={}
   ret['ret']=cq(request)
   ret['remotes']=cU()
   ret['jobs']=cL()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='setting_save':
  ret=cI(request)
  x=M('rclone_bin_path')
  d=M('rclone_config_path')
  return jsonify(ret)
 elif sub=='scheduler':
  try:
   go=ca['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    cg()
   else:
    cE()
   return jsonify(go)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
   return jsonify('fail')
 elif sub=='status':
  try:
   pass
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='stop':
  try:
   ret=cC()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='scheduler_stop':
  try:
   ret=cC()
   if v(package_name):
    cE()
    ret='success'
   else:
    ret='not_running'
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='execute_job':
  try:
   ret=cK(request)
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='remove_job':
  try:
   ret={}
   ret['ret']=cX(request)
   ret['remotes']=cU()
   ret['jobs']=cL()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='filelist':
  try:
   ret=cu(request)
   ret['jobs']=cL()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='reset_db':
  try:
   ret=cY()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b()) 
 elif sub=='get_log':
  try:
   return jsonify(cJ(request))
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='load_mounts':
  try:
   ret={}
   ret['mounts']=cW()
   ret['remotes']=cU()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='mount_save':
  try:
   ret={}
   ret['ret']=ck(request)
   ret['remotes']=cU()
   ret['mounts']=cW()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='mount_execute':
  try:
   ret={}
   mount_id=ca['id']
   ret['ret']=ct(mount_id)
   ret['remotes']=cU()
   ret['mounts']=cW()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='mount_stop':
  try:
   ret={}
   ret['ret']=cR(request)
   ret['remotes']=cU()
   ret['mounts']=cW()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='mount_remove':
  try:
   ret={}
   mount_id=ca['id']
   cV(mount_id)
   ret['ret']=cj(mount_id)
   ret['remotes']=cU()
   ret['mounts']=cW()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='load_serves':
  try:
   from.logic_serve import LogicServe
   ret={}
   ret['serves']=LogicServe.serve_list()
   ret['remotes']=cU()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='serve_save':
  try:
   from.logic_serve import LogicServe
   ret={}
   ret['ret']=LogicServe.serve_save(request)
   ret['remotes']=cU()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='serve_execute':
  try:
   from.logic_serve import LogicServe
   ret={}
   serve_id=ca['id']
   ret['ret']=LogicServe.serve_execute(serve_id)
   ret['remotes']=cU()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='serve_stop':
  try:
   from.logic_serve import LogicServe
   ret={}
   ret['ret']=LogicServe.serve_stop(request)
   ret['remotes']=cU()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
 elif sub=='serve_remove':
  try:
   from.logic_serve import LogicServe
   ret={}
   serve_id=ca['id']
   LogicServe.serve_kill(serve_id)
   ret['ret']=LogicServe.serve_remove(serve_id)
   ret['remotes']=cU()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except Y as e:
   logger.error('Exception:%s',e)
   logger.error(b())
sid_list=[]
@cO('connect',namespace='/%s'%package_name)
def connect():
 try:
  logger.debug('socket_connect')
  sid_list.append(cQ)
  tmp=X
  if cN is not X:
   tmp=T(cN,cls=AlchemyEncoder)
   tmp=cH(tmp)
  emit('on_connect',tmp,namespace='/%s'%package_name)
 except Y as e:
  logger.error('Exception:%s',e)
  logger.error(b())
@cO('disconnect',namespace='/%s'%package_name)
def disconnect():
 try:
  sid_list.remove(cQ)
  logger.debug('socket_disconnect')
 except Y as e:
  logger.error('Exception:%s',e)
  logger.error(b())
def socketio_callback(cmd,data):
 if sid_list:
  tmp=T(data,cls=AlchemyEncoder)
  tmp=cH(tmp)
  cn(cmd,tmp,namespace='/%s'%package_name,broadcast=W)
"""
@blueprint.route('/rc/<path:path>',methods=['GET','POST','DELETE'])
def rc(path):
    url = 'http://127.0.0.1:5572/rc/' + path
    return proxy(request, url)
@blueprint.route('/core/<path:path>',methods=['GET','POST','DELETE'])
def core(path):
    url = 'http://127.0.0.1:5572/core/' + path
    return proxy(request, url)
def proxy(request, url):
    resp = requests.request(method=request.method, url=url, headers={key: value for (key, value) in request.headers if key != 'Host'}, data=request.get_data(), cookies=request.cookies, allow_redirects=False)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.text, resp.status_code, headers)
    return response
# coding:utf-8
# Copyright 2011 litl, LLC. All Rights Reserved.
import httplib
import re
import urllib
import urlparse
from flask import Blueprint, request, Response, url_for
from werkzeug.datastructures import Headers
from werkzeug.exceptions import NotFound
HTML_REGEX = re.compile(r'((?:src|action|href)=["\'])/')
JQUERY_REGEX = re.compile(r'(\$\.(?:get|post)\(["\'])/')
JS_LOCATION_REGEX = re.compile(r'((?:window|document)\.location.*=.*["\'])/')
CSS_REGEX = re.compile(r'(url\(["\']?)/')
REGEXES = [HTML_REGEX, JQUERY_REGEX, JS_LOCATION_REGEX, CSS_REGEX]
def iterform(multidict):
    for key in multidict.keys():
        for value in multidict.getlist(key):
            yield (key.encode("utf8"), value.encode("utf8"))
def parse_host_port(h):
    host_port = h.split(":", 1)
    if len(host_port) == 1:
        return (h, 80)
    else:
        host_port[1] = int(host_port[1])
        return host_port
#@blueprint.route('/proxy/<host>/', methods=["GET", "POST"])
#@blueprint.route('/proxy/<host>/<path:file>', methods=["GET", "POST"])
@blueprint.route('/proxy/', methods=["GET", "POST"])
@blueprint.route('/proxy/<path:file>', methods=["GET", "POST"])
def proxy_request(file=""):
    #hostname, port = parse_host_port(host)
    hostname = 'http://sjva:sjva@127.0.0.1'
    host = 'http://sjva:sjva@127.0.0.1:9998'
    port = 9998
    # Whitelist a few headers to pass on
    request_headers = {}
    for h in ["Cookie", "Referer", "X-Csrf-Token"]:
        if h in request.headers:
            request_headers[h] = request.headers[h]
    if request.query_string:
        path = "/%s?%s" % (file, request.query_string)
    else:
        path = "/" + file
    if request.method == "POST":
        form_data = list(iterform(request.form))
        form_data = py_urllib.urlencode(form_data)
        request_headers["Content-Length"] = len(form_data)
    else:
        form_data = None
    conn = httplib.HTTPConnection(hostname, port)
    conn.request(request.method, path, body=form_data, headers=request_headers)
    resp = conn.getresponse()
    # Clean up response headers for forwarding
    response_headers = Headers()
    for key, value in resp.getheaders():
        if key in ["content-length", "connection", "content-type"]:
            continue
        if key == "set-cookie":
            cookies = value.split(",")
            [response_headers.add(key, c) for c in cookies]
        else:
            response_headers.add(key, value)
    # If this is a redirect, munge the Location URL
    if "location" in response_headers:
        redirect = response_headers["location"]
        parsed = urlparse.urlparse(request.url)
        redirect_parsed = urlparse.urlparse(redirect)
        redirect_host = redirect_parsed.netloc
        if not redirect_host:
            redirect_host = "%s:%d" % (hostname, port)
        redirect_path = redirect_parsed.path
        if redirect_parsed.query:
            redirect_path += "?" + redirect_parsed.query
        munged_path = url_for(".proxy_request", host=redirect_host, file=redirect_path[1:])
        url = "%s://%s%s" % (parsed.scheme, parsed.netloc, munged_path)
        response_headers["location"] = url
    # Rewrite URLs in the content to point to our URL scheme instead.
    # Ugly, but seems to mostly work.
    root = url_for(".proxy_request", host=host)
    contents = resp.read()
    for regex in REGEXES:
        contents = regex.sub(r'\1%s' % root, contents)
    flask_response = Response(response=contents, status=resp.status, headers=response_headers, content_type=resp.getheader('content-type'))
    return flask_response
"""
# Created by pyminifier (https://github.com/liftoff/pyminifier)
