import os
y=object
Oc=staticmethod
OW=abs
R=True
i=False
A=int
J=Exception
Oq=iter
E=None
OM=str
x=len
OQ=classmethod
OJ=isinstance
OT=dir
OI=TypeError
l=os.listdir
k=os.path
import json
Oz=json.JSONEncoder
Od=json.dumps
import traceback
O=traceback.format_exc
import platform
Ou=platform.system
import subprocess
OA=subprocess.STDOUT
OC=subprocess.PIPE
Oe=subprocess.Popen
from sqlalchemy.ext.declarative import DeclarativeMeta
from framework.logger import get_logger
from framework import app
f=app.config
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Util(y):
 @Oc
 def sizeof_fmt(num,suffix='Bytes'):
  for unit in['','K','M','G','T','P','E','Z']:
   if OW(num)<1024.0:
    return "%3.1f%s%s"%(num,unit,suffix)
   num/=1024.0
  return "%.1f%s%s"%(num,'Y',suffix)
 @Oc
 def db_list_to_dict(db_list):
  ret={}
  for item in db_list:
   ret[item.key]=item.value
  return ret
 @Oc
 def db_to_dict(db_list):
  ret=[]
  for item in db_list:
   ret.append(item.as_dict())
  return ret
 @Oc
 def get_paging_info(count,current_page,page_size):
  try:
   paging={}
   paging['prev_page']=R
   paging['next_page']=R
   if current_page<=10:
    paging['prev_page']=i
   paging['total_page']=A(count/page_size)+1
   if count%page_size==0:
    paging['total_page']-=1
   paging['start_page']=A((current_page-1)/10)*10+1
   paging['last_page']=paging['total_page']if paging['start_page']+9>paging['total_page']else paging['start_page']+9
   if paging['last_page']==paging['total_page']:
    paging['next_page']=i
   paging['current_page']=current_page
   paging['count']=count
   logger.debug('paging : c:%s %s %s %s %s %s',count,paging['total_page'],paging['prev_page'],paging['next_page'],paging['start_page'],paging['last_page'])
   return paging
  except J as e:
   logger.debug('Exception:%s',e)
   logger.debug(O())
 @Oc
 def get_list_except_empty(source):
  tmp=[]
  for _ in source:
   if _.strip().startswith('#'):
    continue
   if _.strip()!='':
    tmp.append(_.strip())
  return tmp
 @Oc
 def save_from_dict_to_json(d,filename):
  try:
   import codecs
   s=Od(d)
   ofp=codecs.open(filename,'w',encoding='utf8')
   ofp.write(s)
   ofp.close()
  except J as e:
   logger.debug('Exception:%s',e)
   logger.debug(O())
 @Oc
 def execute_command(command):
  try:
   logger.debug('COMMAND RUN START : %s',command)
   if Ou()=='Windows':
    new_command=[]
    for c in command:
     new_command.append(c.encode('cp949'))
    command=new_command
   ret=[]
   if f['config']['is_py2']:
    p=Oe(command,stdin=OC,stdout=OC,stderr=OA,universal_newlines=R,bufsize=1)
    with p.stdout:
     for line in Oq(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except J as e:
       try:
        line=line.decode('cp949')
       except J as e:
        pass
      ret.append(line.strip())
     p.wait()
   else:
    p=Oe(command,stdin=OC,stdout=OC,stderr=OA,universal_newlines=R)
    with p.stdout:
     for line in Oq(p.stdout.readline,''):
      ret.append(line.strip())
     p.wait()
   logger.debug('COMMAND RUN END : %s',command)
   return ret
  except J as e:
   logger.error('Exception:%s',e)
   logger.error(O()) 
 @Oc
 def change_text_for_use_filename(text):
  try:
   import re
   return re.sub('[\\/:*?\"<>|]','',text).strip()
  except J as e:
   logger.error('Exception:%s',e)
   logger.error(O()) 
 @Oc
 def get_max_size_fileinfo(torrent_info):
  try:
   ret={}
   max_size=-1
   max_filename=E
   for t in torrent_info['files']:
    if t['size']>max_size:
     max_size=t['size']
     max_filename=OM(t['path'])
   t=max_filename.split('/')
   ret['filename']=t[-1]
   if x(t)==1:
    ret['dirname']=''
   elif x(t)==2:
    ret['dirname']=t[0]
   else:
    ret['dirname']=max_filename.replace('/%s'%ret['filename'],'')
   ret['max_size']=max_size
   return ret
  except J as e:
   logger.error('Exception:%s',e)
   logger.error(O())
 @Oc
 def makezip(zip_path):
  import zipfile
  try:
   if k.isdir(zip_path):
    zipfilename=k.join(k.dirname(zip_path),'%s.zip'%k.basename(zip_path))
    fantasy_zip=zipfile.ZipFile(zipfilename,'w')
    for f in l(zip_path):
     src=k.join(zip_path,f)
     fantasy_zip.write(src,k.basename(src),compress_type=zipfile.ZIP_DEFLATED)
    fantasy_zip.close()
   import shutil
   shutil.rmtree(zip_path)
   return R
  except J as e:
   logger.error('Exception:%s',e)
   logger.error(O())
  return i
class SingletonClass(y):
 __instance=E
 @OQ
 def __getInstance(cls):
  return cls.__instance
 @OQ
 def instance(cls,*args,**kargs):
  cls.__instance=cls(*args,**kargs)
  cls.instance=cls.__getInstance
  return cls.__instance
class AlchemyEncoder(Oz):
 def default(self,obj):
  if OJ(obj.__class__,DeclarativeMeta):
   fields={}
   for field in[x for x in OT(obj)if not x.startswith('_')and x!='metadata']:
    data=obj.__getattribute__(field)
    try:
     Od(data)
     fields[field]=data
    except OI:
     fields[field]=E
   return fields
  return Oz.default(self,obj)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
