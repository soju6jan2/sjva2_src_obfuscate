import base64
t=len
z=chr
S=ord
q=object
r=staticmethod
p=None
u=base64.b64decode
I=base64.b64encode
from Crypto.Cipher import AES
v=AES.MODE_CBC
N=AES.new
D=AES.block_size
from Crypto import Random
V=Random.new
from framework.logger import get_logger
from framework import app,logger
y=app.config
BS=16
pad=lambda s:s+(BS-t(s)%BS)*z(BS-t(s)%BS)
if y['config']['is_py2']:
 unpad=lambda s:s[0:-S(s[-1])]
else:
 unpad=lambda s:s[0:-s[-1]]
key='140b41b22a29beb4061bda66b6747e14'
class AESCipher(q):
 @r
 def encrypt(raw,mykey=p):
  if y['config']['is_py2']:
   raw=pad(raw)
   iv=V().read(D)
   cipher=N(key if mykey is p else mykey,v,iv)
   ret=I(iv+cipher.encrypt(raw))
   if y['config']['is_py3']:
    ret=ret.decode()
   return ret
  else:
   raw=pad(raw)
   iv=V().read(D)
   cipher=N(key if mykey is p else mykey,v,iv)
   try:
    tmp=cipher.encrypt(raw)
   except:
    tmp=cipher.encrypt(raw.encode())
   ret=I(iv+tmp)
   if y['config']['is_py3']:
    ret=ret.decode()
   return ret
 @r
 def decrypt(enc,mykey=p):
  enc=u(enc)
  iv=enc[:16]
  cipher=N(key if mykey is p else mykey,v,iv)
  return unpad(cipher.decrypt(enc[16:]))
if __name__=="__main__":
 key="140b41b22a29beb4061bda66b6747e14"
 text=u'안녕하세요..'
 key=key[:32]
 a=AESCipher.encrypt(text)
 b=AESCipher.decrypt(a)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
