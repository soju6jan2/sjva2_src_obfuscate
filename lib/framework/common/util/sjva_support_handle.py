import os
Y=staticmethod
J=True
A=Exception
i=False
m=os.remove
n=os.system
u=os.path
import io
import traceback
z=traceback.format_exc
from framework import app,logger,path_data
N=logger.error
O=logger.debug
o=app.config
git_name='sjva_support'
class SJVASupportControl:
 @Y
 def epg_upload():
  try:
   O('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
   from epg.model import ModelEpgMakerSetting
   data={'updated':ModelEpgMakerSetting.get('updated')}
   from framework.util import Util
   Util.save_from_dict_to_json(data,u.join(path_data,'sjva_support','epg_updated.json'))
   epg_sh=u.join(path_data,'sjva_support','epg_commit.sh')
   n(epg_sh)
   return J
  except A as e:
   N('Exception:%s',e)
   N(z())
  return i
 @Y
 def epg_refresh():
  try:
   O('epg_refresh.....')
   if o['config']['server']:
    return 'server'
   from framework.common.util import download
   epg_db_filepath=u.join(path_data,'db','epg.db')
   try:
    from epg import ModelEpgMakerSetting
   except:
    return 'no_epg_plugin'
   if u.exists(epg_db_filepath):
    import requests
    url='https://raw.githubusercontent.com/soju6jan/sjva_support/master/epg_updated.json'
    data=requests.get(url).json()
    if data['updated']==ModelEpgMakerSetting.get('updated'):
     return 'recent'
   url='https://raw.githubusercontent.com/soju6jan/sjva_support/master/epg.db'
   tmp=u.join(path_data,'db','_epg.db')
   download(url,tmp)
   if u.exists(epg_db_filepath):
    m(epg_db_filepath)
   import shutil
   if u.exists(tmp):
    shutil.move(tmp,epg_db_filepath)
    O('Download epg.db.....')
   return 'refresh'
  except A as e:
   N('Exception:%s',e)
   N(z())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
