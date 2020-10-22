import os
w=True
Q=False
d=Exception
import sys
from datetime import datetime,timedelta
import json
import traceback
from flask import redirect,render_template,Response,request,jsonify,send_from_directory
from flask_login import login_user,logout_user,current_user,login_required
from framework import app,db,version,USERS,login_manager,logger,path_data,check_api
import system
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  username=request.form['username']
  password=request.form['password']
  remember=(request.form['remember']=='True')
  if username not in USERS:
   return jsonify('no_id')
  elif not USERS[username].can_login(password):
   return jsonify('wrong_password')
  else:
   USERS[username].authenticated=w
   login_user(USERS[username],remember=remember)
   return jsonify('redirect')
 else:
  if db.session.query(system.ModelSetting).filter_by(key='use_login').first().value=='False':
   username=db.session.query(system.ModelSetting).filter_by(key='id').first().value
   USERS[username].authenticated=w
   login_user(USERS[username],remember=w)
   return redirect(request.args.get("next"))
  return render_template('login.html',next=request.args.get("next"))
@app.errorhandler(401)
def custom_401(error):
 return 'login_required'
@login_manager.user_loader
def user_loader(user_id):
 return USERS[user_id]
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
 user=current_user
 user.authenticated=Q
 json_res={'ok':w,'msg':'user <%s> logout'%user.user_id}
 logout_user()
 return redirect('/login')
@app.route("/")
@app.route("/None")
@app.route("/home")
def home():
 return redirect('/system/home')
@app.route("/version")
def get_version():
 return version
@app.route("/open_file/<path:path>")
@login_required
def open_file(path):
 logger.debug('open_file :%s',path)
 return send_from_directory('',path)
@app.route("/file/<path:path>")
@check_api
def file2(path):
 logger.debug('file2 :%s',path)
 return send_from_directory('',path)
@app.route("/download_file/<path:path>")
@login_required
def download_file(path):
 logger.debug('download_file :%s',path)
 return send_from_directory('',path,as_attachment=w)
@app.route("/hls")
def hls_play():
 url=request.args.get('url')
 logger.debug('hls url : %s',url)
 return render_template('hls_player3.html',url=url)
@app.route("/iframe/<sub>")
@login_required
def iframe(sub):
 if sub=='forum':
  return render_template('iframe.html',site='https://soju6jan.com/sjva')
 elif sub=='file_manager':
  if app.config['config']['is_debug']or current_user.is_authenticated:
   logger.debug(request.base_url)
   logger.debug(request.path)
   from system.logic import SystemLogic
   site=SystemLogic.get_setting_value('ddns')+'/flaskfilemanager'
   logger.debug(site)
   return render_template('iframe.html',site=site)
  else:
   return redirect('/login?next='+request.path)
 elif sub=='file_manager2':
  if current_user.is_authenticated:
   return redirect('/flaskfilemanager')
  else:
   return redirect('/login?next=/flaskfilemanager'+request.path)
@app.route("/upload",methods=['GET','POST'])
def upload():
 try:
  if request.method=='POST':
   f=request.files['file']
   from werkzeug import secure_filename
   tmp=secure_filename(f.filename)
   logger.debug('upload : %s',tmp)
   f.save(os.path.join(path_data,'upload',tmp))
   return jsonify('success')
 except d as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
  return jsonify('fail')
@app.route('/robots.txt')
def robot_to_root():
 return send_from_directory('','static/file/robots.txt')
@app.route('/static/<path:path>')
def rc():
 try:
  logger.debug('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
  logger.debug(path)
 except d as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
  return jsonify('fail')
@app.route('/get_ip')
def get_ip():
 if system.SystemLogic.get_setting_value('ddns').find('soju6jan.com')!=-1:
  headers_list=request.headers.getlist("X-Forwarded-For")
  user_ip=headers_list[0]if headers_list else request.remote_addr
  logger.debug('IIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPPPPPP : %s',user_ip)
  return jsonify(user_ip)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
