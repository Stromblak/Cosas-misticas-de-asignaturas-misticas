from rudp import RUDPClient
import sys


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


print(f"Recibiendo el archivo {info[0]} de tamaño {info[1]} MB.")
	

