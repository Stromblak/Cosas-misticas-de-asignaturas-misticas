from asyncio.windows_events import NULL
import sys
import encriptacion as enc
import os
from rudp import RUDPServer


def server(host, port, cifrado, filename):
    print("Servidor inicializado")

    filepath = "server\\" + filename
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

    s = RUDPServer(host, port)
    print("Esperando conexiones")
    print(f"Se enviara el archivo {filename} de tamaño {filesize} MB.")
    
    while True:
        message, address = s.receive()
        for d in data:
            try:
                s.reply(address, d)
            except:
                print("no response; giving up", file=sys.stderr)
                os._exit(1)
        s.reply(address, NULL)
        print(message)
    print(f"Conexion finalizada\n")
