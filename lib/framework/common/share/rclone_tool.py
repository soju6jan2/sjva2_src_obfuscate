import os
r=object
N=staticmethod
c=None
e=Exception
h=False
A=True
f=str
X=range
H=sorted
from datetime import datetime
import traceback
import subprocess
import time
import re
import threading
import json
from framework import app,path_data,socketio
from system.logic_command import SystemLogicCommand
from.import logger,Vars
REMOTE_NAME_SJVA_SHARE_TEMP='SJVA_SHARE_TEMP' 
class RcloneTool(r):
 @N
 def lsjson(rclone_path,config_path,remote_path,option=c):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'lsjson',remote_path]
   logger.debug(command)
   if option is not c:
    command+=option
   logger.debug(command)
   ret=SystemLogicCommand.execute_command_return(command,format='json')
   return ret
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @N
 def size(rclone_path,config_path,remote_path,option=c):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'size',remote_path,'--json']
   if option is not c:
    command+=option
   ret=SystemLogicCommand.execute_command_return(command,format='json')
   return ret
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @N
 def rmdir(rclone_path,config_path,remote_path,option=c):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'rmdir',remote_path]
   logger.debug(command)
   if option is not c:
    command+=option
   logger.debug(command)
   ret=SystemLogicCommand.execute_command_return(command)
   return ret
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @N
 def do_action(rclone_path,config_path,mode,server_type,folder_id,folder_name,server_filename,remote_path,action,folder_id_encrypted=h,listener=c,dry=h,option=c,remove_config=A,show_modal=A,force_remote_name=c):
  try:
   logger.debug('%s %s %s %s %s %s',mode,server_type,folder_id,remote_path,action,folder_id_encrypted)
   if folder_id_encrypted:
    from framework.common.util import AESCipher
    folder_id=AESCipher.decrypt(f(folder_id),Vars.key)
   rclone_upload_remote=remote_path.split(':')[0]
   return_folder_id=h
   if mode=='download':
    src_remote=remote_path.split(':')[0]if force_remote_name is c or force_remote_name=='' else force_remote_name
   else:
    src_remote=remote_path.split(':')[0]
   server_remote='{src_remote}:{{{folderid}}}'.format(src_remote=src_remote,folderid=folder_id)
   if mode=='download':
    if server_filename!='':
     server_remote+='/%s'%server_filename
    else:
     remote_path+='/%s'%folder_name
    command=[rclone_path,'--config',config_path,'copyto',server_remote,remote_path,'--drive-server-side-across-configs=true','-v']
   elif mode=='upload':
    if server_type=='category':
     if folder_name!='':
      server_remote+='/%s'%folder_name
     else:
      server_remote+='/%s'%remote_path.split('/')[-1]
     return_folder_id=A
    elif server_type=='content':
     pass
    command=[rclone_path,'--config',config_path,'copy',remote_path,server_remote,'--drive-server-side-across-configs=true','-v']
   elif mode=='move':
    if server_type=='category':
     if folder_name!='':
      server_remote+='/%s'%folder_name
     else:
      server_remote+='/%s'%remote_path.split('/')[-1]
     return_folder_id=A
    command=[rclone_path,'--config',config_path,'move',remote_path,server_remote,'--drive-server-side-across-configs=true','-v']
   if dry:
    command.append('--dry-run')
   if option is not c:
    command+=option
   logger.debug(command)
   from system.logic_command2 import SystemLogicCommand2
   from system.logic_command import SystemLogicCommand
   ret={'percent':0,'folder_id':'','config_path':config_path,'server_remote':server_remote}
   return_log=SystemLogicCommand2('공유',[['msg','잠시만 기다리세요'],command,['msg','Rclone 명령을 완료하였습니다.'],],wait=A,show_modal=show_modal).start()
   for tmp in return_log:
    if tmp.find('Transferred')!=-1 and tmp.find('100%')!=-1:
     logger.debug(tmp)
     ret['percent']=100
     break
    elif mode=='move' and tmp.find('Checks:')!=-1 and tmp.find('100%')!=-1:
     ret['percent']=100
     break
    elif tmp.find('Checks:')!=-1 and tmp.find('100%')!=-1:
     ret['percent']=100
     break
   if return_folder_id:
    if ret['percent']==100:
     parent_remote='/'.join(server_remote.split('/')[:-1])
     logger.debug('parent_remote : %s',parent_remote)
     for i in X(20):
      command=[rclone_path,'--config',config_path,'lsjson',parent_remote,'--dirs-only']
      logger.debug(command)
      ret['lsjson']=SystemLogicCommand.execute_command_return(command,format='json')
      logger.debug(ret)
      tmp=server_remote.split('/')[-1]
      for item in ret['lsjson']:
       if item['Name']==tmp:
        from framework.common.util import AESCipher
        ret['folder_id']=AESCipher.encrypt(f(item['ID']),Vars.key)
        command=[rclone_path,'--config',config_path,'lsjson',parent_remote+'/'+item['Name'],'-R','--files-only']
        logger.debug(command)
        ret['lsjson']=SystemLogicCommand.execute_command_return(command,format='json')
        ret['lsjson']=H(ret['lsjson'],key=lambda k:k['Path'])
        break
      logger.debug('folderid:%s',ret['folder_id'])
      if ret['folder_id']=='':
       logger.debug('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
       logger.debug('CCCCCRRRRRRRIIIIIIITTTTTIIIIICCCCCCAAAAAAALLLLL...... : %s',i)
       logger.debug(ret)
      else:
       break
      time.sleep(30)
      logger.debug('GET FOLDERID : %s',i)
   return ret
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  """
        finally:
            try:
                if rclone_conf_filepath is not None and os.path.exists(rclone_conf_filepath):
                    if remove_config:
                        os.remove(rclone_conf_filepath)
                        pass
                pass
            except Exception as exception: 
                logger.error('Exception:%s', exception)
                logger.error(traceback.format_exc())
        """  
 @N
 def fileid_copy(rclone_path,config_path,fileid,remote_path):
  try:
   from framework.common.util import AESCipher
   fileid=AESCipher.decrypt(f(fileid),Vars.key)
   command=[rclone_path,'--config',config_path,'copy','{remote}:{{{fileid}}}'.format(remote=remote_path.split(':')[0],fileid=fileid),remote_path,'--drive-server-side-across-configs','-v']
   from system.logic_command import SystemLogicCommand
   log=SystemLogicCommand.execute_command_return(command)
   logger.debug('fileid copy 결과 : %s',log)
   if log.find('100%')!=-1:
    return A
   return h
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @N
 def __make_rclone_conf(config_path,rclone_upload_remote,folder_id):
  try:
   from framework.common.util import read_file
   if os.path.exists(config_path):
    rclone_info=read_file(config_path)
   from framework import path_data
   import time
   filename='%s.conf'%(f(time.time()).split('.')[0])
   conf_filepath=os.path.join(path_data,'tmp',filename)
   start=-1
   dest_remote=c
   match=c
   first_rclone_info=c
   while A:
    start=rclone_info.find('[',start+1)
    if start==-1:
     break
    next_start=rclone_info.find('[',start+1)
    if next_start==-1:
     dest_remote=rclone_info[start:]
    else:
     dest_remote=rclone_info[start:next_start]
    if first_rclone_info is c and dest_remote.find('access_token')!=-1:
     first_rclone_info=dest_remote
    import re
    match=re.compile(r'\[(?P<remote_name>.*?)\]').search(dest_remote.strip())
    if match.group('remote_name')==rclone_upload_remote:
     break
    else:
     dest_remote=c
     match=c
   if rclone_upload_remote is not c:
    if dest_remote is c:
     raise e('cannot find remote_name')
    else:
     if dest_remote.find('type = drive')==-1:
      if first_rclone_info is not c:
       src_remote_ready=first_rclone_info
      else:
       raise e('cannot find google remote_name')
     else:
      pass
      src_remote_ready=dest_remote
   else:
    src_remote_ready=first_rclone_info
   src_remote_ready=src_remote_ready.replace('team_drive','team_drive_dummy')
   match=re.compile(r'\[(?P<remote_name>.*?)\]').search(src_remote_ready.strip())
   server_rclone=src_remote_ready.replace('[%s]'%match.group('remote_name'),'[%s]'%REMOTE_NAME_SJVA_SHARE_TEMP)
   server_rclone+='\nroot_folder_id = %s'%folder_id
   filedata='%s\n\n%s\n'%(dest_remote,server_rclone)
   import framework.common.util as CommonUtil
   CommonUtil.write_file(filedata,conf_filepath)
   return conf_filepath
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @N
 def folderid_decrypt(folderid):
  from framework.common.util import AESCipher
  folderid=AESCipher.decrypt(f(folderid),Vars.key)
  return folderid
# Created by pyminifier (https://github.com/liftoff/pyminifier)
