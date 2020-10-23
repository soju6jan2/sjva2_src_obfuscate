import os
N=None
c=False
D=str
H=True
class User:
 def __init__(self,user_id,email=N,passwd_hash=N,authenticated=c):
  self.user_id=user_id
  self.email=email
  self.passwd_hash=passwd_hash
  self.authenticated=authenticated
 def __repr__(self):
  r={'user_id':self.user_id,'email':self.email,'passwd_hash':self.passwd_hash,'authenticated':self.authenticated,}
  return D(r)
 def can_login(self,passwd_hash):
  return self.passwd_hash==passwd_hash
 def is_active(self):
  return H
 def get_id(self):
  return self.user_id
 def is_authenticated(self):
  return self.authenticated
 def is_anonymous(self):
  return c
# Created by pyminifier (https://github.com/liftoff/pyminifier)
