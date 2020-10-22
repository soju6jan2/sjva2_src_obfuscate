import os
c=object
v=None
S=staticmethod
D=Exception
y=str
a=getattr
G=ImportError
R=True
N=len
t=enumerate
E=False
import traceback
import json
import datetime
import time
from telepot import Bot,glance
from telepot.loop import MessageLoop
from framework import app
from framework.common.telegram_bot import logger
from framework.common.util import AESCipher
from system.model import ModelSetting as SystemModelSetting
class TelegramBot(c):
 bot=v
 message_loop=v
 SUPER_TOKEN='817624975:AAH4zRESDTWwYL4xmmks-ohl9LkC3qYiWV0'
 SUPER_BOT=v
 SJVA_BOT_CHANNEL_CHAT_ID=['-1001424350090','-1001290967798','-1001428878939','-1001478260118','-1001276582768','-1001287732044','-1001185127926','-1001236433271','-1001241700529','-1001231080344','-1001176084443','-1001338380585','-1001107581425','-1001374760690','-1001195790611','-1001239823262','-1001300536937','-1001417416651','-1001411726438','-1001312832402','-1001473554220','-1001214198736','-1001366983815','-1001336003806','-1001229313654','-1001403657137','-1001368328507','-1001197617982','-1001256559181','-1001202840141']
 @S
 def start(bot_token):
  try:
   if TelegramBot.message_loop is v:
    TelegramBot.bot=Bot(bot_token)
    me=TelegramBot.bot.getMe()
    logger.debug('TelegramBot bot : %s',me)
    TelegramBot.message_loop=MessageLoop(TelegramBot.bot,TelegramBot.receive_callback)
    TelegramBot.message_loop.run_as_thread()
    import framework.common.notify as Notify
    Notify.send_message('텔레그램 메시지 수신을 시작합니다. %s'%(datetime.datetime.now()))
    TelegramBot.SUPER_BOT=Bot(TelegramBot.SUPER_TOKEN)
    if SystemModelSetting.get('ddns')=='https://sjva-server.soju6jan.com':
     MessageLoop(TelegramBot.SUPER_BOT,TelegramBot.super_receive_callback).run_as_thread()
     pass
    while TelegramBot.message_loop is not v:
     time.sleep(60*60)
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @S
 def receive_callback(msg):
  try:
   content_type,chat_type,chat_id=glance(msg)
   try:
    if content_type=='text' and msg['text'][0]=='^':
     if SystemModelSetting.get_bool('telegram_resend'):
      chat_list=SystemModelSetting.get_list('telegram_resend_chat_id')
      if y(chat_id)not in chat_list:
       for c in chat_list:
        import framework.common.notify as Notify
        Notify.send_telegram_message(msg['text'],SystemModelSetting.get('telegram_bot_token'),chat_id=c)
   except D as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc())
   if content_type=='text':
    text=msg['text']
    if msg['text']=='/bot':
     text=json.dumps(TelegramBot.bot.getMe(),indent=2)
     TelegramBot.bot.sendMessage(chat_id,text)
    elif msg['text']=='/me':
     text=json.dumps(msg,indent=2)
     TelegramBot.bot.sendMessage(chat_id,text)
    elif msg['text'][0]=='^':
     TelegramBot.process_receive_data(msg['text'][1:])
    elif msg['text']=='/call':
     data=TelegramBot.bot.getMe()
     from framework import version
     text='call : %s / %s / %s / %s / %s / %s'%(data['username'],data['id'],data['first_name'],version,SystemModelSetting.get('sjva_me_user_id'),SystemModelSetting.get('sjva_id'))
     TelegramBot.bot.sendMessage(chat_id,text)
    elif msg['text'].startswith('call'):
     logger.debug(msg['text'])
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @S
 def process_receive_data(text):
  try:
   text=AESCipher.decrypt(text)
   data=json.loads(text)
   msg=text
   if 'plugin' in data:
    try:
     plugin_name=data['plugin']
     target=v
     if 'policy_level' in data:
      logger.debug(data)
      if data['policy_level']>app.config['config']['level']:
       return
     if 'target' in data:
      target=data['target']
     mod=__import__('%s'%(plugin_name),fromlist=[])
     mod_process_telegram_data=a(mod,'process_telegram_data')
     if mod_process_telegram_data:
      try:
       mod.process_telegram_data(data['data'],target=target)
      except:
       mod.process_telegram_data(data['data'])
     return
    except G:
     pass
    except D as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc())
    return
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @S
 def super_receive_callback(msg):
  try:
   content_type,chat_type,chat_id=glance(msg)
   logger.debug('super content_type:%s chat_type:%s chat_id:%s',content_type,chat_type,chat_id)
   if content_type=='text':
    text=msg['text']
    if 'from' not in msg:
     return
    user_id=msg['from']['id']
    if msg['text']=='/add':
     logger.debug('user_id:%s',user_id)
     try:
      name=msg['from']['first_name']
     except D as exception:
      name=''
     try:
      TelegramBot.SUPER_BOT.promoteChatMember(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID[-1],user_id,can_post_messages=R,can_invite_users=R,can_promote_members=R)
      text='%s님을 SJVA Bot Group 채널에 관리자로 추가하였습니다.\n채널에서 봇을 추가하시고 나가주세요.'%name
     except D as exception:
      logger.error('Exception:%s',exception)
      logger.error(traceback.format_exc())
      text='%s님이 봇 채널에 입장해 있지 않은 것 같습니다.\n%s'%(name,'https://t.me/sjva_bot_channel')
     TelegramBot.SUPER_BOT.sendMessage(chat_id,text)
    elif msg['text'].startswith('/where'):
     try:
      tmp=msg['text'].split(' ')
      logger.debug(tmp)
      if N(tmp)==2:
       user_id=tmp[1]
       logger.debug('/where : %s',user_id)
       data=v
       text='입장한 방이 없습니다.'
       for idx,c in t(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID):
        try:
         data=TelegramBot.SUPER_BOT.getChatMember(c,user_id)
         if data is not v:
          if data['status']=='administrator':
           logger.debug('getChatMemner result : %s',data)
           text=json.dumps(data,indent=2)+'\n'+'%s번 방에 있습니다. 32번=%s, 33번=%s'%((idx+1),N(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID)-1,N(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID))
           break
        except D as exception:
         logger.error('Exception:%s',exception)
         logger.error(traceback.format_exc())
      else:
       text='/where 봇ID(숫자형식) 를 입력하세요.'
      TelegramBot.SUPER_BOT.sendMessage(chat_id,text)
     except D as exception:
      logger.error('Exception:%s',exception)
      logger.error(traceback.format_exc())
      TelegramBot.SUPER_BOT.sendMessage(chat_id,y(e)) 
    else:
     text='Your ID : %s'%(user_id)
     TelegramBot.SUPER_BOT.sendMessage(chat_id,text)
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @S
 def super_send_message(text,encryped=R,only_last=E):
  try:
   if TelegramBot.SUPER_BOT is v:
    TelegramBot.SUPER_BOT=Bot(TelegramBot.SUPER_TOKEN)
   if encryped:
    text='^'+AESCipher.encrypt(text)
   if only_last:
    TelegramBot.SUPER_BOT.sendMessage(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID[-1],text)
   else:
    for c_id in TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID:
     try:
      TelegramBot.SUPER_BOT.sendMessage(c_id,text)
     except D as exception:
      logger.error('Exception:%s',exception)
      logger.error('Chat ID : %s',c_id)
      logger.error(traceback.format_exc()) 
   return R
  except D as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return E
# Created by pyminifier (https://github.com/liftoff/pyminifier)
