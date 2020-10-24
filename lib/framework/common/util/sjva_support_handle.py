import os
R=staticmethod
N=True
K=Exception
b=False
import io
import traceback
from framework import app,logger,path_data
git_name='sjva_support'
class SJVASupportControl:
 @R
 def epg_upload():
  try:
   logger.debug('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
   from epg.model import ModelEpgMakerSetting
   data={'updated':ModelEpgMakerSetting.get('updated')}
   from framework.util import Util
   Util.save_from_dict_to_json(data,os.path.join(path_data,'sjva_support','epg_updated.json'))
   epg_sh=os.path.join(path_data,'sjva_support','epg_commit.sh')
   os.system(epg_sh)
   return N
  except K as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return b
 @R
 def epg_refresh():
  try:
   logger.debug('epg_refresh.....')
   if app.config['config']['server']:
    return 'server'
   from framework.common.util import download
   epg_db_filepath=os.path.join(path_data,'db','epg.db')
   try:
    from epg import ModelEpgMakerSetting
   except:
    return 'no_epg_plugin'
   if os.path.exists(epg_db_filepath):
    import requests
    url='https://raw.githubusercontent.com/soju6jan/sjva_support/master/epg_updated.json'
    data=requests.get(url).json()
    if data['updated']==ModelEpgMakerSetting.get('updated'):
     return 'recent'
   url='https://raw.githubusercontent.com/soju6jan/sjva_support/master/epg.db'
   tmp=os.path.join(path_data,'db','_epg.db')
   download(url,tmp)
   if os.path.exists(epg_db_filepath):
    os.remove(epg_db_filepath)
   import shutil
   if os.path.exists(tmp):
    shutil.move(tmp,epg_db_filepath)
    logger.debug('Download epg.db.....')
   return 'refresh'
  except K as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
