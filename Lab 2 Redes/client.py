from rudp import RUDPClient
import sys
import os


client = RUDPClient("localhost", 25565, 'key')

ROOT = client.send_recv( ('', '') )
dir = [ROOT]
archivos = client.send_recv( ('search', dir) )

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

	match accion:
		case '..':
			if dir[-1] != ROOT:
				dir.pop()
		
		case '~':
			dir = [ROOT]

		case 'close':
			sys.exit(1)
		
		case archivos:
			dir.append(accion)
			if accion.split('.')[-1] in ['txt', 'bin', 'py']:
				info = client.send_recv( ('select', dir) )
				break

	archivos = client.send_recv( ('search', dir) )


filename = info[0]
filesize = info[1]
partes = info[2]
print(f"Descargando el archivo {filename} de tamaño {filesize} MB.")

data = []
for i in range(partes):
	data.append( client.send_recv( ('download', i) ) )
	print(f"Progreso: {round(100*(i+1)/partes,2)}%")

client.send_recv( ('fin', 1) )


if not os.path.exists(filename):
	with open(filename, "w") as r:
		r.write( ''.join(data) )

else:
	i = 1
	nombre, ext = filename.rsplit('.', 1)
	nombre, ext = nombre + '-', '.' + ext
	while os.path.exists(nombre + str(i) + ext):
		i += 1

	with open(nombre + str(i) + ext, "w") as r:
		r.write(''.join(data))
