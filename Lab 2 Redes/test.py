import hashlib
from Crypto.Cipher import AES



class cifrado:
	def __init__(self, key):
		self.iv = 'This is an IV456'.encode()
		self.hashKey = hashlib.sha256( key.encode() ).digest()

	def encrypt(self, pickle):	
		cipher = AES.new(self.hashKey, AES.MODE_CFB, self.iv)
		return cipher.encrypt( pickle )

	def decrypt(self, cipherPickle):
		cipher = AES.new(self.hashKey, AES.MODE_CFB, self.iv)
		return cipher.decrypt(cipherPickle)


c = cifrado("hola")

text = b'hola'


en = c.encrypt(text)

print(en)

dec = c.decrypt(en)

print(dec)
