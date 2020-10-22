import base64
F=len
s=chr
B=ord
x=object
Y=staticmethod
U=None
k=base64.b64decode
P=base64.b64encode
from Crypto.Cipher import AES
e=AES.MODE_CBC
G=AES.new
I=AES.block_size
from Crypto import Random
K=Random.new
from framework.logger import get_logger
from framework import app,logger
o=app.config
BS=16
pad=lambda s:s+(BS-F(s)%BS)*s(BS-F(s)%BS)
if o['config']['is_py2']:
 unpad=lambda s:s[0:-B(s[-1])]
else:
 unpad=lambda s:s[0:-s[-1]]
key='140b41b22a29beb4061bda66b6747e14'
class AESCipher(x):
 @Y
 def encrypt(raw,mykey=U):
  if o['config']['is_py2']:
   raw=pad(raw)
   iv=K().read(I)
   cipher=G(key if mykey is U else mykey,e,iv)
   ret=P(iv+cipher.encrypt(raw))
   if o['config']['is_py3']:
    ret=ret.decode()
   return ret
  else:
   raw=pad(raw)
   iv=K().read(I)
   cipher=G(key if mykey is U else mykey,e,iv)
   try:
    tmp=cipher.encrypt(raw)
   except:
    tmp=cipher.encrypt(raw.encode())
   ret=P(iv+tmp)
   if o['config']['is_py3']:
    ret=ret.decode()
   return ret
 @Y
 def decrypt(enc,mykey=U):
  enc=k(enc)
  iv=enc[:16]
  cipher=G(key if mykey is U else mykey,e,iv)
  return unpad(cipher.decrypt(enc[16:]))
if __name__=="__main__":
 key="140b41b22a29beb4061bda66b6747e14"
 text=u'안녕하세요..'
 key=key[:32]
 a=AESCipher.encrypt(text)
 b=AESCipher.decrypt(a)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
