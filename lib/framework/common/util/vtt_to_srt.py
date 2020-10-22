import re
U=None
S=str
r=re.sub
p=re.compile
def convert_vtt_to_srt(fileContents):
 data=_step1(fileContents).strip()
 regex=p(r'\d{2}:\d{2}(:\d{2})?(,\d{3})?\s-->\s\d{2}:\d{2}(:\d{2})?(,\d{3})?')
 ret=[]
 idx=1
 pre_line=U
 for tmp in data.split('\n'):
  match=regex.match(tmp)
  if match:
   if pre_line is not U and pre_line!=S(idx):
    ret.append(S(idx))
   idx+=1
  ret.append(tmp.strip())
  pre_line=tmp.strip()
 data='\n'.join(ret).strip()
 data=data.replace('&nbsp;',' ')
 return data
def _step1(fileContents):
 fileContents=fileContents.replace('\r\n','\n')
 replacement=r(r'(\d\d:\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n',r'\1,\2 --> \3,\4\n',fileContents)
 replacement=r(r'(\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n',r'\1,\2 --> \3,\4\n',replacement)
 replacement=r(r'(\d\d).(\d\d\d) --> (\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n',r'\1,\2 --> \3,\4\n',replacement)
 replacement=r(r'WEBVTT(.*?)?\n','',replacement)
 replacement=r(r'Kind:[ \-\w]+\n','',replacement)
 replacement=r(r'Language:[ \-\w]+\n','',replacement)
 replacement=r(r'<c[.\w\d]*>','',replacement)
 replacement=r(r'</c>','',replacement)
 replacement=r(r'<\d\d:\d\d:\d\d.\d\d\d>','',replacement)
 replacement=r(r'::[\-\w]+\([\-.\w\d]+\)[ ]*{[.,:;\(\) \-\w\d]+\n }\n','',replacement)
 replacement=r(r'Style:\n##\n','',replacement)
 return replacement
# Created by pyminifier (https://github.com/liftoff/pyminifier)
