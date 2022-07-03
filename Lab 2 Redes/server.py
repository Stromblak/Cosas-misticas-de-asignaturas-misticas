from rudp import RUDPServer
import os

server = RUDPServer('localhost', 25565, 'key')

ROOT = 'Cosas'
con = dict()

def procesar(address, filepath, filename):
	with open(filepath, "r") as f:
		contenido = f.read()

	data = []
	for i in range(0, len(contenido), 398):
		data.append( contenido[i:i+398] )

	filesize = round(os.path.getsize(filepath) / (1000 ** 2), 3)
	partes = len(data)
	info = (filename, filesize, partes)

	server.reply(address, info)
	print(f"{address} Enviando el archivo {filename} de tamaño {filesize} MB.")
	
	return data
		
while True:
	message, address = server.receive()

	if message[0] != '/':
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
					con[address] = procesar(address, path, filename = message)
					continue
	
		files = os.listdir( '/'.join(con[address]) )
		server.reply(address, files)
		
	else:
		parte = int( message[1] )
		data = con[address]
		partes = len( data )

		if parte < partes:
			print(f"{address} Progreso: {round(100*(parte+1)/partes,2)}%")
			server.reply(address, data[parte])
		else:
			server.reply(address, '')
