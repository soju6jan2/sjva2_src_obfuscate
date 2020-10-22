if __name__=='__main__':
r=reload
C=object
d=None
F=True
H=False
Q=enumerate
E=int
U=len
D=classmethod
i=Exception
 import os
 j=os.mkdir
 G=os.remove
 p=os.listdir
 A=os.path
 import sys
 r(sys)
 sys.setdefaultencoding('utf-8')
 sys.path.insert(0,A.dirname(A.dirname(A.abspath(__file__))))
import os
j=os.mkdir
G=os.remove
p=os.listdir
A=os.path
import re
W=re.compile
J=re.sub
import datetime
w=datetime.now
u=datetime.datetime
import shutil
q=shutil.move
from enum import Enum
from pytz import timezone
import plex
O=plex.Logic
import daum_tv
L=daum_tv.Logic
from framework.logger import get_logger
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class EntityLibraryPathRoot(C):
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
 replace_for_plex=d
 def __init__(self,drive_type,mount_path,depth,rclone_path=d,sync_path=d,replace_for_plex=d):
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
  return p(self.mount_path)
class EntityLibraryPath(C):
 RENAME_REGEX=r'[\s\.\,\-\[\]\?\:\!\_\=\+]'
 entity_library_root=d
 basename='' 
 abspath='' 
 compare_name='' 
 def __init__(self,entity_library_root,basename,abspath):
  self.entity_library_root=entity_library_root
  self.basename=basename
  self.abspath=abspath
  self.compare_name=J(self.RENAME_REGEX,'',basename)
 def __str__(self):
  return "RootType: {0}\tBasename: {1}\tAbspath: {2}\tCompareName: {3} ".format(self.entity_library_root.drive_type,self.basename.encode('cp949'),self.abspath.encode('cp949'),self.compare_name.encode('cp949'))
class EntityShow(C):
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
 nd_find_library_path=d 
 nd_plex_show=''
 modelfile=d
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
 daum_info=d
 def __init__(self,filename,by=0,nd_download_path=d,daum_info=d,except_genre_remove_epi_number=d):
  self.original_filename=filename
  self.filename=filename
  self.analyze_filename()
  self.except_genre_remove_epi_number=except_genre_remove_epi_number
  if by==0:
   if self.video_type==-1:
    return d 
   self.nd_download_path=nd_download_path
   self.nd_download_abspath=A.join(nd_download_path,filename)
   self.download_time=u.now()
   self.change_filename_continous_episode()
   self.nd_compare_name=J(EntityLibraryPath.RENAME_REGEX,'',self.filename_name)
   self.daum_info=L.get_daum_tv_info(self.filename_name)
   logger.debug('<Daum>')
   self.log+='<Daum>\n'
   if self.daum_info:
    logger.debug(' - 파일명으로 매칭된 Daum 정보: %s(%s)\n',self.daum_info.title,self.daum_info.genre)
    self.log+='매칭된 Daum 정보: %s(%s)\n'%(self.daum_info.title,self.daum_info.genre)
   else:
    logger.debug(' - 파일명으로 매칭된 Daum 정보 없음\n')
    self.log+='Daum 정보 없음\n'
   if F and self.daum_info is not d:
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
   self.change_filename_continous_episode(move=H)
   self.daum_info=daum_info
   self.change_filename_by_rule(move=H)
  elif by=='only_filename':
   if self.video_type==-1:
    return d
   self.change_filename_continous_episode(move=H)
   if self.video_type==EntityShow.VideoType.KOREA_TV:
    self.daum_info=L.get_daum_tv_info(self.filename_name)
    if self.daum_info is not d:
     self.change_filename_by_rule(move=H)
   else:
    self.daum_info=d
 def analyze_filename(self):
  for idx,regex in Q(self._REGEX_FILENAME):
   match=W(regex).match(self.filename)
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
    if self.filename_no is not d and self.filename_no!='':
     self.filename_no=E(self.filename_no)
    else:
     self.filename_no=-1
    if idx==1:
     self.filename=EntityShow.make_filename(self)
    break
 def change_filename_continous_episode(self,move=F):
  if self.filename_name.find('합')==-1:
   return
  match=W(self._REGEX_FILENAME_RENAME).match(self.filename_name)
  if match:
   logger.debug('<합본 처리>')
   self.log+='<합본 파일 처리>\n'
   self.filename_name=match.group('title').strip()
   self.filename_no=E(match.group('no'))
   self.filename=EntityShow.make_filename(self)
   if move:
    _=A.join(self.nd_download_path,self.filename)
    q(self.nd_download_abspath,_)
    self.nd_download_abspath=_
    logger.debug(' - 파일명 변경:%s -> %s',self.original_filename,self.filename)
    self.log+=' - 파일명변경\nFrom : %s\nTo : %s\n'%(self.original_filename,self.filename)
 def change_filename_by_rule(self,move=F):
  logger.debug('<Daum 정보 기반으로 파일명 변경>')
  flag_need_rename=H
  if self.daum_info.has_episode_info():
   self.log+='1-1. Daum 에피소드 정보 있음\n'
   key='20'+self.filename_date
   if key in self.daum_info.episode_list:
    self.log+='2-1. 파일명 방송일과 일치하는 Daum 에피소드 정보 있음\n'
    flag=H
    logger.debug(' - 파일정보 Episode Date:%s No:%s',self.filename_date,self.filename_no)
    self.log+=' - 파일명 정보. 방송일:%s 회차:%s\n'%(self.filename_date,self.filename_no)
    if self.filename_no!=-1:
     self.log+='3-1. 파일명에 회차 정보 있음 : %s\n'%self.filename_no
     for _ in self.daum_info.episode_list[key]:
      if E(_)==self.filename_no:
       flag=F
       break
     if flag:
      logger.debug(' - Daum 정보와 일치')
      self.log+='4-1. 회차 정보 Daum과 일치\n'
     else:
      logger.debug(' - Daum 정보와 불일치')
      self.log+='4-2. 회차 정보 Daum과 불일치\n'
      logger.debug(' - Daum 정보 Date:%s Count:%s No:%s',key,U(self.daum_info.episode_list[key]),self.daum_info.episode_list[key][0])
      self.log+=' - Daum 정보. 방송일:%s 회차:%s Count:%s\n'%(key,self.daum_info.episode_list[key][0],U(self.daum_info.episode_list[key]))
      logger.debug(' - episode_count_one_day : %s',self.daum_info.episode_count_one_day)
      if self.daum_info.episode_count_one_day==4:
       if self.filename_no*2 ==E(self.daum_info.episode_list[key][1]):
        self.filename_no=E(self.daum_info.episode_list[key][0])
       elif self.filename_no*2 ==E(self.daum_info.episode_list[key][3]):
        self.filename_no=E(self.daum_info.episode_list[key][2])
       flag_need_rename=F
      else:
       self.filename_no=E(self.daum_info.episode_list[key][0])
       flag_need_rename=F
    else:
     self.log+='3-2. 파일명에 회차 정보 없음\n'
     self.log+=' - 파일명에 회차정보 삽입. Daum 정보. 방송일:%s 회차:%s Count:%s\n'%(key,self.daum_info.episode_list[key][0],U(self.daum_info.episode_list[key]))
     logger.debug(' - 파일정보 Epi no : %s date: %s',self.filename_no,self.filename_date)
     logger.debug(' - 파일명에 회차정보 삽입. Daum 정보 - date:%s count:%s %s',key,U(self.daum_info.episode_list[key]),self.daum_info.episode_list[key][0])
     self.filename_no=E(self.daum_info.episode_list[key][0])
     flag_need_rename=F
   else:
    self.log+='2-2. 파일명 방송일과 일치하는 Daum 에피소드 정보 없음\n'
  else:
   self.log+='1-2. Daum에 에피소드 정보 없음\n'
   logger.debug(' - 다음 회차 정보 없음')
   if F and self.filename_no!=-1:
    if self.except_genre_remove_epi_number is not d and('all' in self.except_genre_remove_epi_number or self.daum_info.genre in self.except_genre_remove_epi_number):
     self.log+=' 1-2-1. 파일명에 회차는 있지만 Daum에 정보가 없어서 회차정보 삭제. 삭제 제외 장르\n'
    else:
     self.log+=' 1-2-1. 파일명에 회차는 있지만 Daum에 정보가 없어서 회차정보 삭제\n'
     self.filename_no=-1 
     flag_need_rename=F
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
    _=A.join(self.nd_download_path,self.filename)
    q(self.nd_download_abspath,_)
    self.nd_download_abspath=_
 @D
 def make_filename(cls,_entity):
  ext=A.splitext(_entity.filename)[1]
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
  if _entity.filename_release!='' and _entity.filename_release is not d:
   ret='%s-%s'%(ret,_entity.filename_release)
  ret='%s%s%s'%(ret,_entity.filename_more,ext) 
  return ret
 def set_find_library_path(self,nd_find_library_path):
  self.nd_find_library_path=nd_find_library_path
  if nd_find_library_path.entity_library_root.drive_type==EntityLibraryPathRoot.DriveType.LOCAL:
   self.move_abspath_local=A.join(self.nd_find_library_path.abspath,self.filename)
   if nd_find_library_path.entity_library_root.replace_for_plex is not d:
    self.plex_abspath=self.move_abspath_local.replace(nd_find_library_path.entity_library_root.replace_for_plex[0],nd_find_library_path.entity_library_root.replace_for_plex[1])
    if nd_find_library_path.entity_library_root.replace_for_plex[1][0]=='/':
     self.plex_abspath=self.plex_abspath.replace('\\','/')
    else:
     self.plex_abspath=self.plex_abspath.replace('/','\\')
   else:
    self.plex_abspath=self.move_abspath_local
  elif nd_find_library_path.entity_library_root.drive_type==EntityLibraryPathRoot.DriveType.RCLONE:
   self.move_abspath_cloud=A.join(self.nd_find_library_path.abspath,self.filename)
   if nd_find_library_path.entity_library_root.replace_for_plex is not d:
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
   O.get_section_id(self)
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
   flag_move_file=F
   logger.debug('_move_file_local move_abspath_local :%s',self.move_abspath_local)
   if A.exists(self.move_abspath_local):
    self.log+='- 로컬 같은 파일 있음\n'
    logger.debug('같은 파일 있음')
    if A.getsize(self.nd_download_abspath)==A.getsize(self.move_abspath_local):
     logger.debug('사이즈가 같아 그냥 삭제')
     self.log+='- 사이즈가 같아 삭제\n'
     G(self.nd_download_abspath)
     flag_move_file=H
     self.set_scan_status(EntityShow.ScanStatus.DELETE_FILE)
    else:
     logger.debug('사이즈가 달라 기존 파일 삭제')
     self.log+='- 사이즈가 달라 기존 파일 삭제\n'
     G(self.move_abspath_local)
   if flag_move_file:
    if A.exists(self.nd_download_abspath):
     q(self.nd_download_abspath,self.move_abspath_local)
    self.set_scan_status(EntityShow.ScanStatus.MOVED)
    self.log+=' * src:%s\n * dest:%s\n'%(self.nd_download_abspath,A.dirname(self.move_abspath_local))
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def _move_file_for_cloud(self):
  try:
   flag_move_file=F
   if A.exists(self.move_abspath_cloud):
    logger.debug('같은 파일 있음')
    self.log+='- 원격폴더 같은 파일 있음\n'
    if A.getsize(self.nd_download_abspath)==A.getsize(self.move_abspath_cloud):
     logger.debug('사이즈가 같아 그냥 삭제')
     self.log+='- 사이즈가 같아 삭제\n'
     G(self.nd_download_abspath)
     flag_move_file=H
    else:
     logger.debug('사이즈가 달라 기존 파일 삭제')
     self.log+='- 사이즈가 달라 기존 파일 삭제\n'
     try:
      G(self.move_abspath_cloud)
     except:
      logger.debug('원격파일 삭제 실패')
     self.set_scan_status(EntityShow.ScanStatus.DELETE_FILE)
   if flag_move_file:
    sync_path=A.join(self.nd_download_path,self.nd_find_library_path.entity_library_root.get_local_temp())
    logger.debug('sync_path : %s',sync_path)
    if not A.exists(sync_path):
     j(sync_path)
    basename=A.basename(self.nd_find_library_path.entity_library_root.mount_path)
    splits=self._path_split(self.scan_abspath)
    idx=splits.index(basename)
    for _ in splits[idx:]:
     sync_path=A.join(sync_path,_)
     if not A.exists(sync_path):
      if not A.exists(sync_path):
       j(sync_path)
       logger.debug('sync_path2 mkdir: %s',sync_path)
    self.move_abspath_sync=A.join(sync_path,self.filename)
    logger.debug('Movefile for cloud %s %s',self.nd_download_abspath,sync_path)
    if A.exists(A.join(sync_path,self.filename)):
     logger.debug('already file exist.. exist file remove : %s',A.join(sync_path,self.filename))
     G(A.join(sync_path,self.filename))
    if A.exists(self.nd_download_abspath):
     q(self.nd_download_abspath,sync_path)
     logger.debug('Real move..')
    self.set_scan_status(EntityShow.ScanStatus.MOVED)
    self.log+=' * src:%s\n * dest:%s\n'%(self.nd_download_abspath,sync_path)
  except i as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def set_scan_status(self,status):
  self.scan_status=status
  if status==EntityShow.ScanStatus.SCAN_COMPLETED:
   self.scan_time=u.now()
 def get_finalpath(self):
  if self.move_type==EntityLibraryPathRoot.DriveType.LOCAL:
   return self.move_abspath_local
  else:
   return self.move_abspath_cloud 
 def _path_split(self,p,l=d):
  if l is d:
   l=[]
  if p==A.dirname(p):
   l.insert(0,A.dirname(p)) 
   return l
  else:
   l.insert(0,A.basename(p))
  return self._path_split(A.dirname(p),l)
if __name__=='__main__':
 pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
