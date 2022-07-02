from asyncio.windows_events import NULL
import socket
import os
import sys
import encriptacion as enc
from rudp import RUDPClient


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

    print("Estableciendo la conexion... ", end='')
    c = RUDPClient(host, port)
    
    print("Conexion exitosa!")
    print(f"Enviando el archivo {filename} de tamaño {filesize} MB.")
    enviado = 0

    for d in data:
        try:
            reply = c.send_recv(d)
            print(reply)
        except:
            print("no response; giving up", file=sys.stderr)
            os._exit(1)

        enviado += len(d)
        if round(100*enviado/total, 2) >= p:
            p += 1
            print(f"Progreso: {round(100*enviado/total,2)}%")

    reply = c.send_recv(NULL)
    print(reply)    
