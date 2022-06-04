import socket


def server(host, port):
    print("Servidor inicializado")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind socket, con la direccion y el puerto
        s.bind((host, port))
        # Listen
        s.listen()
        print("Esperando la conexion")

        while True:
            clientsocket, address = s.accept()

            with clientsocket as c:
                print(f"Conexion entrante: {address}")

                filename, size, = c.recv(1024).decode().split()
                size = int(size)

                print(f"Nombre y tamaño del archivo recibido: {filename}, {size} bytes")
				
                data = []
                tamActual = 0
                while True:
                    buffer = c.recv(1024)
                    if not buffer:
                        break
                    data.append(buffer)
                    # como es inmutable el tipo byte, es cuadratico hacer data += buffer
                    # por crear un nuevo data, haciendo el join(data) es lineal

                    # la suma total de esto no da el tamano del archivo
                    tamActual += len(buffer)
                    print(f"{round(100*tamActual/size,2)}/100% completado")
                print("100%/100% completado. Archivo recibido")

                with open("recv" + filename, "w") as r:
                    r.write(b''.join(data).decode())

                print(f"Conexion finalizada: {address}\n")