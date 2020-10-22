import os
u=None
B=True
Q=Exception
r=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=u,chat_id=u,image_url=u,disable_notification=u):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is u:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is u:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is u:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not u:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=B,disable_notification=disable_notification)
  return B
 except Q as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return r
# Created by pyminifier (https://github.com/liftoff/pyminifier)
