import os
V=object
k=None
C=staticmethod
m=Exception
q=False
c=True
p=len
I=id
O=int
import sys
import traceback
import time
from datetime import datetime,timedelta
import logging
import urllib
import shutil
import re
import requests
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from sqlalchemy import desc
from framework import app,db,scheduler,celery
from framework.job import Job
from framework.util import Util
from framework.event import MyEvent
from.model import ModelSetting,ModelKtvFile,ModelKtvLibrary
from.entity_show import EntityLibraryPathRoot,EntityLibraryPath,EntityShow
package_name=__name__.split('.')[0]
logger=logging.getLogger(package_name)
class Logic(V):
 db_default={'auto_start':'False','interval':'2','not_ktv_move_folder_name':'no_ktv','manual_folder_name':'manual','no_daum_folder_name':u'기타','web_page_size':20,'download_path':'','telegram':'','except_partial':'.part','except_genre_remove_epi_number':u'애니메이션',}
 _DOWNLOAD_PATH=k
 _LIBRARY_ROOT_LIST=k
 @C
 def db_init():
  try:
   for key,value in Logic.db_default.items():
    if db.session.query(ModelSetting).filter_by(key=key).count()==0:
     db.session.add(ModelSetting(key,value))
   db.session.commit()
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 def plugin_load():
  try:
   Logic.db_init()
   logger.debug('plugin_load:%s',scheduler.sched)
   if ModelSetting.query.filter_by(key='auto_start').first().value=='True':
    Logic.scheduler_start()
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 def plugin_unload():
  pass
 @C
 def scheduler_start():
  try:
   interval=ModelSetting.query.filter_by(key='interval').first().value
   job=Job(package_name,'ktv_process',interval,Logic.process_download_file0,[u'국내영상 파일 처리'],q)
   scheduler.add_job_instance(job)
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 def scheduler_stop():
  try:
   scheduler.remove_job('ktv_process')
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 def setting_save(req):
  try:
   for key,value in req.form.items():
    logger.debug('Key:%s Value:%s',key,value)
    entity=db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
    entity.value=value
   db.session.commit()
   return c 
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 @C 
 def check_except_partial(filename,except_partial):
  try:
   for tmp in except_partial:
    if tmp=='':
     continue
    elif filename.find(tmp.strip())!=-1:
     return c
   return q
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 @C
 def for_synoindex(arg):
  try:
   logger.debug('FOR SYNOINDEX : %s'%arg)
   if arg['status']=='PROGRESS':
    result=arg['result']
    if 'filename' in result:
     Logic.send_to_listener(result['filename'])
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 def process_download_file0():
  try:
   if app.config['config']['use_celery']:
    result=Logic.process_download_file.apply_async()
    try:
     flag_rclone_start=result.get(on_message=Logic.for_synoindex,propagate=c)
     if flag_rclone_start:
      scheduler.execute_job('rclone')
    except:
     logger.debug('CELERY on_message not process.. only get() start')
     try:
      flag_rclone_start=result.get()
      if flag_rclone_start:
       scheduler.execute_job('rclone')
     except:
      pass
   else:
    Logic.process_download_file()
   if Logic.plex_update_list:
    logger.debug('>> len plex_update_list : %s',p(Logic.plex_update_list))
    for item in Logic.plex_update_list:
     try:
      db.session.add(item)
     except m as exception:
      logger.error('Exception:%s',exception)
      logger.error(traceback.format_exc())
    db.session.commit()
    Logic.plex_update_list=[]
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @C
 @celery.task(bind=c)
 def process_download_file(self):
  setting_list=Util.db_list_to_dict(db.session.query(ModelSetting).all())
  Logic._DOWNLOAD_PATH=setting_list['download_path']
  except_partial=setting_list['except_partial'].split(',')
  except_genre_remove_epi_number=[x.strip()for x in setting_list['except_genre_remove_epi_number'].split(',')]
  if '' in except_genre_remove_epi_number:
   except_genre_remove_epi_number.remove('')
  library_list=db.session.query(ModelKtvLibrary).all()
  Logic._LIBRARY_ROOT_LIST=[]
  for item in library_list:
   if item.library_type==0:
    drive_type=EntityLibraryPathRoot.DriveType.LOCAL
   else:
    drive_type=EntityLibraryPathRoot.DriveType.RCLONE
   lib=EntityLibraryPathRoot(drive_type=drive_type,mount_path=item.library_path,rclone_path=item.rclone_path,depth=2,replace_for_plex=[item.replace_for_plex_source,item.replace_for_plex_target])
   Logic._LIBRARY_ROOT_LIST.append(lib)
  dir_list=k
  path=Logic._DOWNLOAD_PATH
  list_=os.listdir(Logic._DOWNLOAD_PATH)
  logger.debug('process_download_file 2')
  logger.debug('list : %s',p(list_))
  flag_rclone_start=q
  for var in list_:
   try:
    if c:
     abspath=os.path.join(path,var)
     telegram_log=k
     entity=k
     if os.path.isfile(abspath):
      if Logic.check_except_partial(var,except_partial):
       continue
      telegram_log=package_name+'\n%s\n'%abspath
      if dir_list is k:
       logger.debug('process_download_file')
       dir_list=Logic._make_dir_list()
       logger.debug('process_download_file 1')
      logger.debug('===================================')
      logger.debug('File Process: %s',var)
      entity=EntityShow(var,nd_download_path=path,except_genre_remove_epi_number=except_genre_remove_epi_number)
      if entity.video_type==EntityShow.VideoType.KOREA_TV:
       logger.debug('<Move>') 
       _find_dir=Logic._get_find_dir(dir_list,entity) 
       if p(_find_dir)==1:
        entity.set_find_library_path(_find_dir[0])
        logger.debug(' - 하나의 폴더 선택됨 : %s',_find_dir[0].abspath)
        entity.move_file()
        if entity.scan_status==EntityShow.ScanStatus.MOVED and entity.nd_find_library_path.entity_library_root.drive_type==EntityLibraryPathRoot.DriveType.LOCAL:
         if app.config['config']['use_celery']:
          self.update_state(state='PROGRESS',meta={'filename':entity.move_abspath_local})
         else:
          Logic.send_to_listener(entity.move_abspath_local)
        elif entity.scan_status==EntityShow.ScanStatus.MOVED and entity.nd_find_library_path.entity_library_root.drive_type==EntityLibraryPathRoot.DriveType.RCLONE:
         if app.config['config']['use_celery']:
          self.update_state(state='PROGRESS',meta={'filename':entity.move_abspath_cloud})
         else:
          Logic.send_to_listener(entity.move_abspath_cloud)
        entity.modelfile=ModelKtvFile.create(entity)
        logger.debug(entity.log)
        db.session.add(entity.modelfile)
        db.session.commit()
        if entity.scan_status==EntityShow.ScanStatus.MOVED:
         try:
          import plex
          plex.Logic.send_scan_command(entity.modelfile,package_name)
         except m as exception:
          logger.error('NOT IMPORT PLEX!!')
         db.session.add(entity.modelfile)
         db.session.commit()
        if entity.move_type==EntityLibraryPathRoot.DriveType.RCLONE:
         flag_rclone_start=c
       elif p(_find_dir)>1:
        logger.debug(' - 선택된 폴더가 2개 이상')
        logger.debug('  %s',_find_dir[0].abspath)
        logger.debug('  %s',_find_dir[1].abspath)
        entity.log+='<파일이동>\n'
        entity.log+='선택된 폴더 %s개\n'%(p(_find_dir))
        entity.log+='  %s\n'%_find_dir[0].abspath
        entity.log+='  %s\n'%_find_dir[1].abspath
        tmp=os.path.join(Logic._DOWNLOAD_PATH,setting_list['manual_folder_name'])
        if not os.path.isdir(tmp):
         os.mkdir(tmp)
        if os.path.exists(os.path.join(tmp,var)):
         os.remove(os.path.join(tmp,var))
        shutil.move(abspath,tmp)
        if app.config['config']['use_celery']:
         self.update_state(state='PROGRESS',meta={'filename':os.path.join(tmp,var)})
        else:
         Logic.send_to_listener(os.path.join(tmp,var))
        entity.log+='  %s 이동\n'%tmp
       elif not _find_dir:
        logger.debug(' - 선택된 폴더 없음')
        entity.log+='<파일이동>\n'
        entity.log+='선택된 폴더 없음\n'
        flag_move=q
        if entity.daum_info is k:
         try:
          import daum_tv
          daum=daum_tv.ModelDaumTVShow(-1)
          daum.genre=setting_list['no_daum_folder_name']
          daum.title=entity.filename_name
         except m as exception:
          logger.error('Exception:%s',exception)
          logger.error(traceback.format_exc())
          daum=k
         entity.daum_info=daum
        if flag_move==q and entity.daum_info:
         flag_search=q
         for library_root in Logic._LIBRARY_ROOT_LIST:
          for _ in library_root.get_genre_list():
           if _==entity.daum_info.genre:
            tmp=os.path.join(library_root.mount_path,_,Util.change_text_for_use_filename(entity.daum_info.title))
            if not os.path.isdir(tmp):
             logger.debug('mkdir:%s',tmp)
             os.mkdir(tmp)
             entity.log+='폴더생성 : %s\n'%tmp
            logger.debug('  * 장르:%s [%s] 폴더 생성. 다음 탐색시 이동',_,tmp)
            flag_search=c
            break
          if flag_search:
           break
         if not flag_search:
          logger.debug('  * 장르:%s 없음.',entity.daum_info.genre)
          _=os.path.join(Logic._LIBRARY_ROOT_LIST[0].mount_path,entity.daum_info.genre)
          if not os.path.isdir(_):
           os.mkdir(_)
           entity.log+='장르 폴더생성 : %s\n'%_
       telegram_log+=entity.log 
       logger.debug('===================================')
      else:
       tmp=os.path.join(Logic._DOWNLOAD_PATH,setting_list['not_ktv_move_folder_name'])
       if not os.path.isdir(tmp):
        os.mkdir(tmp)
       if os.path.exists(os.path.join(tmp,var)):
        os.remove(os.path.join(tmp,var))
       shutil.move(abspath,tmp)
       if app.config['config']['use_celery']:
        self.update_state(state='PROGRESS',meta={'filename':os.path.join(tmp,var)})
       else:
        Logic.send_to_listener(os.path.join(tmp,var))
       telegram_log+='처리하지 못하는 파일 형식\n이동:%s\n'%tmp
     else:
      tmp=var+'.mp4'
      match_flag=q
      for regex in EntityShow._REGEX_FILENAME:
       match=re.compile(regex).match(tmp)
       if match:
        match_flag=c
        break
      if match_flag:
       try:
        childs=os.listdir(abspath)
        for c in childs:
         if os.path.isdir(os.path.join(abspath,c)):
          continue
        for c in childs:
         tmp=os.path.join(abspath,c)
         if os.stat(tmp).st_size<1000000:
          os.remove(tmp)
         else:
          if os.path.exists(os.path.join(path,c)):
           if os.stat(os.path.join(path,c)).st_size>=os.stat(tmp).st_size:
            os.remove(tmp)
           else:
            os.remove(os.path.join(path,c))
            shutil.move(tmp,path)
          else:
           shutil.move(tmp,path)
        shutil.rmtree(abspath)
       except m as exception:
        logger.error('Exception:%s',exception)
        logger.error(traceback.format_exc())
   except m as exception:
    try:
     db.session.rollback()
     logger.debug('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except:
     logger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>')
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc())
   finally:
    try:
     if ModelSetting.query.filter_by(key='telegram').first().value=='True' and telegram_log is not k:
      img=k
      if entity is not k and entity.daum_info is not k and entity.daum_info.poster_url is not k:
       img=entity.daum_info.poster_url
      import framework.common.notify as Notify
      Notify.send_message(telegram_log,image_url=img,message_id='fileprocess_ktv_result')
    except m as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc())
  logger.debug('flag_rclone_start : %s',flag_rclone_start) 
  Logic.check_library_completed()
  return flag_rclone_start
 @C
 def _make_dir_list():
  dir_list=[]
  for library_root in Logic._LIBRARY_ROOT_LIST:
   dir_list=Logic._explore_by_depth(library_root,library_root.mount_path,dir_list,library_root.depth,1)
  return dir_list
 """
    @staticmethod 
    def _explore(library_root, fnpath, dir_list):
        logger.debug('_explore %s %s %s', library_root, fnpath, dir_list)
        flag_append = False
        flag_exist_file = False
        flag_exist_dir = False
        listdir = os.listdir(fnpath)
        for var in listdir:
            _abspath = os.path.join(fnpath, var)
            if os.path.isdir(_abspath):
                if var.lower().startswith('season') or var.startswith(u'시즌'):
                    flag_append = True
                    break
                elif var.startswith('.'):
                    pass
                else:
                    flag_exist_dir = True
                    self._explore(library_root, _abspath, dir_list)
            else:
                flag_exist_file = True
        if flag_exist_dir and flag_exist_file:
            pass
        elif flag_exist_dir and not flag_exist_file:
            pass
        elif not flag_exist_dir and flag_exist_file:
            flag_append = True
        elif not flag_exist_dir and not flag_exist_file:
            flag_append = True
        if flag_append:
            dir_list.append(EntityLibraryPath(library_root, os.path.basename(fnpath), fnpath))
        return dir_list
    """ 
 @C
 def _explore_by_depth(library_root,fnpath,dir_list,library_root_depth,current_depth):
  listdir=os.listdir(fnpath)
  for var in listdir:
   _abspath=os.path.join(fnpath,var)
   if os.path.isdir(_abspath):
    if library_root_depth>current_depth:
     Logic._explore_by_depth(library_root,_abspath,dir_list,library_root_depth,(current_depth+1))
    else:
     dir_list.append(EntityLibraryPath(library_root,var,_abspath))
  return dir_list
 @C
 def _get_find_dir(dir_list,entity):
  ret=[]
  for item in dir_list:
   if entity.filename.find(item.basename)!=-1:
    ret.append(item)
   elif entity.nd_compare_name.find(item.compare_name)!=-1:
    ret.append(item)
   elif entity.nd_compare_name.replace(u'시즌','').find(item.compare_name.replace(u'시즌',''))!=-1:
    ret.append(item)
   elif entity.daum_info is not k and entity.daum_info.title==item.basename:
    ret.append(item)
  logger.debug('entity.filename_name : %s entity.nd_compare_name: %s',entity.filename_name,entity.nd_compare_name)
  for item in ret:
   logger.debug('item.basename : %s item.basename: %s',item.basename,item.compare_name)
   if entity.filename_name==item.basename:
    return[item]
   elif entity.nd_compare_name==item.compare_name:
    return[item]
  return ret
 plex_update_list=[]
 @C
 def receive_scan_result(I,filename):
  try:
   import plex
   logger.debug('Receive Scan Completed : %s-%s',I,filename)
   modelfile=db.session.query(ModelKtvFile).filter_by(I=O(I)).first()
   if modelfile is not k:
    modelfile.scan_status=3
    modelfile.scan_time=datetime.now()
    plex.Logic.get_section_id(modelfile,more=c)
    if scheduler.is_running('ktv_process'):
     Logic.plex_update_list.append(modelfile)
     logger.debug('>> plex_update_list insert!!')
    else:
     db.session.add(modelfile)
     db.session.commit()
     logger.debug('>> direct commit!!')
    if ModelSetting.query.filter_by(key='telegram').first().value=='True':
     text='<PLEX 스캔 완료 - KTV>\n%s\n\n%s'%(modelfile.filename,modelfile.plex_part)
     import framework.common.notify as Notify
     Notify.send_message(text,message_id='fileprocess_ktv_scan_completed')
  except m as exception:
   logger.debug('>>>>> receive_scan_result')
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 """
    @staticmethod
    def check_library_completed0():
        Logic.check_library_completed()
        return
        try:
            if app.config['config']['use_celery']:
                result =Logic.check_library_completed.apply_async()
                # Logic.process_download_file.apply_async()
                result.get()
            else:
                Logic.check_library_completed()
        except Exception as exception: 
            logger.error('Exception:%s', exception)
            logger.error(traceback.format_exc())
    """ 
 @C
 @celery.task
 def check_library_completed():
  try:
   import plex
   logger.debug('==========Cloud upload file check==========')
   entity_list=ModelKtvFile.get_library_check_list()
   for entity in entity_list:
    logger.debug('filename:%s',entity.filename)
    if entity.move_type==0:
     plex.Logic.send_scan_command(entity,package_name)
     db.session.add(entity)
    else:
     if not os.path.exists(entity.move_abspath_sync):
      plex.Logic.send_scan_command(entity,package_name)
      db.session.add(entity)
     else:
      logger.debug(' - upload not completed!!')
    """
                if os.path.exists(entity.get_finalpath()):
                    # 이건 최초 다운받을때 쇼가 아예 없었다면 항상 False이다.
                    # 쇼ID가 없을 때는 전체 라이브러리에서 재 탐색해야한다.
                    exist_in_library = PlexHandle.instance().exist_file_in_library(entity)
                    logger.debug(' - check exist file in library : %s %s', exist_in_library, entity.get_finalpath())
                    if exist_in_library:
                        logger.debug('  * exist!! status change!!') 
                        entity.set_scan_status(EntityShow.ScanStatus.EXIST_IN_LIBRARY)
                        DBManager.update_status_download_korea_tv(entity)
                    else:
                        logger.debug('  * not exist!! send add command!!')
                        self._send_scan_command(entity)
                else:
                    logger.debug(' - upload not completed!!')
                """    
   logger.debug('get_image_empty_list')
   entity_list=ModelKtvFile.get_image_empty_list()
   for entity in entity_list:
    logger.debug('filename:%s',entity.filename)
    plex.Logic.get_section_id(entity,more=c)
    db.session.add(entity)
   db.session.commit()
  except m as exception:
   logger.debug('Exception:%s',exception)
   logger.debug(traceback.format_exc()) 
 @C
 def filelist(req):
  try:
   ret={}
   page=1
   page_size=O(db.session.query(ModelSetting).filter_by(key='web_page_size').first().value)
   job_id=''
   search=''
   if 'page' in req.form:
    page=O(req.form['page'])
   if 'search_word' in req.form:
    search=req.form['search_word']
   query=db.session.query(ModelKtvFile)
   if search!='':
    query=query.filter(ModelKtvFile.plex_abspath.like('%'+search+'%'))
   count=query.count()
   query=(query.order_by(desc(ModelKtvFile.I)).limit(page_size).offset((page-1)*page_size))
   logger.debug('ModelKtvFile count:%s',count)
   lists=query.all()
   ret['list']=[item.as_dict()for item in lists]
   ret['paging']=Util.get_paging_info(count,page,page_size)
   try:
    import plex
    ret['plex_server_hash']=plex.Logic.get_server_hash()
   except m as exception:
    ret['plex_server_hash']=""
   return ret
  except m as exception:
   logger.debug('Exception:%s',exception)
   logger.debug(traceback.format_exc())
 @C
 def library_save(req):
  try:
   if c:
    library_id=O(req.form['library_id'])
    if library_id==-1:
     item=ModelKtvLibrary()
    else:
     item=db.session.query(ModelKtvLibrary).filter_by(I=library_id).with_for_update().first()
    item.library_type=O(req.form['library_type'])
    item.library_path=req.form['library_path']
    if item.library_type==1:
     item.rclone_path=req.form['rclone_path']
    item.replace_for_plex_source=req.form['replace_for_plex_source']
    item.replace_for_plex_target=req.form['replace_for_plex_target']
    item.index=O(req.form['index'])
    db.session.add(item)
    db.session.commit()
    logger.debug('item.library_type:%s',item.library_type)
    if item.library_type!=0:
     Logic.call_rclone_plugin(item)
   return c 
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 @C
 def call_rclone_plugin(item,remove=q):
  local=os.path.join(db.session.query(ModelSetting).filter_by(key='download_path').first().value,'rclone_%s'%item.rclone_path.split(':')[0],os.path.basename(item.library_path))
  logger.debug('Local:%s',local)
  import rclone
  rclone.Logic.rclone_job_by_ktv(local,item.rclone_path,remove)
 @C
 def library_list():
  try:
   return db.session.query(ModelKtvLibrary).order_by(ModelKtvLibrary.index).all()
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 @C
 def library_remove(req):
  try:
   if c:
    library_id=O(req.form['library_id'])
    lib=db.session.query(ModelKtvLibrary).filter_by(I=library_id).first()
    if lib.library_type!=0:
     Logic.call_rclone_plugin(lib,remove=c)
    db.session.delete(lib)
    db.session.commit()
   return c
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 @C
 def reset_db():
  try:
   db.session.query(ModelKtvFile).delete()
   db.session.commit()
   return c
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 listener=MyEvent()
 @C
 def add_listener(f):
  try:
   Logic.listener+=f
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 @C
 def remove_listener(f):
  try:
   Logic.listener-=f
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return q
 @C
 def send_to_listener(target_file):
  try:
   args=[]
   kargs={'plugin':'ktv','type':'add','filepath':target_file,'is_file':c}
   Logic.listener.fire(*args,**kargs)
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
# Created by pyminifier (https://github.com/liftoff/pyminifier)
