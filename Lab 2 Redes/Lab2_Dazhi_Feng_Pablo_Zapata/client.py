from rudp import RUDPClient
import sys
import os


def printBonito(lista):
    maxlen = max(len(a) for a in lista) + 4
    capacidad = 90//maxlen + 1

    for i in range(0, len(lista), capacidad):
        print(' ' + ''.join(f'{l:<{maxlen}}' for l in lista[i:i+capacidad]))


client = RUDPClient("localhost", 25565, input('Ingresar clave: '))
ROOT = client.send_recv(('root', ''))
dir = [ROOT]

print('Cliente inicializado')
print('(carpeta): Moverse a la carpeta')
print('(archivo): Descargar archivo')
print('..       : Retroceder')
print('~        : Volver al inicio')
print('/close   : Salir')

while True:
    print('\n')
    carpetas, archivos = client.send_recv(('search', dir))
    if carpetas:
        print('Carpetas:')
        printBonito(carpetas)
        print()
    if archivos:
        print('Archivos:')
        printBonito(archivos)

    accion = input(' ')
    if accion == '..' and dir[-1] != ROOT:
        dir.pop()

    elif accion == '~':
        dir = [ROOT]

    elif accion == '/close':
        sys.exit(1)

    elif accion in archivos:
        dir.append(accion)
        break

    elif accion in carpetas:
        dir.append(accion)

filename, filesize, partes = client.send_recv(('info', dir))
print(f"\nDescargando el archivo {filename} de tamaño {filesize} MB.")

data = []
CotaPorcentaje = 1
for i in range(partes):
    data.append(client.send_recv(('send', (i, dir))))

    if round(100*(i+1)/partes, 2) >= CotaPorcentaje:
        print(f"Progreso: {round(100*(i+1)/partes, 2)}%")
        CotaPorcentaje += 1


if not os.path.exists(filename):
    with open(filename, "w") as r:
        r.write(''.join(data))
else:
    i = 1
    nombre, ext = filename.rsplit('.', 1)
    nombre, ext = nombre + '-', '.' + ext
    while os.path.exists(nombre + str(i) + ext):
        i += 1

    with open(nombre + str(i) + ext, "w") as r:
        r.write(''.join(data))
