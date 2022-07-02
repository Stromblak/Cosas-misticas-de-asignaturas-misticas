from cliente import client
from server import server
import os

host = 'localhost'
port = 25565

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
    archivo = input("Ingresar el nombre del archivo que se permitira descargar: ")

    while not os.path.exists("server\\" + archivo):
        print("Archivo no encontrado")
        archivo = input("Ingresar nombre de archivo: ")
    print()
    server.server(host, port, cifrado, archivo)
if modo == 2:
    client.client(host, port, cifrado)
