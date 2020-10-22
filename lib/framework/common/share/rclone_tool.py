import os
W=object
E=staticmethod
p=None
s=Exception
T=False
K=True
P=str
M=range
u=sorted
Q=os.path
from datetime import datetime
import traceback
h=traceback.format_exc
import subprocess
import time
G=time.time
D=time.sleep
import re
o=re.compile
import threading
import json
from framework import app,path_data,socketio
from system.logic_command import SystemLogicCommand
x=SystemLogicCommand.execute_command_return
from.import logger,Vars
z=Vars.key
N=logger.error
q=logger.debug
REMOTE_NAME_SJVA_SHARE_TEMP='SJVA_SHARE_TEMP' 
class RcloneTool(W):
 @E
 def lsjson(rclone_path,config_path,remote_path,option=p):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'lsjson',remote_path]
      x=SystemLogicCommand.execute_command_return
   q(command)
   if option is not p:
    command+=option
   q(command)
   ret=x(command,format='json')
   return ret
  except s as e:
   N('Exception:%s',e)
   N(h())
 @E
 def size(rclone_path,config_path,remote_path,option=p):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'size',remote_path,'--json']
      x=SystemLogicCommand.execute_command_return
   if option is not p:
    command+=option
   ret=x(command,format='json')
   return ret
  except s as e:
   N('Exception:%s',e)
   N(h())
 @E
 def rmdir(rclone_path,config_path,remote_path,option=p):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'rmdir',remote_path]
      x=SystemLogicCommand.execute_command_return
   q(command)
   if option is not p:
    command+=option
   q(command)
   ret=x(command)
   return ret
  except s as e:
   N('Exception:%s',e)
   N(h())
 @E
 def do_action(rclone_path,config_path,mode,server_type,folder_id,folder_name,server_filename,remote_path,action,folder_id_encrypted=T,listener=p,dry=T,option=p,remove_config=K,show_modal=K,force_remote_name=p):
  try:
   q('%s %s %s %s %s %s',mode,server_type,folder_id,remote_path,action,folder_id_encrypted)
   if folder_id_encrypted:
    from framework.common.util import AESCipher
    folder_id=AESCipher.decrypt(P(folder_id),z)
   rclone_upload_remote=remote_path.split(':')[0]
   return_folder_id=T
   if mode=='download':
    src_remote=remote_path.split(':')[0]if force_remote_name is p or force_remote_name=='' else force_remote_name
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
     return_folder_id=K
    elif server_type=='content':
     pass
    command=[rclone_path,'--config',config_path,'copy',remote_path,server_remote,'--drive-server-side-across-configs=true','-v']
   elif mode=='move':
    if server_type=='category':
     if folder_name!='':
      server_remote+='/%s'%folder_name
     else:
      server_remote+='/%s'%remote_path.split('/')[-1]
     return_folder_id=K
    command=[rclone_path,'--config',config_path,'move',remote_path,server_remote,'--drive-server-side-across-configs=true','-v']
   if dry:
    command.append('--dry-run')
   if option is not p:
    command+=option
   q(command)
   from system.logic_command2 import SystemLogicCommand2
   from system.logic_command import SystemLogicCommand
   ret={'percent':0,'folder_id':'','config_path':config_path,'server_remote':server_remote}
      x=SystemLogicCommand.execute_command_return
   return_log=SystemLogicCommand2('공유',[['msg','잠시만 기다리세요'],command,['msg','Rclone 명령을 완료하였습니다.'],],wait=K,show_modal=show_modal).start()
   for tmp in return_log:
    if tmp.find('Transferred')!=-1 and tmp.find('100%')!=-1:
     q(tmp)
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
     q('parent_remote : %s',parent_remote)
     for i in M(20):
      command=[rclone_path,'--config',config_path,'lsjson',parent_remote,'--dirs-only']
      q(command)
      ret['lsjson']=x(command,format='json')
      q(ret)
      tmp=server_remote.split('/')[-1]
      for item in ret['lsjson']:
       if item['Name']==tmp:
        from framework.common.util import AESCipher
        ret['folder_id']=AESCipher.encrypt(P(item['ID']),z)
        command=[rclone_path,'--config',config_path,'lsjson',parent_remote+'/'+item['Name'],'-R','--files-only']
        q(command)
        ret['lsjson']=x(command,format='json')
        ret['lsjson']=u(ret['lsjson'],key=lambda k:k['Path'])
        break
      q('folderid:%s',ret['folder_id'])
      if ret['folder_id']=='':
       q('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
       q('CCCCCRRRRRRRIIIIIIITTTTTIIIIICCCCCCAAAAAAALLLLL...... : %s',i)
       q(ret)
      else:
       break
      D(30)
      q('GET FOLDERID : %s',i)
   return ret
  except s as e:
   N('Exception:%s',e)
   N(h())
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
 @E
 def fileid_copy(rclone_path,config_path,fileid,remote_path):
  try:
   from framework.common.util import AESCipher
   fileid=AESCipher.decrypt(P(fileid),z)
   command=[rclone_path,'--config',config_path,'copy','{remote}:{{{fileid}}}'.format(remote=remote_path.split(':')[0],fileid=fileid),remote_path,'--drive-server-side-across-configs','-v']
   from system.logic_command import SystemLogicCommand
   log=x(command)
      x=SystemLogicCommand.execute_command_return
   q('fileid copy 결과 : %s',log)
   if log.find('100%')!=-1:
    return K
   return T
  except s as e:
   N('Exception:%s',e)
   N(h())
 @E
 def __make_rclone_conf(config_path,rclone_upload_remote,folder_id):
  try:
   from framework.common.util import read_file
   if Q.exists(config_path):
    rclone_info=read_file(config_path)
   from framework import path_data
   import time
   filename='%s.conf'%(P(G()).split('.')[0])
      G=time.time
      D=time.sleep
   conf_filepath=Q.join(path_data,'tmp',filename)
   start=-1
   dest_remote=p
   match=p
   first_rclone_info=p
   while K:
    start=rclone_info.find('[',start+1)
    if start==-1:
     break
    next_start=rclone_info.find('[',start+1)
    if next_start==-1:
     dest_remote=rclone_info[start:]
    else:
     dest_remote=rclone_info[start:next_start]
    if first_rclone_info is p and dest_remote.find('access_token')!=-1:
     first_rclone_info=dest_remote
    import re
    match=o(r'\[(?P<remote_name>.*?)\]').search(dest_remote.strip())
          o=re.compile
    if match.group('remote_name')==rclone_upload_remote:
     break
    else:
     dest_remote=p
     match=p
   if rclone_upload_remote is not p:
    if dest_remote is p:
     raise s('cannot find remote_name')
    else:
     if dest_remote.find('type = drive')==-1:
      if first_rclone_info is not p:
       src_remote_ready=first_rclone_info
      else:
       raise s('cannot find google remote_name')
     else:
      pass
      src_remote_ready=dest_remote
   else:
    src_remote_ready=first_rclone_info
   src_remote_ready=src_remote_ready.replace('team_drive','team_drive_dummy')
   match=o(r'\[(?P<remote_name>.*?)\]').search(src_remote_ready.strip())
   server_rclone=src_remote_ready.replace('[%s]'%match.group('remote_name'),'[%s]'%REMOTE_NAME_SJVA_SHARE_TEMP)
   server_rclone+='\nroot_folder_id = %s'%folder_id
   filedata='%s\n\n%s\n'%(dest_remote,server_rclone)
   import framework.common.util as CommonUtil
   CommonUtil.write_file(filedata,conf_filepath)
   return conf_filepath
  except s as e:
   N('Exception:%s',e)
   N(h())
 @E
 def folderid_decrypt(folderid):
  from framework.common.util import AESCipher
  folderid=AESCipher.decrypt(P(folderid),z)
  return folderid
# Created by pyminifier (https://github.com/liftoff/pyminifier)
