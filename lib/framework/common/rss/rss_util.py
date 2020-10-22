import os
U=object
E=staticmethod
b=len
u=Exception
x=None
import traceback
a=traceback.format_exc
import logging
import urllib
import xml.etree.ElementTree as ET
from framework import logger,py_urllib2
t=py_urllib2.urlopen
V=py_urllib2.Request
g=logger.error
y=logger.debug
class RssUtil(U):
 @E
 def get_rss(url):
  try:
   y('get_rss : %s',url)
   req=V(url)
   req.add_header('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36')
   resp=t(req)
   tree=ET.ElementTree(file=resp)
   root=tree.getroot()
   item_list=root.find('channel').findall('item')
   y('xml item count:%s',b(item_list))
   ret=[]
   for item in item_list:
    try:
     link=item.find('link').text.strip()
     if link.startswith('magnet'):
      try:
       link=link[0:60]
      except:
       g(e)
       g(a())
       link=item.find('link').text.strip()
     rss=Feed(item.find('title').text.strip(),link)
     ret.append(rss)
    except u as e:
     y(e)
     y(a())
   return ret
  except u as e:
   y(e)
   y(a())
   y('url:%s',url)
   return x
 """
    @staticmethod
    def make_rss(title, rss_list, torrent_mode, ddns, is_bot=False):
        xml = '<rss xmlns:showrss=\"http://showrss.info/\" version=\"2.0\">\n'
        xml += '\t<channel>\n'
        xml += '\t\t<title>' + '%s</title>\n' % title
        xml += '\t\t<link></link>\n'
        xml += '\t\t<description></description>\n'
        for bbs in rss_list:
            for download in bbs.files:
                try:
                    item_str = '\t\t<item>\n'
                    if download.filename.lower().endswith('.smi') or download.filename.lower().endswith('.srt') or download.filename.lower().endswith('.ass') or download.filename.lower().endswith('.ssa') or download.filename.lower().endswith('.sub'):
                        tmp = '\t\t\t<title>[자막]%s</title>\n' % TorrentSite.replace_xml(bbs.title)
                    else:
                        tmp = '\t\t\t<title>%s</title>\n' % TorrentSite.replace_xml(bbs.title)
                    item_str += tmp
                    if torrent_mode == 'magnet' and download.is_torrent:
                        item_str += '\t\t\t<link>%s</link>\n' % download.magnet
                    else:  
                        if is_bot:
                            item_str += '\t\t\t<link>%s/rss/download_bot/%s</link>\n' % (ddns, download.id)
                        else:
                            item_str += '\t\t\t<link>%s/rss/download/%s</link>\n' % (ddns, download.id)
                    item_str += '\t\t\t<description>%s</description>\n' % TorrentSite.replace_xml(download.filename)
                    date_str = bbs.created_time.strftime("%a, %d %b %Y %H:%M:%S") + ' +0900'
                    item_str += '\t\t\t<pubDate>%s</pubDate>\n' % date_str
                    item_str += '\t\t</item>\n'
                    xml += item_str
                except Exception as e:
                    logger.debug('Exception:%s', e)
                    logger.debug(traceback.format_exc())
        xml += '\t</channel>\n'
        xml += '</rss>'
        return xml
    """ 
 @E
 def replace_xml(xml):
  tmp=[['&','&amp;'],['<','&lt;'],['>','&gt;'],['‘','&apos;'],['"','&quot;']]
  for t in tmp:
   xml=xml.replace(t[0],t[1])
  return xml
 @E
 def make_rss(package_name,rss_list):
  xml='<rss xmlns:showrss=\"http://showrss.info/\" version=\"2.0\">\n'
  xml+='\t<channel>\n'
  xml+='\t\t<title>'+'%s</title>\n'%package_name
  xml+='\t\t<link></link>\n'
  xml+='\t\t<description></description>\n'
  for bbs in rss_list:
   try:
    item_str='\t\t<item>\n'
    tmp='\t\t\t<title>%s</title>\n'%RssUtil.replace_xml(bbs['title'])
    item_str+=tmp
    item_str+='\t\t\t<link>%s</link>\n'%RssUtil.replace_xml(bbs['link'])
    date_str=bbs['created_time'].strftime("%a, %d %b %Y %H:%M:%S")+' +0900'
    item_str+='\t\t\t<pubDate>%s</pubDate>\n'%date_str
    item_str+='\t\t</item>\n'
    xml+=item_str
   except u as e:
    y('Exception:%s',e)
    y(a())
  xml+='\t</channel>\n'
  xml+='</rss>'
  return xml
class Feed(U):
 def __init__(self,title,link):
  self.title=title
  self.link=link
# Created by pyminifier (https://github.com/liftoff/pyminifier)
