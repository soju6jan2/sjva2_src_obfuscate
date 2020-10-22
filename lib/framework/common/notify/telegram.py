import os
q=None
h=True
R=Exception
D=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=q,chat_id=q,image_url=q,disable_notification=q):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is q:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is q:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is q:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not q:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=h,disable_notification=disable_notification)
  return h
 except R as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return D
# Created by pyminifier (https://github.com/liftoff/pyminifier)
