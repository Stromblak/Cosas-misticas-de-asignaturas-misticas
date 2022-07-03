from rudp import RUDPServer
import os

server = RUDPServer('localhost', 25565)

ROOT = 'Cosas'
con = dict()

while True:
	message, address = server.receive()

	if address not in con:
		print('Nueva conexion', address)
		con[address] = [ROOT]

	match message:
		case '~':
			con[address] = [ROOT]
		case '..':
			if con[address][-1] != ROOT:
				con[address].pop()
		case _:
			con[address].append(message)
			if os.path.isfile( '/'.join( con[address] )):
				del con[address]
				break
				#pasar a enviar archivo


	files = os.listdir('/'.join( con[address] ))
	server.reply(address, files)
