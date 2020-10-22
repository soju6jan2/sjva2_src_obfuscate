import os
v=None
Y=True
l=Exception
F=False
import traceback
R=traceback.format_exc
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
N=logger.debug
r=logger.error
def send_telegram_message(text,bot_token=v,chat_id=v,image_url=v,disable_notification=v):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is v:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is v:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is v:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not v:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=Y,disable_notification=disable_notification)
  return Y
 except l as e:
  r('Exception:%s',e)
  r(R())
  N('Chatid:%s',chat_id)
 return F
# Created by pyminifier (https://github.com/liftoff/pyminifier)
