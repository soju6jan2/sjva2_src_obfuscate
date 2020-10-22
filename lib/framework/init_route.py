import os
f=True
Y=False
P=Exception
b=os.path
import sys
from datetime import datetime,timedelta
import json
import traceback
t=traceback.format_exc
from flask import redirect,render_template,Response,request,jsonify,send_from_directory
v=request.remote_addr
W=request.headers
K=request.files
p=request.path
Q=request.base_url
J=request.args
U=request.form
O=request.method
from flask_login import login_user,logout_user,current_user,login_required
y=current_user.is_authenticated
from framework import app,db,version,USERS,login_manager,logger,path_data,check_api
o=logger.error
M=logger.debug
c=login_manager.user_loader
w=db.session
e=app.config
A=app.errorhandler
a=app.route
import system
n=system.SystemLogic
tS=system.logic
H=system.ModelSetting
@a('/login',methods=['GET','POST'])
def login():
 if O=='POST':
  username=U['username']
  password=U['password']
  remember=(U['remember']=='True')
  if username not in USERS:
   return jsonify('no_id')
  elif not USERS[username].can_login(password):
   return jsonify('wrong_password')
  else:
   USERS[username].authenticated=f
   login_user(USERS[username],remember=remember)
   return jsonify('redirect')
 else:
  if w.query(H).filter_by(key='use_login').first().value=='False':
   username=w.query(H).filter_by(key='id').first().value
   USERS[username].authenticated=f
   login_user(USERS[username],remember=f)
   return redirect(J.get("next"))
  return render_template('login.html',next=J.get("next"))
@A(401)
def custom_401(error):
 return 'login_required'
@c
def user_loader(user_id):
 return USERS[user_id]
@a('/logout',methods=['GET','POST'])
@login_required
def logout():
 user=current_user
 user.authenticated=Y
 json_res={'ok':f,'msg':'user <%s> logout'%user.user_id}
 logout_user()
 return redirect('/login')
@a("/")
@a("/None")
@a("/home")
def home():
 return redirect('/system/home')
@a("/version")
def get_version():
 return version
@a("/open_file/<path:path>")
@login_required
def open_file(path):
 M('open_file :%s',path)
 return send_from_directory('',path)
@a("/file/<path:path>")
@check_api
def file2(path):
 M('file2 :%s',path)
 return send_from_directory('',path)
@a("/download_file/<path:path>")
@login_required
def download_file(path):
 M('download_file :%s',path)
 return send_from_directory('',path,as_attachment=f)
@a("/hls")
def hls_play():
 url=J.get('url')
 M('hls url : %s',url)
 return render_template('hls_player3.html',url=url)
@a("/iframe/<sub>")
@login_required
def iframe(sub):
 if sub=='forum':
  return render_template('iframe.html',site='https://soju6jan.com/sjva')
 elif sub=='file_manager':
  if e['config']['is_debug']or y:
   M(Q)
   M(p)
   from tS import SystemLogic
   site=SystemLogic.get_setting_value('ddns')+'/flaskfilemanager'
   M(site)
   return render_template('iframe.html',site=site)
  else:
   return redirect('/login?next='+p)
 elif sub=='file_manager2':
  if y:
   return redirect('/flaskfilemanager')
  else:
   return redirect('/login?next=/flaskfilemanager'+p)
@a("/upload",methods=['GET','POST'])
def upload():
 try:
  if O=='POST':
   f=K['file']
   from werkzeug import secure_filename
   tmp=secure_filename(f.filename)
   M('upload : %s',tmp)
   f.save(b.join(path_data,'upload',tmp))
   return jsonify('success')
 except P as e:
  o('Exception:%s',e)
  o(t())
  return jsonify('fail')
@a('/robots.txt')
def robot_to_root():
 return send_from_directory('','static/file/robots.txt')
@a('/static/<path:path>')
def rc():
 try:
  M('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
  M(path)
 except P as e:
  o('Exception:%s',e)
  o(t())
  return jsonify('fail')
@a('/get_ip')
def get_ip():
 if n.get_setting_value('ddns').find('soju6jan.com')!=-1:
  headers_list=W.getlist("X-Forwarded-For")
  user_ip=headers_list[0]if headers_list else v
  M('IIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPPPPPP : %s',user_ip)
  return jsonify(user_ip)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
