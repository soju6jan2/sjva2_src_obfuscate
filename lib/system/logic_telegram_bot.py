import os
I=object
h=staticmethod
j=Exception
C=False
import traceback
V=traceback.format_exc
import logging
import platform
import time
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
Vg=request.form
from framework.logger import get_logger
from framework import app,path_app_root,path_data,scheduler
U=scheduler.add_job_instance
A=app.config
from framework.job import Job
import framework.common.notify as Notify
from.plugin import logger,package_name
D=logger.error
o=logger.debug
from.model import ModelSetting
w=ModelSetting.get
VH=ModelSetting.get_bool
class SystemLogicTelegramBot(I):
 @h
 def process_ajax(sub,req):
  try:
   if sub=='telegram_test':
    ret=Notify.send_telegram_message(req.form['text'],bot_token=req.form['bot_token'],chat_id=req.form['chat_id'])
    return jsonify(ret)
   elif sub=='discord_test':
    ret=Notify.send_discord_message(req.form['text'],webhook_url=req.form['url'])
    return jsonify(ret)
   elif sub=='advanced_test':
    ret=Notify.send_advanced_message(req.form['text'],policy=req.form['policy'],message_id=req.form['message_id'])
    return jsonify(ret)
   elif sub=='scheduler':
    go=Vg['scheduler']
    o('scheduler :%s',go)
    if go=='true':
     SystemLogicTelegramBot.scheduler_start()
    else:
     SystemLogicTelegramBot.scheduler_stop()
    return jsonify(go)
  except j as e:
   D('Exception:%s',e)
   D(V())
   return jsonify('exception')
 @h
 def plugin_load():
  try:
   if A['config']['run_by_worker']:
    return
   if VH('telegram_bot_auto_start'):
    SystemLogicTelegramBot.scheduler_start()
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def scheduler_start():
  try:
   interval=60*24
   job=Job(package_name,'%s_telegram_bot'%(package_name),9999,SystemLogicTelegramBot.scheduler_function,u"시스템 - 텔레그램 봇",C)
   U(job)
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def scheduler_function():
  try:
   bot_token=w('telegram_bot_token')
   from framework.common.telegram_bot import TelegramBot
   TelegramBot.start(bot_token)
  except j as e:
   D('Exception:%s',e)
   D(V())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
