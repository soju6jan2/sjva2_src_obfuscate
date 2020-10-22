import os
K=None
o=True
O=Exception
g=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=K,chat_id=K,image_url=K,disable_notification=K):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is K:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is K:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is K:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not K:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=o,disable_notification=disable_notification)
  return o
 except O as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return g
# Created by pyminifier (https://github.com/liftoff/pyminifier)
