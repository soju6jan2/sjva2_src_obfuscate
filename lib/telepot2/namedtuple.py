import collections
import warnings
import sys
class _Field(object):
 def __init__(self,name,constructor=None,default=None):
  self.name=name
  self.constructor=constructor
  self.default=default
def _create_class(typename,fields):
 field_names=[e.name if type(e)is _Field else e for e in fields]
 keymap=[(k.rstrip('_'),k)for k in filter(lambda e:e in['from_'],field_names)]
 conversions=[(e.name,e.constructor)for e in fields if type(e)is _Field and e.constructor is not None]
 defaults=[e.default if type(e)is _Field else None for e in fields]
 base=collections.namedtuple(typename,field_names)
 base.__new__.__defaults__=tuple(defaults)
 class sub(base):
  def __new__(cls,**kwargs):
   for oldkey,newkey in keymap:
    if oldkey in kwargs:
     kwargs[newkey]=kwargs[oldkey]
     del kwargs[oldkey]
   unexpected=set(kwargs.keys())-set(super(sub,cls)._fields)
   if unexpected:
    for k in unexpected:
     del kwargs[k]
    s=('Unexpected fields: '+', '.join(unexpected)+'' '\nBot API seems to have added new fields to the returned data.' ' This version of namedtuple is not able to capture them.' '\n\nPlease upgrade telepot by:' '\n  sudo pip install telepot --upgrade' '\n\nIf you still see this message after upgrade, that means I am still working to bring the code up-to-date.' ' Please try upgrade again a few days later.' ' In the meantime, you can access the new fields the old-fashioned way, through the raw dictionary.')
    warnings.warn(s,UserWarning)
   for key,func in conversions:
    if key in kwargs:
     if type(kwargs[key])is dict:
      kwargs[key]=func(**kwargs[key])
     elif type(kwargs[key])is list:
      kwargs[key]=func(kwargs[key])
     else:
      raise RuntimeError('Can only convert dict or list')
   return super(sub,cls).__new__(cls,**kwargs)
 if sys.version_info>=(3,4):
  def _asdict(self):
   return collections.OrderedDict(zip(self._fields,self))
  sub._asdict=_asdict
 sub.__name__=typename
 return sub
"""
Different treatments for incoming and outgoing namedtuples:
- Incoming ones require type declarations for certain fields for deeper parsing.
- Outgoing ones need no such declarations because users are expected to put the correct object in place.
"""
def _Message(**kwargs):
 return getattr(sys.modules[__name__],'Message')(**kwargs)
User=_create_class('User',['id','is_bot','first_name','last_name','username','language_code'])
def UserArray(data):
 return[User(**p)for p in data]
ChatPhoto=_create_class('ChatPhoto',['small_file_id','big_file_id',])
Chat=_create_class('Chat',['id','type','title','username','first_name','last_name','all_members_are_administrators',_Field('photo',constructor=ChatPhoto),'description','invite_link',_Field('pinned_message',constructor=_Message),'sticker_set_name','can_set_sticker_set',])
PhotoSize=_create_class('PhotoSize',['file_id','width','height','file_size','file_path',])
Audio=_create_class('Audio',['file_id','duration','performer','title','mime_type','file_size'])
Document=_create_class('Document',['file_id',_Field('thumb',constructor=PhotoSize),'file_name','mime_type','file_size','file_path',])
MaskPosition=_create_class('MaskPosition',['point','x_shift','y_shift','scale',])
Sticker=_create_class('Sticker',['file_id','width','height',_Field('thumb',constructor=PhotoSize),'emoji','set_name',_Field('mask_position',constructor=MaskPosition),'file_size',])
def StickerArray(data):
 return[Sticker(**p)for p in data]
StickerSet=_create_class('StickerSet',['name','title','contains_masks',_Field('stickers',constructor=StickerArray),])
Video=_create_class('Video',['file_id','width','height','duration',_Field('thumb',constructor=PhotoSize),'mime_type','file_size','file_path',])
Voice=_create_class('Voice',['file_id','duration','mime_type','file_size'])
VideoNote=_create_class('VideoNote',['file_id','length','duration',_Field('thumb',constructor=PhotoSize),'file_size'])
Contact=_create_class('Contact',['phone_number','first_name','last_name','user_id'])
Location=_create_class('Location',['longitude','latitude'])
Venue=_create_class('Venue',[_Field('location',constructor=Location),'title','address','foursquare_id',])
File=_create_class('File',['file_id','file_size','file_path'])
def PhotoSizeArray(data):
 return[PhotoSize(**p)for p in data]
def PhotoSizeArrayArray(data):
 return[[PhotoSize(**p)for p in array]for array in data]
UserProfilePhotos=_create_class('UserProfilePhotos',['total_count',_Field('photos',constructor=PhotoSizeArrayArray)])
ChatMember=_create_class('ChatMember',[_Field('user',constructor=User),'status','until_date','can_be_edited','can_change_info','can_post_messages','can_edit_messages','can_delete_messages','can_invite_users','can_restrict_members','can_pin_messages','can_promote_members','can_send_messages','can_send_media_messages','can_send_other_messages','can_add_web_page_previews',])
def ChatMemberArray(data):
 return[ChatMember(**p)for p in data]
ReplyKeyboardMarkup=_create_class('ReplyKeyboardMarkup',['keyboard','resize_keyboard','one_time_keyboard','selective',])
KeyboardButton=_create_class('KeyboardButton',['text','request_contact','request_location',])
ReplyKeyboardRemove=_create_class('ReplyKeyboardRemove',[_Field('remove_keyboard',default=True),'selective',])
ForceReply=_create_class('ForceReply',[_Field('force_reply',default=True),'selective',])
InlineKeyboardButton=_create_class('InlineKeyboardButton',['text','url','callback_data','switch_inline_query','switch_inline_query_current_chat','callback_game','pay',])
InlineKeyboardMarkup=_create_class('InlineKeyboardMarkup',['inline_keyboard',])
MessageEntity=_create_class('MessageEntity',['type','offset','length','url',_Field('user',constructor=User),])
def MessageEntityArray(data):
 return[MessageEntity(**p)for p in data]
GameHighScore=_create_class('GameHighScore',['position',_Field('user',constructor=User),'score',])
Animation=_create_class('Animation',['file_id',_Field('thumb',constructor=PhotoSize),'file_name','mime_type','file_size',])
Game=_create_class('Game',['title','description',_Field('photo',constructor=PhotoSizeArray),'text',_Field('text_entities',constructor=MessageEntityArray),_Field('animation',constructor=Animation),])
Invoice=_create_class('Invoice',['title','description','start_parameter','currency','total_amount',])
LabeledPrice=_create_class('LabeledPrice',['label','amount',])
ShippingOption=_create_class('ShippingOption',['id','title','prices',])
ShippingAddress=_create_class('ShippingAddress',['country_code','state','city','street_line1','street_line2','post_code',])
OrderInfo=_create_class('OrderInfo',['name','phone_number','email',_Field('shipping_address',constructor=ShippingAddress),])
ShippingQuery=_create_class('ShippingQuery',['id',_Field('from_',constructor=User),'invoice_payload',_Field('shipping_address',constructor=ShippingAddress),])
PreCheckoutQuery=_create_class('PreCheckoutQuery',['id',_Field('from_',constructor=User),'currency','total_amount','invoice_payload','shipping_option_id',_Field('order_info',constructor=OrderInfo),])
SuccessfulPayment=_create_class('SuccessfulPayment',['currency','total_amount','invoice_payload','shipping_option_id',_Field('order_info',constructor=OrderInfo),'telegram_payment_charge_id','provider_payment_charge_id',])
Message=_create_class('Message',['message_id',_Field('from_',constructor=User),'date',_Field('chat',constructor=Chat),_Field('forward_from',constructor=User),_Field('forward_from_chat',constructor=Chat),'forward_from_message_id','forward_signature','forward_date',_Field('reply_to_message',constructor=_Message),'edit_date','author_signature','text',_Field('entities',constructor=MessageEntityArray),_Field('caption_entities',constructor=MessageEntityArray),_Field('audio',constructor=Audio),_Field('document',constructor=Document),_Field('game',constructor=Game),_Field('photo',constructor=PhotoSizeArray),_Field('sticker',constructor=Sticker),_Field('video',constructor=Video),_Field('voice',constructor=Voice),_Field('video_note',constructor=VideoNote),_Field('new_chat_members',constructor=UserArray),'caption',_Field('contact',constructor=Contact),_Field('location',constructor=Location),_Field('venue',constructor=Venue),_Field('new_chat_member',constructor=User),_Field('left_chat_member',constructor=User),'new_chat_title',_Field('new_chat_photo',constructor=PhotoSizeArray),'delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id',_Field('pinned_message',constructor=_Message),_Field('invoice',constructor=Invoice),_Field('successful_payment',constructor=SuccessfulPayment),'connected_website',])
InlineQuery=_create_class('InlineQuery',['id',_Field('from_',constructor=User),_Field('location',constructor=Location),'query','offset',])
ChosenInlineResult=_create_class('ChosenInlineResult',['result_id',_Field('from_',constructor=User),_Field('location',constructor=Location),'inline_message_id','query',])
CallbackQuery=_create_class('CallbackQuery',['id',_Field('from_',constructor=User),_Field('message',constructor=Message),'inline_message_id','chat_instance','data','game_short_name',])
Update=_create_class('Update',['update_id',_Field('message',constructor=Message),_Field('edited_message',constructor=Message),_Field('channel_post',constructor=Message),_Field('edited_channel_post',constructor=Message),_Field('inline_query',constructor=InlineQuery),_Field('chosen_inline_result',constructor=ChosenInlineResult),_Field('callback_query',constructor=CallbackQuery),])
def UpdateArray(data):
 return[Update(**u)for u in data]
WebhookInfo=_create_class('WebhookInfo',['url','has_custom_certificate','pending_update_count','last_error_date','last_error_message',])
InputTextMessageContent=_create_class('InputTextMessageContent',['message_text','parse_mode','disable_web_page_preview',])
InputLocationMessageContent=_create_class('InputLocationMessageContent',['latitude','longitude','live_period',])
InputVenueMessageContent=_create_class('InputVenueMessageContent',['latitude','longitude','title','address','foursquare_id',])
InputContactMessageContent=_create_class('InputContactMessageContent',['phone_number','first_name','last_name',])
InlineQueryResultArticle=_create_class('InlineQueryResultArticle',[_Field('type',default='article'),'id','title','input_message_content','reply_markup','url','hide_url','description','thumb_url','thumb_width','thumb_height',])
InlineQueryResultPhoto=_create_class('InlineQueryResultPhoto',[_Field('type',default='photo'),'id','photo_url','thumb_url','photo_width','photo_height','title','description','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultGif=_create_class('InlineQueryResultGif',[_Field('type',default='gif'),'id','gif_url','gif_width','gif_height','gif_duration','thumb_url','title','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultMpeg4Gif=_create_class('InlineQueryResultMpeg4Gif',[_Field('type',default='mpeg4_gif'),'id','mpeg4_url','mpeg4_width','mpeg4_height','mpeg4_duration','thumb_url','title','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultVideo=_create_class('InlineQueryResultVideo',[_Field('type',default='video'),'id','video_url','mime_type','thumb_url','title','caption','parse_mode','video_width','video_height','video_duration','description','reply_markup','input_message_content',])
InlineQueryResultAudio=_create_class('InlineQueryResultAudio',[_Field('type',default='audio'),'id','audio_url','title','caption','parse_mode','performer','audio_duration','reply_markup','input_message_content',])
InlineQueryResultVoice=_create_class('InlineQueryResultVoice',[_Field('type',default='voice'),'id','voice_url','title','caption','parse_mode','voice_duration','reply_markup','input_message_content',])
InlineQueryResultDocument=_create_class('InlineQueryResultDocument',[_Field('type',default='document'),'id','title','caption','parse_mode','document_url','mime_type','description','reply_markup','input_message_content','thumb_url','thumb_width','thumb_height',])
InlineQueryResultLocation=_create_class('InlineQueryResultLocation',[_Field('type',default='location'),'id','latitude','longitude','title','live_period','reply_markup','input_message_content','thumb_url','thumb_width','thumb_height',])
InlineQueryResultVenue=_create_class('InlineQueryResultVenue',[_Field('type',default='venue'),'id','latitude','longitude','title','address','foursquare_id','reply_markup','input_message_content','thumb_url','thumb_width','thumb_height',])
InlineQueryResultContact=_create_class('InlineQueryResultContact',[_Field('type',default='contact'),'id','phone_number','first_name','last_name','reply_markup','input_message_content','thumb_url','thumb_width','thumb_height',])
InlineQueryResultGame=_create_class('InlineQueryResultGame',[_Field('type',default='game'),'id','game_short_name','reply_markup',])
InlineQueryResultCachedPhoto=_create_class('InlineQueryResultCachedPhoto',[_Field('type',default='photo'),'id','photo_file_id','title','description','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultCachedGif=_create_class('InlineQueryResultCachedGif',[_Field('type',default='gif'),'id','gif_file_id','title','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultCachedMpeg4Gif=_create_class('InlineQueryResultCachedMpeg4Gif',[_Field('type',default='mpeg4_gif'),'id','mpeg4_file_id','title','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultCachedSticker=_create_class('InlineQueryResultCachedSticker',[_Field('type',default='sticker'),'id','sticker_file_id','reply_markup','input_message_content',])
InlineQueryResultCachedDocument=_create_class('InlineQueryResultCachedDocument',[_Field('type',default='document'),'id','title','document_file_id','description','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultCachedVideo=_create_class('InlineQueryResultCachedVideo',[_Field('type',default='video'),'id','video_file_id','title','description','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultCachedVoice=_create_class('InlineQueryResultCachedVoice',[_Field('type',default='voice'),'id','voice_file_id','title','caption','parse_mode','reply_markup','input_message_content',])
InlineQueryResultCachedAudio=_create_class('InlineQueryResultCachedAudio',[_Field('type',default='audio'),'id','audio_file_id','caption','parse_mode','reply_markup','input_message_content',])
InputMediaPhoto=_create_class('InputMediaPhoto',[_Field('type',default='photo'),'media','caption','parse_mode',])
InputMediaVideo=_create_class('InputMediaVideo',[_Field('type',default='video'),'media','caption','parse_mode','width','height','duration','supports_streaming',])
ResponseParameters=_create_class('ResponseParameters',['migrate_to_chat_id','retry_after',])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
