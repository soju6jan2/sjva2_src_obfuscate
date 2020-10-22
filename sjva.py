import os
E=reload
W=print
t=Exception
B=range
V=str
n=KeyboardInterrupt
u=os.remove
O=os.system
w=os.path
import sys
Q=sys.exit
J=sys.argv
C=sys.path
H=sys.setdefaultencoding
f=sys.version_info
if f[0]==2:
 E(sys)
 H('utf-8')
C.insert(0,w.join(w.dirname(w.abspath(__file__)),'lib'))
import platform
M=platform.system
W(C)
try:
 from gevent import monkey;monkey.patch_all()
except:
 W('not monkey')
try:
 W(J)
 W(J)
 W(J)
 if J[0].startswith('sjva.py'):
  try:
   if M()!='Windows':
    custom=w.join(w.dirname(w.abspath(__file__)),'data','custom')
    O("chmod 777 -R %s"%custom)
    custom=w.join(w.dirname(w.abspath(__file__)),'bin')
    O("chmod 777 -R %s"%custom)
  except:
   W('Exception:%s',e)
  server_plugin_path=w.join(w.dirname(w.abspath(__file__)),'data','custom')
  try:
   import shutil
   remove_plugin=['ani24','manamoa','launcher_gateone']
   for plugin in remove_plugin:
    try:
     plugin_path=w.join(server_plugin_path,plugin)
     if w.exists(plugin_path):
      W('remove plugin:%s',plugin)
      shutil.rmtree(plugin_path)
     tmp=w.join(w.dirname(w.abspath(__file__)),'data','db','%s.db'%plugin)
     if w.exists(tmp):
      W('remove plugin db:%s'%plugin)
      u(tmp)
    except t as e:
     W('Exception:%s'%e) 
  except t as e:
   W('Exception:%s'%e)
except t as e:
 W('Exception:%s'%e)
import framework
l=framework.exit_code
T=framework.socketio
U=framework.celery
v=framework.app
import system
app=v
celery=U
def start_app():
 for i in B(10):
  try:
   T.run(app,host='0.0.0.0',port=app.config['config']['port'])
   W('EXIT CODE : %s'%l)
   if l!=-1:
    Q(l)
    break
   else:
    W('framework.exit_code is -1')
   break
  except t as e:
   W(V(e))
   import time
   time.sleep(10*i)
   continue
  except n:
   W('KeyboardInterrupt !!')
 W('start_app() end')
if __name__=='__main__':
 try:
  start_app()
 except t as e:
  W(V(e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
