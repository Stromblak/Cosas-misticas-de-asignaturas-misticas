import socket
import os

def client(host, port):
	print("Cliente inicializado")

	# filename = input("Nombre del archivo: ")
	filename = "data.txt"
	size = os.path.getsize(filename)

	stats = str(filename) + ' ' + str(size)

	with open(filename, "r") as f:
		contents = f.read()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		
		s.sendall(stats.encode())	
		# esto no puede estar justo antes del otro send porque se juntan los mensajes
		# ni idea por que

		# Enviar mensaje
		print("Enviando el archivo", filename, "con tamaño", size)
		s.sendall(contents.encode())