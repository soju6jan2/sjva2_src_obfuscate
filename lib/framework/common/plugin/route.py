import traceback
Q=None
U=Exception
x=True
I=traceback.format_exc
import json
f=json.loads
j=json.dumps
from flask import Blueprint,request,render_template,redirect,jsonify
k=request.sid
g=request.form
from flask_login import login_required
from flask_socketio import SocketIO,emit,send
from framework import socketio,check_api
E=socketio.emit
V=socketio.on
from framework.util import AlchemyEncoder
def default_route(P):
 @P.blueprint.route('/')
 def home():
  if P.ModelSetting is not Q:
   tmp=P.ModelSetting.get('recent_menu_plugin')
   if tmp is not Q and tmp!='':
    tmps=tmp.split('|')
    return redirect('/{package_name}/{sub}/{sub2}'.format(package_name=P.package_name,sub=tmps[0],sub2=tmps[1]))
  return redirect('/{package_name}/{home_module}'.format(package_name=P.package_name,home_module=P.home_module))
 @P.blueprint.route('/<sub>',methods=['GET','POST'])
 @login_required
 def first_menu(sub):
  try:
   for module in P.module_list:
    if sub==module.name:
     return redirect('/{package_name}/{sub}/{first_menu}'.format(package_name=P.package_name,sub=sub,first_menu=module.get_first_menu()))
   if sub=='log':
    return render_template('log.html',package=P.package_name)
   return render_template('sample.html',title='%s - %s'%(P.package_name,sub))
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
 @P.blueprint.route('/<sub>/<sub2>',methods=['GET','POST'])
 @login_required
 def second_menu(sub,sub2):
  if P.ModelSetting is not Q:
   P.ModelSetting.set('recent_menu_plugin','{}|{}'.format(sub,sub2))
  try:
   for module in P.module_list:
    if sub==module.name:
     return module.process_menu(sub2,request)
   if sub=='log':
    return render_template('log.html',package=P.package_name)
   return render_template('sample.html',title='%s - %s'%(P.package_name,sub))
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
 @P.blueprint.route('/ajax/<sub>',methods=['GET','POST'])
 @login_required
 def ajax(sub):
  P.logger.debug('AJAX %s %s',P.package_name,sub)
  try:
   if sub=='setting_save':
    ret=P.ModelSetting.setting_save(request)
    for module in P.module_list:
     module.setting_save_after()
    return jsonify(ret)
   elif sub=='scheduler':
    sub=g['sub']
    go=g['scheduler']
    P.logger.debug('scheduler :%s',go)
    if go=='true':
     P.logic.scheduler_start(sub)
    else:
     P.logic.scheduler_stop(sub)
    return jsonify(go)
   elif sub=='reset_db':
    sub=g['sub']
    ret=P.logic.reset_db(sub)
    return jsonify(ret)
   elif sub=='one_execute':
    sub=g['sub']
    ret=P.logic.one_execute(sub)
    return jsonify(ret)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I()) 
 @P.blueprint.route('/ajax/<sub>/<sub2>',methods=['GET','POST'])
 @login_required
 def second_ajax(sub,sub2):
  try:
   for module in P.module_list:
    if sub==module.name:
     return module.process_ajax(sub2,request)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
 @P.blueprint.route('/api/<sub>/<sub2>',methods=['GET','POST'])
 @check_api
 def api(sub,sub2):
  try:
   for module in P.module_list:
    if sub==module.name:
     return module.process_api(sub2,request)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
 @P.blueprint.route('/normal/<sub>/<sub2>',methods=['GET','POST'])
 def normal(sub,sub2):
  try:
   for module in P.module_list:
    if sub==module.name:
     return module.process_normal(sub2,request)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
def default_route_single_module(P):
 @P.blueprint.route('/')
 def home():
  return redirect('/{package_name}/{home_module}'.format(package_name=P.package_name,home_module=P.home_module))
 @P.blueprint.route('/<sub>',methods=['GET','POST'])
 @login_required
 def first_menu(sub):
  if sub=='log':
   return render_template('log.html',package=P.package_name)
  return P.module_list[0].process_menu(sub,request)
 @P.blueprint.route('/ajax/<sub>',methods=['GET','POST'])
 @login_required
 def ajax(sub):
  P.logger.debug('AJAX %s %s',P.package_name,sub)
  try:
   if sub=='setting_save':
    ret=P.ModelSetting.setting_save(request)
    P.module_list[0].setting_save_after()
    return jsonify(ret)
   elif sub=='scheduler':
    sub=g['sub']
    go=g['scheduler']
    P.logger.debug('scheduler :%s',go)
    if go=='true':
     P.logic.scheduler_start(sub)
    else:
     P.logic.scheduler_stop(sub)
    return jsonify(go)
   elif sub=='reset_db':
    sub=g['sub']
    ret=P.logic.reset_db(sub)
    return jsonify(ret)
   elif sub=='one_execute':
    sub=g['sub']
    ret=P.logic.one_execute(sub)
    return jsonify(ret)
   else:
    return P.module_list[0].process_ajax(sub,request)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I()) 
 @P.blueprint.route('/api/<sub>',methods=['GET','POST'])
 @check_api
 def api(sub):
  try:
   return P.module_list[0].process_api(sub,request)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
 @P.blueprint.route('/normal/<sub>',methods=['GET','POST'])
 def normal(sub):
  try:
   return P.module_list[0].process_normal(sub,request)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I()) 
def default_route_socketio(P,instance):
 if instance.socketio_list is Q:
  instance.socketio_list=[]
 @V('connect',namespace='/{package_name}/{sub}'.format(package_name=P.package_name,sub=instance.name))
 def connect():
  try:
   P.logger.debug('socket_connect : %s - %s',P.package_name,instance.name)
   instance.socketio_list.append(k)
   socketio_callback('start','')
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
 @V('disconnect',namespace='/{package_name}/{sub}'.format(package_name=P.package_name,sub=instance.name))
 def disconnect():
  try:
   P.logger.debug('socket_disconnect : %s - %s',P.package_name,instance.name)
   instance.socketio_list.remove(k)
  except U as e:
   P.logger.error('Exception:%s',e)
   P.logger.error(I())
 def socketio_callback(cmd,data,encoding=x):
  if instance.socketio_list:
   if encoding:
    data=j(data,cls=AlchemyEncoder)
    data=f(data)
   E(cmd,data,namespace='/{package_name}/{sub}'.format(package_name=P.package_name,sub=instance.name),broadcast=x)
 instance.socketio_callback=socketio_callback
# Created by pyminifier (https://github.com/liftoff/pyminifier)
