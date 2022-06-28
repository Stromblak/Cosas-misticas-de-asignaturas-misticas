#!/usr/bin/env python3

from rudp import RUDPServer


def main():
	server = RUDPServer('localhost', 25565)

	while True:
		message, address = server.receive()

		print(message)

		server.reply(address, b"chao")
		break

if __name__ == "__main__":
	main()
