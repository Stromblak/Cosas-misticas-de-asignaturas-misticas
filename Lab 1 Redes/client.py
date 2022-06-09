import socket
import os
import encriptacion as enc

def client(host, port, filename, modo):
	print("Cliente inicializado")

	with open(filename, "r") as f:
		contenido = f.read()

	total = len(contenido)
	filesize = round(os.path.getsize(filename) / (1024 * 1024), 3)
	stats = str(filename) + '|' + str(filesize) + '|' + str(total) + '|'
	contenido = stats + contenido

	total = 0
	data = []
	if modo == 1: n = 512
	if modo == 2: n = 496

	for i in range(0, len(contenido), n):
		if modo == 1: dataEnc = enc.encrypt_sim(contenido[i:i+n])
		if modo == 2: dataEnc = enc.encrypt(contenido[i:i+n])
		total += len(dataEnc)
		data.append( dataEnc )


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