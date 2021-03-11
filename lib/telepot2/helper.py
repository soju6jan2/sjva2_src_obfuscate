import time
import traceback
import threading
import logging
import collections
import re
import inspect
from functools import partial
from.import filtering,exception
from.import(flavor,chat_flavors,inline_flavors,is_event,message_identifier,origin_identifier)
try:
 import Queue as queue
except ImportError:
 import queue
class Microphone(object):
 def __init__(self):
  self._queues=set()
  self._lock=threading.Lock()
 def _locked(func):
  def k(self,*args,**kwargs):
   with self._lock:
    return func(self,*args,**kwargs)
  return k
 @_locked
 def add(self,q):
  self._queues.add(q)
 @_locked
 def remove(self,q):
  self._queues.remove(q)
 @_locked
 def send(self,msg):
  for q in self._queues:
   try:
    q.put_nowait(msg)
   except queue.Full:
    traceback.print_exc()
class Listener(object):
 def __init__(self,mic,q):
  self._mic=mic
  self._queue=q
  self._patterns=[]
 def __del__(self):
  self._mic.remove(self._queue)
 def capture(self,pattern):
  self._patterns.append(pattern)
 def wait(self):
  if not self._patterns:
   raise RuntimeError('Listener has nothing to capture')
  while 1:
   msg=self._queue.get(block=True)
   if any(map(lambda p:filtering.match_all(msg,p),self._patterns)):
    return msg
class Sender(object):
 def __init__(self,bot,chat_id):
  for method in['sendMessage','forwardMessage','sendPhoto','sendAudio','sendDocument','sendSticker','sendVideo','sendVoice','sendVideoNote','sendMediaGroup','sendLocation','sendVenue','sendContact','sendGame','sendChatAction',]:
   setattr(self,method,partial(getattr(bot,method),chat_id))
class Administrator(object):
 def __init__(self,bot,chat_id):
  for method in['kickChatMember','unbanChatMember','restrictChatMember','promoteChatMember','exportChatInviteLink','setChatPhoto','deleteChatPhoto','setChatTitle','setChatDescription','pinChatMessage','unpinChatMessage','leaveChat','getChat','getChatAdministrators','getChatMembersCount','getChatMember','setChatStickerSet','deleteChatStickerSet']:
   setattr(self,method,partial(getattr(bot,method),chat_id))
class Editor(object):
 def __init__(self,bot,msg_identifier):
  if isinstance(msg_identifier,dict):
   msg_identifier=message_identifier(msg_identifier)
  for method in['editMessageText','editMessageCaption','editMessageReplyMarkup','deleteMessage','editMessageLiveLocation','stopMessageLiveLocation']:
   setattr(self,method,partial(getattr(bot,method),msg_identifier))
class Answerer(object):
 def __init__(self,bot):
  self._bot=bot
  self._workers={} 
  self._lock=threading.Lock() 
 def answer(outerself,inline_query,compute_fn,*compute_args,**compute_kwargs):
  from_id=inline_query['from']['id']
  class Worker(threading.Thread):
   def __init__(innerself):
    super(Worker,innerself).__init__()
    innerself._cancelled=False
   def cancel(innerself):
    innerself._cancelled=True
   def run(innerself):
    try:
     query_id=inline_query['id']
     if innerself._cancelled:
      return
     ans=compute_fn(*compute_args,**compute_kwargs)
     if innerself._cancelled:
      return
     if isinstance(ans,list):
      outerself._bot.answerInlineQuery(query_id,ans)
     elif isinstance(ans,tuple):
      outerself._bot.answerInlineQuery(query_id,*ans)
     elif isinstance(ans,dict):
      outerself._bot.answerInlineQuery(query_id,**ans)
     else:
      raise ValueError('Invalid answer format')
    finally:
     with outerself._lock:
      if not innerself._cancelled:
       del outerself._workers[from_id]
  with outerself._lock:
   if from_id in outerself._workers:
    outerself._workers[from_id].cancel()
   outerself._workers[from_id]=Worker()
   outerself._workers[from_id].start()
class AnswererMixin(object):
 Answerer=Answerer 
 def __init__(self,*args,**kwargs):
  self._answerer=self.Answerer(self.bot)
  super(AnswererMixin,self).__init__(*args,**kwargs)
 @property
 def answerer(self):
  return self._answerer
class CallbackQueryCoordinator(object):
 def __init__(self,id,origin_set,enable_chat,enable_inline):
  self._id=id
  self._origin_set=origin_set
  def dissolve(enable):
   if not enable:
    return False,None
   elif enable is True:
    return True,None
   elif callable(enable):
    return True,enable
   else:
    raise ValueError()
  self._enable_chat,self._chat_notify=dissolve(enable_chat)
  self._enable_inline,self._inline_notify=dissolve(enable_inline)
 def configure(self,listener):
  listener.capture([lambda msg:flavor(msg)=='callback_query',{'message':self._chat_origin_included}])
  listener.capture([lambda msg:flavor(msg)=='callback_query',{'inline_message_id':self._inline_origin_included}])
 def _chat_origin_included(self,msg):
  try:
   return(msg['chat']['id'],msg['message_id'])in self._origin_set
  except KeyError:
   return False
 def _inline_origin_included(self,inline_message_id):
  return(inline_message_id,)in self._origin_set
 def _rectify(self,msg_identifier):
  if isinstance(msg_identifier,tuple):
   if len(msg_identifier)==2:
    return msg_identifier,self._chat_notify
   elif len(msg_identifier)==1:
    return msg_identifier,self._inline_notify
   else:
    raise ValueError()
  else:
   return(msg_identifier,),self._inline_notify
 def capture_origin(self,msg_identifier,notify=True):
  msg_identifier,notifier=self._rectify(msg_identifier)
  self._origin_set.add(msg_identifier)
  notify and notifier and notifier(msg_identifier,self._id,True)
 def uncapture_origin(self,msg_identifier,notify=True):
  msg_identifier,notifier=self._rectify(msg_identifier)
  self._origin_set.discard(msg_identifier)
  notify and notifier and notifier(msg_identifier,self._id,False)
 def _contains_callback_data(self,message_kw):
  def contains(obj,key):
   if isinstance(obj,dict):
    return key in obj
   else:
    return hasattr(obj,key)
  if contains(message_kw,'reply_markup'):
   reply_markup=filtering.pick(message_kw,'reply_markup')
   if contains(reply_markup,'inline_keyboard'):
    inline_keyboard=filtering.pick(reply_markup,'inline_keyboard')
    for array in inline_keyboard:
     if any(filter(lambda button:contains(button,'callback_data'),array)):
      return True
  return False
 def augment_send(self,send_func):
  def augmented(*aa,**kw):
   sent=send_func(*aa,**kw)
   if self._enable_chat and self._contains_callback_data(kw):
    self.capture_origin(message_identifier(sent))
   return sent
  return augmented
 def augment_edit(self,edit_func):
  def augmented(msg_identifier,*aa,**kw):
   edited=edit_func(msg_identifier,*aa,**kw)
   if(edited is True and self._enable_inline)or(isinstance(edited,dict)and self._enable_chat):
    if self._contains_callback_data(kw):
     self.capture_origin(msg_identifier)
    else:
     self.uncapture_origin(msg_identifier)
   return edited
  return augmented
 def augment_delete(self,delete_func):
  def augmented(msg_identifier,*aa,**kw):
   deleted=delete_func(msg_identifier,*aa,**kw)
   if deleted is True:
    self.uncapture_origin(msg_identifier)
   return deleted
  return augmented
 def augment_on_message(self,handler):
  def augmented(msg):
   if(self._enable_inline and flavor(msg)=='chosen_inline_result' and 'inline_message_id' in msg):
    inline_message_id=msg['inline_message_id']
    self.capture_origin(inline_message_id)
   return handler(msg)
  return augmented
 def augment_bot(self,bot):
  class BotProxy(object):
   pass
  proxy=BotProxy()
  send_methods=['sendMessage','forwardMessage','sendPhoto','sendAudio','sendDocument','sendSticker','sendVideo','sendVoice','sendVideoNote','sendLocation','sendVenue','sendContact','sendGame','sendInvoice','sendChatAction',]
  for method in send_methods:
   setattr(proxy,method,self.augment_send(getattr(bot,method)))
  edit_methods=['editMessageText','editMessageCaption','editMessageReplyMarkup',]
  for method in edit_methods:
   setattr(proxy,method,self.augment_edit(getattr(bot,method)))
  delete_methods=['deleteMessage']
  for method in delete_methods:
   setattr(proxy,method,self.augment_delete(getattr(bot,method)))
  def public_untouched(nv):
   name,value=nv
   return(not name.startswith('_')and name not in send_methods+edit_methods+delete_methods)
  for name,value in filter(public_untouched,inspect.getmembers(bot)):
   setattr(proxy,name,value)
  return proxy
class SafeDict(dict):
 def __init__(self,*args,**kwargs):
  super(SafeDict,self).__init__(*args,**kwargs)
  self._lock=threading.Lock()
 def _locked(func):
  def k(self,*args,**kwargs):
   with self._lock:
    return func(self,*args,**kwargs)
  return k
 @_locked
 def __getitem__(self,key):
  return super(SafeDict,self).__getitem__(key)
 @_locked
 def __setitem__(self,key,value):
  return super(SafeDict,self).__setitem__(key,value)
 @_locked
 def __delitem__(self,key):
  return super(SafeDict,self).__delitem__(key)
_cqc_origins=SafeDict()
class InterceptCallbackQueryMixin(object):
 CallbackQueryCoordinator=CallbackQueryCoordinator
 def __init__(self,intercept_callback_query,*args,**kwargs):
  global _cqc_origins
  if self.id in _cqc_origins:
   origin_set=_cqc_origins[self.id]
  else:
   origin_set=set()
   _cqc_origins[self.id]=origin_set
  if isinstance(intercept_callback_query,tuple):
   cqc_enable=intercept_callback_query
  else:
   cqc_enable=(intercept_callback_query,)*2
  self._callback_query_coordinator=self.CallbackQueryCoordinator(self.id,origin_set,*cqc_enable)
  cqc=self._callback_query_coordinator
  cqc.configure(self.listener)
  self.__bot=self._bot 
  self._bot=cqc.augment_bot(self._bot) 
  self.on_message=cqc.augment_on_message(self.on_message) 
  super(InterceptCallbackQueryMixin,self).__init__(*args,**kwargs)
 def __del__(self):
  global _cqc_origins
  if self.id in _cqc_origins and not _cqc_origins[self.id]:
   del _cqc_origins[self.id]
 @property
 def callback_query_coordinator(self):
  return self._callback_query_coordinator
class IdleEventCoordinator(object):
 def __init__(self,scheduler,timeout):
  self._scheduler=scheduler
  self._timeout_seconds=timeout
  self._timeout_event=None
 def refresh(self):
  try:
   if self._timeout_event:
    self._scheduler.cancel(self._timeout_event)
  except exception.EventNotFound:
   pass
  finally:
   self._timeout_event=self._scheduler.event_later(self._timeout_seconds,('_idle',{'seconds':self._timeout_seconds}))
 def augment_on_message(self,handler):
  def augmented(msg):
   is_event(msg)or self.refresh()
   if flavor(msg)=='_idle' and msg is not self._timeout_event.data:
    return
   return handler(msg)
  return augmented
 def augment_on_close(self,handler):
  def augmented(ex):
   try:
    if self._timeout_event:
     self._scheduler.cancel(self._timeout_event)
     self._timeout_event=None
   except exception.EventNotFound:
    self._timeout_event=None
   return handler(ex)
  return augmented
class IdleTerminateMixin(object):
 IdleEventCoordinator=IdleEventCoordinator
 def __init__(self,timeout,*args,**kwargs):
  self._idle_event_coordinator=self.IdleEventCoordinator(self.scheduler,timeout)
  idlec=self._idle_event_coordinator
  idlec.refresh() 
  self.on_message=idlec.augment_on_message(self.on_message)
  self.on_close=idlec.augment_on_close(self.on_close)
  super(IdleTerminateMixin,self).__init__(*args,**kwargs)
 @property
 def idle_event_coordinator(self):
  return self._idle_event_coordinator
 def on__idle(self,event):
  raise exception.IdleTerminate(event['_idle']['seconds'])
class StandardEventScheduler(object):
 def __init__(self,scheduler,event_space,source_id):
  self._base=scheduler
  self._event_space=event_space
  self._source_id=source_id
 @property
 def event_space(self):
  return self._event_space
 def configure(self,listener):
  listener.capture([{re.compile('^_.+'):{'source':{'space':self._event_space,'id':self._source_id}}}])
 def make_event_data(self,flavor,data):
  if not flavor.startswith('_'):
   raise ValueError('Event flavor must start with _underscore')
  d={'source':{'space':self._event_space,'id':self._source_id}}
  d.update(data)
  return{flavor:d}
 def event_at(self,when,data_tuple):
  return self._base.event_at(when,self.make_event_data(*data_tuple))
 def event_later(self,delay,data_tuple):
  return self._base.event_later(delay,self.make_event_data(*data_tuple))
 def event_now(self,data_tuple):
  return self._base.event_now(self.make_event_data(*data_tuple))
 def cancel(self,event):
  return self._base.cancel(event)
class StandardEventMixin(object):
 StandardEventScheduler=StandardEventScheduler
 def __init__(self,event_space,*args,**kwargs):
  self._scheduler=self.StandardEventScheduler(self.bot.scheduler,event_space,self.id)
  self._scheduler.configure(self.listener)
  super(StandardEventMixin,self).__init__(*args,**kwargs)
 @property
 def scheduler(self):
  return self._scheduler
class ListenerContext(object):
 def __init__(self,bot,context_id,*args,**kwargs):
  self._bot=bot
  self._id=context_id
  self._listener=bot.create_listener()
  super(ListenerContext,self).__init__(*args,**kwargs)
 @property
 def bot(self):
  return self._bot
 @property
 def id(self):
  return self._id
 @property
 def listener(self):
  return self._listener
class ChatContext(ListenerContext):
 def __init__(self,bot,context_id,*args,**kwargs):
  super(ChatContext,self).__init__(bot,context_id,*args,**kwargs)
  self._chat_id=context_id
  self._sender=Sender(self.bot,self._chat_id)
  self._administrator=Administrator(self.bot,self._chat_id)
 @property
 def chat_id(self):
  return self._chat_id
 @property
 def sender(self):
  return self._sender
 @property
 def administrator(self):
  return self._administrator
class UserContext(ListenerContext):
 def __init__(self,bot,context_id,*args,**kwargs):
  super(UserContext,self).__init__(bot,context_id,*args,**kwargs)
  self._user_id=context_id
  self._sender=Sender(self.bot,self._user_id)
 @property
 def user_id(self):
  return self._user_id
 @property
 def sender(self):
  return self._sender
class CallbackQueryOriginContext(ListenerContext):
 def __init__(self,bot,context_id,*args,**kwargs):
  super(CallbackQueryOriginContext,self).__init__(bot,context_id,*args,**kwargs)
  self._origin=context_id
  self._editor=Editor(self.bot,self._origin)
 @property
 def origin(self):
  return self._origin
 @property
 def editor(self):
  return self._editor
class InvoiceContext(ListenerContext):
 def __init__(self,bot,context_id,*args,**kwargs):
  super(InvoiceContext,self).__init__(bot,context_id,*args,**kwargs)
  self._payload=context_id
 @property
 def payload(self):
  return self._payload
def openable(cls):
 def open(self,initial_msg,seed):
  pass
 def on_message(self,msg):
  raise NotImplementedError()
 def on_close(self,ex):
  logging.error('on_close() called due to %s: %s',type(ex).__name__,ex)
 def close(self,ex=None):
  raise ex if ex else exception.StopListening()
 @property
 def listener(self):
  raise NotImplementedError()
 def ensure_method(name,fn):
  if getattr(cls,name,None)is None:
   setattr(cls,name,fn)
 ensure_method('open',open)
 ensure_method('on_message',on_message)
 ensure_method('on_close',on_close)
 ensure_method('close',close)
 ensure_method('listener',listener)
 return cls
class Router(object):
 def __init__(self,key_function,routing_table):
  super(Router,self).__init__()
  self.key_function=key_function
  self.routing_table=routing_table
 def map(self,msg):
  k=self.key_function(msg)
  key=k[0]if isinstance(k,(tuple,list))else k
  return self.routing_table[key]
 def route(self,msg,*aa,**kw):
  k=self.key_function(msg)
  if isinstance(k,(tuple,list)):
   key,args,kwargs={1:tuple(k)+((),{}),2:tuple(k)+({},),3:tuple(k),}[len(k)]
  else:
   key,args,kwargs=k,(),{}
  try:
   fn=self.routing_table[key]
  except KeyError as e:
   if None in self.routing_table:
    fn=self.routing_table[None]
   else:
    raise RuntimeError('No handler for key: %s, and default handler not defined'%str(e.args))
  return fn(msg,*args,**kwargs)
class DefaultRouterMixin(object):
 def __init__(self,*args,**kwargs):
  self._router=Router(flavor,{'chat':lambda msg:self.on_chat_message(msg),'callback_query':lambda msg:self.on_callback_query(msg),'inline_query':lambda msg:self.on_inline_query(msg),'chosen_inline_result':lambda msg:self.on_chosen_inline_result(msg),'shipping_query':lambda msg:self.on_shipping_query(msg),'pre_checkout_query':lambda msg:self.on_pre_checkout_query(msg),'_idle':lambda event:self.on__idle(event)})
  super(DefaultRouterMixin,self).__init__(*args,**kwargs)
 @property
 def router(self):
  return self._router
 def on_message(self,msg):
  self._router.route(msg)
@openable
class Monitor(ListenerContext,DefaultRouterMixin):
 def __init__(self,seed_tuple,capture,**kwargs):
  bot,initial_msg,seed=seed_tuple
  super(Monitor,self).__init__(bot,seed,**kwargs)
  for pattern in capture:
   self.listener.capture(pattern)
@openable
class ChatHandler(ChatContext,DefaultRouterMixin,StandardEventMixin,IdleTerminateMixin):
 def __init__(self,seed_tuple,include_callback_query=False,**kwargs):
  bot,initial_msg,seed=seed_tuple
  super(ChatHandler,self).__init__(bot,seed,**kwargs)
  self.listener.capture([{'chat':{'id':self.chat_id}}])
  if include_callback_query:
   self.listener.capture([{'message':{'chat':{'id':self.chat_id}}}])
@openable
class UserHandler(UserContext,DefaultRouterMixin,StandardEventMixin,IdleTerminateMixin):
 def __init__(self,seed_tuple,include_callback_query=False,flavors=chat_flavors+inline_flavors,**kwargs):
  bot,initial_msg,seed=seed_tuple
  super(UserHandler,self).__init__(bot,seed,**kwargs)
  if flavors=='all':
   self.listener.capture([{'from':{'id':self.user_id}}])
  else:
   self.listener.capture([lambda msg:flavor(msg)in flavors,{'from':{'id':self.user_id}}])
  if include_callback_query:
   self.listener.capture([{'message':{'chat':{'id':self.user_id}}}])
class InlineUserHandler(UserHandler):
 def __init__(self,seed_tuple,**kwargs):
  super(InlineUserHandler,self).__init__(seed_tuple,flavors=inline_flavors,**kwargs)
@openable
class CallbackQueryOriginHandler(CallbackQueryOriginContext,DefaultRouterMixin,StandardEventMixin,IdleTerminateMixin):
 def __init__(self,seed_tuple,**kwargs):
  bot,initial_msg,seed=seed_tuple
  super(CallbackQueryOriginHandler,self).__init__(bot,seed,**kwargs)
  self.listener.capture([lambda msg:flavor(msg)=='callback_query' and origin_identifier(msg)==self.origin])
@openable
class InvoiceHandler(InvoiceContext,DefaultRouterMixin,StandardEventMixin,IdleTerminateMixin):
 def __init__(self,seed_tuple,**kwargs):
  bot,initial_msg,seed=seed_tuple
  super(InvoiceHandler,self).__init__(bot,seed,**kwargs)
  self.listener.capture([{'invoice_payload':self.payload}])
  self.listener.capture([{'successful_payment':{'invoice_payload':self.payload}}])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
