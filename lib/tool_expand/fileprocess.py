import os,re
import traceback
import time
import threading
import shutil
from framework import app
from.import logger
EXTENSION='mp4|avi|mkv|ts|wmv|m2ts|smi|srt|ass|m4v|flv|asf|mpg|ogm'
class ToolExpandFileProcess(object):
 @classmethod
 def remove_extension(cls,filename):
  ret=filename
  regex=r'(.*?)\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   ret=filename.replace('.'+match.group('ext'),'')
  return ret
 @classmethod
 def remove_small_file_and_move_target(cls,path,size,target=None,except_ext=None,small_move_path=None):
  try:
   if target is None:
    target=path
   if except_ext is None:
    except_ext=['.smi','.srt','ass']
   lists=os.listdir(path)
   for f in lists:
    try:
     file_path=os.path.join(path,f)
     except_file=False
     if os.path.splitext(file_path.lower())[1]in except_ext:
      except_file=True
     if os.path.isdir(file_path):
      cls.remove_small_file_and_move_target(file_path,size,target=target,except_ext=except_ext)
      if not os.listdir(file_path):
       logger.info('REMOVE DIR : %s',file_path)
       os.rmdir(file_path)
     else:
      if os.stat(file_path).st_size>1024*1024*size or except_file:
       if path==target:
        continue
       try:
        logger.info('MOVE : %s',os.path.join(target,f))
       except:
        logger.info('MOVE')
       if os.path.exists(os.path.join(target,f)):
        logger.info(u'ALREADY in Target : %s',os.path.join(target,f))
        os.remove(file_path)
       else:
        shutil.move(file_path,os.path.join(target,f))
      else:
       if small_move_path is None or small_move_path=='':
        try:
         logger.info(u'FILE REMOVE : %s %s',file_path,os.stat(file_path).st_size)
        except:
         logger.info(u'FILE REMOVE')
        os.remove(file_path)
       else:
        logger.info(u'SNALL FILE MOVE : %s',file_path)
        shutil.move(file_path,os.path.join(small_move_path,f))
    except UnicodeDecodeError:
     pass
    except Exception as exception:
     logger.error('Exception:%s',exception)
     logger.error(traceback.format_exc())
  except Exception as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @classmethod
 def change_filename_censored(cls,filename):
  match=re.compile('\d{2}id',re.I).search(filename.lower())
  id_before=None
  if match:
   id_before=match.group(0)
   filename=filename.lower().replace(id_before,'zzid')
  filename=cls.change_filename_censored_old(filename)
  if id_before is not None:
   filename=filename.replace('zzid',id_before)
  try:
   if filename is not None:
    base,ext=os.path.splitext(filename)
    tmps=base.split('-')
    tmp2=tmps[1].split('cd')
    if len(tmp2)==1:
     tmp='%s-%s%s'%(tmps[0],str(int(tmps[1])).zfill(3),ext)
    elif len(tmp2)==2:
     tmp='%s-%scd%s%s'%(tmps[0],str(int(tmp2[0])).zfill(3),tmp2[1],ext)
    return tmp
  except Exception as exception:
   logger.debug('filename : %s',filename)
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return filename
 @classmethod
 def change_filename_censored_old(cls,filename):
  original_filename=filename
  filename=filename.lower()
  filename=filename.replace('-h264','')
  filename=filename.replace('-264','')
  filename=filename.replace('z_1080p','').replace('z_720p','')
  filename=filename.replace('z_','')
  filename=filename.replace('-c','')
  regex=r'^(?P<code>.*?)\.1080p\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^(?P<code>.*?)(\_|\-)fhd\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^\[.*?\]\d+(?P<code>.*?)\.(?P<ext>%s)$'
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^\[.*?\](?P<code>.*?)\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^\(.*?\)(?P<code>.*?)\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^\d{3,4}(?P<code>.*?)\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^.*\.com\-?\d*\-?\d*@?(?P<code>.*?)(\-h264)??\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^(?P<dummy>.*\.com.*?)(?P<code>[a-z]+)'
  match=re.compile(regex).match(filename)
  if match:
   filename=filename.replace(match.group('dummy'),'')
  regex=r'^(?P<code>.*?)\-5.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   filename='%s.%s'%(match.group('code'),match.group('ext'))
  regex=r'^s-cute\s(?P<code>\d{3}).*?.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   ret='scute-%s.%s'%(match.group('code'),match.group('ext'))
   return ret.lower()
  logger.debug('5. %s',filename)
  regex_list=[r'^(?P<name>[a-zA-Z]+)[-_]?(?P<no>\d+)(([-_]?(cd|part)?(?P<part_no>\d))|[-_]?(?P<part_char>\w))?\.(?P<ext>%s)$'%EXTENSION,r'^\w+.\w+@(?P<name>[a-zA-Z]+)[-_]?(?P<no>\d+)(([-_\.]?(cd|part)?(?P<part_no>\d))|[-_\.]?(?P<part_char>\w))?\.(?P<ext>%s)$'%EXTENSION]
  for regex in regex_list:
   match=re.compile(regex).match(filename)
   if match:
    ret=filename
    part=None
    if match.group('part_no')is not None:
     part='cd%s'%match.group('part_no')
    elif match.group('part_char')is not None:
     part='cd%s'%(ord(match.group('part_char').lower())-ord('a')+1)
    if part is None:
     ret='%s-%s.%s'%(match.group('name').lower(),match.group('no'),match.group('ext'))
    else:
     ret='%s-%s%s.%s'%(match.group('name').lower(),match.group('no'),part,match.group('ext'))
    return ret.lower()
  regex=r'(?P<name>[a-zA-Z]+\d+)\-(?P<no>\d+).*?\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   ret='%s-%s.%s'%(match.group('name'),match.group('no'),match.group('ext'))
   return ret.lower()
  regex=r'^(?P<name>[a-zA-Z]{3,})\-?(?P<no>\d+).*?\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(filename)
  if match:
   ret='%s-%s.%s'%(match.group('name'),match.group('no'),match.group('ext'))
   return ret.lower()
  regex=r'^(?P<name>[a-zA-Z]{3,})\-?(?P<no>\d+).*?\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(original_filename)
  if match:
   ret='%s-%s.%s'%(match.group('name'),match.group('no'),match.group('ext'))
   return ret.lower()
  regex=r'(?P<name>[a-zA-Z]+)\-(?P<no>\d+).*?\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).search(filename)
  if match:
   ret='%s-%s.%s'%(match.group('name'),match.group('no'),match.group('ext'))
   logger.debug('N1. %s -> %s'%(file,ret))
   logger.debug('match 22')
   return ret.lower()
  regex=r'(?P<name>[a-zA-Z]+)\-(?P<no>\d+).*?\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).search(original_filename)
  if match:
   ret='%s-%s.%s'%(match.group('name'),match.group('no'),match.group('ext'))
   return ret.lower()
  regex=r'\w+.\w+@(?P<name>[a-zA-Z]+)(?P<no>\d{5})\.(cd|part)(?P<part_no>\d+)\.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).match(original_filename)
  if match:
   ret=filename
   part=None
   if match.group('part_no')is not None:
    part='cd%s'%match.group('part_no')
   if part is None:
    ret='%s-%s.%s'%(match.group('name').lower(),match.group('no'),match.group('ext'))
   else:
    ret='%s-%s%s.%s'%(match.group('name').lower(),match.group('no'),part,match.group('ext'))
   return ret.lower()
  regex=r'\w+.\w+@(?P<name>[a-zA-Z]+)(?P<no>\d{5}).*?.(?P<ext>%s)$'%EXTENSION
  match=re.compile(regex).search(original_filename)
  if match:
   no=match.group('no').replace('0','').zfill(3)
   ret='%s-%s.%s'%(match.group('name'),no,match.group('ext'))
   return ret.lower()
  return None
# Created by pyminifier (https://github.com/liftoff/pyminifier)
