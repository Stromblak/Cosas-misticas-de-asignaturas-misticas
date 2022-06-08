# pip install rsa
# https://stuvel.eu/python-rsa-doc/

import rsa
import os

dirPublica = 'publicKey.pem'
dirPrivada = 'privateKey.pem'

def generateKeys():
	(publicKey, privateKey) = rsa.newkeys(4092)
	with open(dirPublica, 'wb') as p:
		p.write( publicKey.save_pkcs1('PEM') )
	with open(dirPrivada, 'wb') as p:
		p.write( privateKey.save_pkcs1('PEM') )


def privateKey():
	if not os.path.exists(dirPrivada):
		generateKeys()

	with open(dirPrivada, 'rb') as p:
		privateKey = rsa.PrivateKey.load_pkcs1(p.read())
	return privateKey

def publicKey():
	if not os.path.exists(dirPublica):
		generateKeys()

	with open(dirPublica, 'rb') as p:
		publicKey = rsa.PublicKey.load_pkcs1(p.read())
	return publicKey

def encrypt(message):
	return rsa.encrypt(message.encode('utf-8'), publicKey())

def decrypt(ciphertext):
	return rsa.decrypt(ciphertext, privateKey()).decode('utf-8')