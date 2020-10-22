import os
D=object
B=None
T=staticmethod
a=Exception
r=str
J=getattr
G=ImportError
N=True
o=len
q=enumerate
y=False
import traceback
c=traceback.format_exc
import json
M=json.loads
Q=json.dumps
import datetime
m=datetime.now
k=datetime.datetime
import time
V=time.sleep
from telepot import Bot,glance
from telepot.loop import MessageLoop
from framework import app
v=app.config
from framework.common.telegram_bot import logger
l=logger.error
b=logger.debug
from framework.common.util import AESCipher
s=AESCipher.encrypt
F=AESCipher.decrypt
from system.model import ModelSetting as SystemModelSetting
K=SystemModelSetting.get_list
X=SystemModelSetting.get_bool
W=SystemModelSetting.get
class TelegramBot(D):
 bot=B
 message_loop=B
 SUPER_TOKEN='817624975:AAH4zRESDTWwYL4xmmks-ohl9LkC3qYiWV0'
 SUPER_BOT=B
 SJVA_BOT_CHANNEL_CHAT_ID=['-1001424350090','-1001290967798','-1001428878939','-1001478260118','-1001276582768','-1001287732044','-1001185127926','-1001236433271','-1001241700529','-1001231080344','-1001176084443','-1001338380585','-1001107581425','-1001374760690','-1001195790611','-1001239823262','-1001300536937','-1001417416651','-1001411726438','-1001312832402','-1001473554220','-1001214198736','-1001366983815','-1001336003806','-1001229313654','-1001403657137','-1001368328507','-1001197617982','-1001256559181','-1001202840141']
 @T
 def start(bot_token):
  try:
   if TelegramBot.message_loop is B:
    TelegramBot.bot=Bot(bot_token)
    me=TelegramBot.bot.getMe()
    b('TelegramBot bot : %s',me)
    TelegramBot.message_loop=MessageLoop(TelegramBot.bot,TelegramBot.receive_callback)
    TelegramBot.message_loop.run_as_thread()
    import framework.common.notify as Notify
    Notify.send_message('텔레그램 메시지 수신을 시작합니다. %s'%(k.now()))
    TelegramBot.SUPER_BOT=Bot(TelegramBot.SUPER_TOKEN)
    if W('ddns')=='https://sjva-server.soju6jan.com':
     MessageLoop(TelegramBot.SUPER_BOT,TelegramBot.super_receive_callback).run_as_thread()
     pass
    while TelegramBot.message_loop is not B:
     V(60*60)
  except a as e:
   l('Exception:%s',e)
   l(c())
 @T
 def receive_callback(msg):
  try:
   content_type,chat_type,chat_id=glance(msg)
   try:
    if content_type=='text' and msg['text'][0]=='^':
     if X('telegram_resend'):
      chat_list=K('telegram_resend_chat_id')
      if r(chat_id)not in chat_list:
       for c in chat_list:
        import framework.common.notify as Notify
        Notify.send_telegram_message(msg['text'],W('telegram_bot_token'),chat_id=c)
   except a as e:
    l('Exception:%s',e)
    l(c())
   if content_type=='text':
    text=msg['text']
    if msg['text']=='/bot':
     text=Q(TelegramBot.bot.getMe(),indent=2)
     TelegramBot.bot.sendMessage(chat_id,text)
    elif msg['text']=='/me':
     text=Q(msg,indent=2)
     TelegramBot.bot.sendMessage(chat_id,text)
    elif msg['text'][0]=='^':
     TelegramBot.process_receive_data(msg['text'][1:])
    elif msg['text']=='/call':
     data=TelegramBot.bot.getMe()
     from framework import version
     text='call : %s / %s / %s / %s / %s / %s'%(data['username'],data['id'],data['first_name'],version,W('sjva_me_user_id'),W('sjva_id'))
     TelegramBot.bot.sendMessage(chat_id,text)
    elif msg['text'].startswith('call'):
     b(msg['text'])
  except a as e:
   l('Exception:%s',e)
   l(c())
 @T
 def process_receive_data(text):
  try:
   text=F(text)
   data=M(text)
   msg=text
   if 'plugin' in data:
    try:
     plugin_name=data['plugin']
     target=B
     if 'policy_level' in data:
      b(data)
      if data['policy_level']>v['config']['level']:
       return
     if 'target' in data:
      target=data['target']
     mod=__import__('%s'%(plugin_name),fromlist=[])
     mod_process_telegram_data=J(mod,'process_telegram_data')
     if mod_process_telegram_data:
      try:
       mod.process_telegram_data(data['data'],target=target)
      except:
       mod.process_telegram_data(data['data'])
     return
    except G:
     pass
    except a as e:
     l('Exception:%s',e)
     l(c())
    return
  except a as e:
   l('Exception:%s',e)
   l(c())
 @T
 def super_receive_callback(msg):
  try:
   content_type,chat_type,chat_id=glance(msg)
   b('super content_type:%s chat_type:%s chat_id:%s',content_type,chat_type,chat_id)
   if content_type=='text':
    text=msg['text']
    if 'from' not in msg:
     return
    user_id=msg['from']['id']
    if msg['text']=='/add':
     b('user_id:%s',user_id)
     try:
      name=msg['from']['first_name']
     except a as e:
      name=''
     try:
      TelegramBot.SUPER_BOT.promoteChatMember(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID[-1],user_id,can_post_messages=N,can_invite_users=N,can_promote_members=N)
      text='%s님을 SJVA Bot Group 채널에 관리자로 추가하였습니다.\n채널에서 봇을 추가하시고 나가주세요.'%name
     except a as e:
      l('Exception:%s',e)
      l(c())
      text='%s님이 봇 채널에 입장해 있지 않은 것 같습니다.\n%s'%(name,'https://t.me/sjva_bot_channel')
     TelegramBot.SUPER_BOT.sendMessage(chat_id,text)
    elif msg['text'].startswith('/where'):
     try:
      tmp=msg['text'].split(' ')
      b(tmp)
      if o(tmp)==2:
       user_id=tmp[1]
       b('/where : %s',user_id)
       data=B
       text='입장한 방이 없습니다.'
       for idx,c in q(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID):
        try:
         data=TelegramBot.SUPER_BOT.getChatMember(c,user_id)
         if data is not B:
          if data['status']=='administrator':
           b('getChatMemner result : %s',data)
           text=Q(data,indent=2)+'\n'+'%s번 방에 있습니다. 32번=%s, 33번=%s'%((idx+1),o(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID)-1,o(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID))
           break
        except a as e:
         l('Exception:%s',e)
         l(c())
      else:
       text='/where 봇ID(숫자형식) 를 입력하세요.'
      TelegramBot.SUPER_BOT.sendMessage(chat_id,text)
     except a as e:
      l('Exception:%s',e)
      l(c())
      TelegramBot.SUPER_BOT.sendMessage(chat_id,r(e)) 
    else:
     text='Your ID : %s'%(user_id)
     TelegramBot.SUPER_BOT.sendMessage(chat_id,text)
  except a as e:
   l('Exception:%s',e)
   l(c())
 @T
 def super_send_message(text,encryped=N,only_last=y):
  try:
   if TelegramBot.SUPER_BOT is B:
    TelegramBot.SUPER_BOT=Bot(TelegramBot.SUPER_TOKEN)
   if encryped:
    text='^'+s(text)
   if only_last:
    TelegramBot.SUPER_BOT.sendMessage(TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID[-1],text)
   else:
    for c_id in TelegramBot.SJVA_BOT_CHANNEL_CHAT_ID:
     try:
      TelegramBot.SUPER_BOT.sendMessage(c_id,text)
     except a as e:
      l('Exception:%s',e)
      l('Chat ID : %s',c_id)
      l(c()) 
   return N
  except a as e:
   l('Exception:%s',e)
   l(c())
   return y
# Created by pyminifier (https://github.com/liftoff/pyminifier)
