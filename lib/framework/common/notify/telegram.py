import os
W=None
u=True
J=Exception
Y=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=W,chat_id=W,image_url=W,disable_notification=W):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is W:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is W:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is W:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not W:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=u,disable_notification=disable_notification)
  return u
 except J as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return Y
# Created by pyminifier (https://github.com/liftoff/pyminifier)
