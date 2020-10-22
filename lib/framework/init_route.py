import os
R=True
i=False
J=Exception
k=os.path
import sys
from datetime import datetime,timedelta
import json
import traceback
O=traceback.format_exc
from flask import redirect,render_template,Response,request,jsonify,send_from_directory
F=request.remote_addr
I=request.headers
T=request.files
q=request.path
W=request.base_url
r=request.args
Y=request.form
j=request.method
from flask_login import login_user,logout_user,current_user,login_required
m=current_user.is_authenticated
from framework import app,db,version,USERS,login_manager,logger,path_data,check_api
B=logger.error
G=logger.debug
a=login_manager.user_loader
S=db.session
f=app.config
H=app.errorhandler
h=app.route
import system
K=system.SystemLogic
Oo=system.logic
X=system.ModelSetting
@h('/login',methods=['GET','POST'])
def login():
 if j=='POST':
  username=Y['username']
  password=Y['password']
  remember=(Y['remember']=='True')
  if username not in USERS:
   return jsonify('no_id')
  elif not USERS[username].can_login(password):
   return jsonify('wrong_password')
  else:
   USERS[username].authenticated=R
   login_user(USERS[username],remember=remember)
   return jsonify('redirect')
 else:
  if S.query(X).filter_by(key='use_login').first().value=='False':
   username=S.query(X).filter_by(key='id').first().value
   USERS[username].authenticated=R
   login_user(USERS[username],remember=R)
   return redirect(r.get("next"))
  return render_template('login.html',next=r.get("next"))
@H(401)
def custom_401(error):
 return 'login_required'
@a
def user_loader(user_id):
 return USERS[user_id]
@h('/logout',methods=['GET','POST'])
@login_required
def logout():
 user=current_user
 user.authenticated=i
 json_res={'ok':R,'msg':'user <%s> logout'%user.user_id}
 logout_user()
 return redirect('/login')
@h("/")
@h("/None")
@h("/home")
def home():
 return redirect('/system/home')
@h("/version")
def get_version():
 return version
@h("/open_file/<path:path>")
@login_required
def open_file(path):
 G('open_file :%s',path)
 return send_from_directory('',path)
@h("/file/<path:path>")
@check_api
def file2(path):
 G('file2 :%s',path)
 return send_from_directory('',path)
@h("/download_file/<path:path>")
@login_required
def download_file(path):
 G('download_file :%s',path)
 return send_from_directory('',path,as_attachment=R)
@h("/hls")
def hls_play():
 url=r.get('url')
 G('hls url : %s',url)
 return render_template('hls_player3.html',url=url)
@h("/iframe/<sub>")
@login_required
def iframe(sub):
 if sub=='forum':
  return render_template('iframe.html',site='https://soju6jan.com/sjva')
 elif sub=='file_manager':
  if f['config']['is_debug']or m:
   G(W)
   G(q)
   from Oo import SystemLogic
   site=SystemLogic.get_setting_value('ddns')+'/flaskfilemanager'
   G(site)
   return render_template('iframe.html',site=site)
  else:
   return redirect('/login?next='+q)
 elif sub=='file_manager2':
  if m:
   return redirect('/flaskfilemanager')
  else:
   return redirect('/login?next=/flaskfilemanager'+q)
@h("/upload",methods=['GET','POST'])
def upload():
 try:
  if j=='POST':
   f=T['file']
   from werkzeug import secure_filename
   tmp=secure_filename(f.filename)
   G('upload : %s',tmp)
   f.save(k.join(path_data,'upload',tmp))
   return jsonify('success')
 except J as e:
  B('Exception:%s',e)
  B(O())
  return jsonify('fail')
@h('/robots.txt')
def robot_to_root():
 return send_from_directory('','static/file/robots.txt')
@h('/static/<path:path>')
def rc():
 try:
  G('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
  G(path)
 except J as e:
  B('Exception:%s',e)
  B(O())
  return jsonify('fail')
@h('/get_ip')
def get_ip():
 if K.get_setting_value('ddns').find('soju6jan.com')!=-1:
  headers_list=I.getlist("X-Forwarded-For")
  user_ip=headers_list[0]if headers_list else F
  G('IIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPPPPPP : %s',user_ip)
  return jsonify(user_ip)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
