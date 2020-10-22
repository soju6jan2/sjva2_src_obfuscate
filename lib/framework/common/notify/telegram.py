import os
Q=None
A=True
s=Exception
l=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=Q,chat_id=Q,image_url=Q,disable_notification=Q):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is Q:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is Q:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is Q:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not Q:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=A,disable_notification=disable_notification)
  return A
 except s as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return l
# Created by pyminifier (https://github.com/liftoff/pyminifier)
