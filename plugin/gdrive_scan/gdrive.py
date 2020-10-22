import os
u=file
C=object
g=None
f=staticmethod
q=True
U=Exception
B=False
M=range
o=TypeError
m=enumerate
X=len
b=type
L=int
N=os.sep
W=os.path
import traceback
i=traceback.format_exc
import time
k=time.sleep
from datetime import datetime
import urllib
import json
J=json.loads
R=json.dumps
import threading
T=threading.Thread
import time
k=time.sleep
import platform
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify,session,send_from_directory 
from flask_socketio import SocketIO,emit,send
import oauth2client
P=oauth2client.client
s=oauth2client.u
from apiclient.discovery import build
from s import Storage
from oauth2client import tools
from P import flow_from_clientsecrets,OAuth2WebServerFlow
from httplib2 import Http
from oauth2client import u,client,tools
p=client.flow_from_clientsecrets
from sqlitedict import SqliteDict
from framework.logger import get_logger
from framework import app,db,scheduler,path_data,socketio,path_app_root
from framework.util import Util,AlchemyEncoder
from system.logic import SystemLogic
from.model import ModelSetting,ModelGDriveScanJob,ModelGDriveScanFile
D=ModelGDriveScanFile.add
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Auth(C):
 current_flow=g
 @f
 def save_token(code,name):
  try:
   credentials=GDrive.current_flow.step2_exchange(code)
   filename=W.join(path_data,'db','gdrive','%s.json'%name)
   storage=Storage(filename)
   storage.put(credentials)
   logger.debug('Save token:%s %s',filename,code)
   return q
  except U as e:
   logger.debug(e)
   logger.debug(i())
   return B
 @f
 def make_token_cli(account_type):
  try:
   logger.debug(account_type)
   tmp='client_secret.json'
   json_file=g
   if account_type=="0":
    pass
   if account_type=="1":
    tmp='client_secret_sjva_me.json'
   if account_type=="2":
    tmp='client_secret_knou_ac_kr.json'
   elif account_type=='99':
    json_file=W.join(path_app_root,'data','db',tmp)
    if not W.exists(json_file):
     return '99_not_exist'
   if json_file is g:
    json_file=W.join(path_app_root,'static','file',tmp)
   GDrive.current_flow =P.flow_from_clientsecrets(json_file,'https://www.googleapis.com/auth/drive',redirect_uri='urn:ietf:wg:oauth:2.0:oob')
   return GDrive.current_flow.step1_get_authorize_url()
  except U as e:
   logger.debug(e)
   logger.debug(i())
   return B
class GDrive(C):
 def __init__(self,match_rule):
  self.match_rule=match_rule.split(',')
  self.gdrive_name=self.match_rule[0].split(':')[0]
  self.match_rule=[self.match_rule[0].split(':')[1],self.match_rule[1]]
  self.db=W.join(W.join(path_data,'db','gdrive','%s.db'%self.gdrive_name))
  self.cache=SqliteDict(self.db,tablename='cache',encode=R,decode=J,autocommit=q)
  self.change_check_interval=60
  self.api_call_inverval=1
  self.flag_thread_run=q
  self.thread=g
  self.gdrive_service=g
 def start_change_watch(self):
  def get_start_page_token(creds):
   try:
    self.gdrive_service=build('drive','v3',http=creds.authorize(Http()))
    results=self.gdrive_service.changes().getStartPageToken().execute()
    page_token=results['startPageToken']
    logger.debug('startPageToken:%s',page_token)
    return page_token
   except U as e:
    logger.debug('Exception:%s',e)
    logger.debug(i()) 
  def thread_function():
   store=Storage(W.join(path_data,'db','gdrive','%s.json'%self.gdrive_name))
   creds=store.get()
   if not creds or creds.invalid:
    return-1
   page_token=get_start_page_token(creds)
   while self.flag_thread_run:
    try:
     for _ in M(self.change_check_interval):
      if self.flag_thread_run==B:
       return
      k(1)
     results=self.gdrive_service.changes().list(pageToken=page_token,pageSize=1000,fields="changes(                                     file(                                         id, md5Checksum,mimeType,modifiedTime,name,parents,teamDriveId,trashed                                     ),                                      fileId,removed                                 ),                                 newStartPageToken").execute()
     page_token=results.get('newStartPageToken')
     logger.debug('PAGE_TOKEN:%s'%page_token)
     items=results.get('changes',[])
     for _ in items:
      logger.debug('1.CHANGE : %s',_)
      is_add=q
      is_file=q
      if _['removed']==q:
       is_add=B
       fileid=_['fileId']
       if fileid in self.cache:
        file_meta={'name':self.cache[fileid]['name'],'parents':self.cache[fileid]['parents'],}
        file_meta['mimeType']=self.cache[fileid]['mimeType']if 'mimeType' in self.cache[fileid]else 'application/vnd.google-apps.folder'
       else:
        logger.debug('remove. not cache')
        continue
      else:
       if 'file' in _:
        if _['file']['mimeType']=='application/vnd.google-apps.folder':
         logger.debug('FOLDER')
        elif _['file']['mimeType'].startswith('video'):
         logger.debug('FILE')
        else:
         logger.debug('not folder, not video')
         continue
       fileid=_['file']['id']
       file_meta=self.gdrive_service.files().get(fileId=fileid,fields="id,mimeType, modifiedTime,name,parents,trashed").execute()
      if file_meta['mimeType']=='application/vnd.google-apps.folder':
       is_file=B
      logger.debug('IS_ADD : %s IS_FILE :%s',is_add,is_file)
      job_list=[]
      if is_add and is_file:
       job_list=[[file_meta,'ADD',is_file]]
      elif is_add and not is_file:
       job_list=[[file_meta,'ADD',is_file]]
       if fileid in self.cache:
        remove_file_meta={'name':self.cache[fileid]['name'],'parents':self.cache[fileid]['parents'],}
        remove_file_meta['mimeType']=self.cache[fileid]['mimeType']if 'mimeType' in self.cache else 'application/vnd.google-apps.folder'
        ttmp=(remove_file_meta['mimeType']!='application/vnd.google-apps.folder')
        job_list.insert(0,[remove_file_meta,'REMOVE',ttmp])
      elif not is_add and is_file:
       job_list=[[file_meta,'REMOVE',is_file]]
      elif not is_add and not is_file:
       job_list=[[file_meta,'REMOVE',is_file]] 
      for job in job_list: 
       file_meta=job[0]
       type_add_remove=job[1]
       is_file=job[2]
       logger.debug('2.FILEMETA:%s %s %s'%(file_meta,type_add_remove,is_file))
       file_paths=self.get_parent(file_meta)
       if file_paths is g:
        logger.debug('get_parent is None')
        continue
       gdrivepath='/'.join(file_paths)
       logger.debug('3.GdrivePath:%s'%gdrivepath)
       mount_abspath=self.get_mount_abspath(file_paths)
       if mount_abspath is g:
        logger.debug('NOT MOUNT INFO')
        continue
       logger.debug('4.MountPath:%s'%mount_abspath)
       s_id=self.get_section_id(mount_abspath)
       if s_id==-1:
        logger.debug('5-2.IGNORE. %s file section_id is -1.',mount_abspath)
       else:
        if is_add:
         self.cache[fileid]={'name':file_meta['name'],'parents':file_meta['parents'],'mimeType':file_meta['mimeType']}
        else:
         self.cache[fileid]=g
        """
                                if is_add and not is_file:
                                    try:
                                        if not os.listdir(mount_abspath):
                                            logger.debug('5. IS EMPTY!!')
                                            continue
                                    except:
                                        logger.debug('os.listdir exception!')
                                        continue
                                """        
        exist_in_library=self.is_exist_in_library(mount_abspath)
        if(not exist_in_library and type_add_remove=='ADD')or(exist_in_library and type_add_remove=='REMOVE'):
         self.send_command(s_id,mount_abspath,type_add_remove,is_file)
         logger.debug('5-1.Send Command %s %s %s %s',s_id,mount_abspath,type_add_remove,is_file)
        else:
         logger.debug('5-3.IGNORE. EXIST:%s TYPE:%s',exist_in_library,type_add_remove)
       try:
        from.logic import Logic
        Logic.send_to_listener(type_add_remove,is_file,mount_abspath)
       except U as e:
        logger.debug('Exception:%s',e)
        logger.debug(i())
       logger.debug('6.File process end.. WAIT :%s',self.api_call_inverval)
       for _ in M(self.api_call_inverval):
        if self.flag_thread_run==B:
         return
        k(1)
       logger.debug('7.AWAKE Continue')
    except o as e:
     page_token=get_start_page_token(creds)
     logger.debug('TYPE ERROR !!!!!!!!!!!!!!!!!!!!') 
     logger.debug('Exception:%s',e)
     logger.debug(i())
    except U as e:
     logger.debug('Exception:%s',e)
     logger.debug(i()) 
  self.thread=T(target=thread_function,args=())
  self.thread.daemon=q
  self.thread.start()
  return q
 def get_mount_abspath(self,gdrive_path):
  try:
   logger.debug(gdrive_path)
   if gdrive_path[0].startswith('My Drive'):
    gdrive_path[0]=gdrive_path[0].replace('My Drive','내 드라이브')
   replace_gdrive_path=self.match_rule[0].split('/')
   if self.match_rule[1][0]!='/':
    (drive,p)=W.splitdrive(self.match_rule[1])
    replace_mount_path=W.split(p)
   else:
    drive=g
    replace_mount_path=W.split(self.match_rule[1])
   flag_find=q
   for idx,val in m(replace_gdrive_path):
    if gdrive_path[idx]!=val:
     flag_find=B
   if flag_find:
    ret=u''
    for _ in replace_mount_path:
     ret=W.join(ret,_)
    for _ in gdrive_path[idx+1:]:
     ret=W.join(ret,_)
    if drive is not g:
     ret=W.join(drive,N,ret)
   else:
    ret=g
    logger.debug('WRONG SETTING PATH!!!!!!!!!!!!!') 
    return ret
   logger.debug('get_mount_abspath1: %s',ret)
   if self.match_rule[1][0]!='/':
    ret=ret.replace('/','\\')
    if ret[0]=='\\':
     ret=ret[1:]
   else:
    ret=ret.replace('\\','/')
   logger.debug('get_mount_abspath2: %s',ret)
   return ret
  except U as e:
   logger.debug('Exception:%s',e)
   logger.debug(i())
 def get_parent(self,file_meta):
  try:
   file_paths=[file_meta['name']]
   parents=file_meta['parents']
   while parents is not g:
    parent_id=parents[0]
    logger.debug('parent_id:%s',parent_id)
    if parent_id not in self.cache:
     parent_result=self.gdrive_service.files().get(fileId=parent_id,fields="id,mimeType, modifiedTime, name, parents, trashed").execute()
     logger.debug('parent_result:%s',parent_result)
     self.cache[parent_id]={'name':parent_result['name'],'parents':parent_result['parents']if 'parents' in parent_result else g,'mimeType':parent_result['mimeType']}
    logger.debug('parent_id in cache : %s',(parent_id in self.cache))
    file_paths.insert(0,self.cache[parent_id]['name'])
    logger.debug('    file_paths:%s',file_paths)
    parents=self.cache[parent_id]['parents']
    logger.debug('    parents:%s',parents)
    if X(file_paths)>30:
     return g
   return file_paths
  except U as e:
   logger.debug('Exception:%s',e)
   logger.debug(i())
 def stop(self):
  logger.debug('Gdrive stop function start..: %s %s ',self.gdrive_name,self.thread.isAlive())
  self.flag_thread_run=B
  self.thread.join()
  logger.debug('Gdrive stop function end..: %s %s',self.gdrive_name,self.thread.isAlive())
 def get_section_id(self,path):
  try:
   import plex
   section_id=plex.Logic.get_section_id_by_file(path)
   logger.debug('SectionID:%s %s',section_id,b(section_id))
   return section_id
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return-1
 def is_exist_in_library(self,path):
  try:
   import plex
   ret=plex.Logic.is_exist_in_library(path)
   logger.debug('is_exist_in_library %s %s',path,ret)
   return ret
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
   return q
 def send_command(self,s_id,mount_abspath,type_add_remove,is_file):
  callback_id=-1
  try:
   callback_id=D(self.gdrive_name,mount_abspath,L(s_id)if b(s_id)==b('')else s_id,is_file,(type_add_remove=='ADD'))
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
  try:
   import plex
   plex.Logic.send_scan_command2('gdrive_scan',s_id,mount_abspath,callback_id,type_add_remove,"GDRIVE")
  except U as e:
   logger.error('Exception:%s',e)
   logger.error(i())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
