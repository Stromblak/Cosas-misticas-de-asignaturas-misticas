import sys
import pandas as pd

args = sys.argv[1:]
instancia = args[0];
modelo = args[1];


def leerInstancia():
    archivo = open(instancia, "r")

    # procesar datos


    info = [ [] for i in range(8) ]

    nLinea = 0;
    for linea in archivo:
        cosas = linea.split()

        if nLinea == 0:
            tipo, vehiculos, clientes, depositos = map(int, cosas)

        elif nLinea <= depositos:
            1

        elif nLinea <= depositos + clientes:
            for i in range(7):
                info[i].append( float(cosas[i]) )

            ##info[8].append( cosas[8:] )

        elif nLinea <= clientes + depositos + depositos:
            for i in range(7):
                info[i].append( float(cosas[i]) )

        nLinea += 1


    df = pd.DataFrame({
        'CUST NO': info[0],
        'x': info[1],
        'y': info[2],
        'duracionServicio': info[3],
        'demanda': info[4],
        'frecuenciaVisita': info[5],
        'numeroCombinacionesVisitas': info[6],
        'lista': info[7]
    })

    print(df)

leerInstancia()