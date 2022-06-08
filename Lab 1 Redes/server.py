import socket
import encriptacion as enc

#	podi usar tabs en vez de espacios o me cambio yo?
#	porque me anda webeando esta cosa con la indentacion dsadasdsa

def server(host, port, modo):
	print("Servidor inicializado")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Bind socket, con la direccion y el puerto
		s.bind((host, port))
		# Listen
		s.listen()
		print("Esperando conexiones")

		while True:
			clientsocket, address = s.accept()

			with clientsocket as c:
				print(f"Conexion entrante: {address}")

				if modo == 1:
					1
				if modo == 2:
					data = enc.decrypt( c.recv(512) ).split("|", 3)

				filename = data.pop(0)
				filesize = float( data.pop(0))
				total = int( data.pop(0))

				print(f"Recibiendo el archivo {filename} de tamaño {filesize} MB.")
				recibido = len(data[0])
				while True:
					buffer = c.recv(512)
					if not buffer:
						break
					
					if modo == 1:
						1
					if modo == 2:
						bufferDec = enc.decrypt( buffer )
						data.append(bufferDec)
						recibido += len(bufferDec)

					print(f"Progreso: {round(100*recibido/total,2)}%")

				with open("recv" + filename, "w") as r:
					r.write(''.join(data))

				print(f"Conexion finalizada\n")