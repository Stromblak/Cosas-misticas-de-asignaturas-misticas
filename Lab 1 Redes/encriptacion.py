# pip install rsa
# https://stuvel.eu/python-rsa-doc/

import rsa
import os
from Crypto.Cipher import AES

# RSA
dirPublica = "server//publicKey.pem"
dirPrivada = "server//privateKey.pem"

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

def encrypt_asim(message):
	return rsa.encrypt(message.encode(), publicKey())

def decrypt_asim(ciphertext):
	return rsa.decrypt(ciphertext, privateKey()).decode()


# AES
clave = "????"
iv = "???"

def encrypt_sim(message):
	obj = AES.new('This is a key123'.encode(), AES.MODE_CFB, 'This is an IV456'.encode())
	ciphertext = obj.encrypt(message.encode())
	return ciphertext

def decrypt_sim(ciphertext):
	obj2 = AES.new('This is a key123'.encode(), AES.MODE_CFB, 'This is an IV456'.encode())
	message = obj2.decrypt(ciphertext).decode()
	return message