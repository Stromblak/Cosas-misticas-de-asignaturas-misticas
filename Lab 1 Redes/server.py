import socket

HOST = socket.gethostname()
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()

	while True:
		clientsocket, address = s.accept()
		
		with clientsocket:
			print(f"Conexion entrante: {address}")

			data = bytes()
			while True:
				buffer = clientsocket.recv(1024)
				if not buffer:
					break
				data += buffer
			
			with open( "recv.txt", "w") as r:
				r.write(data.decode())
				r.close()
			
			print(f"Conexion finalizada: {address}")
