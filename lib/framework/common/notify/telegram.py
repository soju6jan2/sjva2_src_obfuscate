import os
d=None
k=True
Q=Exception
o=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=d,chat_id=d,image_url=d,disable_notification=d):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is d:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is d:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is d:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not d:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=k,disable_notification=disable_notification)
  return k
 except Q as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return o
# Created by pyminifier (https://github.com/liftoff/pyminifier)
