import os
i=None
w=True
F=Exception
k=False
import traceback
n=traceback.format_exc
from telepot import Bot,glance
from telepot.loop import MessageLoop
from time import sleep
from framework.common.notify import logger
l=logger.debug
W=logger.error
def send_telegram_message(text,bot_token=i,chat_id=i,image_url=i,disable_notification=i):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if bot_token is i:
   bot_token=SystemModelSetting.get('notify_telegram_token')
  if chat_id is i:
   chat_id=SystemModelSetting.get('notify_telegram_chat_id')
  if disable_notification is i:
   disable_notification=SystemModelSetting.get_bool('notify_telegram_disable_notification')
  bot=Bot(bot_token)
  if image_url is not i:
   bot.sendPhoto(chat_id,image_url,disable_notification=disable_notification)
  bot.sendMessage(chat_id,text,disable_web_page_preview=w,disable_notification=disable_notification)
  return w
 except F as e:
  W('Exception:%s',e)
  W(n())
  l('Chatid:%s',chat_id)
 return k
# Created by pyminifier (https://github.com/liftoff/pyminifier)
