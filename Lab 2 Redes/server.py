from rudp import RUDPServer
import os
import sys

server = RUDPServer('localhost', 25565, 'key')

ROOT = 'Cosas'
con = dict()

def enviar(address, filepath, filename):
	filesize = round(os.path.getsize(filepath) / (1000 ** 2), 3)
	info = (message, filesize)

	server.reply(address, info)
	print(f"Enviando el archivo {filename} de tamaño {filesize} MB.")
	
	sys.exit(1)


while True:
	message, address = server.receive()

	if address not in con:
		print('Nueva conexion:', address)
		con[address] = [ROOT]

	match message:
		case '~':
			con[address] = [ROOT]

		case '..':
			if con[address][-1] != ROOT:
				con[address].pop()

		case _:
			con[address].append(message)
			
			path = '/'.join(con[address])
			if os.path.isfile(path):
				del con[address]
				enviar(address, path, filename = message)

	files = os.listdir( '/'.join(con[address]) )
	server.reply(address, files)

