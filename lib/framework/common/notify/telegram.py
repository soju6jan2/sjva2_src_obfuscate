import os
Y=None
p=True
v=Exception
K=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=Y,chat_id=Y,image_url=Y,disable_notification=Y):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is Y:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is Y:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is Y:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not Y:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=p,disable_notification=disable_notification)
  return p
 except v as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return K
# Created by pyminifier (https://github.com/liftoff/pyminifier)
