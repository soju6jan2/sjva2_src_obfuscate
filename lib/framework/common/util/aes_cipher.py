import base64
x=len
q=chr
e=ord
u=object
y=staticmethod
H=None
from Crypto.Cipher import AES
from Crypto import Random
from framework.logger import get_logger
from framework import app,logger
BS=16
pad=lambda s:s+(BS-x(s)%BS)*q(BS-x(s)%BS)
if app.config['config']['is_py2']:
 unpad=lambda s:s[0:-e(s[-1])]
else:
 unpad=lambda s:s[0:-s[-1]]
key='140b41b22a29beb4061bda66b6747e14'
class AESCipher(u):
 @y
 def encrypt(raw,mykey=H):
  if app.config['config']['is_py2']:
   raw=pad(raw)
   iv=Random.new().read(AES.block_size)
   cipher=AES.new(key if mykey is H else mykey,AES.MODE_CBC,iv)
   ret=base64.b64encode(iv+cipher.encrypt(raw))
   if app.config['config']['is_py3']:
    ret=ret.decode()
   return ret
  else:
   raw=pad(raw)
   iv=Random.new().read(AES.block_size)
   cipher=AES.new(key if mykey is H else mykey,AES.MODE_CBC,iv)
   try:
    tmp=cipher.encrypt(raw)
   except:
    tmp=cipher.encrypt(raw.encode())
   ret=base64.b64encode(iv+tmp)
   if app.config['config']['is_py3']:
    ret=ret.decode()
   return ret
 @y
 def decrypt(enc,mykey=H):
  enc=base64.b64decode(enc)
  iv=enc[:16]
  cipher=AES.new(key if mykey is H else mykey,AES.MODE_CBC,iv)
  return unpad(cipher.decrypt(enc[16:]))
if __name__=="__main__":
 key="140b41b22a29beb4061bda66b6747e14"
 text=u'안녕하세요..'
 key=key[:32]
 a=AESCipher.encrypt(text)
 b=AESCipher.decrypt(a)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
