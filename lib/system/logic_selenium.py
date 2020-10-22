import os
H=None
I=object
h=staticmethod
e=str
j=Exception
i=True
C=False
VC=sum
u=os.path
import traceback
V=traceback.format_exc
import logging
import platform
m=platform.system
import time
T=time.sleep
VA=time.time
import base64
Vo=base64.b64decode
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from selenium import webdriver
VI=webdriver.Chrome
Vz=webdriver.Remote
Vw=webdriver.ChromeOptions
VD=webdriver.support
from selenium.VD.ui import WebDriverWait
from PIL import Image
VR=Image.new
Vj=Image.open
Vh=Image.MAX_IMAGE_PIXELS
Vh=H
from io import BytesIO
from framework.logger import get_logger
from framework import path_app_root,path_data
from.plugin import logger,package_name
D=logger.error
o=logger.debug
from.model import ModelSetting
Vi=ModelSetting.get_list
w=ModelSetting.get
class SystemLogicSelenium(I):
 chrome_driver=H
 chrome_driver_list=[]
 @h
 def process_ajax(sub,req):
  try:
   if sub=='selenium_test_go':
    driver=SystemLogicSelenium.get_driver()
    driver.get(req.form['url'])
    return jsonify('success')
   elif sub=='capture':
    driver=SystemLogicSelenium.get_driver()
    img=Vj(BytesIO((driver.get_screenshot_as_png())))
    timestamp=VA()
    timestamp=e(timestamp).split('.')[0]
    tmp=u.join(path_data,'tmp','%s.png'%timestamp)
    img.save(tmp)
    from system.model import ModelSetting as SystemModelSetting
          Vi=ModelSetting.get_list
          w=ModelSetting.get
    ddns=SystemModelSetting.get('ddns')
    url='%s/open_file%s'%(ddns,tmp.replace(path_app_root,''))
    o(url)
    ret={}
    ret['ret']='success'
    ret['data']=url
    return jsonify(ret)
   elif sub=='full_capture':
    driver=SystemLogicSelenium.get_driver()
    img=SystemLogicSelenium.full_screenshot(driver)
    timestamp=VA()
    timestamp=e(timestamp).split('.')[0]
    tmp=u.join(path_data,'tmp','%s.png'%timestamp)
    img.save(tmp)
    return send_file(tmp,mimetype='image/png')
   elif sub=='cookie':
    driver=SystemLogicSelenium.get_driver()
    data=driver.get_cookies()
    return jsonify(data)
  except j as e:
   D('Exception:%s',e)
   D(V())
   return jsonify('exception')
 @h
 def get_pagesoruce_by_selenium(url,wait_xpath,retry=i):
  try:
   o('get_pagesoruce_by_selenium:%s %s',url,wait_xpath)
   driver=SystemLogicSelenium.get_driver()
   driver.get(url)
   WebDriverWait(driver,30).until(lambda driver:driver.find_element_by_xpath(wait_xpath))
   o('return page_source') 
   return driver.page_source
  except j as e:
   D('Exception:%s',e)
   D(V())
   SystemLogicSelenium.chrome_driver=H
   if retry:
    return SystemLogicSelenium.get_pagesoruce_by_selenium(url,wait_xpath,retry=C)
 @h
 def get_driver(chrome_options=H):
  try:
   if SystemLogicSelenium.chrome_driver is H:
    SystemLogicSelenium.chrome_driver=SystemLogicSelenium.inner_create_driver(chrome_options)
   return SystemLogicSelenium.chrome_driver
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def create_driver(chrome_options=H):
  try:
   driver=SystemLogicSelenium.inner_create_driver(chrome_options)
   if driver is not H:
    SystemLogicSelenium.chrome_driver_list.append(driver)
    return driver
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def close_driver():
  try:
   if SystemLogicSelenium.chrome_driver is not H:
    SystemLogicSelenium.chrome_driver.quit()
    SystemLogicSelenium.chrome_driver=H
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def inner_create_driver(chrome_options):
  try:
   driver=H
   remote_url=w('selenium_remote_url')
   if remote_url.endswith('/wd/hub/'):
    remote_url=remote_url[:-1]
   if remote_url!='':
    if chrome_options is H:
     chrome_options=Vw()
     tmp=Vi('selenium_remote_default_option')
     for t in tmp:
      chrome_options.add_argument(t)
    driver=Vz(command_executor=remote_url,desired_capabilities=chrome_options.to_capabilities())
    driver.set_window_size(1920,1080)
    o('Using Remote :%s',driver)
   else:
    path_chrome=u.join(path_app_root,'bin',m(),'chromedriver')
    if m()=='Windows':
     path_chrome+='.exe'
    if chrome_options is H:
     chrome_options=Vw()
     tmp=Vi('selenium_binary_default_option')
     for t in tmp:
      chrome_options.add_argument(t)
    driver=VI(path_chrome,chrome_options=chrome_options)
    o('Using local bin :%s',driver)
   if driver is not H:
    return driver
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def plugin_unload():
  try:
   o(SystemLogicSelenium.chrome_driver)
   if SystemLogicSelenium.chrome_driver is not H:
    SystemLogicSelenium.chrome_driver.quit()
    o(SystemLogicSelenium.chrome_driver)
   for tmp in SystemLogicSelenium.chrome_driver_list:
    if tmp is not H:
     tmp.quit()
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def get_text_excluding_children(driver,element):
  return driver.execute_script("""
        return jQuery(arguments[0]).contents().filter(function() {return this.nodeType == Node.TEXT_NODE; }).text();
        """  , element)
 @h
 def full_screenshot(driver,low_offset=0):
  try:
   img_li=[] 
   offset=0 
   height=driver.execute_script('return Math.max(' 'document.documentElement.clientHeight, window.innerHeight);')
   max_window_height=driver.execute_script('return Math.max(' 'document.body.scrollHeight, ' 'document.body.offsetHeight, ' 'document.documentElement.clientHeight, ' 'document.documentElement.scrollHeight, ' 'document.documentElement.offsetHeight);')
   while offset<max_window_height:
    driver.execute_script("""
                window.scrollTo(0, arguments[0]);
                """    , offset)
    img=Vj(BytesIO((driver.get_screenshot_as_png())))
    if low_offset!=0:
     img=img.crop((0,0,img.width,img.height-low_offset))
    img_li.append(img)
    offset+=height
    o('offset : %s / %s',offset,max_window_height)
   img_frame_height=VC([img_frag.size[1]for img_frag in img_li])
   img_frame=VR('RGB',(img_li[0].size[0],img_frame_height))
   offset=0
   for img_frag in img_li:
    img_frame.paste(img_frag,(0,offset))
    offset+=img_frag.size[1]
    o('paste offset : %s ',offset)
   return img_frame
  except j as e:
   D('Exception:%s',e)
   D(V())
 @h
 def remove_element(driver,element):
  driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """  , element)
 @h
 def __get_downloaded_files(driver=H):
  if driver is H:
   driver=SystemLogicSelenium.get_driver()
  if not driver.current_url.startswith("chrome://downloads"):
   driver.get("chrome://downloads/")
  return driver.execute_script("return downloads.Manager.get().items_   " "  .filter(e => e.state === 'COMPLETE')  " "  .map(e => e.filePath || e.file_path); ")
 @h
 def get_file_content(path,driver=H):
  if driver is H:
   driver=SystemLogicSelenium.get_driver()
  elem=driver.execute_script("var input = window.document.createElement('INPUT'); " "input.setAttribute('type', 'file'); " "input.hidden = true; " "input.onchange = function (e) { e.stopPropagation() }; " "return window.document.documentElement.appendChild(input); ")
  elem._execute('sendKeysToElement',{'value':[path],'text':path})
  result=driver.execute_async_script("var input = arguments[0], callback = arguments[1]; " "var reader = new FileReader(); " "reader.onload = function (ev) { callback(reader.result) }; " "reader.onerror = function (ex) { callback(ex.message) }; " "reader.readAsDataURL(input.files[0]); " "input.remove(); ",elem)
  if not result.startswith('data:'):
   raise j("Failed to get file content: %s"%result)
  return Vo(result[result.find('base64,')+7:])
 @h
 def get_downloaded_files(driver=H):
  if driver is H:
   driver=SystemLogicSelenium.get_driver()
  files=SystemLogicSelenium.__get_downloaded_files()
  return files
 @h
 def waitUntilDownloadCompleted(maxTime=600,driver=H):
  if driver is H:
   driver=SystemLogicSelenium.get_driver()
  driver.execute_script("window.open()")
  driver.switch_to.window(driver.window_handles[-1])
  driver.get('chrome://downloads')
  endTime=VA()+maxTime
  while i:
   try:
    downloadPercentage=driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
    if downloadPercentage==100:
     return downloadPercentage
   except:
    pass
   T(1)
   if VA()>endTime:
    break
"""
driver = webdriver.Chrome(desired_capabilities=capabilities_chrome)
#driver = webdriver.Remote('http://127.0.0.1:5555/wd/hub', capabilities_chrome)
# download a pdf file
driver.get("https://www.mozilla.org/en-US/foundation/documents")
driver.find_element_by_css_selector("[href$='.pdf']").click()
# list all the completed remote files (waits for at least one)
files = WebDriverWait(driver, 20, 1).until(get_downloaded_files)
# get the content of the first file remotely
content = get_file_content(driver, files[0])
# save the content in a local file in the working directory
with open(os.path.basename(files[0]), 'wb') as f:
  f.write(content)
capabilities_chrome = {'browserName': 'chrome', # 'proxy': {# 'sslProxy': '50.59.162.78:8088', # 'httpProxy': '50.59.162.78:8088' # }, 'goog:chromeOptions': {'args': [], 'prefs': {# 'download.directory_upgrade': True, 'download.prompt_for_download': False, 'plugins.always_open_pdf_externally': True, 'safebrowsing_for_trusted_sources_enabled': False } } }
"""
# Created by pyminifier (https://github.com/liftoff/pyminifier)
