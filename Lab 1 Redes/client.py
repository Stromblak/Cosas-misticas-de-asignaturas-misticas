# copy paste de https://realpython.com/python-sockets/
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
# le agregue pa leer archivos nomas
filename = input("Nombre del archivo: ")
with open(filename, "r") as f:
    contents = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(contents.encode())
    data = s.recv(1024)

print(f"Received {data!r}")
