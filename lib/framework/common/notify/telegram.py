import os
r=None
S=True
s=Exception
Q=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=r,chat_id=r,image_url=r,disable_notification=r):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is r:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is r:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is r:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not r:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=S,disable_notification=disable_notification)
  return S
 except s as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return Q
# Created by pyminifier (https://github.com/liftoff/pyminifier)
