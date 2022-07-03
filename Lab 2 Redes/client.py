from rudp import RUDPClient


client = RUDPClient("localhost", 25565)
archivos = client.send_recv('~')

print('(carpeta): Moverse a la carpeta')
print('(archivo): Descargar archivo')
print('..       : Retroceder')
print('~        : Volver al inicio')
print('close    : Salir')
print()


while True:
	print( '    '.join(archivos) )
	accion = input()
	print()

	if accion in ['..', '~']:
		archivos = client.send_recv( accion )
		
	elif accion in archivos:
		if accion.split('.')[-1] in ['txt', 'bin', 'py']:
			client.send_recv( accion )
			break
			# pasar a recivir archivo
		else: 
			archivos = client.send_recv( accion )

	elif accion == 'close':
		break

	

