import traceback
from functools import wraps
from.import exception
from.import flavor,peel,is_event,chat_flavors,inline_flavors
def _wrap_none(fn):
 def w(*args,**kwargs):
  try:
   return fn(*args,**kwargs)
  except(KeyError,exception.BadFlavor):
   return None
 return w
def per_chat_id(types='all'):
 return _wrap_none(lambda msg:msg['chat']['id']if types=='all' or msg['chat']['type']in types else None)
def per_chat_id_in(s,types='all'):
 return _wrap_none(lambda msg:msg['chat']['id']if(types=='all' or msg['chat']['type']in types)and msg['chat']['id']in s else None)
def per_chat_id_except(s,types='all'):
 return _wrap_none(lambda msg:msg['chat']['id']if(types=='all' or msg['chat']['type']in types)and msg['chat']['id']not in s else None)
def per_from_id(flavors=chat_flavors+inline_flavors):
 return _wrap_none(lambda msg:msg['from']['id']if flavors=='all' or flavor(msg)in flavors else None)
def per_from_id_in(s,flavors=chat_flavors+inline_flavors):
 return _wrap_none(lambda msg:msg['from']['id']if(flavors=='all' or flavor(msg)in flavors)and msg['from']['id']in s else None)
def per_from_id_except(s,flavors=chat_flavors+inline_flavors):
 return _wrap_none(lambda msg:msg['from']['id']if(flavors=='all' or flavor(msg)in flavors)and msg['from']['id']not in s else None)
def per_inline_from_id():
 return per_from_id(flavors=inline_flavors)
def per_inline_from_id_in(s):
 return per_from_id_in(s,flavors=inline_flavors)
def per_inline_from_id_except(s):
 return per_from_id_except(s,flavors=inline_flavors)
def per_application():
 return lambda msg:1
def per_message(flavors='all'):
 return _wrap_none(lambda msg:[]if flavors=='all' or flavor(msg)in flavors else None)
def per_event_source_id(event_space):
 def f(event):
  if is_event(event):
   v=peel(event)
   if v['source']['space']==event_space:
    return v['source']['id']
   else:
    return None
  else:
   return None
 return _wrap_none(f)
def per_callback_query_chat_id(types='all'):
 def f(msg):
  if(flavor(msg)=='callback_query' and 'message' in msg and(types=='all' or msg['message']['chat']['type']in types)):
   return msg['message']['chat']['id']
  else:
   return None
 return f
def per_callback_query_origin(origins='all'):
 def f(msg):
  def origin_type_ok():
   return(origins=='all' or('chat' in origins and 'message' in msg)or('inline' in origins and 'inline_message_id' in msg))
  if flavor(msg)=='callback_query' and origin_type_ok():
   if 'inline_message_id' in msg:
    return msg['inline_message_id'],
   else:
    return msg['message']['chat']['id'],msg['message']['message_id']
  else:
   return None
 return f
def per_invoice_payload():
 def f(msg):
  if 'successful_payment' in msg:
   return msg['successful_payment']['invoice_payload']
  else:
   return msg['invoice_payload']
 return _wrap_none(f)
def call(func,*args,**kwargs):
 def f(seed_tuple):
  return func,(seed_tuple,)+args,kwargs
 return f
def create_run(cls,*args,**kwargs):
 def f(seed_tuple):
  j=cls(seed_tuple,*args,**kwargs)
  return j.run
 return f
def create_open(cls,*args,**kwargs):
 def f(seed_tuple):
  j=cls(seed_tuple,*args,**kwargs)
  def wait_loop():
   bot,msg,seed=seed_tuple
   try:
    handled=j.open(msg,seed)
    if not handled:
     j.on_message(msg)
    while 1:
     msg=j.listener.wait()
     j.on_message(msg)
   except(exception.IdleTerminate,exception.StopListening)as e:
    j.on_close(e)
   except Exception as e:
    traceback.print_exc()
    j.on_close(e)
  return wait_loop
 return f
def until(condition,fns):
 def f(msg):
  for fn in fns:
   seed=fn(msg)
   if condition(seed):
    return seed
  return None
 return f
def chain(*fns):
 return until(lambda seed:seed is not None,fns)
def _ensure_seeders_list(fn):
 @wraps(fn)
 def e(seeders,*aa,**kw):
  return fn(seeders if isinstance(seeders,list)else[seeders],*aa,**kw)
 return e
@_ensure_seeders_list
def pair(seeders,delegator_factory,*args,**kwargs):
 return(chain(*seeders)if len(seeders)>1 else seeders[0],delegator_factory(*args,**kwargs))
def _natural_numbers():
 x=0
 while 1:
  x+=1
  yield x
_event_space=_natural_numbers()
def pave_event_space(fn=pair):
 global _event_space
 event_space=next(_event_space)
 @_ensure_seeders_list
 def p(seeders,delegator_factory,*args,**kwargs):
  return fn(seeders+[per_event_source_id(event_space)],delegator_factory,*args,event_space=event_space,**kwargs)
 return p
def include_callback_query_chat_id(fn=pair,types='all'):
 @_ensure_seeders_list
 def p(seeders,delegator_factory,*args,**kwargs):
  return fn(seeders+[per_callback_query_chat_id(types=types)],delegator_factory,*args,include_callback_query=True,**kwargs)
 return p
from.import helper
def intercept_callback_query_origin(fn=pair,origins='all'):
 origin_map=helper.SafeDict()
 def tuplize(fn):
  def tp(msg):
   return(fn(msg),)
  return tp
 router=helper.Router(tuplize(per_callback_query_origin(origins=origins)),origin_map)
 def modify_origin_map(origin,dest,set):
  if set:
   origin_map[origin]=dest
  else:
   try:
    del origin_map[origin]
   except KeyError:
    pass
 if origins=='all':
  intercept=modify_origin_map
 else:
  intercept=(modify_origin_map if 'chat' in origins else False,modify_origin_map if 'inline' in origins else False)
 @_ensure_seeders_list
 def p(seeders,delegator_factory,*args,**kwargs):
  return fn(seeders+[_wrap_none(router.map)],delegator_factory,*args,intercept_callback_query=intercept,**kwargs)
 return p
# Created by pyminifier (https://github.com/liftoff/pyminifier)
