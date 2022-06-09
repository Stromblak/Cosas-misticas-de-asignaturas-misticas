from cliente import client
from server import server
import socket
import os

host = socket.gethostname()
port = 800

print("1: Servidor")
print("2: Cliente")
modo = int(input("Ingresar modo: "))

while modo != 1 and modo != 2:
    print("Input incorrecto")
    modo = int(input("Ingresar modo: "))
print()

print("0: Sin encriptacion")
print("1: Encriptacion simetrica")
print("2: Encriptacion asimetrica")
cifrado = int(input("Ingresar tipo de encriptacion: "))

while cifrado != 1 and cifrado != 2 and cifrado != 0:
    print("Input incorrecto")
    cifrado = int(input("Ingresar tipo de encriptacion: "))
print()

if modo == 1:
    server.server(host, port, cifrado)
if modo == 2:
    archivo = input("Ingresar nombre de archivo: ")

    while not os.path.exists("cliente\\" + archivo):
        print("Archivo no encontrado")
        archivo = input("Ingresar nombre de archivo: ")
    print()

    client.client(host, port, cifrado, archivo)
