import socket

HOST = socket.gethostname()
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()

	while True:
		clientsocket, address = s.accept()

		with clientsocket as c:
			print(f"Conexion entrante: {address}")

			filename, size = c.recv(1024).decode().split()
			size = int(size)

			data = []
			tamActual = 0
			while True:
				buffer = c.recv(1024)
				if not buffer:
					break
				data.append(buffer)
				# como es inmutable el tipo byte, es cuadratico hacer data += buffer
				# por crear un nuevo data, haciendo el join(data) es lineal

				# la suma total de esto no da el tamano del archivo
				tamActual += len(buffer)
				print(tamActual, '/', size)

			with open("recv" + filename, "w") as r:
				r.write(b''.join(data).decode())
			
			print(f"Conexion finalizada: {address}")
