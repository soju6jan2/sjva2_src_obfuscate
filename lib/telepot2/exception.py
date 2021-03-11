import sys
class TelepotException(Exception):
 pass
class BadFlavor(TelepotException):
 def __init__(self,offender):
  super(BadFlavor,self).__init__(offender)
 @property
 def offender(self):
  return self.args[0]
PY_3=sys.version_info.major>=3
class BadHTTPResponse(TelepotException):
 def __init__(self,status,text,response):
  super(BadHTTPResponse,self).__init__(status,text,response)
 @property
 def status(self):
  return self.args[0]
 @property
 def text(self):
  return self.args[1]
 @property
 def response(self):
  return self.args[2]
class EventNotFound(TelepotException):
 def __init__(self,event):
  super(EventNotFound,self).__init__(event)
 @property
 def event(self):
  return self.args[0]
class WaitTooLong(TelepotException):
 def __init__(self,seconds):
  super(WaitTooLong,self).__init__(seconds)
 @property
 def seconds(self):
  return self.args[0]
class IdleTerminate(WaitTooLong):
 pass
class StopListening(TelepotException):
 pass
class TelegramError(TelepotException):
 def __init__(self,description,error_code,json):
  super(TelegramError,self).__init__(description,error_code,json)
 @property
 def description(self):
  return self.args[0]
 @property
 def error_code(self):
  return self.args[1]
 @property
 def json(self):
  return self.args[2]
class UnauthorizedError(TelegramError):
 DESCRIPTION_PATTERNS=['unauthorized']
class BotWasKickedError(TelegramError):
 DESCRIPTION_PATTERNS=['bot.*kicked']
class BotWasBlockedError(TelegramError):
 DESCRIPTION_PATTERNS=['bot.*blocked']
class TooManyRequestsError(TelegramError):
 DESCRIPTION_PATTERNS=['too *many *requests']
class MigratedToSupergroupChatError(TelegramError):
 DESCRIPTION_PATTERNS=['migrated.*supergroup *chat']
class NotEnoughRightsError(TelegramError):
 DESCRIPTION_PATTERNS=['not *enough *rights']
# Created by pyminifier (https://github.com/liftoff/pyminifier)
