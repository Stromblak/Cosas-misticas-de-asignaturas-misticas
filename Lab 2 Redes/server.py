from rudp import RUDPServer
import os
import time


def eliminarTemp(lista):
	eliminar = []
	for a in lista:
		if time.time() - lista[a][1] > 2:
			eliminar.append(a)
	for e in eliminar:
		del lista[e]


key = input('Ingresar clave: ')
server = RUDPServer('localhost', 25565, key)
archivos = dict()
porcentaje = dict()
ROOT = 'Cosas'

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

			dir = []
			file = []
			for f in os.listdir(path):
				if os.path.isdir(f):
					dir.append(f)
				else:
					file.append(f)

			server.reply(address, (dir, file))

		case 'info':
			filepath = '/'.join( message )
			if filepath not in archivos:
				with open(filepath, "r") as f:
					contenido = f.read()

				data = []
				for i in range(0, len(contenido), 398):
					data.append( contenido[i:i+398] )

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

	eliminarTemp(archivos)
	eliminarTemp(porcentaje)