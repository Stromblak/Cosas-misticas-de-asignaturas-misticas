import socket
import pickle
import sys
import time
import hashlib
from Crypto.Cipher import AES


BUFFERSIZE = 1024
MINREENVIO = 0.5
MAXREENVIO = 8


class Datagram:
    def __init__(self, payload, sequence_no):
        self._payload = payload
        self._sequence = sequence_no


class cifrado:
    def __init__(self, key):
        self.__iv = 'This is an IV456'.encode()
        self.__hashKey = hashlib.sha256(key.encode()).digest()
        self.__mode = AES.MODE_CFB

    def __cipher(self):
        return AES.new(self.__hashKey, self.__mode, self.__iv)

    def encrypt(self, datagram):
        pickleData = pickle.dumps(datagram)
        cipherPickle = self.__cipher().encrypt(pickleData)
        return cipherPickle

    def decrypt(self, cipherPickle):
        pickleData = self.__cipher().decrypt(cipherPickle)

        try:
            datagram = pickle.loads(pickleData)
            return datagram
        except:
            return Datagram(('error', -1), -1)


class RUDPServer:
    def __init__(self, host, port, key):
        self.__aes = cifrado(key)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((host, port))
        except:
            print("Couldn't initialise server", sys.stderr)
            sys.exit(1)

    def receive(self):
        cipherPickle, address = self.s.recvfrom(BUFFERSIZE)
        datagram = self.__aes.decrypt(cipherPickle)

        self.last_seqno = datagram._sequence

        return (datagram._payload, address)

    def reply(self, address, payload):
        datagram = Datagram(payload, self.last_seqno)
        cipherPickle = self.__aes.encrypt(datagram)

        self.s.sendto(cipherPickle, address)


class RUDPClient:
    def __init__(self, host, port, key):
        self.__aes = cifrado(key)
        self.address = (host, port)
        self.sequence = 0

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.setblocking(False)
        except:
            print("Couldn't initialise client", sys.stderr)
            sys.exit(1)

    def send_recv(self, payload):
        datagram = Datagram(payload, self.sequence)
        cipherPickle = self.__aes.encrypt(datagram)

        t = MINREENVIO
        send = False
        while not send and t <= MAXREENVIO:
            if t >= 2:
                print('Sin respuesta')

            ti = time.time()
            self.s.sendto(cipherPickle, self.address)
            while True:
                try:
                    if time.time() - ti > t:
                        t *= 2
                        break

                    recvCipherPickle = self.s.recv(BUFFERSIZE)
                    recvDatagram = self.__aes.decrypt(recvCipherPickle)
                except:
                    continue

                if recvDatagram._sequence == self.sequence:
                    send = True
                    break

        if send:
            self.sequence += 1
            return recvDatagram._payload
        else:
            print("Fallo en la conexion con el servidor")
            sys.exit(1)
