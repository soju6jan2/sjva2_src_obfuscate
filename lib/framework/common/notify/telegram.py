import os
z=None
Q=True
R=Exception
O=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=z,chat_id=z,image_url=z,disable_notification=z):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is z:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is z:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is z:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not z:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=Q,disable_notification=disable_notification)
  return Q
 except R as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return O
# Created by pyminifier (https://github.com/liftoff/pyminifier)
