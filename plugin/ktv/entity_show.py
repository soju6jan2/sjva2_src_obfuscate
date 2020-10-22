import os
s=object
X=None
Y=True
j=False
I=enumerate
E=int
p=len
b=classmethod
m=Exception
import re
import datetime
import shutil
from enum import Enum
from pytz import timezone
import plex
import daum_tv
from framework.logger import get_logger
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class EntityLibraryPathRoot(s):
 class DriveType(Enum):
  LOCAL=0 
  RCLONE=1
  CLOUD=2
  def __int__(self):
   return self.value
 drive_type=-1 
 mount_path=''
 rclone_path='' 
 sync_path=''
 depth=-1
 replace_for_plex=X
 def __init__(self,drive_type,mount_path,depth,rclone_path=X,sync_path=X,replace_for_plex=X):
  self.drive_type=drive_type
  self.mount_path=mount_path
  self.rclone_path=rclone_path
  self.sync_path=sync_path
  self.depth=depth
  self.replace_for_plex=replace_for_plex
 def _get_rclone_remove(self):
  return self.rclone_path.split(':')[0]
 def get_local_temp(self):
  return 'rclone_'+self._get_rclone_remove()
 def is_rclone(self):
  return self.drive_type==EntityLibraryPathRoot.DriveType.RCLONE
 def get_genre_list(self):
  return os.listdir(self.mount_path)
class EntityLibraryPath(s):
 RENAME_REGEX=r'[\s\.\,\-\[\]\?\:\!\_\=\+]'
 entity_library_root=X
 basename='' 
 abspath='' 
 compare_name='' 
 def __init__(self,entity_library_root,basename,abspath):
  self.entity_library_root=entity_library_root
  self.basename=basename
  self.abspath=abspath
  self.compare_name=re.sub(self.RENAME_REGEX,'',basename)
 def __str__(self):
  return "RootType: {0}\tBasename: {1}\tAbspath: {2}\tCompareName: {3} ".format(self.entity_library_root.drive_type,self.basename.encode('cp949'),self.abspath.encode('cp949'),self.compare_name.encode('cp949'))
class EntityShow(s):
 idx=-1
 class VideoType(Enum):
  KOREA_TV=0
  SUBS=1
  def __int__(self):
   return self.value
 video_type=-1 
 filename='' 
 original_filename='' 
 download_time='' 
 move_type=-1 
 match_folder_name='' 
 move_abspath_local='' 
 move_abspath_sync='' 
 move_abspath_cloud='' 
 send_command_time='' 
 scan_status=-1 
 scan_time='' 
 scan_abspath='' 
 plex_section_id=-1 
 plex_show_id=-1 
 plex_daum_id=-1 
 plex_title='' 
 plex_image='' 
 plex_abspath=''
 nd_compare_name='' 
 nd_download_path='' 
 nd_download_abspath='' 
 nd_find_library_path=X 
 nd_plex_show=''
 modelfile=X
 log=''
 class ScanStatus(Enum):
  DEFAULT=-1
  MOVED=1
  EXIST_IN_LIBRARY=2
  SCAN_COMPLETED=3
  DELETE_FILE=9
  def __int__(self):
   return self.value
 _REGEX_FILENAME=[r'^(?P<name>.*?)\.E(?P<no>\d+)(\-E\d{1,4})?\.?(END\.)?(?P<date>\d{6})\.(?P<etc>.*?)(?P<quality>\d+)[p|P](\-?(?P<release>.*?))?(\.(.*?))?$',r'^(?P<name>.*?)\sE(?P<no>\d+)(\-E\d{1,4})?\.?(END\.)?(?P<date>\d{6})\.(?P<etc>.*?)(?P<quality>\d+)[p|P](?P<more>\..*?)(?P<ext>\.[\w|\d]{3})$',r'^(?P<name>.*?)\.(E(?P<no>\d+)\.?)?(END\.)?(?P<date>\d{6})\.(?P<etc>.*?)(?P<quality>\d+)[p|P](\-?(?P<release>.*?))?(\.(.*?))?$',]
 _REGEX_FILENAME_RENAME=r'(?P<title>.*?)[\s\.]E?(?P<no>\d{1,2})[\-\~\s\.]?E?\d{1,2}'
 filename_name=''
 filename_no=''
 filename_date=''
 filename_etc=''
 filename_quality=''
 filename_release=''
 filename_more=''
 daum_info=X
 def __init__(self,filename,by=0,nd_download_path=X,daum_info=X,except_genre_remove_epi_number=X):
  self.original_filename=filename
  self.filename=filename
  self.analyze_filename()
  self.except_genre_remove_epi_number=except_genre_remove_epi_number
  if by==0:
   if self.video_type==-1:
    return X 
   self.nd_download_path=nd_download_path
   self.nd_download_abspath=os.path.join(nd_download_path,filename)
   self.download_time=datetime.datetime.now()
   self.change_filename_continous_episode()
   self.nd_compare_name=re.sub(EntityLibraryPath.RENAME_REGEX,'',self.filename_name)
   self.daum_info=daum_tv.Logic.get_daum_tv_info(self.filename_name)
   logger.debug('<Daum>')
   self.log+='<Daum>\n'
   if self.daum_info:
    logger.debug(' - 파일명으로 매칭된 Daum 정보: %s(%s)\n',self.daum_info.title,self.daum_info.genre)
    self.log+='매칭된 Daum 정보: %s(%s)\n'%(self.daum_info.title,self.daum_info.genre)
   else:
    logger.debug(' - 파일명으로 매칭된 Daum 정보 없음\n')
    self.log+='Daum 정보 없음\n'
   if Y and self.daum_info is not X:
    self.change_filename_by_rule()
   logger.debug('<Info>')
   logger.debug(' - 방송명: %s',self.filename_name)
   logger.debug(' - 방송일: %s',self.filename_date)
   logger.debug(' - 에피소드넘버: %s',self.filename_no)
   logger.debug(' - quality: %s %s',self.filename_quality,self.filename_release)
   self.log+='<파일명 정보>\n'
   self.log+=' - 방송명: %s\n'%self.filename_name
   self.log+=' - 방송일: %s\n'%self.filename_date
   self.log+=' - 에피소드넘버: %s\n'%self.filename_no
   self.log+=' - quality: %s %s\n'%(self.filename_quality,self.filename_release)
  elif by==1:
   pass
  elif by==2:
   self.change_filename_continous_episode(move=j)
   self.daum_info=daum_info
   self.change_filename_by_rule(move=j)
  elif by=='only_filename':
   if self.video_type==-1:
    return X
   self.change_filename_continous_episode(move=j)
   if self.video_type==EntityShow.VideoType.KOREA_TV:
    self.daum_info=daum_tv.Logic.get_daum_tv_info(self.filename_name)
    if self.daum_info is not X:
     self.change_filename_by_rule(move=j)
   else:
    self.daum_info=X
 def analyze_filename(self):
  for idx,regex in I(self._REGEX_FILENAME):
   match=re.compile(regex).match(self.filename)
   if match:
    logger.debug('매칭:%s %s',regex,self.filename)
    self.video_type=EntityShow.VideoType.KOREA_TV
    self.filename_name=match.group('name')
    self.filename_no=match.group('no')
    self.filename_date=match.group('date')
    self.filename_etc=match.group('etc').replace('.','')
    self.filename_quality=match.group('quality')
    self.filename_release=match.group('release')if 'release' in match.groupdict()else ''
    self.filename_more=match.group('more')if 'more' in match.groupdict()else ''
    if self.filename_no is not X and self.filename_no!='':
     self.filename_no=E(self.filename_no)
    else:
     self.filename_no=-1
    if idx==1:
     self.filename=EntityShow.make_filename(self)
    break
 def change_filename_continous_episode(self,move=Y):
  if self.filename_name.find('합')==-1:
   return
  match=re.compile(self._REGEX_FILENAME_RENAME).match(self.filename_name)
  if match:
   logger.debug('<합본 처리>')
   self.log+='<합본 파일 처리>\n'
   self.filename_name=match.group('title').strip()
   self.filename_no=E(match.group('no'))
   self.filename=EntityShow.make_filename(self)
   if move:
    _=os.path.join(self.nd_download_path,self.filename)
    shutil.move(self.nd_download_abspath,_)
    self.nd_download_abspath=_
    logger.debug(' - 파일명 변경:%s -> %s',self.original_filename,self.filename)
    self.log+=' - 파일명변경\nFrom : %s\nTo : %s\n'%(self.original_filename,self.filename)
 def change_filename_by_rule(self,move=Y):
  logger.debug('<Daum 정보 기반으로 파일명 변경>')
  flag_need_rename=j
  if self.daum_info.has_episode_info():
   self.log+='1-1. Daum 에피소드 정보 있음\n'
   key='20'+self.filename_date
   if key in self.daum_info.episode_list:
    self.log+='2-1. 파일명 방송일과 일치하는 Daum 에피소드 정보 있음\n'
    flag=j
    logger.debug(' - 파일정보 Episode Date:%s No:%s',self.filename_date,self.filename_no)
    self.log+=' - 파일명 정보. 방송일:%s 회차:%s\n'%(self.filename_date,self.filename_no)
    if self.filename_no!=-1:
     self.log+='3-1. 파일명에 회차 정보 있음 : %s\n'%self.filename_no
     for _ in self.daum_info.episode_list[key]:
      if E(_)==self.filename_no:
       flag=Y
       break
     if flag:
      logger.debug(' - Daum 정보와 일치')
      self.log+='4-1. 회차 정보 Daum과 일치\n'
     else:
      logger.debug(' - Daum 정보와 불일치')
      self.log+='4-2. 회차 정보 Daum과 불일치\n'
      logger.debug(' - Daum 정보 Date:%s Count:%s No:%s',key,p(self.daum_info.episode_list[key]),self.daum_info.episode_list[key][0])
      self.log+=' - Daum 정보. 방송일:%s 회차:%s Count:%s\n'%(key,self.daum_info.episode_list[key][0],p(self.daum_info.episode_list[key]))
      logger.debug(' - episode_count_one_day : %s',self.daum_info.episode_count_one_day)
      if self.daum_info.episode_count_one_day==4:
       if self.filename_no*2 ==E(self.daum_info.episode_list[key][1]):
        self.filename_no=E(self.daum_info.episode_list[key][0])
       elif self.filename_no*2 ==E(self.daum_info.episode_list[key][3]):
        self.filename_no=E(self.daum_info.episode_list[key][2])
       flag_need_rename=Y
      else:
       self.filename_no=E(self.daum_info.episode_list[key][0])
       flag_need_rename=Y
    else:
     self.log+='3-2. 파일명에 회차 정보 없음\n'
     self.log+=' - 파일명에 회차정보 삽입. Daum 정보. 방송일:%s 회차:%s Count:%s\n'%(key,self.daum_info.episode_list[key][0],p(self.daum_info.episode_list[key]))
     logger.debug(' - 파일정보 Epi no : %s date: %s',self.filename_no,self.filename_date)
     logger.debug(' - 파일명에 회차정보 삽입. Daum 정보 - date:%s count:%s %s',key,p(self.daum_info.episode_list[key]),self.daum_info.episode_list[key][0])
     self.filename_no=E(self.daum_info.episode_list[key][0])
     flag_need_rename=Y
   else:
    self.log+='2-2. 파일명 방송일과 일치하는 Daum 에피소드 정보 없음\n'
  else:
   self.log+='1-2. Daum에 에피소드 정보 없음\n'
   logger.debug(' - 다음 회차 정보 없음')
   if Y and self.filename_no!=-1:
    if self.except_genre_remove_epi_number is not X and('all' in self.except_genre_remove_epi_number or self.daum_info.genre in self.except_genre_remove_epi_number):
     self.log+=' 1-2-1. 파일명에 회차는 있지만 Daum에 정보가 없어서 회차정보 삭제. 삭제 제외 장르\n'
    else:
     self.log+=' 1-2-1. 파일명에 회차는 있지만 Daum에 정보가 없어서 회차정보 삭제\n'
     self.filename_no=-1 
     flag_need_rename=Y
   else:
    self.log+='1-2-2. 파일명과 Daum 모두 회차 정보 없음\n'
  if flag_need_rename:
   self.log+='<파일명 변경>\n'
   logger.debug(' - 파일명 변경')
   logger.debug('  * From : %s',self.filename)
   self.log+='  * From : %s\n'%self.filename
   self.filename=EntityShow.make_filename(self)
   logger.debug('  * To : %s',self.filename)
   self.log+='  * To : %s\n'%self.filename
   if move:
    _=os.path.join(self.nd_download_path,self.filename)
    shutil.move(self.nd_download_abspath,_)
    self.nd_download_abspath=_
 @b
 def make_filename(cls,_entity):
  ext=os.path.splitext(_entity.filename)[1]
  ret=_entity.filename_name
  if _entity.filename_no!=-1:
   if _entity.filename_no<10:
    ret='%s.E0%s'%(ret,_entity.filename_no)
   else:
    ret='%s.E%s'%(ret,_entity.filename_no)
  ret='%s.%s'%(ret,_entity.filename_date)
  if _entity.filename_etc:
   ret='%s.%s'%(ret,_entity.filename_etc)
  if _entity.filename_quality:
   ret='%s.%sp'%(ret,_entity.filename_quality)
  if _entity.filename_release!='' and _entity.filename_release is not X:
   ret='%s-%s'%(ret,_entity.filename_release)
  ret='%s%s%s'%(ret,_entity.filename_more,ext) 
  return ret
 def set_find_library_path(self,nd_find_library_path):
  self.nd_find_library_path=nd_find_library_path
  if nd_find_library_path.entity_library_root.drive_type==EntityLibraryPathRoot.DriveType.LOCAL:
   self.move_abspath_local=os.path.join(self.nd_find_library_path.abspath,self.filename)
   if nd_find_library_path.entity_library_root.replace_for_plex is not X:
    self.plex_abspath=self.move_abspath_local.replace(nd_find_library_path.entity_library_root.replace_for_plex[0],nd_find_library_path.entity_library_root.replace_for_plex[1])
    if nd_find_library_path.entity_library_root.replace_for_plex[1][0]=='/':
     self.plex_abspath=self.plex_abspath.replace('\\','/')
    else:
     self.plex_abspath=self.plex_abspath.replace('/','\\')
   else:
    self.plex_abspath=self.move_abspath_local
  elif nd_find_library_path.entity_library_root.drive_type==EntityLibraryPathRoot.DriveType.RCLONE:
   self.move_abspath_cloud=os.path.join(self.nd_find_library_path.abspath,self.filename)
   if nd_find_library_path.entity_library_root.replace_for_plex is not X:
    self.plex_abspath=self.move_abspath_cloud.replace(nd_find_library_path.entity_library_root.replace_for_plex[0],nd_find_library_path.entity_library_root.replace_for_plex[1])
    if nd_find_library_path.entity_library_root.replace_for_plex[1][0]=='/':
     self.plex_abspath=self.plex_abspath.replace('\\','/')
    else:
     self.plex_abspath=self.plex_abspath.replace('/','\\')
   else:
    self.plex_abspath=self.move_abspath_cloud 
  self.scan_abspath=self.nd_find_library_path.abspath
  self.match_folder_name=self.nd_find_library_path.basename 
  self.move_type=nd_find_library_path.entity_library_root.drive_type
  if self.scan_abspath!='':
   plex.Logic.get_section_id(self)
 def move_file(self):
  self.log+='<파일이동>\n'
  if self.nd_find_library_path.entity_library_root.drive_type==EntityLibraryPathRoot.DriveType.LOCAL:
   logger.debug(' * 로컬 폴더임')
   logger.debug(' * 파일 이동')
   self.log+='- 로컬 이동 처리\n'
   self._move_file_local()
  else:
   logger.debug(' * 클라우드 폴더임')
   self.log+='- 원격 동기화 폴더 이동 처리\n'
   self._move_file_for_cloud()
 def _move_file_local(self):
  try:
   flag_move_file=Y
   logger.debug('_move_file_local move_abspath_local :%s',self.move_abspath_local)
   if os.path.exists(self.move_abspath_local):
    self.log+='- 로컬 같은 파일 있음\n'
    logger.debug('같은 파일 있음')
    if os.path.getsize(self.nd_download_abspath)==os.path.getsize(self.move_abspath_local):
     logger.debug('사이즈가 같아 그냥 삭제')
     self.log+='- 사이즈가 같아 삭제\n'
     os.remove(self.nd_download_abspath)
     flag_move_file=j
     self.set_scan_status(EntityShow.ScanStatus.DELETE_FILE)
    else:
     logger.debug('사이즈가 달라 기존 파일 삭제')
     self.log+='- 사이즈가 달라 기존 파일 삭제\n'
     os.remove(self.move_abspath_local)
   if flag_move_file:
    if os.path.exists(self.nd_download_abspath):
     shutil.move(self.nd_download_abspath,self.move_abspath_local)
    self.set_scan_status(EntityShow.ScanStatus.MOVED)
    self.log+=' * src:%s\n * dest:%s\n'%(self.nd_download_abspath,os.path.dirname(self.move_abspath_local))
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def _move_file_for_cloud(self):
  try:
   flag_move_file=Y
   if os.path.exists(self.move_abspath_cloud):
    logger.debug('같은 파일 있음')
    self.log+='- 원격폴더 같은 파일 있음\n'
    if os.path.getsize(self.nd_download_abspath)==os.path.getsize(self.move_abspath_cloud):
     logger.debug('사이즈가 같아 그냥 삭제')
     self.log+='- 사이즈가 같아 삭제\n'
     os.remove(self.nd_download_abspath)
     flag_move_file=j
    else:
     logger.debug('사이즈가 달라 기존 파일 삭제')
     self.log+='- 사이즈가 달라 기존 파일 삭제\n'
     try:
      os.remove(self.move_abspath_cloud)
     except:
      logger.debug('원격파일 삭제 실패')
     self.set_scan_status(EntityShow.ScanStatus.DELETE_FILE)
   if flag_move_file:
    sync_path=os.path.join(self.nd_download_path,self.nd_find_library_path.entity_library_root.get_local_temp())
    logger.debug('sync_path : %s',sync_path)
    if not os.path.exists(sync_path):
     os.mkdir(sync_path)
    basename=os.path.basename(self.nd_find_library_path.entity_library_root.mount_path)
    splits=self._path_split(self.scan_abspath)
    idx=splits.index(basename)
    for _ in splits[idx:]:
     sync_path=os.path.join(sync_path,_)
     if not os.path.exists(sync_path):
      if not os.path.exists(sync_path):
       os.mkdir(sync_path)
       logger.debug('sync_path2 mkdir: %s',sync_path)
    self.move_abspath_sync=os.path.join(sync_path,self.filename)
    logger.debug('Movefile for cloud %s %s',self.nd_download_abspath,sync_path)
    if os.path.exists(os.path.join(sync_path,self.filename)):
     logger.debug('already file exist.. exist file remove : %s',os.path.join(sync_path,self.filename))
     os.remove(os.path.join(sync_path,self.filename))
    if os.path.exists(self.nd_download_abspath):
     shutil.move(self.nd_download_abspath,sync_path)
     logger.debug('Real move..')
    self.set_scan_status(EntityShow.ScanStatus.MOVED)
    self.log+=' * src:%s\n * dest:%s\n'%(self.nd_download_abspath,sync_path)
  except m as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def set_scan_status(self,status):
  self.scan_status=status
  if status==EntityShow.ScanStatus.SCAN_COMPLETED:
   self.scan_time=datetime.datetime.now()
 def get_finalpath(self):
  if self.move_type==EntityLibraryPathRoot.DriveType.LOCAL:
   return self.move_abspath_local
  else:
   return self.move_abspath_cloud 
 def _path_split(self,p,l=X):
  if l is X:
   l=[]
  if p==os.path.dirname(p):
   l.insert(0,os.path.dirname(p)) 
   return l
  else:
   l.insert(0,os.path.basename(p))
  return self._path_split(os.path.dirname(p),l)
if __name__=='__main__':
 pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
