import os
h=None
J=object
d=staticmethod
M=str
o=Exception
Y=True
x=False
E=sum
import traceback
import logging
import platform
import time
import base64
from flask import Blueprint,request,Response,send_file,render_template,redirect,jsonify
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
Image.MAX_IMAGE_PIXELS=h
from io import BytesIO
from framework.logger import get_logger
from framework import path_app_root,path_data
from.plugin import logger,package_name
from.model import ModelSetting
class SystemLogicSelenium(J):
 chrome_driver=h
 chrome_driver_list=[]
 @d
 def process_ajax(sub,req):
  try:
   if sub=='selenium_test_go':
    driver=SystemLogicSelenium.get_driver()
    driver.get(req.form['url'])
    return jsonify('success')
   elif sub=='capture':
    driver=SystemLogicSelenium.get_driver()
    img=Image.open(BytesIO((driver.get_screenshot_as_png())))
    timestamp=time.time()
    timestamp=M(timestamp).split('.')[0]
    tmp=os.path.join(path_data,'tmp','%s.png'%timestamp)
    img.save(tmp)
    from system.model import ModelSetting as SystemModelSetting
    ddns=SystemModelSetting.get('ddns')
    url='%s/open_file%s'%(ddns,tmp.replace(path_app_root,''))
    logger.debug(url)
    ret={}
    ret['ret']='success'
    ret['data']=url
    return jsonify(ret)
   elif sub=='full_capture':
    driver=SystemLogicSelenium.get_driver()
    img=SystemLogicSelenium.full_screenshot(driver)
    timestamp=time.time()
    timestamp=M(timestamp).split('.')[0]
    tmp=os.path.join(path_data,'tmp','%s.png'%timestamp)
    img.save(tmp)
    return send_file(tmp,mimetype='image/png')
   elif sub=='cookie':
    driver=SystemLogicSelenium.get_driver()
    data=driver.get_cookies()
    return jsonify(data)
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   return jsonify('exception')
 @d
 def get_pagesoruce_by_selenium(url,wait_xpath,retry=Y):
  try:
   logger.debug('get_pagesoruce_by_selenium:%s %s',url,wait_xpath)
   driver=SystemLogicSelenium.get_driver()
   driver.get(url)
   WebDriverWait(driver,30).until(lambda driver:driver.find_element_by_xpath(wait_xpath))
   logger.debug('return page_source') 
   return driver.page_source
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
   SystemLogicSelenium.chrome_driver=h
   if retry:
    return SystemLogicSelenium.get_pagesoruce_by_selenium(url,wait_xpath,retry=x)
 @d
 def get_driver(chrome_options=h):
  try:
   if SystemLogicSelenium.chrome_driver is h:
    SystemLogicSelenium.chrome_driver=SystemLogicSelenium.inner_create_driver(chrome_options)
   return SystemLogicSelenium.chrome_driver
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def create_driver(chrome_options=h):
  try:
   driver=SystemLogicSelenium.inner_create_driver(chrome_options)
   if driver is not h:
    SystemLogicSelenium.chrome_driver_list.append(driver)
    return driver
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def close_driver():
  try:
   if SystemLogicSelenium.chrome_driver is not h:
    SystemLogicSelenium.chrome_driver.quit()
    SystemLogicSelenium.chrome_driver=h
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def inner_create_driver(chrome_options):
  try:
   driver=h
   remote_url=ModelSetting.get('selenium_remote_url')
   if remote_url.endswith('/wd/hub/'):
    remote_url=remote_url[:-1]
   if remote_url!='':
    if chrome_options is h:
     chrome_options=webdriver.ChromeOptions()
     tmp=ModelSetting.get_list('selenium_remote_default_option')
     for t in tmp:
      chrome_options.add_argument(t)
    driver=webdriver.Remote(command_executor=remote_url,desired_capabilities=chrome_options.to_capabilities())
    driver.set_window_size(1920,1080)
    logger.debug('Using Remote :%s',driver)
   else:
    path_chrome=os.path.join(path_app_root,'bin',platform.system(),'chromedriver')
    if platform.system()=='Windows':
     path_chrome+='.exe'
    if chrome_options is h:
     chrome_options=webdriver.ChromeOptions()
     tmp=ModelSetting.get_list('selenium_binary_default_option')
     for t in tmp:
      chrome_options.add_argument(t)
    driver=webdriver.Chrome(path_chrome,chrome_options=chrome_options)
    logger.debug('Using local bin :%s',driver)
   if driver is not h:
    return driver
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def plugin_unload():
  try:
   logger.debug(SystemLogicSelenium.chrome_driver)
   if SystemLogicSelenium.chrome_driver is not h:
    SystemLogicSelenium.chrome_driver.quit()
    logger.debug(SystemLogicSelenium.chrome_driver)
   for tmp in SystemLogicSelenium.chrome_driver_list:
    if tmp is not h:
     tmp.quit()
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def get_text_excluding_children(driver,element):
  return driver.execute_script("""
        return jQuery(arguments[0]).contents().filter(function() {return this.nodeType == Node.TEXT_NODE; }).text();
        """  , element)
 @d
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
    img=Image.open(BytesIO((driver.get_screenshot_as_png())))
    if low_offset!=0:
     img=img.crop((0,0,img.width,img.height-low_offset))
    img_li.append(img)
    offset+=height
    logger.debug('offset : %s / %s',offset,max_window_height)
   img_frame_height=E([img_frag.size[1]for img_frag in img_li])
   img_frame=Image.new('RGB',(img_li[0].size[0],img_frame_height))
   offset=0
   for img_frag in img_li:
    img_frame.paste(img_frag,(0,offset))
    offset+=img_frag.size[1]
    logger.debug('paste offset : %s ',offset)
   return img_frame
  except o as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 @d
 def remove_element(driver,element):
  driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """  , element)
 @d
 def __get_downloaded_files(driver=h):
  if driver is h:
   driver=SystemLogicSelenium.get_driver()
  if not driver.current_url.startswith("chrome://downloads"):
   driver.get("chrome://downloads/")
  return driver.execute_script("return downloads.Manager.get().items_   " "  .filter(e => e.state === 'COMPLETE')  " "  .map(e => e.filePath || e.file_path); ")
 @d
 def get_file_content(path,driver=h):
  if driver is h:
   driver=SystemLogicSelenium.get_driver()
  elem=driver.execute_script("var input = window.document.createElement('INPUT'); " "input.setAttribute('type', 'file'); " "input.hidden = true; " "input.onchange = function (e) { e.stopPropagation() }; " "return window.document.documentElement.appendChild(input); ")
  elem._execute('sendKeysToElement',{'value':[path],'text':path})
  result=driver.execute_async_script("var input = arguments[0], callback = arguments[1]; " "var reader = new FileReader(); " "reader.onload = function (ev) { callback(reader.result) }; " "reader.onerror = function (ex) { callback(ex.message) }; " "reader.readAsDataURL(input.files[0]); " "input.remove(); ",elem)
  if not result.startswith('data:'):
   raise o("Failed to get file content: %s"%result)
  return base64.b64decode(result[result.find('base64,')+7:])
 @d
 def get_downloaded_files(driver=h):
  if driver is h:
   driver=SystemLogicSelenium.get_driver()
  files=SystemLogicSelenium.__get_downloaded_files()
  return files
 @d
 def waitUntilDownloadCompleted(maxTime=600,driver=h):
  if driver is h:
   driver=SystemLogicSelenium.get_driver()
  driver.execute_script("window.open()")
  driver.switch_to.window(driver.window_handles[-1])
  driver.get('chrome://downloads')
  endTime=time.time()+maxTime
  while Y:
   try:
    downloadPercentage=driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
    if downloadPercentage==100:
     return downloadPercentage
   except:
    pass
   time.sleep(1)
   if time.time()>endTime:
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
