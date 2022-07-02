import socket
import pickle
import sys
import _thread
import threading

import hashlib
from Crypto.Cipher import AES

import rtt
buffersize = 1024

# https://github.com/jorgejarai/redes_udec/tree/main/lab1-2_rtt/python
# cambie algunas cosas, y me gustaria desacerme del rtt porque siento que es innecesario xD
# tambien hacerle un rework a los intentos de envio xD

class Datagram:
	def __init__(self, payload, address, sequence_no, timestamp):
		self.payload = payload
		self.address = address
		self.sequence_no = sequence_no
		self.timestamp = timestamp

class cifrado:
	def __init__(self, key):
		self.iv = 'This is an IV456'.encode()
		self.hashKey = hashlib.sha256( key.encode() ).digest()
		self.mode = AES.MODE_CFB

	def encrypt(self, pickle):	
		cipher = AES.new(self.hashKey, self.mode, self.iv)
		return cipher.encrypt( pickle )

	def decrypt(self, cipherPickle):
		cipher = AES.new(self.hashKey, self.mode, self.iv)
		return cipher.decrypt(cipherPickle)


class RUDPServer(cifrado):
	def __init__(self, host, port):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.s.bind( (host, port) )
		except:
			print("Couldn't initialise server", sys.stderr)
			sys.exit(1)

	def receive(self):
		data, address = self.s.recvfrom( buffersize )
		datagram = pickle.loads(data)

		self.last_seqno = datagram.sequence_no
		self.last_ts = datagram.timestamp

		return (datagram.payload, address)

	def reply(self, address, payload):
		datagram = Datagram(payload, address, self.last_seqno, self.last_ts)
		self.s.sendto( pickle.dumps(datagram), address )


class RUDPClient(cifrado):
	def __init__(self, host, port):
		self.address = (host, port)
		self.sequence_no = 0
		self.rtt = rtt.RTT()

		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.s.setblocking(False)
		except:
			print("Couldn't initialise client", sys.stderr)
			sys.exit(1)

	def send_recv(self, payload):
		timestamp = self.rtt.timestamp()

		datagram = Datagram(payload, self.address, self.sequence_no, timestamp)
		serialised_datagram = pickle.dumps(datagram)

		self.rtt.new_packet()

		event = threading.Event()

		def timeout():
			print("timeout")
			if self.rtt.timeout():
				_thread.interrupt_main()
			else:
				event.set()

		recvDatagram = None
		attempting_send = True
		while attempting_send:
			event.clear()
			self.s.sendto(serialised_datagram, self.address)

			timer = threading.Timer(self.rtt.start(), timeout)
			timer.start()

			while True:
				try:
					if event.wait(timeout=0.05):
						break

					data = self.s.recv( buffersize )
					recvDatagram = pickle.loads(data)
				except BlockingIOError:
					continue

				if recvDatagram.sequence_no == self.sequence_no:
					attempting_send = False
					break

		timer.cancel()
		self.rtt.stop(self.rtt.timestamp() - recvDatagram.timestamp)

		return recvDatagram.payload