import socket
import os

HOST = socket.gethostname()
PORT = 80  

# Archivo, nombre y tamaño
# filename = input("Nombre del archivo: ")
filename = "data.txt"
filesize = os.path.getsize(filename)

with open(filename, "r") as f:
    contents = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Estableciendo la conexion...")
    s.connect((HOST, PORT))
    print("Conexion exitosa!")
    # Enviar mensaje
    print(
        f"Enviando el archivo {filename} con tamaño de {filesize} bytes/{filesize / (1024 * 1024)} MB.")
    s.sendall(filename.encode())
    s.recv(1024)
    s.sendall(str(filesize).encode())
    s.recv(1024)
    s.sendall(contents.encode())
    print("Mensaje enviado con exito.")

