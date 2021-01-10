import os
import traceback,time
import random
import requests
from discord_webhook import DiscordWebhook,DiscordEmbed
from framework import app
from.import logger
server_plugin_ddns='https://sjva-server2.soju6jan.com'
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
    if data['target'].startswith('https://images-ext-')and requests.get(data['target']).status_code==200:
     return data['target']
  except Exception as exception:
   logger.error('server disconnect..')
 @classmethod
 def discord_proxy_set_target(cls,source,target):
  try:
   if source is None or target is None:
    return False
   if requests.get(target).status_code!=200:
    return False
   if target.startswith('https://images-ext-')and target.find('discordapp.net')!=-1:
    from framework import py_urllib
    from system.model import ModelSetting as SystemModelSetting
    url='{server_plugin_ddns}/server/normal/discord_proxy/set_target?source={source}&target={target}&user={user}'.format(server_plugin_ddns=server_plugin_ddns,source=py_urllib.quote_plus(source),target=py_urllib.quote_plus(target),user=SystemModelSetting.get('sjva_me_user_id'))
    data=requests.get(url).json()
  except Exception as exception:
   logger.error('server disconnect..')
  return True
 webhook_list=['https://discordapp.com/api/webhooks/723161710030225510/_kqNtqrPtEH8pBV9oh-STl9qplcx1iZXa0VnyZNtQzk8LJs9jJt1p19abWVUwmRUgbzt','https://discordapp.com/api/webhooks/794660845232848946/3B4UaxHTD_UyfDu_B79FaWeOuXQlctjvxY_pU6a7G2D58OU6qXepzlHpvQF4O2tM35g-','https://discordapp.com/api/webhooks/794660932386029589/XfehQxY7gLJgKNlZCAP5RQv6vMVXfroWa9SiXBqiNN84no5Hrsukoo5_dS-ZrOApTSRo','https://discordapp.com/api/webhooks/794661043863027752/A9O-vZSHIgfQ3KX7wO5_e2xisqpLw5TJxg2Qs1stBHxyd5PK-Zx0IJbAQXmyDN1ixZ-n','https://discordapp.com/api/webhooks/794661121184497674/cZi0nYDWOifmWb97X7zJQoIvZu-qXaKYHANxQBquzWqhybBKG7dqccL8uIIKHRwfR3D9','https://discord.com/api/webhooks/796558049380663296/5OtW7YKhOHnYRJycuUdRWRmFmMHOz--7mJ4f-VRoCLSQyS_4AcVVz5J81c2ce_9M7Y04','https://discord.com/api/webhooks/796558388326039552/k2VV356S1gKQa9ht-JuAs5Dqw5eVkxgZsLUzFoxmFG5lW6jqKl7zCBbbKVhs3pcLOetm','https://discord.com/api/webhooks/796558518324822036/XSkvTF8s6gY4yzAOKDEKsV2WeKHVXtV0sdGJDuBwTiBRYgEvU0W-3Ljf1VorQ6Y3zm7R','https://discord.com/api/webhooks/796558620812247050/BO1lRRtT9oNWodHRjrXyBIj_dJhaDvaiYaZ_rNBtUff7bZMyB1G5pbOe4sJ-N8qoBuCe','https://discord.com/api/webhooks/796558720208338947/gx-1oj3Unt29EGqQ7mRIEC1Zn4aPiytXBiwGuJyoQqI2KMj3T1_uxoGkVDDRfHscLZse',]
 @classmethod
 def discord_proxy_image(cls,image_url,webhook_url=None,retry=True):
  data=None
  if webhook_url is None or webhook_url=='':
   webhook_url= cls.webhook_list[random.randint(0,9)] 
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
   data=None
   if type(response)==type([]):
    if len(response)>0:
     data=response[0].json()
   else:
    data=response.json() 
   if data is not None and 'embeds' in data:
    target=data['embeds'][0]['image']['proxy_url']
    if requests.get(target).status_code==200:
     return target
    else:
     return image_url
   else:
    raise Exception(str(data))
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   if retry:
    time.sleep(1)
    return cls.discord_proxy_image(image_url,webhook_url=None,retry=False)
   else:
    return image_url
# Created by pyminifier (https://github.com/liftoff/pyminifier)
