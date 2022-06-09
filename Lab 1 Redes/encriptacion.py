# pip install rsa
# https://stuvel.eu/python-rsa-doc/

import rsa
import os
from Crypto.Cipher import AES

# RSA
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


# AES
def encrypt_sim(message):
	obj = AES.new('This is a key123'.encode('utf-8'), AES.MODE_CFB, 'This is an IV456'.encode('utf-8'))
	ciphertext = obj.encrypt(message.encode('utf-8'))
	return ciphertext

def decrypt_sim(ciphertext):
	obj2 = AES.new('This is a key123'.encode('utf-8'), AES.MODE_CFB, 'This is an IV456'.encode('utf-8'))
	message = obj2.decrypt(ciphertext).decode('utf-8')
	return message