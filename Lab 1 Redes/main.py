from cliente import client
from server import server
import socket

host = socket.gethostname()
port = 800

print("1: Servidor")
print("2: Cliente")
modo = int(input("Ingresar modo: "))
print()

print("1: Encriptacion simetrica")
print("2: Encriptacion asimetrica")
enc = int(input("Ingresar tipo de encriptacion: "))
print()

if modo == 1:
	server.server(host, port, enc)
elif modo == 2:
	archivo = input("Ingresar nombre de archivo: ")
	client.client(host, port, enc, archivo)
