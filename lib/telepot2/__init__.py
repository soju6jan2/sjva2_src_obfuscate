import sys
import io
import time
import json
import threading
import traceback
import collections
import bisect
try:
 import Queue as queue
except ImportError:
 import queue
from.import hack
from.import exception
__version_info__=(12,7)
__version__='.'.join(map(str,__version_info__))
def flavor(msg):
 if 'message_id' in msg:
  return 'chat'
 elif 'id' in msg and 'chat_instance' in msg:
  return 'callback_query'
 elif 'id' in msg and 'query' in msg:
  return 'inline_query'
 elif 'result_id' in msg:
  return 'chosen_inline_result'
 elif 'id' in msg and 'shipping_address' in msg:
  return 'shipping_query'
 elif 'id' in msg and 'total_amount' in msg:
  return 'pre_checkout_query'
 else:
  top_keys=list(msg.keys())
  if len(top_keys)==1:
   return top_keys[0]
  raise exception.BadFlavor(msg)
chat_flavors=['chat']
inline_flavors=['inline_query','chosen_inline_result']
def _find_first_key(d,keys):
 for k in keys:
  if k in d:
   return k
 raise KeyError('No suggested keys %s in %s'%(str(keys),str(d)))
all_content_types=['text','audio','document','game','photo','sticker','video','voice','video_note','contact','location','venue','new_chat_member','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message','new_chat_members','invoice','successful_payment','my_chat_member']
def glance(msg,flavor='chat',long=False):
 def gl_chat():
  content_type=_find_first_key(msg,all_content_types)
  if long:
   return content_type,msg['chat']['type'],msg['chat']['id'],msg['date'],msg['message_id']
  else:
   return content_type,msg['chat']['type'],msg['chat']['id']
 def gl_callback_query():
  return msg['id'],msg['from']['id'],msg['data']
 def gl_inline_query():
  if long:
   return msg['id'],msg['from']['id'],msg['query'],msg['offset']
  else:
   return msg['id'],msg['from']['id'],msg['query']
 def gl_chosen_inline_result():
  return msg['result_id'],msg['from']['id'],msg['query']
 def gl_shipping_query():
  return msg['id'],msg['from']['id'],msg['invoice_payload']
 def gl_pre_checkout_query():
  if long:
   return msg['id'],msg['from']['id'],msg['invoice_payload'],msg['currency'],msg['total_amount']
  else:
   return msg['id'],msg['from']['id'],msg['invoice_payload']
 try:
  fn={'chat':gl_chat,'callback_query':gl_callback_query,'inline_query':gl_inline_query,'chosen_inline_result':gl_chosen_inline_result,'shipping_query':gl_shipping_query,'pre_checkout_query':gl_pre_checkout_query}[flavor]
 except KeyError:
  raise exception.BadFlavor(flavor)
 return fn()
def flance(msg,long=False):
 f=flavor(msg)
 g=glance(msg,flavor=f,long=long)
 return f,g
def peel(event):
 return list(event.values())[0]
def fleece(event):
 return flavor(event),peel(event)
def is_event(msg):
 return flavor(msg).startswith('_')
def origin_identifier(msg):
 if 'message' in msg:
  return msg['message']['chat']['id'],msg['message']['message_id']
 elif 'inline_message_id' in msg:
  return msg['inline_message_id'],
 else:
  raise ValueError()
def message_identifier(msg):
 if 'chat' in msg and 'message_id' in msg:
  return msg['chat']['id'],msg['message_id']
 elif 'inline_message_id' in msg:
  return msg['inline_message_id'],
 else:
  raise ValueError()
def _dismantle_message_identifier(f):
 if isinstance(f,tuple):
  if len(f)==2:
   return{'chat_id':f[0],'message_id':f[1]}
  elif len(f)==1:
   return{'inline_message_id':f[0]}
  else:
   raise ValueError()
 else:
  return{'inline_message_id':f}
def _split_input_media_array(media_array):
 def ensure_dict(input_media):
  if isinstance(input_media,tuple)and hasattr(input_media,'_asdict'):
   return input_media._asdict()
  elif isinstance(input_media,dict):
   return input_media
  else:
   raise ValueError()
 def given_attach_name(input_media):
  if isinstance(input_media['media'],tuple):
   return input_media['media'][0]
  else:
   return None
 def attach_name_generator(used_names):
  x=0
  while 1:
   x+=1
   name='media'+str(x)
   if name in used_names:
    continue;
   yield name
 def split_media(input_media,name_generator):
  file_spec=input_media['media']
  if _isstring(file_spec):
   return(input_media,None)
  if isinstance(file_spec,tuple):
   name,f=file_spec
  else:
   name,f=next(name_generator),file_spec
  m=input_media.copy()
  m['media']='attach://'+name
  return(m,(name,f))
 ms=[ensure_dict(m)for m in media_array]
 used_names=[given_attach_name(m)for m in ms if given_attach_name(m)is not None]
 name_generator=attach_name_generator(used_names)
 splitted=[split_media(m,name_generator)for m in ms]
 legal_media,attachments=map(list,zip(*splitted))
 files_to_attach=dict([a for a in attachments if a is not None])
 return(legal_media,files_to_attach)
PY_3=sys.version_info.major>=3
_string_type=str if PY_3 else basestring
_file_type=io.IOBase if PY_3 else file
def _isstring(s):
 return isinstance(s,_string_type)
def _isfile(f):
 return isinstance(f,_file_type)
from.import helper
def flavor_router(routing_table):
 router=helper.Router(flavor,routing_table)
 return router.route
class _BotBase(object):
 def __init__(self,token):
  self._token=token
  self._file_chunk_size=65536
def _strip(params,more=[]):
 return{key:value for key,value in params.items()if key not in['self']+more}
def _rectify(params):
 def make_jsonable(value):
  if isinstance(value,list):
   return[make_jsonable(v)for v in value]
  elif isinstance(value,dict):
   return{k:make_jsonable(v)for k,v in value.items()if v is not None}
  elif isinstance(value,tuple)and hasattr(value,'_asdict'):
   return{k:make_jsonable(v)for k,v in value._asdict().items()if v is not None}
  else:
   return value
 def flatten(value):
  v=make_jsonable(value)
  if isinstance(v,(dict,list)):
   return json.dumps(v,separators=(',',':'))
  else:
   return v
 return{k:flatten(v)for k,v in params.items()if v is not None}
from.import api
class Bot(_BotBase):
 class Scheduler(threading.Thread):
  Event=collections.namedtuple('Event',['timestamp','data'])
  Event.__eq__=lambda self,other:self.timestamp==other.timestamp
  Event.__ne__=lambda self,other:self.timestamp!=other.timestamp
  Event.__gt__=lambda self,other:self.timestamp>other.timestamp
  Event.__ge__=lambda self,other:self.timestamp>=other.timestamp
  Event.__lt__=lambda self,other:self.timestamp<other.timestamp
  Event.__le__=lambda self,other:self.timestamp<=other.timestamp
  def __init__(self):
   super(Bot.Scheduler,self).__init__()
   self._eventq=[]
   self._lock=threading.RLock() 
   self._event_handler=None
  def _locked(fn):
   def k(self,*args,**kwargs):
    with self._lock:
     return fn(self,*args,**kwargs)
   return k
  @_locked
  def _insert_event(self,data,when):
   ev=self.Event(when,data)
   bisect.insort(self._eventq,ev)
   return ev
  @_locked
  def _remove_event(self,event):
   i=bisect.bisect(self._eventq,event)
   while i>0:
    i-=1
    e=self._eventq[i]
    if e.timestamp!=event.timestamp:
     raise exception.EventNotFound(event)
    elif id(e)==id(event):
     self._eventq.pop(i)
     return
   raise exception.EventNotFound(event)
  @_locked
  def _pop_expired_event(self):
   if not self._eventq:
    return None
   if self._eventq[0].timestamp<=time.time():
    return self._eventq.pop(0)
   else:
    return None
  def event_at(self,when,data):
   return self._insert_event(data,when)
  def event_later(self,delay,data):
   return self._insert_event(data,time.time()+delay)
  def event_now(self,data):
   return self._insert_event(data,time.time())
  def cancel(self,event):
   self._remove_event(event)
  def run(self):
   while 1:
    e=self._pop_expired_event()
    while e:
     if callable(e.data):
      d=e.data() 
      if d is not None:
       self._event_handler(d)
     else:
      self._event_handler(e.data)
     e=self._pop_expired_event()
    time.sleep(0.1)
  def run_as_thread(self):
   self.daemon=True
   self.start()
  def on_event(self,fn):
   self._event_handler=fn
 def __init__(self,token):
  super(Bot,self).__init__(token)
  self._scheduler=self.Scheduler()
  self._router=helper.Router(flavor,{'chat':lambda msg:self.on_chat_message(msg),'callback_query':lambda msg:self.on_callback_query(msg),'inline_query':lambda msg:self.on_inline_query(msg),'chosen_inline_result':lambda msg:self.on_chosen_inline_result(msg)})
 @property
 def scheduler(self):
  return self._scheduler
 @property
 def router(self):
  return self._router
 def handle(self,msg):
  self._router.route(msg)
 def _api_request(self,method,params=None,files=None,**kwargs):
  return api.request((self._token,method,params,files),**kwargs)
 def _api_request_with_file(self,method,params,file_key,file_value,**kwargs):
  if _isstring(file_value):
   params[file_key]=file_value
   return self._api_request(method,_rectify(params),**kwargs)
  else:
   files={file_key:file_value}
   return self._api_request(method,_rectify(params),files,**kwargs)
 def getMe(self):
  return self._api_request('getMe')
 def sendMessage(self,chat_id,text,parse_mode=None,disable_web_page_preview=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals())
  return self._api_request('sendMessage',_rectify(p))
 def forwardMessage(self,chat_id,from_chat_id,message_id,disable_notification=None):
  p=_strip(locals())
  return self._api_request('forwardMessage',_rectify(p))
 def sendPhoto(self,chat_id,photo,caption=None,parse_mode=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals(),more=['photo'])
  return self._api_request_with_file('sendPhoto',_rectify(p),'photo',photo)
 def sendAudio(self,chat_id,audio,caption=None,parse_mode=None,duration=None,performer=None,title=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals(),more=['audio'])
  return self._api_request_with_file('sendAudio',_rectify(p),'audio',audio)
 def sendDocument(self,chat_id,document,caption=None,parse_mode=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals(),more=['document'])
  return self._api_request_with_file('sendDocument',_rectify(p),'document',document)
 def sendVideo(self,chat_id,video,duration=None,width=None,height=None,caption=None,parse_mode=None,supports_streaming=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals(),more=['video'])
  return self._api_request_with_file('sendVideo',_rectify(p),'video',video)
 def sendVoice(self,chat_id,voice,caption=None,parse_mode=None,duration=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals(),more=['voice'])
  return self._api_request_with_file('sendVoice',_rectify(p),'voice',voice)
 def sendVideoNote(self,chat_id,video_note,duration=None,length=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals(),more=['video_note'])
  return self._api_request_with_file('sendVideoNote',_rectify(p),'video_note',video_note)
 def sendMediaGroup(self,chat_id,media,disable_notification=None,reply_to_message_id=None):
  p=_strip(locals(),more=['media'])
  legal_media,files_to_attach=_split_input_media_array(media)
  p['media']=legal_media
  return self._api_request('sendMediaGroup',_rectify(p),files_to_attach)
 def sendLocation(self,chat_id,latitude,longitude,live_period=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals())
  return self._api_request('sendLocation',_rectify(p))
 def editMessageLiveLocation(self,msg_identifier,latitude,longitude,reply_markup=None):
  p=_strip(locals(),more=['msg_identifier'])
  p.update(_dismantle_message_identifier(msg_identifier))
  return self._api_request('editMessageLiveLocation',_rectify(p))
 def stopMessageLiveLocation(self,msg_identifier,reply_markup=None):
  p=_strip(locals(),more=['msg_identifier'])
  p.update(_dismantle_message_identifier(msg_identifier))
  return self._api_request('stopMessageLiveLocation',_rectify(p))
 def sendVenue(self,chat_id,latitude,longitude,title,address,foursquare_id=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals())
  return self._api_request('sendVenue',_rectify(p))
 def sendContact(self,chat_id,phone_number,first_name,last_name=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals())
  return self._api_request('sendContact',_rectify(p))
 def sendGame(self,chat_id,game_short_name,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals())
  return self._api_request('sendGame',_rectify(p))
 def sendInvoice(self,chat_id,title,description,payload,provider_token,start_parameter,currency,prices,provider_data=None,photo_url=None,photo_size=None,photo_width=None,photo_height=None,need_name=None,need_phone_number=None,need_email=None,need_shipping_address=None,is_flexible=None,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals())
  return self._api_request('sendInvoice',_rectify(p))
 def sendChatAction(self,chat_id,action):
  p=_strip(locals())
  return self._api_request('sendChatAction',_rectify(p))
 def getUserProfilePhotos(self,user_id,offset=None,limit=None):
  p=_strip(locals())
  return self._api_request('getUserProfilePhotos',_rectify(p))
 def getFile(self,file_id):
  p=_strip(locals())
  return self._api_request('getFile',_rectify(p))
 def kickChatMember(self,chat_id,user_id,until_date=None):
  p=_strip(locals())
  return self._api_request('kickChatMember',_rectify(p))
 def unbanChatMember(self,chat_id,user_id):
  p=_strip(locals())
  return self._api_request('unbanChatMember',_rectify(p))
 def restrictChatMember(self,chat_id,user_id,until_date=None,can_send_messages=None,can_send_media_messages=None,can_send_other_messages=None,can_add_web_page_previews=None):
  p=_strip(locals())
  return self._api_request('restrictChatMember',_rectify(p))
 def promoteChatMember(self,chat_id,user_id,can_change_info=None,can_post_messages=None,can_edit_messages=None,can_delete_messages=None,can_invite_users=None,can_restrict_members=None,can_pin_messages=None,can_promote_members=None):
  p=_strip(locals())
  return self._api_request('promoteChatMember',_rectify(p))
 def exportChatInviteLink(self,chat_id):
  p=_strip(locals())
  return self._api_request('exportChatInviteLink',_rectify(p))
 def setChatPhoto(self,chat_id,photo):
  p=_strip(locals(),more=['photo'])
  return self._api_request_with_file('setChatPhoto',_rectify(p),'photo',photo)
 def deleteChatPhoto(self,chat_id):
  p=_strip(locals())
  return self._api_request('deleteChatPhoto',_rectify(p))
 def setChatTitle(self,chat_id,title):
  p=_strip(locals())
  return self._api_request('setChatTitle',_rectify(p))
 def setChatDescription(self,chat_id,description=None):
  p=_strip(locals())
  return self._api_request('setChatDescription',_rectify(p))
 def pinChatMessage(self,chat_id,message_id,disable_notification=None):
  p=_strip(locals())
  return self._api_request('pinChatMessage',_rectify(p))
 def unpinChatMessage(self,chat_id):
  p=_strip(locals())
  return self._api_request('unpinChatMessage',_rectify(p))
 def leaveChat(self,chat_id):
  p=_strip(locals())
  return self._api_request('leaveChat',_rectify(p))
 def getChat(self,chat_id):
  p=_strip(locals())
  return self._api_request('getChat',_rectify(p))
 def getChatAdministrators(self,chat_id):
  p=_strip(locals())
  return self._api_request('getChatAdministrators',_rectify(p))
 def getChatMembersCount(self,chat_id):
  p=_strip(locals())
  return self._api_request('getChatMembersCount',_rectify(p))
 def getChatMember(self,chat_id,user_id):
  p=_strip(locals())
  return self._api_request('getChatMember',_rectify(p))
 def setChatStickerSet(self,chat_id,sticker_set_name):
  p=_strip(locals())
  return self._api_request('setChatStickerSet',_rectify(p))
 def deleteChatStickerSet(self,chat_id):
  p=_strip(locals())
  return self._api_request('deleteChatStickerSet',_rectify(p))
 def answerCallbackQuery(self,callback_query_id,text=None,show_alert=None,url=None,cache_time=None):
  p=_strip(locals())
  return self._api_request('answerCallbackQuery',_rectify(p))
 def answerShippingQuery(self,shipping_query_id,ok,shipping_options=None,error_message=None):
  p=_strip(locals())
  return self._api_request('answerShippingQuery',_rectify(p))
 def answerPreCheckoutQuery(self,pre_checkout_query_id,ok,error_message=None):
  p=_strip(locals())
  return self._api_request('answerPreCheckoutQuery',_rectify(p))
 def editMessageText(self,msg_identifier,text,parse_mode=None,disable_web_page_preview=None,reply_markup=None):
  p=_strip(locals(),more=['msg_identifier'])
  p.update(_dismantle_message_identifier(msg_identifier))
  return self._api_request('editMessageText',_rectify(p))
 def editMessageCaption(self,msg_identifier,caption=None,parse_mode=None,reply_markup=None):
  p=_strip(locals(),more=['msg_identifier'])
  p.update(_dismantle_message_identifier(msg_identifier))
  return self._api_request('editMessageCaption',_rectify(p))
 def editMessageReplyMarkup(self,msg_identifier,reply_markup=None):
  p=_strip(locals(),more=['msg_identifier'])
  p.update(_dismantle_message_identifier(msg_identifier))
  return self._api_request('editMessageReplyMarkup',_rectify(p))
 def deleteMessage(self,msg_identifier):
  p=_strip(locals(),more=['msg_identifier'])
  p.update(_dismantle_message_identifier(msg_identifier))
  return self._api_request('deleteMessage',_rectify(p))
 def sendSticker(self,chat_id,sticker,disable_notification=None,reply_to_message_id=None,reply_markup=None):
  p=_strip(locals(),more=['sticker'])
  return self._api_request_with_file('sendSticker',_rectify(p),'sticker',sticker)
 def getStickerSet(self,name):
  p=_strip(locals())
  return self._api_request('getStickerSet',_rectify(p))
 def uploadStickerFile(self,user_id,png_sticker):
  p=_strip(locals(),more=['png_sticker'])
  return self._api_request_with_file('uploadStickerFile',_rectify(p),'png_sticker',png_sticker)
 def createNewStickerSet(self,user_id,name,title,png_sticker,emojis,contains_masks=None,mask_position=None):
  p=_strip(locals(),more=['png_sticker'])
  return self._api_request_with_file('createNewStickerSet',_rectify(p),'png_sticker',png_sticker)
 def addStickerToSet(self,user_id,name,png_sticker,emojis,mask_position=None):
  p=_strip(locals(),more=['png_sticker'])
  return self._api_request_with_file('addStickerToSet',_rectify(p),'png_sticker',png_sticker)
 def setStickerPositionInSet(self,sticker,position):
  p=_strip(locals())
  return self._api_request('setStickerPositionInSet',_rectify(p))
 def deleteStickerFromSet(self,sticker):
  p=_strip(locals())
  return self._api_request('deleteStickerFromSet',_rectify(p))
 def answerInlineQuery(self,inline_query_id,results,cache_time=None,is_personal=None,next_offset=None,switch_pm_text=None,switch_pm_parameter=None):
  p=_strip(locals())
  return self._api_request('answerInlineQuery',_rectify(p))
 def getUpdates(self,offset=None,limit=None,timeout=None,allowed_updates=None):
  p=_strip(locals())
  return self._api_request('getUpdates',_rectify(p))
 def setWebhook(self,url=None,certificate=None,max_connections=None,allowed_updates=None):
  p=_strip(locals(),more=['certificate'])
  if certificate:
   files={'certificate':certificate}
   return self._api_request('setWebhook',_rectify(p),files)
  else:
   return self._api_request('setWebhook',_rectify(p))
 def deleteWebhook(self):
  return self._api_request('deleteWebhook')
 def getWebhookInfo(self):
  return self._api_request('getWebhookInfo')
 def setGameScore(self,user_id,score,game_message_identifier,force=None,disable_edit_message=None):
  p=_strip(locals(),more=['game_message_identifier'])
  p.update(_dismantle_message_identifier(game_message_identifier))
  return self._api_request('setGameScore',_rectify(p))
 def getGameHighScores(self,user_id,game_message_identifier):
  p=_strip(locals(),more=['game_message_identifier'])
  p.update(_dismantle_message_identifier(game_message_identifier))
  return self._api_request('getGameHighScores',_rectify(p))
 def download_file(self,file_id,dest):
  f=self.getFile(file_id)
  try:
   d=dest if _isfile(dest)else open(dest,'wb')
   r=api.download((self._token,f['file_path']),preload_content=False)
   while 1:
    data=r.read(self._file_chunk_size)
    if not data:
     break
    d.write(data)
  finally:
   if not _isfile(dest)and 'd' in locals():
    d.close()
   if 'r' in locals():
    r.release_conn()
 def message_loop(self,callback=None,relax=0.1,timeout=20,allowed_updates=None,source=None,ordered=True,maxhold=3,run_forever=False):
  if callback is None:
   callback=self.handle
  elif isinstance(callback,dict):
   callback=flavor_router(callback)
  collect_queue=queue.Queue()
  def collector():
   while 1:
    try:
     item=collect_queue.get(block=True)
     callback(item)
    except:
     traceback.print_exc()
  def relay_to_collector(update):
   key=_find_first_key(update,['message','edited_message','channel_post','edited_channel_post','callback_query','inline_query','chosen_inline_result','shipping_query','pre_checkout_query'])
   collect_queue.put(update[key])
   return update['update_id']
  def get_from_telegram_server():
   offset=None 
   allowed_upd=allowed_updates
   while 1:
    try:
     result=self.getUpdates(offset=offset,timeout=timeout,allowed_updates=allowed_upd)
     allowed_upd=None
     if len(result)>0:
      offset=max([relay_to_collector(update)for update in result])+1
    except exception.BadHTTPResponse as e:
     traceback.print_exc()
     if e.status==502:
      time.sleep(30)
    except:
     traceback.print_exc()
    finally:
     time.sleep(relax)
  def dictify3(data):
   if type(data)is bytes:
    return json.loads(data.decode('utf-8'))
   elif type(data)is str:
    return json.loads(data)
   elif type(data)is dict:
    return data
   else:
    raise ValueError()
  def dictify27(data):
   if type(data)in[str,unicode]:
    return json.loads(data)
   elif type(data)is dict:
    return data
   else:
    raise ValueError()
  def get_from_queue_unordered(qu):
   dictify=dictify3 if sys.version_info>=(3,)else dictify27
   while 1:
    try:
     data=qu.get(block=True)
     update=dictify(data)
     relay_to_collector(update)
    except:
     traceback.print_exc()
  def get_from_queue(qu):
   dictify=dictify3 if sys.version_info>=(3,)else dictify27
   max_id=None 
   buffer=collections.deque() 
   qwait=None 
   while 1:
    try:
     data=qu.get(block=True,timeout=qwait)
     update=dictify(data)
     if max_id is None:
      max_id=relay_to_collector(update)
     elif update['update_id']==max_id+1:
      max_id=relay_to_collector(update)
      if len(buffer)>0:
       buffer.popleft() 
       while 1:
        try:
         if type(buffer[0])is dict:
          max_id=relay_to_collector(buffer.popleft()) 
         else:
          break 
        except IndexError:
         break 
     elif update['update_id']>max_id+1:
      nbuf=len(buffer)
      if update['update_id']<=max_id+nbuf:
       buffer[update['update_id']-max_id-1]=update
      else:
       expire=time.time()+maxhold
       for a in range(nbuf,update['update_id']-max_id-1):
        buffer.append(expire) 
       buffer.append(update)
     else:
      pass 
    except queue.Empty:
     while 1:
      try:
       if type(buffer[0])is dict:
        max_id=relay_to_collector(buffer.popleft())
       else:
        expire=buffer[0]
        if expire<=time.time():
         max_id+=1
         buffer.popleft()
        else:
         break 
      except IndexError:
       break 
    except:
     traceback.print_exc()
    finally:
     try:
      qwait=buffer[0]-time.time()
      if qwait<0:
       qwait=0
     except IndexError:
      qwait=None
  collector_thread=threading.Thread(target=collector)
  collector_thread.daemon=True
  collector_thread.start()
  if source is None:
   message_thread=threading.Thread(target=get_from_telegram_server)
  elif isinstance(source,queue.Queue):
   if ordered:
    message_thread=threading.Thread(target=get_from_queue,args=(source,))
   else:
    message_thread=threading.Thread(target=get_from_queue_unordered,args=(source,))
  else:
   raise ValueError('Invalid source')
  message_thread.daemon=True 
  message_thread.start()
  self._scheduler.on_event(collect_queue.put)
  self._scheduler.run_as_thread()
  if run_forever:
   if _isstring(run_forever):
    print(run_forever)
   while 1:
    time.sleep(10)
import inspect
class SpeakerBot(Bot):
 def __init__(self,token):
  super(SpeakerBot,self).__init__(token)
  self._mic=helper.Microphone()
 @property
 def mic(self):
  return self._mic
 def create_listener(self):
  q=queue.Queue()
  self._mic.add(q)
  ln=helper.Listener(self._mic,q)
  return ln
class DelegatorBot(SpeakerBot):
 def __init__(self,token,delegation_patterns):
  super(DelegatorBot,self).__init__(token)
  self._delegate_records=[p+({},)for p in delegation_patterns]
 def _startable(self,delegate):
  return((hasattr(delegate,'start')and inspect.ismethod(delegate.start))and(hasattr(delegate,'is_alive')and inspect.ismethod(delegate.is_alive)))
 def _tuple_is_valid(self,t):
  return len(t)==3 and callable(t[0])and type(t[1])in[list,tuple]and type(t[2])is dict
 def _ensure_startable(self,delegate):
  if self._startable(delegate):
   return delegate
  elif callable(delegate):
   return threading.Thread(target=delegate)
  elif type(delegate)is tuple and self._tuple_is_valid(delegate):
   func,args,kwargs=delegate
   return threading.Thread(target=func,args=args,kwargs=kwargs)
  else:
   raise RuntimeError('Delegate does not have the required methods, is not callable, and is not a valid tuple.')
 def handle(self,msg):
  self._mic.send(msg)
  for calculate_seed,make_delegate,dict in self._delegate_records:
   id=calculate_seed(msg)
   if id is None:
    continue
   elif isinstance(id,collections.Hashable):
    if id not in dict or not dict[id].is_alive():
     d=make_delegate((self,msg,id))
     d=self._ensure_startable(d)
     dict[id]=d
     dict[id].start()
   else:
    d=make_delegate((self,msg,id))
    d=self._ensure_startable(d)
    d.start()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
