import socket
import pickle
import sys
import time
import hashlib
from Crypto.Cipher import AES

buffersize = 1024

# https://github.com/jorgejarai/redes_udec/tree/main/lab1-2_rtt/python
# inicios de funciones y atributos
#  publico
# _ protegido
# __ privado


class Datagram:
	def __init__(self, payload, sequence_no):
		self._payload = payload
		self._sequence_no = sequence_no


class cifrado:
	def __init__(self, key):
		self.__iv = 'This is an IV456'.encode()
		self.__hashKey = hashlib.sha256( key.encode() ).digest()
		self.__mode = AES.MODE_CFB

	def __cipher(self):
		return AES.new(self.__hashKey, self.__mode, self.__iv)

	def encrypt(self, datagram):	
		pickleData = pickle.dumps( datagram )
		cipherPickle = self.__cipher().encrypt( pickleData )
		return cipherPickle

	def decrypt(self, cipherPickle):
		pickleData = self.__cipher().decrypt( cipherPickle )

		try:
			datagram = pickle.loads( pickleData )
			return datagram
		except:
			return Datagram( ('error', -1) , -1)


class RUDPServer:
	def __init__(self, host, port, key):
		self.__aes = cifrado(key)
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.s.bind( (host, port) )
		except:
			print("Couldn't initialise server", sys.stderr)
			sys.exit(1)

	def receive(self):
		cipherPickle, address = self.s.recvfrom( buffersize )
		datagram = self.__aes.decrypt( cipherPickle )

		self.last_seqno = datagram._sequence_no
	
		return (datagram._payload, address)

	def reply(self, address, payload):
		datagram = Datagram( payload, self.last_seqno )
		cipherPickle = self.__aes.encrypt( datagram )

		self.s.sendto( cipherPickle, address )


class RUDPClient:
	def __init__(self, host, port, key):
		self.__aes = cifrado(key)
		self.address = (host, port)
		self.sequence_no = 0

		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.s.setblocking(False)
		except:
			print("Couldn't initialise client", sys.stderr)
			sys.exit(1)

	def send_recv(self, payload):
		datagram = Datagram( payload, self.sequence_no )
		cipherPickle = self.__aes.encrypt( datagram )

		t = 0.5
		send = False

		while not send and t <= 16:
			ti = time.time()
			self.s.sendto(cipherPickle, self.address)
			while True:
				try:
					if time.time() - ti > t:
						t *= 2
						break

					recvCipherPickle = self.s.recv( buffersize )
					recvDatagram = self.__aes.decrypt( recvCipherPickle )
				except BlockingIOError:
					continue

				if recvDatagram._sequence_no == self.sequence_no:
					send = True
					break

		if send:
			self.sequence_no += 1
			return recvDatagram._payload
		else:
			print("Conexion perdida con el servidor", sys.stderr)
			sys.exit(1)
