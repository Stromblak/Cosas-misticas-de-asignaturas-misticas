import os
import encriptacion as enc
from rudp import RUDPClient


def client(host, port, cifrado):
    print("Cliente inicializado")
    print("Estableciendo la conexion... ", end='')

    c = RUDPClient(host, port)
    print("Conexion exitosa!")

    reply = c.send_recv(f"Enviando el archivo...")

    if cifrado == 0:
        try:
            data = reply.decode().split("|", 3)
        except:
            print("Error al procesar el archivo, cerrando servidor")
            return

    if cifrado == 1:
        clave = input("Ingresar clave: ")
        try:
            data = enc.decrypt_sim(
                reply, clave).split("|", 3)
        except:
            print("Clave incorrecta, cerrando servidor")
            return

    if cifrado == 2:
        try:
            data = enc.decrypt_asim(reply).split("|", 3)
        except:
            print("Error al procesar el archivo, cerrando servidor")
            return

    filename = data.pop(0)
    filesize = float(data.pop(0))
    filepath = "cliente\\" + filename
    total = int(data.pop(0))
    recibido = len(data[0])

    print(
        f"Recibiendo el archivo {filename} de tamaño {filesize} MB.")
    print(f"Progreso: {round(100*recibido/total,2)}%")

    p = 1
    while True:
        try:
            buffer = c.send_recv(f"Progreso: {round(100*recibido/total,2)}%")

        except:
            print("Error al recibir el archivo, cerrando servidor")
            return

        if not buffer:
            break

        if cifrado == 0:
            bufferDec = buffer.decode()
        if cifrado == 1:
            bufferDec = enc.decrypt_sim(buffer, clave)
        if cifrado == 2:
            bufferDec = enc.decrypt_asim(buffer)
        data.append(bufferDec)
        recibido += len(bufferDec)

        if round(100*recibido/total, 2) >= p:
            p += 1
            print(f"Progreso: {round(100*recibido/total,2)}%")

    if not os.path.exists("cliente\\" + filename):
        with open(filepath, "w") as r:
            r.write(''.join(data))

    else:
        i = 1
        nombre, ext = filename.rsplit('.', 1)
        while os.path.exists("cliente\\" + nombre + '-' + str(i) + '.' + ext):
            i += 1
        with open("cliente\\" + nombre + '-' + str(i) + '.' + ext, "w") as r:
            r.write(''.join(data))

    print(f"Archivo recibido exitosamente.\n")
