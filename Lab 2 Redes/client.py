from rudp import RUDPClient


client = RUDPClient("localhost", 25565)

print('(carpeta): Moverse a la carpeta')
print('(archivo): Descargar archivo')
print('..       : Retroceder')
print('~        : Volver al inicio')
print('close    : Salir')



archivos = client.send_recv('~')
print( archivos )

while True:
	accion = input()

	if accion in ['..', '~']:
		archivos = client.send_recv( accion )
		print( archivos )
	
	elif accion.split('.')[-1] in ['.txt', '.bin']:
		break
		# pasar a recivir archivo

	elif accion in archivos:
		archivos = client.send_recv( accion )
		print( archivos )

	elif accion == 'close':
		break
	
	else:
		print('Input incorrecto')
		continue

