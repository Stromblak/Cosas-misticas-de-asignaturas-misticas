from rudp import RUDPServer
import os
import time


MAXT = 32
ROOT = 'Cosas'

key = input('Ingresar clave: ')
server = RUDPServer('localhost', 25565, key)
archivos = dict()
porcentaje = dict()

print('Servidor inicializado')
while True:
	(tipo, message), address = server.receive()
	direccion = str(address[0]) + ' ' +  str(address[1])
	
	match tipo:
		case 'root':
			server.reply(address, ROOT)
			print(direccion, ' Nueva conexion')

		case 'search':
			path = '/'.join( message )
			carpetas = [ f for f in os.listdir(path) if os.path.isdir(f) ]
			noCarpetas = [ f for f in os.listdir(path) if not os.path.isdir(f) ]
			server.reply(address, (carpetas, noCarpetas))

		case 'info':
			filepath = '/'.join( message )
			if filepath not in archivos:
				with open(filepath, "r") as f:
					contenido = f.read()

				data = [ contenido[i:i+398] for i in range(0, len(contenido), 398) ]
				archivos[filepath] = [data, time.time()]

			filesize = round(os.path.getsize(filepath) / (1000 ** 2), 3)
			filename = message[-1]
			partes = len(data)

			porcentaje[address] = [1, time.time()]
			server.reply( address, (filename, filesize, partes) )
			print(f"{direccion}  Listo para enviar el archivo {filename} de tamaño {filesize} MB")

		case 'send':
			parte = message[0]
			filepath = '/'.join( message[1] )

			data = archivos[filepath][0]
			archivos[filepath][1] = time.time()
			porcentaje[address][1] = time.time()

			server.reply(address, data[parte])

			p = round(100*(parte+1)/len(data), 2)
			if p >= porcentaje[address][0]:
				print(f"{direccion}  Enviando: {p}%")
				porcentaje[address][0] += 1

				
	for k in list(archivos.keys()):
		if time.time() - archivos[k][1] > MAXT:
			del archivos[k]

	for k in list(porcentaje.keys()):
		if time.time() - porcentaje[k][1] > MAXT:
			del porcentaje[k]