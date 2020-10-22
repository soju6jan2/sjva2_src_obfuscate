import os
k=None
c=True
z=Exception
x=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=k,chat_id=k,image_url=k,disable_notification=k):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is k:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is k:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is k:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not k:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=c,disable_notification=disable_notification)
  return c
 except z as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return x
# Created by pyminifier (https://github.com/liftoff/pyminifier)
