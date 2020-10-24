import re
u=None
a=False
from flask_login import current_user
def get_menu(full_query):
 match=re.compile(r'\/(?P<menu>.*?)\/(?P<sub>.*?)\/(?P<sub2>.*?)($|\/|\?)').match(full_query)
 if match:
  return match.group('menu'),match.group('sub'),match.group('sub2')
 match=re.compile(r'\/(?P<menu>.*?)\/(?P<sub>.*?)($|\/|\?)').match(full_query)
 if match:
  return match.group('menu'),match.group('sub'),u
 match=re.compile(r'\/(?P<menu>.*?)($|\/|\?)').match(full_query)
 if match:
  return match.group('menu'),u,u
 return 'home',u,u
def get_theme():
 theme_list={'Default':56,'Cerulean':56,'Cosmo':54,'Cyborg':54,'Darkly':70,'Flatly':70,'Journal':56,'Litera':57,'Lumen':56,'Lux':88,'Materia':80,'Minty':56,'Pulse':75,'Sandstone':53,'Simplex':67,'Sketchy':56,'Slate':53,'Solar':56,'Spacelab':58,'Superhero':48,'United':56,'Yeti':54,}
 from system.model import ModelSetting as SystemModelSetting
 theme=SystemModelSetting.get('theme')
 return[theme,theme_list[theme]]
def get_login_status():
 if current_user is u:
  return a
 return current_user.is_authenticated
def get_web_title():
 try:
  from system.model import ModelSetting as SystemModelSetting
  return SystemModelSetting.get('web_title')
 except:
  return 'SJ Video Assitant'
# Created by pyminifier (https://github.com/liftoff/pyminifier)
