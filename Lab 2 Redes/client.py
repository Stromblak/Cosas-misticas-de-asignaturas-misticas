#!/usr/bin/env python3
import sys
import os

from rudp import RUDPClient


def main():
    client = RUDPClient("localhost", 10000)

    try:
        reply = client.send_recv(b"hola")

        print(reply)
    except:
        print("no response; giving up", file=sys.stderr)

        # Necesitamos usar os._exit en lugar de sys.exit,
        # pues el proceso de esperar una respuesta del servidor
        # utiliza hilos y la salida "forzosa" que nos ofrece
        # os._exit mata esos hilos a la vez que mata el proceso
        # principal
        os._exit(1)


if __name__ == "__main__":
    main()
