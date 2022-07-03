from audioop import add
from rudp import RUDPServer
import os

from collections import defaultdict

server = RUDPServer('localhost', 25565)

ROOT = 'Cosas'
con = dict()

while True:
	message, address = server.receive()

	if address not in con:
		print('Nueva conexxion', address)
		con[address] = [ROOT]

	match message:
		case '~':
			con[address] = [ROOT]
		case '..':
			if con[address][-1] != ROOT:
				dir.pop()
		case _:
			con[address].append(message)
			if os.path.isfile( '/'.join( con[address] )):
				del con[address]
				break
				#pasar a enviar archivo


	files = os.listdir('/'.join( con[address] ))
	server.reply(address, files)
