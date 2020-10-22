import base64
n=len
u=chr
h=ord
j=object
O=staticmethod
b=None
from Crypto.Cipher import AES
from Crypto import Random
from framework.logger import get_logger
from framework import app,logger
BS=16
pad=lambda s:s+(BS-n(s)%BS)*u(BS-n(s)%BS)
if app.config['config']['is_py2']:
 unpad=lambda s:s[0:-h(s[-1])]
else:
 unpad=lambda s:s[0:-s[-1]]
key='140b41b22a29beb4061bda66b6747e14'
class AESCipher(j):
 @O
 def encrypt(raw,mykey=b):
  if app.config['config']['is_py2']:
   raw=pad(raw)
   iv=Random.new().read(AES.block_size)
   cipher=AES.new(key if mykey is b else mykey,AES.MODE_CBC,iv)
   ret=base64.b64encode(iv+cipher.encrypt(raw))
   if app.config['config']['is_py3']:
    ret=ret.decode()
   return ret
  else:
   raw=pad(raw)
   iv=Random.new().read(AES.block_size)
   cipher=AES.new(key if mykey is b else mykey,AES.MODE_CBC,iv)
   try:
    tmp=cipher.encrypt(raw)
   except:
    tmp=cipher.encrypt(raw.encode())
   ret=base64.b64encode(iv+tmp)
   if app.config['config']['is_py3']:
    ret=ret.decode()
   return ret
 @O
 def decrypt(enc,mykey=b):
  enc=base64.b64decode(enc)
  iv=enc[:16]
  cipher=AES.new(key if mykey is b else mykey,AES.MODE_CBC,iv)
  return unpad(cipher.decrypt(enc[16:]))
if __name__=="__main__":
 key="140b41b22a29beb4061bda66b6747e14"
 text=u'안녕하세요..'
 key=key[:32]
 a=AESCipher.encrypt(text)
 b=AESCipher.decrypt(a)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
