import os
import traceback,time
import requests
from discord_webhook import DiscordWebhook,DiscordEmbed
from framework import app
from.import logger
server_plugin_ddns='https://sjva-server.soju6jan.com'
class ToolExpandDiscord(object):
 @classmethod
 def send_discord_message(cls,text,image_url=None,webhook_url=None):
  from system.model import ModelSetting as SystemModelSetting
  try:
   if webhook_url is None:
    webhook_url=SystemModelSetting.get('notify_discord_webhook')
   webhook=DiscordWebhook(url=webhook_url,content=text)
   if image_url is not None:
    embed=DiscordEmbed()
    embed.set_timestamp()
    embed.set_image(url=image_url)
    webhook.add_embed(embed)
   response=webhook.execute()
   return True
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return False
 @classmethod
 def discord_proxy_get_target(cls,image_url):
  try:
   from framework import py_urllib
   url='{server_plugin_ddns}/server/normal/discord_proxy/get_target?source={source}'.format(server_plugin_ddns=server_plugin_ddns,source=py_urllib.quote_plus(image_url))
   data=requests.get(url).json()
   if data['ret']=='success':
    if data['target'].startswith('https://images-ext-')and data['target'].find('discordapp.net')!=-1:
     return data['target']
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @classmethod
 def discord_proxy_set_target(cls,source,target):
  try:
   if target.startswith('https://images-ext-')and target.find('discordapp.net')!=-1:
    from framework import py_urllib
    from system.model import ModelSetting as SystemModelSetting
    url='{server_plugin_ddns}/server/normal/discord_proxy/set_target?source={source}&target={target}&user={user}'.format(server_plugin_ddns=server_plugin_ddns,source=py_urllib.quote_plus(source),target=py_urllib.quote_plus(target),user=SystemModelSetting.get('sjva_me_user_id'))
    data=requests.get(url).json()
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @classmethod
 def discord_proxy_image(cls,image_url,webhook_url=None,retry=True):
  ret=cls.discord_proxy_get_target(image_url)
  if ret is not None:
   return ret
  if webhook_url is None or webhook_url=='':
   webhook_url='https://discordapp.com/api/webhooks/723161710030225510/_kqNtqrPtEH8pBV9oh-STl9qplcx1iZXa0VnyZNtQzk8LJs9jJt1p19abWVUwmRUgbzt'
  try:
   from framework import py_urllib
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
   target=data['embeds'][0]['image']['proxy_url']
   cls.discord_proxy_set_target(image_url,target)
   return target
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   logger.debug(image_url)
   logger.debug(data)
   if retry:
    time.sleep(3)
    return cls.discord_proxy_image(image_url,webhook_url=None,retry=False)
   else:
    return image_url
# Created by pyminifier (https://github.com/liftoff/pyminifier)
