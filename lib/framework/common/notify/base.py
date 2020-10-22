import os
u=None
B=True
Q=Exception
r=False
L=len
import traceback
from framework.common.notify import logger
from framework.common.notify.telegram import send_telegram_message
from framework.common.notify.discord import send_discord_message
def send_message(text,message_id=u,image_url=u):
 from system.model import ModelSetting as SystemModelSetting
 if SystemModelSetting.get_bool('notify_advaned_use'):
  return send_advanced_message(text,image_url=image_url,message_id=message_id)
 else:
  if SystemModelSetting.get_bool('notify_telegram_use'):
   send_telegram_message(text,image_url=image_url,bot_token=SystemModelSetting.get('notify_telegram_token'),chat_id=SystemModelSetting.get('notify_telegram_chat_id'))
  if SystemModelSetting.get_bool('notify_discord_use'):
   send_discord_message(text,image_url=image_url,webhook_url=SystemModelSetting.get('notify_discord_webhook'))
def send_advanced_message(text,image_url=u,policy=u,message_id=u):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if policy is u:
   policy=SystemModelSetting.get('notify_advaned_policy')
  if message_id is u:
   message_id='DEFAULT'
  policy_list=_make_policy_dict(policy)
  if message_id.strip()not in policy_list:
   message_id='DEFAULT'
  for tmp in policy_list[message_id.strip()]:
   if tmp.startswith('http'):
    send_discord_message(text,image_url=image_url,webhook_url=tmp)
   elif tmp.find(',')!=-1:
    tmp2=tmp.split(',')
    send_telegram_message(text,image_url=image_url,bot_token=tmp2[0],chat_id=tmp2[1])
  return B
 except Q as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
 return r
def _make_policy_dict(policy):
 try:
  ret={}
  for t in policy.split('\n'):
   t=t.strip()
   if t=='' or t.startswith('#'):
    continue
   else:
    tmp2=t.split('=')
    if L(tmp2)!=2:
     continue
    ret[tmp2[0].strip()]=[x.strip()for x in tmp2[1].split('|')]
  return ret
 except Q as e:
  logger.error('Exception:%s',e)
  logger.error(traceback.format_exc())
 return r
# Created by pyminifier (https://github.com/liftoff/pyminifier)
