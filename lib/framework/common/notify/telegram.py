import os
w=None
Q=True
E=Exception
O=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=w,chat_id=w,image_url=w,disable_notification=w):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is w:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is w:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is w:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not w:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=Q,disable_notification=disable_notification)
  return Q
 except E as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return O
# Created by pyminifier (https://github.com/liftoff/pyminifier)
