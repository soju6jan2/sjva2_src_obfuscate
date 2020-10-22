import os
f=object
L=staticmethod
A=abs
I=True
M=False
h=int
S=Exception
T=iter
N=None
P=str
B=len
Q=classmethod
X=isinstance
J=dir
F=TypeError
import json
import traceback
import platform
import subprocess
from sqlalchemy.ext.declarative import DeclarativeMeta
from framework.logger import get_logger
from framework import app
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Util(f):
 @L
 def sizeof_fmt(num,suffix='Bytes'):
  for unit in['','K','M','G','T','P','E','Z']:
   if A(num)<1024.0:
    return "%3.1f%s%s"%(num,unit,suffix)
   num/=1024.0
  return "%.1f%s%s"%(num,'Y',suffix)
 @L
 def db_list_to_dict(db_list):
  ret={}
  for item in db_list:
   ret[item.key]=item.value
  return ret
 @L
 def db_to_dict(db_list):
  ret=[]
  for item in db_list:
   ret.append(item.as_dict())
  return ret
 @L
 def get_paging_info(count,current_page,page_size):
  try:
   paging={}
   paging['prev_page']=I
   paging['next_page']=I
   if current_page<=10:
    paging['prev_page']=M
   paging['total_page']=h(count/page_size)+1
   if count%page_size==0:
    paging['total_page']-=1
   paging['start_page']=h((current_page-1)/10)*10+1
   paging['last_page']=paging['total_page']if paging['start_page']+9>paging['total_page']else paging['start_page']+9
   if paging['last_page']==paging['total_page']:
    paging['next_page']=M
   paging['current_page']=current_page
   paging['count']=count
   logger.debug('paging : c:%s %s %s %s %s %s',count,paging['total_page'],paging['prev_page'],paging['next_page'],paging['start_page'],paging['last_page'])
   return paging
  except S as exception:
   logger.debug('Exception:%s',exception)
   logger.debug(traceback.format_exc())
 @L
 def get_list_except_empty(source):
  tmp=[]
  for _ in source:
   if _.strip().startswith('#'):
    continue
   if _.strip()!='':
    tmp.append(_.strip())
  return tmp
 @L
 def save_from_dict_to_json(d,filename):
  try:
   import codecs
   s=json.dumps(d)
   ofp=codecs.open(filename,'w',encoding='utf8')
   ofp.write(s)
   ofp.close()
  except S as exception:
   logger.debug('Exception:%s',exception)
   logger.debug(traceback.format_exc())
 @L
 def execute_command(command):
  try:
   logger.debug('COMMAND RUN START : %s',command)
   if platform.system()=='Windows':
    new_command=[]
    for c in command:
     new_command.append(c.encode('cp949'))
    command=new_command
   ret=[]
   if app.config['config']['is_py2']:
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=I,bufsize=1)
    with p.stdout:
     for line in T(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except S as exception:
       try:
        line=line.decode('cp949')
       except S as exception:
        pass
      ret.append(line.strip())
     p.wait()
   else:
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=I)
    with p.stdout:
     for line in T(p.stdout.readline,''):
      ret.append(line.strip())
     p.wait()
   logger.debug('COMMAND RUN END : %s',command)
   return ret
  except S as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @L
 def change_text_for_use_filename(text):
  try:
   import re
   return re.sub('[\\/:*?\"<>|]','',text).strip()
  except S as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc()) 
 @L
 def get_max_size_fileinfo(torrent_info):
  try:
   ret={}
   max_size=-1
   max_filename=N
   for t in torrent_info['files']:
    if t['size']>max_size:
     max_size=t['size']
     max_filename=P(t['path'])
   t=max_filename.split('/')
   ret['filename']=t[-1]
   if B(t)==1:
    ret['dirname']=''
   elif B(t)==2:
    ret['dirname']=t[0]
   else:
    ret['dirname']=max_filename.replace('/%s'%ret['filename'],'')
   ret['max_size']=max_size
   return ret
  except S as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @L
 def makezip(zip_path):
  import zipfile
  try:
   if os.path.isdir(zip_path):
    zipfilename=os.path.join(os.path.dirname(zip_path),'%s.zip'%os.path.basename(zip_path))
    fantasy_zip=zipfile.ZipFile(zipfilename,'w')
    for f in os.listdir(zip_path):
     src=os.path.join(zip_path,f)
     fantasy_zip.write(src,os.path.basename(src),compress_type=zipfile.ZIP_DEFLATED)
    fantasy_zip.close()
   import shutil
   shutil.rmtree(zip_path)
   return I
  except S as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
  return M
class SingletonClass(f):
 __instance=N
 @Q
 def __getInstance(cls):
  return cls.__instance
 @Q
 def instance(cls,*args,**kargs):
  cls.__instance=cls(*args,**kargs)
  cls.instance=cls.__getInstance
  return cls.__instance
class AlchemyEncoder(json.JSONEncoder):
 def default(self,obj):
  if X(obj.__class__,DeclarativeMeta):
   fields={}
   for field in[x for x in J(obj)if not x.startswith('_')and x!='metadata']:
    data=obj.__getattribute__(field)
    try:
     json.dumps(data)
     fields[field]=data
    except F:
     fields[field]=N
   return fields
  return json.JSONEncoder.default(self,obj)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
