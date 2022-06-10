import socket
import os
import encriptacion as enc


def client(host, port, cifrado, filename):
    print("Cliente inicializado")

    filepath = "cliente\\" + filename
    with open(filepath, "r") as f:
        contenido = f.read()

    total = len(contenido)
    filesize = round(os.path.getsize(filepath) / (1000 ** 2), 3)
    stats = str(filename) + '|' + str(filesize) + '|' + str(total) + '|'
    contenido = stats + contenido

    total = 0
    data = []
    n = 512
    if cifrado == 1:
        key = input("Ingrese la clave para cifrar: ")
    if cifrado == 2:
        n = 496

    p = 0
    for i in range(0, len(contenido), n):
        if cifrado == 0:
            dataEnc = contenido[i:i+n].encode()
        if cifrado == 1:
            dataEnc = enc.encrypt_sim(contenido[i:i+n], key)
        if cifrado == 2:
            dataEnc = enc.encrypt_asim(contenido[i:i+n])

        if round(100*i/len(contenido), 2) >= p:
            p += 1
            print(f"Codificando archivo: {round(100*i/len(contenido),2)}%")

        total += len(dataEnc)
        data.append(dataEnc)
    print("Codificando archivo: 100%\n")
    p = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Estableciendo la conexion... ", end='')
        if not s.connect_ex((host, port)):
            print("Conexion exitosa!")
        else:
            print("Conexion fallida")
            print("Cerrando cliente")
            return

        print(f"Enviando el archivo {filename} de tamaño {filesize} MB.")
        enviado = 0
        for d in data:
            try:
                s.sendall(d)
            except socket.error:
                print("Error enviando el archivo")
                print("Cerrando cliente")
                return

            enviado += len(d)

            if round(100*enviado/total, 2) >= p:
                p += 1
                print(f"Progreso: {round(100*enviado/total,2)}%")
