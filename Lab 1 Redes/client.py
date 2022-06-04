import socket
import os


HOST = socket.gethostname()
PORT = 80

# filename = input("Nombre del archivo: ")
filename = "data.txt"
ext = os.path.splitext(filename)[1]
size = os.path.getsize(filename)

with open(filename, "r") as f:
    contents = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Enviar mensaje
    print("Enviando el archivo", filename, "con tamaño")
    s.sendall(contents.encode())



# los with hacen que no sea necesario poner los close
