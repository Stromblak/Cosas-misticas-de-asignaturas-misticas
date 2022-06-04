import socket
import os

HOST = socket.gethostname()
PORT = 80  # este puerto me pide permisos de admin xd

# Archivo, nombre y tamaño
# filename = input("Nombre del archivo: ")
#ext = os.path.splitext(filename)[1]
#size = os.path.getsize(filename)
filename = "data.txt"
filesize = os.stat(filename).st_size
with open(filename, "r") as f:
    contents = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Estableciendo la conexion...")
    s.connect((HOST, PORT))
    print("Conexion exitosa!")
    # Enviar mensaje
    print(
        f"Enviando el archivo {filename} con tamaño de {filesize} bytes/{filesize / (1024 * 1024)} MB.")
    s.sendall(contents.encode())
    print("Mensaje enviado con exito.")

# los with hacen que no sea necesario poner los close
# hay que meter else cuando no funciona algo creo