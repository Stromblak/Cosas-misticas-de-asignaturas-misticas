from rudp import RUDPClient
from rudp import Datagram
import sys
import os


client = RUDPClient("localhost", 25565, 'key')
archivos = client.send_recv('~')

print('(carpeta): Moverse a la carpeta')
print('(archivo): Descargar archivo')
print('..       : Retroceder')
print('~        : Volver al inicio')
print('close    : Salir')
print()

while True:
	# si son muchos archivos aqui es una linea gigante
	print( '    '.join(archivos) )
	accion = input()
	print()

	if accion in ['..', '~']:
		archivos = client.send_recv( accion )
		
	elif accion in archivos:
		if accion.split('.')[-1] in ['txt', 'bin', 'py']:
			info = client.send_recv( accion )
			break
		else: 
			archivos = client.send_recv( accion )

	elif accion == 'close':
		sys.exit(1)


filename = info[0]
filesize = info[1]
partes = info[2]
print(f"Recibiendo el archivo {filename} de tamaño {filesize} MB.")

data = []
for i in range(partes):
	data.append( client.send_recv( '/' + str(i) ) )
	print(f"Progreso: {round(100*(i+1)/partes,2)}%")

data.append( client.send_recv('/' + str(partes)) )


if not os.path.exists(filename):
	with open(filename, "w") as r:
		r.write( ''.join(data) )

else:
	i = 1
	nombre, ext = filename.rsplit('.', 1)
	while os.path.exists(nombre + '-' + str(i) + '.' + ext):
		i += 1
	with open(nombre + '-' + str(i) + '.' + ext, "w") as r:
		r.write(''.join(data))
