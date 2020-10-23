import os
y=None
L=True
s=Exception
A=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=y,chat_id=y,image_url=y,disable_notification=y):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is y:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is y:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is y:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not y:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=L,disable_notification=disable_notification)
  return L
 except s as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return A
# Created by pyminifier (https://github.com/liftoff/pyminifier)
