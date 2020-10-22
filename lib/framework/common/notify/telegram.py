import os
s=None
N=True
f=Exception
o=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=s,chat_id=s,image_url=s,disable_notification=s):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is s:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is s:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is s:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not s:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=N,disable_notification=disable_notification)
  return N
 except f as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return o
# Created by pyminifier (https://github.com/liftoff/pyminifier)
