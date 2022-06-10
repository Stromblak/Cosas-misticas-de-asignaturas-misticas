import socket
import encriptacion as enc
import os


def server(host, port, modo):
    print("Servidor inicializado")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Bind socket, con la direccion y el puerto, luego un listen
            s.bind((host, port))
            s.listen()
        except socket.error:
            print("Error en la creacion del servidor, cerrando programa")
            return

        print("Esperando conexiones")

        while True:
            clientsocket, address = s.accept()

            with clientsocket as c:
                print(f"Conexion entrante: {address}")

                if modo == 0:
                    try:
                        data = c.recv(512).decode().split("|", 3)
                    except:
                        print("Error al procesar el archivo, cerrando servidor")
                        return

                if modo == 1:
                    clave = input("Ingresar clave: ")
                    try:
                        data = enc.decrypt_sim(
                            c.recv(512), clave).split("|", 3)
                    except:
                        print("Clave incorrecta, cerrando servidor")
                        return

                if modo == 2:
                    try:
                        data = enc.decrypt_asim(c.recv(512)).split("|", 3)
                    except:
                        print("Error al procesar el archivo, cerrando servidor")
                        return

                filename = data.pop(0)
                filesize = float(data.pop(0))
                filepath = "server\\" + filename
                total = int(data.pop(0))
                recibido = len(data[0])

                print(
                    f"Recibiendo el archivo {filename} de tamaño {filesize} MB.")
                print(f"Progreso: {round(100*recibido/total,2)}%")

                p = 1
                while True:
                    try:
                        buffer = c.recv(512)
                    except socket.error:
                        print("Error al recibir el archivo, cerrando servidor")
                        return

                    if not buffer:
                        break

                    if modo == 0:
                        bufferDec = buffer.decode()
                    if modo == 1:
                        bufferDec = enc.decrypt_sim(buffer, clave)
                    if modo == 2:
                        bufferDec = enc.decrypt_asim(buffer)
                    data.append(bufferDec)
                    recibido += len(bufferDec)

                    if round(100*recibido/total, 2) >= p:
                        p += 1
                        print(f"Progreso: {round(100*recibido/total,2)}%")

                if not os.path.exists("server\\" + filename):
                    with open(filepath, "w") as r:
                        r.write(''.join(data))

                else:
                    i = 1
                    nombre, ext = filename.rsplit('.', 1)
                    while os.path.exists("server\\" + nombre + '-' + str(i) + '.' + ext):
                        i += 1
                    with open("server\\" + nombre + '-' + str(i) + '.' + ext, "w") as r:
                        r.write(''.join(data))

                print(f"Conexion finalizada\n")
