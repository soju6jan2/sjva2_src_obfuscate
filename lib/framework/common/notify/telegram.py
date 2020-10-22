import os
G=None
K=True
v=Exception
a=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=G,chat_id=G,image_url=G,disable_notification=G):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is G:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is G:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is G:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not G:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=K,disable_notification=disable_notification)
  return K
 except v as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return a
# Created by pyminifier (https://github.com/liftoff/pyminifier)
