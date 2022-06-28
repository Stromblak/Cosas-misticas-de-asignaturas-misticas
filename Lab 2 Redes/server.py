#!/usr/bin/env python3

from rudp import RUDPServer


def main():
    server = RUDPServer(10000)

    while True:
        message, address = server.receive()

        print(message)

        server.reply(address, b"chao")


if __name__ == "__main__":
    main()
