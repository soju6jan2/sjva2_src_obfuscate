import os
T=object
tC=staticmethod
tQ=abs
f=True
Y=False
R=int
P=Exception
tp=iter
E=None
tV=str
i=len
td=classmethod
tP=isinstance
tK=dir
tW=TypeError
j=os.listdir
b=os.path
import json
tF=json.JSONEncoder
tl=json.dumps
import traceback
t=traceback.format_exc
import platform
tg=platform.system
import subprocess
tR=subprocess.STDOUT
tq=subprocess.PIPE
tr=subprocess.Popen
from sqlalchemy.ext.declarative import DeclarativeMeta
from framework.logger import get_logger
from framework import app
e=app.config
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Util(T):
 @tC
 def sizeof_fmt(num,suffix='Bytes'):
  for unit in['','K','M','G','T','P','E','Z']:
   if tQ(num)<1024.0:
    return "%3.1f%s%s"%(num,unit,suffix)
   num/=1024.0
  return "%.1f%s%s"%(num,'Y',suffix)
 @tC
 def db_list_to_dict(db_list):
  ret={}
  for item in db_list:
   ret[item.key]=item.value
  return ret
 @tC
 def db_to_dict(db_list):
  ret=[]
  for item in db_list:
   ret.append(item.as_dict())
  return ret
 @tC
 def get_paging_info(count,current_page,page_size):
  try:
   paging={}
   paging['prev_page']=f
   paging['next_page']=f
   if current_page<=10:
    paging['prev_page']=Y
   paging['total_page']=R(count/page_size)+1
   if count%page_size==0:
    paging['total_page']-=1
   paging['start_page']=R((current_page-1)/10)*10+1
   paging['last_page']=paging['total_page']if paging['start_page']+9>paging['total_page']else paging['start_page']+9
   if paging['last_page']==paging['total_page']:
    paging['next_page']=Y
   paging['current_page']=current_page
   paging['count']=count
   logger.debug('paging : c:%s %s %s %s %s %s',count,paging['total_page'],paging['prev_page'],paging['next_page'],paging['start_page'],paging['last_page'])
   return paging
  except P as e:
   logger.debug('Exception:%s',e)
   logger.debug(t())
 @tC
 def get_list_except_empty(source):
  tmp=[]
  for _ in source:
   if _.strip().startswith('#'):
    continue
   if _.strip()!='':
    tmp.append(_.strip())
  return tmp
 @tC
 def save_from_dict_to_json(d,filename):
  try:
   import codecs
   s=tl(d)
   ofp=codecs.open(filename,'w',encoding='utf8')
   ofp.write(s)
   ofp.close()
  except P as e:
   logger.debug('Exception:%s',e)
   logger.debug(t())
 @tC
 def execute_command(command):
  try:
   logger.debug('COMMAND RUN START : %s',command)
   if tg()=='Windows':
    new_command=[]
    for c in command:
     new_command.append(c.encode('cp949'))
    command=new_command
   ret=[]
   if e['config']['is_py2']:
    p=tr(command,stdin=tq,stdout=tq,stderr=tR,universal_newlines=f,bufsize=1)
    with p.stdout:
     for line in tp(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except P as e:
       try:
        line=line.decode('cp949')
       except P as e:
        pass
      ret.append(line.strip())
     p.wait()
   else:
    p=tr(command,stdin=tq,stdout=tq,stderr=tR,universal_newlines=f)
    with p.stdout:
     for line in tp(p.stdout.readline,''):
      ret.append(line.strip())
     p.wait()
   logger.debug('COMMAND RUN END : %s',command)
   return ret
  except P as e:
   logger.error('Exception:%s',e)
   logger.error(t()) 
 @tC
 def change_text_for_use_filename(text):
  try:
   import re
   return re.sub('[\\/:*?\"<>|]','',text).strip()
  except P as e:
   logger.error('Exception:%s',e)
   logger.error(t()) 
 @tC
 def get_max_size_fileinfo(torrent_info):
  try:
   ret={}
   max_size=-1
   max_filename=E
   for t in torrent_info['files']:
    if t['size']>max_size:
     max_size=t['size']
     max_filename=tV(t['path'])
   t=max_filename.split('/')
   ret['filename']=t[-1]
   if i(t)==1:
    ret['dirname']=''
   elif i(t)==2:
    ret['dirname']=t[0]
   else:
    ret['dirname']=max_filename.replace('/%s'%ret['filename'],'')
   ret['max_size']=max_size
   return ret
  except P as e:
   logger.error('Exception:%s',e)
   logger.error(t())
 @tC
 def makezip(zip_path):
  import zipfile
  try:
   if b.isdir(zip_path):
    zipfilename=b.join(b.dirname(zip_path),'%s.zip'%b.basename(zip_path))
    fantasy_zip=zipfile.ZipFile(zipfilename,'w')
    for f in j(zip_path):
     src=b.join(zip_path,f)
     fantasy_zip.write(src,b.basename(src),compress_type=zipfile.ZIP_DEFLATED)
    fantasy_zip.close()
   import shutil
   shutil.rmtree(zip_path)
   return f
  except P as e:
   logger.error('Exception:%s',e)
   logger.error(t())
  return Y
class SingletonClass(T):
 __instance=E
 @td
 def __getInstance(cls):
  return cls.__instance
 @td
 def instance(cls,*args,**kargs):
  cls.__instance=cls(*args,**kargs)
  cls.instance=cls.__getInstance
  return cls.__instance
class AlchemyEncoder(tF):
 def default(self,obj):
  if tP(obj.__class__,DeclarativeMeta):
   fields={}
   for field in[x for x in tK(obj)if not x.startswith('_')and x!='metadata']:
    data=obj.__getattribute__(field)
    try:
     tl(data)
     fields[field]=data
    except tW:
     fields[field]=E
   return fields
  return tF.default(self,obj)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
