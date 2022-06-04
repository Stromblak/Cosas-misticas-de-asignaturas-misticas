import client
import server
import socket

HOST = socket.gethostname()
PORT = 80

print("1: Servidor")
print("2: Cliente")
modo = int(input())

if modo == 1:
	server.server(HOST, PORT)
elif modo == 2:
	client.client(HOST, PORT)

# esto lo hice porque lei que era un solo programa, y luego me di cuenta que decia
# que se podia hacer un ejecutable junto o separado xd
# no se si lo prefieres asi