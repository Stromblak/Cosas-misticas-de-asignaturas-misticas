from pstats import Stats
import socket
import os

HOST = socket.gethostname()
PORT = 80

# filename = input("Nombre del archivo: ")
filename = "data.txt"
size = os.path.getsize(filename)

stats = str(filename) + ' ' + str(size)

with open(filename, "r") as f:
	contents = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	
	# Enviar mensaje
	print("Enviando el archivo", filename, "con tamaño", size)
	s.sendall(stats.encode())
	s.sendall(contents.encode())