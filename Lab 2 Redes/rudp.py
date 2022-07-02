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
	def __init__(self, payload, address, sequence_no):
		self._payload = payload
		self._address = address
		self._sequence_no = sequence_no

class cifrado:
	def __init__(self, key):
		self.__iv = 'This is an IV456'.encode()
		self.__hashKey = hashlib.sha256( key.encode() ).digest()
		self.__mode = AES.MODE_CFB

	def encrypt(self, pickle):	
		cipher = AES.new(self.__hashKey, self.__mode, self.__iv)
		return cipher.encrypt( pickle )

	def decrypt(self, cipherPickle):
		cipher = AES.new(self.__hashKey, self.__mode, self.__iv)
		return cipher.decrypt( cipherPickle )


class RUDPServer(cifrado):
	def __init__(self, host, port):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.s.bind( (host, port) )
		except:
			print("Couldn't initialise server", sys.stderr)
			sys.exit(1)

	def receive(self):
		pickleData, address = self.s.recvfrom( buffersize )
		datagram = pickle.loads( pickleData )

		self.last_seqno = datagram._sequence_no
		
		return (datagram._payload, address)

	def reply(self, address, payload):
		datagram = Datagram(payload, address, self.last_seqno)
		self.s.sendto( pickle.dumps(datagram), address )


class RUDPClient(cifrado):
	def __init__(self, host, port):
		self.address = (host, port)
		self.sequence_no = 0

		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.s.setblocking(False)
		except:
			print("Couldn't initialise client", sys.stderr)
			sys.exit(1)

	def send_recv(self, payload):
		datagram = Datagram(payload, self.address, self.sequence_no)
		pickleData = pickle.dumps(datagram)

		t = 0.5
		send = False

		while not send and t <= 16:
			ti = time.time()
			self.s.sendto(pickleData, self.address)
			while True:
				try:
					if time.time() - ti > t:
						t *= 2
						break

					recvPickleData = self.s.recv( buffersize )
					recvDatagram = pickle.loads( recvPickleData )

				except BlockingIOError:
					continue

				if recvDatagram._sequence_no == self.sequence_no:
					send = True
					break

		if send:
			return recvDatagram._payload
		else:
			pass
			# error?		
