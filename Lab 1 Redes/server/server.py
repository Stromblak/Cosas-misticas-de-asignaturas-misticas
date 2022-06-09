import socket
import encriptacion as enc

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

				if modo == 1: data = enc.decrypt_sim( c.recv(512) ).split("|", 3)
				if modo == 2: data = enc.decrypt_asim( c.recv(512) ).split("|", 3)
				filename = data.pop(0)
				filesize = float(data.pop(0))
				total = int(data.pop(0))
				filepath = "server\\" + filename
				recibido = len(data[0])

				print(f"Recibiendo el archivo {filename} de tamaño {filesize} MB.")
				print(f"Progreso: {round(100*recibido/total,2)}%")	
				while True:
					buffer = c.recv(512)
					if not buffer:
						break
					
					if modo == 1: bufferDec = enc.decrypt_sim(buffer)
					if modo == 2: bufferDec = enc.decrypt_asim(buffer)
					data.append(bufferDec)
					recibido += len(bufferDec)

					print(f"Progreso: {round(100*recibido/total,2)}%")

				with open(filepath, "w") as r:
					r.write(''.join(data))

				print(f"Conexion finalizada\n")