from rudp import RUDPServer, MAXREENVIO
from os.path import isdir, getsize
from os import listdir
import time


MAXT = MAXREENVIO*2
ROOT = ''
while True:
	r = input('Ingresar carpeta: ')
	if isdir(r):
		ROOT = r
		break
server = RUDPServer('localhost', 25565, input('Ingresar clave: '))
archivos, CotaPorcentaje = dict(), dict()

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
			carpetas = [ f for f in listdir(path) if isdir(f) ]
			noCarpetas = [ f for f in listdir(path) if not isdir(f) ]
			server.reply(address, (carpetas, noCarpetas))

		case 'info':
			filepath = '/'.join( message )
			if filepath not in archivos:
				with open(filepath, "r") as f:
					contenido = f.read()

				data = [ contenido[i:i+398] for i in range(0, len(contenido), 398) ]
				archivos[filepath] = [data, time.time()]

			filesize = round(getsize(filepath) / (1000 ** 2), 3)
			filename = message[-1]
			partes = len(data)

			CotaPorcentaje[address] = [1, time.time()]
			server.reply( address, (filename, filesize, partes) )
			print(f"{direccion}  Listo para enviar el archivo {filename} de tamaño {filesize} MB")

		case 'send':
			parte = message[0]
			filepath = '/'.join( message[1] )

			data = archivos[filepath][0]
			archivos[filepath][1] = time.time()
			CotaPorcentaje[address][1] = time.time()

			server.reply(address, data[parte])

			p = round(100*(parte+1)/len(data), 2)
			if p >= CotaPorcentaje[address][0]:
				print(f"{direccion}  Enviando: {p}%")
				CotaPorcentaje[address][0] += 1

				
	for k in list(archivos.keys()):
		if time.time() - archivos[k][1] > MAXT:
			del archivos[k]

	for k in list(CotaPorcentaje.keys()):
		if time.time() - CotaPorcentaje[k][1] > MAXT:
			del CotaPorcentaje[k]