import socket
import os
import encriptacion as enc
import math

def client(host, port, filename, modo):
	print("Cliente inicializado")

	with open(filename, "r") as f:
		contenido = f.read()

	total = len(contenido)
	filesize = round(os.path.getsize(filename) / (1024 * 1024), 3)
	stats = str(filename) + '|' + str(filesize) + '|' + str(total) + '|'
	contenido = stats + contenido

	if modo == 1:
		1
	if modo == 2:
		# separo el contenido en pedacitos de tamano n
		# encripar los deja en tamano 512
		n = 496
		data = []
		total = math.ceil( len(contenido)/n )*512

		for i in range(0, len(contenido), n):
			data.append( enc.encrypt(contenido[i:i+n]) )

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("Estableciendo la conexion... ", end = '')
		s.connect((host, port))
		print("Conexion exitosa!")

		# Enviar mensaje
		print(f"Enviando el archivo {filename} de tamaño {filesize} MB.")

		enviado = 0
		for d in data:
			
			s.sendall(d)
			enviado += len(d)
			print(f"Progreso: {round(100*enviado/total,2)}%")