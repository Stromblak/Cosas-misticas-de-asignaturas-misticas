import socket
import os


def client(host, port):
    print("Cliente inicializado")

    # filename = input("Nombre del archivo: ")
    filename = "data.txt"
    size = os.path.getsize(filename)
    stats = str(filename) + ' ' + str(size)

    with open(filename, "r") as f:
        contents = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Estableciendo la conexion...")
        s.connect((host, port))
        print("Conexion exitosa!")
        s.sendall(stats.encode())
        # esto no puede estar justo antes del otro send porque se juntan los mensajes
        # ni idea por que

        # Enviar mensaje
        print(
            f"Enviando el archivo {filename} con tamaño de {size} bytes ({round(size / (1024 * 1024),3)} MB).")
        s.sendall(contents.encode())
        print("Mensaje enviado con exito.")
