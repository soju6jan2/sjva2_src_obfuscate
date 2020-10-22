import os
m=True
u=object
f=staticmethod
U=None
e=list
E=sorted
H=Exception
A=len
F=int
b=False
M=range
x=str
from datetime import datetime,timedelta
import traceback
import subprocess
import time
import re
import threading
import json
from framework import app,path_data,socketio,path_app_root
from system.model import ModelSetting as SystemModelSetting
from system.logic_command import SystemLogicCommand
from system.logic_command2 import SystemLogicCommand2
from.import logger,Vars
REMOTE_NAME_SJVA_SHARE_TEMP='SJVA_SHARE_TEMP' 
def emit(msg):
 socketio.emit("command_modal_add_text",msg,namespace='/framework',broadcast=m)
class RcloneTool2(u):
 @f
 def lsjson(rclone_path,config_path,remote_path,option=U):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'lsjson',remote_path]
   if option is not U:
    command+=option
   ret=SystemLogicCommand.execute_command_return(command,format='json')
   if ret is not U:
    ret=e(E(ret,key=lambda k:k['Path']))
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def size(rclone_path,config_path,remote_path,option=U):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'size',remote_path,'--json']
   if option is not U:
    command+=option
   ret=SystemLogicCommand.execute_command_return(command,format='json')
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def rmdir(rclone_path,config_path,remote_path,option=U):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'rmdir',remote_path,'--drive-use-trash=false','-vv']
   if option is not U:
    command+=option
   logger.debug('RMDIR:%s',' '.join(command))
   ret=SystemLogicCommand.execute_command_return(command)
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def purge(rclone_path,config_path,remote_path,option=U):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'purge',remote_path,'--drive-use-trash=false','-vv']
   if option is not U:
    command+=option
   logger.debug('PURGE:%s',' '.join(command))
   ret=SystemLogicCommand.execute_command_return(command,force_log=m)
   logger.debug(ret)
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def mkdir(rclone_path,config_path,remote_path,option=U):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'mkdir',remote_path]
   if option is not U:
    command+=option
   logger.debug('MKDIR:%s',' '.join(command))
   ret=SystemLogicCommand.execute_command_return(command)
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def getid(rclone_path,config_path,remote_path,option=U):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'backend','getid',remote_path]
   if option is not U:
    command+=option
   ret=SystemLogicCommand.execute_command_return(command).strip()
   logger.debug('GETID : %s\n%s',' '.join(command),ret)
   if ret is not U and(A(ret.split(' '))>1 or ret==''):
    ret=U
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def moveto(rclone_path,config_path,remote_path,remote_path2,option=U):
  try:
   from system.logic_command import SystemLogicCommand
   command=[rclone_path,'--config',config_path,'moveto',remote_path,remote_path2]
   if option is not U:
    command+=option
   logger.debug('MOVETO : %s',' '.join(command))
   ret=SystemLogicCommand.execute_command_return(command).strip()
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def get_datetime(item):
  ret=datetime.strptime(item['ModTime'],'%Y-%m-%dT%H:%M:%S.%fZ')
  ret=ret+timedelta(hours=9)
  return ret
 @f
 def get_datetime_diff(item):
  d=RcloneTool2.get_datetime(item)
  delta=datetime.now()-d
  seconds=delta.total_seconds()
  return(F)(seconds/60)
 @f
 def can_use_share(rclone_path,config_path,remote_path):
  try:
   size_data=RcloneTool2.size(rclone_path,config_path,'%s:{1vgB9BQaDjjKDa04k6st7po7HUqGeYY5o}'%remote_path.split(':')[0])
   if size_data['count']==1 and size_data['bytes']==7:
    return m
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  return b
 @f
 def can_use_relay(rclone_path,config_path,remote_path):
  try:
   folderid=RcloneTool2.getid(rclone_path,config_path,remote_path)
   config_path=os.path.join(path_app_root,'lib','framework','common','share','tool.pyo')
   tmp=RcloneTool2.lsjson(rclone_path,config_path,'remote_test:{%s}'%folderid)
   if tmp is not U:
    return m
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  return b
 @f
 def do_user_upload(rclone_path,config_path,remote_path,folder_name,upload_folderid,board_type,category_type,show_modal=m,is_move=b):
  try:
   ret={'completed':b,'folderid':'','lsjson':U}
   gdrive_remote=remote_path.split(':')[0]
   server_remote='{gdrive_remote}:{{{upload_folderid}}}'.format(gdrive_remote=gdrive_remote,upload_folderid=upload_folderid)
   socketio.emit("command_modal_clear",U,namespace='/framework',broadcast=m)
   socketio.emit("command_modal_show",'업로드',namespace='/framework',broadcast=m)
   socketio.emit("command_modal_add_text",'잠시만 기다리세요.\n\n',namespace='/framework',broadcast=m)
   socketio.emit("command_modal_add_text",'1. 업로드 가능 테스트.\n',namespace='/framework',broadcast=m)
   can_use_share_flag=RcloneTool2.can_use_share(rclone_path,config_path,remote_path)
   if can_use_share_flag:
    socketio.emit("command_modal_add_text",'업로드 가능합니다.\n\n',namespace='/framework',broadcast=m)
   else:
    socketio.emit("command_modal_add_text",'업로드 불가능합니다. 구글 그룹스에 가입하세요.\n\n',namespace='/framework',broadcast=m)
    return ret
   socketio.emit("command_modal_add_text",'2. 컨텐츠 크기 및 파일목록.\n',namespace='/framework',broadcast=m)
   ret['lsjson']=RcloneTool2.lsjson(rclone_path,config_path,remote_path,option=['-R','--files-only'])
   ret['size']=RcloneTool2.size(rclone_path,config_path,remote_path)
   emit('파일수 : {}\n파일크기 : {}\n\n'.format(ret['size']['count'],ret['size']['bytes']))
   socketio.emit("command_modal_add_text",'3. 공유드라이브 폴더 생성\n',namespace='/framework',broadcast=m)
   tmp_foldername="{board_type}^{category_type}^{count}^{bytes}^{folder_name}^{user_id}".format(board_type=board_type,category_type=category_type,count=ret['size']['count'],bytes=ret['size']['bytes'],folder_name=folder_name,user_id=SystemModelSetting.get('sjva_me_user_id'))
   upload_remote='{server_remote}/{tmp_foldername}/{folder_name}'.format(server_remote=server_remote,tmp_foldername=tmp_foldername,folder_name=folder_name)
   RcloneTool2.mkdir(rclone_path,config_path,upload_remote)
   emit('remote path : {}\n\n'.format(upload_remote))
   socketio.emit("command_modal_add_text",'4. 생성된 폴더의 ID 정보\n',namespace='/framework',broadcast=m)
   for i in M(1,11):
    emit('{}/10. GETID 시도\n'.format(i))
    tmp=RcloneTool2.getid(rclone_path,config_path,upload_remote)
    if tmp is not U:
     ret['folder_id']=tmp
     break
    emit('실패. 10초 후 다시 시도합니다.\n')
    time.sleep(10)
   emit('\n')
   if ret['folder_id']is U:
    emit('폴더ID를 얻을 수 없어 중단합니다.\n\n')
    emit('이미 폴더는 만들어졌으니, 잠시 후 다시 시도하면 정보를 가져올 수 있습니다.\n\n')
    return ret
   else:
    emit('폴더 ID : %s\n\n'%ret['folder_id'])
   command=[rclone_path,'--config',config_path,'move' if is_move else 'copy',remote_path,upload_remote,'--drive-server-side-across-configs=true','-v']
   return_log=SystemLogicCommand2('업로드',[['msg','5. Rclone 명령'],command,['msg','Rclone 명령을 완료하였습니다.'],],wait=m,show_modal=show_modal,clear=b).start()
   for tmp in return_log:
    if(tmp.find('Transferred')!=-1 and tmp.find('100%')!=-1)or(tmp.find('Checks:')!=-1 and tmp.find('100%')!=-1):
     ret['completed']=m
     if is_move:
      emit('purge 명령으로 move 루트 삭제\n')
      RcloneTool2.purge(rclone_path,config_path,remote_path)
     break
   emit('업로드 결과 : {}. (True:성공, False:실패)\n\n'.format(ret['completed']))
   return ret
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
   emit('에러 : {}'.format(x(e)))
 @f
 def do_user_download(rclone_path,config_path,folderid,remote_path):
  try:
   ret={'completed':b,'folderid':'','lsjson':U}
   source_remote='{gdrive_remote}:{{{folderid}}}'.format(gdrive_remote=remote_path.split(':')[0],folderid=folderid)
   command=[rclone_path,'--config',config_path,'move',source_remote,remote_path,'--drive-server-side-across-configs=true','-v','--delete-empty-src-dirs','--drive-use-trash=false']
   return_log=SystemLogicCommand.execute_command_return(command)
   logger.debug('확인:%s',return_log)
   if(return_log.find('Transferred')!=-1 and return_log.find('100%')!=-1)or(return_log.find('Checks:')!=-1 and return_log.find('100%')!=-1):
    RcloneTool2.purge(rclone_path,config_path,source_remote)
    logger.debug('성공')
    return m
   logger.debug('성공xxxxxxxxxxxxx')
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  return b
 @f
 def do_relay_completed(rclone_path,config_path,source_remote_path,original_remote_path):
  try:
   command=[rclone_path,'--config',config_path,'move',source_remote_path,original_remote_path,'--drive-server-side-across-configs=true','-v','--delete-empty-src-dirs','--drive-use-trash=false']
   return_log=SystemLogicCommand.execute_command_return(command)
   if(return_log.find('Transferred')!=-1 and return_log.find('100%')!=-1)or(return_log.find('Checks:')!=-1 and return_log.find('100%')!=-1):
    RcloneTool2.purge(rclone_path,config_path,source_remote_path)
    return m
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  return b
 @f
 def do_relay_download(rclone_path,config_path,clone_id,relay_remote_path,original_id,last_remote_path):
  try:
   ret1=ret2=ret3=b
   ret1=RcloneTool2.do_user_download(rclone_path,config_path,clone_id,relay_remote_path)
   if ret1:
    sourceid=RcloneTool2.getid(rclone_path,config_path,relay_remote_path)
    ret2=RcloneTool2.do_relay_copy(rclone_path,sourceid,original_id)
   ret3=RcloneTool2.do_relay_completed(rclone_path,config_path,relay_remote_path,last_remote_path)
   if ret1 and ret2 and ret3:
    return m
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  return b
 @f
 def do_relay_copy(rclone_path,sourceid,targetid):
  try:
   sa_worker_path=os.path.join(path_app_root,'lib','framework','common','share','tool.pyo')
   account_file_path=sa_worker_path.replace('tool.pyo','account/')
   target_remote='worker1:{%s}'%(targetid)
   tmp=RcloneTool2.lsjson(rclone_path,sa_worker_path,target_remote,['--dirs-only','--drive-service-account-file-path',account_file_path])
   logger.debug("mmmmmmmmmmmmmmmmmmmmmmmmm")
   logger.debug(tmp)
   copy_count=0
   for t in tmp:
    if t['Name'].startswith('copy'):
     copy_count+=1
   for_range=3 if copy_count<10 else 1
   is_correct=b
   try:
    content_source_size_data=RcloneTool2.size(rclone_path,sa_worker_path,'worker1:{%s}/source'%targetid,['--drive-service-account-file-path',account_file_path])
    logger.debug('content_source_size_data : %s',content_source_size_data)
    source_remote='worker1:{%s}'%sourceid
    for i in M(10):
     user_size_data=RcloneTool2.size(rclone_path,sa_worker_path,source_remote,['--drive-service-account-file-path',account_file_path])
     if user_size_data is not U and content_source_size_data is not U and user_size_data['bytes']==content_source_size_data['bytes']:
      logger.debug('복사 사이즈 같음 : %s %s',user_size_data,content_source_size_data)
      is_correct=m
      break
     else:
      logger.debug('복사 사이즈 다름 : %s %s',user_size_data,content_source_size_data)
      time.sleep(30)
   except H as e:
    logger.debug('!bbbbbbbbbbbbbbbb  !!')
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
   if is_correct==m:
    for i in M(0,for_range):
     tmp='%s/copy_%s_%s'%(target_remote,F(x(time.time()).split('.')[0]),SystemModelSetting.get('sjva_me_user_id'))
     command=[rclone_path,'--config',sa_worker_path,'copy',source_remote,tmp,'--drive-service-account-file-path',account_file_path,'--drive-server-side-across-configs=true','-vv']
     logger.debug(command)
     return_log=SystemLogicCommand.execute_command_return(command)
     if return_log.find('100%')!=-1: 
      logger.debug('토렌트 공드에 복사 성공.. : %s',tmp)
     else:
      RcloneTool2.purge(rclone_path,sa_worker_path,tmp,option=['--drive-service-account-file-path',account_file_path])
      for_range+=1
      if for_range>10:
       for_range=10
    return m
   else:
    logger.debug("mmmmm RELAY COPY FAIL!!")
  except H as e:
   logger.debug('!!!!!!!!!!!!!!!!!!!relay copy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def fileid_copy(rclone_path,config_path,fileid,remote_path):
  try:
   from framework.common.util import AESCipher
   fileid=AESCipher.decrypt(x(fileid),Vars.key)
   command=[rclone_path,'--config',config_path,'copy','{remote}:{{{fileid}}}'.format(remote=remote_path.split(':')[0],fileid=fileid),remote_path,'--drive-server-side-across-configs','-v']
   from system.logic_command import SystemLogicCommand
   log=SystemLogicCommand.execute_command_return(command)
   logger.debug('fileid copy 결과 : %s',log)
   if log.find('100%')!=-1:
    return m
   return b
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def __make_rclone_conf(config_path,rclone_upload_remote,folder_id):
  try:
   from framework.common.util import read_file
   if os.path.exists(config_path):
    rclone_info=read_file(config_path)
   from framework import path_data
   import time
   filename='%s.conf'%(x(time.time()).split('.')[0])
   conf_filepath=os.path.join(path_data,'tmp',filename)
   start=-1
   dest_remote=U
   match=U
   first_rclone_info=U
   while m:
    start=rclone_info.find('[',start+1)
    if start==-1:
     break
    next_start=rclone_info.find('[',start+1)
    if next_start==-1:
     dest_remote=rclone_info[start:]
    else:
     dest_remote=rclone_info[start:next_start]
    if first_rclone_info is U and dest_remote.find('access_token')!=-1:
     first_rclone_info=dest_remote
    import re
    match=re.compile(r'\[(?P<remote_name>.*?)\]').search(dest_remote.strip())
    if match.group('remote_name')==rclone_upload_remote:
     break
    else:
     dest_remote=U
     match=U
   if rclone_upload_remote is not U:
    if dest_remote is U:
     raise H('cannot find remote_name')
    else:
     if dest_remote.find('type = drive')==-1:
      if first_rclone_info is not U:
       src_remote_ready=first_rclone_info
      else:
       raise H('cannot find google remote_name')
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
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @f
 def folderid_decrypt(folderid):
  from framework.common.util import AESCipher
  folderid=AESCipher.decrypt(x(folderid),Vars.key)
  return folderid
 """
    @staticmethod
    def copy_with_json(binary, config, fileid, remote_path, show_modal=True):
        try:
            import time
            json_path = os.path.join(path_data, 'tmp', '%s.json' % (str(time.time()).split('.')[0]))
            command = [binary, '--config', config, 'copyto', '{remote}:{{{fileid}}}'.format(remote=remote_path.split(':')[0], fileid=fileid), json_path, '-v']
            if show_modal:
                socketio.emit("command_modal_clear", None, namespace='/framework', broadcast=True)
                socketio.emit("command_modal_show", '공유', namespace='/framework', broadcast=True)
                socketio.emit("command_modal_add_text", '잠시만 기다리세요%s\n\n', namespace='/framework', broadcast=True)
                #socketio.emit("command_modal_add_text", '%s\n\n' % command, namespace='/framework', broadcast=True)
            if fileid.endswith('=='):
                socketio.emit("command_modal_add_text", '예전 방식이라 처리하지 못합니다.\n\n', namespace='/framework', broadcast=True)
                return
            log = SystemLogicCommand.execute_command_return(command)
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
            ret = True
            th_list = []
            for item in data:
                if item['isdir'] == 'false':
                    def func():
                        tmp_remote_path = remote_path + item['path'] + '/' + item['name']
                        command = [binary, '--config', config, 'copyto', '{remote}:{{{fileid}}}'.format(remote=remote_path.split(':')[0], fileid=item['id']), tmp_remote_path, '--drive-server-side-across-configs', '-v']
                        if show_modal:
                            socketio.emit("command_modal_add_text", '$ %s\n\n' % ' '.join(command), namespace='/framework', broadcast=True)
                        log = SystemLogicCommand.execute_command_return(command)
                        if show_modal:
                            socketio.emit("command_modal_add_text", '%s\n\n' % log, namespace='/framework', broadcast=True)
                        logger.debug('fileid copy 결과 : %s', log)
                    th = threading.Thread(target=func)
                    th.setDaemon(True)
                    th.start()
                    th_list.append(th)
                    time.sleep(5)
            for th in th_list:
                th.join()
            if show_modal:
                socketio.emit("command_modal_add_text", '모두 완료하였습니다.\n\n', namespace='/framework', broadcast=True)
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
    """ 
# Created by pyminifier (https://github.com/liftoff/pyminifier)
