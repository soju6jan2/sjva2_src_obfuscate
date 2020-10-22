import os
import sys
if sys.version_info[0]==2:
 reload(sys)
 sys.setdefaultencoding('utf-8')
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib'))
import platform
print(sys.path)
try:
 from gevent import monkey;monkey.patch_all()
except:
 print('not monkey')
try:
 print(sys.argv)
 print(sys.argv)
 print(sys.argv)
 if sys.argv[0].startswith('sjva.py'):
  try:
   if platform.system()!='Windows':
    custom=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','custom')
    os.system("chmod 777 -R %s"%custom)
    custom=os.path.join(os.path.dirname(os.path.abspath(__file__)),'bin')
    os.system("chmod 777 -R %s"%custom)
  except:
   print('Exception:%s',e)
  server_plugin_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','custom')
  try:
   import shutil
   remove_plugin=['ani24','manamoa','launcher_gateone']
   for plugin in remove_plugin:
    try:
     plugin_path=os.path.join(server_plugin_path,plugin)
     if os.path.exists(plugin_path):
      print('remove plugin:%s',plugin)
      shutil.rmtree(plugin_path)
     tmp=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','db','%s.db'%plugin)
     if os.path.exists(tmp):
      print('remove plugin db:%s'%plugin)
      os.remove(tmp)
    except Exception as exception:
     print('Exception:%s'%exception) 
  except Exception as exception:
   print('Exception:%s'%exception)
except Exception as exception:
 print('Exception:%s'%exception)
import framework
import system
app=framework.app
celery=framework.celery
def start_app():
 for i in range(10):
  try:
   framework.socketio.run(app,host='0.0.0.0',port=app.config['config']['port'])
   print('EXIT CODE : %s'%framework.exit_code)
   if framework.exit_code!=-1:
    sys.exit(framework.exit_code)
    break
   else:
    print('framework.exit_code is -1')
   break
  except Exception as exception:
   print(str(exception))
   import time
   time.sleep(10*i)
   continue
  except KeyboardInterrupt:
   print('KeyboardInterrupt !!')
 print('start_app() end')
if __name__=='__main__':
 try:
  start_app()
 except Exception as exception:
  print(str(exception))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
