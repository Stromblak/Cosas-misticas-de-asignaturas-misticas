import socket

HOST = socket.gethostname()
PORT = 80

# Crear socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind socket, con la direccion y el puerto
    s.bind((HOST, PORT))
    # Listen
    s.listen()

    while True:
        print("Esperando la conexion")
        clientsocket, address = s.accept()

        with clientsocket as c:
            print(f"Conexion entrante: {address}")

            # me daba error el split
            filename = c.recv(1024).decode()
            print(f"Nombre del archivo recibido: {filename}")
            c.send(b'aux')
            filesize = int(c.recv(1024).decode())
            print(f"Tamaño del archivo recibido: {filesize}")
            c.send(b'aux')

            data = []
            tamActual = 0
            while True:
                buffer = c.recv(filesize)
                if not buffer:
                    break
                data.append(buffer)
                # como es inmutable el tipo byte, es cuadratico hacer data += buffer
                # por crear un nuevo data, haciendo el join(data) es lineal

                # la suma total de esto no da el tamano del archivo
                tamActual += len(buffer)
                print(tamActual, '/', filesize)

            with open("recv" + filename, "w") as r:
                r.write(b''.join(data).decode())

            print(f"Conexion finalizada: {address}")
