from rudp import RUDPServer
import os
import time


server = RUDPServer('localhost', 25565, 'key')
archivos = dict()
ROOT = 'Cosas'

while True:
	try:
		(tipo, message), address = server.receive()
		direccion = str(address[0]) + ' ' +  str(address[1])
	except:
		continue

	match tipo:
		case 'con':
			server.reply(address, ROOT)
			print(direccion, ' Nueva conexion')

		case 'search':
			path = '/'.join( message )
			files = os.listdir(path)
			server.reply(address, files)

		case 'select':
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
			info = (filename, filesize, partes)

			server.reply(address, info)
			print(f"{direccion}  Listo para enviar el archivo {filename} de tamaño {filesize} MB")

		case 'send':
			parte = message[0]
			filepath = '/'.join( message[1] )

			data = archivos[filepath][0]
			archivos[filepath][1] = time.time()
			porcentaje = round(100*(parte+1)/len(data), 2)

			server.reply(address, data[parte])
			print(f"{direccion}  Enviando: {porcentaje}%")


	eliminar = []
	for a in archivos:
		if time.time() - archivos[a][1] > 32:
			eliminar.append(a)

	for e in eliminar:
		del archivos[e]