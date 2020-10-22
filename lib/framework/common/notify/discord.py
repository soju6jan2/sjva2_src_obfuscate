import os
v=None
Y=True
l=Exception
F=False
import traceback
R=traceback.format_exc
from discord_webhook import DiscordWebhook,DiscordEmbed
from framework.common.notify import logger
r=logger.error
def send_discord_message(text,image_url=v,webhook_url=v):
 from system.model import ModelSetting as SystemModelSetting
 try:
  if webhook_url is v:
   webhook_url=SystemModelSetting.get('notify_discord_webhook')
  webhook=DiscordWebhook(url=webhook_url,content=text)
  if image_url is not v:
   embed=DiscordEmbed()
   embed.set_timestamp()
   embed.set_image(url=image_url)
   webhook.add_embed(embed)
  response=webhook.execute()
  return Y
 except l as e:
  r('Exception:%s',e)
  r(R())
 return F
def discord_proxy_image(image_url,webhook_url=v):
 if webhook_url is v or webhook_url=='':
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
 except l as e:
  r('Exception:%s',e)
  r(R())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
