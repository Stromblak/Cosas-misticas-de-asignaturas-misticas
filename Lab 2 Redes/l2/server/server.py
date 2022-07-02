import socket
import encriptacion as enc
import os
from rudp import RUDPServer


def server(host, port, modo):
    print("Servidor inicializado")

    server = RUDPServer(host, port)
    print("Esperando conexiones")

    while True:
        c, address = server.receive()
        server.reply(address, b"Recibido exitosamente.")
        print(f"Conexion entrante: {address}")

        if modo == 0:
            try:
                data = c.decode().split("|", 3)
            except:
                print("Error al procesar el archivo, cerrando servidor")
                return

        if modo == 1:
            clave = input("Ingresar clave: ")
            try:
                data = enc.decrypt_sim(
                    c, clave).split("|", 3)
            except:
                print("Clave incorrecta, cerrando servidor")
                return

        if modo == 2:
            try:
                data = enc.decrypt_asim(c).split("|", 3)
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
                buffer, address = server.receive()
                server.reply(address, b"Recibido exitosamente.")
            except:
                print("Error al recibir el archivo, cerrando servidor")
                return

            if not buffer:
                server.reply(address, b"Recibido exitosamente.")
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
