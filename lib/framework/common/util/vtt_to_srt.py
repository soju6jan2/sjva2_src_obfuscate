import re
p=None
h=str
Q=re.sub
o=re.compile
def convert_vtt_to_srt(fileContents):
 data=_step1(fileContents).strip()
 regex=o(r'\d{2}:\d{2}(:\d{2})?(,\d{3})?\s-->\s\d{2}:\d{2}(:\d{2})?(,\d{3})?')
 ret=[]
 idx=1
 pre_line=p
 for tmp in data.split('\n'):
  match=regex.match(tmp)
  if match:
   if pre_line is not p and pre_line!=h(idx):
    ret.append(h(idx))
   idx+=1
  ret.append(tmp.strip())
  pre_line=tmp.strip()
 data='\n'.join(ret).strip()
 data=data.replace('&nbsp;',' ')
 return data
def _step1(fileContents):
 fileContents=fileContents.replace('\r\n','\n')
 replacement=Q(r'(\d\d:\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n',r'\1,\2 --> \3,\4\n',fileContents)
 replacement=Q(r'(\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n',r'\1,\2 --> \3,\4\n',replacement)
 replacement=Q(r'(\d\d).(\d\d\d) --> (\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n',r'\1,\2 --> \3,\4\n',replacement)
 replacement=Q(r'WEBVTT(.*?)?\n','',replacement)
 replacement=Q(r'Kind:[ \-\w]+\n','',replacement)
 replacement=Q(r'Language:[ \-\w]+\n','',replacement)
 replacement=Q(r'<c[.\w\d]*>','',replacement)
 replacement=Q(r'</c>','',replacement)
 replacement=Q(r'<\d\d:\d\d:\d\d.\d\d\d>','',replacement)
 replacement=Q(r'::[\-\w]+\([\-.\w\d]+\)[ ]*{[.,:;\(\) \-\w\d]+\n }\n','',replacement)
 replacement=Q(r'Style:\n##\n','',replacement)
 return replacement
# Created by pyminifier (https://github.com/liftoff/pyminifier)
