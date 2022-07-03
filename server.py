from rudp import RUDPServer
import os


server = RUDPServer('localhost', 25565, 'key')
ROOT = 'Cosas'
con = dict()

while True:
	message, address = server.receive()

	if address not in con:
		print(address, ' Conexion entrante')
		con[address] = 1
		server.reply(address, ROOT)
		continue

	match message[0]:
		case 'search':
			path = '/'.join( message[1] )
			files = os.listdir(path)
			server.reply(address, files)

		case 'select':
			filepath = '/'.join( message[1] )
			with open(filepath, "r") as f:
				contenido = f.read()

			data = []
			for i in range(0, len(contenido), 398):
				data.append( contenido[i:i+398] )

			filesize = round(os.path.getsize(filepath) / (1000 ** 2), 3)
			filename = message[1][-1]
			partes = len(data)
			info = (filename, filesize, partes)

			con[address] = data
			server.reply(address, info)

			print(f"{address}  Listo para enviar el archivo {filename} de tamaño {filesize} MB")

		case 'download':
			parte = message[1]
			data = con[address]
			porcentaje = round(100*(parte+1)/len(data), 2)

			print(f"{address}  Enviando: {porcentaje}%")
			server.reply(address, data[parte])
		
		case 'fin':
			del con[address]
			server.reply(address, '')
			print(f"{address}  Finalizado")