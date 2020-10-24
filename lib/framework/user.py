import os
u=None
C=False
W=str
h=True
class User:
 def __init__(self,user_id,email=u,passwd_hash=u,authenticated=C):
  self.user_id=user_id
  self.email=email
  self.passwd_hash=passwd_hash
  self.authenticated=authenticated
 def __repr__(self):
  r={'user_id':self.user_id,'email':self.email,'passwd_hash':self.passwd_hash,'authenticated':self.authenticated,}
  return W(r)
 def can_login(self,passwd_hash):
  return self.passwd_hash==passwd_hash
 def is_active(self):
  return h
 def get_id(self):
  return self.user_id
 def is_authenticated(self):
  return self.authenticated
 def is_anonymous(self):
  return C
# Created by pyminifier (https://github.com/liftoff/pyminifier)
