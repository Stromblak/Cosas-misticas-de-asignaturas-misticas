from rudp import RUDPClient
import sys
import os


client = RUDPClient("localhost", 25565, 'key')

ROOT = client.send_recv( ('root', '') )
dir = [ROOT]
carpetas, archivos = client.send_recv( ('search', dir) )

print('(carpeta): Moverse a la carpeta')
print('(archivo): Descargar archivo')
print('..       : Retroceder')
print('~        : Volver al inicio')
print('close    : Salir')
print()

# si son muchos archivos aqui es una linea gigante
while True:
	if len(carpetas):
		print('Carpetas:')
		print( '    '.join(carpetas) )
		print()
	if len(archivos):
		print('Archivos:')
		print( '    '.join(archivos) )

	accion = input()
	print('\n')

	if accion == '..' and dir[-1] != ROOT:
		dir.pop()

	elif accion == '~':
		dir = [ROOT]

	elif accion == 'close':
		sys.exit(1)

	elif accion in archivos:
		dir.append(accion)
		info = client.send_recv( ('info', dir) )
		break

	elif accion in carpetas:
		dir.append(accion)

	carpetas, archivos = client.send_recv( ('search', dir) )


filename = info[0]
print(f"Descargando el archivo {filename} de tamaño {info[1]} MB.")

data = []
for i in range(info[2]):
	data.append( client.send_recv( ('send', (i, dir)) ) )
	print(f"Progreso: {round(100*(i+1)/info[2], 2)}%")


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
