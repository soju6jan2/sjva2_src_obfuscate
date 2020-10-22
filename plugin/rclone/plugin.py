import os
R=Exception
X=str
v=None
H=False
W=True
n=os.listdir
D=os.path
import traceback
F=traceback.format_exc
import time
from datetime import datetime
import urllib
import json
DC=json.loads
A=json.dumps
import platform
import requests
DF=requests.request
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
Dz=session.query
Db=request.sid
Da=request.form
Ds=request.cookies
DS=request.get_data
Dh=request.headers
Di=request.method
from flask_socketio import SocketIO,emit,send
from flask_login import login_user,logout_user,current_user,login_required
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio
DP=socketio.emit
Du=socketio.on
DB=scheduler.is_running
x=scheduler.is_include
B=db.session
from framework.util import Util,AlchemyEncoder
Dx=Util.db_list_to_dict
from system.model import ModelSetting as SystemModelSetting
e=ModelSetting.get
DJ=ModelSetting.setting_save
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
from.model import ModelSetting
e=ModelSetting.get
DJ=ModelSetting.setting_save
from.logic import Logic
Dd=Logic.current_data
Dy=Logic.mount_remove
Dg=Logic.mount_kill
DH=Logic.mount_stop
Dk=Logic.mount_execute
DL=Logic.mount_save
DW=Logic.mount_list
DX=Logic.get_log
DR=Logic.reset_db
DG=Logic.filelist
Dv=Logic.remove_job
DE=Logic.execute_job
DM=Logic.scheduler_stop
Dt=Logic.scheduler_start
Dw=Logic.job_save
Dr=Logic.get_jobs
DY=Logic.load_remotes
c=Logic.path_config
Dp=Logic.rclone_version
DO=Logic.default_rclone_setting
Q=Logic.path_rclone
DU=Logic.kill
DV=Logic.plugin_unload
De=Logic.plugin_load
blueprint=Blueprint(package_name,package_name,url_prefix='/%s'%package_name,template_folder=D.join(D.dirname(__file__),'templates'),static_folder=D.join(D.dirname(__file__),'build'),static_url_path='build')
menu={'main':[package_name,u'RClone'],'sub':[['setting',u'설정'],['status',u'상태'],['list',u'목록'],['mount',u'Mount'],['serve_setting',u'Serve'],['log',u'로그']]}
def plugin_load():
 try:
  logger.debug('plugin_load:%s',package_name)
  De()
 except R as e:
  logger.error('Exception:%s',e)
  logger.error(F())
def plugin_unload():
 try:
  logger.debug('plugin_unload:%s',package_name)
  DV()
  DU()
 except R as e:
  logger.error('Exception:%s',e)
  logger.error(F())
@blueprint.route('/')
def home():
 return redirect('/%s/list'%package_name)
@blueprint.route('/<sub>')
@login_required
def detail(sub):
 logger.debug('DETAIL %s %s',package_name,sub)
 if sub=='setting':
  setting_list=db.Dz(ModelSetting).all()
  arg=Dx(setting_list)
  arg['scheduler']=X(x(package_name))
  arg['is_running']=X(DB(package_name))
  arg['path_rclone']=Q
  arg['default_rclone_setting']=DO
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
  if path is v:
   return blueprint.send_static_file(sub)
  else:
   url='http://127.0.0.1:5572/%s/%s'%(sub,path)
   return proxy(request,url)
 return render_template('sample.html',title='%s - %s'%(package_name,sub))
def proxy(request,url):
 try:
  resp=DF(method=Di,url=url,headers={key:value for(key,value)in Dh if key!='Host'},data=DS(),cookies=Ds,allow_redirects=H)
  excluded_headers=['content-encoding','content-length','transfer-encoding','connection']
  headers=[(name,value)for(name,value)in resp.raw.headers.items()if name.lower()not in excluded_headers]
  response=Response(resp.text,resp.status_code,headers)
  return response
 except R as e:
  logger.error('Exception:%s',e)
  logger.error(F())
@blueprint.route('/ajax/<sub>',methods=['GET','POST'])
@login_required
def ajax(sub):
 logger.debug('AJAX %s %s',package_name,sub)
 if sub=='rclone_version':
  try:
   ret=Dp()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='send_to_command_plugin':
  try:
   c=Da['command']
   ret='%s --config %s %s'%(Q,c,c)
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='load_remotes':
  try:
   ret={}
   ret['remotes']=DY()
   ret['jobs']=Dr()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='remote_ls':
  try:
   remote=Da['remote']
   remote_path=Da['remote_path']
   ret='%s --config %s lsf "%s:%s" --max-depth 1'%(Q,c,remote,remote_path)
   import command 
   ret=command.LogicNormal.execute_thread_function(ret)
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='local_ls':
  try:
   local_path=Da['local_path']
   logger.debug('local_path:%s',local_path)
   if not D.exists(local_path):
    ret='NOT EXIST'
   else:
    ret=n(local_path)
    if not ret:
     ret='EMPTY'
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='job_save':
  try:
   ret={}
   ret['ret']=Dw(request)
   ret['remotes']=DY()
   ret['jobs']=Dr()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='setting_save':
  ret=DJ(request)
  Q=e('rclone_bin_path')
  c=e('rclone_config_path')
  return jsonify(ret)
 elif sub=='scheduler':
  try:
   go=Da['scheduler']
   logger.debug('scheduler :%s',go)
   if go=='true':
    Dt()
   else:
    DM()
   return jsonify(go)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
   return jsonify('fail')
 elif sub=='status':
  try:
   pass
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='stop':
  try:
   ret=DU()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='scheduler_stop':
  try:
   ret=DU()
   if x(package_name):
    DM()
    ret='success'
   else:
    ret='not_running'
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='execute_job':
  try:
   ret=DE(request)
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='remove_job':
  try:
   ret={}
   ret['ret']=Dv(request)
   ret['remotes']=DY()
   ret['jobs']=Dr()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='filelist':
  try:
   ret=DG(request)
   ret['jobs']=Dr()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='reset_db':
  try:
   ret=DR()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F()) 
 elif sub=='get_log':
  try:
   return jsonify(DX(request))
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='load_mounts':
  try:
   ret={}
   ret['mounts']=DW()
   ret['remotes']=DY()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='mount_save':
  try:
   ret={}
   ret['ret']=DL(request)
   ret['remotes']=DY()
   ret['mounts']=DW()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='mount_execute':
  try:
   ret={}
   mount_id=Da['id']
   ret['ret']=Dk(mount_id)
   ret['remotes']=DY()
   ret['mounts']=DW()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='mount_stop':
  try:
   ret={}
   ret['ret']=DH(request)
   ret['remotes']=DY()
   ret['mounts']=DW()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='mount_remove':
  try:
   ret={}
   mount_id=Da['id']
   Dg(mount_id)
   ret['ret']=Dy(mount_id)
   ret['remotes']=DY()
   ret['mounts']=DW()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='load_serves':
  try:
   from.logic_serve import LogicServe
   ret={}
   ret['serves']=LogicServe.serve_list()
   ret['remotes']=DY()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='serve_save':
  try:
   from.logic_serve import LogicServe
   ret={}
   ret['ret']=LogicServe.serve_save(request)
   ret['remotes']=DY()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='serve_execute':
  try:
   from.logic_serve import LogicServe
   ret={}
   serve_id=Da['id']
   ret['ret']=LogicServe.serve_execute(serve_id)
   ret['remotes']=DY()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='serve_stop':
  try:
   from.logic_serve import LogicServe
   ret={}
   ret['ret']=LogicServe.serve_stop(request)
   ret['remotes']=DY()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
 elif sub=='serve_remove':
  try:
   from.logic_serve import LogicServe
   ret={}
   serve_id=Da['id']
   LogicServe.serve_kill(serve_id)
   ret['ret']=LogicServe.serve_remove(serve_id)
   ret['remotes']=DY()
   ret['serves']=LogicServe.serve_list()
   return jsonify(ret)
  except R as e:
   logger.error('Exception:%s',e)
   logger.error(F())
sid_list=[]
@Du('connect',namespace='/%s'%package_name)
def connect():
 try:
  logger.debug('socket_connect')
  sid_list.append(Db)
  tmp=v
  if Dd is not v:
   tmp=A(Dd,cls=AlchemyEncoder)
   tmp=DC(tmp)
  emit('on_connect',tmp,namespace='/%s'%package_name)
 except R as e:
  logger.error('Exception:%s',e)
  logger.error(F())
@Du('disconnect',namespace='/%s'%package_name)
def disconnect():
 try:
  sid_list.remove(Db)
  logger.debug('socket_disconnect')
 except R as e:
  logger.error('Exception:%s',e)
  logger.error(F())
def socketio_callback(cmd,data):
 if sid_list:
  tmp=A(data,cls=AlchemyEncoder)
  tmp=DC(tmp)
  DP(cmd,tmp,namespace='/%s'%package_name,broadcast=W)
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
