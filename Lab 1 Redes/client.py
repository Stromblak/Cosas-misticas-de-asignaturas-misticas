import socket
import os

def client(host, port, filename):
	print("Cliente inicializado")

	size = os.path.getsize(filename)
	stats = str(filename) + '|' + str(size) + '|'

	with open(filename, "r") as f:
		contenido = stats + f.read()

	# separo el contenido en pedacitos de tamano 1024
	data = [contenido[i:i+1024] for i in range(0, len(contenido), 1024)]

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("Estableciendo la conexion...")
		s.connect((host, port))
		print("Conexion exitosa!")

		# Enviar mensaje
		mb = round(size / (1024 * 1024), 3)
		print(f"Enviando el archivo {filename} de tamaño {mb} MB.")

		enviado = 0
		for d in data:
			# envio los pedacitos, no estoy seguro del len pa ver lo enviado si si
			s.sendall(d.encode())
			enviado += len(d)
			print(f"Progreso: {round(100*enviado/size,2)}%")
		print(f"Progreso: 100%")