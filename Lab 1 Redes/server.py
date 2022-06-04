import socket


def server(host, port):
    print("Servidor inicializado")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind socket, con la direccion y el puerto
        s.bind((host, port))
        # Listen
        print("Esperando la conexion")
        s.listen()

        while True:
            clientsocket, address = s.accept()

            with clientsocket as c:
                print(f"Conexion entrante: {address}")

                filename, size, = c.recv(1024).decode().split()
                size = int(size)
                print(
                    f"Recibiendo el archivo {filename} con tamaño de {size} bytes ({round(size / (1024 * 1024),3)} MB).")

                data = []
                tamActual = 0
                while True:
                    buffer = c.recv(1024)
                    if not buffer:
                        break
                    data.append(buffer)
                    tamActual += len(buffer)
                    print(f"{round(100*tamActual/size,2)}/100% completado")
                    # forma fea de ver el progreso
                    c.sendall(str(tamActual).encode())
                print("100%/100% completado. Archivo recibido")

                with open("recv" + filename, "w") as r:
                    r.write(b''.join(data).decode())

                print(f"Conexion finalizada: {address}\n")
