import socket
import os

def client(host, port, filename):
	print("Cliente inicializado")

	with open(filename, "r") as f:
		contenido = f.read()

	filesize = round(os.path.getsize(filename) / (1024 * 1024), 3)
	total = len(contenido)
	stats = str(filename) + '|' + str(filesize) + '|' + str(total) + '|'
	contenido = stats + contenido

	# separo el contenido en pedacitos de tamano 1024
	data = [contenido[i:i+1024] for i in range(0, len(contenido), 1024)]

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("Estableciendo la conexion...")
		s.connect((host, port))
		print("Conexion exitosa!")

		# Enviar mensaje
		print(f"Enviando el archivo {filename} de tamaño {filesize} MB.")

		enviado = -len(stats)
		for d in data:
			# envio los pedacitos
			s.sendall(d.encode())
			enviado += len(d)
			print(f"Progreso: {round(100*enviado/total,2)}%")