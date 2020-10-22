import os
L=object
N=staticmethod
e=Exception
j=False
import traceback
H=traceback.format_exc
import logging
import platform
import time
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
HE=request.form
from framework.logger import get_logger
from framework import app,path_app_root,path_data,scheduler
K=scheduler.add_job_instance
X=app.config
from framework.job import Job
import framework.common.notify as Notify
from.plugin import logger,package_name
J=logger.error
G=logger.debug
from.model import ModelSetting
I=ModelSetting.get
HQ=ModelSetting.get_bool
class SystemLogicTelegramBot(L):
 @N
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
    go=HE['scheduler']
    G('scheduler :%s',go)
    if go=='true':
     SystemLogicTelegramBot.scheduler_start()
    else:
     SystemLogicTelegramBot.scheduler_stop()
    return jsonify(go)
  except e as e:
   J('Exception:%s',e)
   J(H())
   return jsonify('exception')
 @N
 def plugin_load():
  try:
   if X['config']['run_by_worker']:
    return
   if HQ('telegram_bot_auto_start'):
    SystemLogicTelegramBot.scheduler_start()
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def scheduler_start():
  try:
   interval=60*24
   job=Job(package_name,'%s_telegram_bot'%(package_name),9999,SystemLogicTelegramBot.scheduler_function,u"시스템 - 텔레그램 봇",j)
   K(job)
  except e as e:
   J('Exception:%s',e)
   J(H())
 @N
 def scheduler_function():
  try:
   bot_token=I('telegram_bot_token')
   from framework.common.telegram_bot import TelegramBot
   TelegramBot.start(bot_token)
  except e as e:
   J('Exception:%s',e)
   J(H())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
