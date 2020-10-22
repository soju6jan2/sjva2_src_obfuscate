class User:
q=None
i=False
S=str
X=True
 def __init__(self,user_id,email=q,passwd_hash=q,authenticated=i):
  self.user_id=user_id
  self.email=email
  self.passwd_hash=passwd_hash
  self.authenticated=authenticated
 def __repr__(self):
  r={'user_id':self.user_id,'email':self.email,'passwd_hash':self.passwd_hash,'authenticated':self.authenticated,}
  return S(r)
 def can_login(self,passwd_hash):
  return self.passwd_hash==passwd_hash
 def is_active(self):
  return X
 def get_id(self):
  return self.user_id
 def is_authenticated(self):
  return self.authenticated
 def is_anonymous(self):
  return i
# Created by pyminifier (https://github.com/liftoff/pyminifier)
