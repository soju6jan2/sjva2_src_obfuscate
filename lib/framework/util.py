import os
P=object
t=staticmethod
H=abs
G=True
y=False
I=int
e=Exception
j=iter
o=None
N=str
f=len
b=classmethod
i=isinstance
n=dir
Q=TypeError
import json
import traceback
import platform
import subprocess
from sqlalchemy.ext.declarative import DeclarativeMeta
from framework.logger import get_logger
from framework import app
package_name=__name__.split('.')[0]
logger=get_logger(package_name)
class Util(P):
 @t
 def sizeof_fmt(num,suffix='Bytes'):
  for unit in['','K','M','G','T','P','E','Z']:
   if H(num)<1024.0:
    return "%3.1f%s%s"%(num,unit,suffix)
   num/=1024.0
  return "%.1f%s%s"%(num,'Y',suffix)
 @t
 def db_list_to_dict(db_list):
  ret={}
  for item in db_list:
   ret[item.key]=item.value
  return ret
 @t
 def db_to_dict(db_list):
  ret=[]
  for item in db_list:
   ret.append(item.as_dict())
  return ret
 @t
 def get_paging_info(count,current_page,page_size):
  try:
   paging={}
   paging['prev_page']=G
   paging['next_page']=G
   if current_page<=10:
    paging['prev_page']=y
   paging['total_page']=I(count/page_size)+1
   if count%page_size==0:
    paging['total_page']-=1
   paging['start_page']=I((current_page-1)/10)*10+1
   paging['last_page']=paging['total_page']if paging['start_page']+9>paging['total_page']else paging['start_page']+9
   if paging['last_page']==paging['total_page']:
    paging['next_page']=y
   paging['current_page']=current_page
   paging['count']=count
   logger.debug('paging : c:%s %s %s %s %s %s',count,paging['total_page'],paging['prev_page'],paging['next_page'],paging['start_page'],paging['last_page'])
   return paging
  except e as e:
   logger.debug('Exception:%s',e)
   logger.debug(traceback.format_exc())
 @t
 def get_list_except_empty(source):
  tmp=[]
  for _ in source:
   if _.strip().startswith('#'):
    continue
   if _.strip()!='':
    tmp.append(_.strip())
  return tmp
 @t
 def save_from_dict_to_json(d,filename):
  try:
   import codecs
   s=json.dumps(d)
   ofp=codecs.open(filename,'w',encoding='utf8')
   ofp.write(s)
   ofp.close()
  except e as e:
   logger.debug('Exception:%s',e)
   logger.debug(traceback.format_exc())
 @t
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
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=G,bufsize=1)
    with p.stdout:
     for line in j(p.stdout.readline,b''):
      try:
       line=line.decode('utf-8')
      except e as e:
       try:
        line=line.decode('cp949')
       except e as e:
        pass
      ret.append(line.strip())
     p.wait()
   else:
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=G)
    with p.stdout:
     for line in j(p.stdout.readline,''):
      ret.append(line.strip())
     p.wait()
   logger.debug('COMMAND RUN END : %s',command)
   return ret
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @t
 def change_text_for_use_filename(text):
  try:
   import re
   return re.sub('[\\/:*?\"<>|]','',text).strip()
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc()) 
 @t
 def get_max_size_fileinfo(torrent_info):
  try:
   ret={}
   max_size=-1
   max_filename=o
   for t in torrent_info['files']:
    if t['size']>max_size:
     max_size=t['size']
     max_filename=N(t['path'])
   t=max_filename.split('/')
   ret['filename']=t[-1]
   if f(t)==1:
    ret['dirname']=''
   elif f(t)==2:
    ret['dirname']=t[0]
   else:
    ret['dirname']=max_filename.replace('/%s'%ret['filename'],'')
   ret['max_size']=max_size
   return ret
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 @t
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
   return G
  except e as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
  return y
class SingletonClass(P):
 __instance=o
 @b
 def __getInstance(cls):
  return cls.__instance
 @b
 def instance(cls,*args,**kargs):
  cls.__instance=cls(*args,**kargs)
  cls.instance=cls.__getInstance
  return cls.__instance
class AlchemyEncoder(json.JSONEncoder):
 def default(self,obj):
  if i(obj.__class__,DeclarativeMeta):
   fields={}
   for field in[x for x in n(obj)if not x.startswith('_')and x!='metadata']:
    data=obj.__getattribute__(field)
    try:
     json.dumps(data)
     fields[field]=data
    except Q:
     fields[field]=o
   return fields
  return json.JSONEncoder.default(self,obj)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
