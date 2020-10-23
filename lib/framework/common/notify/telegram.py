import os
f=None
n=True
T=Exception
k=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=f,chat_id=f,image_url=f,disable_notification=f):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is f:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is f:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is f:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not f:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=n,disable_notification=disable_notification)
  return n
 except T as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return k
# Created by pyminifier (https://github.com/liftoff/pyminifier)
