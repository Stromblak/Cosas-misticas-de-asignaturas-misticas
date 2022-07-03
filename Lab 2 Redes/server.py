from rudp import RUDPServer
import os


server = RUDPServer('localhost', 25565, 'key')
con = dict()
ROOT = 'Cosas'

while True:
	(tipo, message), address = server.receive()
	direccion = str(address[0]) + ' ' +  str(address[1])

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
			with open(filepath, "r") as f:
				contenido = f.read()

			data = []
			for i in range(0, len(contenido), 398):
				data.append( contenido[i:i+398] )

			filesize = round(os.path.getsize(filepath) / (1000 ** 2), 3)
			filename = message[-1]
			partes = len(data)
			info = (filename, filesize, partes)

			con[address] = data
			server.reply(address, info)
			print(f"{direccion}  Listo para enviar el archivo {filename} de tamaño {filesize} MB")

		case 'download':
			parte = message
			data = con[address]
			porcentaje = round(100*(parte+1)/len(data), 2)

			server.reply(address, data[parte])
			print(f"{direccion}  Enviando: {porcentaje}%")
		
		case 'fin':
			del con[address]
			server.reply(address, '')
			print(f"{direccion}  Finalizado")