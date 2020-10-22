import os
U=None
x=True
j=Exception
S=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=U,chat_id=U,image_url=U,disable_notification=U):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is U:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is U:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is U:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not U:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=x,disable_notification=disable_notification)
  return x
 except j as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return S
# Created by pyminifier (https://github.com/liftoff/pyminifier)
