import socket

HOST = socket.gethostname()
PORT = 80

# filename = input("Nombre del archivo: ")
filename = "data.txt"

with open(filename, "r") as f:
	contents = f.read()
	f.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(contents.encode())
	s.close()						# termina la conexion
