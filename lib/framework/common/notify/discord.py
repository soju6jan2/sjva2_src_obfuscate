import os
f=None
n=True
T=Exception
k=False
import traceback
from discord_webhook import DiscordWebhook,DiscordEmbed
from framework.common.notify import logger
def send_discord_message(text,image_url=f,webhook_url=f):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if webhook_url is f:
   webhook_url=SystemModelSetting.get('notify_discord_webhook')
  webhook=DiscordWebhook(url=webhook_url,content=text)
  if image_url is not f:
   embed=DiscordEmbed()
   embed.set_timestamp()
   embed.set_image(url=image_url)
   webhook.add_embed(embed)
  response=webhook.execute()
  return n
 except T as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
 return k
def discord_proxy_image(image_url,webhook_url=f):
 if webhook_url is f or webhook_url=='':
  webhook_url='https://discordapp.com/api/webhooks/723161710030225510/_kqNtqrPtEH8pBV9oh-STl9qplcx1iZXa0VnyZNtQzk8LJs9jJt1p19abWVUwmRUgbzt'
 try:
  webhook=DiscordWebhook(url=webhook_url,content='')
  embed=DiscordEmbed()
  embed.set_timestamp()
  embed.set_image(url=image_url)
  webhook.add_embed(embed)
  import io
  byteio=io.BytesIO()
  webhook.add_file(file=byteio.getvalue(),filename='dummy')
  response=webhook.execute()
  data=response.json()
  url=data['embeds'][0]['image']['proxy_url']
  return url
 except T as exception:
  logger.error('Exception:%s',exception)
  logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
