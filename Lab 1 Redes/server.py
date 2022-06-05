import socket
#	podi usar tabs en vez de espacios o me cambio yo?
#	porque me anda webeando esta cosa dsadas

def server(host, port):
	print("Servidor inicializado")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Bind socket, con la direccion y el puerto
		s.bind((host, port))
		# Listen
		s.listen()
		print("Esperando la conexion")

		while True:
			clientsocket, address = s.accept()

			with clientsocket as c:
				print(f"Conexion entrante: {address}")

				data = c.recv(50).split(b"|", 2)
				filename = data[0].decode()
				size = int(data[1].decode())
				data.pop(0)
				data.pop(0)


				mb = round(size / (1024 * 1024), 3)
				print(f"Recibiendo el archivo {filename} de tamaño {mb} MB.")

				recibido = len(data[0])
				while True:
					buffer = c.recv(1024)
					if not buffer:
						break
					data.append(buffer)
					recibido += len(buffer)
					print(f"Progreso: {round(100*recibido/size,2)}%")
				print("Progreso: 100%")

				with open("recv" + filename, "w") as r:
					r.write(b''.join(data).decode())

				print(f"Conexion finalizada\n")