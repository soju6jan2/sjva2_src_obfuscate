import os
U=object
u=staticmethod
x=None
T=Exception
p=False
f=True
y=str
D=range
d=sorted
v=os.path
from datetime import datetime
import traceback
z=traceback.format_exc
import subprocess
import time
t=time.time
V=time.sleep
import re
Q=re.compile
import threading
import json
from framework import app,path_data,socketio
from system.logic_command import SystemLogicCommand
j=SystemLogicCommand.execute_command_return
from.import logger,Vars
W=Vars.key
q=logger.error
b=logger.debug
REMOTE_NAME_SJVA_SHARE_TEMP='SJVA_SHARE_TEMP' 
class RcloneTool(U):
 @u
 def lsjson(rclone_path,config_path,remote_path,option=x):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'lsjson',remote_path]
      j=SystemLogicCommand.execute_command_return
   b(command)
   if option is not x:
    command+=option
   b(command)
   ret=j(command,format='json')
   return ret
  except T as e:
   q('Exception:%s',e)
   q(z())
 @u
 def size(rclone_path,config_path,remote_path,option=x):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'size',remote_path,'--json']
      j=SystemLogicCommand.execute_command_return
   if option is not x:
    command+=option
   ret=j(command,format='json')
   return ret
  except T as e:
   q('Exception:%s',e)
   q(z())
 @u
 def rmdir(rclone_path,config_path,remote_path,option=x):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'rmdir',remote_path]
      j=SystemLogicCommand.execute_command_return
   b(command)
   if option is not x:
    command+=option
   b(command)
   ret=j(command)
   return ret
  except T as e:
   q('Exception:%s',e)
   q(z())
 @u
 def do_action(rclone_path,config_path,mode,server_type,folder_id,folder_name,server_filename,remote_path,action,folder_id_encrypted=p,listener=x,dry=p,option=x,remove_config=f,show_modal=f,force_remote_name=x):
  try:
   b('%s %s %s %s %s %s',mode,server_type,folder_id,remote_path,action,folder_id_encrypted)
   if folder_id_encrypted:
    from framework.common.util import AESCipher
    folder_id=AESCipher.decrypt(y(folder_id),W)
   rclone_upload_remote=remote_path.split(':')[0]
   return_folder_id=p
   if mode=='download':
    src_remote=remote_path.split(':')[0]if force_remote_name is x or force_remote_name=='' else force_remote_name
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
     return_folder_id=f
    elif server_type=='content':
     pass
    command=[rclone_path,'--config',config_path,'copy',remote_path,server_remote,'--drive-server-side-across-configs=true','-v']
   elif mode=='move':
    if server_type=='category':
     if folder_name!='':
      server_remote+='/%s'%folder_name
     else:
      server_remote+='/%s'%remote_path.split('/')[-1]
     return_folder_id=f
    command=[rclone_path,'--config',config_path,'move',remote_path,server_remote,'--drive-server-side-across-configs=true','-v']
   if dry:
    command.append('--dry-run')
   if option is not x:
    command+=option
   b(command)
   from system.logic_command2 import SystemLogicCommand2
   from system.logic_command import SystemLogicCommand
   ret={'percent':0,'folder_id':'','config_path':config_path,'server_remote':server_remote}
      j=SystemLogicCommand.execute_command_return
   return_log=SystemLogicCommand2('공유',[['msg','잠시만 기다리세요'],command,['msg','Rclone 명령을 완료하였습니다.'],],wait=f,show_modal=show_modal).start()
   for tmp in return_log:
    if tmp.find('Transferred')!=-1 and tmp.find('100%')!=-1:
     b(tmp)
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
     b('parent_remote : %s',parent_remote)
     for i in D(20):
      command=[rclone_path,'--config',config_path,'lsjson',parent_remote,'--dirs-only']
      b(command)
      ret['lsjson']=j(command,format='json')
      b(ret)
      tmp=server_remote.split('/')[-1]
      for item in ret['lsjson']:
       if item['Name']==tmp:
        from framework.common.util import AESCipher
        ret['folder_id']=AESCipher.encrypt(y(item['ID']),W)
        command=[rclone_path,'--config',config_path,'lsjson',parent_remote+'/'+item['Name'],'-R','--files-only']
        b(command)
        ret['lsjson']=j(command,format='json')
        ret['lsjson']=d(ret['lsjson'],key=lambda k:k['Path'])
        break
      b('folderid:%s',ret['folder_id'])
      if ret['folder_id']=='':
       b('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
       b('CCCCCRRRRRRRIIIIIIITTTTTIIIIICCCCCCAAAAAAALLLLL...... : %s',i)
       b(ret)
      else:
       break
      V(30)
      b('GET FOLDERID : %s',i)
   return ret
  except T as e:
   q('Exception:%s',e)
   q(z())
  """
        finally:
            try:
                if rclone_conf_filepath is not None and os.path.exists(rclone_conf_filepath):
                    if remove_config:
                        os.remove(rclone_conf_filepath)
                        pass
                pass
            except Exception as e: 
                logger.error('Exception:%s', e)
                logger.error(traceback.format_exc())
        """  
 @u
 def fileid_copy(rclone_path,config_path,fileid,remote_path):
  try:
   from framework.common.util import AESCipher
   fileid=AESCipher.decrypt(y(fileid),W)
   command=[rclone_path,'--config',config_path,'copy','{remote}:{{{fileid}}}'.format(remote=remote_path.split(':')[0],fileid=fileid),remote_path,'--drive-server-side-across-configs','-v']
   from system.logic_command import SystemLogicCommand
   log=j(command)
      j=SystemLogicCommand.execute_command_return
   b('fileid copy 결과 : %s',log)
   if log.find('100%')!=-1:
    return f
   return p
  except T as e:
   q('Exception:%s',e)
   q(z())
 @u
 def __make_rclone_conf(config_path,rclone_upload_remote,folder_id):
  try:
   from framework.common.util import read_file
   if v.exists(config_path):
    rclone_info=read_file(config_path)
   from framework import path_data
   import time
   filename='%s.conf'%(y(t()).split('.')[0])
      t=time.time
      V=time.sleep
   conf_filepath=v.join(path_data,'tmp',filename)
   start=-1
   dest_remote=x
   match=x
   first_rclone_info=x
   while f:
    start=rclone_info.find('[',start+1)
    if start==-1:
     break
    next_start=rclone_info.find('[',start+1)
    if next_start==-1:
     dest_remote=rclone_info[start:]
    else:
     dest_remote=rclone_info[start:next_start]
    if first_rclone_info is x and dest_remote.find('access_token')!=-1:
     first_rclone_info=dest_remote
    import re
    match=Q(r'\[(?P<remote_name>.*?)\]').search(dest_remote.strip())
          Q=re.compile
    if match.group('remote_name')==rclone_upload_remote:
     break
    else:
     dest_remote=x
     match=x
   if rclone_upload_remote is not x:
    if dest_remote is x:
     raise T('cannot find remote_name')
    else:
     if dest_remote.find('type = drive')==-1:
      if first_rclone_info is not x:
       src_remote_ready=first_rclone_info
      else:
       raise T('cannot find google remote_name')
     else:
      pass
      src_remote_ready=dest_remote
   else:
    src_remote_ready=first_rclone_info
   src_remote_ready=src_remote_ready.replace('team_drive','team_drive_dummy')
   match=Q(r'\[(?P<remote_name>.*?)\]').search(src_remote_ready.strip())
   server_rclone=src_remote_ready.replace('[%s]'%match.group('remote_name'),'[%s]'%REMOTE_NAME_SJVA_SHARE_TEMP)
   server_rclone+='\nroot_folder_id = %s'%folder_id
   filedata='%s\n\n%s\n'%(dest_remote,server_rclone)
   import framework.common.util as CommonUtil
   CommonUtil.write_file(filedata,conf_filepath)
   return conf_filepath
  except T as e:
   q('Exception:%s',e)
   q(z())
 @u
 def folderid_decrypt(folderid):
  from framework.common.util import AESCipher
  folderid=AESCipher.decrypt(y(folderid),W)
  return folderid
# Created by pyminifier (https://github.com/liftoff/pyminifier)
