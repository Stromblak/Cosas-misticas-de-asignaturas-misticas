import socket
import os
import time


def client(host, port, filename):
	print("Cliente inicializado")

	size = os.path.getsize(filename)
	stats = str(filename) + ' ' + str(size) + ' '

	with open(filename, "r") as f:
		contents = f.read()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("Estableciendo la conexion...")
		s.connect((host, port))
		print("Conexion exitosa!")

		s.sendall(stats.encode())
		time.sleep(1)

		# Enviar mensaje
		print(f"Enviando el archivo {filename} con tamaño de {size} bytes ({round(size / (1024 * 1024),3)} MB).")
		s.sendall(contents.encode())
		print("Mensaje enviado con exito.")