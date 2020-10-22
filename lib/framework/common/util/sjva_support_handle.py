import os
r=staticmethod
H=True
x=Exception
j=False
W=os.remove
A=os.system
J=os.path
import io
import traceback
U=traceback.format_exc
from framework import app,logger,path_data
b=logger.error
Y=logger.debug
y=app.config
git_name='sjva_support'
class SJVASupportControl:
 @r
 def epg_upload():
  try:
   Y('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
   from epg.model import ModelEpgMakerSetting
   data={'updated':ModelEpgMakerSetting.get('updated')}
   from framework.util import Util
   Util.save_from_dict_to_json(data,J.join(path_data,'sjva_support','epg_updated.json'))
   epg_sh=J.join(path_data,'sjva_support','epg_commit.sh')
   A(epg_sh)
   return H
  except x as e:
   b('Exception:%s',e)
   b(U())
  return j
 @r
 def epg_refresh():
  try:
   Y('epg_refresh.....')
   if y['config']['server']:
    return 'server'
   from framework.common.util import download
   epg_db_filepath=J.join(path_data,'db','epg.db')
   try:
    from epg import ModelEpgMakerSetting
   except:
    return 'no_epg_plugin'
   if J.exists(epg_db_filepath):
    import requests
    url='https://raw.githubusercontent.com/soju6jan/sjva_support/master/epg_updated.json'
    data=requests.get(url).json()
    if data['updated']==ModelEpgMakerSetting.get('updated'):
     return 'recent'
   url='https://raw.githubusercontent.com/soju6jan/sjva_support/master/epg.db'
   tmp=J.join(path_data,'db','_epg.db')
   download(url,tmp)
   if J.exists(epg_db_filepath):
    W(epg_db_filepath)
   import shutil
   if J.exists(tmp):
    shutil.move(tmp,epg_db_filepath)
    Y('Download epg.db.....')
   return 'refresh'
  except x as e:
   b('Exception:%s',e)
   b(U())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
