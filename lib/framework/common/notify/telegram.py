import os
L=None
R=True
M=Exception
z=False
import traceback
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
def send_telegram_message(text,bot_token=L,chat_id=L,image_url=L,disable_notification=L):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is L:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is L:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is L:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not L:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=R,disable_notification=disable_notification)
  return R
 except M as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
  logger.debug('Chatid:%s',chat_id)
 return z
# Created by pyminifier (https://github.com/liftoff/pyminifier)
