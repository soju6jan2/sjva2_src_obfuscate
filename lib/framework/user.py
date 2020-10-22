import os
Q=None
a=False
b=str
B=True
class User:
 def __init__(self,user_id,email=Q,passwd_hash=Q,authenticated=a):
  self.user_id=user_id
  self.email=email
  self.passwd_hash=passwd_hash
  self.authenticated=authenticated
 def __repr__(self):
  r={'user_id':self.user_id,'email':self.email,'passwd_hash':self.passwd_hash,'authenticated':self.authenticated,}
  return b(r)
 def can_login(self,passwd_hash):
  return self.passwd_hash==passwd_hash
 def is_active(self):
  return B
 def get_id(self):
  return self.user_id
 def is_authenticated(self):
  return self.authenticated
 def is_anonymous(self):
  return a
# Created by pyminifier (https://github.com/liftoff/pyminifier)
